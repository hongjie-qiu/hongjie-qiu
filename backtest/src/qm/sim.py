"""Trade-path simulator (numba) and portfolio simulator.

Conventions
-----------
* A signal is (t0, j, entry, stop): the position is opened on day t0 at price `entry`.
  `at_close=True` means the fill is the close of t0 (so day t0's own range cannot stop it);
  `at_close=False` means an intraday fill on day t0 (stop-entry or open), so day t0's range
  matters and the intraday order of events is unknown -> see `day0_mode`.
* Costs: `cost` is a fraction charged on every fill (entry, partial, final), e.g. 0.0015 = 15 bps.
* R multiple = net P&L per share / (entry - stop) for longs, / (stop - entry) for shorts.

Exit reasons: 0 initial/breakeven stop, 1 trailing-MA exit, 2 max holding period, 3 data ended
(delisting / end of sample), 4 stopped on the entry day, 5 profit target (shorts).
"""
import numpy as np
import numba as nb


@nb.njit(cache=True)
def simulate_longs(O, H, L, C, MA, t0s, js, entries, stops, at_close, day0_mode,
                   part_day, part_frac, be_after_part, max_hold, cost):
    """Simulate long trades.

    day0_mode (intraday entries only):
        0 = optimistic  - day-0 low is assumed to have printed before the entry (never stops day 0)
        1 = pessimistic - if day-0 low <= stop the trade is stopped on day 0
        2 = close-based - stopped on day 0 only if the day-0 close finished below the stop
    Exits: stop (gap-aware), optional partial at the first profitable close on/after `part_day`
    sessions (then stop -> breakeven if be_after_part), trailing exit at the next open after a
    close below MA, time stop.
    """
    n = len(t0s)
    T = C.shape[0]
    exit_day = np.zeros(n, dtype=np.int32)
    part_dayo = np.full(n, -1, dtype=np.int32)
    part_px = np.full(n, np.nan)
    final_px = np.full(n, np.nan)
    ret = np.full(n, np.nan)
    rmult = np.full(n, np.nan)
    reason = np.full(n, -1, dtype=np.int8)
    hold = np.zeros(n, dtype=np.int32)
    mfe = np.full(n, np.nan)
    for k in range(n):
        t0 = t0s[k]
        j = js[k]
        entry = entries[k]
        stop = stops[k]
        risk = entry - stop
        if not (risk > 0 and np.isfinite(entry)):
            continue
        frac = 1.0
        realized = 0.0
        cur_stop = stop
        pending = False
        done = False
        best = entry
        d = t0
        last_c = entry
        last_d = t0
        if not at_close:
            lo = L[t0, j]
            c0 = C[t0, j]
            hi = H[t0, j]
            if hi > best:
                best = hi
            hit = False
            if day0_mode == 1 and lo <= cur_stop:
                hit = True
            elif day0_mode == 2 and c0 < cur_stop:
                hit = True
            if hit:
                realized = frac * cur_stop * (1.0 - cost)
                frac = 0.0
                exit_day[k] = t0
                final_px[k] = cur_stop
                reason[k] = 4
                done = True
            else:
                last_c = c0
                m = MA[t0, j]
                if np.isfinite(m) and c0 < m:
                    pending = True
        nheld = 0
        miss = 0
        while not done:
            d += 1
            if d >= T:
                realized += frac * last_c * (1.0 - cost)
                exit_day[k] = last_d
                final_px[k] = last_c
                reason[k] = 3
                break
            o = O[d, j]
            c = C[d, j]
            if not (np.isfinite(o) and np.isfinite(c)):
                miss += 1
                if miss > 10:  # ticker stopped printing: exit at the last known close
                    realized += frac * last_c * (1.0 - cost)
                    exit_day[k] = last_d
                    final_px[k] = last_c
                    reason[k] = 3
                    break
                continue
            miss = 0
            nheld += 1
            h = H[d, j]
            l = L[d, j]
            if pending:
                realized += frac * o * (1.0 - cost)
                exit_day[k] = d
                final_px[k] = o
                reason[k] = 1
                break
            if l <= cur_stop:
                px = cur_stop if o > cur_stop else o
                realized += frac * px * (1.0 - cost)
                exit_day[k] = d
                final_px[k] = px
                reason[k] = 0
                break
            if h > best:
                best = h
            if part_frac > 0.0 and frac == 1.0 and nheld >= part_day and c > entry:
                realized += part_frac * c * (1.0 - cost)
                frac -= part_frac
                part_dayo[k] = d
                part_px[k] = c
                if be_after_part and entry > cur_stop:
                    cur_stop = entry
            last_c = c
            last_d = d
            m = MA[d, j]
            if np.isfinite(m) and c < m:
                pending = True
            if nheld >= max_hold:
                realized += frac * c * (1.0 - cost)
                exit_day[k] = d
                final_px[k] = c
                reason[k] = 2
                break
        cost_entry = entry * (1.0 + cost)
        pnl = realized - cost_entry
        ret[k] = pnl / cost_entry
        rmult[k] = pnl / risk
        hold[k] = exit_day[k] - t0
        mfe[k] = (best - entry) / risk
    return exit_day, part_dayo, part_px, final_px, ret, rmult, reason, hold, mfe


@nb.njit(cache=True)
def simulate_shorts(O, H, L, C, MA, t0s, js, entries, stops, at_close, day0_mode,
                    use_target, max_hold, cost, borrow_daily):
    """Simulate short trades.

    Exits: stop above (gap-aware), optional profit target = cover when price trades down to the
    previous day's MA value, time stop.  If stop and target are both touched in one bar the stop is
    assumed to come first.  `borrow_daily` is charged on the entry notional per calendar row held.
    day0_mode as in simulate_longs but mirrored (uses the day-0 high).
    """
    n = len(t0s)
    T = C.shape[0]
    exit_day = np.zeros(n, dtype=np.int32)
    final_px = np.full(n, np.nan)
    ret = np.full(n, np.nan)
    rmult = np.full(n, np.nan)
    reason = np.full(n, -1, dtype=np.int8)
    hold = np.zeros(n, dtype=np.int32)
    for k in range(n):
        t0 = t0s[k]
        j = js[k]
        entry = entries[k]
        stop = stops[k]
        risk = stop - entry
        if not (risk > 0 and np.isfinite(entry)):
            continue
        px_out = np.nan
        done = False
        d = t0
        last_c = entry
        last_d = t0
        if not at_close:
            hi = H[t0, j]
            c0 = C[t0, j]
            hit = False
            if day0_mode == 1 and hi >= stop:
                hit = True
            elif day0_mode == 2 and c0 > stop:
                hit = True
            if hit:
                px_out = stop
                exit_day[k] = t0
                reason[k] = 4
                done = True
            else:
                last_c = c0
        nheld = 0
        miss = 0
        while not done:
            d += 1
            if d >= T:
                px_out = last_c
                exit_day[k] = last_d
                reason[k] = 3
                break
            o = O[d, j]
            c = C[d, j]
            if not (np.isfinite(o) and np.isfinite(c)):
                miss += 1
                if miss > 10:
                    px_out = last_c
                    exit_day[k] = last_d
                    reason[k] = 3
                    break
                continue
            miss = 0
            nheld += 1
            h = H[d, j]
            l = L[d, j]
            if h >= stop:
                px_out = stop if o < stop else o
                exit_day[k] = d
                reason[k] = 0
                break
            if use_target:
                tgt = MA[d - 1, j]
                if np.isfinite(tgt) and tgt < entry and l <= tgt:
                    px_out = tgt if o > tgt else o
                    exit_day[k] = d
                    reason[k] = 5
                    break
            last_c = c
            last_d = d
            if nheld >= max_hold:
                px_out = c
                exit_day[k] = d
                reason[k] = 2
                break
        final_px[k] = px_out
        hold[k] = exit_day[k] - t0
        proceeds = entry * (1.0 - cost)
        cover = px_out * (1.0 + cost)
        pnl = proceeds - cover - borrow_daily * entry * max(hold[k], 1)
        ret[k] = pnl / entry
        rmult[k] = pnl / risk
    return exit_day, final_px, ret, rmult, reason, hold


def portfolio_sim(trades, C, dates, start_equity=100_000.0, risk_pct=0.005, max_pos_w=0.20,
                  max_gross=1.0, max_positions=20, cost=0.0015, direction=1, min_w=0.01,
                  dv20=None, max_dv_frac=None, borrow_daily=0.0, start_idx=0):
    """Event-driven portfolio simulation on pre-computed trade paths.

    `trades` is a dict of equal-length arrays: t0, j, entry, stop, exit_day, final_px, prio and, for
    longs, part_day (-1 if none), part_px, part_frac.  Signals on the same day are taken in
    descending `prio` until a constraint binds.  Sizing: shares = risk_pct * equity / |entry-stop|,
    capped by max_pos_w * equity, by remaining gross exposure and (optionally) by a fraction of the
    stock's 20-day average dollar volume.  Equity is marked to market at each close.
    `borrow_daily` (shorts) is charged every day on the market value of open positions.
    Days before `start_idx` are skipped (equity stays at start_equity).
    Returns (equity array, list of taken-trade indices, exposure array).
    """
    T = len(dates)
    Cf = np.array(C, dtype=np.float64, copy=True)
    # forward-fill closes for marking positions on days without a print
    for i in range(1, T):
        row = Cf[i]
        prev = Cf[i - 1]
        nanmask = ~np.isfinite(row)
        row[nanmask] = prev[nanmask]
    n = len(trades["t0"])
    order = np.lexsort((-trades["prio"], trades["t0"]))
    by_day = {}
    for k in order:
        by_day.setdefault(int(trades["t0"][k]), []).append(int(k))
    cash = start_equity
    equity = np.full(T, np.nan)
    gross_exp = np.zeros(T)
    open_pos = {}  # k -> shares currently held (signed by direction)
    exits_on = {}  # day -> list of (k, kind) with kind 'p' partial or 'f' final
    taken = []
    prev_eq = start_equity
    has_part = "part_day" in trades
    for i in range(T):
        if i < start_idx:
            equity[i] = start_equity
            continue
        # 1) exits scheduled today for positions opened earlier
        for k, kind in exits_on.pop(i, []):
            sh = open_pos.get(k)
            if sh is None:
                continue
            if kind == "p":
                q = sh * trades["part_frac"][k]
                px = trades["part_px"][k]
                open_pos[k] = sh - q
            else:
                q = sh
                px = trades["final_px"][k]
                del open_pos[k]
            cash += direction * q * px - abs(q) * px * cost
        # 2) entries
        for k in by_day.get(i, []):
            if len(open_pos) >= max_positions:
                break
            entry = trades["entry"][k]
            risk = abs(entry - trades["stop"][k])
            if not (risk > 0):
                continue
            gross_now = sum(abs(s) * Cf[i - 1 if i > 0 else 0, trades["j"][kk]] for kk, s in open_pos.items())
            room = max_gross * prev_eq - gross_now
            dollars = min(risk_pct * prev_eq / risk * entry, max_pos_w * prev_eq, room)
            if dv20 is not None and max_dv_frac is not None and i > 0:
                liq = dv20[i - 1, trades["j"][k]]
                if np.isfinite(liq):
                    dollars = min(dollars, max_dv_frac * liq)
            if dollars < min_w * prev_eq:
                continue
            sh = dollars / entry
            cash -= direction * sh * entry + sh * entry * cost
            open_pos[k] = sh
            taken.append(k)
            xd = int(trades["exit_day"][k])
            if has_part and trades["part_day"][k] >= 0:
                pd_ = int(trades["part_day"][k])
                if pd_ == i:
                    q = sh * trades["part_frac"][k]
                    cash += direction * q * trades["part_px"][k] - q * trades["part_px"][k] * cost
                    open_pos[k] = sh - q
                else:
                    exits_on.setdefault(pd_, []).append((k, "p"))
            if xd == i:  # stopped on the entry day
                q = open_pos.pop(k)
                cash += direction * q * trades["final_px"][k] - q * trades["final_px"][k] * cost
            else:
                exits_on.setdefault(xd, []).append((k, "f"))
        # 3) mark to market
        mv = 0.0
        g = 0.0
        for k, sh in open_pos.items():
            px = Cf[i, trades["j"][k]]
            if not np.isfinite(px):
                px = trades["entry"][k]
            mv += direction * sh * px
            g += abs(sh) * px
        if borrow_daily:
            cash -= borrow_daily * g
        eq = cash + mv
        equity[i] = eq
        gross_exp[i] = g / eq if eq > 0 else np.nan
        prev_eq = eq
    return equity, np.array(taken, dtype=np.int64), gross_exp


def perf_stats(equity, dates, rf_daily=None):
    """CAGR, annualised vol, Sharpe (excess of rf if given), max drawdown, worst year, Calmar."""
    eq = np.asarray(equity, dtype=np.float64)
    ok = np.isfinite(eq)
    eq = eq[ok]
    d = dates[ok]
    r = eq[1:] / eq[:-1] - 1.0
    years = (d[-1] - d[0]).astype("timedelta64[D]").astype(float) / 365.25
    cagr = (eq[-1] / eq[0]) ** (1.0 / years) - 1.0
    ex = r if rf_daily is None else r - rf_daily[ok][1:]
    vol = r.std(ddof=1) * np.sqrt(252)
    sharpe = ex.mean() / r.std(ddof=1) * np.sqrt(252) if r.std() > 0 else np.nan
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1.0
    mdd = dd.min()
    return {
        "cagr": cagr, "vol": vol, "sharpe": sharpe, "maxdd": mdd,
        "calmar": cagr / abs(mdd) if mdd < 0 else np.nan, "final_mult": eq[-1] / eq[0],
    }


def yearly_returns(equity, dates):
    eq = np.asarray(equity, dtype=np.float64)
    yrs = dates.astype("datetime64[Y]").astype(int) + 1970
    out = {}
    for y in np.unique(yrs):
        idx = np.where(yrs == y)[0]
        first = idx[0] - 1 if idx[0] > 0 else idx[0]
        if np.isfinite(eq[first]) and np.isfinite(eq[idx[-1]]):
            out[int(y)] = eq[idx[-1]] / eq[first] - 1.0
    return out


def trade_stats(r, ret=None):
    """Summary of a vector of R multiples (and optionally % returns)."""
    r = np.asarray(r, dtype=np.float64)
    r = r[np.isfinite(r)]
    if len(r) == 0:
        return {"n": 0}
    w = r[r > 0]
    l = r[r <= 0]
    srt = np.sort(r)[::-1]
    tot = r.sum()
    out = {
        "n": int(len(r)),
        "win_rate": float(len(w) / len(r)),
        "avg_R": float(r.mean()),
        "median_R": float(np.median(r)),
        "avg_win_R": float(w.mean()) if len(w) else np.nan,
        "avg_loss_R": float(l.mean()) if len(l) else np.nan,
        "profit_factor": float(w.sum() / -l.sum()) if len(l) and l.sum() < 0 else np.nan,
        "t_stat": float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))) if len(r) > 2 else np.nan,
        "top1pct_share": float(srt[: max(1, len(r) // 100)].sum() / tot) if tot != 0 else np.nan,
        "top5pct_share": float(srt[: max(1, len(r) // 20)].sum() / tot) if tot != 0 else np.nan,
        "max_R": float(r.max()),
        "skew": float(((r - r.mean()) ** 3).mean() / r.std() ** 3) if r.std() > 0 else np.nan,
    }
    if ret is not None:
        ret = np.asarray(ret, dtype=np.float64)
        ret = ret[np.isfinite(ret)]
        out["avg_ret"] = float(ret.mean())
        out["median_ret"] = float(np.median(ret))
    return out

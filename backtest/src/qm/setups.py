"""Rule-based daily-bar versions of the three Qullamaggie setups.

Every function returns a dict of equal-length arrays describing candidate trades:
    t0 (entry day index), j (symbol column), entry, stop, prio (higher = taken first) + extras.
Only information available before the fill is used to decide the fill:
  * stop-entries on day t use indicators from the close of t-1 and day t's open/high to test the fill;
  * close-entries on day t use day t's completed bar and fill at that close.
"""
import numpy as np
from .data import rolling_max, rolling_min, days_since_max, rolling_mean, consec_up, near_split


def _a(x):
    return np.asarray(x)


def regime_on(bench_close, fast=10, slow=20, rising=False):
    """Market filter: benchmark fast SMA above slow SMA (known at the close).

    rising=True additionally requires both averages to be higher than the day before, which is
    Kullamagi's stricter wording ("10-day above the 20-day and both rising").
    """
    c = np.asarray(bench_close, dtype=np.float64)
    n = len(c)
    out = np.zeros(n, dtype=bool)
    cs = np.cumsum(np.where(np.isfinite(c), c, 0.0))
    fa = np.full(n, np.nan)
    sl = np.full(n, np.nan)
    for i in range(slow - 1, n):
        fa[i] = (cs[i] - (cs[i - fast] if i >= fast else 0.0)) / fast
        sl[i] = (cs[i] - (cs[i - slow] if i >= slow else 0.0)) / slow
    out = fa > sl
    if rising:
        up = np.zeros(n, dtype=bool)
        up[1:] = (fa[1:] > fa[:-1]) & (sl[1:] > sl[:-1])
        out &= up
    return out


def leaders_mask(f, top=0.02, adr_min=0.04, horizons=("gk22", "gk65", "gk126")):
    """Top-`top` momentum names on any horizon, inside the liquid base universe, with ADR >= adr_min."""
    best = np.zeros(_a(f["base"]).shape, dtype=np.float32)
    for h in horizons:
        r = _a(f[h])
        best = np.fmax(best, np.where(np.isfinite(r), r, 0.0).astype(np.float32))
    return _a(f["base"]) & (best >= 1.0 - top) & (_a(f["adr20"]) >= adr_min), best


def breakout_signals(p, f, top=0.02, adr_min=0.04, min_cons=5, max_cons=40, max_depth_adr=5.0,
                     tight=True, trend=True, mode="intraday", stop_adr=1.0, stop_floor_adr=0.25,
                     max_ext_adr=1.0, regime=None, start=None, end=None, dv_min=None,
                     horizons=("gk22", "gk65", "gk126"), vol_dryup=False):
    """Breakout from a consolidation in a leading stock.

    Setup, judged at the close of day t-1:
      leader     : top `top` by 1m/3m/6m return in the liquid universe, ADR20 >= adr_min
      pivot      : highest high of the last `max_cons` days, set at least `min_cons` days ago
      depth      : low since the pivot no deeper than `max_depth_adr` x ADR below the pivot
      tight      : mean true range of the last 5 days below that of the last 20 (range contraction)
                   and the low of the last 5 days above the low of the 5 days before (higher lows)
      trend      : close above SMA20 and SMA50, SMA10 > SMA20 > SMA50
    Trigger on day t: high > pivot.
      mode='intraday' : buy-stop at the pivot -> fill = max(pivot, open); stop = fill - stop_adr*ADR;
                        skipped when the fill would be more than max_ext_adr x ADR above the prior close
      mode='close'    : requires close > pivot and close >= open; fill = close;
                        stop = day's low, bounded to [stop_floor_adr, stop_adr] x ADR below the fill
    """
    O, H, L, C = (_a(p[k]) for k in ("open", "high", "low", "close"))
    V = _a(p["volume"])
    T, S = C.shape
    lead, best = leaders_mask(f, top, adr_min, horizons)
    if dv_min is not None:
        lead &= _a(f["dv20"]) >= dv_min
    if vol_dryup:
        lead &= rolling_mean(V, 5, 5) < _a(f["vol50"])
    adr = _a(f["adr20"])
    hh = rolling_max(H, max_cons)                 # pivot candidate as of each close
    dsm = days_since_max(H, max_cons)             # days since that high
    ok = lead & (dsm >= min_cons) & np.isfinite(hh)
    if max_depth_adr is not None:
        low_recent = rolling_min(L, min_cons)     # proxy for the low inside the consolidation
        ll = rolling_min(L, max_cons)
        # low since the pivot: use the min low over the days since the high (bounded by max_cons)
        depth = (hh - low_since_high(L, dsm)) / hh
        ok &= depth <= max_depth_adr * adr
    if tight:
        tr = _a(f["atr14"])  # only used for existence; contraction uses 5 vs 20 day ranges
        hl = (H - L) / C
        r5 = rolling_mean(hl.astype(np.float32), 5, 5)
        r20 = rolling_mean(hl.astype(np.float32), 20, 15)
        lo5 = rolling_min(L, 5)
        lo5_prev = np.full_like(lo5, np.nan)
        lo5_prev[5:] = lo5[:-5]
        ok &= (r5 < r20) & (lo5 > lo5_prev)
    if trend:
        s10, s20, s50 = _a(f["sma10"]), _a(f["sma20"]), _a(f["sma50"])
        ok &= (C > s20) & (C > s50) & (s10 > s20) & (s20 > s50)
    # shift: conditions known at t-1, trigger on t
    okp = np.zeros_like(ok)
    okp[1:] = ok[:-1]
    pivot = np.full_like(hh, np.nan)
    pivot[1:] = hh[:-1]
    adrp = np.full_like(adr, np.nan)
    adrp[1:] = adr[:-1]
    bestp = np.zeros_like(best)
    bestp[1:] = best[:-1]
    tradable = np.isfinite(O) & np.isfinite(C) & (V > 0)
    trig = okp & tradable & (H > pivot)
    if regime is not None:
        rp = np.zeros(T, dtype=bool)
        rp[1:] = regime[:-1]
        trig &= rp[:, None]
    prevC = np.full_like(C, np.nan)
    prevC[1:] = C[:-1]
    if mode == "intraday":
        entry = np.maximum(pivot, O)
        if max_ext_adr is not None:
            # his rule: do not buy a stock that is already up more than ~1x ADR on the day
            trig &= entry <= prevC * (1.0 + max_ext_adr * adrp)
        stop = entry * (1.0 - np.minimum(stop_adr * adrp, 0.5))
    else:
        trig &= (C > pivot) & (C >= O)
        entry = C.copy()
        dist = (C - L) / C
        dist = np.clip(dist, stop_floor_adr * adrp, stop_adr * adrp)
        stop = entry * (1.0 - dist)
    return _collect(trig, entry, stop, bestp, p, start, end, extra={"adr": adrp, "pivot": pivot})


def low_since_high(L, dsm):
    """Lowest low over the days since the window high (inclusive of the high's day)."""
    import numba as nb

    @nb.njit(parallel=True, cache=True)
    def _f(L, dsm):
        T, S = L.shape
        out = np.full((T, S), np.nan, dtype=np.float32)
        for j in nb.prange(S):
            for i in range(T):
                k = dsm[i, j]
                if k < 0:
                    continue
                m = np.inf
                for q in range(i - k, i + 1):
                    x = L[q, j]
                    if x < m:
                        m = x
                if m < np.inf:
                    out[i, j] = m
        return out

    return _f(np.asarray(L), np.asarray(dsm))


def ep_signals(p, f, gap_min=0.10, vol_mult=3.0, dv_day_min=10e6, price_min=3.0, dv_min=2e6,
               mode="close", stop_adr=1.5, stop_floor_adr=0.25, orb_k=0.25, close_strength=0.5,
               earnings=None, require_earnings=None, neglect=None, start=None, end=None):
    """Episodic pivot: a large gap-up on unusual volume.

    Day t qualifies when open/prev close - 1 >= gap_min, the stock was liquid before the gap
    (as-traded prev close >= price_min, DV20 >= dv_min) and it is a common stock.
      mode='open'  : buy the open, stop = open - stop_adr*ADR (no volume information is used)
      mode='orb'   : opening-range proxy: buy-stop at open*(1+orb_k*ADR) if the high reaches it,
                     stop = open*(1-orb_k*ADR)
      mode='close' : requires day volume >= vol_mult x 50-day average, day dollar volume >= dv_day_min
                     and a close in the top `close_strength` of the day's range and not below the open;
                     buy the close, stop = day's low bounded to [stop_floor_adr, stop_adr] x ADR.
    `earnings` is an optional bool array [T,S] marking earnings-reaction days;
    require_earnings=True/False keeps only earnings / non-earnings gaps.
    `neglect`=(lo, hi) keeps only names whose prior 126-day return was within that range.
    """
    O, H, L, C = (_a(p[k]) for k in ("open", "high", "low", "close"))
    V = _a(p["volume"])
    R = _a(p["rawclose"])
    T, S = C.shape
    is_common = np.array([p["meta"][s]["kind"] == "common" for s in p["symbols"]])
    prevC = np.full_like(C, np.nan)
    prevC[1:] = C[:-1]
    prevR = np.full_like(R, np.nan)
    prevR[1:] = R[:-1]
    adrp = np.full_like(C, np.nan)
    adrp[1:] = _a(f["adr20"])[:-1]
    dvp = np.full_like(C, np.nan)
    dvp[1:] = _a(f["dv20"])[:-1]
    volp = np.full_like(C, np.nan)
    volp[1:] = _a(f["vol50"])[:-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        gap = O / prevC - 1.0
    trig = (
        is_common[None, :] & np.isfinite(gap) & (gap >= gap_min) & (V > 0)
        & (prevR >= price_min) & (dvp >= dv_min) & np.isfinite(adrp) & (adrp > 0)
    )
    if earnings is not None and require_earnings is not None:
        trig &= (earnings if require_earnings else ~earnings)
    if neglect is not None:
        r126 = np.full_like(C, np.nan)
        r126[1:] = _a(f["ret126"])[:-1]
        trig &= (r126 >= neglect[0]) & (r126 <= neglect[1])
    if mode == "open":
        entry = O.copy()
        stop = entry * (1.0 - np.minimum(stop_adr * adrp, 0.5))   # never further than 50% away
    elif mode == "orb":
        entry = O * (1.0 + orb_k * adrp)
        trig &= H >= entry
        stop = O * (1.0 - np.minimum(orb_k * adrp, 0.5))
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            pos = (C - L) / (H - L)
        trig &= (V >= vol_mult * volp) & (C * V >= dv_day_min) & (C >= O) & (pos >= 1.0 - close_strength)
        entry = C.copy()
        dist = np.clip((C - L) / C, stop_floor_adr * adrp, stop_adr * adrp)
        stop = entry * (1.0 - dist)
    with np.errstate(divide="ignore", invalid="ignore"):
        volx = V / volp
    return _collect(trig, entry, stop, gap, p, start, end, extra={"gap": gap, "adr": adrp, "volx": volx})


def parabolic_signals(p, f, run_days=5, run_min=1.0, up_days=3, ext_sma10=0.3, dv_min=10e6,
                      price_min=2.0, mode="first_red", wait_days=5, stop_buffer=0.0,
                      naive_stop=0.3, run_max=10.0, start=None, end=None):
    """Parabolic short: fade a vertical run.

    "Parabolic" at the close of day s: close/close[s-run_days] - 1 >= run_min, at least `up_days`
    consecutive higher closes, close >= (1+ext_sma10) x SMA10, as-traded close >= price_min and
    that day's dollar volume >= dv_min.
      mode='next_open' : short the next open, stop = entry x (1 + naive_stop)
      mode='first_red' : within `wait_days` after s, the first day that closes below both its open and
                         the prior close; short that close, stop = the highest high since s (plus buffer),
                         bounded to 5%-100% above the entry
    """
    O, H, L, C = (_a(p[k]) for k in ("open", "high", "low", "close"))
    V = _a(p["volume"])
    R = _a(p["rawclose"])
    T, S = C.shape
    is_common = np.array([p["meta"][s]["kind"] == "common" for s in p["symbols"]])
    run = np.full_like(C, np.nan)
    with np.errstate(divide="ignore", invalid="ignore"):
        run[run_days:] = C[run_days:] / C[:-run_days] - 1.0
        ext = C / _a(f["sma10"]) - 1.0
    cu = consec_up(C)
    para = (
        is_common[None, :] & np.isfinite(run) & (run >= run_min) & (run <= run_max) & (cu >= up_days)
        & (ext >= ext_sma10) & (R >= price_min) & (C * V >= dv_min)
    )
    ns = near_split(p)
    if ns is not None:
        para &= ~ns
    if mode == "next_open":
        trig = np.zeros_like(para)
        trig[1:] = para[:-1]
        trig &= np.isfinite(O) & (V > 0)
        entry = O.copy()
        stop = entry * (1.0 + naive_stop)
        prio = np.full_like(C, np.nan)
        prio[1:] = run[:-1]
        return _collect(trig, entry, stop, prio, p, start, end, extra={"run": prio})
    # first red day after a parabolic close
    t_idx, j_idx = np.nonzero(para)
    seen = set()
    rows, cols, ent, stp, rr = [], [], [], [], []
    for s, j in zip(t_idx, j_idx):
        top = H[s, j]
        for d in range(s + 1, min(s + 1 + wait_days, T)):
            o, c, h = O[d, j], C[d, j], H[d, j]
            if not (np.isfinite(o) and np.isfinite(c)):
                continue
            if h > top:
                top = h
            if c < o and c < C[d - 1, j]:
                key = (d, j)
                if key not in seen:
                    seen.add(key)
                    rows.append(d); cols.append(j); ent.append(c)
                    # stop = high of the run, kept between 5% and 100% above the entry so that R stays meaningful
                    stp.append(min(max(top * (1.0 + stop_buffer), c * 1.05), c * 2.0)); rr.append(run[s, j])
                break
            if para[d, j]:
                break  # still going parabolic: a later signal day takes over
    out = {
        "t0": np.array(rows, dtype=np.int64), "j": np.array(cols, dtype=np.int64),
        "entry": np.array(ent, dtype=np.float64), "stop": np.array(stp, dtype=np.float64),
        "prio": np.array(rr, dtype=np.float64), "run": np.array(rr, dtype=np.float64),
    }
    return _window(out, p, start, end)


def _collect(trig, entry, stop, prio, p, start, end, extra=None):
    ns = near_split(p)
    if ns is not None:
        trig = trig & ~ns
    t_idx, j_idx = np.nonzero(trig)
    out = {
        "t0": t_idx.astype(np.int64), "j": j_idx.astype(np.int64),
        "entry": entry[t_idx, j_idx].astype(np.float64),
        "stop": stop[t_idx, j_idx].astype(np.float64),
        "prio": np.nan_to_num(prio[t_idx, j_idx].astype(np.float64)),
    }
    for k, a in (extra or {}).items():
        out[k] = a[t_idx, j_idx].astype(np.float64)
    good = np.isfinite(out["entry"]) & np.isfinite(out["stop"]) & (out["entry"] > 0)
    out = {k: v[good] for k, v in out.items()}
    return _window(out, p, start, end)


def _window(out, p, start, end):
    d = p["dates"]
    lo = 0 if start is None else int(np.searchsorted(d, np.datetime64(start)))
    hi = len(d) if end is None else int(np.searchsorted(d, np.datetime64(end), side="right"))
    m = (out["t0"] >= lo) & (out["t0"] < hi)
    return {k: v[m] for k, v in out.items()}


def dedupe_open(sig, exit_day):
    """Drop signals that fire while an earlier trade in the same symbol is still open."""
    order = np.lexsort((sig["t0"], sig["j"]))
    keep = np.zeros(len(order), dtype=bool)
    last_j = -1
    busy_until = -1
    for k in order:
        j = sig["j"][k]
        if j != last_j:
            last_j = j
            busy_until = -1
        if sig["t0"][k] > busy_until:
            keep[k] = True
            busy_until = exit_day[k]
    return keep

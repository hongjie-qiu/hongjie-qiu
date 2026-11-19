"""Portfolio-level simulation of the rule-based setups versus buy-and-hold benchmarks.

Usage: python3 -I run_portfolio.py <panel_dir> <out_dir> <label> <start> <end|-> <hf_dir> <french_dir>
            [--sec announcements.parquet] [--ident identifiers.parquet] [--current]
"""
import argparse
import io
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from qm.data import load_panel, compute_features
from qm.setups import breakout_signals, ep_signals, parabolic_signals, regime_on
from qm.run import long_trades, short_trades
from qm.sim import portfolio_sim, perf_stats, yearly_returns
from qm.bench import nasdaq_proxy, total_return_index, load_dividends
from qm.earnings import reaction_matrix_sec

ap = argparse.ArgumentParser()
for a_ in ("panel_dir", "out_dir", "label", "start", "end", "hf_dir", "french_dir"):
    ap.add_argument(a_)
ap.add_argument("--sec"); ap.add_argument("--ident"); ap.add_argument("--current", action="store_true")
a = ap.parse_args()
END = None if a.end == "-" else a.end
os.makedirs(a.out_dir, exist_ok=True)
p = load_panel(a.panel_dir)
f = compute_features(p, cache_dir=os.path.join(a.panel_dir, "feat"))
C = np.asarray(p["close"]); dates = p["dates"]; T = len(dates)
i0 = int(np.searchsorted(dates, np.datetime64(a.start)))
i1 = T if END is None else int(np.searchsorted(dates, np.datetime64(END), side="right"))
REG = regime_on(nasdaq_proxy(p), 10, 20, rising=True)
E, info = reaction_matrix_sec(p, a.sec, a.ident, a.current)
dv20 = np.asarray(f["dv20"])


def french_daily(name):
    z = zipfile.ZipFile(os.path.join(a.french_dir, name))
    txt = z.read(z.namelist()[0]).decode("latin-1").splitlines()
    rows = []
    hdr = None
    for ln in txt:
        parts = [x.strip() for x in ln.split(",")]
        if hdr is None and len(parts) > 1 and parts[0] == "":
            hdr = parts[1:]
            continue
        if hdr and len(parts) == len(hdr) + 1 and parts[0].isdigit() and len(parts[0]) == 8:
            rows.append([np.datetime64(f"{parts[0][:4]}-{parts[0][4:6]}-{parts[0][6:]}")] + [float(x) / 100 for x in parts[1:]])
    return pd.DataFrame(rows, columns=["date"] + hdr).set_index("date")


ff = french_daily("F-F_Research_Data_Factors_daily_CSV.zip").join(french_daily("F-F_Momentum_Factor_daily_CSV.zip"), how="inner")
ff.columns = [c.strip() for c in ff.columns]
momcol = [c for c in ff.columns if c.lower().startswith("mom")][0]
rf = pd.Series(ff["RF"]).reindex(pd.DatetimeIndex(dates)).fillna(0.0).values


def to_tr(df, shorts=False):
    d = {k: df[k].values for k in ("t0", "j", "entry", "stop", "exit_day", "final_px", "prio")}
    if not shorts:
        d["part_day"] = df["part_day"].values; d["part_px"] = df["part_px"].values; d["part_frac"] = df["part_frac"].values
    return d


def run(name, df, shorts=False, **kw):
    df = df[(df.t0 >= i0) & (df.t0 < i1)].reset_index(drop=True)
    eq, taken, g = portfolio_sim(to_tr(df, shorts), C, dates, direction=(-1 if shorts else 1), start_idx=i0, **kw)
    eq[i1:] = np.nan
    st = perf_stats(eq[i0:i1], dates[i0:i1], rf[i0:i1])
    st.update(name=name, signals=len(df), taken=len(taken), avg_gross=float(np.nanmean(g[i0:i1])),
              pct_days_invested=float(np.mean(g[i0:i1] > 0.01)))
    return eq, st, df.iloc[taken]


out = {}
stats = []
TRD = dict(day0_mode=2, part_day=3, part_frac=1 / 3, be_after_part=True, trail="sma10", cost=0.0015)
SIG = dict(top=0.02, adr_min=0.04, min_cons=5, max_cons=40, max_depth_adr=5.0, tight=True, trend=True, max_ext_adr=1.0)

bo = long_trades(p, f, breakout_signals(p, f, mode="intraday", regime=REG, start=a.start, end=END, **SIG), at_close=False, **TRD)
bo_nr = long_trades(p, f, breakout_signals(p, f, mode="intraday", regime=None, start=a.start, end=END, **SIG), at_close=False, **TRD)
bo_pess = long_trades(p, f, breakout_signals(p, f, mode="intraday", regime=REG, start=a.start, end=END, **SIG), at_close=False,
                      **dict(TRD, day0_mode=1))
for nm, df in (("Breakout Q0 (regime filter)", bo), ("Breakout Q0, no regime filter", bo_nr), ("Breakout Q0, day-0 pessimistic", bo_pess)):
    eq, st, tk = run(nm, df, risk_pct=0.005, max_pos_w=0.20, max_gross=1.0, max_positions=20, cost=0.0015)
    out[nm] = eq; stats.append(st)
eq, st, tk = run("Breakout Q0, 1% risk, 140% gross", bo, risk_pct=0.01, max_pos_w=0.25, max_gross=1.4, max_positions=25, cost=0.0015)
out[st["name"]] = eq; stats.append(st)

EPK = dict(mode="close", earnings=E, require_earnings=True)
ep50 = long_trades(p, f, ep_signals(p, f, start=a.start, end=END, **EPK), at_close=True,
                   **dict(TRD, trail="sma50", part_frac=0.0, be_after_part=False))
ep10 = long_trades(p, f, ep_signals(p, f, start=a.start, end=END, **EPK), at_close=True, **TRD)
ep_all50 = long_trades(p, f, ep_signals(p, f, mode="close", start=a.start, end=END), at_close=True,
                       **dict(TRD, trail="sma50", part_frac=0.0, be_after_part=False))
for nm, df in (("Earnings EP, close entry, 50-day trail", ep50), ("Earnings EP, close entry, his 3-5d/10-day rules", ep10),
               ("All EPs, close entry, 50-day trail", ep_all50)):
    eq, st, tk = run(nm, df, risk_pct=0.005, max_pos_w=0.10, max_gross=1.0, max_positions=25, cost=0.0015)
    out[nm] = eq; stats.append(st)
    if nm.startswith("Earnings EP, close entry, 50"):
        tk.assign(date=tk["date"].astype(str)).to_csv(os.path.join(a.out_dir, f"portfolio_trades_ep50_{a.label}.csv"), index=False)
# capacity: cap each position at 1% of 20-day average dollar volume (his stated rule)
for size in (1e5, 1e6, 1e7, 1e8):
    eq, st, tk = run(f"Earnings EP 50-day trail, ${size:,.0f} account, <=1% of ADV", ep50, start_equity=size, risk_pct=0.005,
                     max_pos_w=0.10, max_gross=1.0, max_positions=25, cost=0.0015, dv20=dv20, max_dv_frac=0.01, min_w=0.002)
    stats.append(st)

ps = short_trades(p, f, parabolic_signals(p, f, mode="next_open", run_min=1.0, naive_stop=0.3, start=a.start, end=END),
                  at_close=False, day0_mode=1, use_target=True, target="sma10", max_hold=10, cost=0.005, borrow_annual=0.5)
for nm, kw in (("Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow", dict(cost=0.005, borrow_daily=0.5 / 252)),
               ("Parabolic short, 100bp/fill, 150% borrow", dict(cost=0.01, borrow_daily=1.5 / 252))):
    eq, st, tk = run(nm, ps, shorts=True, risk_pct=0.005, max_pos_w=0.02, max_gross=0.30, max_positions=20, min_w=0.002, **kw)
    out[nm] = eq; stats.append(st)

# benchmarks
for s_ in ("SPY", "QQQ"):
    if s_ in p["col"]:
        tr = total_return_index(p, s_, load_dividends(a.hf_dir, s_))
        if s_ == "QQQ":  # the snapshot's QQQ series stops early; continue it with the QQQM-spliced proxy
            q = nasdaq_proxy(p); last = np.where(np.isfinite(C[:, p["col"]["QQQ"]]))[0][-1]
            for i in range(last + 1, T):
                tr[i] = tr[i - 1] * (q[i] / q[i - 1] if np.isfinite(q[i]) and np.isfinite(q[i - 1]) and q[i - 1] > 0 else 1.0)
        tr = pd.Series(tr).ffill().values
        eq = np.full(T, np.nan); eq[i0:i1] = tr[i0:i1] / tr[i0] * 1e5
        st = perf_stats(eq[i0:i1], dates[i0:i1], rf[i0:i1]); st.update(name=f"{s_} buy & hold (total return)", signals=0, taken=0, avg_gross=1.0, pct_days_invested=1.0)
        out[st["name"]] = eq; stats.append(st)

S = pd.DataFrame(stats)[["name", "cagr", "vol", "sharpe", "maxdd", "calmar", "final_mult", "taken", "signals", "avg_gross", "pct_days_invested"]]
S.to_csv(os.path.join(a.out_dir, f"portfolio_stats_{a.label}.csv"), index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70)
print(S.assign(cagr=(S.cagr * 100).round(1), vol=(S.vol * 100).round(1), sharpe=S.sharpe.round(2), maxdd=(S.maxdd * 100).round(1),
               calmar=S.calmar.round(2), final_mult=S.final_mult.round(2), avg_gross=S.avg_gross.round(2),
               pct_days_invested=S.pct_days_invested.round(2)).to_string(index=False))
curves = pd.DataFrame({k: v for k, v in out.items()}, index=pd.DatetimeIndex(dates)).iloc[i0:i1]
curves.to_csv(os.path.join(a.out_dir, f"portfolio_equity_{a.label}.csv"))
yr = pd.DataFrame({k: pd.Series(yearly_returns(v[i0:i1], dates[i0:i1])) for k, v in out.items()})
yr.to_csv(os.path.join(a.out_dir, f"portfolio_yearly_{a.label}.csv"))
show = [c for c in yr.columns if c in ("Breakout Q0 (regime filter)", "Earnings EP, close entry, 50-day trail",
                                        "Earnings EP, close entry, his 3-5d/10-day rules",
                                        "Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow",
                                        "SPY buy & hold (total return)", "QQQ buy & hold (total return)")]
print("\nCalendar-year returns (%):")
print((yr[show] * 100).round(1).rename(columns=lambda c: c[:24]).to_string())

# factor regression of the earnings-EP portfolio (daily, excess of RF)
for nm in ("Earnings EP, close entry, 50-day trail", "Breakout Q0 (regime filter)"):
    eq = pd.Series(out[nm], index=pd.DatetimeIndex(dates)).iloc[i0:i1]
    r = eq.pct_change().dropna()
    X = ff.reindex(r.index).dropna()
    y = (r.reindex(X.index) - X["RF"]).values
    A = np.column_stack([np.ones(len(X)), X["Mkt-RF"].values, X["SMB"].values, X["HML"].values, X[momcol].values])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ beta
    cov = np.linalg.inv(A.T @ A) * (res @ res) / (len(y) - A.shape[1])
    se = np.sqrt(np.diag(cov))
    print(f"\nFactor regression, {nm} ({X.index[0].date()}..{X.index[-1].date()}, n={len(y)}): "
          f"alpha {beta[0]*252*100:+.1f}%/yr (t={beta[0]/se[0]:+.1f}) | Mkt {beta[1]:+.2f} (t={beta[1]/se[1]:+.1f}) | "
          f"SMB {beta[2]:+.2f} (t={beta[2]/se[2]:+.1f}) | HML {beta[3]:+.2f} (t={beta[3]/se[3]:+.1f}) | "
          f"MOM {beta[4]:+.2f} (t={beta[4]/se[4]:+.1f}) | R2 {1 - res.var()/y.var():.2f}")

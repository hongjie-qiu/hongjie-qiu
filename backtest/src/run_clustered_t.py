"""Cluster-robust significance for the headline trade results: trades entered in the same calendar
month are treated as one cluster (their outcomes share market conditions and often overlap in time).

Usage: python3 -I run_clustered_t.py <panel_dir> <start> <end|-> [--sec PARQUET [--ident PARQUET] [--current]]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from qm.data import load_panel, compute_features
from qm.setups import breakout_signals, ep_signals, parabolic_signals, regime_on
from qm.run import long_trades, short_trades
from qm.bench import nasdaq_proxy
from qm.earnings import reaction_matrix_sec

ap = argparse.ArgumentParser()
ap.add_argument("panel_dir"); ap.add_argument("start"); ap.add_argument("end")
ap.add_argument("--sec"); ap.add_argument("--ident"); ap.add_argument("--current", action="store_true")
a = ap.parse_args()
END = None if a.end == "-" else a.end
p = load_panel(a.panel_dir)
f = compute_features(p, cache_dir=os.path.join(a.panel_dir, "feat"))
REG = regime_on(nasdaq_proxy(p), 10, 20, rising=True)
E, _ = reaction_matrix_sec(p, a.sec, a.ident, a.current)


def clustered(df, col):
    x = df[col].values.astype(float)
    n = len(x)
    m = x.mean()
    g = pd.DatetimeIndex(df["date"]).to_period("M")
    s = pd.Series(x - m).groupby(np.asarray(g.astype(str))).sum().values
    G = len(s)
    se = np.sqrt((s ** 2).sum()) / n * np.sqrt(G / (G - 1))
    naive = m / (x.std(ddof=1) / np.sqrt(n))
    return m, naive, m / se, G


TRD = dict(day0_mode=2, part_day=3, part_frac=1 / 3, be_after_part=True, trail="sma10", cost=0.0015)
SIG = dict(top=0.02, adr_min=0.04, min_cons=5, max_cons=40, max_depth_adr=5.0, tight=True, trend=True, max_ext_adr=1.0)
rows = []
rows.append(("Breakout Q0", long_trades(p, f, breakout_signals(p, f, mode="intraday", regime=REG, start=a.start, end=END, **SIG), at_close=False, **TRD)))
rows.append(("Breakout close-confirmed", long_trades(p, f, breakout_signals(p, f, mode="close", regime=REG, start=a.start, end=END, **SIG), at_close=True, **TRD)))
rows.append(("EP close entry, standard rules", long_trades(p, f, ep_signals(p, f, mode="close", start=a.start, end=END), at_close=True, **TRD)))
rows.append(("Earnings EP, standard rules", long_trades(p, f, ep_signals(p, f, mode="close", earnings=E, require_earnings=True, start=a.start, end=END), at_close=True, **TRD)))
rows.append(("Earnings EP, 50-day trail", long_trades(p, f, ep_signals(p, f, mode="close", earnings=E, require_earnings=True, start=a.start, end=END), at_close=True,
                                                 **dict(TRD, trail="sma50", part_frac=0.0, be_after_part=False))))
rows.append(("Parabolic short, next open, +30% stop", short_trades(p, f, parabolic_signals(p, f, mode="next_open", run_min=1.0, naive_stop=0.3, start=a.start, end=END),
                                                                  at_close=False, day0_mode=1, use_target=True, target="sma10", max_hold=10, cost=0.005, borrow_annual=0.5)))
rows.append(("Parabolic short, first red day", short_trades(p, f, parabolic_signals(p, f, mode="first_red", run_min=1.0, start=a.start, end=END),
                                                           at_close=True, day0_mode=1, use_target=True, target="sma10", max_hold=10, cost=0.005, borrow_annual=0.5)))
print(f"{a.panel_dir} {a.start}..{END}")
print(f"{'setup':<40} {'n':>6} {'avgR':>8} {'t naive':>8} {'t month-clustered':>18} {'avgRet':>8} {'t ret clustered':>16} {'months':>7}")
for nm, df in rows:
    mR, tn, tc, G = clustered(df, "R")
    mr, _, tcr, _ = clustered(df, "ret")
    print(f"{nm:<40} {len(df):>6} {mR:>+8.3f} {tn:>+8.1f} {tc:>+18.1f} {mr*100:>+7.2f}% {tcr:>+16.1f} {G:>7}")

"""Parabolic short: event study + rule-based trades.

Usage: python3 -I run_parabolic.py <panel_dir> <out_dir> [label] [start] [end]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from qm.data import load_panel, compute_features, consec_up
from qm.setups import parabolic_signals
from qm.run import short_trades, summarize, fmt_stats, by_year

panel_dir, out_dir = sys.argv[1], sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 else ""
START = sys.argv[4] if len(sys.argv) > 4 else "2005-01-01"
END = sys.argv[5] if len(sys.argv) > 5 else None
sfx = f"_{label}" if label else ""
os.makedirs(out_dir, exist_ok=True)
p = load_panel(panel_dir)
f = compute_features(p, cache_dir=os.path.join(panel_dir, "feat"))
O, H, L, C, V, R = (np.asarray(p[k]) for k in ("open", "high", "low", "close", "volume", "rawclose"))
T, S = C.shape
dates = p["dates"]
ERAS = ((2005, 2012), (2013, 2018), (2019, 2021), (2022, 2026))

# ------------------------------------------------------------------ event study from the next open
print("=== Event study: return of a SHORT opened at the next open after a 'parabolic' close (positive = short wins), no stops, no costs ===")


def study(name, **kw):
    sg = parabolic_signals(p, f, mode="next_open", start=START, end=END, **kw)
    t0, j = sg["t0"], sg["j"]
    # one event per symbol per 10 days to limit overlap
    order = np.lexsort((t0, j)); keep = np.zeros(len(t0), dtype=bool); lj = -1; lt = -100
    for k in order:
        if j[k] != lj or t0[k] - lt >= 10:
            keep[k] = True; lj = j[k]; lt = t0[k]
    t0, j = t0[keep], j[keep]
    out = f"{name:<50} n={len(t0):>5}"
    for h in (1, 3, 5, 10, 20):
        ok = t0 + h < T
        r = -(C[t0[ok] + h, j[ok]] / O[t0[ok], j[ok]] - 1.0)
        r = r[np.isfinite(r)]
        out += f" | {h}d mean {r.mean()*100:+.1f}% med {np.median(r)*100:+.1f}% win {np.mean(r>0)*100:.0f}% worst {r.min()*100:+.0f}%"
    print(out)


study("5d run >= 100%, 3 up days, >=30% over SMA10", run_min=1.0)
study("5d run >= 60%", run_min=0.6)
study("5d run >= 200%", run_min=2.0)
study("5d run >= 100%, day $vol >= 50M", run_min=1.0, dv_min=50e6)
study("10d run >= 200%", run_days=10, run_min=2.0)
study("5d run >= 50%, day $vol >= 200M (large/liquid)", run_min=0.5, dv_min=200e6)
for a, b in ERAS:
    sg = None
    study(f"5d run >= 100%  {a}-{b}", run_min=1.0) if False else None
for a, b in ERAS:
    START_, END_ = f"{a}-01-01", f"{b}-12-31"
    sg = parabolic_signals(p, f, mode="next_open", start=START_, end=END_, run_min=1.0)
    t0, j = sg["t0"], sg["j"]
    if len(t0) < 10:
        print(f"5d run >= 100% {a}-{b}: n={len(t0)} (too few)"); continue
    ok = t0 + 5 < T
    r = -(C[t0[ok] + 5, j[ok]] / O[t0[ok], j[ok]] - 1.0); r = r[np.isfinite(r)]
    print(f"5d run >= 100% {a}-{b}: n={len(r)} 5d mean {r.mean()*100:+.1f}% med {np.median(r)*100:+.1f}% win {np.mean(r>0)*100:.0f}%")

# ------------------------------------------------------------------ rule-based trades
BASE_TRADE = dict(at_close=True, day0_mode=1, use_target=True, target="sma10", max_hold=10, cost=0.005, borrow_annual=0.5)
variants = [
    ("P-red: first red close after 5d>=100%, stop=run high", dict(mode="first_red", run_min=1.0), {}),
    ("P-red, target SMA20, hold<=20d", dict(mode="first_red", run_min=1.0), {"target": "sma20", "max_hold": 20}),
    ("P-red, no target, 5-day time exit", dict(mode="first_red", run_min=1.0), {"use_target": False, "max_hold": 5}),
    ("P-red, run >= 60%", dict(mode="first_red", run_min=0.6), {}),
    ("P-red, run >= 200%", dict(mode="first_red", run_min=2.0), {}),
    ("P-red, day $vol >= 50M", dict(mode="first_red", run_min=1.0, dv_min=50e6), {}),
    ("P-red, cost 0, borrow 0", dict(mode="first_red", run_min=1.0), {"cost": 0.0, "borrow_annual": 0.0}),
    ("P-red, cost 100bp/fill, borrow 100%/yr", dict(mode="first_red", run_min=1.0), {"cost": 0.01, "borrow_annual": 1.0}),
    ("P-red, cost 100bp/fill, borrow 300%/yr", dict(mode="first_red", run_min=1.0), {"cost": 0.01, "borrow_annual": 3.0}),
    ("P-open: short next open, stop +30%, pessimistic", dict(mode="next_open", run_min=1.0, naive_stop=0.3),
     {"at_close": False}),
    ("P-open, stop +50%", dict(mode="next_open", run_min=1.0, naive_stop=0.5), {"at_close": False}),
    ("P-open, stop +100%", dict(mode="next_open", run_min=1.0, naive_stop=1.0), {"at_close": False}),
]
rows = []; keep = {}
for name, so, to in variants:
    tp = dict(BASE_TRADE); tp.update(to)
    sg = parabolic_signals(p, f, start=START, end=END, **so)
    df = short_trades(p, f, sg, **tp)
    s = summarize(df, name)
    for a, b in ERAS:
        g = df[(df.year >= a) & (df.year <= b)]
        s[f"avgR_{a}_{b}"] = g["R"].mean() if len(g) else np.nan
        s[f"n_{a}_{b}"] = len(g)
    s["worst_ret"] = df["ret"].min() if len(df) else np.nan
    rows.append(s); keep[name] = df
    print(fmt_stats(s) + f"  worstRet={s['worst_ret']*100:+.0f}%")
    print("    by era avgR: " + "  ".join(f"{a}-{b}: {s[f'avgR_{a}_{b}']:+.3f} (n={s[f'n_{a}_{b}']})" for a, b in ERAS))
pd.DataFrame(rows).to_csv(os.path.join(out_dir, f"parabolic_variants{sfx}.csv"), index=False)
df = keep[variants[0][0]]
cols = ["date", "symbol", "entry", "stop", "exit_date", "ret", "R", "hold", "reason", "run"]
df[cols].to_csv(os.path.join(out_dir, f"parabolic_trades_Pred{sfx}.csv"), index=False)
by_year(df).to_csv(os.path.join(out_dir, f"parabolic_by_year_Pred{sfx}.csv"), index=False)
print("\nP-red by year:")
print(by_year(df).round(3).to_string(index=False))
print("exit reasons (0 stop, 2 time, 3 data end, 5 target):", df["reason"].value_counts().to_dict())
print("worst 10 P-red trades:")
print(df.nsmallest(10, "ret")[cols].to_string(index=False))
print("best 10 P-red trades:")
print(df.nlargest(10, "ret")[cols].to_string(index=False))

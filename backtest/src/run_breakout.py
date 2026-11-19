"""Breakout setup: trade-level results for a rule-faithful baseline and one-at-a-time variants.

Usage: python3 -I run_breakout.py <panel_dir> <out_dir> [label] [start] [end]
Writes CSVs into <out_dir> and prints the tables.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from qm.data import load_panel, compute_features
from qm.setups import breakout_signals, regime_on, leaders_mask, _collect
from qm.run import long_trades, summarize, fmt_stats, by_year
from qm.bench import nasdaq_proxy

panel_dir, out_dir = sys.argv[1], sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 else ""
START = sys.argv[4] if len(sys.argv) > 4 else "2005-01-01"
END = sys.argv[5] if len(sys.argv) > 5 else None
os.makedirs(out_dir, exist_ok=True)
p = load_panel(panel_dir)
f = compute_features(p, cache_dir=os.path.join(panel_dir, "feat"))
qqq = nasdaq_proxy(p)
REG = regime_on(qqq, 10, 20, rising=True)
REG_LOOSE = regime_on(qqq, 10, 20, rising=False)
ERAS = ((2005, 2012), (2013, 2018), (2019, 2021), (2022, 2026))

BASE_SIG = dict(top=0.02, adr_min=0.04, min_cons=5, max_cons=40, max_depth_adr=5.0, tight=True, trend=True,
                max_ext_adr=1.0, regime=REG)
BASE_TRADE = dict(day0_mode=2, part_day=3, part_frac=1 / 3, be_after_part=True, trail="sma10", cost=0.0015)
RET_H = ("rk21", "rk63", "rk126")

variants = [
    # (name, mode, signal overrides, trade overrides)
    ("Q0 baseline: pivot stop-entry, 1xADR stop, regime on (entry day: close-based = optimistic bound)", "intraday", {}, {}),
    ("Q0 day0 worst case (entry-day low <= stop => out)", "intraday", {}, {"day0_mode": 1}),
    ("Q0 day0 ignored (entry-day low ignored)", "intraday", {}, {"day0_mode": 0}),
    ("C0 close-confirmed entry, LOD stop, regime on", "close", {}, {}),
    ("Q0 no regime filter", "intraday", {"regime": None}, {}),
    ("Q0 regime = 10>20 only (not 'both rising')", "intraday", {"regime": REG_LOOSE}, {}),
    ("C0 no regime filter", "close", {"regime": None}, {}),
    ("Q0 top 1% leaders", "intraday", {"top": 0.01}, {}),
    ("Q0 top 7% leaders (his TC2000 cut-off)", "intraday", {"top": 0.07}, {}),
    ("Q0 momentum = point-to-point 1/3/6m return", "intraday", {"horizons": RET_H}, {}),
    ("Q0 ADR >= 6%", "intraday", {"adr_min": 0.06}, {}),
    ("Q0 dollar volume >= $20M", "intraday", {"dv_min": 20e6}, {}),
    ("Q0 consolidation 10-40 days", "intraday", {"min_cons": 10}, {}),
    ("Q0 depth <= 3 ADR", "intraday", {"max_depth_adr": 3.0}, {}),
    ("Q0 no tightness filter", "intraday", {"tight": False}, {}),
    ("Q0 + volume dry-up in base", "intraday", {"vol_dryup": True}, {}),
    ("Q0 no '1xADR extension' skip", "intraday", {"max_ext_adr": None}, {}),
    ("Q0 stop 0.5 ADR", "intraday", {"stop_adr": 0.5}, {}),
    ("Q0 stop 1.5 ADR", "intraday", {"stop_adr": 1.5}, {}),
    ("Q0 no partial", "intraday", {}, {"part_frac": 0.0}),
    ("Q0 partial 1/2", "intraday", {}, {"part_frac": 0.5}),
    ("Q0 no breakeven stop", "intraday", {}, {"be_after_part": False}),
    ("Q0 trail SMA20", "intraday", {}, {"trail": "sma20"}),
    ("Q0 cost 0 bp per fill", "intraday", {}, {"cost": 0.0}),
    ("Q0 cost 5 bp per fill", "intraday", {}, {"cost": 0.0005}),
    ("Q0 cost 30 bp per fill", "intraday", {}, {"cost": 0.003}),
    ("Q0 cost 50 bp per fill", "intraday", {}, {"cost": 0.005}),
]

rows = []
keep = {}
for name, mode, so, to in variants:
    sp = dict(BASE_SIG)
    sp.update(so)
    tp = dict(BASE_TRADE)
    tp.update(to)
    sig = breakout_signals(p, f, mode=mode, start=START, end=END, **sp)
    df = long_trades(p, f, sig, at_close=(mode == "close"), **tp)
    s = summarize(df, name)
    for a, b in ERAS:
        g = df[(df.year >= a) & (df.year <= b)]
        s[f"avgR_{a}_{b}"] = g["R"].mean() if len(g) else np.nan
        s[f"n_{a}_{b}"] = len(g)
    rows.append(s)
    keep[name] = df
    print(fmt_stats(s))
    print("    by era avgR: " + "  ".join(f"{a}-{b}: {s[f'avgR_{a}_{b}']:+.3f} (n={s[f'n_{a}_{b}']})" for a, b in ERAS))

# ---- control: random entries in the same leader universe / regime, same trade management
O = np.asarray(p["open"]); C = np.asarray(p["close"]); V = np.asarray(p["volume"])
lead, best = leaders_mask(f, 0.02, 0.04)
s10, s20, s50 = (np.asarray(f[k]) for k in ("sma10", "sma20", "sma50"))
lead_tr = lead & (C > s20) & (C > s50) & (s10 > s20) & (s20 > s50)
okp = np.zeros_like(lead_tr); okp[1:] = lead_tr[:-1]
rp = np.zeros(len(REG), dtype=bool); rp[1:] = REG[:-1]
okp &= rp[:, None] & np.isfinite(O) & (V > 0)
adrp = np.full(C.shape, np.nan, dtype=np.float32); adrp[1:] = np.asarray(f["adr20"])[:-1]
bestp = np.zeros_like(best); bestp[1:] = best[:-1]
n_target = len(keep[variants[0][0]])
ctrl_rows = []
for seed in range(20):
    rng = np.random.default_rng(seed)
    pick = okp & (rng.random(okp.shape) < 3.0 * n_target / max(okp.sum(), 1))
    sig = _collect(pick, O.astype(np.float64), O * (1.0 - adrp), bestp, p, START, END, extra={"adr": adrp})
    df = long_trades(p, f, sig, at_close=False, **BASE_TRADE)
    ctrl_rows.append(summarize(df, f"control seed {seed}"))
ctrl = pd.DataFrame(ctrl_rows)
print("\nControl - random entry at the open in trending leaders, regime on, same exits (20 seeds; fills at the open are exact):")
print("  n per run ~%d | avgR mean %+.3f (min %+.3f, max %+.3f) | win %.1f%% | avgRet %+.2f%%" % (
    ctrl["n"].mean(), ctrl["avg_R"].mean(), ctrl["avg_R"].min(), ctrl["avg_R"].max(),
    ctrl["win_rate"].mean() * 100, ctrl["avg_ret"].mean() * 100))
s = {"label": "CONTROL random entry in trending leaders (mean of 20 seeds)", "n": int(ctrl["n"].mean()),
     "win_rate": ctrl["win_rate"].mean(), "avg_R": ctrl["avg_R"].mean(), "avg_ret": ctrl["avg_ret"].mean(),
     "profit_factor": ctrl["profit_factor"].mean()}
rows.append(s)

res = pd.DataFrame(rows)
sfx = f"_{label}" if label else ""
res.to_csv(os.path.join(out_dir, f"breakout_variants{sfx}.csv"), index=False)
cols = ["date", "symbol", "entry", "stop", "exit_date", "ret", "R", "hold", "reason", "prio", "adr"]
for key, tag in ((variants[0][0], "Q0"), (variants[3][0], "C0"), (variants[4][0], "Q0_noregime")):
    by_year(keep[key]).to_csv(os.path.join(out_dir, f"breakout_by_year_{tag}{sfx}.csv"), index=False)
    keep[key][cols].to_csv(os.path.join(out_dir, f"breakout_trades_{tag}{sfx}.csv"), index=False)
print("\nQ0 by year:")
print(by_year(keep[variants[0][0]]).round(3).to_string(index=False))
print("\nQ0 without regime filter, by year:")
print(by_year(keep[variants[4][0]]).round(3).to_string(index=False))
df = keep[variants[0][0]]
r = np.sort(df["R"].values)[::-1]
k1 = max(1, len(r) // 100)
print("\nQ0 profit concentration: sum R = %.1f | top 10 trades = %.1f | top 1%% (%d trades) = %.1f | all others = %.1f" % (
    r.sum(), r[:10].sum(), k1, r[:k1].sum(), r[k1:].sum()))
print("exit reasons (0 stop, 1 trail, 2 time, 3 data end, 4 day-0 stop):", df["reason"].value_counts().to_dict())
i0 = int(np.searchsorted(p["dates"], np.datetime64(START)))
print("regime-on share of days: strict %.2f, loose %.2f" % (REG[i0:].mean(), REG_LOOSE[i0:].mean()))
print("top 15 Q0 trades:")
print(df.nlargest(15, "R")[["date", "symbol", "entry", "stop", "exit_date", "ret", "R", "hold"]].to_string(index=False))

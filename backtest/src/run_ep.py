"""Episodic pivot (large gap-up): event study + rule-based trades.

Usage: python3 -I run_ep.py <panel_dir> <out_dir> [--label L] [--start D] [--end D]
                             [--sec announcements.parquet [--ident identifiers.parquet] [--current]]
                             [--nasdaq nasdaq_json_dir]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from qm.data import load_panel, compute_features
from qm.setups import ep_signals
from qm.earnings import reaction_matrix, reaction_matrix_sec
from qm.run import long_trades, summarize, fmt_stats, by_year

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("panel_dir"); ap.add_argument("out_dir")
ap.add_argument("--label", default=""); ap.add_argument("--start", default="2005-01-01"); ap.add_argument("--end", default=None)
ap.add_argument("--sec", default=None, help="SEC 8-K earnings announcements parquet (delisted companies included)")
ap.add_argument("--ident", default=None, help="security-master identifiers parquet (CIK -> current ticker)")
ap.add_argument("--current", action="store_true", help="panel is keyed by today's tickers")
ap.add_argument("--nasdaq", default=None, help="directory of Nasdaq earnings-calendar JSON (adds EPS surprise)")
a = ap.parse_args()
panel_dir, out_dir, label, START, END = a.panel_dir, a.out_dir, a.label, a.start, a.end
sfx = f"_{label}" if label else ""
os.makedirs(out_dir, exist_ok=True)
p = load_panel(panel_dir)
f = compute_features(p, cache_dir=os.path.join(panel_dir, "feat"))
O, H, L, C, V, R = (np.asarray(p[k]) for k in ("open", "high", "low", "close", "volume", "rawclose"))
T, S = C.shape
dates = p["dates"]
spy = C[:, p["col"]["SPY"]].astype(np.float64)
for _i in range(1, len(spy)):          # sessions the delisting-inclusive file lacks: carry SPY forward
    if not np.isfinite(spy[_i]):
        spy[_i] = spy[_i - 1]
E = SUR = None
if a.sec:
    E, info = reaction_matrix_sec(p, a.sec, a.ident, a.current)
    print("earnings flags:", info)
if a.nasdaq and os.path.isdir(a.nasdaq):
    E2, SUR, info2 = reaction_matrix(p, a.nasdaq)
    print("nasdaq calendar (EPS surprise):", info2)
    if E is None:
        E = E2
ERAS = ((2005, 2012), (2013, 2018), (2019, 2021), (2022, 2026))

# ------------------------------------------------------------------ event study
sig = ep_signals(p, f, gap_min=0.10, mode="open", start=START, end=END)  # every qualifying gap, at the open
t0, j = sig["t0"], sig["j"]
ev = pd.DataFrame({"t0": t0, "j": j, "gap": sig["gap"], "adr": sig["adr"], "volx": sig["volx"]})
ev["year"] = pd.DatetimeIndex(dates[t0]).year
ev["o"] = O[t0, j]; ev["c"] = C[t0, j]; ev["h"] = H[t0, j]; ev["l"] = L[t0, j]
ev["dvday"] = C[t0, j].astype(np.float64) * V[t0, j]
ev["intraday"] = ev["c"] / ev["o"] - 1.0
ev["pos"] = (ev["c"] - ev["l"]) / (ev["h"] - ev["l"]).replace(0, np.nan)
ev["r126"] = np.asarray(f["ret126"])[np.maximum(t0 - 1, 0), j]
ev["earn"] = E[t0, j] if E is not None else False
ev["sur"] = SUR[t0, j] if SUR is not None else np.nan
# earnings filings start in 2003-04; before 2004 a missing flag means "unknown", not "no earnings"
ev_known = ev[ev.year >= 2004]
for h in (1, 5, 10, 20, 60):
    ok = t0 + h < T
    r = np.full(len(t0), np.nan); m = np.full(len(t0), np.nan)
    r[ok] = C[t0[ok] + h, j[ok]] / C[t0[ok], j[ok]] - 1.0
    m[ok] = spy[t0[ok] + h] / spy[t0[ok]] - 1.0
    ev[f"f{h}"] = r
    ev[f"x{h}"] = r - m
ev.to_csv(os.path.join(out_dir, f"ep_events{sfx}.csv"), index=False)


def line(name, g):
    if len(g) < 30:
        return f"{name:<52} n={len(g):>6}  (too few)"
    out = f"{name:<52} n={len(g):>6}  open->close {g['intraday'].mean()*100:+.2f}%"
    for h in (1, 5, 20, 60):
        x = g[f"x{h}"].dropna()
        # cluster by entry day for the t-stat (same-day events are correlated)
        dm = g.loc[x.index].groupby("t0")[f"x{h}"].mean()
        t = dm.mean() / (dm.std(ddof=1) / np.sqrt(len(dm))) * np.sqrt(min(1.0, 5.0 / h)) if len(dm) > 5 else np.nan
        out += f" | +{h}d xs {x.mean()*100:+.2f}% (med {x.median()*100:+.2f}%, t~{t:+.1f})"
    return out


print("\n=== Event study: every gap-up >= 10% in a liquid common stock; returns after the gap-day CLOSE, minus SPY ===")
print(line("all gaps >= 10%", ev))
strong = ev[(ev.volx >= 3) & (ev.dvday >= 10e6)]
print(line("volume >= 3x and day $vol >= 10M", strong))
print(line("  ... and close >= open, top half of range", strong[(strong.c >= strong.o) & (strong.pos >= 0.5)]))
print(line("  ... and close < open (faded)", strong[strong.c < strong.o]))
if E is not None:
    print(line("  earnings reaction day", strong[strong.earn]))
    print(line("  not an earnings day", strong[~strong.earn]))
    e2 = strong[strong.earn]
    print(line("  earnings + close>=open, top half of range", e2[(e2.c >= e2.o) & (e2.pos >= 0.5)]))
    if SUR is not None:
        print(line("  earnings + EPS surprise >= +20%", e2[e2.sur >= 20]))
        print(line("  earnings + EPS surprise <= 0", e2[e2.sur <= 0]))
for lo, hi in ((0.10, 0.20), (0.20, 0.40), (0.40, 9.9)):
    print(line(f"  gap {int(lo*100)}-{int(hi*100) if hi<9 else 'inf'}%", strong[(strong.gap >= lo) & (strong.gap < hi)]))
print(line("  'neglected': prior 6m return in [-30%, +30%]", strong[(strong.r126 >= -0.3) & (strong.r126 <= 0.3)]))
print(line("  extended: prior 6m return > +50%", strong[strong.r126 > 0.5]))
print(line("  beaten down: prior 6m return < -30%", strong[strong.r126 < -0.3]))
print(line("  volume >= 10x", strong[strong.volx >= 10]))
for a, b in ERAS:
    g = strong[(strong.year >= a) & (strong.year <= b)]
    print(line(f"  {a}-{b}", g))
    if E is not None:
        print(line(f"    earnings only {a}-{b}", g[g.earn]))

# ------------------------------------------------------------------ rule-based trades
BASE_TRADE = dict(day0_mode=2, part_day=3, part_frac=1 / 3, be_after_part=True, trail="sma10", cost=0.0015)
variants = [
    ("E-close: vol>=3x, strong close; buy close, LOD stop", dict(mode="close"), {}, True),
    ("E-close, trail SMA20", dict(mode="close"), {"trail": "sma20"}, True),
    ("E-close, trail SMA50, no partial/BE", dict(mode="close"), {"trail": "sma50", "part_frac": 0.0, "be_after_part": False}, True),
    ("E-close, earnings only", dict(mode="close", earnings=E, require_earnings=True), {}, True),
    ("E-close, earnings only, trail SMA20", dict(mode="close", earnings=E, require_earnings=True), {"trail": "sma20"}, True),
    ("E-close, earnings only, trail SMA50 no partial/BE", dict(mode="close", earnings=E, require_earnings=True),
     {"trail": "sma50", "part_frac": 0.0, "be_after_part": False}, True),
    ("E-close, non-earnings only", dict(mode="close", earnings=E, require_earnings=False), {}, True),
    ("E-close, neglected (6m ret -30..+30%)", dict(mode="close", neglect=(-0.3, 0.3)), {}, True),
    ("E-close, earnings + neglected, trail SMA20", dict(mode="close", neglect=(-0.3, 0.3), earnings=E, require_earnings=True),
     {"trail": "sma20"}, True),
    ("E-close, gap >= 20%", dict(mode="close", gap_min=0.20), {}, True),
    ("E-close, volume >= 5x", dict(mode="close", vol_mult=5.0), {}, True),
    ("E-close, cost 0", dict(mode="close"), {"cost": 0.0}, True),
    ("E-close, cost 30 bp", dict(mode="close"), {"cost": 0.003}, True),
    # a fill at the open is exact on daily bars: the whole day's range follows the fill
    ("E-open: buy the open, 1xADR stop (exact)", dict(mode="open", stop_adr=1.0), {}, False),
    ("E-open, 1.5xADR stop (exact)", dict(mode="open", stop_adr=1.5), {}, False),
    ("E-open, earnings only (exact)", dict(mode="open", stop_adr=1.0, earnings=E, require_earnings=True), {}, False),
    # the opening-range proxy fills after the open, so the entry day is ambiguous: three assumptions
    ("E-orb proxy: buy open+0.25ADR, stop open-0.25ADR, worst case", dict(mode="orb", orb_k=0.25), {"day0_mode": 1}, False),
    ("E-orb proxy, close-based (optimistic bound)", dict(mode="orb", orb_k=0.25), {"day0_mode": 2}, False),
    ("E-orb proxy, entry-day low ignored", dict(mode="orb", orb_k=0.25), {"day0_mode": 0}, False),
]
rows = []
keep = {}
for name, so, to, at_close in variants:
    if E is None and "earnings" in so:
        continue
    tp = dict(BASE_TRADE); tp.update(to)
    sg = ep_signals(p, f, start=START, end=END, **so)
    df = long_trades(p, f, sg, at_close=at_close, **tp)
    s = summarize(df, name)
    for a, b in ERAS:
        g = df[(df.year >= a) & (df.year <= b)]
        s[f"avgR_{a}_{b}"] = g["R"].mean() if len(g) else np.nan
        s[f"n_{a}_{b}"] = len(g)
    rows.append(s); keep[name] = df
    print(fmt_stats(s))
    print("    by era avgR: " + "  ".join(f"{a}-{b}: {s[f'avgR_{a}_{b}']:+.3f} (n={s[f'n_{a}_{b}']})" for a, b in ERAS))
pd.DataFrame(rows).to_csv(os.path.join(out_dir, f"ep_variants{sfx}.csv"), index=False)
cols = ["date", "symbol", "entry", "stop", "exit_date", "ret", "R", "hold", "reason", "gap", "volx", "adr"]
for key, tag in ((variants[0][0], "Eclose"), (variants[4][0], "Eclose_earn_sma20"), ("E-open: buy the open, 1xADR stop (exact)", "Eopen")):
    if key in keep:
        by_year(keep[key]).to_csv(os.path.join(out_dir, f"ep_by_year_{tag}{sfx}.csv"), index=False)
        keep[key][cols].to_csv(os.path.join(out_dir, f"ep_trades_{tag}{sfx}.csv"), index=False)
for key in (variants[0][0], variants[4][0]):
    if key in keep:
        print(f"\n{key} by year:")
        print(by_year(keep[key]).round(3).to_string(index=False))
df = keep[variants[0][0]]
r = np.sort(df["R"].values)[::-1]
k1 = max(1, len(r) // 100)
print("\nE-close profit concentration: sum R = %.1f | top 10 = %.1f | top 1%% (%d) = %.1f | others = %.1f" % (
    r.sum(), r[:10].sum(), k1, r[:k1].sum(), r[k1:].sum()))
print("top 15 E-close trades:")
print(df.nlargest(15, "R")[["date", "symbol", "entry", "stop", "exit_date", "ret", "R", "hold", "gap", "volx"]].to_string(index=False))

"""What does the scan universe do on its own?  Forward returns of "leaders" and of breakout days.

Usage: python3 -I run_universe.py <panel_dir> <start> [end]
Per-day equal-weight forward return minus SPY, sampled every 5th day; the t-stat treats those daily
cross-sectional means as the observations and deflates for the overlap of h-day windows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from qm.data import load_panel, compute_features, xs_pct_rank
from qm.setups import breakout_signals, leaders_mask, regime_on
from qm.bench import nasdaq_proxy

panel_dir, START = sys.argv[1], sys.argv[2]
END = sys.argv[3] if len(sys.argv) > 3 else None
p = load_panel(panel_dir)
f = compute_features(p, cache_dir=os.path.join(panel_dir, "feat"))
O, H, L, C = (np.asarray(p[k]) for k in ("open", "high", "low", "close"))
T, S = C.shape
dates = p["dates"]
spy = C[:, p["col"]["SPY"]].astype(np.float64)
yr = dates.astype("datetime64[Y]").astype(int) + 1970
i0 = int(np.searchsorted(dates, np.datetime64(START)))
i1 = T if END is None else int(np.searchsorted(dates, np.datetime64(END), side="right"))
base = np.asarray(f["base"]); adr = np.asarray(f["adr20"])
ERAS = [(a, b) for a, b in ((2005, 2012), (2013, 2018), (2019, 2021), (2022, 2026)) if b >= yr[i0] and a <= yr[i1 - 1]]


def xs(mask, h=20):
    out = []
    for a, b in [(int(yr[i0]), int(yr[i1 - 1]))] + ERAS:
        rows = np.where((yr >= a) & (yr <= b) & (np.arange(T) >= i0) & (np.arange(T) + h < i1))[0]
        dm = []
        for i in rows[::5]:
            js = np.where(mask[i])[0]
            if len(js) < 3:
                continue
            r = C[i + h, js] / C[i, js] - 1
            r = r[np.isfinite(r)]
            if len(r) >= 3:
                dm.append(r.mean() - (spy[i + h] / spy[i] - 1))
        dm = np.array(dm)
        if len(dm) < 10:
            out.append(f"{a}-{b}: n/a")
            continue
        t = dm.mean() / (dm.std(ddof=1) / np.sqrt(len(dm) / (h / 5)))
        out.append(f"{a}-{b}: {dm.mean()*100:+.2f}% (t={t:+.1f})")
    return " | ".join(out)


liq = base & (adr >= 0.04)
lead, best = leaders_mask(f, 0.02, 0.04)
print(f"=== {panel_dir}  {START}..{END or dates[-1]} : 20-day forward return minus SPY, equal-weighted across names each day ===")
print("liquid universe (price>=$3, $vol>=3M)        ", xs(base))
print("  ... with ADR >= 4%                          ", xs(liq))
print("LEADERS: top 2% on any horizon, ADR >= 4%     ", xs(lead))
for h_, nm in (("gk22", "1-month"), ("gk65", "3-month"), ("gk126", "6-month")):
    print(f"  top 2% by {nm} gain, ADR >= 4%            ", xs(liq & (np.asarray(f[h_]) >= 0.98)))
print("top 7% on any horizon, ADR >= 4%              ", xs(leaders_mask(f, 0.07, 0.04)[0]))
r252 = np.full_like(C, np.nan); r252[252:] = C[231:-21] / C[:-252] - 1
rk122 = xs_pct_rank(r252.astype(np.float32), base)
print("academic 12-2 momentum, top decile            ", xs(base & (rk122 >= 0.90)))
print("academic 12-2 momentum, bottom decile         ", xs(base & (rk122 <= 0.10)))
print("leaders 5-day forward                         ", xs(lead, 5))
print("leaders 60-day forward                        ", xs(lead, 60))

# breakout days under the final Q0 definition
REG = regime_on(nasdaq_proxy(p), 10, 20, rising=True)
for nm, reg in (("regime on", REG), ("no regime filter", None)):
    sg = breakout_signals(p, f, top=0.02, adr_min=0.04, mode="intraday", regime=reg, start=START, end=END)
    t0, j, e = sg["t0"], sg["j"], sg["entry"]
    same = C[t0, j] / e - 1
    line = f"breakout stop-entries ({nm}) n={len(t0)}: entry->same-day close mean {same.mean()*100:+.2f}% median {np.median(same)*100:+.2f}% up {np.mean(same>0)*100:.0f}%"
    for h in (1, 5, 20):
        ok = t0 + h < i1
        x = C[t0[ok] + h, j[ok]] / e[ok] - 1 - (spy[t0[ok] + h] / spy[t0[ok] - 1] - 1)
        x = x[np.isfinite(x)]
        line += f" | entry->+{h}d minus SPY {x.mean()*100:+.2f}% (med {np.median(x)*100:+.2f}%)"
    lo = L[t0, j] / e - 1
    line += f" | day-0 low: median {np.median(lo)*100:.1f}% below entry; <= entry-1ADR on {np.mean(lo <= -sg['adr'])*100:.0f}% of days, <= entry-0.5ADR on {np.mean(lo <= -0.5*sg['adr'])*100:.0f}%"
    print(line)
    c2 = breakout_signals(p, f, top=0.02, adr_min=0.04, mode="close", regime=reg, start=START, end=END)
    t0, j, e = c2["t0"], c2["j"], c2["entry"]
    line = f"  close-confirmed breakouts ({nm}) n={len(t0)}:"
    for h in (1, 5, 20):
        ok = t0 + h < i1
        x = C[t0[ok] + h, j[ok]] / e[ok] - 1 - (spy[t0[ok] + h] / spy[t0[ok]] - 1)
        x = x[np.isfinite(x)]
        line += f" close->+{h}d minus SPY {x.mean()*100:+.2f}% (med {np.median(x)*100:+.2f}%) |"
    print(line)
print("avg number of leaders per day:", int(lead[i0:i1].sum(axis=1).mean()), "| base universe:", int(base[i0:i1].sum(axis=1).mean()))

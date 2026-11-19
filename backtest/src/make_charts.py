"""Render the three report figures from the result CSVs.

Usage: python3 -I make_charts.py <results_dir> <figures_dir>
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

res, figdir = sys.argv[1], sys.argv[2]
os.makedirs(figdir, exist_ok=True)

# palette: validated categorical slots 1-3 (light surface) + chart chrome tokens
SURFACE, INK, INK2, MUTED, GRID, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({
    "font.family": ["WenQuanYi Zen Hei", "DejaVu Sans"], "axes.unicode_minus": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "font.size": 10,
})


def title(ax, main, sub):
    ax.set_title(main, loc="left", fontsize=13, fontweight="bold", color=INK, pad=28)
    ax.text(0, 1.035, sub, transform=ax.transAxes, fontsize=9.5, color=INK2, va="bottom")


# ------------------------------------------------------------------ figure 1: equity curves
eq = pd.read_csv(os.path.join(res, "portfolio_equity_hf.csv"), index_col=0, parse_dates=True)
series = [
    ([c for c in eq.columns if c.startswith("QQQ buy")][0], "QQQ 买入持有", MUTED, (0, (4, 2))),
    ("SPY buy & hold (total return)", "SPY 买入持有", MUTED, "-"),
    ("Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow", "抛物线做空（规则版）", AQUA, "-"),
    ("Earnings EP, close entry, 50-day trail", "财报 EP（收盘确认，50日线跟踪）", ORANGE, "-"),
    ("Breakout Q0 (regime filter)", "突破（规则版）", BLUE, "-"),
]
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
ends = []
for col, lab, color, ls in series:
    s = (eq[col] / 1e5).dropna()
    ax.plot(s.index, s.values, color=color, lw=2, ls=ls, solid_capstyle="round", label=lab)
    ends.append((s.index[-1], s.values[-1], lab, color))
ax.set_yscale("log")
ax.set_yticks([0.5, 1, 2, 5, 10, 20])
ax.set_yticklabels(["0.5×", "1×", "2×", "5×", "10×", "20×"])
ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax.grid(axis="x", visible=False)
ax.axhline(1, color=BASE, lw=1)
# direct labels at the line ends, nudged apart in log space
ends.sort(key=lambda e: e[1])
ypos = []
for _, y, _, _ in ends:
    y2 = y if not ypos else max(y, ypos[-1] * 1.22)
    ypos.append(y2)
xmax = eq.index[-1]
for (x, y, lab, color), y2 in zip(ends, ypos):
    ax.plot([x], [y], marker="o", ms=6, color=color, mec=SURFACE, mew=1.5, zorder=5)
    ax.annotate(f"{lab}  {y:.2f}×", xy=(x, y), xytext=(xmax + pd.Timedelta(days=150), y2), fontsize=9, color=INK2,
                va="center", arrowprops=dict(arrowstyle="-", color=BASE, lw=0.8))
ax.set_xlim(eq.index[0], xmax + pd.Timedelta(days=3300))
ax.set_xticks(pd.to_datetime([f"{y}-01-01" for y in range(2006, 2027, 4)]))
ax.set_xticklabels([str(y) for y in range(2006, 2027, 4)])
ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=1, labelcolor=INK2)
title(ax, "规则化之后，三种形态都没有跑赢指数", "10 万美元起始的净值倍数（对数轴），2005-01 至 2026-11；每笔风险 0.5%，含交易成本；数据仅含至今仍上市的股票")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "fig1_equity.png"))
plt.close(fig)

# ------------------------------------------------------------------ figure 2: sensitivity to the intraday assumption
bo = pd.read_csv(os.path.join(res, "breakout_variants.csv")).set_index("label")["avg_R"]
ep = pd.read_csv(os.path.join(res, "ep_variants.csv")).set_index("label")["avg_R"]


def pick(sr, prefix):
    m = [k for k in sr.index if k.startswith(prefix)]
    assert len(m) == 1, (prefix, m)
    return float(sr[m[0]])


rows = [
    ("突破：枢轴价挂单买入", {"pess": pick(bo, "Q0 day0 worst case"), "close": pick(bo, "Q0 baseline"), "opt": pick(bo, "Q0 day0 ignored")}),
    ("EP：开盘区间突破（日线代理）", {"pess": pick(ep, "E-orb proxy: buy"), "close": pick(ep, "E-orb proxy, close-based"),
                           "opt": pick(ep, "E-orb proxy, entry-day low ignored")}),
    ("EP：开盘价买入", {"none": pick(ep, "E-open: buy the open")}),
    ("突破：收盘确认后买入", {"none": pick(bo, "C0 close-confirmed")}),
    ("EP：收盘确认后买入", {"none": pick(ep, "E-close: vol>=3x")}),
    ("EP：仅财报跳空，收盘确认", {"none": pick(ep, "E-close, earnings only  ") if False else float(ep[[k for k in ep.index if k.strip() == "E-close, earnings only"][0]])}),
    ("EP：仅财报跳空，50日线跟踪", {"none": pick(ep, "E-close, earnings only, trail SMA50")}),
]
style = {"pess": (BLUE, "最坏情形：入场当日最低价触及止损即出局"), "close": (ORANGE, "乐观端：入场当日收盘跌破止损才算出局"),
         "opt": (AQUA, "忽略入场当日的最低价"), "none": (INK2, "无盘中歧义（按开盘价或收盘价成交）")}
fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
ys = np.arange(len(rows))[::-1]
for y, (lab, vals) in zip(ys, rows):
    xs = list(vals.values())
    if len(xs) > 1:
        ax.plot([min(xs), max(xs)], [y, y], color=BASE, lw=2, zorder=1, solid_capstyle="round")
    for k, v in vals.items():
        ax.plot([v], [y], marker="o", ms=9, color=style[k][0], mec=SURFACE, mew=2, zorder=3)
    # label the extremes only
    lo, hi = min(xs), max(xs)
    ax.text(hi + 0.02, y, f"{hi:+.2f}R", va="center", ha="left", fontsize=9, color=INK2)
    if len(xs) > 1:
        ax.text(lo - 0.02, y, f"{lo:+.2f}R", va="center", ha="right", fontsize=9, color=INK2)
ax.axvline(0, color=BASE, lw=1.2, zorder=0)
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], color=INK, fontsize=10)
ax.set_xlim(-0.66, 0.82)
ax.set_xlabel("平均每笔盈亏（R = 初始止损距离的倍数；每次成交计 15 个基点成本）")
ax.grid(axis="y", visible=False)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=c, mec=SURFACE, mew=1.5, label=l) for c, l in style.values()]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.42, -0.17), ncol=2, frameon=False, fontsize=9,
          labelcolor=INK2, columnspacing=2.0, handletextpad=0.4)
title(ax, "盘中入场的回测结论，取决于日线无法知道的盘中顺序", "同一批信号在不同“入场当日”假设下的平均 R，2005–2026；灰线两端是日线能给出的上下界，线越长越无法下结论")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "fig2_intraday_assumption.png"))
plt.close(fig)

# ------------------------------------------------------------------ figure 3: parabolic short vs costs
pv = pd.read_csv(os.path.join(res, "parabolic_variants.csv")).set_index("label")["avg_ret"]
bars = [
    ("零成本", pick(pv, "P-red, cost 0, borrow 0")),
    ("每次成交 0.5%\n融券费 50%/年", pick(pv, "P-red: first red close")),
    ("每次成交 1%\n融券费 100%/年", pick(pv, "P-red, cost 100bp/fill, borrow 100%/yr")),
    ("每次成交 1%\n融券费 300%/年", pick(pv, "P-red, cost 100bp/fill, borrow 300%/yr")),
]
fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=200)
x = np.arange(len(bars))
vals = [b[1] * 100 for b in bars]
ax.bar(x, vals, width=0.2, color=BLUE, zorder=3)
for xi, v in zip(x, vals):
    ax.text(xi, v + (0.18 if v >= 0 else -0.18), f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top", fontsize=10, color=INK)
ax.axhline(0, color=BASE, lw=1.2, zorder=2)
ax.set_xticks(x)
ax.set_xticklabels([b[0] for b in bars], color=INK2, fontsize=9.5)
ax.set_ylabel("平均每笔净收益（占仓位市值）")
ax.set_ylim(min(vals) - 1.2, max(vals) + 1.2)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:+.0f}%"))
ax.grid(axis="x", visible=False)
title(ax, "抛物线做空的优势，被滑点和融券费吃掉", "5 日涨幅≥100% 后首个收阴日收盘做空、回落至 10 日线平仓，2005–2026，约 1,360 笔")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "fig3_short_costs.png"))
plt.close(fig)
print("figures written to", figdir, os.listdir(figdir))

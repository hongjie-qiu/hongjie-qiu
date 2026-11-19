"""Turn the result CSVs and logs into the markdown tables used in the research notes.

Usage: python3 -I make_tables.py <results_dir> > tables.md
Everything printed here is read straight from files written by the run_* scripts, so the notes
cannot drift from the results.
"""
import os
import re
import sys

import numpy as np
import pandas as pd

R = sys.argv[1]
ERAS = ("2005_2012", "2013_2018", "2019_2021", "2022_2026")


def read(fn):
    p = os.path.join(R, fn)
    return open(p).read() if os.path.exists(p) else ""


def clustered(fn):
    """label -> (avgR, t naive, t clustered, avg ret, t ret clustered)"""
    out = {}
    for ln in read(fn).splitlines():
        m = re.match(r"^(.{40})\s+(\d+)\s+([+-][\d.]+)\s+([+-][\d.]+)\s+([+-][\d.]+)\s+([+-][\d.]+)%\s+([+-][\d.]+)\s+(\d+)", ln)
        if m:
            out[m.group(1).strip()] = tuple(float(m.group(k)) for k in (3, 4, 5, 6, 7)) + (int(m.group(2)),)
    return out


def variants(fn, title, eras=True):
    p = os.path.join(R, fn)
    if not os.path.exists(p):
        return
    d = pd.read_csv(p)
    print(f"\n#### {title}\n")
    hdr = "| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance |"
    sep = "|---|---|---|---|---|---|---|---|---|"
    if eras:
        hdr += " 2005-12 | 2013-18 | 2019-21 | 2022-26 |"
        sep += "---|---|---|---|"
    if "worst_ret" in d.columns:
        hdr += " Worst trade |"
        sep += "---|"
    print(hdr)
    print(sep)
    for _, r in d.iterrows():
        def g(k, f="{:+.2f}"):
            v = r.get(k, np.nan)
            return "" if pd.isna(v) else f.format(v)
        row = (f"| {r['label']} | {int(r['n']):,} | {r['win_rate']*100:.1f}% | {r['avg_R']:+.3f} | {g('t_stat','{:+.1f}')} | "
               f"{g('avg_ret','{:+.2%}')} | {g('profit_factor','{:.2f}')} | {g('avg_hold','{:.1f}')} | {g('avg_risk_pct','{:.1%}')} |")
        if eras:
            row += "".join(f" {g('avgR_'+e)} |" for e in ERAS)
        if "worst_ret" in d.columns:
            row += f" {g('worst_ret','{:+.0%}')} |"
        print(row)


def by_year(fn, title):
    p = os.path.join(R, fn)
    if not os.path.exists(p):
        return
    d = pd.read_csv(p)
    print(f"\n#### {title}\n")
    print("| Year | Trades | Win rate | Avg R | Sum R | Avg return |")
    print("|---|---|---|---|---|---|")
    for _, r in d.iterrows():
        print(f"| {int(r['year'])} | {int(r['n'])} | {r['win']*100:.0f}% | {r['avgR']:+.2f} | {r['sumR']:+.1f} | {r['avg_ret']:+.2%} |")


def universe(fn, title):
    txt = read(fn)
    if not txt:
        return
    print(f"\n#### {title}\n")
    lines = [ln for ln in txt.splitlines() if re.search(r"\d{4}-\d{4}: ", ln)]
    eras = re.findall(r"(\d{4}-\d{4}):", lines[0])
    print("| Group | " + " | ".join(eras) + " |")
    print("|---|" + "---|" * len(eras))
    for ln in lines:
        label = re.split(r"\s{2,}\d{4}-\d{4}:", ln)[0].strip()
        cells = re.findall(r"\d{4}-\d{4}: ([^|]+)", ln)
        print(f"| {label} | " + " | ".join(c.strip() for c in cells) + " |")
    for ln in txt.splitlines():
        if ln.startswith("breakout stop-entries") or ln.strip().startswith("close-confirmed breakouts") or ln.startswith("avg number"):
            print("\n" + ln.strip())


def ep_events(fn, title):
    txt = read(fn)
    if not txt:
        return
    print(f"\n#### {title}\n")
    print("| Subset | Events | Gap-day open->close | +1 day | +5 days | +20 days | +60 days |")
    print("|---|---|---|---|---|---|---|")
    for ln in txt.splitlines():
        m = re.match(r"^(.{52})\s+n=\s*(\d+)\s+open->close ([+-][\d.]+%)(.*)$", ln)
        if not m:
            continue
        cells = re.findall(r"\+(\d+)d xs ([+-][\d.]+%) \(med ([+-][\d.]+%), t~([+-][\d.]+|nan)\)", m.group(4))
        cs = {int(h): f"{x} (median {med}, t ~ {t})" for h, x, med, t in cells}
        print(f"| {m.group(1).strip()} | {int(m.group(2)):,} | {m.group(3)} | " + " | ".join(cs.get(h, "") for h in (1, 5, 20, 60)) + " |")


def para_events(fn, title):
    txt = read(fn)
    if not txt:
        return
    print(f"\n#### {title}\n")
    print("| Definition | Events | +1 day | +3 days | +5 days | +10 days | +20 days |")
    print("|---|---|---|---|---|---|---|")
    for ln in txt.splitlines():
        m = re.match(r"^(.{50})\s+n=\s*(\d+) \| (.*)$", ln)
        if not m:
            continue
        cells = re.findall(r"(\d+)d mean ([+-][\d.]+%) med ([+-][\d.]+%) win (\d+%) worst ([+-]\d+%)", m.group(3))
        cs = {int(h): f"mean {a}, median {b}, {w} win, worst {x}" for h, a, b, w, x in cells}
        print(f"| {m.group(1).strip()} | {int(m.group(2)):,} | " + " | ".join(cs.get(h, "") for h in (1, 3, 5, 10, 20)) + " |")
    for ln in txt.splitlines():
        if re.match(r"^5d run >= 100% \d{4}-\d{4}:", ln):
            print("\n" + ln.strip())


def portfolio(label, title):
    p = os.path.join(R, f"portfolio_stats_{label}.csv")
    if not os.path.exists(p):
        return
    d = pd.read_csv(p)
    print(f"\n#### {title}\n")
    print("| Strategy | CAGR | Vol | Sharpe | Max drawdown | Final multiple | Trades taken / signals | Avg gross exposure |")
    print("|---|---|---|---|---|---|---|---|")
    for _, r in d.iterrows():
        print(f"| {r['name']} | {r['cagr']:+.1%} | {r['vol']:.1%} | {r['sharpe']:.2f} | {r['maxdd']:.1%} | {r['final_mult']:.2f}x | "
              f"{int(r['taken']):,} / {int(r['signals']):,} | {r['avg_gross']:.0%} |")
    y = pd.read_csv(os.path.join(R, f"portfolio_yearly_{label}.csv"), index_col=0)
    cols = [c for c in y.columns if c in ("Breakout Q0 (regime filter)", "Breakout Q0, no regime filter",
                                           "Earnings EP, close entry, 50-day trail", "Earnings EP, close entry, his 3-5d/10-day rules",
                                           "Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow") or "buy & hold" in c]
    print(f"\nCalendar-year returns, {title} (%):\n")
    print("| Year | " + " | ".join(cols) + " |")
    print("|---|" + "---|" * len(cols))
    for yr, r in y[cols].iterrows():
        print(f"| {int(yr)} | " + " | ".join("n/a" if pd.isna(v) else f"{v*100:+.1f}" for v in r.values) + " |")
    for ln in read(f"portfolio_log_{label}.txt").splitlines():
        if ln.startswith("Factor regression"):
            print("\n" + ln.strip())


def clustered_table(fn, title):
    c = clustered(fn)
    if not c:
        return
    print(f"\n#### {title}\n")
    print("| Setup | Trades | Avg R | t naive | t month-clustered | Avg return | t of return, clustered |")
    print("|---|---|---|---|---|---|---|")
    for k, (mR, tn, tc, mr, tcr, n) in c.items():
        print(f"| {k} | {n:,} | {mR:+.3f} | {tn:+.1f} | {tc:+.1f} | {mr:+.2f}% | {tcr:+.1f} |")


def misc(fn, keys):
    for ln in read(fn).splitlines():
        if any(ln.startswith(k) or ln.strip().startswith(k) for k in keys):
            print("\n" + ln.strip())


print("## Generated result tables\n")
print("Machine-generated from `backtest/results/` by `src/make_tables.py`. Panel A = main snapshot (survivors only), "
      "2005-01-03 to 2026-11-17. Panel B = delisting-inclusive data, 2019-07-01 to 2026-01-28. 'A-window' = Panel A "
      "restricted to Panel B's dates. Long trades cost 15 bp per fill, shorts 50 bp per fill plus 50% a year borrow, "
      "unless the label says otherwise. t (naive) treats trades as independent.")

print("\n### T1. The scan universe on its own (20-day forward return minus SPY unless the row says otherwise)")
universe("universe_log_hf.txt", "Panel A")
universe("universe_log_dolt.txt", "Panel B")

print("\n### T2. Breakouts")
variants("breakout_variants.csv", "Breakout variants, Panel A")
misc("breakout_log.txt", ("Control", "n per run", "Q0 profit concentration", "exit reasons", "regime-on share"))
by_year("breakout_by_year_Q0.csv", "Q0 baseline by year, Panel A")
by_year("breakout_by_year_Q0_noregime.csv", "Q0 without the regime filter by year, Panel A")
variants("breakout_variants_dolt.csv", "Breakout variants, Panel B", eras=False)
misc("breakout_log_dolt.txt", ("n per run", "Q0 profit concentration"))
variants("breakout_variants_hfwin.csv", "Breakout variants, A-window", eras=False)
misc("breakout_log_hfwin.txt", ("n per run",))

print("\n### T3. Episodic pivots")
ep_events("ep_log.txt", "Event study, Panel A: return after the gap-day close, minus SPY")
variants("ep_variants.csv", "EP trade variants, Panel A")
misc("ep_log.txt", ("E-close profit concentration",))
by_year("ep_by_year_Eclose.csv", "EP bought at the close, standard rules, by year, Panel A")
by_year("ep_by_year_Eclose_earn_sma20.csv", "Earnings EP, 20-day trail, by year, Panel A")
ep_events("ep_log_dolt.txt", "Event study, Panel B")
variants("ep_variants_dolt.csv", "EP trade variants, Panel B", eras=False)
ep_events("ep_log_hfwin.txt", "Event study, A-window")
variants("ep_variants_hfwin.csv", "EP trade variants, A-window", eras=False)

print("\n### T4. Parabolic shorts")
para_events("parabolic_log.txt", "Event study, Panel A: profit of a short opened at the next open, no stop, no costs")
variants("parabolic_variants.csv", "Parabolic-short variants, Panel A")
by_year("parabolic_by_year_Pred.csv", "First-red-day short by year, Panel A")
misc("parabolic_log.txt", ("exit reasons",))
para_events("parabolic_log_dolt.txt", "Event study, Panel B")
variants("parabolic_variants_dolt.csv", "Parabolic-short variants, Panel B", eras=False)
para_events("parabolic_log_hfwin.txt", "Event study, A-window")
variants("parabolic_variants_hfwin.csv", "Parabolic-short variants, A-window", eras=False)

print("\n### T5. Portfolio level ($100,000 start, 0.5% risk per trade)")
portfolio("hf", "Panel A, 2005-01-03 to 2026-11-17")
portfolio("dolt", "Panel B, 2019-07-01 to 2026-01-28")

print("\n### T6. Month-clustered significance")
clustered_table("clustered_t_hf.txt", "Panel A")
clustered_table("clustered_t_dolt.txt", "Panel B")

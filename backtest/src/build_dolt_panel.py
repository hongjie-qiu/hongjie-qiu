"""Build a delisting-inclusive OHLCV panel from the Hugging Face `siddharthmb/stocks-*` export
(same schema as the DoltHub `post-no-preference/stocks` database).

Usage:
    python3 -I build_dolt_panel.py <dolt_dir> <hf_defeatbeta_dir> <out_dir>

Why a second panel: the main snapshot only has tickers still listed in 2024-2026.  This export is a
daily point-in-time record, so tickers that were later delisted (TWTR, SIVB, ATVI, ...) are present
with their history.  Coverage of then-listed stocks is essentially complete from mid-2019, so results
on this panel for 2019-07 onward are free of survivorship bias.  Prices in the file are RAW; they are
back-adjusted here with split events that are validated against the actual overnight price change.
"""
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import duckdb
from qm.clean import repair_scaling_glitches, clean_bars

dolt_dir, hf_dir, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out_dir, exist_ok=True)
BENCH = {"SPY", "QQQ", "IWM", "QQQM", "DIA", "MDY"}

con = duckdb.connect()
con.execute("PRAGMA threads=4")
con.execute("PRAGMA memory_limit='6GB'")
con.execute(
    f"""create table px as select cast(date as date) d, act_symbol symbol,
               cast(open as double) o, cast(high as double) h, cast(low as double) l,
               cast(close as double) c, cast(volume as double) v
        from read_csv('{dolt_dir}/ohlcv.csv', header=true,
                      columns={{'date':'VARCHAR','act_symbol':'VARCHAR','open':'VARCHAR','high':'VARCHAR',
                               'low':'VARCHAR','close':'VARCHAR','volume':'VARCHAR'}})
        where try_cast(close as double) is not null"""
)
print("rows:", con.execute("select count(*), min(d), max(d), count(distinct symbol) from px").fetchone())

# ---------------------------------------------------------------- classification from security names
sym_rows = con.execute(
    f"""select act_symbol, security_name, is_etf, is_test_issue
        from read_csv('{dolt_dir}/symbol.csv', header=true, all_varchar=true)"""
).fetchall()
EXCL = re.compile(
    r"warrant|\bunits?\b|\brights?\b|preferred|\bpfd\b|depositary shares? (each )?represent\w* .*(interest|preferred)"
    r"|notes?\b.*\bdue\b|\bdue 20\d\d|debenture|%|\betn\b|\bfund\b|subordinated|senior notes|contingent value"
    r"|\bbond\b|income shares|trust preferred|when[- ]issued|\bwi\b$|tracking etf|\betf\b",
    re.I,
)
KEEP_UNITS = re.compile(r"common units|limited partner", re.I)


def classify(sym, name, is_etf, is_test):
    if sym in BENCH:
        return "bench"
    if is_etf in ("1", "true", "True") or is_test in ("1", "true", "True"):
        return "x_etf_or_test"
    name = name or ""
    if EXCL.search(name) and not KEEP_UNITS.search(name):
        return "x_name"
    if not re.fullmatch(r"[A-Z]{1,5}([.\-][A-Z])?", sym or ""):
        return "x_symbol"
    return "common"


kind = {r[0]: classify(*r) for r in sym_rows}
names = {r[0]: (r[1] or "").strip() for r in sym_rows}
px_syms = [r[0] for r in con.execute("select distinct symbol from px").fetchall()]
for s in px_syms:
    kind.setdefault(s, "x_unknown")  # traded but absent from the symbol master
keep = sorted(s for s in px_syms if kind[s] in ("common", "bench"))
print("classification of traded symbols:", Counter(kind[s] for s in px_syms))

dates = np.array([r[0] for r in con.execute("select distinct d from px where symbol='SPY' order by d").fetchall()],
                 dtype="datetime64[D]")
n_d, n_s = len(dates), len(keep)
print("calendar:", dates[0], "->", dates[-1], n_d, "days;", n_s, "symbols")
con.execute("create table sym(symbol varchar, j integer)")
con.executemany("insert into sym values (?, ?)", [(s, j) for j, s in enumerate(keep)])
con.execute("create table cal(d date, i integer)")
con.executemany("insert into cal values (?, ?)", [(str(d), i) for i, d in enumerate(dates)])
res = con.execute("select cal.i, sym.j, o, h, l, c, v from px join sym using(symbol) join cal using(d)").fetchnumpy()
ii, jj = res["i"].astype(np.int64), res["j"].astype(np.int64)
F = {}
for name, key in (("open", "o"), ("high", "h"), ("low", "l"), ("close", "c"), ("volume", "v")):
    a = np.full((n_d, n_s), np.nan, dtype=np.float32)
    a[ii, jj] = res[key].astype(np.float32)
    F[name] = a
del res
con.execute("drop table px")
O, H, L, C, V = (F[k] for k in ("open", "high", "low", "close", "volume"))
print("bars dropped / repaired:", clean_bars(O, H, L, C, V))
RAW = C.copy()  # as-traded close

# ---------------------------------------------------------------- split one ticker into separate
# instruments when it disappears for > 20 sessions (ticker reuse by a different company)
col = {s: j for j, s in enumerate(keep)}
extra_cols = []
n_reuse = 0
for j in range(n_s):
    idx = np.nonzero(np.isfinite(C[:, j]))[0]
    if len(idx) < 2:
        continue
    gaps = np.nonzero(np.diff(idx) > 20)[0]
    if len(gaps) == 0 or keep[j] in BENCH:
        continue
    # keep the last run in place, move earlier runs to new columns
    starts = [idx[0]] + [idx[g + 1] for g in gaps]
    ends = [idx[g] for g in gaps] + [idx[-1]]
    for r, (a, b) in enumerate(zip(starts[:-1], ends[:-1])):
        block = {k: F[k][a:b + 1, j].copy() for k in F}
        raw_block = RAW[a:b + 1, j].copy()
        for k in F:
            F[k][a:b + 1, j] = np.nan
        RAW[a:b + 1, j] = np.nan
        if b - a + 1 >= 60:
            extra_cols.append((f"{keep[j]}~{r + 1}", a, b, block, raw_block, keep[j]))
        n_reuse += 1
if extra_cols:
    add = len(extra_cols)
    for k in list(F):
        F[k] = np.concatenate([F[k], np.full((n_d, add), np.nan, dtype=np.float32)], axis=1)
    RAW = np.concatenate([RAW, np.full((n_d, add), np.nan, dtype=np.float32)], axis=1)
    for q, (nm, a, b, block, raw_block, parent) in enumerate(extra_cols):
        for k in F:
            F[k][a:b + 1, n_s + q] = block[k]
        RAW[a:b + 1, n_s + q] = raw_block
        keep.append(nm)
        kind[nm] = kind[parent]
        names[nm] = names.get(parent, "")
    O, H, L, C, V = (F[k] for k in ("open", "high", "low", "close", "volume"))
    n_s = len(keep)
    col = {s: j for j, s in enumerate(keep)}
print("ticker-reuse segments separated:", n_reuse, "| kept as own columns:", len(extra_cols))

# ---------------------------------------------------------------- split adjustment (validated)
cands = []
for sym, d, to_f, for_f in con.execute(
    f"select act_symbol, cast(ex_date as date), cast(to_factor as double), cast(for_factor as double) "
    f"from read_csv('{dolt_dir}/split.csv', header=true, all_varchar=true)"
).fetchall():
    if for_f and to_f:
        cands.append((sym, np.datetime64(d), to_f / for_f, "dolt"))
if os.path.exists(os.path.join(hf_dir, "stock_split_events.parquet")):
    for sym, d, fac in con.execute(
        f"select symbol, cast(report_date as date), split_factor from read_parquet('{hf_dir}/stock_split_events.parquet')"
    ).fetchall():
        try:
            a, b = fac.split(":")
            cands.append((sym.replace("-", "."), np.datetime64(d), float(a) / float(b), "yahoo"))
            cands.append((sym, np.datetime64(d), float(a) / float(b), "yahoo"))
        except Exception:
            pass
splitday = np.zeros((n_d, n_s), dtype=bool)
applied = set()
stat = Counter()
for sym, d, r, src in sorted(cands, key=lambda x: (x[0], x[1], x[3])):
    j = col.get(sym)
    if j is None or not np.isfinite(r) or r <= 0 or abs(np.log(r)) < 1e-6:
        continue
    i = int(np.searchsorted(dates, d))
    if i <= 0 or i >= n_d or dates[i] != d:
        stat["no_bar"] += 1
        continue
    # previous valid bar
    k = i - 1
    while k >= 0 and not np.isfinite(RAW[k, j]):
        k -= 1
    if k < 0 or not np.isfinite(O[i, j]):
        stat["no_prev"] += 1
        continue
    key = (j, i)
    if key in applied:
        continue
    g = float(O[i, j]) / float(RAW[k, j])  # observed overnight ratio on the raw series (O is still raw here)
    informative = abs(np.log(r)) >= np.log(1.5)
    ok = abs(np.log(g * r)) < np.log(1.35)
    if informative and not ok:
        stat[f"rejected_{src}"] += 1
        continue
    if not informative and src != "dolt":
        continue
    for a_ in (O, H, L, C):
        a_[:i, j] /= r
    V[:i, j] *= r
    splitday[i, j] = True
    applied.add(key)
    stat[f"applied_{src}"] += 1
print("split candidates:", dict(stat))

nb, nr, at, rescaled = repair_scaling_glitches(O, H, L, C, V)
print("scaling glitches repaired: blanked", nb, "| rescaled as missing split", nr)
for b, j in at:
    splitday[b, j] = True
RAW[~np.isfinite(C)] = np.nan

# ---------------------------------------------------------------- save
for name in ("open", "high", "low", "close", "volume"):
    np.save(os.path.join(out_dir, f"{name}.npy"), F[name])
np.save(os.path.join(out_dir, "rawclose.npy"), RAW)
np.save(os.path.join(out_dir, "splitday.npy"), splitday)
np.save(os.path.join(out_dir, "dates.npy"), dates)
with open(os.path.join(out_dir, "symbols.txt"), "w") as f:
    f.write("\n".join(keep) + "\n")
has = np.isfinite(C)
first = has.argmax(axis=0)
last = n_d - 1 - has[::-1].argmax(axis=0)
with open(os.path.join(out_dir, "meta.csv"), "w") as f:
    f.write("symbol,sector,industry,kind,first_date,last_date,n_bars\n")
    for j, s in enumerate(keep):
        nm = names.get(s, "").replace('"', "'")
        f.write(f'{s},"","{nm}",{kind[s]},{dates[first[j]]},{dates[last[j]]},{int(has[:, j].sum())}\n')
alive = has[-1]
print("saved", out_dir, "| columns:", n_s, "| common:", sum(kind[s] == "common" for s in keep),
      "| common columns not trading on the last day (delisted/renamed):",
      int(sum((not alive[j]) and kind[s] == "common" for j, s in enumerate(keep))))

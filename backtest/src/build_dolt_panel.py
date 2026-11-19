"""Build a delisting-inclusive OHLCV panel from the Hugging Face `siddharthmb/stocks-*` export
(same schema as the DoltHub `post-no-preference/stocks` database).

Usage:
    python3 -I build_dolt_panel.py <dolt_dir> <hf_defeatbeta_dir> <calendar.npy> <sec_announcements.parquet> <out_dir>

Why a second panel: the main snapshot only has tickers still listed in 2024-2026.  This export is a
daily point-in-time record, so tickers that were later delisted (TWTR, SIVB, ATVI, ...) are present
with their history.  Coverage of then-listed stocks is essentially complete from mid-2019, so results
on this panel for 2019-07 onward are free of survivorship bias.

What this script has to get right (each item was a defect found by the code audit of the first version):
  * calendar  - the file has rows on some market holidays and lacks SPY rows on some trading days, so
                the trading calendar is taken from the main panel (Yahoo SPY) instead of from the file;
  * splits    - prices are RAW; every recorded split is validated against the actual overnight price
                change, searched within +/-3 sessions of the stated ex-date, and applied before a ticker
                is cut into segments;
  * reuse     - a ticker that disappears for > 20 sessions is cut into separate instruments; the symbol
                master only describes the ticker's latest owner, so for tickers that are an ETF or a
                preferred today, an earlier segment is kept as common stock when SEC earnings filings
                (8-K item 2.02) exist for that ticker inside the segment (e.g. FB 2012-2022).
"""
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import duckdb
from qm.clean import repair_scaling_glitches, clean_bars

dolt_dir, hf_dir, cal_path, sec_path, out_dir = sys.argv[1:6]
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
d_lo, d_hi = con.execute("select min(d), max(d) from px").fetchone()
print("rows:", con.execute("select count(*), count(distinct symbol) from px").fetchone(), d_lo, "->", d_hi)

# ---------------------------------------------------------------- trading calendar from the main panel
ref = np.load(cal_path)
dates = ref[(ref >= np.datetime64(d_lo)) & (ref <= np.datetime64(d_hi))]
file_days = {np.datetime64(r[0]) for r in con.execute("select distinct d from px").fetchall()}
missing = [d for d in dates if d not in file_days]
extra = sorted(d for d in file_days if d not in set(dates))
print("calendar:", dates[0], "->", dates[-1], len(dates), "sessions | trading days with no rows in the file:",
      len(missing), [str(d) for d in missing][:20], "| non-trading days dropped:", len(extra), [str(d) for d in extra][:12])
n_d = len(dates)

# ---------------------------------------------------------------- SEC earnings filings per ticker
sec = {}
for tk, d in con.execute(
    f"select ticker, cast(first_tradeable_session as date) from read_parquet('{sec_path}') "
    f"where ticker is not null and first_tradeable_session is not null"
).fetchall():
    sec.setdefault(tk.replace("-", "."), []).append(np.datetime64(d))
sec = {k: np.sort(np.array(v, dtype="datetime64[D]")) for k, v in sec.items()}

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
    if not re.fullmatch(r"[A-Z]{1,5}([.\-][A-Z])?", sym or ""):
        return "x_symbol"
    if is_etf in ("1", "true", "True") or is_test in ("1", "true", "True"):
        return "x_etf_or_test"
    if EXCL.search(name or "") and not KEEP_UNITS.search(name or ""):
        return "x_name"
    return "common"


kind = {r[0]: classify(*r) for r in sym_rows}
names = {r[0]: (r[1] or "").strip() for r in sym_rows}
px_syms = [r[0] for r in con.execute("select distinct symbol from px").fetchall()]
for s in px_syms:
    kind.setdefault(s, "x_unknown")  # traded but absent from the symbol master
# a ticker that is not a common stock today may have belonged to an operating company earlier:
# load it as "check" when SEC earnings filings exist under that ticker
for s in px_syms:
    if kind[s] in ("x_etf_or_test", "x_name", "x_unknown") and len(sec.get(s, ())) >= 4 \
            and re.fullmatch(r"[A-Z]{1,5}([.\-][A-Z])?", s):
        kind[s] = "check"
keep = sorted(s for s in px_syms if kind[s] in ("common", "bench", "check"))
print("classification of traded symbols:", Counter(kind[s] for s in px_syms))
n_s = len(keep)
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
RAW = C.copy()    # as-traded close
RAWO = O.copy()   # as-traded open, for validating splits
col = {s: j for j, s in enumerate(keep)}

# ---------------------------------------------------------------- split adjustment (validated, +/-3 sessions)
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
            r_ = float(a) / float(b)
        except Exception:
            continue
        for s_ in {sym, sym.replace("-", ".")}:
            cands.append((s_, np.datetime64(d), r_, "yahoo"))


def overnight(i, j):
    """as-traded open of row i over the previous valid as-traded close, or nan"""
    if i <= 0 or i >= n_d or not np.isfinite(RAWO[i, j]):
        return np.nan
    k = i - 1
    while k >= 0 and not np.isfinite(RAW[k, j]):
        k -= 1
    return float(RAWO[i, j]) / float(RAW[k, j]) if k >= 0 else np.nan


splitday = np.zeros((n_d, n_s), dtype=bool)
split_events = {}
applied = set()
stat = Counter()
for sym, d, r, src in sorted(cands, key=lambda x: (x[0], x[1], x[3])):
    j = col.get(sym)
    if j is None or not np.isfinite(r) or r <= 0 or abs(np.log(r)) < 1e-6:
        continue
    i0 = int(np.searchsorted(dates, d))
    if i0 >= n_d:
        continue
    split_events.setdefault(j, []).append((i0, 1.0 / r))
    informative = abs(np.log(r)) >= np.log(1.5)
    hit = None
    order = [i0] + [i0 + k for k in (1, -1, 2, -2, 3, -3)] if informative else [i0]
    for i in order:
        g = overnight(i, j)
        if not np.isfinite(g):
            continue
        if not informative or abs(np.log(g * r)) < np.log(1.35):
            hit = i
            break
    if hit is None:
        stat[f"rejected_{src}" if informative else f"no_bar_{src}"] += 1
        continue
    if not informative and src != "dolt":
        continue
    # one adjustment per (column, +/-3 rows): the two sources often list the same split
    if any((j, hit + k) in applied for k in range(-3, 4)):
        continue
    for a_ in (O, H, L, C):
        a_[:hit, j] /= r
    V[:hit, j] *= r
    splitday[hit, j] = True
    applied.add((j, hit))
    stat[f"applied_{src}" + ("" if hit == i0 else "_shifted")] += 1
print("split candidates:", dict(stat))

nb, nr, nleft, at, rescaled = repair_scaling_glitches(O, H, L, C, V, split_events)
print("scaling glitches: blanked", nb, "| rescaled as missing split", nr, "| left untouched (no corroboration)", nleft)
for b, j in at:
    splitday[b, j] = True
RAW[~np.isfinite(C)] = np.nan

# ---------------------------------------------------------------- cut tickers into instruments
ARR = dict(F)
ARR["rawclose"] = RAW
ARR["splitday"] = splitday
final_names, final_kind, final_parent, blocks = [], [], [], []
n_cut = n_dropped_seg = n_rescued = 0
for j in range(n_s):
    s = keep[j]
    idx = np.nonzero(np.isfinite(C[:, j]))[0]
    if len(idx) == 0:
        continue
    if kind[s] == "bench":
        runs = [(idx[0], idx[-1])]
    else:
        gaps = np.nonzero(np.diff(idx) > 20)[0]
        starts = [idx[0]] + [idx[g + 1] for g in gaps]
        ends = [idx[g] for g in gaps] + [idx[-1]]
        runs = list(zip(starts, ends))
        n_cut += len(runs) - 1
    for r_, (a, b) in enumerate(runs):
        last = r_ == len(runs) - 1
        if kind[s] == "check":
            f_ = sec.get(s, np.array([], dtype="datetime64[D]"))
            n_f = int(((f_ >= dates[a]) & (f_ <= dates[b])).sum())
            if n_f < 2:
                n_dropped_seg += 1
                continue
            n_rescued += 1
        elif not last and b - a + 1 < 60:
            n_dropped_seg += 1
            continue
        # the plain ticker names the latest run of a ticker that is a common stock today; earlier runs,
        # and every kept run of a ticker that is something else today, are named SYM~k
        final_names.append(s if (last and kind[s] in ("common", "bench")) else f"{s}~{r_ + 1}")
        final_kind.append("bench" if kind[s] == "bench" else "common")
        final_parent.append(s)
        blocks.append((j, a, b))
n_f = len(final_names)
OUT = {}
for k_, src in ARR.items():
    out = np.zeros((n_d, n_f), dtype=bool) if src.dtype == bool else np.full((n_d, n_f), np.nan, dtype=np.float32)
    for q, (j, a, b) in enumerate(blocks):
        out[a:b + 1, q] = src[a:b + 1, j]
    OUT[k_] = out
print("ticker-reuse cuts:", n_cut, "| segments dropped (short, or no SEC filings for a non-common ticker):", n_dropped_seg,
      "| segments of now-non-common tickers kept as common:", n_rescued)

# ---------------------------------------------------------------- save
for name in ("open", "high", "low", "close", "volume", "rawclose", "splitday"):
    np.save(os.path.join(out_dir, f"{name}.npy"), OUT[name])
np.save(os.path.join(out_dir, "dates.npy"), dates)
with open(os.path.join(out_dir, "symbols.txt"), "w") as f:
    f.write("\n".join(final_names) + "\n")
has = np.isfinite(OUT["close"])
first = has.argmax(axis=0)
last_ = n_d - 1 - has[::-1].argmax(axis=0)
with open(os.path.join(out_dir, "meta.csv"), "w") as f:
    f.write("symbol,sector,industry,kind,first_date,last_date,n_bars\n")
    for q, s in enumerate(final_names):
        nm = names.get(final_parent[q], "").replace('"', "'")
        f.write(f'{s},"","{nm}",{final_kind[q]},{dates[first[q]]},{dates[last_[q]]},{int(has[:, q].sum())}\n')
alive = has[-1]
n_common = sum(k_ == "common" for k_ in final_kind)
print("saved", out_dir, "| columns:", n_f, "| common:", n_common,
      "| common columns not trading on the last day (delisted/renamed):",
      int(sum((not alive[q]) and final_kind[q] == "common" for q in range(n_f))))
for s_ in ("FB~1", "META", "TWTR", "SIVB", "TOP"):
    if s_ in final_names:
        q = final_names.index(s_)
        print("  check", s_, dates[first[q]], "->", dates[last_[q]], int(has[:, q].sum()), "bars")

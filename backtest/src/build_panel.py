"""Build a dense [day x symbol] OHLCV panel from the Hugging Face `defeatbeta/yahoo-finance-data` snapshot.

Usage:
    python3 -I build_panel.py <hf_dir> <out_dir>

Outputs (float32 .npy, shape [n_days, n_symbols]) in <out_dir>:
    open, high, low, close   split-adjusted prices (Yahoo "Close", NOT dividend-adjusted)
    volume                   split-adjusted share volume
    rawclose                 as-traded (unadjusted) close, rebuilt from the split table
    dates.npy                datetime64[D] trading calendar (SPY trading days)
    symbols.txt              one symbol per line (column order)
    meta.csv                 symbol, sector, industry, kind, first_date, last_date

Notes on what this file is and is not:
  * The snapshot only contains tickers that were still listed in ~2024-2026, so the panel is
    survivorship-biased.  `build_qlib_panel.py` adds a 2020-vintage snapshot to measure that bias.
  * Prices are split-adjusted, so price-level filters must use `rawclose`.
"""
import re
import sys
import os
import numpy as np
import duckdb

hf_dir, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
START = "1999-12-31"

con = duckdb.connect()
con.execute("PRAGMA threads=4")
con.execute(
    f"""create table px as
        select symbol, cast(report_date as date) d,
               cast(open as double) o, cast(high as double) h, cast(low as double) l,
               cast(close as double) c, cast(volume as double) v
        from read_parquet('{hf_dir}/stock_prices.parquet')
        where cast(report_date as date) >= DATE '{START}'"""
)
con.execute(f"create table prof as select symbol, sector, industry from read_parquet('{hf_dir}/stock_profile.parquet')")

# ---------------------------------------------------------------- security classification
BENCH = {"SPY", "QQQ", "IWM", "QQQM", "DIA", "MDY"}
rows = con.execute(
    """select a.symbol, p.sector, p.industry, (p.symbol is not null) has_prof
       from (select distinct symbol from px) a left join prof p using(symbol)"""
).fetchall()


def classify(sym, sector, industry, has_prof):
    """Return 'common', 'bench' or an exclusion reason."""
    if sym in BENCH:
        return "bench"
    if "-" in sym or "." in sym:
        # share classes such as BRK-B / BF-B are common stock; everything else with a dash is a
        # preferred, warrant, unit or right.
        if re.fullmatch(r"[A-Z]{1,4}-[AB]", sym) and sector:
            return "common"
        return "x_dash"
    if not re.fullmatch(r"[A-Z]{1,5}", sym):
        return "x_pattern"
    if len(sym) == 5 and not (sym[-1] in "ABK" or sym == "GOOGL"):
        # five-letter tickers are warrants (W), units (U), rights (R), OTC foreign shares / ADRs
        # (F, Y), bankrupt issuers (Q) or preferreds and notes; only class shares (..A/..B/..K) stay.
        return "x_5th_letter"
    if has_prof and not sector:
        return "x_no_sector"  # ETFs, funds, notes ... (Yahoo gives them no sector)
    if industry == "Shell Companies":
        return "x_shell"
    return "common"  # includes recently-delisted tickers that have no profile row


kind = {r[0]: classify(*r) for r in rows}
meta = {r[0]: (r[1] or "", r[2] or "") for r in rows}
keep = sorted(s for s, k in kind.items() if k in ("common", "bench"))
from collections import Counter

print("classification:", Counter(kind.values()))
print("kept symbols:", len(keep))

# ---------------------------------------------------------------- calendar & pivot
dates = np.array(
    [r[0] for r in con.execute("select distinct d from px where symbol='SPY' order by d").fetchall()],
    dtype="datetime64[D]",
)
n_d, n_s = len(dates), len(keep)
print("calendar:", dates[0], "->", dates[-1], n_d, "days;", n_s, "symbols")
con.execute("create table sym(symbol varchar, j integer)")
con.executemany("insert into sym values (?, ?)", [(s, j) for j, s in enumerate(keep)])
con.execute("create table cal(d date, i integer)")
con.executemany("insert into cal values (?, ?)", [(str(d), i) for i, d in enumerate(dates)])
res = con.execute(
    """select cal.i, sym.j, o, h, l, c, v from px join sym using(symbol) join cal using(d)"""
).fetchnumpy()
ii, jj = res["i"].astype(np.int64), res["j"].astype(np.int64)
print("rows placed:", len(ii))

fields = {}
for name, key in (("open", "o"), ("high", "h"), ("low", "l"), ("close", "c"), ("volume", "v")):
    a = np.full((n_d, n_s), np.nan, dtype=np.float32)
    a[ii, jj] = res[key].astype(np.float32)
    fields[name] = a
del res

# ---------------------------------------------------------------- cleaning
O, H, L, C, V = (fields[k] for k in ("open", "high", "low", "close", "volume"))
bad = ~(np.isfinite(O) & np.isfinite(H) & np.isfinite(L) & np.isfinite(C)) | (O <= 0) | (H <= 0) | (L <= 0) | (C <= 0)
n_bad_price = int((bad & np.isfinite(C)).sum())
for a in (O, H, L, C, V):
    a[bad] = np.nan
# repair bars where high/low do not bracket open/close (rounding or feed glitches)
hi = np.fmax(np.fmax(O, C), H)
lo = np.fmin(np.fmin(O, C), L)
n_fix = int(((hi != H) | (lo != L))[np.isfinite(C)].sum())
H[:] = hi
L[:] = lo
V[~np.isfinite(V)] = 0.0
V[bad] = np.nan
print("bars dropped for non-positive prices:", n_bad_price, "| bars with H/L repaired:", n_fix)

# ---------------------------------------------------------------- drop duplicate series (ticker renames)
# The snapshot sometimes carries one company under both its old and its new ticker (e.g. YY/JOYY).
# Two columns are duplicates when the last 20 closes of the shorter-lived one trace the same path.
has0 = np.isfinite(C)
last0 = n_d - 1 - has0[::-1].argmax(axis=0)
nbars = has0.sum(axis=0)
drop = np.zeros(n_s, dtype=bool)
is_bench = np.array([s in BENCH for s in keep])
for j in range(n_s):
    e = int(last0[j])
    if nbars[j] < 30 or e < 20 or is_bench[j]:
        continue
    w = C[e - 19:e + 1, j]
    if not np.isfinite(w).all():
        continue
    # compare price *paths* (each window scaled by its last bar) so that two copies of one company
    # carrying different split adjustments are still recognised; require some movement in the window
    wn = w / w[-1]
    if wn.max() - wn.min() < 0.02:
        continue
    blk = C[e - 19:e + 1, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        same = np.isclose(blk / blk[-1:, :], wn[:, None], rtol=2e-3, atol=0).all(axis=0)
    same[j] = False
    for k in np.nonzero(same)[0]:
        if is_bench[k] or drop[k] or drop[j]:
            continue
        # keep the column with more history; tie -> keep the one that is still trading
        loser = j if (nbars[j], last0[j]) < (nbars[k], last0[k]) else k
        drop[loser] = True
print("duplicate series dropped:", int(drop.sum()), [keep[j] for j in np.nonzero(drop)[0][:40]])
if drop.any():
    sel = ~drop
    keep = [s for s, d in zip(keep, drop) if not d]
    for name in list(fields):
        fields[name] = np.ascontiguousarray(fields[name][:, sel])
    O, H, L, C, V = (fields[k] for k in ("open", "high", "low", "close", "volume"))
    n_s = len(keep)

# ---------------------------------------------------------------- repair scaling glitches
# Signature of a vendor scaling error (misdated or missing reverse-split adjustment): the close jumps
# by a factor r >= 5 while share volume falls by about the same factor, i.e. dollar volume is roughly
# continuous.  A genuine spike shows the opposite (volume explodes).  If the jump reverses within 10
# bars the bars in between are blanked; otherwise all earlier bars are rescaled like a split.
glitch_blank = glitch_rescale = 0
glitch_at = []
rescaled = []
for j in range(n_s):
    c = C[:, j]
    idx = np.nonzero(np.isfinite(c))[0]
    if len(idx) < 3:
        continue
    cv = c[idx].astype(np.float64)
    vv = V[idx, j].astype(np.float64)
    ratio = cv[1:] / cv[:-1]
    cand = np.nonzero(ratio >= 5.0)[0]
    for k in cand:
        a, b = idx[k], idx[k + 1]          # jump between bar a and bar b
        r = C[b, j] / C[a, j] if np.isfinite(C[a, j]) and np.isfinite(C[b, j]) else np.nan
        if not np.isfinite(r) or r < 5.0 or not (vv[k] > 0) or vv[k + 1] / vv[k] > 2.0 / r:
            continue
        end = None
        for m in range(k + 1, min(k + 11, len(idx) - 1)):
            if cv[m + 1] / cv[m] <= 2.0 / r:
                end = idx[m + 1]
                break
        if end is not None:
            for a_ in (O, H, L, C, V):
                a_[b:end, j] = np.nan
            glitch_blank += 1
        else:
            for a_ in (O, H, L, C):
                a_[:b, j] *= r
            V[:b, j] /= r
            glitch_rescale += 1
            rescaled.append((b, j, r))
        glitch_at.append((b, j))
print("scaling glitches repaired: blanked", glitch_blank, "| rescaled as missing split", glitch_rescale)

# ---------------------------------------------------------------- as-traded close from the split table
splits = con.execute(
    f"select symbol, cast(report_date as date) d, split_factor from read_parquet('{hf_dir}/stock_split_events.parquet')"
).fetchall()
col = {s: j for j, s in enumerate(keep)}
mult = np.ones((n_d, n_s), dtype=np.float32)
splitday = np.zeros((n_d, n_s), dtype=bool)  # ex-dates, used to quarantine signals around splits
n_used = 0
for sym, d, fac in splits:
    j = col.get(sym)
    if j is None or not fac or ":" not in fac:
        continue
    try:
        a, b = fac.split(":")
        ratio = float(a) / float(b)
    except ValueError:
        continue
    if not np.isfinite(ratio) or ratio <= 0:
        continue
    # bars strictly before the ex-date were divided by `ratio` in the adjusted series
    i = int(np.searchsorted(dates, np.datetime64(d)))
    if i > 0:
        mult[:i, j] *= ratio
        n_used += 1
    if i < n_d:
        splitday[i, j] = True
for b, j in glitch_at:
    splitday[b, j] = True  # quarantine signals around repaired bars as well
rawclose = C * mult
for b, j, r in rescaled:
    rawclose[:b, j] /= r  # the as-traded price is the vendor's original number, not the rescaled one
print("split events applied:", n_used)

# ---------------------------------------------------------------- save
for name, a in fields.items():
    np.save(os.path.join(out_dir, f"{name}.npy"), a)
np.save(os.path.join(out_dir, "rawclose.npy"), rawclose.astype(np.float32))
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
        sec, ind = meta[s]
        f.write(
            f'{s},"{sec}","{ind}",{kind[s]},{dates[first[j]]},{dates[last[j]]},{int(has[:, j].sum())}\n'
        )
print("saved to", out_dir)

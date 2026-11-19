"""Earnings-reaction-day matrix from the Nasdaq earnings calendar dump.

The calendar lists, per calendar date, the companies reporting that day with a coarse time flag.
A gap on trading day t is treated as an earnings reaction if the company reported
  * on date(t) with flag pre-market or unspecified, or
  * on the previous trading day with flag after-hours or unspecified.
Caveat: the calendar only covers companies that are still listed today, so it is itself a
survivor sample; missing rows are treated as "not an earnings day".
"""
import json
import os
import numpy as np


def _num(x):
    if x is None:
        return np.nan
    s = str(x).replace("$", "").replace(",", "").replace("(", "-").replace(")", "").strip()
    try:
        return float(s)
    except ValueError:
        return np.nan


def load_calendar(cal_dir):
    """Return list of (date64, symbol, time_flag, eps, forecast, surprise_pct, n_est)."""
    out = []
    for fn in sorted(os.listdir(cal_dir)):
        if not fn.endswith(".json"):
            continue
        d = np.datetime64(fn[:10])
        with open(os.path.join(cal_dir, fn)) as f:
            rows = json.load(f)
        for r in rows:
            sym = (r.get("symbol") or "").strip().upper().replace(".", "-").replace("/", "-")
            if not sym:
                continue
            out.append((d, sym, r.get("time") or "", _num(r.get("eps")), _num(r.get("epsForecast")),
                        _num(r.get("surprise")), _num(r.get("noOfEsts"))))
    return out


def reaction_matrix(p, cal_dir):
    """Bool [T,S] matrix of earnings-reaction candidate days plus a float matrix of EPS surprise %."""
    dates = p["dates"]
    col = p["col"]
    T, S = len(dates), len(p["symbols"])
    E = np.zeros((T, S), dtype=bool)
    SUR = np.full((T, S), np.nan, dtype=np.float32)
    n_rows = n_hit = 0
    for d, sym, tflag, eps, fc, sur, nest in load_calendar(cal_dir):
        n_rows += 1
        j = col.get(sym)
        if j is None:
            continue
        i = int(np.searchsorted(dates, d))  # first trading day >= report date
        if i >= T:
            continue
        n_hit += 1
        same_day = dates[i] == d
        days = []
        if same_day and tflag != "time-after-hours":
            days.append(i)
        if tflag != "time-pre-market":
            days.append(i + 1 if same_day else i)
        if not same_day and tflag == "time-pre-market":
            days.append(i)
        for k in days:
            if k < T:
                E[k, j] = True
                if np.isfinite(sur):
                    SUR[k, j] = sur
    return E, SUR, {"calendar_rows": n_rows, "matched_rows": n_hit}


def reaction_matrix_sec(p, ann_path, ident_path=None, current=False):
    """Earnings-reaction days from SEC 8-K Item 2.02 filings (Hugging Face `ZipLime/earnings-calendar`).

    Each filing carries the ticker as of the filing day and `first_tradeable_session`, the first session in
    which the release can be traded (same day for pre-market and intraday releases, next session for
    after-close releases).  Delisted companies are included.
      current=False : match on the as-of ticker (right for a point-in-time panel)
      current=True  : map the filer (CIK) to its current ticker first (right for a panel keyed by today's
                      tickers, e.g. Facebook filings -> META), falling back to the as-of ticker.
    Returns (bool [T,S], info dict).
    """
    import duckdb

    con = duckdb.connect()
    rows = con.execute(
        f"""select cik, ticker, cast(first_tradeable_session as varchar)
            from read_parquet('{ann_path}')
            where first_tradeable_session is not null"""
    ).fetchall()
    cur = {}
    if current and ident_path:
        for cik, val in con.execute(
            f"select cik, value from read_parquet('{ident_path}') where kind='ticker' and is_current"
        ).fetchall():
            cur.setdefault(cik, []).append(val)
    dates = p["dates"]
    col = p["col"]
    T, S = len(dates), len(p["symbols"])
    E = np.zeros((T, S), dtype=bool)
    n_hit = 0

    def find(sym):
        if not sym:
            return None
        for cand in (sym, sym.replace(".", "-"), sym.replace("-", ".")):
            j = col.get(cand)
            if j is not None:
                return j
        return None

    for cik, ticker, fts in rows:
        j = None
        if current:
            for t in cur.get(cik, []):
                j = find(t)
                if j is not None:
                    break
        if j is None:
            j = find(ticker)
        if j is None:
            continue
        i = int(np.searchsorted(dates, np.datetime64(fts)))
        if i >= T:
            continue
        E[i, j] = True
        n_hit += 1
    return E, {"filings": len(rows), "matched": n_hit, "source": "SEC 8-K item 2.02"}

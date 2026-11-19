"""Benchmark helpers: Nasdaq-100 proxy and total-return series for ETFs."""
import numpy as np


def nasdaq_proxy(p):
    """QQQ close; the snapshot's QQQ series stops in Sep 2026, so later days are spliced from QQQM returns."""
    C = np.asarray(p["close"])
    q = C[:, p["col"]["QQQ"]].astype(np.float64).copy()
    if "QQQM" in p["col"]:
        q2 = C[:, p["col"]["QQQM"]].astype(np.float64)
        valid = np.where(np.isfinite(q))[0]
        last = valid[-1]
        for i in range(last + 1, len(q)):
            if np.isfinite(q2[i]) and np.isfinite(q2[i - 1]):
                q[i] = q[i - 1] * q2[i] / q2[i - 1]
            else:
                q[i] = q[i - 1]
    return q


def total_return_index(p, symbol, dividends=None):
    """Total-return index for one symbol. `dividends` maps date64 -> cash amount (split-adjusted)."""
    C = np.asarray(p["close"])
    c = C[:, p["col"][symbol]].astype(np.float64)
    dates = p["dates"]
    tr = np.full(len(c), np.nan)
    prev = None
    level = 1.0
    for i in range(len(c)):
        if not np.isfinite(c[i]):
            if prev is not None:
                tr[i] = level
            continue
        if prev is not None:
            d = 0.0 if dividends is None else dividends.get(dates[i], 0.0)
            level *= (c[i] + d) / prev
        tr[i] = level
        prev = c[i]
    return tr


def load_dividends(hf_dir, symbol):
    """Dividends for a symbol from the Hugging Face snapshot, keyed by ex-date."""
    import duckdb

    rows = duckdb.connect().execute(
        f"select cast(report_date as date), cast(amount as double) from read_parquet('{hf_dir}/stock_dividend_events.parquet') where symbol=?",
        [symbol],
    ).fetchall()
    return {np.datetime64(d): a for d, a in rows}

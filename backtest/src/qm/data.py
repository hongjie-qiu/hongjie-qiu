"""Panel loading and indicator computation.

All indicator arrays are shaped [n_days, n_symbols] and are *as of the close of that row's day*.
Signals that act on day t must therefore read row t-1.
"""
import os
import numpy as np
import numba as nb


def load_panel(path):
    """Load the dense OHLCV panel written by build_panel.py / build_qlib_panel.py."""
    p = {}
    for k in ("open", "high", "low", "close", "volume", "rawclose"):
        p[k] = np.load(os.path.join(path, f"{k}.npy"), mmap_mode="r")
    sp = os.path.join(path, "splitday.npy")
    p["splitday"] = np.load(sp, mmap_mode="r") if os.path.exists(sp) else None
    p["dates"] = np.load(os.path.join(path, "dates.npy"))
    with open(os.path.join(path, "symbols.txt")) as f:
        p["symbols"] = f.read().split()
    p["col"] = {s: j for j, s in enumerate(p["symbols"])}
    meta = {}
    with open(os.path.join(path, "meta.csv")) as f:
        header = f.readline().strip().split(",")
        import csv

        for row in csv.reader(f):
            meta[row[0]] = dict(zip(header, row))
    p["meta"] = meta
    return p


@nb.njit(parallel=True, cache=True)
def rolling_mean(a, n, min_n):
    """Trailing mean over the last n rows (inclusive), NaN-aware; needs >= min_n valid points."""
    T, S = a.shape
    out = np.full((T, S), np.nan, dtype=np.float32)
    for j in nb.prange(S):
        s = 0.0
        c = 0
        for i in range(T):
            x = a[i, j]
            if np.isfinite(x):
                s += x
                c += 1
            if i >= n:
                y = a[i - n, j]
                if np.isfinite(y):
                    s -= y
                    c -= 1
            if c >= min_n:
                out[i, j] = s / c
    return out


@nb.njit(parallel=True, cache=True)
def rolling_max(a, n):
    """Trailing max over the last n rows (inclusive); NaNs ignored; NaN if no valid point."""
    T, S = a.shape
    out = np.full((T, S), np.nan, dtype=np.float32)
    for j in nb.prange(S):
        for i in range(T):
            m = -np.inf
            lo = i - n + 1
            if lo < 0:
                lo = 0
            for k in range(lo, i + 1):
                x = a[k, j]
                if x > m:
                    m = x
            if m > -np.inf:
                out[i, j] = m
    return out


@nb.njit(parallel=True, cache=True)
def rolling_min(a, n):
    T, S = a.shape
    out = np.full((T, S), np.nan, dtype=np.float32)
    for j in nb.prange(S):
        for i in range(T):
            m = np.inf
            lo = i - n + 1
            if lo < 0:
                lo = 0
            for k in range(lo, i + 1):
                x = a[k, j]
                if x < m:
                    m = x
            if m < np.inf:
                out[i, j] = m
    return out


@nb.njit(parallel=True, cache=True)
def days_since_max(a, n):
    """Number of rows since the highest value in the trailing n-row window (0 = today is the high)."""
    T, S = a.shape
    out = np.full((T, S), -1, dtype=np.int16)
    for j in nb.prange(S):
        for i in range(T):
            m = -np.inf
            arg = -1
            lo = i - n + 1
            if lo < 0:
                lo = 0
            for k in range(lo, i + 1):
                x = a[k, j]
                if x >= m:  # latest occurrence of the max
                    m = x
                    arg = k
            if arg >= 0:
                out[i, j] = i - arg
    return out


@nb.njit(parallel=True, cache=True)
def pct_change_n(c, n):
    """c[t] / c[t-n] - 1 using calendar rows (NaN if either end is missing)."""
    T, S = c.shape
    out = np.full((T, S), np.nan, dtype=np.float32)
    for j in nb.prange(S):
        for i in range(n, T):
            a = c[i - n, j]
            b = c[i, j]
            if np.isfinite(a) and np.isfinite(b) and a > 0:
                out[i, j] = b / a - 1.0
    return out


@nb.njit(parallel=True, cache=True)
def xs_pct_rank(x, mask):
    """Cross-sectional percentile rank (0..1) of x within `mask` on each row; NaN elsewhere."""
    T, S = x.shape
    out = np.full((T, S), np.nan, dtype=np.float32)
    for i in nb.prange(T):
        idx = np.empty(S, dtype=np.int64)
        n = 0
        for j in range(S):
            if mask[i, j] and np.isfinite(x[i, j]):
                idx[n] = j
                n += 1
        if n < 20:
            continue
        vals = np.empty(n, dtype=np.float64)
        for k in range(n):
            vals[k] = x[i, idx[k]]
        order = np.argsort(vals)
        for r in range(n):
            out[i, idx[order[r]]] = (r + 0.5) / n
    return out


@nb.njit(parallel=True, cache=True)
def true_range(h, l, c):
    T, S = c.shape
    out = np.full((T, S), np.nan, dtype=np.float32)
    for j in nb.prange(S):
        for i in range(T):
            hi = h[i, j]
            lo = l[i, j]
            if not (np.isfinite(hi) and np.isfinite(lo)):
                continue
            tr = hi - lo
            if i > 0:
                pc = c[i - 1, j]
                if np.isfinite(pc):
                    tr = max(tr, abs(hi - pc), abs(lo - pc))
            out[i, j] = tr
    return out


@nb.njit(parallel=True, cache=True)
def consec_up(c):
    """Number of consecutive higher closes ending today."""
    T, S = c.shape
    out = np.zeros((T, S), dtype=np.int16)
    for j in nb.prange(S):
        run = 0
        for i in range(1, T):
            a = c[i - 1, j]
            b = c[i, j]
            if np.isfinite(a) and np.isfinite(b) and b > a:
                run += 1
            else:
                run = 0
            out[i, j] = run
    return out


def compute_features(p, cache_dir=None, price_min=3.0, dv_min=3e6):
    """Compute the indicator set used by all three setups.  Returns a dict of arrays.

    Base universe for cross-sectional momentum ranks: common stock, as-traded close >= price_min,
    20-day average dollar volume >= dv_min, traded today.
    """
    names = [
        "sma10", "sma20", "sma50", "adr20", "atr14", "dv20", "vol50",
        "ret21", "ret63", "ret126", "rk21", "rk63", "rk126", "base",
        "gain22", "gain65", "gain126", "gk22", "gk65", "gk126",
    ]
    if cache_dir and all(os.path.exists(os.path.join(cache_dir, n + ".npy")) for n in names):
        return {n: np.load(os.path.join(cache_dir, n + ".npy"), mmap_mode="r") for n in names}

    O = np.asarray(p["open"]); H = np.asarray(p["high"]); L = np.asarray(p["low"])
    C = np.asarray(p["close"]); V = np.asarray(p["volume"]); R = np.asarray(p["rawclose"])
    f = {}
    # averages over the valid closes in the window; a few missing bars (halts, vendor holes) must not
    # blank the average for the next n rows, which would silently switch off trailing exits
    f["sma10"] = rolling_mean(C, 10, 8)
    f["sma20"] = rolling_mean(C, 20, 16)
    f["sma50"] = rolling_mean(C, 50, 40)
    with np.errstate(divide="ignore", invalid="ignore"):
        hl = (H / L - 1.0).astype(np.float32)
        dv = (C.astype(np.float64) * V.astype(np.float64)).astype(np.float32)
    f["adr20"] = rolling_mean(hl, 20, 15)
    f["atr14"] = rolling_mean(true_range(H, L, C), 14, 10)
    f["dv20"] = rolling_mean(dv, 20, 15)
    f["vol50"] = rolling_mean(V, 50, 20)
    f["ret21"] = pct_change_n(C, 21)
    f["ret63"] = pct_change_n(C, 63)
    f["ret126"] = pct_change_n(C, 126)
    is_common = np.array([p["meta"][s]["kind"] == "common" for s in p["symbols"]])
    base = (
        is_common[None, :]
        & np.isfinite(C)
        & (V > 0)
        & (R >= price_min)
        & (f["dv20"] >= dv_min)
    )
    f["base"] = base
    f["rk21"] = xs_pct_rank(f["ret21"], base)
    f["rk63"] = xs_pct_rank(f["ret63"], base)
    f["rk126"] = xs_pct_rank(f["ret126"], base)
    # Kullamagi's own scan measure: close relative to the lowest low of the last N days
    for n in (22, 65, 126):
        with np.errstate(divide="ignore", invalid="ignore"):
            g = (C / rolling_min(L, n) - 1.0).astype(np.float32)
        f[f"gain{n}"] = g
        f[f"gk{n}"] = xs_pct_rank(g, base)
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        for n, a in f.items():
            np.save(os.path.join(cache_dir, n + ".npy"), a)
    return f


def near_split(p, window=10):
    """Bool [T,S]: True within `window` trading days either side of a split ex-date.

    Split-adjusted vendor data is least reliable around (especially reverse) splits: an ex-date that
    is off by a few bars shows up as a fake multi-hundred-percent move.  Signals there are skipped.
    """
    sd = p.get("splitday")
    if sd is None:
        return None
    sd = np.asarray(sd)
    T = sd.shape[0]
    cs = np.cumsum(sd.astype(np.int32), axis=0)
    hi = np.minimum(np.arange(T) + window, T - 1)
    lo = np.maximum(np.arange(T) - window - 1, 0)
    out = (cs[hi] - cs[lo]) > 0
    out[: window + 1] |= cs[: window + 1] > 0
    return out

"""Data-cleaning helpers shared by the panel builders."""
import numpy as np


def repair_scaling_glitches(O, H, L, C, V, min_ratio=5.0, max_bars=10):
    """Repair vendor scaling errors in place.

    Signature of a misdated or missing (reverse-)split adjustment: the close jumps by a factor
    r >= min_ratio while share volume falls by about the same factor, i.e. dollar volume stays
    roughly continuous.  A genuine price spike shows the opposite (volume explodes).
      * if the jump reverses within `max_bars` bars, the bars in between are blanked;
      * otherwise every earlier bar is rescaled as if a split had been missed.
    Returns (n_blanked, n_rescaled, [(row, col)], [(row, col, ratio)]).
    """
    n_s = C.shape[1]
    blanked = rescaled_n = 0
    at = []
    rescaled = []
    for j in range(n_s):
        c = C[:, j]
        idx = np.nonzero(np.isfinite(c))[0]
        if len(idx) < 3:
            continue
        cv = c[idx].astype(np.float64)
        vv = V[idx, j].astype(np.float64)
        ratio = cv[1:] / cv[:-1]
        for k in np.nonzero(ratio >= min_ratio)[0]:
            a, b = idx[k], idx[k + 1]  # jump between bar a and bar b
            r = C[b, j] / C[a, j] if np.isfinite(C[a, j]) and np.isfinite(C[b, j]) else np.nan
            if not np.isfinite(r) or r < min_ratio or not (vv[k] > 0) or vv[k + 1] / vv[k] > 2.0 / r:
                continue
            end = None
            for m in range(k + 1, min(k + 1 + max_bars, len(idx) - 1)):
                if cv[m + 1] / cv[m] <= 2.0 / r:
                    end = idx[m + 1]
                    break
            if end is not None:
                for a_ in (O, H, L, C, V):
                    a_[b:end, j] = np.nan
                blanked += 1
            else:
                for a_ in (O, H, L, C):
                    a_[:b, j] *= r
                V[:b, j] /= r
                rescaled_n += 1
                rescaled.append((b, j, r))
            at.append((b, j))
    return blanked, rescaled_n, at, rescaled


def clean_bars(O, H, L, C, V):
    """Drop bars with non-positive prices and make high/low bracket open/close. In place."""
    bad = ~(np.isfinite(O) & np.isfinite(H) & np.isfinite(L) & np.isfinite(C)) | (O <= 0) | (H <= 0) | (L <= 0) | (C <= 0)
    n_bad = int((bad & np.isfinite(C)).sum())
    for a in (O, H, L, C, V):
        a[bad] = np.nan
    hi = np.fmax(np.fmax(O, C), H)
    lo = np.fmin(np.fmin(O, C), L)
    n_fix = int(((hi != H) | (lo != L))[np.isfinite(C)].sum())
    H[:] = hi
    L[:] = lo
    V[~np.isfinite(V)] = 0.0
    V[bad] = np.nan
    return n_bad, n_fix

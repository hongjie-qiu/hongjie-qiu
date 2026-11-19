"""Data-cleaning helpers shared by the panel builders."""
import numpy as np


def _snap(r):
    """Snap an observed jump to the nearest whole split ratio (1:5, 1:10, ...) when it is close.

    The close-to-close jump across a reverse split is (split ratio) x (1 + that day's real return);
    rescaling by the snapped ratio keeps the real return instead of erasing it.
    """
    k = float(round(r))
    if k >= 2 and abs(np.log(r / k)) < np.log(1.25):
        return k
    return float(r)


def repair_scaling_glitches(O, H, L, C, V, split_events=None, min_ratio=5.0, max_bars=10, near=30):
    """Repair vendor scaling errors in place, conservatively.

    Candidate: the close jumps by a factor r >= min_ratio while share volume falls by about the same
    factor (dollar volume roughly continuous).  That alone is not proof - a genuine squeeze can show
    it too (TOP Financial, April 2023) - so a repair needs corroboration:
      * `split_events[col]` = [(row, price_factor)] lists recorded splits, price_factor being the jump
        the as-traded price makes at the split (10 for a 1:10 reverse split).  A recorded split within
        `near` rows whose factor matches r marks the jump as a misdated/missing adjustment;
      * without one, a jump that does NOT reverse is still treated as a missed reverse split when share
        volume stays lower for the following ten bars (a squeeze has the opposite volume signature).
    Jump that reverses within `max_bars` bars + matching recorded split -> the bars in between are
    blanked (adjustment applied on the wrong dates).  Jump that does not reverse + corroboration ->
    earlier bars are rescaled by the recorded (or snapped) ratio.  Everything else is left alone.
    Returns (n_blanked, n_rescaled, n_left_alone, [(row, col)], [(row, col, ratio)]).
    """
    split_events = split_events or {}
    n_s = C.shape[1]
    blanked = rescaled_n = left = 0
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
            ev = [pf for (row, pf) in split_events.get(j, ()) if abs(row - b) <= near and pf > 0
                  and abs(np.log(r / pf)) < np.log(1.5)]
            end = None
            for m in range(k + 1, min(k + 1 + max_bars, len(idx) - 1)):
                if cv[m + 1] / cv[m] <= 2.0 / r:
                    end = idx[m + 1]
                    break
            if end is not None:
                if ev:
                    for a_ in (O, H, L, C, V):
                        a_[b:end, j] = np.nan
                    blanked += 1
                    at.append((b, j))
                else:
                    left += 1
                continue
            before = vv[max(0, k - 9):k + 1]
            after = vv[k + 1:k + 11]
            persistent = len(after) >= 5 and np.median(after) <= (2.0 / r) * np.median(before)
            if ev or persistent:
                use = float(ev[0]) if ev else _snap(r)
                for a_ in (O, H, L, C):
                    a_[:b, j] *= use
                V[:b, j] /= use
                rescaled_n += 1
                rescaled.append((b, j, use))
                at.append((b, j))
            else:
                left += 1
    return blanked, rescaled_n, left, at, rescaled


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

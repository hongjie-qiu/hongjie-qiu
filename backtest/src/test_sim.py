"""Hand-checkable unit tests for the trade simulator and portfolio accounting (synthetic bars).

Run: python3 -I test_sim.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from qm.sim import simulate_longs, simulate_shorts, portfolio_sim


def bars(rows):
    """rows: list of (o, h, l, c) for one symbol -> four [T,1] float32 arrays."""
    a = np.array(rows, dtype=np.float32)
    return tuple(a[:, k:k + 1].copy() for k in range(4))


def run_long(rows, ma, t0, entry, stop, **kw):
    O, H, L, C = bars(rows)
    MA = np.array(ma, dtype=np.float32).reshape(-1, 1)
    args = dict(at_close=False, day0_mode=1, part_day=3, part_frac=0.0, be_after_part=True, max_hold=250, cost=0.0,
                exact0=False)
    args.update(kw)
    return simulate_longs(O, H, L, C, MA, np.array([t0]), np.array([0]), np.array([float(entry)]),
                          np.array([float(stop)]), args["at_close"], args["day0_mode"], args["part_day"],
                          args["part_frac"], args["be_after_part"], args["max_hold"], args["cost"],
                          np.array([args["exact0"]]))


def approx(a, b, tol=1e-6):
    assert abs(a - b) < tol, (a, b)


# 1) plain stop on day 2: entry 100, stop 95, day-1 fine, day-2 low 94 -> exit 95 = -1R
rows = [(99, 101, 98, 100.5), (100.5, 103, 100, 102), (102, 102.5, 94, 96), (96, 97, 95, 96)]
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0, 0, 0], 0, 100, 95)
assert ex[0] == 2 and why[0] == 0, (ex, why)
approx(fpx[0], 95); approx(r[0], -1.0); approx(ret[0], -0.05)

# 2) gap through the stop: day-1 opens at 90 -> exit at the open (90), R = -2
rows = [(99, 101, 98, 100.5), (90, 92, 88, 91)]
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0], 0, 100, 95)
approx(fpx[0], 90); approx(r[0], -2.0)

# 3) day-0 pessimistic: day-0 low 94 <= stop 95 -> stopped on entry day at 95
rows = [(99, 101, 94, 100.5), (101, 110, 100, 109)]
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0], 0, 100, 95)
assert why[0] == 4 and ex[0] == 0
approx(r[0], -1.0)
#    same bars, optimistic: survives day 0, then runs; exits at data end (last close 109) -> +1.8R
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0], 0, 100, 95, day0_mode=0)
assert why[0] == 3
approx(r[0], 1.8)

# 4) trailing MA: close below MA on day 2 -> exit at day-3 open
rows = [(99, 101, 98, 100.5), (101, 106, 100.5, 105), (105, 106, 102, 103), (104, 105, 103, 104.5), (1, 1, 1, 1)]
ma = [90, 95, 104, 104, 104]  # day-2 close 103 < 104
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, ma, 0, 100, 95)
assert ex[0] == 3 and why[0] == 1, (ex, why)
approx(fpx[0], 104); approx(r[0], 0.8)

# 5) partial 1/2 at first profitable close on/after 3 sessions, then breakeven stop
rows = [(99, 101, 98, 100.5),       # day 0 entry 100
        (100.5, 102, 100, 101),     # 1
        (101, 103, 100.5, 102),     # 2
        (102, 111, 101.5, 110),     # 3 -> partial half at 110
        (110, 111, 99, 100.5)]      # 4 -> low 99 <= breakeven 100 -> rest out at 100
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0] * 5, 0, 100, 95, part_frac=0.5)
assert pd_[0] == 3 and ex[0] == 4 and why[0] == 0, (pd_, ex, why)
approx(ppx[0], 110); approx(fpx[0], 100)
approx(r[0], (0.5 * 110 + 0.5 * 100 - 100) / 5)  # +1R

# 6) costs: 1% per fill, entry 100 exit 110 at max_hold=1 close
rows = [(99, 101, 98, 100.5), (101, 111, 100.5, 110)]
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0], 0, 100, 95, max_hold=1, cost=0.01)
assert why[0] == 2
approx(ret[0], (110 * 0.99 - 101) / 101); approx(r[0], (110 * 0.99 - 101) / 5)

# 7) close entry ignores the entry day's own range
rows = [(99, 101, 80, 100), (100, 104, 99.5, 103)]
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0], 0, 100, 95, at_close=True, max_hold=1)
assert why[0] == 2
approx(r[0], 0.6)

# 8) missing bars are skipped; >10 missing in a row -> exit at last close
rows = [(99, 101, 98, 100.5), (101, 103, 100, 102)] + [(np.nan,) * 4] * 12
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0] * 14, 0, 100, 95)
assert why[0] == 3 and ex[0] == 1
approx(fpx[0], 102)

# 8b) a fill AT THE OPEN has no entry-day ambiguity: the low comes after the fill, so even the
#     "close-based" and "ignore" modes must stop the trade when the day's low reaches the stop
rows = [(100, 101, 94, 100.5), (101, 110, 100, 109)]
for mode in (0, 1, 2):
    ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0], 0, 100, 95, day0_mode=mode, exact0=True)
    assert why[0] == 4 and ex[0] == 0, (mode, why, ex)
    approx(r[0], -1.0)
#     the same bars with a later intraday fill (not at the open) stay ambiguous: mode 2 keeps the trade
ex, pd_, ppx, fpx, ret, r, why, hold, mfe = run_long(rows, [0, 0], 0, 100, 95, day0_mode=2, exact0=False)
assert why[0] == 3

# ---- shorts
def run_short(rows, ma, t0, entry, stop, **kw):
    O, H, L, C = bars(rows)
    MA = np.array(ma, dtype=np.float32).reshape(-1, 1)
    args = dict(at_close=True, day0_mode=1, use_target=True, max_hold=10, cost=0.0, borrow_daily=0.0, exact0=False)
    args.update(kw)
    return simulate_shorts(O, H, L, C, MA, np.array([t0]), np.array([0]), np.array([float(entry)]),
                           np.array([float(stop)]), args["at_close"], args["day0_mode"], args["use_target"],
                           args["max_hold"], args["cost"], args["borrow_daily"], np.array([args["exact0"]]))

# 9) short 100 at close, stop 110, target = previous day's MA (80): day 2 low 78 -> cover at 80 (+2R)
rows = [(105, 108, 99, 100), (98, 99, 90, 91), (90, 91, 78, 79)]
ex, fpx, ret, r, why, hold = run_short(rows, [80, 80, 80], 0, 100, 110)
assert ex[0] == 2 and why[0] == 5, (ex, why)
approx(fpx[0], 80); approx(r[0], 2.0)
# 10) stop: day 1 gaps to 115 -> cover at open 115 = -1.5R
rows = [(105, 108, 99, 100), (115, 120, 114, 118)]
ex, fpx, ret, r, why, hold = run_short(rows, [80, 80], 0, 100, 110)
assert why[0] == 0
approx(fpx[0], 115); approx(r[0], -1.5)
# 11) stop and target in the same bar -> stop first
rows = [(105, 108, 99, 100), (100, 111, 70, 75)]
ex, fpx, ret, r, why, hold = run_short(rows, [80, 80], 0, 100, 110)
assert why[0] == 0
approx(r[0], -1.0)
# 12) borrow fee 1%/day for 2 days on a flat trade exits at max_hold
rows = [(105, 108, 99, 100), (100, 101, 99, 100), (100, 101, 99, 100)]
ex, fpx, ret, r, why, hold = run_short(rows, [0, 0, 0], 0, 100, 110, use_target=False, max_hold=2, borrow_daily=0.01)
approx(ret[0], -0.02)

# ---- portfolio accounting: one trade, risk 1% of 100k, entry 100 stop 95 -> 200 sh; exit 110 -> +2000
C = np.array([[100.5], [105.0], [110.0], [110.0]], dtype=np.float32)
dates = np.arange("2020-01-01", "2020-01-05", dtype="datetime64[D]")
tr = {"t0": np.array([0]), "j": np.array([0]), "entry": np.array([100.0]), "stop": np.array([95.0]),
      "exit_day": np.array([2]), "final_px": np.array([110.0]), "prio": np.array([1.0]),
      "part_day": np.array([-1]), "part_px": np.array([np.nan]), "part_frac": np.array([0.0])}
eq, taken, g = portfolio_sim(tr, C, dates, start_equity=100_000, risk_pct=0.01, max_pos_w=0.5, cost=0.0)
approx(eq[0], 100_000 + 200 * 0.5); approx(eq[1], 100_000 + 200 * 5); approx(eq[2], 102_000); approx(eq[3], 102_000)
# position cap: max_pos_w 10% -> 100 sh -> +1000
eq, taken, g = portfolio_sim(tr, C, dates, start_equity=100_000, risk_pct=0.01, max_pos_w=0.10, cost=0.0)
approx(eq[3], 101_000)
# short accounting: direction=-1, entry 100, cover 110 -> -2000 with 200 sh
tr_s = dict(tr); tr_s["stop"] = np.array([105.0])
eq, taken, g = portfolio_sim(tr_s, C, dates, start_equity=100_000, risk_pct=0.01, max_pos_w=0.5, cost=0.0, direction=-1)
approx(eq[3], 98_000)
# ---- twin detection must not merge different companies that were stopped out on the same day
import pandas as pd
from qm.run import _drop_twins
Cx = np.array([[10, 20, 30], [11, 21, 33], [12, 23, 37], [9, 17, 27]], dtype=np.float32)
df = pd.DataFrame({"t0": [2, 2, 2], "j": [0, 1, 2], "exit_day": [3, 3, 3], "ret": [-0.3, -0.3, -0.3]})
assert len(_drop_twins(df, Cx)) == 3          # same outcome, different price paths -> all kept
Cy = Cx.copy(); Cy[:, 1] = Cx[:, 0] * 7.0      # column 1 is column 0 listed under another ticker and scale
assert len(_drop_twins(df, Cy)) == 2          # the true duplicate is dropped
print("all simulator tests passed")

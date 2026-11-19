"""Glue: turn signal dicts into trade tables and summaries."""
import numpy as np
import pandas as pd
from .sim import simulate_longs, simulate_shorts, trade_stats
from .setups import dedupe_open


def _arr(p, k):
    return np.asarray(p[k])


def long_trades(p, f, sig, at_close, day0_mode=1, part_day=3, part_frac=1 / 3, be_after_part=True,
                trail="sma10", max_hold=250, cost=0.0015, dedupe=True):
    """Simulate long signals -> DataFrame (one row per trade)."""
    O, H, L, C = (_arr(p, k) for k in ("open", "high", "low", "close"))
    MA = np.asarray(f[trail])
    res = simulate_longs(O, H, L, C, MA, sig["t0"], sig["j"], sig["entry"], sig["stop"], at_close,
                         day0_mode, part_day, part_frac, be_after_part, max_hold, cost,
                         _open_fill(O, sig, at_close))
    exit_day, part_dayo, part_px, final_px, ret, rmult, reason, hold, mfe = res
    keep = np.isfinite(rmult)
    if dedupe:
        keep &= dedupe_open(sig, exit_day)
    df = pd.DataFrame({
        "t0": sig["t0"], "j": sig["j"], "entry": sig["entry"], "stop": sig["stop"], "prio": sig["prio"],
        "exit_day": exit_day, "part_day": part_dayo, "part_px": part_px, "final_px": final_px,
        "ret": ret, "R": rmult, "reason": reason, "hold": hold, "mfe": mfe,
    })
    for k, v in sig.items():
        if k not in df.columns:
            df[k] = v
    df["part_frac"] = part_frac
    df = _drop_twins(df[keep], C)
    df["date"] = p["dates"][df["t0"].values]
    df["exit_date"] = p["dates"][df["exit_day"].values]
    df["symbol"] = [p["symbols"][j] for j in df["j"].values]
    df["year"] = df["date"].dt.year if hasattr(df["date"], "dt") else pd.DatetimeIndex(df["date"]).year
    df["risk_pct"] = (df["entry"] - df["stop"]) / df["entry"]
    return df


def short_trades(p, f, sig, at_close=True, day0_mode=1, use_target=True, target="sma10", max_hold=10,
                 cost=0.005, borrow_annual=0.5, dedupe=True):
    O, H, L, C = (_arr(p, k) for k in ("open", "high", "low", "close"))
    MA = np.asarray(f[target])
    res = simulate_shorts(O, H, L, C, MA, sig["t0"], sig["j"], sig["entry"], sig["stop"], at_close,
                          day0_mode, use_target, max_hold, cost, borrow_annual / 252.0,
                          _open_fill(O, sig, at_close))
    exit_day, final_px, ret, rmult, reason, hold = res
    keep = np.isfinite(rmult)
    if dedupe:
        keep &= dedupe_open(sig, exit_day)
    df = pd.DataFrame({
        "t0": sig["t0"], "j": sig["j"], "entry": sig["entry"], "stop": sig["stop"], "prio": sig["prio"],
        "exit_day": exit_day, "final_px": final_px, "ret": ret, "R": rmult, "reason": reason, "hold": hold,
    })
    for k, v in sig.items():
        if k not in df.columns:
            df[k] = v
    df = _drop_twins(df[keep], C)
    df["date"] = p["dates"][df["t0"].values]
    df["exit_date"] = p["dates"][df["exit_day"].values]
    df["symbol"] = [p["symbols"][j] for j in df["j"].values]
    df["year"] = pd.DatetimeIndex(df["date"]).year
    df["risk_pct"] = (df["stop"] - df["entry"]) / df["entry"]
    return df


def _open_fill(O, sig, at_close):
    """True where an intraday fill happened exactly at the open (no entry-day ambiguity)."""
    n = len(sig["t0"])
    if at_close or n == 0:
        return np.zeros(n, dtype=np.bool_)
    o = O[sig["t0"], sig["j"]].astype(np.float64)
    return np.isclose(sig["entry"], o, rtol=1e-6, atol=0.0)


def _drop_twins(df, C):
    """Remove trades that duplicate another trade because one company is listed under two tickers.

    Two trades are twins only if they share entry day, exit day and return AND the stock's own
    close-to-close path into the entry (the two daily changes before the fill) is identical.  The
    path test matters: with a fixed-percentage stop, different companies stopped out on the same day
    have identical returns, and must not be mistaken for duplicates.
    """
    if len(df) == 0:
        return df.reset_index(drop=True)
    t0 = df["t0"].values.astype(np.int64)
    j = df["j"].values.astype(np.int64)
    a = np.maximum(t0 - 1, 0)
    b = np.maximum(t0 - 2, 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        r1 = np.round(np.nan_to_num(C[t0, j].astype(np.float64) / C[a, j], nan=-1.0), 4)
        r2 = np.round(np.nan_to_num(C[a, j].astype(np.float64) / C[b, j], nan=-1.0), 4)
    key = pd.DataFrame({"t0": t0, "x": df["exit_day"].values, "r": df["ret"].round(6).values, "r1": r1, "r2": r2})
    return df[~key.duplicated(keep="first").values].reset_index(drop=True)


def summarize(df, label=""):
    s = trade_stats(df["R"].values, df["ret"].values)
    s["label"] = label
    if len(df):
        s["avg_hold"] = float(df["hold"].mean())
        s["avg_risk_pct"] = float(df["risk_pct"].mean())
    return s


def by_year(df):
    rows = []
    for y, g in df.groupby("year"):
        s = trade_stats(g["R"].values, g["ret"].values)
        rows.append({"year": int(y), "n": s["n"], "win": s["win_rate"], "avgR": s["avg_R"],
                     "sumR": float(g["R"].sum()), "avg_ret": s.get("avg_ret", np.nan), "pf": s["profit_factor"]})
    return pd.DataFrame(rows)


def fmt_stats(s):
    if s.get("n", 0) == 0:
        return f"{s.get('label',''):<34} n=0"
    return (f"{s.get('label',''):<34} n={s['n']:>6}  win={s['win_rate']*100:5.1f}%  avgR={s['avg_R']:+.3f}"
            f"  medR={s['median_R']:+.2f}  avgW={s['avg_win_R']:+.2f}R  avgL={s['avg_loss_R']:+.2f}R"
            f"  PF={s['profit_factor']:.2f}  t={s['t_stat']:+.1f}  avgRet={s.get('avg_ret', float('nan'))*100:+.2f}%"
            f"  top5%={s['top5pct_share']*100:.0f}%  hold={s.get('avg_hold', float('nan')):.1f}d"
            f"  risk={s.get('avg_risk_pct', float('nan'))*100:.1f}%")

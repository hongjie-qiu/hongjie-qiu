# Independent audit of the backtest code and results

Date: 2026-11-19. Scope: `src/qm/*.py`, `src/run_breakout.py`, `src/run_ep.py`, `src/run_parabolic.py`,
`src/build_panel.py`, `src/build_dolt_panel.py`, the two panels under `data/`, and the 21 current trade lists in
`results/` (Q0, C0, Q0_noregime, Eclose, Eclose_earn_sma20, Eopen_pess, Pred, each for hf / dolt / hfwin).

Code state audited: the files as they stood at 05:11 UTC (last edits: `qm/sim.py` 05:03:28, `qm/setups.py` and
`qm/data.py` 04:36:52, `qm/run.py` 04:35:33, `qm/clean.py` 04:44:59, `qm/earnings.py` 04:46:58, `build_panel.py`
04:40:06, `build_dolt_panel.py` 04:45:36). They were unchanged at 06:25. `run_portfolio.py`, `run_universe.py`,
`make_charts.py` and `run_clustered_t.py` appeared while the audit was running; I read them and tested
`portfolio_sim`, but did not reproduce their outputs.

Nothing under `src/`, `data/` or `results/` was edited. Importing the package let numba add compiled-cache files
(`*.nbc`, `*.nbi`) to `src/qm/__pycache__`; no source, data or result file was touched.

## 摘要

- **引擎本身没有发现未来函数或记账错误。** 截断与扰动测试、独立重写的模拟器（逐笔重放 67,967 笔已保存交易，另加
  140,793 笔其他模式的交易）、独立重算的信号（约 1,150 个抽样交易日 × 全部股票）全部吻合；21 个结果 CSV 可逐位复现。
- **唯一用到未来信息的信号环节**是拆股前后 ±10 日的隔离窗口（`near_split`），实测影响不超过 0.002R。
- **会改变结论数字的问题有 8 个（major）**：① “收盘判定”的入场日假设对开盘价成交的交易在逻辑上不可能，且它是乐观上界而非“折中”；
  ② `_drop_twins` 把同日止损的不同公司当成重复而删掉，P-open 的平均 R 被抬高 0.02（14–17%）；
  ③ 任何缺失 K 线都会让均线在其后 10/20/50 行变成 NaN，跟踪止盈被悄悄关闭，dolt 面板上“财报 EP + 50 日线”的 +0.42R 因此虚高约 0.08R；
  ④ dolt 面板缺 14 个真实交易日，并多出 9 个假日行（2020-02-17 一行让 88% 的股票均线失效 10–50 天）；
  ⑤ dolt 的拆股复权有漏洞（203 处未复权的跳变；修复逻辑抹掉了拆股当日的真实涨跌）；
  ⑥ “缩放故障修复”在两个面板里都删掉了一次真实的逼空行情（TOP，2023-04-28 起 4 根 K 线），并且处理不了 2026 年年中供应商数据的交替缩放；
  ⑦ dolt 按代码“现在的归属”分类，Facebook（FB，2012–2022）等至少 16 家流动性好的公司被整段丢弃；
  ⑧ HF 面板的幸存者偏差随时间变化（中途消失的代码几乎都集中在 2024–2026 年，更早退市的一概没有），分年代比较不可靠。
- 这些问题对已保存的突破与 EP 交易清单影响很小（多数在 0.5% 的交易以内），不改变“多数变体期望为负”的结论；受影响较大的是两个正收益的结果：P-open 做空和 dolt 上的财报 EP 50 日线版本。

## 1. Bottom line

1. **No critical defect.** I found no look-ahead in features, cross-sectional ranks, signal conditions, entry
   prices, stop levels or exits, and no accounting error in the trade simulator or `portfolio_sim`. The one path
   that uses future data in signal generation is the split quarantine (finding 9); its measured effect is at most
   0.002R on any saved variant.
2. **The saved results are what the current code and data produce**: all 21 CSVs reproduce bit for bit, and an
   independent plain-Python simulator returns the same exit day, price, return, R and reason for every one of the
   67,967 trades.
3. **Eight major issues bias specific numbers** (findings 1–8). Two of them inflate the positive results:
   `_drop_twins` deletes stopped-out shorts (P-open +0.171R should be +0.148R on HF, +0.122R should be +0.102R on
   dolt), and the NaN moving-average rule disables the 50-day trailing exit on the dolt panel (earnings EP
   +0.423R becomes +0.339R when the average skips missing bars).
4. **The dolt panel is weaker as a cross-check than the README says.** It lacks 14 trading days, has a bogus
   2020-02-17 row, 203 unadjusted split jumps and no Facebook. For trades that exist in both sources, outcomes
   still agree: 96–98% have the same exit date and return, and the mean R is equal to three decimals.

## 2. Findings

Severity: critical = invalidates results; major = biases a reported number or silently breaks data or logic;
minor = real but small measured effect; note = worth knowing.

| # | Sev. | Where | What is wrong | Evidence | Suggested fix |
|---|---|---|---|---|---|
| 1 | major | `qm/sim.py:67-76`, `:185-193`; used as baseline in `run_breakout.py:31`, `run_ep.py:112,129,134`, `run_portfolio.py:79`, `run_clustered_t.py:42`; plotted in `make_charts.py:83-92` | `day0_mode=2` ("close-based") keeps a trade alive when the entry-day low touched the stop but the close recovered. For a fill **at the open** the low necessarily comes after the fill, so this uses the close to forgive a stop that was hit. It is also the optimistic bound, not a middle case; `day0_mode=0` is not an upper bound. | E-open (HF): all 18,089 fills are at the open; 8,068 (44.6%) have low <= stop; 3,806 (21.0%) are kept alive. Log: -0.116R (t -8.1) exact vs **+0.077R (t +4.1)** "close-based"; dolt -0.055 vs +0.102. E-orb: pessimistic -0.469, "close-based" +0.605, "optimistic" +0.003. Q0: 122 of 1,463 fills at the open, 11 wrongly kept (-0.83R simulated, -1.05R true); avg R -0.0620 -> -0.0636; true range is [-0.111, -0.062]. The random-entry control (`run_breakout.py:99-100`) also fills at the open: -0.061R as shipped vs -0.081R exact (4 seeds). | Pass a flag (or test `entry == open`) so open fills always use the low. Delete the E-open "close-based" row. Relabel mode 2 as the optimistic bound and report intraday entries as the range [mode 1, mode 2]. |
| 2 | major | `qm/run.py:67-70` (called at `:32`, `:58`) | `_drop_twins` treats trades with the same entry day, exit day and return (6 dp) as one company listed twice. With a fixed-percentage stop every trade stopped at the stop price has the same return, so different companies are deleted, and they are all losers. It also decides from the trade's outcome, i.e. future data. | P-open +30%: HF removes 76 = 45 duplicate listings + **30–31 different companies** (stopped out on day 0 or later, mean R -1.045); dolt removes 22, **all different companies** (e.g. 2020-06-09 keeps DGLY, drops ENT, RNET, SPCB, CHK~1). Avg R +0.1712 -> +0.1476 (HF), +0.1221 -> +0.1017 (dolt); month-clustered t 5.79 -> 5.11 and 3.11 -> 2.79. E-open: 2 of 174 (HF) and 3 of 3 (dolt) drops are different companies. | Remove duplicate listings in the panel builder by price-path identity over a long window, not by trade outcome. HF still holds enough duplicates to trigger 1–3% of signals. |
| 3 | major | `qm/data.py:208-210` (`rolling_mean(C, n, n)`), consumed at `qm/sim.py:80-82,132-134` and `qm/setups.py:96-97` | One missing bar makes SMA-n NaN for the next n rows. `c < NaN` is false, so the trailing exit is silently off, and the breakout trend filter silently fails. | dolt: 5.55% of liquid symbol-days in the run window have SMA50 undefined because of a hole (261,181 of 4,704,206); HF 0.01%. dolt "earnings EP, SMA50 trail": 63 trades (5.2%) held through such days, mean R +2.98 vs +1.38 with an SMA over the last 50 valid closes; variant avg R **+0.423 -> +0.339**. All-EP SMA50 +0.291 -> +0.257. SMA10/20 variants move by <= 0.002R. GME 2021-01-14: +7.13R on HF, +0.97R on dolt (bar of 2021-01-26 missing). | Average the last n valid closes (or forward-fill before averaging), and assert that the MA is finite on every held day. |
| 4 | major | `build_dolt_panel.py:76-77` (calendar = dates on which SPY has a row) | The dolt calendar is wrong on 23 days. 14 real trading days are absent, so every symbol loses them and the next "overnight gap" spans two or three sessions. 9 market holidays are present; on 8 of them most bars are copies of the previous close, and on 2020-02-17 only 585 of ~5,000 symbols have a bar. | Missing: 2011-10-18, 2015-06-30, 2019-08-23, 2019-09-17, 2019-09-19, 2019-10-02, 2021-05-03, 2021-05-14, 2021-07-07, 2021-07-08, 2022-08-01, 2022-09-19, 2023-06-30, 2024-03-25. EP events: median 5 per day, but 97 on 2021-05-17, 30 on 2021-05-04, 27 on 2021-07-09; 231 E-open trades sit on such days. After 2020-02-17 SMA10/20/50 are finite for ~550 symbols instead of ~4,800 during the next 10/20/50 rows (SMA50 recovers on 2020-04-28): P-red entries 2020-02-18..03-02 are 1 on dolt vs 9 on hfwin; Q0_noregime 2020-02-18..04-29 are 3 vs 7. | Use an exchange calendar. Drop rows where fewer than half of the symbols print. Re-fetch the 14 missing days. |
| 5 | major | `build_dolt_panel.py:159-190`, `:99-136`; `qm/clean.py:41-46` | Split adjustment of the raw dolt prices has three gaps. (a) A split is rejected when the ex-date open differs from the expected price by more than a factor of 1.35, or when the ex-date bar is missing. (b) The glitch repair then uses the observed close ratio as the split ratio, which sets that step's real return to zero; if the volume test fails, nothing is adjusted. (c) Splits are never applied to ticker-reuse columns (`SYM~k`), because candidates are matched to the base ticker's column only. | 203 split-coincident close-to-close jumps (>= 2.5x or <= 0.4x) carry no split flag: 188 up, 15 down, 58 above $3. Examples: ACHV 2020-07-31 x22.7, ASTI 2023-09-13 x237, BETS 2024-01-10 x661, CP 2021-05-17 x0.19 (5:1 split dated on a missing calendar day), RGC 2025-06-16 x0.10. Of 208 "rescaled" repairs, 140 have a table split within 7 days: erased return median -12.5%, 37 beyond 25% (TTOO 2023-10-13 -52%, GNLN -59%). 1,243 `~k` columns contain 144 split events; 101 are unadjusted. Effect on saved trades is small: at most 0.5% of the trades in any file have such a jump in their look-back window; 6 E-open trades follow one directly. | Apply table splits of ratio >= 1.5 without the 1.35 test (use the next valid bar when the ex-date bar is missing). In the repair, snap to the table ratio. Match candidates to segments by date. Flag every adjusted or suspect bar. |
| 6 | major | `qm/clean.py:32-40`, `build_panel.py:181-197` | The "jump reverses within 10 bars" rule blanks bars. It deleted a genuine squeeze, and it mishandles the vendor's alternating-scale bars around mid-2026 reverse splits (blanks the correctly scaled bars, or leaves glitch bars in place). The "rescale everything before" branch turns a one-bar bad print into a fake crash. | TOP Financial 2023-04-28..05-03 (as-traded closes 20 -> 108.21 -> 51.52 -> 53.01 -> 84.80 -> 17.48): 4 real bars blanked in **both** panels. Of 15 sampled HF repairs: 4 correct, 5 on illiquid OTC names, 6 wrong or incomplete (JUNS keeps a fake 493 -> 7.3 crash on 2026-08-03; AEHL blanks the right-scale bars; ELPW keeps a 7.875 bar between 0.197 and 0.105; CLEU shows +61% on 2025-01-30, where the vendor's own bars imply a fall of about 98%). HF panel still has 19,314 jumps >= 2.5x or <= 0.4x (mostly sub-$1 OTC); 726 are split-coincident and all lie inside the quarantine. `rawclose` is off by the split factor where the vendor lists a split its prices do not reflect (DFNS x125, ELPW x45). | Require a second condition before blanking (a split-table event, or disagreement with the other source). Handle down-then-up patterns. End the HF panel before the vendor's unsettled months, or exclude symbols with a split after 2026-06. |
| 7 | major | `build_dolt_panel.py:55-73`, `:131` | A ticker is classified by its **current** owner (the symbol master has one row per ticker). If a ticker was later reused by an ETF or preferred, the earlier company's whole history is dropped. A renamed company restarts with no look-back. | 649 excluded tickers have a gap over 45 days. Among the 400 longest, 24 earlier owners were liquid (>= 250 bars, median dollar volume >= $3M, price >= $3); 16 of them are operating companies: FB 2012-05-18..2022-06-08, INFO, TOT, EV, IIVI, PLT, GSX, KEM, SEMG, FLOW, INOV, FLXN, BCOR, RESI, ETH, LMNX. META starts 2022-06-13, so it has no SMA50 for 50 rows and no 6-month rank for 126. | Classify per segment (use `last_seen`, or the name valid at the time). Chain ticker changes through the identifiers file already in `data/ziplime/`. |
| 8 | major | `build_panel.py:49-69`; all by-era tables | The HF panel is a hybrid, not "survivors only": 1,158 of 7,554 columns stop before 2026-11, all but 3 of them in 2024, 2025 or 2026 (87, 497, 571). Tickers that died before 2024 are absent in every era, so the survivorship bias is largest early and smallest late. Era comparisons mix a real trend with this gradient. | Q0_noregime, tickers that stop early vs the rest, mean R by era: -0.098 vs +0.018 (2005-12), -0.239 vs +0.084 (2013-18), -0.376 vs +0.080 (2019-21), -0.203 vs -0.109 (2022-26). | Do not read the HF by-era columns as decay of the edge. State that long results before 2024 are upward biased by an unknown amount. |
| 9 | minor | `qm/data.py:246-262` (`hi = t + window`), applied at `qm/setups.py:244-246`, `:286-288` | `near_split` drops a signal on day t if a split or flagged glitch occurs in the **next** 10 rows. This is the only look-ahead in signal generation. | Perturbation test with split flags scrambled after T0: 94 signals vanish, all within 10 rows before T0, none otherwise. Re-run with a backward-only window: Q0 +4 trades (mean +0.71R), avg R -0.0620 -> -0.0599; Q0_noregime +7; E-open +17 (mean -0.69R); P-red +2 (mean -1.16R, one is a real data artifact, IFBD 2024-02-27), +0.0467 -> +0.0449. | Use a backward-only window and detect bad bars explicitly; or keep it and say it is a data-quality filter that also removes trades ahead of real splits. |
| 10 | minor | `qm/bench.py:9-17`, `qm/setups.py:26` | HF has no QQQM column and QQQ ends 2026-09-11, so the proxy is NaN afterwards. `regime_on` turns NaN into 0, so the filter is off for the last 47 sessions. On dolt, QQQ is NaN on 2017-07-03 and 2022-09-20. | Q0 and C0 have 0 entries after 2026-09-11; Q0_noregime has 28. A SPY regime is on for 10 of those 47 days and would admit 4 trades. On dolt the "10>20 only" regime is forced on for 2022-10-04..10-17; the strict regime is unaffected. | Fall back to SPY (85.8% agreement with QQQ) and raise on NaN instead of summing zeros. |
| 11 | minor | `qm/setups.py:120,201` (stop = entry x (1 - k x ADR)), `:273`, `:298`; `qm/sim.py:387-409` | Stop distance is unbounded, so R is unstable. ADR20 above 100% gives a negative stop; a first-red short can have a stop 0.15% away, where the assumed 1% round-trip cost alone is 6.5R. Mean R and mean return can disagree in sign. | E-open HF: 13 trades with stop <= 0, 104 with risk above 50% of price. P-red: risk from 0.15% to 1,431% of price. dolt P-red: mean R -0.020, mean return +1.47%, risk-weighted R +0.026. HF earnings EP SMA50: sum R +549, top 1% (21 trades) +563, the other 2,177 trades -14. | Require 0 < stop, floor and cap the stop distance, and report mean return and risk-weighted R (sum of P&L / sum of risk) next to mean R. |
| 12 | minor | `qm/sim.py:405`; `run_ep.py:77-80` | Log t-stats treat trades as independent. The event-study line prints the event-weighted mean beside a t computed from the day-weighted mean, with an ad hoc sqrt(5/h) factor. 59 variants are compared with no hold-out. | E-open HF: t -8.09 naive, -3.88 by day, -3.06 by month (282 trades on 2020-11-09). dolt E-open: -2.96 -> -0.95. Sign conflict in `ep_log.txt`: "earnings + close>=open ... +1d xs +0.07% (t~-0.7)". `run_clustered_t.py` fixes this for seven headline rows only. | Print the month-clustered t everywhere. In the event study, compute mean and t on the same weighting. |
| 13 | note | `qm/sim.py:114-116`, `:219-220` | A stop is booked at the stop price whenever the open is on the right side of it, even on a day the stock closes 60–95% lower. | Q0_noregime HF: 8 exits on days that closed <= 0.4x the prior close, booked at mean -18.7%. E-open HF: 19 such exits. OST 2025-06-26 (-94% day) is booked at +3.8%. | Add a slippage sensitivity for days whose range exceeds a few ADR. |
| 14 | note | `qm/sim.py:87-103`, `:200-214` | A trade whose ticker stops printing exits at the last close, dated on the last bar. No delisting return; in `portfolio_sim` the capital is freed before the delisting could be known. | Rare: reason-3 exits before the panel end are 35 of 11,946 (E-open dolt), 9 of 2,925 (E-close dolt), 4 of 1,082 (P-red dolt). | Leave as is; state it. |
| 15 | note | `qm/sim.py:288-336` | `portfolio_sim` processes all of a day's exits before that day's entries, so an intraday entry can use a slot or cash that is only freed at that day's close. | Hand example with `max_positions=1`: Y is taken on the day X leaves at the close. Cash accounting itself is exact (section 3.10). | Process open exits, then entries, then intraday and close exits. |
| 16 | note | `qm/data.py:202-203`; `results/` | The feature cache is reused whenever the files exist, with no check against the panel or parameters. `breakout_trades_A0*.csv`, `breakout_trades_B0.csv` and their by-year files date from 04:27 and an older driver; they cannot be reproduced. | Cache currently matches the panels (section 3.4). | Store a panel hash in the cache; delete the stale files. |
| 17 | note | `qm/earnings.py:76-132` | 23% (dolt) to 30% (HF) of symbols with more than 3 years of history have no earnings flag at all (foreign filers, unmatched tickers), so "non-earnings" groups contain earnings gaps. | 9 of 10 known report dates are flagged on the correct session and none on the day before; GOOGL 2015-07-17 is missed. | Restrict earnings vs non-earnings comparisons to symbols with at least one flag. |
| 18 | note | dolt raw data | Busted prints are kept. On 2023-01-24 (NYSE opening failure) the "open" of LLY, WMT, MO, UNP and some 30 other large caps is 10–15% above the prior close. | 36 E-open trades that day (HF has 3), all stopped on day 0, sum -40.3R of the file's -662.0R. | Drop opens that neither the close nor the next day confirms, or cross-check against HF. |
| 19 | note | `qm/sim.py:60-83` | A close entry whose close is already below the trailing MA is not exited next open (the entry bar is skipped for close entries only). | 114 of 4,538 E-close trades (2.5%); avg R would change by +0.004. | Document the choice. |
| 20 | note | `results/*.csv` | The ticker `NA` is read as missing by `pandas.read_csv` defaults (4 E-open trades). | Seen when comparing files. | Quote symbols or document `keep_default_na=False`. |

Things that are correct and that I expected might not be: the one-bar shift of every indicator used by a
stop-entry; the regime shift; gap-aware stops; partial then breakeven; costs on every fill; borrow fee; the
`dedupe_open` rule; exact decimal ties (`close == SMA`, `gap == 10%`), which the float32 pipeline resolves the
way exact arithmetic would.

## 3. Empirical checks

All scripts are in
`/tmp/claude-0/-home-user-hongjie-qiu/ec9bb88d-d878-5857-a53a-aad2b9b22892/scratchpad/audit/` (session scratch
space; copy them if you want to keep them). Script names are given per check.

### 3.1 Reproduction of the result files (`repro.py`, `a05_repro.py`, `a05c_exact_sorted.py`)

I re-ran the seven saved variants on both panels and the hfwin window with the author's code, in column chunks
of 700 to stay under 3 GB, using the cached features.

- 21 files, 799,226 cells: **0 cells differ, bit for bit**. The three `Pred` files differ in row order only.
- Windows inferred from the files: hf 2005-01-01 onward, dolt 2019-07-01 onward, hfwin 2019-07-01..2026-01-28.
- Earnings matching reproduces the logged counts: 278,079 (HF, `--current`) and 300,605 (dolt).

### 3.2 (a) Truncation test (`harness.py`, `a03_truncation.py`)

Sub-panels of 500 random common symbols plus SPY, QQQ, IWM (and QQQM on dolt), all days. Features, 20 signal
configurations (breakout intraday and close, with regime, loose, alternative horizons, volume dry-up; EP open,
orb, close, earnings, non-earnings, neglected; parabolic next-open and first-red; strict and loosened
thresholds) and 2 to 4 trade-management variants each were computed on the full sub-panel and on the same
sub-panel cut at T0. Four T0 per panel (HF rows 2500, 4000, 5200, 6300; dolt 1500, 2400, 3000, 3500), each with
and without the split flags.

- Features: 20 arrays x 16 runs, **0 mismatching** on rows before T0.
- Signals with entry day before T0: 419,300 comparisons, **0 differ** in day, symbol, entry or stop.
- Trades completed before T0: 1,343,399 comparisons, **0 differ**.
- One trade is missing in one truncated run (TSLA, entry on the last row): two trades entered on the final close
  both exit at entry with return -(2 x cost + borrow) and `_drop_twins` deletes one. This is finding 2, not
  look-ahead.
- This test has little power against `near_split`, because a split must fall within 10 rows after T0 for a
  symbol that also signals within 10 rows before it. The perturbation test covers it.

### 3.3 (b) Perturbation test (`a04_perturb.py`)

Same sub-panels; every open, high, low, close, raw close (lognormal noise, sigma 0.15) and volume (sigma 0.7) at
rows >= T0 was changed.

- Split flags untouched: features 0 of 20 mismatching before T0 in all 8 runs (all 20 change after T0);
  208,993 signal comparisons and 669,859 completed-trade comparisons, **0 differ**.
- Split flags also scrambled after T0 (2% of cells set): **94 signals vanish**, every one within 9 rows before
  T0; none appears and none changes entry or stop. The only trade differences (130) are the trades of those
  signals. This isolates the forward half of `near_split` (finding 9).

### 3.4 Independent re-derivation of features and signals (`mysignals.py`, `a07a`–`a07e`)

I wrote the three setups again in plain numpy (float64, no `qm` imports), computing everything for one entry day
from the raw panel rows up to that day, and compared with the author's raw signal lists on 611 HF days and
538 dolt days (250 random days per panel plus the entry days of 60 random trades from each CSV), all symbols.

- Base-universe mask: 0 mismatching cells of 4,618,549 (HF) and 5,859,358 (dolt).
- SMA10/20/50, dollar volume, volume: maximum relative difference 1e-7 (float32 storage).
- Ranks: differences only inside groups of exactly tied values (e.g. 64 stocks with gain22 = 0 on 2007-11-26)
  and at most 1.4e-3 (one rank position) for names ranked above 0.90.
- Leader mask (top 2% on any horizon, ADR >= 4%): 0 mismatching cells of 1,511,800 (HF) and 2,178,200 (dolt) on
  200 days.
- Signals: 25,692 author signals on the sample days across 11 configurations.

| configuration | HF author / mine | dolt author / mine |
|---|---|---|
| breakout Q0, Q0_noregime, C0, C0_noregime, top 7% | 2,690 / 2,690 | 2,868 / 2,868 |
| EP open | 3,644 / 3,642 | 5,227 / 5,216 |
| EP orb | 2,620 / 2,618 | 3,795 / 3,786 |
| EP close, EP close earnings | 1,433 / 1,433 | 1,711 / 1,709 |
| parabolic next-open, first-red | 692 / 692 | 1,012 / 1,012 |

- All 13 "author only" EP symbol-days sit on the 10% threshold: 12 are gaps of exactly 10.0000% in quoted
  prices (e.g. LNC 2020-06-05, 43.50 -> 47.85) and one is a split-adjusted price within 2e-8 of it (BBD
  2020-03-24). The author's float32 arithmetic gives 0.10000002 and keeps them, which is what `>= 10%` means;
  my float64 gives 0.09999996. The author's side is right.
- Entry and stop agree to 1e-7 relative everywhere, except one EP-open signal with a negative stop (GDC
  2023-05-16, ADR20 = 100.05%, finding 11).

### 3.5 (c) Brute-force re-simulation (`mysim.py`, `a06_replay.py`, `a06c_replay_f32.py`, `a15_dedupe.py`, `a20_allmodes.py`)

`mysim.py` is a plain-Python (no numba, no `qm.sim`) long and short simulator written from the docstrings. It
reads bars from the `.npy` panels and computes its own moving average.

- **All 67,967 trades in the 21 CSVs**, moving average in float64: 24 rows (11 distinct trades, several saved
  in more than one file) differ in exit day or return, and 1,502 parabolic target fills differ by at most 6e-8
  in return.
  - All 11 hinge on an exact decimal tie: the close equals the SMA (JBLU 2012-02-07, 5.95 vs 5.950; CRVS
    2023-06-12; GSM 2026-08-17; OMER 2026-08-26, two trades; DSP 2026-09-23; API 2022-03-28; FULC 2025-05-27;
    LLNW 2019-10-31; GRCL 2024-01-11), or the target equals the entry (APLD 2022-08-08, 2.13). In exact
    arithmetic "close below MA" is false; my float64 mean of float32 prices is off by 1e-8 and says true.
    **My side is wrong; the author's is right.**
- Same replay with the moving average rounded to the stored float32 precision: **0 of 67,967 differ** (maximum
  |d ret| and |d R| are 0.0).
- Closing the loop without `qm.sim` or `qm.run`: author's raw signals -> my simulator -> my own one-position
  rule gives exactly the CSV trade sets for 14 files, plus only the trades `_drop_twins` removes; 50,700 common
  trades, 0 differ.
- Modes not saved to CSV (day-0 optimistic and pessimistic, no partial, partial 1/2, no breakeven, SMA20 and
  SMA50 trails, 50 bp cost, 0.5 ADR stop, E-open close-based, E-orb in all three modes, P-open with +30% and
  +100% stops in all three day-0 modes, P-red with SMA20 target, without target, with 100 bp and 300% borrow):
  40 runs, **140,793 trades, 0 mismatches**, including partial day and price.
- The author's `test_sim.py` passes on the current code.

### 3.6 (d) Ten trades by hand (`a18_spot.py`)

Bars printed and each number recomputed by hand from the rules.

| trade | check | result |
|---|---|---|
| Q0 LEU 2021-11-01 | pivot 57.80 set 9 rows earlier; open 56.89, high 61.20 -> fill 57.80; stop 57.80 x (1 - 0.0968) = 52.20; 1/3 sold at 70.29 on session 3; first close below SMA10 on 11-17 -> out at next open 68.21 | +18.85%, +1.950R, as in CSV |
| Q0 EBS 2008-12-31 | fill at pivot 26.35 (high 26.40); stop 24.17; low 24.11 on 01-05, open 25.00 above stop -> filled at stop | -8.54%, -1.035R |
| C0 AGTC 2020-01-22 (dolt) | close 9.86 above pivot 9.50; low-of-day distance 16.9% capped at 1 ADR (15.2%) -> stop 8.36; next open 7.00 below stop -> filled at open | -29.22%, -1.926R |
| E-close MXL 2015-11-04 | gap 12.03%, volume 8.49x, close in top 1% of range; stop capped at 1.5 ADR = 15.82; 1/3 at 17.06 on session 3, rest at breakeven | +0.23%, +0.041R |
| E-close SIG 2022-12-06 (dolt) | gap 10.67%, volume 7.35x; first profitable close on session 5 (70.34); rest at breakeven on 12-15 | +0.08%, +0.011R |
| E-close earnings SMA20 TREE 2026-03-03 | stop = day low 41.02 (inside the 0.25–1.5 ADR band); low 39.83 on 03-09, open above stop | -12.52%, -1.023R |
| E-open NCTY 2021-01-29 | open 186.50, stop 131.82; day-0 low 142.10 above stop; 1/3 at 198.80 on session 4; close below SMA10 on 02-23 -> out at 609.30 | +152.57%, +5.212R |
| E-open NTCO 2022-10-18 (dolt) | open 5.73, stop 5.42, day-0 low 5.35 -> stopped on day 0 | -5.74%, -1.054R |
| P-red OUST 2024-04-04 | 5-day run 100.8%; first red close 9.99; stop = run high 11.40; 04-10 opens 8.28 below target 8.72 -> covered at open; borrow 4 days | +15.41%, +1.092R |
| P-red MCRB 2020-08-11 (dolt) | run 455% (a one-day news gap); short 400.8, stop 660; no target hit; time exit at 490.4 after 10 sessions | -25.45%, -0.394R |

All ten match the CSV to the printed precision.

### 3.7 (e) Split and cleaning logic, `rawclose` (`a08`, `a10`, `a10b`, `a16`–`a19b`, `a17`)

- **`rawclose` is the as-traded close** for 16 checks from memory on HF and 13 on dolt, most on the last session
  before a split: AAPL 499.23 (2020-08-28), 645.57 (2014-06-06), 88.99 (2005-02-25); TSLA 2213.40, 891.29; NVDA
  751.19, 1208.88; AMZN 2447.00; GE 12.95; C 4.52; AIG 1.16; NFLX 702.60; CMG 3283.04; BRK-B 3476.00; MSFT
  336.32; SPY 222.95. All match to the cent. Two further values differ from my recollection (GOOGL 2022-07-15:
  2235.55 vs 2255.34; SHOP 2022-06-28: 350.26 vs about 334); both panels agree with each other, so I put these
  down to my memory. `rawclose` is wrong where the vendor's split table and price series disagree (finding 6).
- **HF panel vs vendor parquet**: on 300 random columns, 1,060,934 bars compared; closes differ in 15 columns
  (27,454 bars, all OTC or penny names, consistent with rescale repairs); 23 vendor bars are absent from the
  panel (blanked); no panel bar is absent from the vendor file.
- **Does the repair touch genuine moves? Yes**, in three ways (findings 5 and 6):
  - Blanking removed the TOP Financial squeeze in both panels.
  - Rescaling zeroes the real return on the day of a reverse split whose table entry was rejected or missed:
    dolt median -12.5%, 37 cases beyond 25%; HF DFNS 2026-07-20 -19%.
  - Rescaling all earlier history for a one-bar bad print (AIXN 2019-01-04) or an alternating-scale glitch (JUNS)
    leaves or creates a fake crash.
- **Sample of 15 per panel.** HF: 372 candidate events (181 rescaled, 169 blanked, 22 left untouched), 35
  touching the liquid universe; verdicts in finding 6. dolt: 2,748 flags = 2,531 table splits + 208 rescaled + 9
  blanked. Of the 9 sampled dolt rescales, 8 are real reverse splits (BHG, TRKA, OSG~1, TTOO, CING, ADTX, REVB,
  NEPH~1) with that step's return erased (-14%, +14%, -4%, -52%, -18%, -25%, -20%, -12%), and 1 is an illiquid
  OTC name I cannot judge (BYRN~2). Of the 6 sampled blanked cases, 5 are bad prints removed correctly (CZR
  2019-06-13, SPB 2014-10-16, MSGN 2016-02-25, ACET~1 2018-11-02, ALTU 2022-06-09) and 1 is genuine (TOP).
- **Do the leftovers reach the saved trades?** Trades with a split- or glitch-related jump inside their
  look-back window: 5 of 1,463 (Q0 HF), 69 of 18,089 (E-open HF), 7 of 1,361 (P-red HF), 2 of 710 (Q0 dolt), 64
  of 11,946 (E-open dolt), 5 of 1,082 (P-red dolt). Large jumps inside a holding period are real events in every
  case I looked at (CDMO 2012-09-24, EH 2021-02-16, OST 2025-06-26, IRBT 2025-12-15, LODE 2021-02-17).
- The worst outcomes in the parabolic event study (-999%, -1702%) are real: DRUG 2024-10-15, HKD 2022-07-29,
  QMMM 2025-09-09.

### 3.8 Calendar, missing bars and cross-source agreement (`a09`, `a09b`, `a11`, `a12`, `a25`)

- Interior missing bars: dolt 328,860 (1.91% of in-span cells, 7,969 of 10,891 columns); HF 37,239 (0.14%, 320
  columns). HF has no day on which fewer than 80% of the usual symbols print; dolt has one (2020-02-17).
- Same (date, symbol) trade in dolt and hfwin: 527 of 710 Q0 trades are common, 514 with the same exit date,
  mean R -0.092 in both; E-close 2,296 common, 2,259 same exit, mean R -0.062 in both; E-open 9,106 common,
  -0.033 vs -0.034; P-red 731 common, -0.001 vs -0.000.
- Between 6% and 32% of each list has no counterpart in the other source: different rank cut-offs in a larger
  universe, renamed tickers (PTHL/ITOC, KIRK/TBHC, GLYC/CBIO), and names present in only one source.
- Because of findings 3–7, the difference between the dolt and hfwin averages is not a clean measure of
  survivorship.

### 3.9 (f) `dedupe_open` and same-day duplicates (`a15_dedupe.py`, `a13_counterfactuals.py`, `a25_followups.py`)

- `dedupe_open` is causal. A signal is dropped if and only if the previously kept trade in that symbol has
  `exit_day >= t0`, which is known at t0. My own implementation gives identical trade sets in 14 files.
- It is not neutral in size: blocked signals would have averaged -0.22R (Q0, 26 signals), -0.65R (E-close, 87)
  and -0.34R (E-open, 1,135) on HF. Allowing re-entry on the day a trade leaves at the open changes avg R by at
  most 0.001.
- `_drop_twins` is the problem (finding 2). On HF it mostly removes true duplicate listings (15 of 15 for Q0, 33
  of 33 for E-close, 42 of 42 for P-red, 171 of 174 for E-open). On P-open it removes 31 (HF) and 22 (dolt)
  different companies, all stopped out (30 on HF by a stricter identity test on 60 days of returns).

### 3.10 (g) `portfolio_sim` (`a14_portfolio.py`)

Three trades, 10 bp cost, risk 1%, start 100,000: A (entry 100, stop 95, half sold at 108 on day 2, rest at 100 on
day 4), B (entry 50, stop 48, stopped on the entry day), C (entry 21 at the close of day 3, exit 22 on day 5).

| day | hand calculation | `portfolio_sim` |
|---|---|---|
| 0 | 200 sh of A; 99,980.00 | 99,980.00 |
| 1 | 499.9 sh of B in and out at 48; 99,731.2098 | 99,731.2098 |
| 2 | half of A at 108; 100,520.4098 | 100,520.4098 |
| 3 | 1,005.204098 sh of C; 100,699.300514 | 100,699.300514 |
| 4 | rest of A at 100; 100,694.504612 | 100,694.504612 |
| 5 | C at 22; 100,672.390122 | 100,672.390122 |

Maximum difference 0.0. A short with a 1% daily borrow fee also matches (99,800; 100,610; 101,610). The
ordering issue is finding 15.

### 3.11 Statistical methodology (`a22_stats.py`, `a21_day0.py`)

- Clustering (finding 12). Mean R with naive, by-day and by-month t: Q0 -1.64 / -1.59 / -1.45; C0 -3.89 / -3.80
  / -3.66; E-close -5.24 / -4.67 / -3.64; E-open -8.09 / -3.88 / -3.06; P-red +1.62 / +1.57 / +1.32. The ten
  busiest days hold 6.7% (HF) and 9.7% (dolt) of E-open trades.
- R against stop distance (finding 11). E-close HF by risk quintile, tight to wide: -0.165, -0.055, -0.107,
  +0.012, -0.242 R. dolt P-red tightest quintile: -0.299R with mean return +1.80%.
- The two positive results after the corrections above:
  - P-open +30%: +0.148R, month-clustered t +5.1 (HF); +0.102R, t +2.8 (dolt). By era on HF: +0.33, +0.26,
    +0.21, +0.07. Borrow availability is an assumption, and 34% of the dolt trades are in tickers that later
    disappeared.
  - Earnings EP with SMA50 trail: HF +0.250R, month-clustered t +2.5, mean return +1.22% (t +2.1), and the top
    21 trades account for more than all of the profit; dolt +0.339R after fixing the moving average.
- `top5%` in the logs is a ratio to total R and is meaningless when the total is negative or near zero (-355%,
  20,781%).
- The parabolic screen does not separate a multi-day run from a one-day news gap after three small up closes
  (MCRB 2020-08-10, +389% on trial data). That is a rule-design point, not a bug.

## 4. Not verified

- Vendor prices against a third source. No web access was used. The two sources agree with each other on common
  trades, but they may share errors; as-traded closes were checked from memory for 16 values on 12 tickers only.
- The SEC `first_tradeable_session` field beyond the 10 report dates in finding 17.
- `compute_features` on a full panel (memory cap). The cache was checked against an independent computation on
  611 and 538 sampled days for all symbols, and the code path on the sub-panels.
- A full rebuild of either panel. HF was compared with the vendor file on 300 random columns and on every glitch
  candidate; dolt was compared with the raw CSV only for the sampled symbols.
- The outputs of `run_portfolio.py`, `run_universe.py`, `run_clustered_t.py` and `make_charts.py` (added during
  the audit). Note that `run_portfolio.py:110` builds its short book from P-open, so finding 2 applies to it, and
  `:82` uses `day0_mode=2` for the main breakout curve (finding 1).
- Stale files `breakout_trades_A0*.csv`, `breakout_trades_B0.csv`: the variants no longer exist in the driver.
- Borrow availability and fees, intraday slippage, halts, and anything that needs intraday data.
- The report and research notes outside `backtest/`.

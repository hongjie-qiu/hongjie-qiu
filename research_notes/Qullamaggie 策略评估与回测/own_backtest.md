# Independent backtest of the three setups (run in this session, 2026-11-19)

Scope: an original, rule-based, daily-bar backtest of Kullamägi's three setups on US stocks, built for this
report. Code is in `/home/user/hongjie-qiu/backtest/src/`, raw outputs in `/home/user/hongjie-qiu/backtest/results/`.
Every number below was produced by that code in this session ([D] = computed directly). Interpretation is
kept in clearly marked "Inference" paragraphs.

**Status of verification:** the simulator has unit tests on hand-built bars (`src/test_sim.py`, all pass). An
independent code audit (look-ahead, fill logic, accounting) was commissioned in parallel; see
`/home/user/hongjie-qiu/backtest/AUDIT.md` and the "Audit outcome" section at the end of this file.

---

## 0. Summary of what the backtest found

1. **The scan universe has negative drift.** Stocks in the top 2% of his own momentum measure with ADR >= 4%
   ("leaders") underperformed SPY by 1.1% over the next 20 days on average in 2005-2026 (t = -2.4), and by 3.6%
   in 2022-2026 (t = -3.4). The academic 12-2 momentum top decile in the same data was roughly flat (+0.2%).
   Holding what the scan shows is a losing proposition; any edge has to come from which names are picked and when.
2. **Mechanical breakouts have no edge on daily bars.** The rule-faithful baseline (1,463 trades, 2005-2026,
   15 bp per fill) averaged -0.06R per trade (t = -1.6); the 27 variants tested ranged from -0.20R to +0.01R,
   none with a t-stat above +0.2. A control that bought the same trending leaders on random days with the same
   exits averaged -0.05R. A portfolio run lost 2.3% a year with a 50% drawdown.
3. **Episodic pivots: most large gaps are traps; only earnings gaps hold, and only with a wide trail.** All
   gap-ups >= 10% lost 3.1% versus SPY over the next 20 days (t ~ -5.9). Non-earnings gaps lost 6.7%; earnings
   gaps were flat (+0.4%). Managed with his standard rules (partial after 3-5 days, breakeven stop, 10-day trail)
   earnings EPs bought at the close averaged -0.05R. Held with a 50-day trail and no breakeven stop they averaged
   +0.25R (t = 3.2), positive in all four eras - but the portfolio made 4.6% a year against 10.6% for SPY, with
   zero factor alpha.
4. **Parabolic shorts carry the only strong mechanical signal - and the worst practical problems.** Shorting
   the open after a >= 100% five-day run made a median +15.6% in five days (71% winners) in every era. After
   50 bp per fill and 50% annual borrow the rule earned about +5% per trade (t = 6.5); at 100 bp and 100-300%
   borrow the edge is zero to negative. Real squeezes of +500% to +3,900% within days are in the sample.
5. **Intraday entries cannot be judged from daily bars.** For an opening-range entry proxy on EP days the
   average result swings from -0.47R to +0.60R purely on the assumed order of the day's high and low. Any
   daily-bar backtest of his opening-range-high entry (including most published ones) bakes in one of these
   assumptions.
6. **Survivorship bias does not drive these conclusions.** Re-running 2019-07 to 2026-01 on a
   delisting-inclusive dataset (5,397 dead tickers) gave the same picture as the survivors-only data for the
   same window.

---

## 1. Data

| Item | Source | Coverage | Notes |
|---|---|---|---|
| Panel A - main, long history | Hugging Face `defeatbeta/yahoo-finance-data`, `stock_prices.parquet`, snapshot of 2026-11-18 | 1999-12-31 -> 2026-11-17; 7,559 columns after cleaning (7,554 common stocks + SPY, QQQ, IWM, QQQM, DIA) | Yahoo prices, split-adjusted, not dividend-adjusted. **Survivors only**: contains tickers still listed in about 2024-2026 (TWTR, ATVI, SIVB, LEH, YHOO are absent). Results use 2005-01-03 onward. |
| Panel B - delisting-inclusive | Hugging Face `siddharthmb/stocks-ohlcv` + `stocks-splits` + `stocks-symbols` (same schema as DoltHub `post-no-preference/stocks`; static snapshot of 2026-01-29) | 2011-01-03 -> 2026-01-28; 10,891 columns, 10,885 common; **5,397 common columns no longer trade on the last day** | Raw prices, back-adjusted here with split events validated against the actual overnight price change (2,029 + 502 applied, 581 rejected as spurious). Coverage of then-listed stocks is essentially complete from mid-2019 (on 2021-03-04 it holds 98.5% of that day's Nasdaq-screener common stocks, incl. TWTR, SIVB, ATVI, XLNX, FRC; in mid-2018 it still lacks TWX, MON, AET). Used for 2019-07-01 -> 2026-01-28 only. |
| Earnings days | SEC 8-K Item 2.02 filings, Hugging Face `ZipLime/earnings-calendar` | 2003-04 -> 2026-11; 458,349 releases, delisted companies included | Gives the first session in which the release can be traded. 278,079 filings matched to Panel A. |
| EPS surprise | Nasdaq earnings-calendar API, one request per weekday 2008-2026 (4,927 days, 234,503 rows) | 2008 -> 2026 | Survivors only; used only for the "EPS surprise" lines. |
| Benchmarks, factors | SPY and QQQ total return (dividends added); Ken French daily Mkt-RF, SMB, HML, Mom, RF | to 2026-11-17 / 2026-09-30 | QQQ in Panel A stops 2026-09-11 and is spliced with QQQM returns after that. |

Cleaning applied to both panels [D]: bars with non-positive prices dropped (28,638 in A); 276 duplicate series
removed in A (one company under old and new ticker); warrants, units, rights, preferreds, OTC foreign shares,
ETFs/funds and SPAC shells excluded by ticker pattern / security name / missing sector; "scaling glitches"
(price jumps >= 5x with share volume falling by the same factor - misdated reverse-split adjustments) repaired
(A: 168 blanked, 184 rescaled; B: 9 and 208); signals within 10 sessions either side of a split ex-date are
skipped; trades that are bar-for-bar copies of another trade are dropped.

Not available for free and therefore not in the test: intraday bars (so no true opening-range entries or
low-of-day stops), borrow availability and actual borrow fees, point-in-time fundamentals, delisted stocks
before 2019.

---

## 2. Definitions (his own where he gives them)

- **Liquid universe**: common stock, as-traded close >= $3, 20-day average dollar volume >= $3M. Average 1,967
  names a day in Panel A (2005-2026), 2,904 in Panel B (2019-2026).
- **ADR%**: his TC2000 formula, `100*(mean over 20 days of High/Low) - 1`.
- **Momentum**: his scan measure - close divided by the lowest low of the last 22, 65 and 126 sessions - ranked
  across the liquid universe each day. **Leader** = top 2% on any of the three horizons and ADR >= 4% (he states
  "top 1-2%"; his actual TC2000 scans used about the top 7%, tested as a variant). Average 63 leaders a day
  (A), 97 (B).
- **Sanity check of the universe** [D]: leaders on 2020-06-15 include TSLA, ZM, MRNA, NKLA, CRWD, PENN, DKNG,
  NIO, NVAX, FSLY, W; on 2021-01-15 NIO, PLUG, QS, MARA, FCEL, BNGO, BLNK, RIOT, GME; on 2023-06-01 PLTR, AI,
  SMCI, CVNA, IONQ, APP, AFRM - the names he was streaming at those times.
- **Market regime**: QQQ 10-day SMA above the 20-day SMA and both rising (his stricter wording). On 47% of days
  since 2005 (63% without the "both rising" clause).
- **R multiple**: net profit per share divided by the initial stop distance. Because the daily-bar stop (about
  1x ADR, 8-9% of price for these names) is two to three times wider than his real low-of-day stops, R numbers
  here are compressed relative to the R multiples he quotes; percentage returns per trade are comparable.

### Fidelity of each rule

| His rule | How it is coded | Fidelity |
|---|---|---|
| Top 1-2% by 1/3/6-month move, ADR filter, liquidity | exactly as above | faithful |
| 2-week to 2-month consolidation, higher lows, tightening, surfing 10/20-day | pivot = highest high of the last 40 sessions, set >= 5 sessions ago; pullback <= 5 ADR; 5-day range < 20-day range; low of last 5 days above low of prior 5; close > SMA20 and SMA50, SMA10 > SMA20 > SMA50 | proxy (shape rules are a crude stand-in for his eye) |
| Buy the opening-range high on the breakout day | buy-stop at the pivot: fill = max(pivot, open); skipped if that is > 1 ADR above the prior close (his "don't chase" rule) | proxy - daily bars cannot see the opening range |
| Stop at the low of the day, never wider than 1 ADR | stop = entry - 1 x ADR (0.5 and 1.5 as variants); entry-day ambiguity bracketed three ways | proxy |
| Sell 1/3-1/2 after 3-5 days, stop to breakeven | sell 1/3 at the first profitable close on/after the 3rd session after entry, then stop = entry | faithful |
| Trail the rest on the 10-day (or 20-day); exit on first close below | exit at the next open after a close below the SMA | faithful |
| Breakouts only when the market is "on" | regime filter above | faithful |
| EP: gap >= 10% on huge volume, buy opening-range high, stop low of day | three versions: buy the open; an opening-range proxy; buy the close of a gap day that had >= 3x volume and closed in the top half of its range, stop = that day's low (bounded 0.25-1.5 ADR) | open/ORB versions are proxies; the close version is exact for what it is, but it is a later, more conservative entry than his |
| Parabolic short: +50-100% (large) / +300-1000% (small) in days, 3-5 up days, short the first crack, stop high of day, cover at 10/20-day | "parabolic" = 5-day gain >= 100%, >= 3 consecutive up closes, >= 30% above SMA10, day dollar volume >= $10M; (a) short next open with a +30% stop, (b) short the close of the first red day, stop = high of the run; cover at the 10-day SMA or after 10 days | proxy |
| Discretionary selection ("I pass on most setups"), themes, catalysts, position pyramiding | not coded | **not testable** |

---

## 3. Results

Costs unless stated: 15 bp per fill for longs (entry, partial, final exit); 50 bp per fill plus 50% a year borrow
for shorts. Panel A, 2005-01-03 -> 2026-11-17 unless stated.

### 3.1 What the scan universe does on its own [D]

20-day forward return minus SPY, equal-weighted across names each day (t-stats use daily cross-sectional means,
deflated for overlapping windows):

| Group | 2005-2026 | 2005-2012 | 2013-2018 | 2019-2021 | 2022-2026 |
|---|---|---|---|---|---|
| Liquid universe | -0.07% (t -0.5) | +0.37% | -0.13% | -0.30% | -0.58% |
| ... with ADR >= 4% | -0.21% (t -0.7) | +0.29% | -0.20% | -0.46% | -0.96% |
| **Leaders (top 2% any horizon, ADR >= 4%)** | **-1.13% (t -2.4)** | -0.06% | -0.68% | -0.93% | **-3.62% (t -3.4)** |
| Top 2% by 1-month gain | -1.75% (t -3.1) | -0.06% | -1.20% | -2.21% | -5.24% (t -4.2) |
| Top 2% by 3-month gain | -1.49% (t -2.6) | -0.15% | -1.12% | -1.17% | -4.49% |
| Top 2% by 6-month gain | -1.32% (t -2.4) | -0.15% | -0.80% | -0.69% | -4.32% |
| Top 7% any horizon (his real scan cut-off) | -0.42% (t -1.1) | +0.24% | -0.30% | -0.54% | -1.69% (t -2.2) |
| Academic 12-2 momentum, top decile | +0.16% (t +0.5) | +0.29% | +0.10% | +0.37% | -0.14% |
| Academic 12-2 momentum, bottom decile | -0.33% (t -0.8) | +0.53% | -0.60% | -0.24% | -1.53% |

Leaders also lagged at 5 days (-0.40%, t -3.2) and 60 days (-1.45%, t -1.0; -7.0% in 2022-2026). On the
delisting-inclusive Panel B (2019-07 -> 2026-01) leaders lagged by 2.52% over 20 days (t -2.3).

Inference: the extreme-winner, high-volatility corner he fishes in is exactly where the literature's lottery /
MAX effect and short-term reversal live; plain momentum (12-2, deciles) is a different, milder thing. His
method therefore is not "ride momentum"; it is "pick the few continuations out of a pool that on average
reverts", and the pool has become markedly worse since 2022.

### 3.2 Breakouts [D]

Event view (regime on, 1,504 signals): from the pivot fill to the same day's close +0.50% on average (median
+0.13%, 51% up); fill to +1 day minus SPY +0.14%; to +5 days -0.37%; to +20 days -1.18% (median -2.95%).
Breakouts bought at the close after confirmation: +1 day -0.16%, +5 days -0.66%, +20 days -1.97% versus SPY.
The entry day's low was a median 4.2% below the fill; it was at least 1 ADR below the fill on 9% of days and at
least 0.5 ADR below on 62% - which is why a low-of-day stop cannot be modelled from daily bars.

Trade results (R per trade, net):

| Variant | Trades | Win rate | Avg R | t | Avg return | 2005-12 | 2013-18 | 2019-21 | 2022-26 |
|---|---|---|---|---|---|---|---|---|---|
| **Q0 baseline** (pivot stop-entry, 1 ADR stop, regime on, entry-day handling "close-based") | 1,463 | 44.0% | **-0.062** | -1.6 | -0.44% | +0.03 | -0.06 | -0.03 | -0.16 |
| Q0, entry day pessimistic (low <= stop => out) | 1,464 | 41.7% | -0.111 | -3.0 | -0.82% | -0.02 | -0.12 | -0.09 | -0.19 |
| Q0, entry day optimistic (entry-day low ignored) | 1,463 | 44.0% | -0.067 | -1.8 | -0.48% | +0.03 | -0.07 | -0.04 | -0.17 |
| C0 close-confirmed entry, low-of-day stop | 911 | 40.0% | -0.204 | -3.9 | -1.15% | -0.34 | -0.22 | -0.14 | -0.13 |
| Q0 without regime filter | 2,677 | 45.1% | -0.027 | -1.0 | -0.27% | +0.00 | +0.03 | +0.01 | -0.12 |
| Q0 top 7% leaders | 3,620 | 42.3% | -0.079 | -3.2 | -0.35% | -0.07 | -0.09 | +0.02 | -0.16 |
| Q0 consolidation 10-40 days only | 546 | 44.0% | +0.010 | +0.1 | -0.03% | +0.15 | +0.17 | +0.05 | -0.26 |
| Q0 stop 0.5 ADR | 1,470 | 32.7% | -0.029 | -0.4 | -0.11% | +0.11 | +0.03 | -0.03 | -0.19 |
| Q0 zero cost | 1,463 | 48.1% | -0.019 | -0.5 | -0.14% | +0.08 | -0.01 | +0.00 | -0.12 |
| **Control: random entry at the open in trending leaders, regime on, same exits** (20 seeds, ~3,700 trades each) | - | 39.0% | **-0.051** (range -0.11 to +0.03) | - | -0.49% | | | | |

All 27 variants (leader cut-off, momentum definition, ADR floor, liquidity floor, consolidation length and depth,
tightness, volume dry-up, extension rule, stop width, partial size, breakeven on/off, 10- vs 20-day trail, costs
0-50 bp) are in `results/breakout_variants.csv`; the full table is reproduced in the appendix. The best is +0.01R
(t = +0.15); none has a t-stat above +0.2.

Other facts [D]: average holding 5.6 sessions; 64% of exits are stops, 35% trailing exits; average stop distance
8.6% of price. **Profit concentration**: the baseline's total is -90.7R; the top 10 trades made +86.7R, the top 1%
(14 trades) +109.6R, all the others -200.3R. Best trades are recognisable leaders (VKTX Feb 2024 +18.2R / +137%,
EH Jan 2021, NVAX Jun 2020, AFRM Nov 2023, SMCI May 2023).

Q0 by calendar year (average R): 2005 +0.22, 2006 +0.03, 2007 -0.06, 2008 -0.12, 2009 -0.03, **2010 +0.40**, 2011
-0.39, 2012 +0.02, **2013 +0.25**, 2014 -0.20, 2015 -0.24, 2016 +0.15, 2017 -0.32, 2018 -0.15, 2019 -0.07,
**2020 +0.13**, 2021 -0.20, **2022 -0.39**, 2023 -0.18, 2024 -0.19, 2025 +0.14, 2026 -0.33 (to mid-November).

Inference: (a) the breakout trigger adds a small same-day pop (+0.5%) and nothing afterwards; under identical
trade management it is indistinguishable from buying the same stocks on random days. (b) The yearly pattern
matches practitioner folklore - 2010, 2013, 2016, 2020 good; 2011, 2015, 2017, 2022 bad - so the test is
picking up the same regime the discretionary traders feel, just without their profits. (c) The P&L shape he
describes (most trades lose a little, a handful pay for everything) is reproduced, but mechanically the handful
does not cover the rest. (d) The regime filter did not help in this test (-0.06R with it, -0.03R without).

### 3.3 Episodic pivots [D]

Event study - return after the gap-day close, minus SPY (liquid common stocks, gap = open vs prior close >= 10%):

| Subset | Events | Gap-day open->close | +5 days | +20 days | +60 days |
|---|---|---|---|---|---|
| All gaps >= 10% | 19,398 | -0.89% | -1.47% | **-3.05%** (median -3.07%, t ~ -5.9) | -2.50% |
| Volume >= 3x average and >= $10M traded | 11,529 | +0.65% | -1.80% | -3.78% (t ~ -5.6) | -4.40% |
| ... and closed strong (above open, top half of range) | 4,658 | +10.52% | -1.40% | -2.22% (t ~ -3.1) | -2.35% |
| ... but closed below the open | 5,659 | -8.33% | -2.06% | -4.61% | -5.59% |
| **Earnings reaction day** | 4,737 | +1.28% | -0.19% | **+0.38%** (median -0.06%, t ~ +0.6) | +0.68% |
| **Not an earnings day** | 6,792 | +0.21% | -2.93% | **-6.66%** (t ~ -6.6) | -7.97% |
| Earnings + strong close | 2,217 | +7.36% | -0.26% | +0.48% (t ~ +0.2) | +0.71% |
| Earnings + EPS surprise >= +20% | 2,178 | +1.67% | -0.12% | +0.61% | +0.49% |
| Gap 10-20% / 20-40% / >= 40% | 8,069 / 2,615 / 845 | | | -2.02% / -5.50% / -15.27% | |
| "Neglected" (prior 6-month return within +/-30%) | 5,470 | | -0.46% | -1.29% | -1.94% |
| Already extended (prior 6 months > +50%) | 2,638 | | -3.43% | -6.76% | -8.05% |
| Volume >= 10x | 2,882 | | -4.34% | -8.09% | -12.48% |

By era, +20 days, volume-qualified gaps: 2005-12 +0.49%, 2013-18 -2.16%, 2019-21 -4.14%, 2022-26 -5.47%;
earnings gaps only: +1.28%, +1.00%, -0.59%, +0.11%.

Trade results:

| Variant | Trades | Win rate | Avg R | t | Avg return | 2005-12 | 2013-18 | 2019-21 | 2022-26 |
|---|---|---|---|---|---|---|---|---|---|
| Buy the close of a strong EP day, low-of-day stop, his 3-5 day / 10-day rules | 4,538 | 41.1% | -0.111 | -5.2 | -1.2% | -0.10 | -0.15 | -0.20 | -0.06 |
| ... earnings gaps only | 2,215 | 45.6% | -0.052 | -1.9 | -0.2% | -0.08 | -0.10 | -0.12 | -0.00 |
| ... earnings only, 20-day trail | 2,214 | 45.3% | -0.015 | -0.5 | -0.0% | -0.04 | -0.07 | -0.08 | +0.04 |
| **... earnings only, 50-day trail, no partial, no breakeven stop** | 2,198 | 25.3% | **+0.250** | +3.2 | +1.2% | +0.39 | +0.14 | +0.19 | +0.27 |
| ... all gaps, 50-day trail, no partial/breakeven | 4,482 | 23.7% | +0.155 | +2.3 | +0.2% | +0.26 | -0.05 | +0.13 | +0.21 |
| ... non-earnings gaps only | 2,333 | 36.9% | -0.165 | -5.1 | -2.1% | -0.14 | -0.20 | -0.24 | -0.12 |
| Buy the open, 1 ADR stop - entry day pessimistic | 18,089 | 30.1% | -0.116 | -8.1 | -1.4% | -0.20 | -0.18 | -0.08 | -0.09 |
| Buy the open, 1 ADR stop - entry day close-based | 17,936 | 36.3% | +0.077 | +4.1 | -0.4% | -0.05 | +0.09 | +0.05 | +0.13 |
| Opening-range proxy (buy open + 0.25 ADR, stop open - 0.25 ADR) - pessimistic | 13,566 | 12.0% | **-0.469** | -21.6 | -2.0% | | | | |
| Opening-range proxy - close-based | 13,278 | 31.7% | **+0.605** | +13.7 | +1.2% | | | | |
| Opening-range proxy - optimistic | 13,204 | 32.3% | +0.003 | +0.1 | -0.7% | | | | |

Earnings EP with 20-day trail by year (avg R): 2005 +0.48, 2006 -0.18, 2007 -0.00, 2008 -0.31, 2009 -0.12, 2010
-0.03, 2011 -0.15, 2012 +0.10, 2013 -0.17, 2014 -0.17, 2015 -0.33, 2016 +0.12, 2017 +0.09, 2018 -0.07, 2019 -0.16,
2020 -0.04, 2021 -0.03, 2022 -0.14, **2023 +0.30**, 2024 +0.10, 2025 +0.08, 2026 -0.17.

Anatomy of the one profitable variant (earnings gaps, close entry, 50-day trail; the 1,634 trades the portfolio run
actually took) [D]: total +325R, of which the 20 best trades made +410R - without them the
rule is net negative. 67% of trades were roughly full 1R losses, 5.5% made 5R or more, 2.3% made 10R or
more. The big winners are the textbook cases from his own model book: NVDA May 2016 (+136% over 197 sessions,
+43.8R), LULU Sep 2010 (+125%), TSLA Oct 2019 (+119%), AMZN Apr 2007, FSLR Feb 2007, TWLO Feb 2018, ENPH May
2019, SMCI Jan 2024 and May 2023, PLTR May 2023, META Jul 2013. Caveat: 5% of the trades left through the
trailing rule within two sessions because the stock was still below its 50-day average when bought (a quirk of
applying a 50-day trail to beaten-down names; those trades averaged -0.07R).

Inference: (a) "A big gap on big volume" by itself is a sell signal on average, strongly so for non-earnings news,
huge gaps, huge volume and already-extended stocks - the population is dominated by promotions, offerings and
one-day squeezes. (b) Earnings gaps are the exception but the post-gap drift is small (well under 1% over 20-60
days) and statistically indistinguishable from zero here, consistent with the papers reporting that
post-earnings drift has faded in liquid stocks. (c) The only profitable formulation is the patient one - earnings
gaps that close strong, held with a wide trail and without the breakeven stop - which is a positively skewed bet
(25% winners averaging about +4R). It is one of about 20 variants tried, so some of its t = 3.2 is selection.
(d) His standard short-term management (partials, breakeven, 10-day trail) turns the same entries into a small
loser on daily bars: it cuts the right tail that is the whole source of profit. His blog does allow trailing EPs
on the 20/50-day. (e) "Neglected" stocks did better than extended ones, as he says, but still not positive.
(f) The opening-range rows show that the true result of his actual entry is unknowable from daily data.

### 3.4 Parabolic shorts [D]

Event study - profit of a short opened at the next open after a parabolic close, no stop, no costs:

| Definition | Events | +1 day | +5 days | +10 days | +20 days | Worst 5-day |
|---|---|---|---|---|---|---|
| 5-day gain >= 100%, >= 3 up closes, >= 30% over SMA10 | 1,387 | mean +3.3%, median +8.9%, 66% win | mean +6.7%, **median +15.6%, 71% win** | +10.8% / +20.8% / 72% | +12.7% / +25.6% / 73% | **-1,701%** |
| 5-day gain >= 200% | 447 | +8.6% / +14.7% / 68% | +11.3% / +23.3% / 74% | +21.0% / +31.6% / 77% | +23.7% / +39.0% / 78% | -675% |
| 5-day gain >= 60% | 3,084 | +2.4% / +4.7% / 62% | +4.3% / +9.3% / 65% | +6.4% / +12.2% / 66% | +7.9% / +16.7% / 67% | -1,701% |
| 5-day gain >= 50% with >= $200M traded (liquid names) | 1,308 | +2.6% / +4.4% / 62% | +4.6% / +8.7% / 65% | +8.0% / +12.7% / 67% | +9.9% / +17.7% / 69% | -581% |

By era (5-day gain >= 100%, +5 days): 2005-12 n=100 mean +11.9%, 69% win; 2013-18 n=227 +13.1%, 72%; 2019-21 n=532
+9.3%, 77%; 2022-26 n=1,132 +7.1%, 68%. The number of qualifying events exploded: about 10 a year before 2016,
184 in 2020, 237 in 2025.

Trade results:

| Variant | Trades | Win rate | Avg R | t | Avg return on position | Worst trade |
|---|---|---|---|---|---|---|
| **Short next open, hard stop +30%**, cover at 10-day SMA or day 10 (entry day pessimistic) | 1,570 | 60.7% | **+0.171** | +6.5 | **+5.1%** | -112% |
| ... stop +50% / +100% | 1,498 / 1,416 | 67.6% / 73.9% | +0.079 / +0.044 | +4.1 / +3.8 | +3.9% / +4.4% | -161% / -303% |
| Short the close of the first red day, stop = high of the run, cover at 10-day SMA | 1,361 | 67.7% | +0.047 | +1.6 | +2.2% | -422% |
| ... zero costs | 1,362 | 70.6% | +0.140 | +5.4 | +4.0% | |
| ... 100 bp per fill, 100% borrow | 1,361 | 65.2% | -0.047 | -1.3 | +0.3% | |
| ... 100 bp per fill, 300% borrow | 1,361 | 58.0% | -0.197 | -4.4 | -3.1% | |

Era split for the +30% stop rule (avg R): +0.32, +0.28, +0.23, +0.11 - positive throughout, fading.

The left tail is real, not a data artefact: the largest adverse moves within five days of the signal were checked
bar by bar - QMMM (Sep 2025, close 11.3 -> 207 the next session), DRUG (Oct 2024, 2.49 -> 38.5), HKD (Jul-Aug
2022, 180 -> 1,680), MRIN (Jun 2021, 21 -> 104), SAVA (Feb 2021, 23 -> 88), INDO (Feb-Mar 2022). One case (CLEU,
Jan 2025) was a vendor scaling error and is removed by the cleaning rules.

Inference: this is the one setup where a blind rule shows a statistically solid edge, in line with the
short-term-reversal and lottery-stock literature. But (a) the names are overwhelmingly micro-caps where shares to
borrow are often unavailable and fees of 100-1,000% a year are normal, so the fills assumed here frequently could
not be had; (b) at 1% slippage per fill and 100% borrow the edge is gone; (c) one unhedged squeeze can cost several
times the position; (d) the edge has roughly halved since 2022 as the number of such events exploded. Position
sizes must therefore be tiny, which caps what the setup can contribute.

### 3.5 Survivorship check [D]

Same code, same window (2019-07-01 -> 2026-01-28), two datasets:

| Measure | Panel B (with 5,397 dead tickers) | Panel A (survivors only) |
|---|---|---|
| Breakout Q0, avg R (trades) | -0.066 (710) | -0.088 (675) |
| Breakout close-confirmed, avg R | -0.147 (425) | -0.110 (397) |
| Random-entry control, avg R | -0.015 | +0.014 |
| Gaps (volume-qualified), +20 days vs SPY | -3.74% (7,583 events) | -4.41% (6,686) |
| ... earnings gaps | +0.15% (2,609) | -0.12% (2,393) |
| ... non-earnings gaps | -5.84% (4,974) | -6.80% (4,293) |
| EP bought at close, standard rules, avg R | -0.075 (2,925) | -0.088 (2,551) |
| Earnings EP, standard rules | +0.037 (1,213) | +0.006 (1,121) |
| Earnings EP, 50-day trail | +0.423, t 2.8, +1.9% per trade (1,202) | +0.317, t 2.7, +1.6% (1,111) |
| Parabolic short, +30% stop | +0.122, t 4.2, +3.7% per trade (1,236) | +0.151, t 4.9, +4.5% (1,136) |
| Parabolic short, first red day | -0.020, +1.5% per trade (1,082) | +0.057, +2.3% (987) |

Inference: for trades that last days to weeks behind a stop, including dead stocks changes nothing material;
differences are inside the noise and not systematically in favour of the survivors-only data. The long-history
Panel A results are therefore usable. (This would not hold for buy-and-hold tests.)

### 3.6 Portfolio level [D]

$100,000 start, 0.5% of equity risked per trade, signals taken in priority order until a limit binds.
Longs: max 20% (breakouts) or 10% (EPs) per position, max 100% gross, max 20-25 positions.
Shorts: max 2% per position, 30% gross.

Panel A, 2005-01-03 -> 2026-11-17:

| Strategy | CAGR | Vol | Sharpe | Max drawdown | Final multiple | Avg gross exposure |
|---|---|---|---|---|---|---|
| Breakout Q0 (regime filter) | **-2.3%** | 8.1% | -0.47 | -50.5% | 0.60x | 10% |
| Breakout Q0, 1% risk, 140% gross (his 2020-21 exposure level) | -5.1% | 15.9% | -0.36 | -77.5% | 0.32x | 19% |
| Earnings EP, close entry, his 3-5 day / 10-day rules | -2.8% | 7.7% | -0.56 | -50.5% | 0.54x | 17% |
| **Earnings EP, close entry, 50-day trail** | **+4.6%** | 16.7% | 0.25 | -37.4% | 2.67x | 55% |
| All EPs, close entry, 50-day trail | +2.4% | 25.3% | 0.15 | -66.1% | 1.69x | 71% |
| **Parabolic short (+30% stop), 50 bp + 50% borrow** | **+6.2%** | 4.9% | 0.89 | -7.5% | 3.73x | 2% |
| Parabolic short, 100 bp + 150% borrow | +3.3% | 4.9% | 0.32 | -14.4% | 2.02x | 2% |
| SPY buy and hold (total return) | 10.6% | 18.9% | 0.54 | -55.2% | 9.05x | 100% |
| QQQ buy and hold (total return) | 15.1% | 21.6% | 0.68 | -53.4% | 21.27x | 100% |

Panel B (delisting-inclusive), 2019-07-01 -> 2026-01-28: Breakout Q0 -4.0% a year (max drawdown -45%); earnings EP
with 50-day trail +7.0% (vol 22.7%, drawdown -34.7%); earnings EP with his standard rules +1.5%; parabolic short
+10.7% (Sharpe 0.98; +2.7% with 100 bp and 150% borrow); SPY +15.6%; QQQ +20.8%.

Calendar years, Panel A (%):

| Year | Breakout Q0 | Earnings EP 50-day trail | Parabolic short | SPY | QQQ |
|---|---|---|---|---|---|
| 2008 | -2.0 | -11.1 | +2.8 | -36.8 | -41.7 |
| 2010 | +10.7 | +13.5 | +2.3 | +15.1 | +20.1 |
| 2013 | +9.6 | +19.0 | -0.3 | +32.3 | +36.6 |
| 2015 | -4.3 | -20.0 | +2.3 | +1.3 | +9.4 |
| 2017 | -10.6 | +5.0 | +6.5 | +21.7 | +32.7 |
| 2019 | -4.6 | +9.1 | +3.1 | +31.2 | +39.0 |
| 2020 | +9.2 | +18.9 | +35.5 | +18.4 | +48.4 |
| 2021 | -9.7 | +4.3 | +12.2 | +28.7 | +27.4 |
| 2022 | -12.0 | -23.8 | +3.8 | -18.2 | -32.6 |
| 2023 | -6.7 | +40.1 | +0.2 | +26.2 | +54.9 |
| 2024 | -14.6 | 0.0 | +9.9 | +24.9 | +25.6 |
| 2025 | +5.9 | -14.6 | +27.8 | +17.7 | +20.8 |
| 2026 (to 17 Nov) | -6.0 | +5.2 | +11.3 | +8.2 | n/a |

(All years are in `results/portfolio_yearly_hf.csv`.)

Factor regression of daily excess returns on Mkt-RF, SMB, HML, Mom (2005-2026): earnings-EP portfolio alpha
+0.3% a year (t = 0.1), market beta 0.39, SMB 0.45, HML -0.08, Mom +0.09, R-squared 0.31; on Panel B 2019-2026 alpha
0.0% (t = 0.0), beta 0.54, SMB 0.57. Breakout portfolio alpha -4.3% a year (t = -2.6).

Capacity (earnings EP, 50-day trail, each position capped at 1% of 20-day average dollar volume - his stated
limit): CAGR 4.6% at $100k, 7.3% at $1M, 6.6% at $10M, 3.1% at $100M (average exposure falls to 8% because most
candidates are too thin). The cap slightly improves results at small sizes because the least liquid names were
the worst.

Inference: (a) even the best long formulation is a small-cap-beta portfolio with no alpha, earning less than half
of what the index paid. (b) The parabolic-short line looks excellent per unit of capital used (2% average
exposure) and its good years (2020, 2025) coincide with speculative manias; scaling it up needs borrow that the
test assumes for free. (c) Nothing here approaches triple-digit annual returns. Mechanical rules at his stated
risk per trade produce single-digit outcomes; his reported results would need a large contribution from things
the rules do not contain: selection, intraday execution with far tighter stops, concentration and leverage,
adding to winners, and being fully engaged only in the few months that work.

---

## 4. What this backtest can and cannot say

It can say: on daily bars, with his published filters and trade management applied blindly, breakouts and standard
EPs have no edge after modest costs over 2005-2026 and none since he became widely followed (2022-2026 is the worst
era for breakouts and for leaders generally); the best mechanical long variant has no factor alpha; the parabolic
short has gross edge but is cost- and borrow-bound; survivorship does not explain these findings.

It cannot say that his actual trading has no edge. Specifically untested:
- **Intraday execution.** His entries are opening-range highs with stops at the low of the day, typically a third
  to a half of an ADR. Daily bars cannot order the intraday high and low; section 3.3 shows the answer for such
  entries can be anything between -0.47R and +0.60R. The best available intraday test of a closely related
  rule-set (a third-party study on CRSP/TAQ data of Martin Luk's rules, summarised in the third-party notes) found
  about +0.4% per trade before spreads and about zero after.
- **Discretion.** He says he trades on intuition, passes on most setups, and reads themes, catalysts and the tape.
  The test takes every signal.
- **Sizing dynamics.** Pyramiding into winners, 10-25% positions, 120-140% gross exposure and varying aggression
  with the regime are not modelled beyond a fixed fractional-risk rule.
- **Borrow.** Short availability and fees are assumed, not observed.
- **Pre-2019 dead stocks** are missing from the long-history panel (shown not to matter for 2019-2026).

Statistical cautions: about 60 variants were examined across the three setups, so isolated t-stats around 2-3
(notably the earnings-EP 50-day-trail result) should be discounted for multiple testing; trade-level t-stats
ignore cross-sectional clustering of trades entered on the same day; R averages weight tight-stop trades more
heavily than percentage returns do, so both are reported.

---

### Month-clustered significance [D]

Trades entered in the same calendar month share market conditions, so treating them as independent overstates
confidence. Re-computing the t-stats with entry-month clusters (`results/clustered_t_hf.txt`, `clustered_t_dolt.txt`):

| Setup (Panel A, 2005-2026) | Trades | Avg R | t, naive | t, month-clustered | Avg return | t of return, clustered |
|---|---|---|---|---|---|---|
| Breakout Q0 | 1,463 | -0.062 | -1.6 | -1.5 | -0.44% | -1.1 |
| Breakout, close-confirmed | 911 | -0.204 | -3.9 | -3.7 | -1.15% | -2.6 |
| EP bought at the close, standard rules | 4,538 | -0.111 | -5.2 | -3.6 | -1.19% | -4.2 |
| Earnings EP, standard rules | 2,215 | -0.052 | -1.9 | -1.4 | -0.24% | -1.0 |
| Earnings EP, 50-day trail | 2,198 | +0.250 | +3.2 | **+2.5** | +1.22% | +2.1 |
| Parabolic short, next open, +30% stop | 1,570 | +0.171 | +6.5 | **+5.8** | +5.14% | +5.8 |
| Parabolic short, first red day | 1,361 | +0.047 | +1.6 | +1.3 | +2.18% | +2.4 |

Panel B (2019-07 to 2026-01), month-clustered t of average R: breakout Q0 -0.9; earnings EP with 50-day trail +2.4
(return t +1.9); parabolic short next open +3.1; first red day -0.4. Conclusions are unchanged: nothing long is
reliably positive except the earnings-EP/50-day-trail variant at roughly t = 2.5 before any multiple-testing
discount, and the parabolic short at the next open stays strongly significant.

## 5. Figures (PNG, in `/home/user/hongjie-qiu/reports/figures/`)

- `fig1_equity.png` - equity multiples 2005-2026 (log axis): breakout rule 0.60x, earnings EP with 50-day trail
  2.67x, parabolic short 3.73x, SPY 9.05x, QQQ 21.27x.
- `fig2_intraday_assumption.png` - average R of the same signals under pessimistic / close-based / optimistic
  entry-day assumptions (breakout -0.11 to -0.06R; EP at the open -0.12 to +0.08R; EP opening-range proxy -0.47 to
  +0.60R) next to the unambiguous close-entry results (-0.20R, -0.11R, -0.05R, +0.25R).
- `fig3_short_costs.png` - parabolic short (first red day) net return per trade: +4.0% at zero cost, +2.2% at
  50 bp + 50% borrow, +0.3% at 100 bp + 100%, -3.1% at 100 bp + 300%.

## 6. Reproduction

```
cd /home/user/hongjie-qiu/backtest
python3 -I src/build_panel.py data/hf_defeatbeta data/panel_hf
python3 -I src/build_dolt_panel.py data/hf_dolt data/hf_defeatbeta data/panel_dolt
python3 -I src/test_sim.py
python3 -I src/run_universe.py data/panel_hf 2005-01-03
python3 -I src/run_breakout.py data/panel_hf results
python3 -I src/run_ep.py data/panel_hf results --sec data/ziplime/announcements.parquet --ident data/ziplime/identifiers.parquet --current --nasdaq data/nasdaq_earnings
python3 -I src/run_parabolic.py data/panel_hf results
python3 -I src/run_portfolio.py data/panel_hf results hf 2005-01-03 - data/hf_defeatbeta data/french --sec data/ziplime/announcements.parquet --ident data/ziplime/identifiers.parquet --current
# survivorship check: same scripts on data/panel_dolt with label dolt, 2019-07-01 .. 2026-01-28
python3 -I src/make_charts.py results ../reports/figures
```
Data downloads are described in `/home/user/hongjie-qiu/backtest/data_sources.md`.

---

## Appendix: full variant tables (Panel A, 2005-2026) [D]

Labels are the code's own; Q0 = breakout baseline, C0 = close-confirmed breakout, E- = episodic pivot, P- = parabolic short. 'Avg return' is net of costs, as a fraction of the position.

### Breakout variants (15 bp per fill unless the label says otherwise)

| Variant | Trades | Win rate | Avg R | t | Avg return | Profit factor | Avg hold (days) | 2005-12 | 2013-18 | 2019-21 | 2022-26 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q0 baseline: pivot stop-entry, 1xADR stop, regime on | 1,463 | 44.0% | -0.062 | -1.6 | -0.44% | 0.88 | 5.6 | +0.03 | -0.06 | -0.03 | -0.16 |
| Q0 day0 pessimistic (day low <= stop => out) | 1,464 | 41.7% | -0.111 | -3.0 | -0.82% | 0.79 | 5.3 | -0.02 | -0.12 | -0.09 | -0.19 |
| Q0 day0 optimistic (day-0 low ignored) | 1,463 | 44.0% | -0.067 | -1.8 | -0.48% | 0.87 | 5.7 | +0.03 | -0.07 | -0.03 | -0.16 |
| C0 close-confirmed entry, LOD stop, regime on | 911 | 40.0% | -0.204 | -3.9 | -1.15% | 0.67 | 4.9 | -0.34 | -0.21 | -0.14 | -0.13 |
| Q0 no regime filter | 2,677 | 45.1% | -0.027 | -1.0 | -0.27% | 0.94 | 5.8 | +0.00 | +0.03 | +0.01 | -0.12 |
| Q0 regime = 10>20 only (not 'both rising') | 1,841 | 44.8% | -0.030 | -0.9 | -0.23% | 0.94 | 5.8 | +0.08 | +0.00 | +0.00 | -0.17 |
| C0 no regime filter | 1,697 | 40.4% | -0.146 | -3.8 | -0.80% | 0.76 | 5.1 | -0.26 | -0.07 | -0.08 | -0.15 |
| Q0 top 1% leaders | 788 | 46.2% | -0.052 | -1.0 | -0.34% | 0.89 | 5.8 | +0.04 | +0.00 | -0.07 | -0.16 |
| Q0 top 7% leaders (his TC2000 cut-off) | 3,620 | 42.3% | -0.079 | -3.2 | -0.35% | 0.85 | 5.6 | -0.07 | -0.09 | +0.02 | -0.16 |
| Q0 momentum = point-to-point 1/3/6m return | 1,683 | 43.9% | -0.047 | -1.3 | -0.25% | 0.91 | 5.7 | -0.01 | -0.05 | +0.07 | -0.15 |
| Q0 ADR >= 6% | 956 | 46.2% | -0.022 | -0.5 | -0.28% | 0.95 | 5.7 | +0.10 | +0.07 | +0.01 | -0.13 |
| Q0 dollar volume >= $20M | 627 | 41.6% | -0.062 | -1.0 | -0.16% | 0.88 | 5.5 | -0.12 | -0.18 | +0.04 | -0.04 |
| Q0 consolidation 10-40 days | 546 | 44.0% | +0.010 | +0.1 | -0.03% | 1.02 | 5.9 | +0.15 | +0.17 | +0.05 | -0.26 |
| Q0 depth <= 3 ADR | 1,256 | 44.3% | -0.079 | -2.0 | -0.58% | 0.84 | 5.6 | +0.02 | -0.10 | -0.08 | -0.13 |
| Q0 no tightness filter | 2,169 | 43.8% | -0.039 | -1.1 | -0.10% | 0.92 | 5.6 | -0.06 | -0.02 | +0.01 | -0.08 |
| Q0 + volume dry-up in base | 1,019 | 42.7% | -0.094 | -2.2 | -0.70% | 0.82 | 5.5 | -0.04 | -0.01 | -0.07 | -0.23 |
| Q0 no '1xADR extension' skip | 1,762 | 44.8% | -0.007 | -0.2 | +0.05% | 0.99 | 5.8 | +0.05 | -0.03 | +0.05 | -0.08 |
| Q0 stop 0.5 ADR | 1,470 | 32.7% | -0.029 | -0.4 | -0.11% | 0.96 | 4.1 | +0.11 | +0.03 | -0.03 | -0.19 |
| Q0 stop 1.5 ADR | 1,458 | 46.7% | -0.046 | -1.7 | -0.50% | 0.87 | 6.2 | +0.02 | -0.05 | -0.04 | -0.11 |
| Q0 no partial | 1,446 | 29.3% | -0.091 | -1.9 | -0.72% | 0.85 | 6.6 | +0.02 | -0.13 | -0.05 | -0.19 |
| Q0 partial 1/2 | 1,463 | 45.8% | -0.055 | -1.6 | -0.36% | 0.89 | 5.6 | +0.03 | -0.06 | -0.02 | -0.15 |
| Q0 no breakeven stop | 1,446 | 33.9% | -0.072 | -1.8 | -0.52% | 0.87 | 6.6 | +0.03 | -0.09 | -0.03 | -0.17 |
| Q0 trail SMA20 | 1,440 | 46.0% | -0.060 | -1.4 | -0.51% | 0.89 | 7.4 | +0.11 | -0.07 | -0.05 | -0.19 |
| Q0 cost 0 bp per fill | 1,463 | 48.1% | -0.019 | -0.5 | -0.14% | 0.96 | 5.6 | +0.08 | -0.01 | +0.00 | -0.12 |
| Q0 cost 5 bp per fill | 1,464 | 47.3% | -0.034 | -0.9 | -0.25% | 0.93 | 5.6 | +0.06 | -0.03 | -0.01 | -0.13 |
| Q0 cost 30 bp per fill | 1,464 | 40.5% | -0.103 | -2.7 | -0.72% | 0.81 | 5.6 | -0.02 | -0.10 | -0.07 | -0.19 |
| Q0 cost 50 bp per fill | 1,463 | 34.9% | -0.162 | -4.3 | -1.13% | 0.71 | 5.6 | -0.09 | -0.18 | -0.12 | -0.23 |
| CONTROL random entry in trending leaders (mean of 20 seeds) | 3,677 | 39.0% | -0.051 |  | -0.49% | 0.88 |  |  |  |  |  |

### Episodic-pivot variants (15 bp per fill unless the label says otherwise)

| Variant | Trades | Win rate | Avg R | t | Avg return | Profit factor | Avg hold (days) | 2005-12 | 2013-18 | 2019-21 | 2022-26 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-close: vol>=3x, strong close; buy close, LOD stop | 4,538 | 41.1% | -0.111 | -5.2 | -1.19% | 0.80 | 5.8 | -0.10 | -0.15 | -0.20 | -0.06 |
| E-close, trail SMA20 | 4,531 | 40.8% | -0.093 | -3.9 | -1.15% | 0.83 | 7.6 | -0.10 | -0.13 | -0.16 | -0.05 |
| E-close, trail SMA50, no partial/BE | 4,482 | 23.7% | +0.155 | +2.3 | +0.22% | 1.19 | 18.7 | +0.26 | -0.05 | +0.13 | +0.21 |
| E-close, earnings only | 2,215 | 45.6% | -0.052 | -1.9 | -0.24% | 0.89 | 6.4 | -0.08 | -0.10 | -0.12 | -0.00 |
| E-close, earnings only, trail SMA20 | 2,214 | 45.3% | -0.015 | -0.5 | -0.03% | 0.97 | 8.5 | -0.04 | -0.07 | -0.08 | +0.04 |
| E-close, earnings only, trail SMA50 no partial/BE | 2,198 | 25.3% | +0.250 | +3.2 | +1.22% | 1.33 | 21.3 | +0.39 | +0.14 | +0.19 | +0.27 |
| E-close, non-earnings only | 2,333 | 36.9% | -0.165 | -5.1 | -2.07% | 0.73 | 5.3 | -0.14 | -0.20 | -0.24 | -0.12 |
| E-close, neglected (6m ret -30..+30%) | 2,330 | 42.1% | -0.088 | -3.0 | -0.54% | 0.84 | 6.2 | -0.06 | -0.13 | -0.23 | -0.03 |
| E-close, earnings + neglected, trail SMA20 | 1,312 | 45.2% | -0.014 | -0.3 | +0.00% | 0.97 | 8.8 | -0.15 | -0.01 | -0.13 | +0.06 |
| E-close, gap >= 20% | 1,129 | 41.7% | -0.053 | -1.2 | -1.43% | 0.91 | 5.9 | -0.02 | -0.10 | -0.23 | +0.01 |
| E-close, volume >= 5x | 2,950 | 40.3% | -0.133 | -5.1 | -1.49% | 0.77 | 5.7 | -0.09 | -0.17 | -0.20 | -0.10 |
| E-close, cost 0 | 4,538 | 47.0% | -0.058 | -2.7 | -0.89% | 0.89 | 5.8 | -0.04 | -0.09 | -0.15 | -0.01 |
| E-close, cost 30 bp | 4,538 | 36.6% | -0.165 | -7.8 | -1.49% | 0.72 | 5.8 | -0.16 | -0.21 | -0.24 | -0.12 |
| E-open: buy the open, 1xADR stop, day0 close-based | 17,936 | 36.3% | +0.077 | +4.1 | -0.41% | 1.12 | 4.4 | -0.05 | +0.09 | +0.05 | +0.13 |
| E-open, day0 pessimistic | 18,089 | 30.1% | -0.116 | -8.1 | -1.37% | 0.83 | 3.5 | -0.20 | -0.18 | -0.08 | -0.09 |
| E-open, 1.5xADR stop, day0 pessimistic | 17,842 | 37.5% | -0.089 | -8.2 | -1.53% | 0.84 | 4.7 | -0.15 | -0.12 | -0.07 | -0.07 |
| E-open, earnings only, day0 pessimistic | 6,637 | 31.3% | -0.043 | -1.8 | -0.26% | 0.94 | 3.9 | -0.03 | -0.08 | +0.01 | -0.05 |
| E-orb proxy: buy open+0.25ADR, stop open-0.25ADR, pess. | 13,566 | 12.0% | -0.469 | -21.6 | -1.97% | 0.53 | 1.3 | -0.51 | -0.58 | -0.38 | -0.47 |
| E-orb proxy, day0 close-based | 13,278 | 31.7% | +0.605 | +13.7 | +1.20% | 1.74 | 3.7 | +0.35 | +0.60 | +0.52 | +0.74 |
| E-orb proxy, day0 optimistic | 13,204 | 32.3% | +0.003 | +0.1 | -0.69% | 1.00 | 4.1 | -0.09 | -0.09 | -0.03 | +0.08 |

### Parabolic-short variants (50 bp per fill and 50% a year borrow unless the label says otherwise)

| Variant | Trades | Win rate | Avg R | t | Avg return | Profit factor | Avg hold (days) | 2005-12 | 2013-18 | 2019-21 | 2022-26 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-red: first red close after 5d>=100%, stop=run high | 1,361 | 67.7% | +0.047 | +1.6 | +2.18% | 1.15 | 4.3 | +0.20 | +0.06 | +0.10 | +0.01 |
| P-red, target SMA20, hold<=20d | 1,363 | 63.6% | +0.036 | +1.1 | +3.49% | 1.09 | 8.1 | -0.08 | +0.06 | +0.10 | +0.01 |
| P-red, no target, 5-day time exit | 1,364 | 59.5% | +0.049 | +1.7 | +2.21% | 1.16 | 4.4 | +0.11 | +0.04 | +0.13 | +0.01 |
| P-red, run >= 60% | 3,044 | 62.0% | -0.043 | -2.2 | +0.63% | 0.89 | 4.1 | +0.05 | +0.01 | +0.01 | -0.10 |
| P-red, run >= 200% | 437 | 69.6% | +0.075 | +1.9 | +3.87% | 1.29 | 4.7 | +0.14 | +0.12 | +0.10 | +0.06 |
| P-red, day $vol >= 50M | 979 | 68.6% | +0.024 | +0.8 | +2.66% | 1.08 | 4.5 | +0.14 | +0.17 | +0.09 | -0.04 |
| P-red, cost 0, borrow 0 | 1,362 | 70.6% | +0.140 | +5.4 | +4.03% | 1.54 | 4.4 | +0.31 | +0.13 | +0.16 | +0.12 |
| P-red, cost 100bp/fill, borrow 100%/yr | 1,361 | 65.2% | -0.047 | -1.3 | +0.34% | 0.87 | 4.3 | +0.10 | -0.00 | +0.04 | -0.11 |
| P-red, cost 100bp/fill, borrow 300%/yr | 1,361 | 58.0% | -0.197 | -4.4 | -3.11% | 0.57 | 4.3 | -0.11 | -0.13 | -0.07 | -0.28 |
| P-open: short next open, stop +30%, pessimistic | 1,570 | 60.7% | +0.171 | +6.5 | +5.14% | 1.44 | 4.0 | +0.32 | +0.28 | +0.23 | +0.11 |
| P-open, stop +50% | 1,498 | 67.6% | +0.079 | +4.1 | +3.93% | 1.28 | 4.7 | +0.22 | +0.15 | +0.09 | +0.05 |
| P-open, stop +100% | 1,416 | 73.9% | +0.044 | +3.8 | +4.43% | 1.31 | 5.5 | +0.13 | +0.08 | +0.06 | +0.02 |

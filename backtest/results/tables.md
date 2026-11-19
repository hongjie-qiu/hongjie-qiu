## Generated result tables

Machine-generated from `backtest/results/` by `src/make_tables.py`. Panel A = main snapshot (survivors only), 2005-01-03 to 2026-11-17. Panel B = delisting-inclusive data, 2019-07-01 to 2026-01-28. 'A-window' = Panel A restricted to Panel B's dates. Long trades cost 15 bp per fill, shorts 50 bp per fill plus 50% a year borrow, unless the label says otherwise. t (naive) treats trades as independent.

### T1. The scan universe on its own (20-day forward return minus SPY unless the row says otherwise)

#### Panel A

| Group | 2005-2026 | 2005-2012 | 2013-2018 | 2019-2021 | 2022-2026 |
|---|---|---|---|---|---|
| liquid universe (price>=$3, $vol>=3M) | -0.07% (t=-0.5) | +0.37% (t=+1.8) | -0.13% (t=-0.7) | -0.30% (t=-0.5) | -0.58% (t=-1.7) |
| ... with ADR >= 4% | -0.21% (t=-0.7) | +0.29% (t=+0.6) | -0.20% (t=-0.4) | -0.46% (t=-0.4) | -0.96% (t=-1.5) |
| LEADERS: top 2% on any horizon, ADR >= 4% | -1.13% (t=-2.4) | -0.06% (t=-0.1) | -0.68% (t=-0.9) | -0.93% (t=-0.5) | -3.62% (t=-3.4) |
| top 2% by 1-month gain, ADR >= 4% | -1.75% (t=-3.1) | -0.06% (t=-0.1) | -1.20% (t=-1.4) | -2.21% (t=-1.2) | -5.25% (t=-4.2) |
| top 2% by 3-month gain, ADR >= 4% | -1.49% (t=-2.6) | -0.15% (t=-0.2) | -1.12% (t=-1.3) | -1.17% (t=-0.6) | -4.49% (t=-3.4) |
| top 2% by 6-month gain, ADR >= 4% | -1.32% (t=-2.4) | -0.15% (t=-0.2) | -0.80% (t=-0.9) | -0.69% (t=-0.3) | -4.32% (t=-3.3) |
| top 7% on any horizon, ADR >= 4% | -0.42% (t=-1.1) | +0.24% (t=+0.5) | -0.30% (t=-0.5) | -0.54% (t=-0.4) | -1.69% (t=-2.2) |
| academic 12-2 momentum, top decile | +0.16% (t=+0.5) | +0.29% (t=+0.7) | +0.10% (t=+0.2) | +0.37% (t=+0.3) | -0.14% (t=-0.2) |
| academic 12-2 momentum, bottom decile | -0.33% (t=-0.8) | +0.53% (t=+0.8) | -0.60% (t=-1.2) | -0.24% (t=-0.2) | -1.53% (t=-1.9) |
| leaders 5-day forward | -0.30% (t=-2.0) | -0.03% (t=-0.2) | -0.20% (t=-1.1) | -0.43% (t=-1.0) | -0.78% (t=-1.6) |
| leaders 60-day forward | -1.45% (t=-1.0) | +0.63% (t=+0.4) | -0.76% (t=-0.3) | -0.41% (t=-0.1) | -7.03% (t=-2.2) |

breakout stop-entries (regime on) n=1520: entry->same-day close mean +0.50% median +0.13% up 51% | entry->+1d minus SPY +0.12% (med -0.39%) | entry->+5d minus SPY -0.44% (med -1.19%) | entry->+20d minus SPY -1.33% (med -2.96%) | day-0 low: median -4.2% below entry; <= entry-1ADR on 9% of days, <= entry-0.5ADR on 62%

close-confirmed breakouts (regime on) n=937: close->+1d minus SPY -0.19% (med -0.52%) | close->+5d minus SPY -0.72% (med -1.30%) | close->+20d minus SPY -2.25% (med -2.84%) |

breakout stop-entries (no regime filter) n=2776: entry->same-day close mean +0.40% median +0.12% up 51% | entry->+1d minus SPY +0.53% (med -0.34%) | entry->+5d minus SPY -0.24% (med -0.89%) | entry->+20d minus SPY -1.56% (med -2.91%) | day-0 low: median -4.1% below entry; <= entry-1ADR on 9% of days, <= entry-0.5ADR on 63%

close-confirmed breakouts (no regime filter) n=1745: close->+1d minus SPY +0.15% (med -0.35%) | close->+5d minus SPY -0.09% (med -0.96%) | close->+20d minus SPY -2.45% (med -3.15%) |

avg number of leaders per day: 63 | base universe: 1967

#### Panel B

| Group | 2019-2026 | 2019-2021 | 2022-2026 |
|---|---|---|---|
| liquid universe (price>=$3, $vol>=3M) | -0.43% (t=-1.2) | -0.29% (t=-0.4) | -0.54% (t=-1.5) |
| ... with ADR >= 4% | -0.71% (t=-1.1) | -0.57% (t=-0.4) | -0.83% (t=-1.1) |
| LEADERS: top 2% on any horizon, ADR >= 4% | -2.55% (t=-2.4) | -1.06% (t=-0.5) | -3.43% (t=-3.0) |
| top 2% by 1-month gain, ADR >= 4% | -4.15% (t=-3.5) | -2.35% (t=-1.1) | -5.16% (t=-3.7) |
| top 2% by 3-month gain, ADR >= 4% | -3.44% (t=-2.9) | -1.24% (t=-0.5) | -4.33% (t=-3.0) |
| top 2% by 6-month gain, ADR >= 4% | -2.81% (t=-2.2) | -0.45% (t=-0.2) | -3.83% (t=-2.6) |
| top 7% on any horizon, ADR >= 4% | -1.18% (t=-1.4) | -0.65% (t=-0.4) | -1.45% (t=-1.7) |
| academic 12-2 momentum, top decile | +0.37% (t=+0.5) | +0.33% (t=+0.2) | +0.44% (t=+0.7) |
| academic 12-2 momentum, bottom decile | -0.79% (t=-0.9) | +0.02% (t=+0.0) | -1.28% (t=-1.4) |
| leaders 5-day forward | -0.93% (t=-3.5) | -0.51% (t=-1.0) | -1.15% (t=-3.6) |
| leaders 60-day forward | -4.55% (t=-1.3) | -0.00% (t=-0.0) | -7.46% (t=-2.6) |

breakout stop-entries (regime on) n=746: entry->same-day close mean +0.39% median +0.07% up 50% | entry->+1d minus SPY -0.16% (med -0.80%) | entry->+5d minus SPY -0.88% (med -2.39%) | entry->+20d minus SPY -2.12% (med -5.48%) | day-0 low: median -5.7% below entry; <= entry-1ADR on 8% of days, <= entry-0.5ADR on 64%

close-confirmed breakouts (regime on) n=441: close->+1d minus SPY -0.13% (med -0.72%) | close->+5d minus SPY -0.83% (med -2.45%) | close->+20d minus SPY -2.37% (med -5.80%) |

breakout stop-entries (no regime filter) n=1191: entry->same-day close mean +0.37% median +0.02% up 50% | entry->+1d minus SPY +0.87% (med -0.90%) | entry->+5d minus SPY -0.62% (med -1.87%) | entry->+20d minus SPY -2.48% (med -5.54%) | day-0 low: median -5.3% below entry; <= entry-1ADR on 8% of days, <= entry-0.5ADR on 63%

close-confirmed breakouts (no regime filter) n=724: close->+1d minus SPY +0.40% (med -0.69%) | close->+5d minus SPY -0.16% (med -1.87%) | close->+20d minus SPY -2.18% (med -5.50%) |

avg number of leaders per day: 98 | base universe: 2908

### T2. Breakouts

#### Breakout variants, Panel A

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance | 2005-12 | 2013-18 | 2019-21 | 2022-26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q0 baseline: pivot stop-entry, 1xADR stop, regime on (entry day: close-based = optimistic bound) | 1,478 | 43.8% | -0.070 | -1.9 | -0.51% | 0.86 | 5.6 | 8.6% | +0.02 | -0.07 | -0.04 | -0.17 |
| Q0 day0 worst case (entry-day low <= stop => out) | 1,479 | 41.5% | -0.118 | -3.2 | -0.88% | 0.78 | 5.3 | 8.6% | -0.03 | -0.13 | -0.09 | -0.20 |
| Q0 day0 ignored (entry-day low ignored) | 1,478 | 43.8% | -0.074 | -2.0 | -0.55% | 0.86 | 5.6 | 8.6% | +0.02 | -0.07 | -0.04 | -0.18 |
| C0 close-confirmed entry, LOD stop, regime on | 918 | 39.7% | -0.210 | -4.0 | -1.19% | 0.66 | 4.9 | 7.0% | -0.34 | -0.22 | -0.14 | -0.15 |
| Q0 no regime filter | 2,694 | 45.0% | -0.024 | -0.9 | -0.19% | 0.95 | 5.8 | 8.3% | -0.01 | +0.03 | +0.01 | -0.10 |
| Q0 regime = 10>20 only (not 'both rising') | 1,865 | 44.7% | -0.034 | -1.0 | -0.27% | 0.93 | 5.7 | 8.5% | +0.08 | +0.01 | -0.00 | -0.18 |
| C0 no regime filter | 1,708 | 40.5% | -0.140 | -3.6 | -0.76% | 0.76 | 5.1 | 6.7% | -0.27 | -0.06 | -0.08 | -0.14 |
| Q0 top 1% leaders | 796 | 45.9% | -0.061 | -1.3 | -0.45% | 0.88 | 5.7 | 9.8% | +0.03 | -0.01 | -0.07 | -0.18 |
| Q0 top 7% leaders (his TC2000 cut-off) | 3,666 | 42.3% | -0.082 | -3.4 | -0.38% | 0.84 | 5.5 | 7.1% | -0.07 | -0.09 | +0.03 | -0.17 |
| Q0 momentum = point-to-point 1/3/6m return | 1,702 | 43.9% | -0.052 | -1.5 | -0.29% | 0.90 | 5.7 | 8.2% | -0.02 | -0.05 | +0.07 | -0.16 |
| Q0 ADR >= 6% | 969 | 45.8% | -0.032 | -0.7 | -0.38% | 0.93 | 5.6 | 10.5% | +0.10 | +0.06 | +0.00 | -0.14 |
| Q0 dollar volume >= $20M | 634 | 41.2% | -0.074 | -1.2 | -0.26% | 0.86 | 5.5 | 8.7% | -0.13 | -0.18 | +0.04 | -0.06 |
| Q0 consolidation 10-40 days | 548 | 43.8% | +0.006 | +0.1 | -0.08% | 1.01 | 5.8 | 9.2% | +0.15 | +0.17 | +0.05 | -0.28 |
| Q0 depth <= 3 ADR | 1,271 | 44.0% | -0.087 | -2.2 | -0.66% | 0.83 | 5.6 | 8.8% | +0.01 | -0.11 | -0.08 | -0.14 |
| Q0 no tightness filter | 2,196 | 43.6% | -0.047 | -1.4 | -0.17% | 0.91 | 5.6 | 8.5% | -0.06 | -0.03 | +0.01 | -0.10 |
| Q0 + volume dry-up in base | 1,033 | 42.5% | -0.101 | -2.4 | -0.76% | 0.80 | 5.5 | 8.3% | -0.04 | -0.02 | -0.07 | -0.24 |
| Q0 no '1xADR extension' skip | 1,780 | 44.3% | -0.025 | -0.7 | -0.09% | 0.95 | 5.7 | 8.6% | +0.05 | -0.05 | +0.02 | -0.10 |
| Q0 stop 0.5 ADR | 1,485 | 32.3% | -0.045 | -0.7 | -0.16% | 0.94 | 4.0 | 4.3% | +0.09 | +0.02 | -0.03 | -0.21 |
| Q0 stop 1.5 ADR | 1,472 | 46.6% | -0.051 | -1.9 | -0.55% | 0.86 | 6.2 | 12.8% | +0.02 | -0.05 | -0.04 | -0.11 |
| Q0 no partial | 1,461 | 29.2% | -0.098 | -2.1 | -0.77% | 0.84 | 6.6 | 8.6% | +0.02 | -0.13 | -0.05 | -0.20 |
| Q0 partial 1/2 | 1,478 | 45.5% | -0.063 | -1.8 | -0.43% | 0.88 | 5.6 | 8.6% | +0.03 | -0.06 | -0.03 | -0.16 |
| Q0 no breakeven stop | 1,461 | 33.7% | -0.079 | -2.0 | -0.57% | 0.86 | 6.6 | 8.6% | +0.03 | -0.10 | -0.03 | -0.18 |
| Q0 trail SMA20 | 1,455 | 45.6% | -0.069 | -1.6 | -0.59% | 0.87 | 7.3 | 8.6% | +0.11 | -0.09 | -0.05 | -0.20 |
| Q0 cost 0 bp per fill | 1,478 | 47.8% | -0.027 | -0.7 | -0.21% | 0.94 | 5.6 | 8.6% | +0.08 | -0.02 | +0.00 | -0.14 |
| Q0 cost 5 bp per fill | 1,479 | 47.1% | -0.042 | -1.1 | -0.32% | 0.92 | 5.6 | 8.6% | +0.06 | -0.03 | -0.01 | -0.15 |
| Q0 cost 30 bp per fill | 1,479 | 40.2% | -0.110 | -2.9 | -0.80% | 0.79 | 5.6 | 8.6% | -0.03 | -0.11 | -0.07 | -0.20 |
| Q0 cost 50 bp per fill | 1,478 | 34.6% | -0.169 | -4.5 | -1.20% | 0.70 | 5.6 | 8.6% | -0.10 | -0.18 | -0.12 | -0.25 |
| CONTROL random entry in trending leaders (mean of 20 seeds) | 3,723 | 38.3% | -0.070 |  | -0.67% | 0.84 |  |  |  |  |  |  |

Control - random entry at the open in trending leaders, regime on, same exits (20 seeds; fills at the open are exact):

n per run ~3723 | avgR mean -0.070 (min -0.132, max +0.010) | win 38.3% | avgRet -0.67%

Q0 profit concentration: sum R = -102.8 | top 10 trades = 86.7 | top 1% (14 trades) = 109.6 | all others = -212.5

exit reasons (0 stop, 1 trail, 2 time, 3 data end, 4 day-0 stop): {0: 939, 1: 506, 4: 33}

regime-on share of days: strict 0.47, loose 0.63

#### Q0 baseline by year, Panel A

| Year | Trades | Win rate | Avg R | Sum R | Avg return |
|---|---|---|---|---|---|
| 2005 | 21 | 57% | +0.12 | +2.6 | +0.66% |
| 2006 | 35 | 40% | +0.03 | +1.2 | +0.63% |
| 2007 | 55 | 45% | -0.06 | -3.2 | -0.55% |
| 2008 | 33 | 45% | -0.12 | -3.9 | -0.65% |
| 2009 | 57 | 53% | -0.03 | -1.8 | +0.60% |
| 2010 | 57 | 51% | +0.40 | +22.8 | +2.39% |
| 2011 | 27 | 30% | -0.39 | -10.5 | -2.25% |
| 2012 | 54 | 43% | +0.02 | +1.0 | -1.05% |
| 2013 | 71 | 55% | +0.24 | +17.2 | +1.43% |
| 2014 | 53 | 42% | -0.20 | -10.6 | -0.73% |
| 2015 | 37 | 32% | -0.24 | -8.7 | -0.44% |
| 2016 | 72 | 54% | +0.14 | +10.1 | +0.91% |
| 2017 | 69 | 35% | -0.33 | -22.9 | -1.97% |
| 2018 | 62 | 42% | -0.15 | -9.4 | -0.51% |
| 2019 | 103 | 50% | -0.08 | -8.3 | -0.76% |
| 2020 | 127 | 50% | +0.13 | +17.0 | +1.57% |
| 2021 | 106 | 34% | -0.20 | -20.8 | -1.60% |
| 2022 | 61 | 31% | -0.38 | -23.5 | -3.37% |
| 2023 | 105 | 40% | -0.18 | -18.9 | -1.59% |
| 2024 | 133 | 41% | -0.20 | -26.4 | -2.57% |
| 2025 | 96 | 51% | +0.12 | +11.2 | +1.72% |
| 2026 | 44 | 30% | -0.39 | -17.1 | -3.02% |

#### Q0 without the regime filter by year, Panel A

| Year | Trades | Win rate | Avg R | Sum R | Avg return |
|---|---|---|---|---|---|
| 2005 | 63 | 38% | -0.28 | -17.7 | -1.94% |
| 2006 | 80 | 40% | -0.12 | -9.3 | -0.53% |
| 2007 | 89 | 43% | -0.09 | -8.4 | -0.70% |
| 2008 | 81 | 49% | -0.13 | -10.8 | -0.95% |
| 2009 | 109 | 60% | +0.14 | +15.6 | +1.20% |
| 2010 | 89 | 53% | +0.41 | +36.6 | +2.35% |
| 2011 | 64 | 39% | -0.14 | -8.7 | -0.73% |
| 2012 | 87 | 44% | -0.03 | -2.8 | -1.17% |
| 2013 | 116 | 56% | +0.20 | +23.6 | +1.14% |
| 2014 | 85 | 46% | -0.15 | -12.7 | -0.59% |
| 2015 | 120 | 42% | -0.14 | -16.9 | -0.53% |
| 2016 | 121 | 58% | +0.30 | +36.6 | +1.68% |
| 2017 | 106 | 42% | -0.09 | -9.9 | -0.41% |
| 2018 | 139 | 42% | +0.02 | +2.6 | +0.80% |
| 2019 | 150 | 52% | +0.04 | +5.4 | +0.19% |
| 2020 | 164 | 49% | +0.14 | +23.3 | +1.22% |
| 2021 | 161 | 39% | -0.15 | -24.1 | -1.23% |
| 2022 | 180 | 38% | -0.25 | -45.6 | -2.18% |
| 2023 | 163 | 40% | -0.07 | -11.2 | +0.25% |
| 2024 | 195 | 42% | -0.12 | -23.7 | -1.61% |
| 2025 | 165 | 48% | +0.05 | +7.9 | +0.59% |
| 2026 | 167 | 37% | -0.08 | -13.6 | -0.89% |

#### Breakout variants, Panel B

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance |
|---|---|---|---|---|---|---|---|---|
| Q0 baseline: pivot stop-entry, 1xADR stop, regime on (entry day: close-based = optimistic bound) | 735 | 43.0% | -0.054 | -0.9 | -0.31% | 0.90 | 5.5 | 10.8% |
| Q0 day0 worst case (entry-day low <= stop => out) | 735 | 41.0% | -0.093 | -1.6 | -0.63% | 0.83 | 5.2 | 10.8% |
| Q0 day0 ignored (entry-day low ignored) | 735 | 43.0% | -0.060 | -1.0 | -0.38% | 0.89 | 5.5 | 10.8% |
| C0 close-confirmed entry, LOD stop, regime on | 436 | 40.8% | -0.121 | -1.5 | -0.82% | 0.80 | 5.0 | 8.7% |
| Q0 no regime filter | 1,174 | 43.1% | -0.046 | -1.0 | -0.26% | 0.91 | 5.5 | 10.5% |
| Q0 regime = 10>20 only (not 'both rising') | 872 | 42.9% | -0.073 | -1.4 | -0.46% | 0.86 | 5.4 | 10.7% |
| C0 no regime filter | 714 | 41.0% | -0.123 | -2.0 | -0.64% | 0.80 | 5.0 | 8.3% |
| Q0 top 1% leaders | 392 | 43.4% | -0.098 | -1.3 | -0.62% | 0.81 | 5.5 | 12.7% |
| Q0 top 7% leaders (his TC2000 cut-off) | 2,140 | 42.7% | -0.064 | -2.0 | -0.24% | 0.88 | 5.6 | 8.0% |
| Q0 momentum = point-to-point 1/3/6m return | 869 | 43.3% | -0.033 | -0.6 | -0.12% | 0.94 | 5.7 | 10.0% |
| Q0 ADR >= 6% | 631 | 43.6% | -0.031 | -0.5 | -0.20% | 0.94 | 5.5 | 11.7% |
| Q0 dollar volume >= $20M | 338 | 45.9% | +0.035 | +0.4 | +0.77% | 1.07 | 5.7 | 10.9% |
| Q0 consolidation 10-40 days | 287 | 39.4% | -0.090 | -0.9 | -0.79% | 0.84 | 5.3 | 11.5% |
| Q0 depth <= 3 ADR | 650 | 42.8% | -0.075 | -1.2 | -0.61% | 0.86 | 5.5 | 11.1% |
| Q0 no tightness filter | 1,128 | 44.1% | -0.005 | -0.1 | +0.27% | 0.99 | 5.5 | 10.4% |
| Q0 + volume dry-up in base | 516 | 40.5% | -0.131 | -2.0 | -1.14% | 0.76 | 5.2 | 10.6% |
| Q0 no '1xADR extension' skip | 881 | 43.8% | -0.012 | -0.2 | +0.09% | 0.98 | 5.6 | 10.9% |
| Q0 stop 0.5 ADR | 740 | 31.5% | -0.018 | -0.2 | +0.04% | 0.98 | 3.9 | 5.4% |
| Q0 stop 1.5 ADR | 730 | 45.6% | -0.051 | -1.2 | -0.54% | 0.86 | 6.0 | 16.0% |
| Q0 no partial | 730 | 28.2% | -0.058 | -0.7 | -0.31% | 0.91 | 6.3 | 10.8% |
| Q0 partial 1/2 | 735 | 43.5% | -0.057 | -1.1 | -0.33% | 0.89 | 5.5 | 10.8% |
| Q0 no breakeven stop | 730 | 32.2% | -0.059 | -1.0 | -0.33% | 0.90 | 6.3 | 10.8% |
| Q0 trail SMA20 | 716 | 45.1% | -0.058 | -0.9 | -0.42% | 0.89 | 7.4 | 10.8% |
| Q0 cost 0 bp per fill | 735 | 44.6% | -0.020 | -0.3 | -0.01% | 0.96 | 5.5 | 10.8% |
| Q0 cost 5 bp per fill | 735 | 44.2% | -0.031 | -0.5 | -0.11% | 0.94 | 5.5 | 10.8% |
| Q0 cost 30 bp per fill | 735 | 40.1% | -0.088 | -1.5 | -0.61% | 0.84 | 5.5 | 10.8% |
| Q0 cost 50 bp per fill | 735 | 35.2% | -0.133 | -2.2 | -1.01% | 0.77 | 5.5 | 10.8% |
| CONTROL random entry in trending leaders (mean of 20 seeds) | 1,202 | 38.7% | -0.046 |  | -0.60% | 0.89 |  |  |

n per run ~1202 | avgR mean -0.046 (min -0.100, max +0.063) | win 38.7% | avgRet -0.60%

Q0 profit concentration: sum R = -39.7 | top 10 trades = 88.9 | top 1% (7 trades) = 70.9 | all others = -110.5

#### Breakout variants, A-window

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance |
|---|---|---|---|---|---|---|---|---|
| Q0 baseline: pivot stop-entry, 1xADR stop, regime on (entry day: close-based = optimistic bound) | 677 | 42.2% | -0.092 | -1.6 | -0.81% | 0.83 | 5.3 | 10.7% |
| Q0 day0 worst case (entry-day low <= stop => out) | 677 | 40.2% | -0.131 | -2.3 | -1.15% | 0.76 | 5.1 | 10.7% |
| Q0 day0 ignored (entry-day low ignored) | 677 | 42.2% | -0.098 | -1.7 | -0.89% | 0.82 | 5.3 | 10.7% |
| C0 close-confirmed entry, LOD stop, regime on | 399 | 41.1% | -0.115 | -1.3 | -0.90% | 0.81 | 4.9 | 8.7% |
| Q0 no regime filter | 1,118 | 43.2% | -0.048 | -1.0 | -0.39% | 0.90 | 5.5 | 10.3% |
| Q0 regime = 10>20 only (not 'both rising') | 823 | 42.0% | -0.088 | -1.7 | -0.76% | 0.83 | 5.4 | 10.6% |
| C0 no regime filter | 676 | 39.9% | -0.134 | -2.1 | -0.77% | 0.78 | 4.9 | 8.3% |
| Q0 top 1% leaders | 356 | 43.5% | -0.121 | -1.7 | -1.05% | 0.76 | 5.4 | 12.7% |
| Q0 top 7% leaders (his TC2000 cut-off) | 1,978 | 41.5% | -0.073 | -2.1 | -0.32% | 0.86 | 5.5 | 7.9% |
| Q0 momentum = point-to-point 1/3/6m return | 836 | 42.8% | -0.045 | -0.8 | -0.34% | 0.91 | 5.6 | 9.8% |
| Q0 ADR >= 6% | 589 | 43.0% | -0.071 | -1.1 | -0.76% | 0.86 | 5.3 | 11.5% |
| Q0 dollar volume >= $20M | 315 | 43.5% | +0.001 | +0.0 | +0.46% | 1.00 | 5.5 | 11.0% |
| Q0 consolidation 10-40 days | 269 | 37.2% | -0.123 | -1.3 | -1.24% | 0.79 | 5.2 | 11.4% |
| Q0 depth <= 3 ADR | 598 | 42.3% | -0.102 | -1.7 | -1.00% | 0.80 | 5.3 | 11.0% |
| Q0 no tightness filter | 1,026 | 43.2% | -0.023 | -0.4 | +0.04% | 0.96 | 5.4 | 10.4% |
| Q0 + volume dry-up in base | 466 | 40.6% | -0.157 | -2.6 | -1.54% | 0.71 | 5.1 | 10.4% |
| Q0 no '1xADR extension' skip | 811 | 43.3% | -0.023 | -0.4 | -0.17% | 0.96 | 5.4 | 10.8% |
| Q0 stop 0.5 ADR | 681 | 30.4% | -0.095 | -0.9 | -0.43% | 0.88 | 3.7 | 5.4% |
| Q0 stop 1.5 ADR | 671 | 45.3% | -0.063 | -1.5 | -0.76% | 0.83 | 5.9 | 15.9% |
| Q0 no partial | 670 | 27.6% | -0.107 | -1.4 | -0.97% | 0.83 | 6.2 | 10.7% |
| Q0 partial 1/2 | 677 | 43.4% | -0.088 | -1.7 | -0.79% | 0.83 | 5.3 | 10.7% |
| Q0 no breakeven stop | 670 | 31.5% | -0.097 | -1.6 | -0.88% | 0.83 | 6.2 | 10.7% |
| Q0 trail SMA20 | 661 | 44.3% | -0.115 | -1.8 | -1.07% | 0.79 | 7.1 | 10.7% |
| Q0 cost 0 bp per fill | 677 | 44.3% | -0.058 | -1.0 | -0.52% | 0.89 | 5.3 | 10.7% |
| Q0 cost 5 bp per fill | 678 | 44.0% | -0.070 | -1.2 | -0.64% | 0.86 | 5.3 | 10.7% |
| Q0 cost 30 bp per fill | 677 | 39.1% | -0.125 | -2.1 | -1.11% | 0.77 | 5.3 | 10.7% |
| Q0 cost 50 bp per fill | 677 | 34.4% | -0.170 | -2.9 | -1.51% | 0.70 | 5.3 | 10.7% |
| CONTROL random entry in trending leaders (mean of 20 seeds) | 867 | 39.3% | -0.005 |  | -0.36% | 0.99 |  |  |

n per run ~867 | avgR mean -0.005 (min -0.090, max +0.224) | win 39.3% | avgRet -0.36%

### T3. Episodic pivots

#### Event study, Panel A: return after the gap-day close, minus SPY

| Subset | Events | Gap-day open->close | +1 day | +5 days | +20 days | +60 days |
|---|---|---|---|---|---|---|
| all gaps >= 10% | 19,402 | -0.89% | -0.18% (median -0.42%, t ~ -2.9) | -1.48% (median -1.51%, t ~ -5.4) | -3.06% (median -3.08%, t ~ -5.9) | -2.52% (median -6.24%, t ~ -1.7) |
| volume >= 3x and day $vol >= 10M | 11,531 | +0.65% | -0.28% (median -0.41%, t ~ -3.0) | -1.82% (median -1.37%, t ~ -6.5) | -3.80% (median -2.82%, t ~ -5.6) | -4.41% (median -6.46%, t ~ -2.0) |
| ... and close >= open, top half of range | 4,658 | +10.52% | +0.01% (median -0.30%, t ~ -0.1) | -1.40% (median -1.01%, t ~ -4.7) | -2.22% (median -1.56%, t ~ -3.1) | -2.35% (median -4.48%, t ~ -0.6) |
| ... and close < open (faded) | 5,660 | -8.34% | -0.50% (median -0.57%, t ~ -2.7) | -2.06% (median -1.71%, t ~ -4.9) | -4.62% (median -3.89%, t ~ -4.9) | -5.60% (median -7.85%, t ~ -1.9) |
| earnings reaction day | 4,737 | +1.28% | +0.11% (median +0.05%, t ~ +0.6) | -0.19% (median -0.37%, t ~ -0.2) | +0.38% (median -0.06%, t ~ +0.6) | +0.68% (median -1.15%, t ~ +0.6) |
| not an earnings day | 6,794 | +0.21% | -0.55% (median -0.89%, t ~ -3.6) | -2.95% (median -2.69%, t ~ -7.7) | -6.68% (median -6.32%, t ~ -6.7) | -8.00% (median -12.37%, t ~ -2.2) |
| earnings + close>=open, top half of range | 2,217 | +7.36% | +0.07% (median +0.05%, t ~ -0.7) | -0.26% (median -0.39%, t ~ -1.3) | +0.48% (median -0.11%, t ~ +0.2) | +0.71% (median -1.14%, t ~ +0.4) |
| earnings + EPS surprise >= +20% | 2,178 | +1.67% | +0.12% (median +0.04%, t ~ +0.4) | -0.12% (median -0.33%, t ~ -0.1) | +0.61% (median +0.33%, t ~ +0.6) | +0.49% (median -0.99%, t ~ +0.2) |
| earnings + EPS surprise <= 0 | 394 | +0.80% | -0.02% (median -0.32%, t ~ -0.2) | -0.21% (median -0.57%, t ~ -0.3) | +1.01% (median -0.67%, t ~ +0.5) | -0.55% (median -3.53%, t ~ +0.0) |
| gap 10-20% | 8,070 | +1.34% | -0.01% (median -0.24%, t ~ -1.0) | -1.00% (median -0.93%, t ~ -4.3) | -2.03% (median -1.94%, t ~ -3.8) | -1.98% (median -4.52%, t ~ -1.1) |
| gap 20-40% | 2,615 | -0.17% | -0.42% (median -0.71%, t ~ -2.1) | -2.79% (median -2.39%, t ~ -7.2) | -5.50% (median -4.55%, t ~ -4.1) | -8.05% (median -10.58%, t ~ -2.3) |
| gap 40-inf% | 846 | -3.44% | -2.44% (median -2.72%, t ~ -1.9) | -6.65% (median -7.23%, t ~ -4.1) | -15.36% (median -14.24%, t ~ -5.4) | -17.18% (median -25.19%, t ~ -1.3) |
| 'neglected': prior 6m return in [-30%, +30%] | 5,470 | +0.71% | +0.00% (median -0.19%, t ~ -0.2) | -0.46% (median -0.47%, t ~ -2.2) | -1.29% (median -1.24%, t ~ -2.7) | -1.94% (median -3.12%, t ~ -1.0) |
| extended: prior 6m return > +50% | 2,640 | +0.14% | -0.67% (median -0.88%, t ~ -2.2) | -3.48% (median -3.97%, t ~ -5.7) | -6.81% (median -7.79%, t ~ -4.3) | -8.11% (median -15.97%, t ~ -1.3) |
| beaten down: prior 6m return < -30% | 2,068 | +1.21% | -0.37% (median -1.24%, t ~ -1.0) | -3.42% (median -3.28%, t ~ -5.8) | -6.69% (median -6.03%, t ~ -4.3) | -5.18% (median -8.34%, t ~ -1.8) |
| volume >= 10x | 2,881 | +2.81% | -1.38% (median -1.16%, t ~ -3.7) | -4.33% (median -3.52%, t ~ -7.9) | -8.08% (median -6.56%, t ~ -5.4) | -12.46% (median -14.21%, t ~ -3.4) |
| 2005-2012 | 1,501 | +0.73% | +0.04% (median -0.12%, t ~ +0.4) | +0.09% (median -0.02%, t ~ +0.5) | +0.49% (median +0.37%, t ~ +0.4) | +1.25% (median +0.15%, t ~ +0.6) |
| earnings only 2005-2012 | 770 | +1.11% | +0.50% (median +0.22%, t ~ +3.2) | +0.53% (median +0.41%, t ~ +2.1) | +1.28% (median +0.81%, t ~ +1.3) | +2.58% (median +2.21%, t ~ +1.0) |
| 2013-2018 | 2,003 | +0.10% | -0.35% (median -0.18%, t ~ -2.1) | -1.09% (median -0.56%, t ~ -2.7) | -2.16% (median -1.12%, t ~ -2.7) | -2.98% (median -2.41%, t ~ -1.4) |
| earnings only 2013-2018 | 962 | +0.84% | +0.18% (median +0.16%, t ~ +0.7) | +0.25% (median -0.09%, t ~ +0.6) | +1.00% (median +0.50%, t ~ +0.9) | +2.28% (median +1.04%, t ~ +0.9) |
| 2019-2021 | 2,751 | -0.02% | -0.41% (median -0.96%, t ~ -2.2) | -2.36% (median -3.05%, t ~ -3.6) | -4.14% (median -5.90%, t ~ -2.3) | -2.15% (median -10.79%, t ~ -0.5) |
| earnings only 2019-2021 | 738 | +1.62% | -0.07% (median +0.02%, t ~ -0.5) | -0.26% (median -1.14%, t ~ +0.5) | -0.59% (median -1.07%, t ~ +0.1) | -0.27% (median -3.51%, t ~ +0.2) |
| 2022-2026 | 5,276 | +1.18% | -0.27% (median -0.49%, t ~ -1.6) | -2.35% (median -1.64%, t ~ -5.6) | -5.50% (median -4.09%, t ~ -5.7) | -7.98% (median -9.28%, t ~ -2.3) |
| earnings only 2022-2026 | 2,267 | +1.41% | -0.00% (median -0.19%, t ~ -0.7) | -0.61% (median -0.77%, t ~ -2.6) | +0.11% (median -0.61%, t ~ -0.7) | -0.40% (median -3.20%, t ~ -0.5) |

#### EP trade variants, Panel A

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance | 2005-12 | 2013-18 | 2019-21 | 2022-26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-close: vol>=3x, strong close; buy close, LOD stop | 4,538 | 41.1% | -0.111 | -5.2 | -1.19% | 0.80 | 5.8 | 8.2% | -0.10 | -0.15 | -0.20 | -0.06 |
| E-close, trail SMA20 | 4,531 | 40.8% | -0.093 | -3.9 | -1.15% | 0.83 | 7.6 | 8.2% | -0.10 | -0.13 | -0.16 | -0.05 |
| E-close, trail SMA50, no partial/BE | 4,482 | 23.6% | +0.153 | +2.3 | +0.19% | 1.19 | 18.7 | 8.2% | +0.26 | -0.05 | +0.13 | +0.21 |
| E-close, earnings only | 2,215 | 45.6% | -0.052 | -1.9 | -0.24% | 0.89 | 6.4 | 6.2% | -0.08 | -0.10 | -0.12 | -0.00 |
| E-close, earnings only, trail SMA20 | 2,214 | 45.3% | -0.015 | -0.5 | -0.03% | 0.97 | 8.5 | 6.2% | -0.04 | -0.07 | -0.08 | +0.04 |
| E-close, earnings only, trail SMA50 no partial/BE | 2,198 | 25.3% | +0.248 | +3.1 | +1.21% | 1.33 | 21.3 | 6.2% | +0.39 | +0.14 | +0.19 | +0.26 |
| E-close, non-earnings only | 2,333 | 36.9% | -0.165 | -5.1 | -2.07% | 0.73 | 5.3 | 10.1% | -0.14 | -0.20 | -0.24 | -0.12 |
| E-close, neglected (6m ret -30..+30%) | 2,330 | 42.1% | -0.088 | -3.0 | -0.54% | 0.84 | 6.2 | 6.2% | -0.06 | -0.13 | -0.23 | -0.03 |
| E-close, earnings + neglected, trail SMA20 | 1,312 | 45.2% | -0.014 | -0.3 | +0.00% | 0.97 | 8.8 | 5.4% | -0.15 | -0.01 | -0.13 | +0.06 |
| E-close, gap >= 20% | 1,129 | 41.7% | -0.053 | -1.2 | -1.43% | 0.91 | 5.9 | 10.8% | -0.02 | -0.10 | -0.23 | +0.01 |
| E-close, volume >= 5x | 2,950 | 40.3% | -0.133 | -5.1 | -1.49% | 0.77 | 5.7 | 8.7% | -0.09 | -0.17 | -0.20 | -0.10 |
| E-close, cost 0 | 4,538 | 47.0% | -0.058 | -2.7 | -0.89% | 0.89 | 5.8 | 8.2% | -0.04 | -0.09 | -0.15 | -0.01 |
| E-close, cost 30 bp | 4,538 | 36.6% | -0.165 | -7.8 | -1.49% | 0.72 | 5.8 | 8.2% | -0.16 | -0.21 | -0.24 | -0.12 |
| E-open: buy the open, 1xADR stop (exact) | 18,099 | 30.0% | -0.117 | -8.2 | -1.38% | 0.83 | 3.5 | 8.6% | -0.20 | -0.18 | -0.08 | -0.09 |
| E-open, 1.5xADR stop (exact) | 17,862 | 37.5% | -0.091 | -8.4 | -1.53% | 0.83 | 4.7 | 12.4% | -0.15 | -0.12 | -0.07 | -0.07 |
| E-open, earnings only (exact) | 6,637 | 31.3% | -0.043 | -1.8 | -0.26% | 0.94 | 3.9 | 4.9% | -0.03 | -0.08 | +0.01 | -0.05 |
| E-orb proxy: buy open+0.25ADR, stop open-0.25ADR, worst case | 13,573 | 12.0% | -0.470 | -21.7 | -1.98% | 0.52 | 1.3 | 4.0% | -0.51 | -0.58 | -0.38 | -0.47 |
| E-orb proxy, close-based (optimistic bound) | 13,283 | 31.6% | +0.604 | +13.7 | +1.19% | 1.74 | 3.7 | 3.9% | +0.35 | +0.60 | +0.52 | +0.74 |
| E-orb proxy, entry-day low ignored | 13,208 | 32.3% | +0.003 | +0.1 | -0.69% | 1.00 | 4.1 | 3.9% | -0.09 | -0.09 | -0.03 | +0.08 |

E-close profit concentration: sum R = -504.8 | top 10 = 107.1 | top 1% (45) = 327.1 | others = -831.9

#### EP bought at the close, standard rules, by year, Panel A

| Year | Trades | Win rate | Avg R | Sum R | Avg return |
|---|---|---|---|---|---|
| 2005 | 61 | 46% | -0.12 | -7.0 | -0.90% |
| 2006 | 76 | 46% | +0.20 | +15.3 | +0.58% |
| 2007 | 77 | 40% | -0.05 | -3.8 | -0.56% |
| 2008 | 99 | 37% | -0.40 | -39.2 | -3.21% |
| 2009 | 101 | 40% | -0.11 | -10.8 | -2.03% |
| 2010 | 53 | 40% | -0.17 | -9.1 | -1.11% |
| 2011 | 92 | 41% | -0.16 | -14.7 | -1.19% |
| 2012 | 85 | 49% | +0.04 | +3.4 | +0.27% |
| 2013 | 89 | 34% | -0.32 | -28.3 | -1.88% |
| 2014 | 112 | 42% | -0.24 | -26.5 | -1.43% |
| 2015 | 133 | 41% | -0.17 | -22.4 | -0.86% |
| 2016 | 117 | 47% | -0.02 | -1.8 | -0.20% |
| 2017 | 158 | 46% | +0.01 | +2.0 | -0.25% |
| 2018 | 185 | 38% | -0.21 | -39.3 | -1.41% |
| 2019 | 199 | 41% | -0.12 | -24.7 | -0.17% |
| 2020 | 408 | 36% | -0.24 | -96.8 | -2.41% |
| 2021 | 326 | 35% | -0.19 | -62.6 | -2.63% |
| 2022 | 295 | 48% | -0.12 | -34.1 | -1.36% |
| 2023 | 303 | 51% | +0.13 | +37.9 | -0.30% |
| 2024 | 477 | 44% | +0.07 | +32.9 | +0.31% |
| 2025 | 607 | 39% | -0.13 | -78.7 | -1.66% |
| 2026 | 485 | 37% | -0.20 | -96.3 | -1.39% |

#### Earnings EP, 20-day trail, by year, Panel A

| Year | Trades | Win rate | Avg R | Sum R | Avg return |
|---|---|---|---|---|---|
| 2005 | 38 | 58% | +0.48 | +18.1 | +2.51% |
| 2006 | 43 | 40% | -0.18 | -7.8 | -0.44% |
| 2007 | 52 | 44% | -0.00 | -0.1 | -0.39% |
| 2008 | 50 | 40% | -0.31 | -15.3 | -1.85% |
| 2009 | 47 | 47% | -0.12 | -5.6 | -0.59% |
| 2010 | 26 | 46% | -0.03 | -0.8 | +0.03% |
| 2011 | 53 | 49% | -0.15 | -8.1 | -0.95% |
| 2012 | 52 | 56% | +0.10 | +5.1 | +0.84% |
| 2013 | 42 | 36% | -0.17 | -7.2 | -1.11% |
| 2014 | 52 | 42% | -0.17 | -8.9 | -0.87% |
| 2015 | 72 | 40% | -0.33 | -23.8 | -1.89% |
| 2016 | 66 | 53% | +0.12 | +7.8 | +0.90% |
| 2017 | 90 | 50% | +0.09 | +7.9 | +1.15% |
| 2018 | 116 | 40% | -0.07 | -7.6 | -0.52% |
| 2019 | 127 | 40% | -0.16 | -20.4 | -0.35% |
| 2020 | 102 | 37% | -0.04 | -3.7 | -0.77% |
| 2021 | 105 | 49% | -0.03 | -3.1 | -0.17% |
| 2022 | 140 | 46% | -0.14 | -19.4 | -1.14% |
| 2023 | 169 | 55% | +0.30 | +51.2 | +1.05% |
| 2024 | 256 | 48% | +0.10 | +26.7 | +0.70% |
| 2025 | 278 | 45% | +0.08 | +22.0 | +0.83% |
| 2026 | 238 | 40% | -0.17 | -40.8 | -0.69% |

#### Event study, Panel B

| Subset | Events | Gap-day open->close | +1 day | +5 days | +20 days | +60 days |
|---|---|---|---|---|---|---|
| all gaps >= 10% | 12,646 | -0.91% | -0.24% (median -0.47%, t ~ -3.8) | -1.39% (median -1.79%, t ~ -3.3) | -2.81% (median -3.70%, t ~ -5.2) | -2.13% (median -7.32%, t ~ -2.3) |
| volume >= 3x and day $vol >= 10M | 7,594 | +0.42% | -0.43% (median -0.53%, t ~ -3.1) | -1.86% (median -1.69%, t ~ -4.7) | -3.67% (median -3.67%, t ~ -4.6) | -3.93% (median -8.29%, t ~ -1.4) |
| ... and close >= open, top half of range | 3,005 | +10.79% | -0.09% (median -0.40%, t ~ +0.1) | -1.49% (median -1.23%, t ~ -3.7) | -1.88% (median -2.28%, t ~ -2.3) | -1.28% (median -5.89%, t ~ -0.3) |
| ... and close < open (faded) | 3,766 | -8.90% | -0.78% (median -0.72%, t ~ -3.2) | -2.34% (median -2.25%, t ~ -3.6) | -4.73% (median -5.12%, t ~ -3.7) | -5.37% (median -10.34%, t ~ -1.3) |
| earnings reaction day | 2,640 | +1.46% | +0.01% (median -0.13%, t ~ -0.3) | -0.24% (median -0.66%, t ~ +0.6) | +0.06% (median -0.74%, t ~ +0.1) | -0.08% (median -3.29%, t ~ -0.1) |
| not an earnings day | 4,954 | -0.14% | -0.67% (median -0.82%, t ~ -3.2) | -2.73% (median -2.69%, t ~ -5.7) | -5.72% (median -6.03%, t ~ -5.1) | -6.09% (median -12.69%, t ~ -1.2) |
| earnings + close>=open, top half of range | 1,227 | +8.19% | +0.04% (median +0.01%, t ~ -0.8) | -0.44% (median -0.82%, t ~ -0.8) | +0.06% (median -0.86%, t ~ -0.4) | -0.35% (median -3.55%, t ~ -0.5) |
| gap 10-20% | 4,939 | +1.34% | +0.09% (median -0.37%, t ~ -0.0) | -0.94% (median -1.42%, t ~ -2.6) | -2.03% (median -3.19%, t ~ -3.0) | -1.21% (median -6.41%, t ~ -0.7) |
| gap 20-40% | 1,932 | -0.14% | -0.88% (median -0.70%, t ~ -2.7) | -3.04% (median -2.06%, t ~ -5.9) | -4.79% (median -3.97%, t ~ -2.9) | -6.87% (median -10.05%, t ~ -1.4) |
| gap 40-inf% | 723 | -4.35% | -2.86% (median -1.35%, t ~ -3.3) | -4.97% (median -3.57%, t ~ -2.5) | -11.96% (median -7.64%, t ~ -4.1) | -16.30% (median -23.81%, t ~ -0.9) |
| 'neglected': prior 6m return in [-30%, +30%] | 3,250 | +0.62% | -0.00% (median -0.31%, t ~ +0.0) | -0.48% (median -0.89%, t ~ -0.8) | -0.97% (median -1.79%, t ~ -1.4) | -1.56% (median -4.44%, t ~ -0.4) |
| extended: prior 6m return > +50% | 1,784 | -0.07% | -0.44% (median -0.66%, t ~ -0.3) | -2.77% (median -3.86%, t ~ -1.7) | -5.47% (median -7.45%, t ~ -2.3) | -4.51% (median -16.72%, t ~ -0.3) |
| beaten down: prior 6m return < -30% | 1,443 | +0.84% | -0.52% (median -1.09%, t ~ -3.0) | -3.12% (median -2.90%, t ~ -4.4) | -5.80% (median -5.51%, t ~ -3.5) | -3.21% (median -7.81%, t ~ -1.6) |
| volume >= 10x | 2,275 | +1.75% | -1.36% (median -0.88%, t ~ -3.1) | -3.44% (median -2.59%, t ~ -5.9) | -6.23% (median -5.13%, t ~ -3.7) | -11.81% (median -14.31%, t ~ -2.6) |
| 2019-2021 | 3,178 | -0.14% | -0.57% (median -0.75%, t ~ -2.4) | -2.36% (median -2.68%, t ~ -3.1) | -3.76% (median -4.96%, t ~ -2.3) | -1.64% (median -9.58%, t ~ -0.5) |
| earnings only 2019-2021 | 782 | +1.45% | +0.08% (median +0.03%, t ~ +0.4) | -0.16% (median -1.04%, t ~ +1.3) | -0.66% (median -1.81%, t ~ +0.4) | +0.73% (median -3.51%, t ~ +0.4) |
| 2022-2026 | 4,416 | +0.82% | -0.33% (median -0.44%, t ~ -1.9) | -1.49% (median -1.13%, t ~ -3.5) | -3.60% (median -2.96%, t ~ -4.1) | -5.69% (median -7.31%, t ~ -1.4) |
| earnings only 2022-2026 | 1,858 | +1.47% | -0.03% (median -0.20%, t ~ -0.8) | -0.27% (median -0.45%, t ~ -0.6) | +0.37% (median -0.29%, t ~ -0.3) | -0.44% (median -3.20%, t ~ -0.6) |

#### EP trade variants, Panel B

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance |
|---|---|---|---|---|---|---|---|---|
| E-close: vol>=3x, strong close; buy close, LOD stop | 2,937 | 40.3% | -0.075 | -2.5 | -1.03% | 0.87 | 5.9 | 8.7% |
| E-close, trail SMA20 | 2,933 | 40.3% | -0.033 | -0.9 | -0.90% | 0.94 | 7.8 | 8.7% |
| E-close, trail SMA50, no partial/BE | 2,898 | 24.8% | +0.258 | +2.8 | +0.71% | 1.33 | 18.9 | 8.7% |
| E-close, earnings only | 1,226 | 46.7% | +0.029 | +0.7 | +0.19% | 1.06 | 6.5 | 6.6% |
| E-close, earnings only, trail SMA20 | 1,226 | 46.5% | +0.083 | +1.6 | +0.46% | 1.17 | 8.7 | 6.6% |
| E-close, earnings only, trail SMA50 no partial/BE | 1,215 | 26.4% | +0.330 | +3.0 | +1.57% | 1.45 | 21.4 | 6.6% |
| E-close, non-earnings only | 1,714 | 35.9% | -0.148 | -3.7 | -1.89% | 0.76 | 5.5 | 10.1% |
| E-close, neglected (6m ret -30..+30%) | 1,392 | 42.2% | -0.030 | -0.7 | +0.03% | 0.95 | 6.5 | 6.4% |
| E-close, earnings + neglected, trail SMA20 | 689 | 48.6% | +0.151 | +2.1 | +1.07% | 1.32 | 9.4 | 5.7% |
| E-close, gap >= 20% | 879 | 38.7% | -0.052 | -0.9 | -1.57% | 0.91 | 6.1 | 10.2% |
| E-close, volume >= 5x | 1,941 | 38.7% | -0.106 | -2.9 | -1.41% | 0.81 | 5.8 | 9.2% |
| E-close, cost 0 | 2,937 | 46.5% | -0.017 | -0.6 | -0.73% | 0.97 | 5.9 | 8.7% |
| E-close, cost 30 bp | 2,937 | 36.1% | -0.132 | -4.4 | -1.32% | 0.78 | 5.9 | 8.7% |
| E-open: buy the open, 1xADR stop (exact) | 11,808 | 30.4% | -0.058 | -3.0 | -1.09% | 0.91 | 3.7 | 9.1% |
| E-open, 1.5xADR stop (exact) | 11,625 | 37.4% | -0.046 | -3.2 | -1.23% | 0.91 | 4.9 | 13.2% |
| E-open, earnings only (exact) | 3,857 | 30.4% | -0.006 | -0.2 | -0.10% | 0.99 | 3.8 | 5.1% |
| E-orb proxy: buy open+0.25ADR, stop open-0.25ADR, worst case | 8,905 | 12.2% | -0.422 | -15.0 | -1.96% | 0.57 | 1.4 | 4.3% |
| E-orb proxy, close-based (optimistic bound) | 8,680 | 30.4% | +0.632 | +13.6 | +1.42% | 1.76 | 3.8 | 4.2% |
| E-orb proxy, entry-day low ignored | 8,627 | 31.1% | +0.031 | +0.6 | -0.65% | 1.02 | 4.2 | 4.2% |

#### Event study, A-window

| Subset | Events | Gap-day open->close | +1 day | +5 days | +20 days | +60 days |
|---|---|---|---|---|---|---|
| all gaps >= 10% | 11,386 | -0.79% | -0.24% (median -0.56%, t ~ -3.7) | -1.58% (median -2.07%, t ~ -3.4) | -3.24% (median -4.42%, t ~ -4.5) | -1.91% (median -8.39%, t ~ -1.1) |
| volume >= 3x and day $vol >= 10M | 6,688 | +0.70% | -0.39% (median -0.64%, t ~ -2.7) | -2.16% (median -2.05%, t ~ -5.5) | -4.43% (median -4.59%, t ~ -4.7) | -4.85% (median -9.58%, t ~ -1.6) |
| ... and close >= open, top half of range | 2,644 | +12.09% | -0.15% (median -0.50%, t ~ -0.4) | -1.97% (median -1.42%, t ~ -4.6) | -2.72% (median -2.69%, t ~ -2.6) | -2.36% (median -7.04%, t ~ -0.3) |
| ... and close < open (faded) | 3,324 | -9.36% | -0.70% (median -0.84%, t ~ -2.4) | -2.44% (median -2.64%, t ~ -3.6) | -5.42% (median -6.26%, t ~ -3.9) | -6.32% (median -11.66%, t ~ -1.4) |
| earnings reaction day | 2,393 | +1.59% | -0.02% (median -0.14%, t ~ -0.4) | -0.41% (median -0.76%, t ~ -0.5) | -0.12% (median -0.59%, t ~ -0.5) | -0.33% (median -3.73%, t ~ -0.2) |
| not an earnings day | 4,295 | +0.20% | -0.60% (median -1.10%, t ~ -2.8) | -3.13% (median -3.71%, t ~ -6.3) | -6.83% (median -8.16%, t ~ -5.2) | -7.39% (median -14.96%, t ~ -1.4) |
| earnings + close>=open, top half of range | 1,122 | +8.35% | -0.04% (median +0.01%, t ~ -1.5) | -0.75% (median -0.93%, t ~ -2.7) | -0.15% (median -0.77%, t ~ -0.8) | -1.09% (median -4.04%, t ~ -0.6) |
| gap 10-20% | 4,425 | +1.57% | +0.14% (median -0.41%, t ~ +0.2) | -1.06% (median -1.55%, t ~ -3.1) | -2.42% (median -3.61%, t ~ -3.1) | -1.92% (median -7.34%, t ~ -0.9) |
| gap 20-40% | 1,675 | +0.05% | -0.94% (median -0.88%, t ~ -3.1) | -3.50% (median -2.84%, t ~ -7.2) | -5.56% (median -5.28%, t ~ -3.0) | -8.36% (median -11.99%, t ~ -1.8) |
| gap 40-inf% | 588 | -3.99% | -2.85% (median -3.10%, t ~ -1.6) | -6.59% (median -8.23%, t ~ -2.9) | -16.30% (median -16.61%, t ~ -4.7) | -17.24% (median -28.58%, t ~ -1.0) |
| 'neglected': prior 6m return in [-30%, +30%] | 2,865 | +0.99% | -0.00% (median -0.35%, t ~ -0.5) | -0.76% (median -1.04%, t ~ -2.9) | -1.81% (median -2.15%, t ~ -2.8) | -2.56% (median -5.42%, t ~ -1.0) |
| extended: prior 6m return > +50% | 1,750 | +0.09% | -0.29% (median -0.96%, t ~ -0.6) | -3.20% (median -4.94%, t ~ -3.1) | -6.62% (median -10.53%, t ~ -2.8) | -7.18% (median -18.91%, t ~ -0.7) |
| beaten down: prior 6m return < -30% | 1,302 | +0.92% | -0.95% (median -1.53%, t ~ -2.4) | -3.49% (median -3.61%, t ~ -4.7) | -6.65% (median -6.55%, t ~ -3.6) | -4.85% (median -10.07%, t ~ -1.6) |
| volume >= 10x | 1,812 | +2.83% | -1.41% (median -1.43%, t ~ -2.0) | -4.67% (median -4.78%, t ~ -6.0) | -8.44% (median -8.86%, t ~ -3.8) | -14.21% (median -19.73%, t ~ -2.8) |
| 2019-2021 | 2,533 | -0.02% | -0.44% (median -1.03%, t ~ -2.0) | -2.52% (median -3.38%, t ~ -3.5) | -4.25% (median -6.38%, t ~ -2.0) | -1.79% (median -11.23%, t ~ -0.4) |
| earnings only 2019-2021 | 616 | +1.67% | -0.09% (median +0.02%, t ~ -0.3) | -0.37% (median -1.35%, t ~ +0.5) | -0.69% (median -1.18%, t ~ +0.2) | +0.16% (median -3.78%, t ~ +0.3) |
| 2022-2026 | 4,155 | +1.14% | -0.36% (median -0.51%, t ~ -1.9) | -1.94% (median -1.35%, t ~ -4.3) | -4.54% (median -3.69%, t ~ -4.5) | -6.74% (median -8.66%, t ~ -1.8) |
| earnings only 2022-2026 | 1,777 | +1.56% | +0.00% (median -0.19%, t ~ -0.3) | -0.43% (median -0.54%, t ~ -1.5) | +0.08% (median -0.49%, t ~ -0.8) | -0.50% (median -3.68%, t ~ -0.6) |

#### EP trade variants, A-window

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance |
|---|---|---|---|---|---|---|---|---|
| E-close: vol>=3x, strong close; buy close, LOD stop | 2,551 | 41.5% | -0.088 | -2.9 | -1.28% | 0.85 | 5.8 | 9.1% |
| E-close, trail SMA20 | 2,548 | 41.4% | -0.060 | -1.7 | -1.18% | 0.89 | 7.5 | 9.1% |
| E-close, trail SMA50, no partial/BE | 2,513 | 23.8% | +0.256 | +2.4 | +1.04% | 1.32 | 18.4 | 9.1% |
| E-close, earnings only | 1,121 | 46.7% | +0.006 | +0.1 | -0.02% | 1.01 | 6.5 | 6.7% |
| E-close, earnings only, trail SMA20 | 1,121 | 46.4% | +0.051 | +1.1 | +0.23% | 1.10 | 8.7 | 6.7% |
| E-close, earnings only, trail SMA50 no partial/BE | 1,111 | 25.9% | +0.317 | +2.7 | +1.59% | 1.42 | 21.3 | 6.7% |
| E-close, non-earnings only | 1,437 | 37.5% | -0.157 | -3.8 | -2.23% | 0.75 | 5.2 | 11.0% |
| E-close, neglected (6m ret -30..+30%) | 1,235 | 43.4% | -0.044 | -1.0 | -0.23% | 0.92 | 6.2 | 6.8% |
| E-close, earnings + neglected, trail SMA20 | 644 | 48.3% | +0.104 | +1.6 | +0.62% | 1.22 | 9.2 | 5.7% |
| E-close, gap >= 20% | 720 | 41.5% | -0.085 | -1.5 | -2.24% | 0.85 | 5.7 | 11.4% |
| E-close, volume >= 5x | 1,630 | 40.3% | -0.116 | -3.1 | -1.79% | 0.80 | 5.6 | 9.9% |
| E-close, cost 0 | 2,551 | 46.3% | -0.039 | -1.3 | -0.98% | 0.93 | 5.8 | 9.1% |
| E-close, cost 30 bp | 2,551 | 37.2% | -0.136 | -4.6 | -1.57% | 0.77 | 5.8 | 9.1% |
| E-open: buy the open, 1xADR stop (exact) | 10,431 | 30.1% | -0.060 | -2.9 | -1.17% | 0.91 | 3.6 | 9.3% |
| E-open, 1.5xADR stop (exact) | 10,263 | 37.4% | -0.053 | -3.4 | -1.34% | 0.90 | 4.7 | 13.5% |
| E-open, earnings only (exact) | 3,539 | 30.6% | +0.000 | +0.0 | -0.07% | 1.00 | 3.8 | 5.1% |
| E-orb proxy: buy open+0.25ADR, stop open-0.25ADR, worst case | 7,961 | 12.1% | -0.427 | -14.0 | -1.96% | 0.57 | 1.4 | 4.4% |
| E-orb proxy, close-based (optimistic bound) | 7,756 | 30.8% | +0.697 | +10.5 | +1.52% | 1.84 | 3.8 | 4.3% |
| E-orb proxy, entry-day low ignored | 7,700 | 31.6% | +0.095 | +1.3 | -0.52% | 1.06 | 4.2 | 4.3% |

### T4. Parabolic shorts

#### Event study, Panel A: profit of a short opened at the next open, no stop, no costs

| Definition | Events | +1 day | +3 days | +5 days | +10 days | +20 days |
|---|---|---|---|---|---|---|
| 5d run >= 100%, 3 up days, >=30% over SMA10 | 1,391 | mean +3.3%, median +8.9%, 67% win, worst -999% | mean +4.8%, median +12.5%, 68% win, worst -1702% | mean +6.8%, median +15.8%, 71% win, worst -1701% | mean +10.8%, median +20.8%, 72% win, worst -1618% | mean +12.8%, median +25.6%, 73% win, worst -1415% |
| 5d run >= 60% | 3,093 | mean +2.3%, median +4.7%, 62% win, worst -999% | mean +0.1%, median +7.7%, 63% win, worst -10039% | mean +4.4%, median +9.4%, 65% win, worst -1701% | mean +6.4%, median +12.2%, 66% win, worst -1618% | mean +8.0%, median +16.7%, 67% win, worst -2005% |
| 5d run >= 200% | 449 | mean +8.7%, median +15.1%, 68% win, worst -354% | mean +8.8%, median +18.2%, 72% win, worst -573% | mean +11.5%, median +23.3%, 74% win, worst -675% | mean +21.1%, median +31.6%, 77% win, worst -391% | mean +23.7%, median +39.0%, 78% win, worst -344% |
| 5d run >= 100%, day $vol >= 50M | 1,003 | mean +4.2%, median +9.2%, 67% win, worst -999% | mean +5.1%, median +12.3%, 68% win, worst -1702% | mean +7.4%, median +16.3%, 71% win, worst -1701% | mean +12.4%, median +22.3%, 73% win, worst -1618% | mean +15.1%, median +28.0%, 74% win, worst -1415% |
| 10d run >= 200% | 639 | mean +7.8%, median +11.8%, 69% win, worst -292% | mean +11.3%, median +17.9%, 73% win, worst -267% | mean +14.9%, median +23.0%, 75% win, worst -269% | mean +22.2%, median +31.5%, 77% win, worst -300% | mean +25.5%, median +38.2%, 80% win, worst -344% |
| 5d run >= 50%, day $vol >= 200M (large/liquid) | 1,311 | mean +2.6%, median +4.4%, 62% win, worst -354% | mean -3.9%, median +6.8%, 64% win, worst -10039% | mean +4.6%, median +8.7%, 65% win, worst -581% | mean +8.1%, median +12.8%, 67% win, worst -802% | mean +10.1%, median +17.8%, 69% win, worst -928% |

5d run >= 100% 2005-2012: n=100 5d mean +11.9% med +13.0% win 69%

5d run >= 100% 2013-2018: n=227 5d mean +13.1% med +18.4% win 72%

5d run >= 100% 2019-2021: n=533 5d mean +9.2% med +17.5% win 77%

5d run >= 100% 2022-2026: n=1138 5d mean +7.3% med +15.1% win 68%

#### Parabolic-short variants, Panel A

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance | 2005-12 | 2013-18 | 2019-21 | 2022-26 | Worst trade |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-red: first red close after 5d>=100%, stop=run high | 1,366 | 67.5% | +0.072 | +2.8 | +1.97% | 1.25 | 4.3 | 46.5% | +0.19 | +0.07 | +0.09 | +0.05 | -422% |
| P-red, target SMA20, hold<=20d | 1,368 | 63.2% | +0.062 | +2.1 | +3.19% | 1.16 | 8.1 | 46.5% | -0.09 | +0.07 | +0.10 | +0.06 | -422% |
| P-red, no target, 5-day time exit | 1,369 | 59.5% | +0.074 | +2.8 | +2.10% | 1.26 | 4.4 | 46.4% | +0.10 | +0.05 | +0.12 | +0.06 | -172% |
| P-red, run >= 60% | 3,054 | 62.0% | -0.008 | -0.4 | +0.56% | 0.98 | 4.1 | 35.1% | +0.05 | +0.02 | +0.01 | -0.03 | -422% |
| P-red, run >= 200% | 439 | 69.0% | +0.069 | +1.8 | +2.67% | 1.26 | 4.6 | 58.1% | +0.09 | +0.13 | +0.08 | +0.05 | -119% |
| P-red, day $vol >= 50M | 981 | 68.5% | +0.064 | +2.5 | +2.27% | 1.24 | 4.5 | 50.5% | +0.12 | +0.17 | +0.08 | +0.03 | -422% |
| P-red, cost 0, borrow 0 | 1,367 | 70.4% | +0.141 | +5.5 | +3.82% | 1.54 | 4.3 | 46.5% | +0.29 | +0.13 | +0.15 | +0.12 | -417% |
| P-red, cost 100bp/fill, borrow 100%/yr | 1,366 | 65.0% | +0.003 | +0.1 | +0.13% | 1.01 | 4.3 | 46.5% | +0.09 | +0.00 | +0.03 | -0.02 | -428% |
| P-red, cost 100bp/fill, borrow 300%/yr | 1,366 | 57.8% | -0.122 | -4.6 | -3.32% | 0.68 | 4.3 | 46.5% | -0.11 | -0.12 | -0.08 | -0.15 | -435% |
| P-open: short next open, stop +30%, pessimistic | 1,609 | 59.5% | +0.147 | +5.7 | +4.42% | 1.37 | 3.9 | 30.0% | +0.32 | +0.25 | +0.20 | +0.09 | -112% |
| P-open, stop +50% | 1,518 | 66.9% | +0.069 | +3.6 | +3.45% | 1.24 | 4.6 | 50.0% | +0.22 | +0.13 | +0.08 | +0.04 | -161% |
| P-open, stop +100% | 1,424 | 73.8% | +0.042 | +3.6 | +4.24% | 1.29 | 5.5 | 100.0% | +0.13 | +0.07 | +0.05 | +0.02 | -303% |

#### First-red-day short by year, Panel A

| Year | Trades | Win rate | Avg R | Sum R | Avg return |
|---|---|---|---|---|---|
| 2005 | 4 | 75% | +0.32 | +1.3 | +1.66% |
| 2006 | 5 | 60% | +0.68 | +3.4 | +5.37% |
| 2007 | 4 | 50% | -0.03 | -0.1 | -0.84% |
| 2008 | 13 | 69% | +0.04 | +0.5 | +6.09% |
| 2009 | 27 | 63% | +0.24 | +6.4 | -5.38% |
| 2010 | 7 | 43% | -0.07 | -0.5 | -2.29% |
| 2011 | 10 | 50% | -0.16 | -1.6 | -3.51% |
| 2012 | 7 | 100% | +0.78 | +5.4 | +15.98% |
| 2013 | 17 | 76% | +0.23 | +3.9 | +6.15% |
| 2014 | 20 | 70% | -0.04 | -0.8 | +0.94% |
| 2015 | 13 | 54% | -0.21 | -2.8 | -2.89% |
| 2016 | 22 | 73% | +0.32 | +7.1 | +7.66% |
| 2017 | 40 | 72% | +0.07 | +2.9 | +2.46% |
| 2018 | 38 | 66% | -0.01 | -0.3 | -0.14% |
| 2019 | 27 | 48% | -0.12 | -3.2 | -1.24% |
| 2020 | 184 | 75% | +0.16 | +28.5 | +4.88% |
| 2021 | 154 | 71% | +0.05 | +7.9 | +0.76% |
| 2022 | 80 | 75% | +0.15 | +12.2 | +4.45% |
| 2023 | 94 | 68% | +0.07 | +6.9 | +2.80% |
| 2024 | 209 | 62% | -0.00 | -0.7 | +0.52% |
| 2025 | 240 | 64% | +0.07 | +17.8 | +0.88% |
| 2026 | 151 | 67% | +0.03 | +4.2 | +2.65% |

exit reasons (0 stop, 2 time, 3 data end, 5 target): {5: 925, 0: 324, 2: 115, 3: 2}

#### Event study, Panel B

| Definition | Events | +1 day | +3 days | +5 days | +10 days | +20 days |
|---|---|---|---|---|---|---|
| 5d run >= 100%, 3 up days, >=30% over SMA10 | 1,093 | mean +1.8%, median +7.8%, 64% win, worst -999% | mean +4.3%, median +11.4%, 69% win, worst -1702% | mean +5.6%, median +14.6%, 71% win, worst -1701% | mean +8.9%, median +20.0%, 71% win, worst -1618% | mean +11.2%, median +24.0%, 73% win, worst -1415% |
| 5d run >= 60% | 2,456 | mean +1.8%, median +4.1%, 61% win, worst -999% | mean +3.5%, median +7.6%, 63% win, worst -1702% | mean +4.2%, median +9.1%, 65% win, worst -1701% | mean +5.7%, median +11.2%, 65% win, worst -1618% | mean +7.1%, median +16.2%, 67% win, worst -2005% |
| 5d run >= 200% | 326 | mean +5.7%, median +12.1%, 65% win, worst -354% | mean +7.5%, median +16.3%, 73% win, worst -573% | mean +10.9%, median +23.0%, 76% win, worst -675% | mean +19.7%, median +31.1%, 76% win, worst -391% | mean +21.6%, median +36.6%, 78% win, worst -344% |
| 5d run >= 100%, day $vol >= 50M | 801 | mean +2.0%, median +8.2%, 63% win, worst -999% | mean +4.0%, median +11.4%, 68% win, worst -1702% | mean +5.5%, median +15.0%, 71% win, worst -1701% | mean +9.7%, median +21.2%, 72% win, worst -1618% | mean +12.1%, median +25.8%, 74% win, worst -1415% |
| 10d run >= 200% | 459 | mean +5.4%, median +10.7%, 68% win, worst -210% | mean +11.8%, median +17.0%, 73% win, worst -200% | mean +15.0%, median +22.3%, 76% win, worst -269% | mean +20.5%, median +29.8%, 75% win, worst -300% | mean +23.1%, median +35.9%, 79% win, worst -344% |
| 5d run >= 50%, day $vol >= 200M (large/liquid) | 1,106 | mean +2.1%, median +3.9%, 62% win, worst -354% | mean +3.8%, median +6.6%, 64% win, worst -573% | mean +4.5%, median +9.1%, 65% win, worst -581% | mean +6.7%, median +11.7%, 66% win, worst -802% | mean +9.1%, median +17.8%, 69% win, worst -928% |

5d run >= 100% 2005-2012: n=15 5d mean +9.8% med +8.5% win 67%

5d run >= 100% 2013-2018: n=241 5d mean +13.2% med +16.8% win 74%

5d run >= 100% 2019-2021: n=603 5d mean +8.1% med +14.9% win 75%

5d run >= 100% 2022-2026: n=943 5d mean +6.3% med +13.9% win 68%

#### Parabolic-short variants, Panel B

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance | Worst trade |
|---|---|---|---|---|---|---|---|---|---|
| P-red: first red close after 5d>=100%, stop=run high | 1,103 | 66.5% | +0.055 | +1.9 | +1.54% | 1.18 | 4.4 | 45.6% | -422% |
| P-red, target SMA20, hold<=20d | 1,103 | 62.0% | +0.038 | +1.1 | +2.58% | 1.10 | 8.2 | 45.6% | -422% |
| P-red, no target, 5-day time exit | 1,103 | 58.9% | +0.072 | +2.4 | +2.05% | 1.25 | 4.5 | 45.6% | -172% |
| P-red, run >= 60% | 2,487 | 61.2% | -0.017 | -0.8 | +0.46% | 0.95 | 4.1 | 34.8% | -422% |
| P-red, run >= 200% | 326 | 69.0% | +0.016 | +0.4 | +0.98% | 1.06 | 4.7 | 58.7% | -163% |
| P-red, day $vol >= 50M | 804 | 67.4% | +0.033 | +1.1 | +1.38% | 1.12 | 4.6 | 49.9% | -422% |
| P-red, cost 0, borrow 0 | 1,103 | 69.9% | +0.130 | +4.5 | +3.40% | 1.50 | 4.4 | 45.6% | -417% |
| P-red, cost 100bp/fill, borrow 100%/yr | 1,103 | 64.1% | -0.021 | -0.7 | -0.32% | 0.94 | 4.4 | 45.6% | -428% |
| P-red, cost 100bp/fill, borrow 300%/yr | 1,103 | 56.6% | -0.165 | -5.2 | -3.82% | 0.61 | 4.4 | 45.6% | -435% |
| P-open: short next open, stop +30%, pessimistic | 1,285 | 57.8% | +0.104 | +3.7 | +3.13% | 1.26 | 4.0 | 30.0% | -140% |
| P-open, stop +50% | 1,215 | 65.3% | +0.047 | +2.2 | +2.34% | 1.16 | 4.7 | 50.0% | -161% |
| P-open, stop +100% | 1,144 | 71.9% | +0.037 | +3.0 | +3.74% | 1.27 | 5.6 | 100.0% | -161% |

#### Event study, A-window

| Definition | Events | +1 day | +3 days | +5 days | +10 days | +20 days |
|---|---|---|---|---|---|---|
| 5d run >= 100%, 3 up days, >=30% over SMA10 | 1,011 | mean +1.8%, median +8.4%, 65% win, worst -999% | mean +3.7%, median +11.8%, 68% win, worst -1702% | mean +5.5%, median +15.6%, 71% win, worst -1701% | mean +9.2%, median +20.4%, 71% win, worst -1618% | mean +10.7%, median +24.8%, 73% win, worst -1415% |
| 5d run >= 60% | 2,224 | mean +1.5%, median +4.5%, 61% win, worst -999% | mean -1.9%, median +7.7%, 63% win, worst -10039% | mean +3.4%, median +9.4%, 65% win, worst -1701% | mean +5.5%, median +11.7%, 65% win, worst -1618% | mean +6.7%, median +16.6%, 67% win, worst -2005% |
| 5d run >= 200% | 319 | mean +5.7%, median +13.0%, 65% win, worst -354% | mean +6.5%, median +17.5%, 72% win, worst -573% | mean +9.8%, median +23.2%, 73% win, worst -675% | mean +19.5%, median +31.0%, 74% win, worst -391% | mean +20.1%, median +37.4%, 75% win, worst -344% |
| 5d run >= 100%, day $vol >= 50M | 749 | mean +2.4%, median +8.6%, 65% win, worst -999% | mean +3.8%, median +11.7%, 68% win, worst -1702% | mean +5.6%, median +16.0%, 71% win, worst -1701% | mean +10.3%, median +22.0%, 72% win, worst -1618% | mean +12.4%, median +26.9%, 74% win, worst -1415% |
| 10d run >= 200% | 460 | mean +5.6%, median +11.4%, 67% win, worst -292% | mean +11.1%, median +17.7%, 73% win, worst -267% | mean +15.4%, median +23.2%, 76% win, worst -269% | mean +21.9%, median +31.3%, 76% win, worst -300% | mean +24.2%, median +37.6%, 79% win, worst -344% |
| 5d run >= 50%, day $vol >= 200M (large/liquid) | 1,021 | mean +2.3%, median +5.1%, 63% win, worst -354% | mean -5.8%, median +7.7%, 64% win, worst -10039% | mean +4.7%, median +10.4%, 66% win, worst -581% | mean +7.9%, median +14.1%, 68% win, worst -802% | mean +10.1%, median +19.3%, 70% win, worst -928% |

5d run >= 100% 2005-2012: n=100 5d mean +11.9% med +13.0% win 69%

5d run >= 100% 2013-2018: n=227 5d mean +13.1% med +18.4% win 72%

5d run >= 100% 2019-2021: n=533 5d mean +9.2% med +17.5% win 77%

5d run >= 100% 2022-2026: n=1138 5d mean +7.3% med +15.1% win 68%

#### Parabolic-short variants, A-window

| Variant | Trades | Win rate | Avg R | t (naive) | Avg return | Profit factor | Avg hold (days) | Avg stop distance | Worst trade |
|---|---|---|---|---|---|---|---|---|---|
| P-red: first red close after 5d>=100%, stop=run high | 992 | 67.7% | +0.072 | +2.3 | +1.98% | 1.25 | 4.4 | 46.4% | -422% |
| P-red, target SMA20, hold<=20d | 994 | 63.9% | +0.076 | +2.2 | +3.35% | 1.20 | 8.0 | 46.4% | -422% |
| P-red, no target, 5-day time exit | 993 | 60.3% | +0.095 | +2.9 | +2.74% | 1.34 | 4.5 | 46.4% | -172% |
| P-red, run >= 60% | 2,196 | 61.7% | -0.013 | -0.6 | +0.42% | 0.96 | 4.1 | 35.7% | -422% |
| P-red, run >= 200% | 309 | 69.3% | +0.043 | +0.9 | +1.81% | 1.15 | 4.7 | 58.3% | -119% |
| P-red, day $vol >= 50M | 732 | 68.4% | +0.048 | +1.6 | +1.72% | 1.17 | 4.6 | 50.6% | -422% |
| P-red, cost 0, borrow 0 | 993 | 70.5% | +0.140 | +4.5 | +3.84% | 1.54 | 4.4 | 46.4% | -417% |
| P-red, cost 100bp/fill, borrow 100%/yr | 992 | 65.5% | +0.005 | +0.2 | +0.14% | 1.02 | 4.4 | 46.4% | -428% |
| P-red, cost 100bp/fill, borrow 300%/yr | 992 | 58.1% | -0.117 | -3.6 | -3.33% | 0.70 | 4.4 | 46.4% | -435% |
| P-open: short next open, stop +30%, pessimistic | 1,166 | 58.5% | +0.128 | +4.2 | +3.83% | 1.31 | 3.9 | 30.0% | -112% |
| P-open, stop +50% | 1,104 | 65.7% | +0.050 | +2.2 | +2.49% | 1.17 | 4.6 | 50.0% | -161% |
| P-open, stop +100% | 1,032 | 73.1% | +0.039 | +2.8 | +3.89% | 1.27 | 5.5 | 100.0% | -303% |

### T5. Portfolio level ($100,000 start, 0.5% risk per trade)

#### Panel A, 2005-01-03 to 2026-11-17

| Strategy | CAGR | Vol | Sharpe | Max drawdown | Final multiple | Trades taken / signals | Avg gross exposure |
|---|---|---|---|---|---|---|---|
| Breakout Q0 (regime filter) | -2.6% | 8.1% | -0.50 | -51.8% | 0.56x | 1,478 / 1,478 | 10% |
| Breakout Q0, no regime filter | -1.9% | 14.5% | -0.18 | -51.3% | 0.66x | 2,691 / 2,694 | 18% |
| Breakout Q0, entry day worst case | -4.1% | 7.9% | -0.72 | -62.8% | 0.40x | 1,479 / 1,479 | 9% |
| Breakout Q0, 1% risk, 140% gross | -5.7% | 15.8% | -0.40 | -78.9% | 0.28x | 1,476 / 1,478 | 19% |
| Earnings EP, close entry, 50-day trail | +4.6% | 16.6% | 0.25 | -37.4% | 2.69x | 1,634 / 2,198 | 55% |
| Earnings EP, close entry, his 3-5d/10-day rules | -2.8% | 7.7% | -0.56 | -50.5% | 0.54x | 2,097 / 2,215 | 17% |
| All EPs, close entry, 50-day trail | +2.3% | 25.2% | 0.14 | -66.1% | 1.65x | 2,608 / 4,482 | 71% |
| Earnings EP 50-day trail, $100,000 account, <=1% of ADV | +4.6% | 16.7% | 0.25 | -37.5% | 2.70x | 1,701 / 2,198 | 55% |
| Earnings EP 50-day trail, $1,000,000 account, <=1% of ADV | +7.2% | 15.6% | 0.41 | -36.8% | 4.62x | 1,847 / 2,198 | 49% |
| Earnings EP 50-day trail, $10,000,000 account, <=1% of ADV | +6.6% | 11.4% | 0.46 | -26.1% | 4.02x | 1,891 / 2,198 | 27% |
| Earnings EP 50-day trail, $100,000,000 account, <=1% of ADV | +3.1% | 5.8% | 0.25 | -11.4% | 1.95x | 1,024 / 2,198 | 8% |
| Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow | +5.4% | 5.1% | 0.72 | -8.5% | 3.18x | 1,600 / 1,609 | 2% |
| Parabolic short, 100bp/fill, 150% borrow | +2.5% | 5.0% | 0.16 | -15.6% | 1.71x | 1,600 / 1,609 | 2% |
| SPY buy & hold (total return) | +10.6% | 18.9% | 0.54 | -55.2% | 9.05x | 0 / 0 | 100% |
| QQQ buy & hold (total return, to 2026-09-11) | +15.1% | 21.6% | 0.68 | -53.4% | 21.27x | 0 / 0 | 100% |

Calendar-year returns, Panel A, 2005-01-03 to 2026-11-17 (%):

| Year | Breakout Q0 (regime filter) | Breakout Q0, no regime filter | Earnings EP, close entry, 50-day trail | Earnings EP, close entry, his 3-5d/10-day rules | Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow | SPY buy & hold (total return) | QQQ buy & hold (total return, to 2026-09-11) |
|---|---|---|---|---|---|---|---|
| 2005 | +1.3 | -8.0 | +31.6 | +2.6 | +0.3 | +5.3 | +2.6 |
| 2006 | +0.4 | -4.2 | +6.4 | -1.0 | +0.6 | +15.8 | +7.1 |
| 2007 | -1.8 | -4.8 | +9.0 | -2.4 | +0.4 | +5.1 | +19.0 |
| 2008 | -2.0 | -5.4 | -11.1 | -6.6 | +2.8 | -36.8 | -41.7 |
| 2009 | -1.5 | +7.2 | +6.8 | -2.8 | +2.3 | +26.4 | +54.7 |
| 2010 | +10.7 | +18.3 | +13.5 | -1.9 | +2.3 | +15.1 | +20.1 |
| 2011 | -3.7 | -2.8 | -1.9 | -2.6 | +1.6 | +1.9 | +3.5 |
| 2012 | +0.2 | -1.9 | +4.2 | +3.4 | +2.8 | +16.0 | +18.1 |
| 2013 | +9.6 | +13.4 | +19.0 | -4.9 | -0.8 | +32.3 | +36.6 |
| 2014 | -6.1 | -7.3 | -4.6 | -2.6 | +3.7 | +13.5 | +19.2 |
| 2015 | -4.3 | -5.1 | -20.0 | -9.6 | +2.3 | +1.3 | +9.4 |
| 2016 | +5.1 | +16.2 | +16.8 | +5.0 | +6.6 | +12.0 | +7.1 |
| 2017 | -11.1 | -6.1 | +5.0 | +3.1 | +6.5 | +21.7 | +32.7 |
| 2018 | -4.9 | +1.0 | +9.9 | -7.8 | +6.2 | -4.6 | -0.1 |
| 2019 | -5.1 | -1.1 | +9.1 | -5.6 | +3.1 | +31.2 | +39.0 |
| 2020 | +9.2 | +15.4 | +18.9 | -9.3 | +32.8 | +18.4 | +48.4 |
| 2021 | -9.7 | -10.9 | +4.3 | -0.3 | +9.3 | +28.7 | +27.4 |
| 2022 | -12.0 | -20.1 | -23.8 | -5.4 | +2.7 | -18.2 | -32.6 |
| 2023 | -6.7 | -5.3 | +40.1 | +9.0 | -0.3 | +26.2 | +54.9 |
| 2024 | -15.0 | -14.3 | +0.0 | +6.6 | +7.4 | +24.9 | +25.6 |
| 2025 | +4.8 | +2.7 | -14.6 | -6.5 | +24.3 | +17.7 | +20.8 |
| 2026 | -8.3 | -7.0 | +6.1 | -17.2 | +7.9 | +8.2 | n/a |

Factor regression, Earnings EP, close entry, 50-day trail (2005-01-04..2026-09-30, n=5469): alpha +0.4%/yr (t=+0.1) | Mkt +0.39 (t=+38.2) | SMB +0.44 (t=+23.1) | HML -0.08 (t=-4.7) | MOM +0.08 (t=+6.9) | R2 0.31

Factor regression, Breakout Q0 (regime filter) (2005-01-04..2026-09-30, n=5469): alpha -4.5%/yr (t=-2.7) | Mkt +0.06 (t=+10.3) | SMB +0.14 (t=+12.9) | HML -0.01 (t=-0.9) | MOM -0.00 (t=-0.4) | R2 0.06

#### Panel B, 2019-07-01 to 2026-01-28

| Strategy | CAGR | Vol | Sharpe | Max drawdown | Final multiple | Trades taken / signals | Avg gross exposure |
|---|---|---|---|---|---|---|---|
| Breakout Q0 (regime filter) | -3.5% | 11.7% | -0.49 | -45.0% | 0.79x | 735 / 735 | 12% |
| Breakout Q0, no regime filter | -4.7% | 22.4% | -0.24 | -54.6% | 0.73x | 1,171 / 1,174 | 20% |
| Breakout Q0, entry day worst case | -5.5% | 11.5% | -0.69 | -48.6% | 0.69x | 735 / 735 | 12% |
| Breakout Q0, 1% risk, 140% gross | -7.7% | 23.0% | -0.36 | -70.2% | 0.59x | 735 / 735 | 25% |
| Earnings EP, close entry, 50-day trail | +4.4% | 20.6% | 0.18 | -33.4% | 1.33x | 755 / 1,215 | 74% |
| Earnings EP, close entry, his 3-5d/10-day rules | +0.8% | 12.1% | -0.11 | -26.3% | 1.06x | 1,125 / 1,226 | 29% |
| All EPs, close entry, 50-day trail | +5.1% | 28.1% | 0.22 | -46.1% | 1.39x | 1,243 / 2,898 | 92% |
| Earnings EP 50-day trail, $100,000 account, <=1% of ADV | +4.3% | 20.6% | 0.17 | -33.7% | 1.32x | 812 / 1,215 | 74% |
| Earnings EP 50-day trail, $1,000,000 account, <=1% of ADV | +6.8% | 20.6% | 0.29 | -33.1% | 1.54x | 863 / 1,215 | 71% |
| Earnings EP 50-day trail, $10,000,000 account, <=1% of ADV | +14.8% | 17.1% | 0.73 | -29.8% | 2.49x | 1,019 / 1,215 | 51% |
| Earnings EP 50-day trail, $100,000,000 account, <=1% of ADV | +5.5% | 7.6% | 0.37 | -11.5% | 1.42x | 595 / 1,215 | 15% |
| Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow | +9.3% | 8.2% | 0.78 | -13.5% | 1.79x | 1,266 / 1,285 | 5% |
| Parabolic short, 100bp/fill, 150% borrow | +1.1% | 8.2% | -0.17 | -23.6% | 1.08x | 1,266 / 1,285 | 5% |
| SPY buy & hold (total return) | +15.6% | 20.1% | 0.68 | -33.7% | 2.59x | 0 / 0 | 100% |
| QQQ buy & hold (total return) | +20.8% | 24.5% | 0.78 | -35.2% | 3.48x | 0 / 0 | 100% |

Calendar-year returns, Panel B, 2019-07-01 to 2026-01-28 (%):

| Year | Breakout Q0 (regime filter) | Breakout Q0, no regime filter | Earnings EP, close entry, 50-day trail | Earnings EP, close entry, his 3-5d/10-day rules | Parabolic short (next open, +30% stop), 50bp/fill, 50% borrow | SPY buy & hold (total return) | QQQ buy & hold (total return) |
|---|---|---|---|---|---|---|---|
| 2019 | +7.1 | +6.3 | -5.6 | +5.4 | -2.0 | +9.9 | +12.8 |
| 2020 | +5.7 | +10.6 | +30.1 | -5.2 | +40.1 | +18.4 | +48.4 |
| 2021 | -8.0 | -13.6 | +3.9 | -3.5 | +3.5 | +28.7 | +27.4 |
| 2022 | -14.2 | -24.0 | -24.9 | -5.8 | +4.2 | -18.2 | -32.7 |
| 2023 | -5.0 | -4.2 | +55.9 | +20.1 | -6.4 | +26.2 | +54.9 |
| 2024 | -14.4 | -14.7 | -1.7 | +5.3 | +2.8 | +24.9 | +25.6 |
| 2025 | +10.0 | +10.0 | -15.8 | -8.0 | +22.9 | +17.7 | +20.8 |
| 2026 | -1.0 | +4.9 | +7.5 | -0.3 | +2.3 | +2.0 | +3.1 |

Factor regression, Earnings EP, close entry, 50-day trail (2019-07-02..2026-01-28, n=1653): alpha -1.1%/yr (t=-0.2) | Mkt +0.42 (t=+20.8) | SMB +0.57 (t=+15.5) | HML -0.11 (t=-4.1) | MOM +0.07 (t=+3.1) | R2 0.36

Factor regression, Breakout Q0 (regime filter) (2019-07-02..2026-01-28, n=1653): alpha -6.1%/yr (t=-1.4) | Mkt +0.07 (t=+5.0) | SMB +0.22 (t=+8.7) | HML -0.00 (t=-0.2) | MOM -0.02 (t=-1.4) | R2 0.08

### T6. Month-clustered significance

#### Panel A

| Setup | Trades | Avg R | t naive | t month-clustered | Avg return | t of return, clustered |
|---|---|---|---|---|---|---|
| Breakout Q0 | 1,478 | -0.070 | -1.9 | -1.6 | -0.51% | -1.3 |
| Breakout close-confirmed | 918 | -0.210 | -4.0 | -3.8 | -1.19% | -2.7 |
| EP close entry, standard rules | 4,538 | -0.111 | -5.2 | -3.6 | -1.19% | -4.2 |
| Earnings EP, standard rules | 2,215 | -0.052 | -1.9 | -1.4 | -0.24% | -1.0 |
| Earnings EP, 50-day trail | 2,198 | +0.248 | +3.1 | +2.5 | +1.21% | +2.1 |
| Parabolic short, next open, +30% stop | 1,609 | +0.147 | +5.7 | +5.1 | +4.42% | +5.1 |
| Parabolic short, first red day | 1,366 | +0.072 | +2.8 | +2.3 | +1.97% | +2.2 |

#### Panel B

| Setup | Trades | Avg R | t naive | t month-clustered | Avg return | t of return, clustered |
|---|---|---|---|---|---|---|
| Breakout Q0 | 735 | -0.054 | -0.9 | -0.7 | -0.31% | -0.4 |
| Breakout close-confirmed | 436 | -0.121 | -1.5 | -1.5 | -0.82% | -1.0 |
| EP close entry, standard rules | 2,937 | -0.075 | -2.5 | -1.8 | -1.03% | -2.7 |
| Earnings EP, standard rules | 1,226 | +0.029 | +0.7 | +0.5 | +0.19% | +0.5 |
| Earnings EP, 50-day trail | 1,215 | +0.330 | +3.0 | +2.1 | +1.57% | +1.7 |
| Parabolic short, next open, +30% stop | 1,285 | +0.104 | +3.7 | +2.8 | +3.13% | +2.8 |
| Parabolic short, first red day | 1,103 | +0.055 | +1.9 | +1.4 | +1.54% | +1.4 |

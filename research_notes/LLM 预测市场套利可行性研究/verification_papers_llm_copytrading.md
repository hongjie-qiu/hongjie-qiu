# Verification log: LLM-trading and copy-trading claims checked against primary sources

> **Status: COMPLETE.** Checked on 26 November 2026. Eleven claims from the earlier notes were traced to their primary sources, which were fetched with plain `curl` requests through the session proxy (no altered headers, no private APIs) and read as text. One of three permitted web searches was used.
>
> **Status labels.**
> - **CONFIRMED**: I saw the figure in the source itself in this pass.
> - **CONFIRMED (cited)**: a second-round researcher read the full text and recorded the figure; as instructed, I cite that entry and did not re-open the source.
> - **CORRECTED**: the source says something different from the notes; use the wording given here.
> - **PARTLY**: part confirmed, part not found or not checkable.
> - **COULD NOT OPEN**: the request was refused and was not retried.
> - "My calculation" marks arithmetic of mine; it is never a published figure.

## Summary table (rows needing a change come first)

| # | Short claim | Status |
|---|---|---|
| 2 | Prophet Arena (ICLR 2026): Brier 0.18–0.22 vs market 0.187; ECE ≤ 0.05 vs 0.069; ablation 0.191 vs 0.169; live Gemini 3 run +80.33%, Sharpe 3.35 | Headline scores CONFIRMED. Ablation **CORRECTED** (an average across models on a different, smaller event set; not comparable with 0.187). Live run CONFIRMED (cited) |
| 9 | Bürgi, Deng and Whelan: −20% before fees, −22% after fees; favourite-longshot; maker vs taker | **PARTLY**: −20% before fees CONFIRMED; −22% after fees NOT FOUND in the version opened; makers −9.64% vs takers −31.46% CONFIRMED |
| 6 | KalshiBench ECE 0.120–0.395; KellyBench all models lose, human +5.1%; PolyBench 5 of 7 negative | All three headline claims CONFIRMED. KellyBench detail **CORRECTED** (best model and bankroll range) |
| 7 | Mitts and Ofir: about $143M anomalous profit; 152 wallets, about $8M in military markets | **PARTLY**: $143M seen only in the authors' own published summary (the paper on SSRN COULD NOT OPEN). The 152 wallets / $8M figure is from a different study (Anti-Corruption Data Collective) and is CONFIRMED in the original report |
| 1 | Prediction Arena: six models, $10,000 each, all lost on Kalshi (−16.0% to −30.8%, average −22.6%); Polymarket −1.1% | CONFIRMED, with a caveat on the −22.6% average |
| 3 | El Lahib et al.: Brier 0.242 → 0.108 from date-filtered search leakage | CONFIRMED, with a scope qualifier |
| 4 | Jia and Sun: Polymarket copy trading with live on-chain execution | CONFIRMED; the missing numbers are now recorded |
| 5 | ForecastBench: 69.2 vs 68.8 (22 Sep 2026) and 69.5 vs 68.1 (25 Nov 2026) | CONFIRMED, both; no conflict (different snapshot dates) |
| 8 | Columbia wash-trading study: about 25% of volume; 45% sports, 3% crypto | CONFIRMED |
| 10 | Bartlett and O'Hara: makers won 63.4% of single-name contracts. Becker: ±2.65% at 50 cents, 72.1M trades | CONFIRMED, both |
| 11 | Gu et al. (v3, 23 Sep 2026): significantly positive simulated score gaps for five newest model variants | CONFIRMED (cited); not re-opened |

## Corrections and wording changes to apply (most important first)

1. **Prophet Arena ablation (claim 2).** The four figures are **averages across all tested LLMs**, not one model: none 0.2349, news sources only 0.1913, market data only 0.1731, both 0.1688. A footnote in the ICLR version says the experiments in that section use a subset of 100 events, whereas the market baseline of 0.187 is computed on 1,367 events. The notes' inference "without market data the model scored 0.191, worse than the market's 0.187" therefore compares two different event sets and should not be stated as a like-for-like result. What the ablation does support: seeing the market price improves the average score far more (0.235 → 0.173) than seeing news does (0.235 → 0.191), and adding news to the market price adds little (0.173 → 0.169).
2. **Bürgi, Deng and Whelan (claim 9).** "−22% after fees" does not appear in the version I could open (GWU working paper 2026-001). That version states −20% as the average **pre-fee** return and gives after-fee averages of −9.64% for makers and −31.46% for takers. Also, "over 300,000 contracts" means 313,972 price observations (Yes and No sides, up to 11 daily snapshots each) on 46,282 distinct contracts, and the average is unweighted across those observations: the paper itself notes that the money-weighted pre-fee return is zero by definition.
3. **KellyBench (claim 6).** In the arXiv paper the best model by return is GPT-5.4 (−7.9%, mean final bankroll £92,063); Claude Opus 4.6 is second (−11.2%, £88,771) and is best only on the "sophistication" rubric (26.5%). The range of mean final bankrolls in the paper is £10,421 to £92,063. "£96,336 (Claude Opus 4.7)" is not in the paper's results table.
4. **Prediction Arena (claim 1).** −22.6% is the paper's figure, but the paper describes it as the Kalshi average "over the concurrent Feb 9–Mar 9 window" used for the Polymarket comparison. The simple mean of the six final Kalshi returns in its Table 1 is −23.95% (my calculation). Add that the Kalshi leg was 29 curated markets in which 71–97% of each model's settled positions were weather markets.
5. **Mitts and Ofir (claim 7).** The $8M / 152 wallets study is by the Anti-Corruption Data Collective, not Mitts and Ofir. For Mitts and Ofir, only the figures in the authors' March 2026 summary are verified ($143M, 210,718 wallet-market pairs, 69.9% win rate); "$119M above execution prices" and "1,152 pairs account for $67.9M" were not checked.
6. **Prophet Arena calibration (claim 2).** "All selected models ≤ 0.05" is slightly too strong: three of the five representative models are at 0.041–0.043; the other two are 0.060 and 0.067, still below the market's 0.069. Across all 23 models the market ranks 19th of 24 on calibration error, so a few models are worse calibrated than the market.
7. **El Lahib et al. (claim 3).** 0.108 is the score on 93 questions selected because a direct-leak document existed, with only the leaky documents supplied. It shows how large the inflation can be, not the score of a typical date-filtered pipeline.
8. **Becker's category gaps (claim 10)** are now verified and can replace the second-round "unverified recollection": politics 1.02, crypto 2.69, entertainment 4.79 percentage points.

---

## Entries per claim

### 1. Prediction Arena — CONFIRMED (caveat on the average)

- **Notes say** (`llm_forecasting_evidence.md` lines 51, 69, 148, 264; `practitioner_implementation_risks.md` lines 92, 97, 136; `residual_inefficiency_calibration.md` line 203): six frontier models with $10,000 each, real money, 12 January–9 March 2026; all lost on Kalshi, −16.0% to −30.8%, average −22.6%; Polymarket average −1.1%.
- **Opened**: [arXiv abstract page](https://arxiv.org/abs/2604.07355) and [full text](https://arxiv.org/html/2604.07355). Only v1 exists (28 March 2026). Authors: Zhang, Liu, Johansson, Yitayew, Ohly, Li (Arcada Labs; Harvard University).
- **Source wording** (abstract): "Each model operates as an independent agent starting with $10,000, making autonomous decisions every 15–45 minutes." "For the primary Cohort 1, final Kalshi returns range from -16.0% to -30.8%." "Cohort 1 models averaged only -1.1% on Polymarket vs. -22.6% on Kalshi".
- **Kalshi, Table 1 (57 days, real capital)**:

| Model | Final value | Total return | Trades | Max drawdown |
|---|---|---|---|---|
| glm-4.7 (Zhipu AI) | $8,398 | −16.0% | 361 | 16.3% |
| grok-4-20-checkpoint (xAI) | $7,999 | −20.0% | 424 | 30.9% |
| gpt-5.2 (OpenAI) | $7,950 | −20.5% | 452 | 18.4% |
| claude-opus-4-5-20251101 (Anthropic) | $7,409 | −25.9% | 886 | 25.9% |
| gemini-3-pro-preview (Google DeepMind) | $6,950 | −30.5% | 664 | 30.8% |
| grok-4-1-fast-reasoning (xAI) | $6,925 | −30.8% | 129 | 30.8% |

- **The −22.6% average**: stated in the abstract, the introduction, the Polymarket results section and the Figure 6 caption. The results section words it as "Cohort 1 models averaged -22.6% on Kalshi over the concurrent Feb 9–Mar 9 window, but only -1.1% on Polymarket over that same period." The mean of the six Table 1 returns is −23.95% (my calculation), so −22.6% is not the mean of the final returns and the paper does not show how it is computed. The average for the first 34 days is given as −13.8%.
- **Polymarket, Table 3 (real capital, 9 February–9 March 2026)**: grok-4-20-checkpoint −1.85% (18 trades, 71.4% settlement win rate); gemini-3-pro-preview −1.81% (155 trades); gpt-5.2 −0.42% (127); glm-4.7 −0.09% (95); claude-opus-4-5 −2.68% (86); grok-4-1-fast-reasoning 0.00% (no trades). No model was positive. The mean is −1.14% including the model that never traded and −1.37% across the five that did (my calculation).
- **Decision frequency**: "Trading cycles execute approximately every 15–45 minutes" (experimental setup).
- **What the authors say drove results**: "initial prediction accuracy and the ability to capitalize on correct predictions are the main drivers, while research volume shows no correlation with outcomes" (abstract); the spread between models is "driven not by market luck but by systematic differences in initial prediction accuracy, risk discipline, and (in Phase 2) the decision of whether to continue trading at all" (conclusion). Settlement win rates were 15.4% to 51.9%. On exits: "most models showing negative average PnL from early exits — suggesting models may be exiting winners too early or holding losers too long" (§8.4). The authors do not attribute the losses to fees.
- **Qualifiers the notes missed**:
  - The Kalshi leg used "a curated set of 29 standardized markets"; "71–97% of settled positions fell in weather markets", and Kalshi "functioned largely as a weather-forecasting benchmark during this period" (§8.5). The Kalshi losses are therefore mostly a statement about weather contracts.
  - On the Kalshi/Polymarket gap: "Whether this reflects better market selection ability or more favorable market pricing on Polymarket cannot be fully disentangled from current data."
  - Returns are real account values (open positions marked at the bid), so they are after fees and spreads. The paper does not break out fees, and I found no dollar figure for inference cost (it analyses token usage only).
  - Stated limitations (§9.1): orders "frequently rejected" for lack of a counterparty; one shared prompt; only "a basic web search tool"; prices fetched at cycle start; a 15% position limit; a short period. No significance tests are reported.
  - The +6.02% for gemini-3.1-pro-preview is three days of paper trading (6–9 March 2026), which "execute[s] unconditionally, without requiring a real counterparty".
  - Self-reported by the benchmark operator; arXiv preprint. Sample: 2,916 Kalshi trades and 700 settled positions.

### 2. Prophet Arena — headline scores CONFIRMED; ablation CORRECTED; live run CONFIRMED (cited)

- **Notes say** (`llm_forecasting_evidence.md` lines 40–41, 49, 68, 121, 193, 198, 228, 236): more than 1,300 Kalshi events; frontier models 0.18–0.22 Brier vs market 0.187; ECE ≤ 0.05 vs 0.069; ablation 0.169 with market data and news, 0.191 with sources only; the team's Gemini 3 agent returned +80.33% in 26 days with Sharpe 3.35.
- **Opened**: [arXiv 2510.17638, v2 of 21 December 2025](https://arxiv.org/html/2510.17638) and the [ICLR 2026 proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/aec5e2847c5ae90f939ab786774856cc-Paper-Conference.pdf).
- **Sample**: "1300+ resolved real-world events" (abstract); "Our evaluation is conducted on 1,367 events that were resolved before October 11, 2025." Category mix: "76% Sports, 8% Entertainment, 7% Politics, and 9% Other" (arXiv v2).
- **Table 2, identical in both versions (Brier with 95% interval; ECE; simulated average return, where 1 is break-even)**:

| Model | Brier | ECE | Average return |
|---|---|---|---|
| GPT-5 (high reasoning) | 0.184 (±0.006) | 0.042 | 0.943 (±0.042) |
| Grok-4 | 0.189 (±0.005) | 0.043 | 0.864 (±0.052) |
| Claude Sonnet 4 | 0.194 (±0.006) | 0.041 | 0.909 (±0.101) |
| Gemini 2.5 Flash | 0.197 (±0.007) | 0.067 | 0.883 (±0.053) |
| Llama-4-Scout | 0.219 (±0.008) | 0.060 | 0.805 (±0.040) |
| Market baseline | 0.187 (±0.006) | 0.069 | 0.899 (±0.043) |

- **Band wording differs by version**: arXiv v2 says "Brier scores fall in a narrow band [0.18,0.22]"; the ICLR version says "[0.17, 0.24]". Both figures in the notes are therefore genuine. The "0.188" in the notes is the market baseline in an appendix table on rebalanced event subsets (0.188 ±0.008), not a different headline.
- **Calibration**: "strong models typically achieve ECE ≤ 0.05, whereas weaker ones fall in the [0.06,0.2] range. Nevertheless, all the selected LLMs demonstrate better calibration than the market baseline" (arXiv v2). In the full table of 23 models the market baseline ranks 3rd of 24 on Brier, 19th of 24 on ECE and 10th of 24 on return.
- **Returns**: "even GPT-5, the top-ranked model, fails to reach break-even (Average Return <1), and most models fall below 0.9." Returns are simulated, not real money.
- **Ablation (CORRECTED)**: the numbers are printed as labels on the ICLR version's Figure 4, left panel (Figure 5 in arXiv v2, where the labels are not in the text): None 0.2349; Sources 0.1913; Market 0.1731; Both 0.1688. The text says the figure "shows the average Brier scores across all tested LLMs under four conditions" with error bars for the interquartile range across models, and "models using only market data perform only slightly worse, on average, than those with both market data and news sources". ICLR footnote 6, on the preceding page: "Due to the resource constraint, our experiment results in this section uses a subset of 100 events sampled uniformly from our full benchmark." I could not locate the footnote's anchor in the extracted text, so its exact scope is my reading. I did not find a market baseline computed on that subset.
- **Qualifiers the notes missed**: every model receives the Kalshi market snapshot in its context by default; three quarters of the events are sports; only one model variant has a lower point estimate than the market (0.184 vs 0.187), with overlapping intervals.
- **Live Gemini 3 run** (this is a different paper, Gu et al., arXiv 2607.06166, not the ICLR paper). Not re-opened; cited from `residual_inefficiency_calibration.md` line 188, marked there as a full-text read: Gemini 3 Pro with search on Kalshi for 26 days in April–May 2026; **starting capital $200**, ending $360.67 (+80.33%); **+24.2% after dropping the three best and three worst trades**; 1,605 forecasts, 396 signals, **236 fills in 129 markets**; $26.31 of fees; win rate 50.9%; maximum drawdown 15.7%; Sharpe 3.35 with a 90% interval of 0.90–6.12; markets closing in 2–14 days only, Mentions excluded; the authors say results "should NOT be interpreted as trading suggestions".

### 3. El Lahib et al. — CONFIRMED (scope qualifier)

- **Notes say** (`llm_forecasting_evidence.md` line 140): gpt-oss-120b scored Brier 0.108 with leaky retrieved documents vs 0.242 with leak-free documents.
- **Opened**: [arXiv 2602.00758](https://arxiv.org/html/2602.00758), latest version (v2, 20 April 2026; the notes cite v1).
- **Table 2**, "Forecasting performance by document leakage level on 93 binary questions from 2025 with at least one score-4 document" (mean Brier): no retrieval 0.244; score 0, no post-cutoff information 0.242; scores 2–4 0.128; **scores 3–4 0.108**; score 4 only 0.129. The abstract rounds this to "Brier score 0.10 vs. 0.24 with leak-free documents".
- **Audit scale**: Google's `before:` filter on 393 questions (38,879 pages) and DuckDuckGo's date-range filter on 389 (34,454 pages); major post-cutoff leakage in at least one page for 71% and 81% of questions; answer directly revealed for 41% and 55%.
- **Qualifiers**: the 93 questions were selected for having a direct-leak document, and the 0.108 condition supplies only the strongly leaky documents (4.8 on average), so it measures the possible size of the inflation, not a typical pipeline. Questions come from Metaculus; the forecasting test uses Google-audited documents only; the same model is both leak judge and forecaster, which the authors list as a limitation.

### 4. Jia and Sun — CONFIRMED; numbers recorded

- **Notes say** (`copy_trading_smart_money.md` lines 65, 98, 146, 255): abstract only; "historical profitability does not necessarily translate into persistent trading advantages or profitable copy trading"; numbers not retrieved.
- **Opened**: [arXiv 2610.34754](https://arxiv.org/html/2610.34754), v1 of 26 October 2026, "Beyond Profit Rankings: Identifying, Understanding, and Evaluating Smart Money in Prediction Markets" (Huaiyu Jia, Shuo Sun). Not peer reviewed.
- **Profit concentration** (Figure 1): "Among 1,541,104 wallets, 68.66% exhibit negative PnL, whereas the top 1% account for 89.2% of total positive profits."
- **Persistence** (§4.2, Table 4): 1,101 candidate wallets, 3,207 weekly pairings, training 6–13 October 2026 and validation 13–20 October. Out-of-sample Brier for "profitable next week": base rate 0.2493, previous-week profit 0.2306, full model 0.2278 (AUC 0.681; 2,156 test observations). Excluding zero-PnL weeks: 0.2480, 0.2459, 0.2470 (AUC 0.577). Finding: "previously profitable wallets showing 2.63 times higher odds of remaining profitable in the following week. However, this advantage weakens after excluding zero-PnL observations, suggesting limited robustness."
- **Copy rule** (§4.5.1): fixed-size fill-or-kill limit orders of 1 USDC (live) or 1 paper dollar, submitted within 300 seconds of the source trade, entry price in [0.05, 0.95), at most 0.05 above the source price.
- **Results** (§4.5.2 and Table 6):

| Metric | Paper trading | Live on-chain |
|---|---|---|
| Period | 13–24 October 2026 | from 19 October 2026 |
| Entry candidates recorded | 2,896 | 1,384 |
| Orders submitted / filled | 713 / 283 (39.69%) | 20 / 20 |
| Entry cost | 693.46 | 20.36 USDC |
| Total PnL | +44.18 | **−3.04 USDC** |
| Fills above / equal / below the source price | 201 / 61 / 21 | 13 / 5 / 2 |
| Mean price gap per share | +0.01015 | +0.00619 |
| Median price gap per share | +0.01000 | +0.01000 |
| Median confirmation gap | not given | 112 seconds |
| 18 trades closed in both accounts | −3.23 | −3.19 |

- **Return on entry cost** (my calculation): paper +6.4%; live −14.9%.
- **Profit concentration in the paper account**: 44 larger trades made +75.73 and 239 smaller trades lost 31.55; one ETH trade made +56.07, and "excluding this trade reduces aggregate paper PnL to -11.89". That trade was not executed live because of a data-validity check.
- **Latency**: "Ten representative trades show confirmation gaps of 46–188 seconds. However, these intervals do not measure exact CLOB matching latency, and the observed price differences cannot be attributed solely to execution delay."
- **Conclusion**: "These results confirm the feasibility of real-time on-chain copy trading but do not establish consistent profitability." "copy-trading profitability depends on execution costs, position sizing, and payoff concentration rather than source-wallet performance alone."
- **Returns of the copied wallets**: no return series for the copied wallets over the test window is reported. Table 5 lists ten representative source wallets with platform-reported sector PnL: all ten were positive over the past month (about +$0.5k to +$552k), four of ten were negative over the past week and four of ten negative all-time.
- **Qualifiers**: tiny scale (20 live orders of $1); 12 days of paper trading and about 6 days live; one table note says some metrics still require "further computation"; the smart-money screen (180- and 90-day windows, positive PnL, profit factor ≥ 1.2) is described by the authors as not establishing "statistically significant predictive skill".

### 5. ForecastBench — CONFIRMED, both figures; reconciled

- **Notes say**: 69.2 vs 68.8 on 22 September 2026, from a Forecasting Research Institute post (`llm_forecasting_evidence.md` lines 23, 65–66); 69.5 vs 68.1 in data of 25 November 2026 (`residual_inefficiency_calibration.md` lines 172, 177).
- **Opened**: the institute's public leaderboard file `leaderboards/csv/leaderboard_tournament.csv` in [forecastbench-datasets](https://github.com/forecastingresearch/forecastbench-datasets) at three points in its nightly history: the commit of 22 September 2026 07:35 UTC (`c1360cb`), the commit of 24 September (`ed6110b`), and the head commit of 25 November 2026 17:20 UTC (`678d514`). The [forecastbench.org](https://www.forecastbench.org/) home page was also opened; it carries no numbers. The institute's post on X was not opened.
- **Figures** ("Overall" column, the difficulty-adjusted Brier Index; higher is better):

| Snapshot | Top AI entry | Superforecaster median | Leaderboard test "supers better than this entry?" | Entries |
|---|---|---|---|---|
| 22 Sep 2026 | Google DeepMind "fire hedgehog" **69.2** [67.9, 70.5], 845 questions | **68.8** [67.3, 70.5], tied rank 3, 578 forecasts | No, p = 0.65 | 377 |
| 24 Sep 2026 | same entry 69.1 [67.8, 70.4] | 68.8 [67.2, 70.4], rank 3 | No, p = 0.65 | 377 |
| 25 Nov 2026 | Anonymous 24 "model-4" **69.5** [68.0, 71.0], 607 questions | **68.1** [66.7, 69.7], rank 9, same 578 forecasts | No, p = 0.91 | 528 |

- **Who is ahead**: in both snapshots the top AI entry is nominally ahead of the superforecaster median (by 0.4 points on 22 September, by 1.4 on 25 November). In neither is the difference statistically significant: the intervals overlap. Calling it a tie is fair for both dates.
- **Why the numbers differ**: same metric, different dates. The superforecaster score fell from 68.8 to 68.1 with no new human forecasts (still 578), because the leaderboard is re-estimated nightly as questions resolve and entries are added, and the top entry changed from Google DeepMind's system (now 68.5) to an anonymous team's. The explanation of the mechanism is my reading of the file history, not a statement by the institute.
- **Qualifier**: on questions sourced from prediction markets the superforecasters are nominally ahead of the top-ranked entry at both dates (75.1 vs 74.1; 73.5 vs 71.3), but on only 57 questions.

### 6. KalshiBench, KellyBench, PolyBench — CONFIRMED; one KellyBench detail CORRECTED

**KalshiBench** — [arXiv 2512.16030](https://arxiv.org/html/2512.16030), v1, 17 December 2025, single author (Nel).
- Notes (`llm_forecasting_evidence.md` lines 106, 194): ECE 0.120 for Claude Opus 4.5 up to 0.395 for GPT-5.2-XHigh, without retrieval.
- Source: "All models exhibit substantial calibration errors, with ECE ranging from 0.120 to 0.395." "Only Claude Opus 4.5 achieves a positive Brier Skill Score (0.057)". GPT-5.2-XHigh: ECE 0.395, skill score −0.799.
- Qualifiers: 300 questions sampled from 1,531, resolving after 1 October 2025; five models; some categories have 1–4 questions. A search of the full text found no description of retrieval, web search or tool use, and the evaluation prompt contains only the question, so "without retrieval" is a fair description but is an inference, not the paper's wording.

**KellyBench** — [arXiv 2604.27865](https://arxiv.org/html/2604.27865), v1, 30 April 2026.
- Notes (`llm_forecasting_evidence.md` lines 57, 191): every model lost; bankrolls from £10,421 (Kimi K2.5) to £96,336 (Claude Opus 4.7); human quant +5.1%.
- Source: "All models lost money on average over five seeds on the 2023/24 English Premier League season, with the mean return on investment ranging from -89.6% (Kimi K2.5) to -7.9% (GPT-5.4). Only 3 out of 25 seeds achieved a positive return on investment".
- Table 2 (five models, five seeds each, £100,000 start): GPT-5.4 −7.9% (£92,063); Claude Opus 4.6 −11.2% (£88,771); GLM-5 −51.6% (£48,395); Gemini 3.1 Pro −66.0% (£34,029); Kimi K2.5 −89.6% (£10,421).
- Table 7: Human Quant **+5.1%** (39 bets, final £105,118); AI Researcher −4.3% (140 bets); Dixon–Coles model −15.4% (249 bets), which "beats 3/5 of the models evaluated".
- Correction: see item 3 in the corrections list. Three further models were run for three seeds in "an earlier version of this paper" and excluded, which matches the press count of eight.
- Qualifiers: a simulated backtest, not real money; bookmaker closing odds with about 5.3% overround; one season; the human quant is one person with a week to build a model, who "would be expected to lose money 38% of the time across those 39 bets". The authors: "The single-season setup restricts us from making overly strong conclusions".

**PolyBench** — [arXiv 2604.14199](https://arxiv.org/html/2604.14199), v1, 3 April 2026.
- Notes (`llm_forecasting_evidence.md` lines 53–54, 69): 5 of 7 models negative.
- Source (abstract): "only two of seven models achieve positive financial returns—MiMo-V2-Flash at 17.6% CWR and Gemini-3-Flash at 6.2% CWR—while the remaining five incur losses despite uniformly high stated confidence."
- Table 5 (base lot $10; confidence-weighted return): Gemini-3-Flash +6.2%; MiMo-V2-Flash +17.6%; Grok-4.1-Fast −12.1%; GPT-OSS-120B −17.8%; DeepSeek-V3.2 −11.4%; Trinity-Large −9.2%; MiniMax-M2.5 −25.2%. Average stated confidence 0.808–0.871 across all seven.
- Qualifiers: simulated fills against stored order-book snapshots (top five levels); no fees are modelled in the passages read; snapshots from 6–12 February 2026, settlements to 21 February; about 5,100 scoreable snapshots per model; per-trade Sharpe ratios of the two winners are 0.01 and 0.02, and their returns rest on a few long-shot wins of more than 1,000%; returns shrink as order size rises from $10 towards $1,000. The "Grok made about 33% on five bets" anecdote from a secondary write-up was not found in the paper's tables.

### 7. Mitts and Ofir; the 152-wallet study — PARTLY

**Mitts and Ofir, "From Iran to Taylor Swift"**
- Notes (`copy_trading_smart_money.md` line 211): about 93,000 markets, February 2024–February 2026; five-signal screen; 210,718 wallet-market pairs, 69.9% win rate; about $143M of realised profit, about $119M above what execution prices implied; 1,152 pairs account for $67.9M.
- **COULD NOT OPEN**: both SSRN abstract pages (6426778 and 7259741) were refused with HTTP 403.
- **Opened instead**: the authors' own summary on the [Harvard Law School Forum on Corporate Governance](https://corpgov.law.harvard.edu/2026/03/25/from-iran-to-taylor-swift-informed-trading-in-prediction-markets/), 25 March 2026, located with one web search.
- Source wording: "a systematic statistical screening of all Polymarket markets from February 2024 through February 2026—a universe of over 93,000 distinct markets and nearly 50,000 unique wallet addresses. The screening combines five signals—cross-sectional bet size, within-trader bet size, profitability, pre-event timing, and directional concentration—into a composite score". "across 210,718 suspicious wallet-market pairs, flagged traders achieved a 69.9% win rate". "We estimate approximately $143 million in aggregate anomalous profit across the study period. This figure is almost certainly a lower bound: the screening is buy-side only, excludes positions below $500".
- Not verified: the $119M and $67.9M / 1,152-pair figures, and anything changed in the 8 August 2026 revision.
- Qualifier: profitability is one of the five screening signals, so the flagged set is partly selected on outcome; the win rate and profit are not what a real-time alert would earn.

**Anti-Corruption Data Collective, "Classifying Insider Trading Risk"**
- Notes (`copy_trading_smart_money.md` line 212), from press only: 152 "Orca" wallets put $2M on military longshots, won 97.2% of the time and made $8M.
- **Opened**: the [original report PDF](https://acdatacollective.org/wp-content/uploads/2026/08/ACDC-Classifying-Insider-Trading-Risk.pdf) (August 2026; pages 02–06 read as page images because the text layer is not extractable), plus [Task & Purpose](https://taskandpurpose.com/news/polymarket-insider-bets-military/) and [Crypto Briefing](https://cryptobriefing.com/polymarket-wallets-military-insider-trading/).
- Source wording (Key Findings, p. 03): "There are only 152 Orca wallets who placed longshot bets in military and defense markets. Collectively, they won $8 million."
- **Detection method** (Box 1, p. 06): a longshot bet is a market price of 35 cents or lower and a bet size of at least $2,500 "cumulative over a 1-hour period"; a longshot wallet made at least one such bet. Wallets are then classed as Orcas, Whales, Bots or Small Fish "using the number of markets and topics they bet on, their overall success rate, and the timing of bets" (556, 3,278, 760 and 7,761 wallets).
- **Period and sample** (p. 05): "78,496 longshot bets and the 12,355 wallets that placed them, using data on all settled markets on Polymarket up to May 5, 2026."
- Other figures in the report: Orcas returned "an average of 132% compared to losses of 2% and 1%" for Whales and Bots; across all longshot bets the average price was 25 cents and the win rate 13.1%; only 42.7% of longshot wallets made money or broke even.
- Seen in press only (report pages 14–18 not read): the 97.2% win rate and the $2M staked.
- Qualifier: the classification uses each wallet's overall success rate, so it is after the fact. The report calls the 152 wallets "the most likely potential insiders" that "could be investigated by law enforcement to determine whether there are any true insiders"; it does not establish that they are insiders.

### 8. Columbia wash-trading study — CONFIRMED

- **Notes say** (`liquidity_capacity_competition_venues.md` lines 258, 261; `structural_arbitrage.md` lines 261, 278): about 25% of historical Polymarket volume; 45% of sports, 3% of crypto; revision of 17 January 2026.
- **Opened**: the paper itself, dated "January 17, 2026" (Sirolly, Ma, Kanoria, Sethi, "Network-Based Detection of Wash Trading"), in the [copy hosted by DeFi Rate](https://defirate.com/wp-content/uploads/2026/02/columbia-study-polymarket-wash-trading.pdf). The Columbia Business School page was refused (403).
- **Source wording** (introduction): "our algorithm classifies nearly 25% of Polymarket's historical volume as activity consistent with wash trading, and flags 14% of the 1.26 million wallets". The estimate "peaked at nearly 60% of total weekly exchange volume in December 2024, subsiding to less than 5% by May 2025 before resurging sharply to about 20% by early October 2025, the end of our sample period". "45% of all-time volume in Sports markets is classified by our algorithm as likely wash trading, compared to 17% in Election markets, 12% in Politics markets, and 3% in Crypto markets."
- **Qualifiers**: data cover all order-book trades "from November 21, 2022 through October 12, 2025" (67.7 million trades), so "historical" stops in October 2025 even in the January 2026 revision; "these results are estimates, as there is no definitive 'ground truth'"; working paper.

### 9. Bürgi, Deng and Whelan — PARTLY

- **Notes say** (`structural_arbitrage.md` lines 196, 225; `residual_inefficiency_calibration.md` line 31; `llm_forecasting_evidence.md` line 242): over 300,000 contracts; average return about −20% before fees and −22% after; takers about −32%, makers about −10%; favourite-longshot bias; bias shrinking over time.
- **COULD NOT OPEN**: the UCD file WP2025_19 (403); the CESifo PDF link (returned a bot-check page, not the paper); the authors' VoxEU column (403).
- **Opened**: the [George Washington University working paper 2026-001](https://www2.gwu.edu/~forcpgm/2026-001.pdf) (cover dated February 2026, paper dated January 2026, 45 pages). It may differ from the UCD version the notes cite.
- **Source wording**:
  - Introduction: "investors who buy contracts costing less than 10c lose over 60 percent of their money. In contrast, there is statistically significant evidence that contracts with prices above 50c earn a small positive rate of return." "there is some evidence that the bias in prices is diminishing over time. Overall, the average rate of return on Kalshi contracts is about minus 20%."
  - §3: "Prior to fees, Kalshi participants simply swap money, so by definition the average return prior to fees across the total volume of money invested is zero. However, the asymmetric pattern of returns on cheap and expensive contracts means the average pre-fee return on a Kalshi contract in our data is -20%."
  - §4 (after-fee returns): "The average return on contracts for Makers was -9.64% while for Takers it was -31.46%." "On average, Makers who buy contracts costing 50c and over earn a 2.6% rate of return."
- **Not found**: any "−22%" figure. The mean of the maker and taker after-fee averages, which cover 156,986 observations each, is −20.55% (my calculation).
- **Qualifiers**: sample from Kalshi's start in 2021 "through April 2025"; 46,282 distinct contracts in 12,403 events; contracts with at least $1,000 volume, final spread no wider than 20 cents, open at least 24 hours (hourly markets excluded); 313,972 price observations; under the fee schedule of that period only takers paid a fee of $0.07 × P × (1 − P) per contract, so the paper pre-dates the current fee regime.

### 10. Bartlett and O'Hara; Becker — CONFIRMED

**Bartlett and O'Hara, "Adverse Selection in Prediction Markets: Evidence from Kalshi"**
- Notes (`liquidity_capacity_competition_venues.md` lines 147, 231): makers won 63.4% of single-name contracts.
- Opened: the [NBER conference copy](https://conference.nber.org/conf_papers/f243677.pdf), "This version: July 2, 2026 (first version: April 16, 2026)".
- Source wording (introduction): "On single-name markets, the frequency edge is the maker's entire source of profit and then some: makers win on 63.4% of contracts, but when they lose, they lose more per contract (23.13 cents) than they earn when they win (16.34 cents)", for "a net profit of 1.91 cents per contract"; on broad-based markets "Makers earn 0.82 cents per contract".
- Qualifiers: 41.6 million trades in 478,167 markets, of which single-name markets are 15,516 markets and 3.0 million trades; sample "from July 2021 through March 11, 2026"; fees are not incorporated; politics, sports, entertainment and weather markets are excluded from the main analysis. Takers on single-name markets buy YES 60.9% of the time (volume-weighted) while 32.5% settle YES.

**Becker, "The Microstructure of Wealth Transfer in Prediction Markets"**
- Notes (`structural_arbitrage.md` lines 195, 226, 311; `residual_inefficiency_calibration.md` lines 32, 65): 72.1M Kalshi trades; takers −2.65% and makers +2.66% at 50 cents; negative taker returns at 80 of 99 price levels.
- Opened: the [author's own page](https://jbecker.dev/research/prediction-market-microstructure), dated 18 January 2026, which now opens. It notes that a formal version went on SSRN on 1 August 2026 (not opened).
- Source wording: "We analyzed 72.1 million trades covering $18.26 billion in volume". "At 50 cents, mispricing compresses; takers show -2.65%, and makers show +2.66%." "Takers exhibit negative excess returns at 80 of 99 price levels." Overall average excess return: taker −1.12%, maker +1.12%.
- Maker-taker gap by category (percentage points): finance 0.17; politics 1.02; sports 2.23; weather 2.57; crypto 2.69; entertainment 4.79; media 7.28; world events 7.32.
- Qualifiers: returns are "gross of platform fees"; resolved markets with at least $100 of volume; data to 25 November 2025; no trader identities, so maker and taker stand in for sophisticated and unsophisticated. The gap is recent: "From launch through 2023, taker returns averaged +2.0% while maker returns averaged -2.0%", and it flipped after the 2024 election. The 50-cent figure is where the gap is narrowest; self-published, not peer reviewed.

### 11. Gu et al., "When do prophets profit in prediction markets?" — CONFIRMED (cited); not re-opened

- **Notes say** (`residual_inefficiency_calibration.md` lines 186–187, 211): v3 of 23 September 2026; significantly positive profit-weighted score gaps against the market for five model variants; simulated, cost-free, market price in context.
- **Not opened in this pass.** The second-round entry is marked as a full-text read of [arXiv 2607.06166](https://arxiv.org/abs/2607.06166), so I cite it as instructed.
- **Figures recorded there**: gap in percent of capital spent, with intervals: Gemini 3.1 Pro (B) +11.7 [+2.4, +21.1]; Claude Fable 5 +12.3 [+3.2, +22.0]; Gemini 3.1 Pro (A) +8.7 [+3.3, +13.7]; GPT-5.6 Sol +10.9 [+1.0, +21.7]; Claude Sonnet 5 +10.2 [+0.2, +19.9]. Simulated returns +25.9% to +38.9%. Based on 94,453 forecasts by 18 model variants; the other 13 variants have negative gaps.
- **Caution on the qualifiers**: line 186 says the simulation uses "zero price impact and contemporaneous bid and ask prices", while line 211 summarises it as "no fees or price impact". Read together, the spread appears to be paid but fees and price impact are not. I did not verify this, or the statement that the market price is in the model's context, against the paper.

---

## Access log

| Source | Result |
|---|---|
| arXiv abstract and full-text pages for 2604.07355, 2510.17638, 2602.00758, 2610.34754, 2512.16030, 2604.27865, 2604.14199 | Opened |
| ICLR 2026 proceedings PDF (Prophet Arena) | Opened |
| ForecastBench leaderboard file at three commits; forecastbench.org home page | Opened |
| Harvard Law School Forum post by Mitts and Ofir | Opened |
| Anti-Corruption Data Collective report PDF | Opened (pages 02–06 read as images) |
| Columbia paper, copy hosted by DeFi Rate | Opened |
| Bürgi, Deng and Whelan, GWU working paper 2026-001 | Opened |
| Bartlett and O'Hara, NBER conference copy; Stanford Law page | Opened |
| Becker, jbecker.dev; KuCoin reprint | Opened |
| SSRN abstract pages 6426778 and 7259741 (Mitts and Ofir) | COULD NOT OPEN (403) |
| Columbia Business School research page | COULD NOT OPEN (403) |
| UCD working paper WP2025_19 | COULD NOT OPEN (403) |
| CESifo working paper 12122 PDF link | COULD NOT OPEN (bot-check page returned) |
| VoxEU column by Bürgi, Deng and Whelan | COULD NOT OPEN (403) |
| Forecasting Research Institute post on X; Prophet Arena live leaderboard; arXiv 2607.06166 | Not attempted |

Downloaded copies and extracted text are in the session scratchpad (temporary): `/tmp/claude-0/-home-user-hongjie-qiu/e1b14ff5-c349-500f-acaf-37657bee47dd/scratchpad/verify_papers_dl/` and `/tmp/claude-0/-home-user-hongjie-qiu/e1b14ff5-c349-500f-acaf-37657bee47dd/scratchpad/verify_papers_txt/`.

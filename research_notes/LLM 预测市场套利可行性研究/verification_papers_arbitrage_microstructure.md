# Verification log: arbitrage and microstructure papers

Status: COMPLETE (26 Nov 2026). Ten of the twelve sources were read in full text. Two SSRN papers could not be opened.

Scope: checks the key quantitative claims in `structural_arbitrage.md` and `event_driven_fast_reaction.md` against the original papers. A claim is marked CONFIRMED only when the figure was seen in the source itself in this session. "My calculation" marks any number derived here and not printed in the source.

Method: each arXiv paper was downloaded from `https://arxiv.org/abs/<id>` (abstract page) and `https://arxiv.org/pdf/<id>` (full text, converted with pdftotext). The four second-round files were searched first; none records a full-text read of any of the twelve sources, so every source was opened here. No web search was used.

## Summary table (corrections first)

| # | Claim in the notes | Status | Correct figure or key qualifier |
|---|---|---|---|
| 5 | NegRisk violations last about 8-16 s at the median (arXiv 2608.00666) | CORRECTED | The medians (16.15 s YES side, 7.99 s NO side) cover only 258 episodes with exact durations (253 YES, 5 NO). Another 366 of the 624 observed episodes (58.7%) lasted at least 50 minutes and were left out of the medians. The counts 2,098 and 36 are not the samples behind the medians. |
| 11 | Kalshi NBA underreaction; exploitability "not established" (Angelini and De Angelis) | CONFIRMED, one point CORRECTED | Underreaction confirmed (0.64-for-one at one minute; larger in thin markets). The paper does test exploitability: returns that buy at the ask and sell at the bid are negative at every gap size (Table 11). |
| 1d | Saguillo: dependent markets found with Linq-Embed-Mistral embeddings plus an LLM | CORRECTED (wording) | Linq-Embed-Mistral only sorts markets into seven topics. The dependency inference is done by the LLM DeepSeek-R1-Distill-Qwen-32B. |
| 1g | Saguillo: "14 of the 20 most profitable wallets were bots" (Substack) | CORRECTED (not in the paper) | The paper lists a top 10 and says only that some large players show "bot-like behaviour". Top account $2,009,631.76 over 4,049 transactions is confirmed. The top 10 hold about 20.7% of the total (my calculation). |
| 1f | Saguillo: accuracy of the LLM step | PARTLY | No accuracy figure for dependency detection. 81.45% is a single-market output-validity check; 92% is topic classification. Only 13 of 1,576 LLM-flagged pairs were valid (0.8%, my calculation). |
| 8 | Akey et al.: 99% of minutes without a trade carry 76% of price variation; trades explain at most 4%; top 1% of winners take 76.5% | PARTLY | Two different papers. The 76.5% figure, 2.4M users and Nov 2022-Mar 2026 are CONFIRMED in "Who Wins and Who Loses". The three microstructure figures are from a second paper (SSRN 7547106) that COULD NOT BE OPENED; they stay unverified. |
| 9 | Gómez-Cram et al.: about 3% skilled; under 3.5% of accounts take over 30% of gains; 44-46% persistence | PARTLY | Seen only in Yale SOM's write-up of the paper, not in the paper (SSRN not opened). That source gives 3%, "fewer than 3.5%" and "over 30%", 1.72M accounts, and 44% (not 46%), computed on a random split of each trader's events. |
| 3 | Gebele and Matthes: about 6% dual-listed; 2-4% deviations; human-validated 100,000+ events on ten venues | CONFIRMED with qualifiers | 6% = events with any cross-platform semantic relation (equivalent, subset or neg-risk), non-sports only. 2-4% = typical (median) gap among the most liquid constructions, from mid-quotes less modelled costs. Human validation = two samples of 1,000 pairs. |
| 1a | Saguillo: about $40M realised, April 2024-April 2025 | CONFIRMED | $39,587,585.02, markets resolved 1 Apr 2024-1 Apr 2025. No fees or gas deducted. Inferred from trade patterns within a one-hour window. |
| 1b | Saguillo: 41% of 17,218 conditions showed an opportunity | CONFIRMED | 7,051 of 17,218 (40.95%, my division). Single-condition (YES+NO) only, detected from average traded prices, not from simultaneous quotes. |
| 1c | Saguillo: split of the profit | CONFIRMED | Single condition $10.58M; within one NegRisk market $29.02M; cross-market combinatorial $0.095M. |
| 1e | Saguillo: 1,576 candidate pairs reduced to 13 | CONFIRMED | 46,360 pairs tested, 1,576 flagged dependent, 374 passed an automatic check, 13 valid after manual review. |
| 2 | Shi and Zhai: 1.9M relations, 255,000+ contracts, 3.5% a week, longer persistence where discovery is costly | CONFIRMED | Simulated order-book replay, 23 Jun-3 Aug 2026 (42 days). $2.50M on $11.1M peak capital is the upper bound; the lower bound is $1.10M. Text-derived relations supply 7% of the profit. |
| 4 | NBA study: 7 episodes in 173 games, median 3.6 s; 101 bps on about 15 shares | CONFIRMED | Sample 4 Feb-4 Mar 2026. Polling interval was 3.6-5.5 s, so 3.6 s is the sampling floor. Zero-fee assumption. Total capped profit for the month: $210 single-market, $560 combinatorial. |
| 6 | OpenMarket: 16 ms median lag; 347 ms after moves of 5 bps or more | CONFIRMED | 16 ms is an "apparent" figure with an unresolved offset of about ±99 ms. 347 ms is the median for the 4,272 of 15,148 large moves (28%) that had a matching quote change within 2 s. |
| 7 | Gebele and Matthes: 48-88% of the near-certainty gradient explained by settlement discounting | CONFIRMED | 47.8%, 60.2% and 87.6% under three discount curves; 56.4-92.9% on held-out events. |
| 12 | Lopez-Lira and Tang: 34 bps a day before costs; returns decline as LLM adoption rises | CONFIRMED | Sample Oct 2021-May 2024. Unprofitable at 20 bps per round trip. The decline is a time trend the authors call "suggestive evidence". |
| 10 | Valentin: post-release convergence trade loses 72-82% of stake | COULD NOT OPEN | SSRN only. Figures stay at search-snippet level. |

## What the report should change

1. Do not describe NegRisk violation lifetimes as "8-16 seconds". In arXiv 2608.00666, most observed violation episodes (58.7%) lasted at least 50 minutes; the 8-16 s medians describe the short-lived minority, and the 8 s figure rests on five episodes.
2. The Kalshi NBA drift is not tradable on the paper's own test: buying at the ask and selling at the bid loses money at every threshold.
3. The 3.5% a week in Shi and Zhai is a simulated upper bound for a trader who takes all displayed depth with no delay. With a one-second delay, 22% of orders lose money at resolution. Relations read from contract text (parsers plus LLMs) supply 7% of the simulated profit.
4. In Saguillo et al., the embedding model does not detect dependencies. It only groups markets by topic. The LLM flagged 1,576 pairs and 13 survived, so its "dependent" label was right less than 1% of the time.
5. The OpenMarket 347 ms figure is conditional on a response being seen within two seconds, which happened for 28% of large Binance moves.
6. Akey et al. are two papers. The profit-concentration numbers are verified. The quote-driven price-discovery numbers (99%, 76%, 4%) are not, and the unverified 76% should not be confused with the verified 76.5%.
7. For Gómez-Cram et al., cite 44% and say it comes from a random split of each trader's events. The 46% variant and the exact 3.16% share were not seen in any source opened here.
8. Valentin's 72-82% loss is unverified.
9. The NBA study assumes zero trading fees for a sample that runs to 4 March 2026, whereas the notes date Polymarket sports fees from 18 February 2026. Either the fee date is wrong for NBA game markets or the paper's edge is overstated for the later half of its sample. This log could not resolve it.

## Access record

| Source | Result |
|---|---|
| arxiv.org abstract and PDF pages for 2508.03474, 2610.23517, 2601.01706, 2605.00864, 2608.00666, 2607.26245, 2605.31431, 2606.07811, 2304.07619 | HTTP 200, all read |
| arxiv.org/html/2608.00666v1 | HTTP 200 (used to check garbled sentences) |
| osc.ca PDF of Akey et al., "Who Wins and Who Loses" | HTTP 200, read |
| insights.som.yale.edu article on Gómez-Cram et al. | HTTP 200, read |
| cepr.org/publications/dp21615 | HTTP 403 (challenge page). Not retried. |
| papers.ssrn.com abstract 7547106 | HTTP 403 (challenge page). Not retried. |
| papers.ssrn.com abstracts 6617059, 7234098, 6443103 | Not requested, because SSRN had just refused the first request. |

Downloaded copies are in `/tmp/claude-0/-home-user-hongjie-qiu/e1b14ff5-c349-500f-acaf-37657bee47dd/scratchpad/verify_dl/` (scratch space, may be cleared).

## Entries

### Claim 1. Saguillo, Ghafouri, Kiffer and Suarez-Tangil, "Unravelling the Probabilistic Forest: Arbitrage in Prediction Markets" (arXiv 2508.03474)

- URL opened: https://arxiv.org/abs/2508.03474 and https://arxiv.org/pdf/2508.03474 (v1, 5 Aug 2025; the only version).
- Nature of the evidence: independent academic measurement (IMDEA Networks, supported by a Flashbots research grant). Realised, after the fact, from executed trades on chain. Before costs.

**1a. About $40M of realised arbitrage, April 2024-April 2025. CONFIRMED.**
- Notes (structural_arbitrage.md lines 27 and 302): "estimate about $40 million of realized profit across both"; "about $40M on Polymarket, April 2024 – April 2025, overwhelmingly within-market".
- Abstract: "We find a realized estimate of 40 million USD of profit extracted across both types of arbitrage".
- Section 7.4: "The combined amount extracted from all strategies presented totals $39,587,585.02, assuming an ε = $1 profit per trade."
- Section 1.1: "Our data collection efforts span markets that were resolved over the period of one year, from April 1, 2024, to April 1, 2025." The window is defined by resolution date.
- Qualifiers (Section 7.1):
  - Bids below $2.00 are dropped.
  - All executed bids from one address "within a time window T" of "950 blocks (approx. 1 hour)" are treated as one opportunity. Profit is "the minimum amount of tokens held across all positions minus the price to acquire the positions". So this is a pattern-based estimate: any address that assembled a complete set within about an hour at a combined price away from $1 is counted.
  - "we do not take into account the fees because Polymarket currently does not charge per trade executed." No gas cost is deducted either.
  - Execution is non-atomic (footnote 11: "there is some inherent risk to attempting arbitrage").

**1b. 41% of 17,218 conditions showed an opportunity; median profit about $0.60 per dollar. CONFIRMED, with qualifiers.**
- Notes (line 28, from alphaXiv): "7,051 of 17,218 conditions (41%) showed at least one arbitrage opportunity, with a median profit of about $0.60 per dollar invested."
- Section 4.1: "totalling 17218 conditions across all markets".
- Section 6.1: "our data set consists of 17.2K conditions (8.56K from NegRisk and 8.66K from Single markets), of these 7,051 conditions have at least one arbitrage opportunity within our parameters (2,628 NegRisk, 4,423 Single)".
- The paper does not print "41%". 7,051 / 17,218 = 40.95% (my division).
- This count is for single-condition (YES plus NO) opportunities only. For multi-condition markets, Section 6.2 says: "Of the 1578 NegRisk markets, 662 had at least one arbitrage opportunity."
- How an "opportunity" is detected (Section 6): prices are volume-weighted averages of executed bids per block, "carrying forward the last known price for up to 5K blocks (2.5 hours) if a token isn't traded", and only while no token is above $0.95. These are inconsistencies in traded prices, not two quotes available at the same instant.
- The minimum-profit threshold is stated inconsistently in the paper: "at least $0.05 on the dollar" in the text of Section 6, but "|1 − VWAP Sum| > 0.02" and "our 2 cents bound" in the captions of Figures 5 and 6.
- Median: "We see the median price of the sum of conditions (i.e., profit per Dollar) is around $0.60 for all topics of markets". The notes' wording matches. Given the stale-price construction, it should not be read as a 60% executable return.
- Figure 10 caption: "About 1% of our estimated U.S. election opportunities were exploited by users."

**1c. Split of the profit. CONFIRMED.**
- Notes (line 52, marked "unverified recollection"): single-condition roughly $10.6M ($5.9M buying, $4.7M selling); NegRisk rebalancing roughly $29M (all NO $17.3M, all YES $11.1M); combinatorial about $0.1M.

| Type | Source wording | Amount |
|---|---|---|
| Single condition, buy YES+NO below $1 | Section 7.2: "the total profit from buying below one dollar amounts to $5,899,287.427" | $5.90M |
| Single condition, sell above $1 | Section 7.2: "the total profit from selling above one dollar is $4,682,074.77" | $4.68M |
| Within one NegRisk market, buy all NO | Section 7.3: "buying "NO" $17,307,113.81" | $17.31M |
| Within one NegRisk market, buy all YES | Section 7.3: "buying "YES" $11,092,286.31" | $11.09M |
| Within one NegRisk market, selling | Section 7.3: "selling "YES" $612,188.83, selling "NO" $4,264.33" | $0.62M |
| Combinatorial, across dependent market pairs | Section 7.3: "pair 2, $60,236.71; pair 4, $18,472.31; pair 1, $15,818.53; pair 3 $629.16" | $0.095M |

- Subtotals (my sums): single condition $10,581,362 (about 27%); within one NegRisk market $29,015,853 (about 73%); combinatorial $95,157 (about 0.24%).
- The paper's terms: "Market Rebalancing Arbitrage" covers the first two groups and "Combinatorial Arbitrage" the third.
- The components add up to $39,692,372, which is $104,787 (0.26%) more than the stated total of $39,587,585.02. The paper does not explain the difference.
- The paper says value extraction was found "in 5 cases" among the 11 NegRisk-NegRisk pairs but lists four amounts.

**1d. Method: Linq-Embed-Mistral embeddings plus an LLM. CORRECTED (wording).**
- Notes (line 66): "then use text embeddings (Linq-Embed-Mistral) and LLMs to extract logical dependencies from market condition descriptions."
- Section 4.1.1: "We first use Linq-Embed-Mistral model [1] to generate vector embeddings for both market questions and topics ... and assign the question to the topic with the highest similarity." The seven topics are Politics, Economy, Technology, Crypto, Twitter, Culture and Sports. Validation: "we randomly sampled 100 instances from the dataset and manually labeled them which yielded an accuracy of 92%."
- Roadmap list before Section 4.1 (item i): "we employ an instance of the LLM DeepSeek-R1-Distill-Qwen-32B [4] together with market description data to capture the state space of possible market resolutions to then infer semantic dependency between pairs of markets and their conditions."
- Section 5.2: pairs are compared only "within the same topic group in the same day" (same end date). Markets with more than four conditions are cut to the four with most volume plus a catch-all fifth.
- Correct wording: embeddings are used to group markets by topic, which shrinks the search space; the open-weight reasoning LLM does the dependency inference by listing the possible joint outcomes as JSON.

**1e. 1,576 candidate pairs reduced to 13 valid ones. CONFIRMED.**
- Notes (lines 67-68): "13 semantically dependent pairs, all tied to the 2024 U.S. presidential election"; "1,576 candidate dependent market pairs".
- Section 5.2, US election group ("Politics" with end date 5 November 2024): "we have 128 NegRisk and 177 Single markets. We run all 46360 pairs of markets, we get that 353 do not return a JSON, and 4374 returned an output which does not satisfy (ii) or (iii). In the end, we get a total of 40057 independent markets and 1576 markets characterized as dependent."
- An automatic check of the arbitrage definition left 374 pairs. "We manually check these 374 pairs and get 11 NegRisk-NegRisk and 2 NegRisk-Single pairs, which satisfy our Combinatorial Arbitrage definition."
- All 13 belong to the 2024 US election group. Outside it: "Of the 2267 pairs of markets checked ... 2033 pairs were classified as independent, and 1 pair in this set was classified as dependent", and that one pair did not strictly meet the definition.
- Causes of false positives: "pairs of markets with some weaker notion of dependency ... or the LLMs conflating U.S. election outcomes". "Eight markets contributed to 1469 invalid pairs, largely due to their own inherent ambiguity".
- The breakdown of the 374 as printed ("4 NegRisk-NegRisk, 94 Single-Sigle, and 276 NegRisk-Sigle") cannot be squared with 11 NegRisk-NegRisk pairs surviving. This looks like a labelling slip in the paper.

**1f. Any stated accuracy of the LLM step. PARTLY.**
- The paper gives no precision or recall for dependency detection.
- Single-market sanity check (Section 5, before subsection 5.2): "out of the 128 markets tested, only 4 do not return a valid JSON, with 101 (81.45% ) fulfilling all conditions". 101 / 124 = 81.45%, so the percentage is of the 124 valid outputs. This tests whether the LLM lists a market's own outcomes correctly.
- Implied precision of the "dependent" label: 13 / 1,576 = 0.8%, or 13 / 374 = 3.5% after the automatic check (my calculations). Recall was not measured: the 40,057 pairs labelled independent were not audited.
- Conclusion section: "Some limitations in the reasoning of the LLM for certain types of markets (e.g., reasoning loops we encountered) underscore the need for future enhancements".

**1g. Concentration among top arbitrageurs. CONFIRMED for the top account; the Substack "14 of 20 bots" claim is NOT in the paper.**
- Notes (lines 29 and 52): "roughly 14 of the 20 most profitable wallets were bots" (Substack); "top arbitrageur about $2.0M over about 4,049 trades".
- Table 1, rank 1: "$2,009,631.76" and "4,049" transactions. Section 7.4: "The user with the highest profits generated a total of $2,009,631.76 through these strategies."
- Table 1 lists ten accounts, from $2.01M down to $383,569.94. Their sum is $8,184,861, or 20.7% of the $39.59M total; the top three hold 11.0% (my calculations). The paper states no concentration share.
- On bots the paper says only: "We see some very big players with bot-like behaviour in the number of bids they participate in." There is no top-20 list and no bot count.
- "86 million" is confirmed, as bids: "In Appendix I.1 we summarize the set of 86 million bids."

### Claim 2. Shi and Zhai, "Combinatorial Arbitrage in Prediction Markets" (arXiv 2610.23517)

- URL opened: https://arxiv.org/abs/2610.23517 and https://arxiv.org/pdf/2610.23517 (v4, 25 Oct 2026; v1 was 16 Oct 2026; 47 pages).
- Notes (structural_arbitrage.md lines 70, 71 and 305): "recover 1.9 million logical relations covering more than 255,000 contracts"; "an ideal arbitrageur that takes the full displayed depth of every opportunity and recycles capital at resolution earns a risk-free return of 3.5% a week after spreads and fees"; opportunities "persist longer and attract less observed participation where relation discovery and execution are more costly"; "Sample period not retrieved."
- Nature of the evidence: independent academic paper. Simulated: a replay of recorded full-depth Polymarket order books. Not realised trading. After spreads and fees.
- Sample (Section 2.2): "The record covers 23 June to 3 August 2026, and over these 42 days we observe roughly 745,000 binary contracts, 73.22 billion order-book messages". Polymarket only.

**2a. 1.9M logical relations over 255,000+ contracts. CONFIRMED.**
- Introduction: "we recover 1.9 million relations and reduce them to about 570,000 relations covering more than 255,000 contracts".
- Section 4: "the 1,942,133 relations the three layers recover, including the ones implied by others; ... the 573,024 relations of the reduced system".
- Three layers: venue-asserted (Polymarket's own negative-risk groups), venue-derived (sports match fields), and semantic-inferred (read from contract text "by structured parsers or by large language models"). "sports accounts for 453,190 relations and crypto for 89,088, together representing 94.6% of the total".
- LLM step (Section 4):
  - A word-overlap pre-screen "cuts 277 billion possible pairs to 704,450 candidate pairs and 13,894 candidate groups".
  - Five open-weight models propose relations (Qwen3-32B, Qwen3-235B-A22B, Llama-4-Maverick, DeepSeek-V4-Flash, GLM-5.2).
  - "every LLM proposal is reviewed by two audit models: Claude Fable 5.1 (Anthropic, 2026) and GPT-5.6 Sol (OpenAI, 2026a)—later supplemented by GPT-6 Astra". "We retain a proposal only when both auditors agree on its type and direction".
  - Table 3, union of proposals: 239,653 pairwise relations proposed, 102,288 (42.7%) confirmed by both auditors; 23,519 multivariate units proposed, 1,153 (4.9%) confirmed. By model, confirmation runs from 18.8% (Llama-4-Maverick) to 64.6% (GLM-5.2).
  - "Layer 3 contributes 118,792 relations after deduplication across the dual-audited LLM outputs of Table 3 and the outputs of the numeric and temporal parsers."
  - No human-labelled accuracy is reported for the LLM relations. The check is agreement between two frontier models, plus the fact that "no settled window in any layer has a profit at resolution below its guaranteed profit" (footnote 14).
  - Appendix B: an audit on 22 September 2026 "identified six parser-generated relations that incorrectly imposed exhaustiveness"; 97 executed windows were removed, of which "82 had settled at a profit ... illustrating why profitable settlement does not validate an ex-ante guarantee."

**2b. 3.5% a week for an idealised arbitrageur after spreads and fees. CONFIRMED.**
- Abstract: "Among settled portfolios, an ideal arbitrageur that takes the full displayed depth of every opportunity and reuses its capital at resolution earns a risk-free return of 3.5% a week after spreads and fees."
- Section 5, Table 5 discussion: "Within the settled sample, the accumulated take is $2.50 million in profit on $113.7 million of capital committed—a guaranteed return of 2.2%, and 3.5% a week on the $11.1 million outstanding at the peak. The first take totals $1.10 million of this profit on $40.6 million of capital".
- Upper and lower bounds (Section 5, simulation steps): "we use the first take as a lower bound, assuming no further execution within the window, and the accumulated take as an upper bound, assuming subsequent quotes remain as observed." The 3.5% a week belongs to the upper bound.
- Scale: "Of the 491,827 arbitrage windows previously detected, we find 125,095 executed windows"; "89.8% of executed windows have settled on every filled leg."
- By layer: "venue-asserted and venue-derived relations contribute 34% and 59% of the guaranteed profit of the accumulated take, respectively. Semantic-inferred relations account for the remaining 7%." Table 5 shows the semantic-inferred layer at $179 thousand of guaranteed profit on $12,089 thousand of capital committed (1.5%).
- "The median window guarantees 0.5% on capital, but half of the accumulated take comes from windows with guaranteed returns above 6.5%".

**2c. Gaps persist longer where relation discovery is costly. CONFIRMED.**
- Introduction: "Among the windows that last at least 0.3 seconds, the median duration is 2.9 seconds for venue-asserted relations, 6.3 seconds for venue-derived relations, and about 31 seconds for semantic-inferred relations."
- Table 7, executed windows of at least 0.3 s: parsers 9,489 windows, median 32.0 s; LLMs 4,798 windows, median 29.0 s, 75th percentile 270.7 s, 61% last 10 s or more.
- "Windows that last less than 0.3 seconds account for 47% of executed windows but only 8% of the accumulated take."
- With controls: "relative to venue-asserted windows, venue-derived windows last about 2 times as long and semantic-inferred windows about 10 times as long."
- Observed participation (Table 8): at least one address traded every leg in the arbitrage direction in 44.1% of venue-asserted executed windows, 14.5% of venue-derived and 8.8% of semantic-inferred. "Within this layer, 10.4% of parser windows have a matched trade, but only 4.2% of LLM windows."
- Those who do trade are fast and few: "the median lag from the opening of a window is about 2.6 seconds"; "854 addresses make these trades, and the 10 most active ones account for 78% of the windows with such a trade."
- The authors read this as "consistent with both discovery and execution costs limiting arbitrage"; they do not separate the two.

**2d. Capacity and realism (Section 5, Table 6 discussion).**
- "Of course, such an ideal arbitrageur does not exist, and a real arbitrageur is subject to frictions in liquidity and execution."
- Capacity: all displayed depth for six weeks produced $2.50M on $11.1M of peak capital. "Across valid two-sided quote states, the pooled median spread is 8.0 cents, and median depth is 40 shares at the best bid and 30 shares at the best ask."
- Order delay (Table 6, Panel B): "With a 1-second delay, 54% of the orders fill in full and the orders fill 84% of the submitted quantity; the settled orders pay 79% of the profit at resolution that the same orders pay in the baseline, and 22% of them lose money at resolution." At 100 ms: 91.4% of baseline profit, 14.2% of orders with a loss. A portfolio "whose legs fill unequally no longer has a guaranteed profit".
- Partial participation: "at 50% participation, the accumulated take retains 57% of its baseline value".
- Capital lock-up: the median holding period is "about 3 hours for venue-derived portfolios and 7 days for semantic-inferred portfolios".
- Not modelled: other traders' reactions to the arbitrageur's orders (the upper bound assumes "subsequent quotes remain as observed").

### Claim 3. Gebele and Matthes, "Semantic Non-Fungibility and Violations of the Law of One Price in Prediction Markets" (arXiv 2601.01706)

- URL opened: https://arxiv.org/abs/2601.01706 and https://arxiv.org/pdf/2601.01706 (v1, 5 Jan 2026).
- Notes (structural_arbitrage.md lines 100 and 306): first human-validated cross-platform dataset, "over 100,000 events across ten venues, 2018–2025"; "About 6% of events are concurrently listed"; "persistent execution-aware price deviations of 2–4% on average, even in highly liquid settings".
- Status: CONFIRMED (all three figures appear in the abstract as quoted), with qualifiers from the body.
- Abstract: "covering over 100 000 events across ten major venues from 2018 to 2025 ... roughly 6% of all events are concurrently listed across platforms and that semantically equivalent markets exhibit persistent execution-aware price deviations of 2-4% on average, even in highly liquid and information-rich settings."

Qualifiers:
- Dataset (Section 4.1): 102,275 events from "Polymarket, Omen/Presagio, Augur v1, Limitless, Myriad, Seer, Truemarkets, Kalshi, Futuur, and PredictIt". Data run "through August 15–22, 2025". "We restrict the analysis to non-sports markets".
- What 6% counts (Section 5.1): "Out of 102,275 events, our semantic-matching pipeline identifies approximately 6% events that are involved in at least one cross-platform semantic relation." The relations are "1,501 equivalence classes comprising 6,709 relations, 1,645 subset-related event sets comprising 6,421 relations, and 1,123 negative-risk constructions". So 6% includes subset and neg-risk links, not only identical listings. These events are "nearly 10% of total event-days".
- What 2-4% is (Section 5.4): "Median deviations are smaller but systematically positive: even among the most liquid constructions, prices typically remain 2–4% away from execution-adjusted parity."
  - The price analysis "covers 7 out of the 10 platforms".
  - Prices are mid-quotes for order-book venues, adjusted by a modelled cost term that "aggregates bid–ask spreads, platform fees, gas costs, and tick-size constraints", using "platform-specific fees and typical bid–ask spreads". This is not executable depth and not realised profit.
- Human validation (Section 4.4): "one human annotator independently labeled a stratified sample of 1,000 candidate pairs" (agreement "effectively perfect", but the sample is "heavily skewed toward true negatives") and "1,000 verification-stage instances" (κ = 0.94). "LLM-based logical verification reduces the false-positive rate to below 2%." The 100,000 events were not individually checked by people.
- Matching pipeline: OpenAI text-embedding-3-large for retrieval, then two LLM passes; "on the order of 200 million tokens across all LLM calls".
- Persistence (Section 5.4): two groups of pairs, one where an execution-aware arbitrage exists nearly the whole overlap period and one near zero where "execution costs—most notably platform fees on venues such as Futuur—fully absorb nominal price differences".
- Simulated strategy (Section 5.4): entering the single highest-yield equivalent-market arbitrage and holding to resolution "yields a cumulative return of 1,218.66% over 800 days, across 15 completed trades." Backtest; 15 trades; no size or capacity given.
- 2024 election case (Section 5.5): Polymarket versus Kalshi, where the Polymarket contract is a "strict superset" of Kalshi's (not identical): "execution-adjusted spreads average approximately $0.03 and reach up to $0.07 for sustained intervals."

### Claim 4. Cheng, Yang and Zou, "Arbitrage Analysis in Polymarket NBA Markets" (arXiv 2605.00864)

- URL opened: https://arxiv.org/abs/2605.00864 and https://arxiv.org/pdf/2605.00864 (v1, 22 Apr 2026).
- Notes (structural_arbitrage.md lines 30, 72 and 303): "only 7 executable in-game episodes, median duration 3.6 seconds"; "median return 101 basis points; 76.9% of opportunities limited to an average executable size of 14.8 shares"; sample period "not retrievable".
- Status: CONFIRMED.
- Sample: "173 NBA games between February 4, 2026, and March 4, 2026". Limitations section: "The dataset spans a single month (February 4 to March 4, 2026) and is restricted to NBA game markets."
- Single market (Table 3 and Conclusion): "only 7 valid in-game episodes were identified across 3,042 markets, persisting for a median of just 3.6 seconds". Table 3: 7 in-game episodes, 0 pre-game, median duration 3.614 s, capped profit $210.19 (cap of $100 per episode), uncapped $4,418.44.
- Combinatorial: "We evaluated 8.59 million discrete combinatorial market states, detecting 523 candidate arbitrage episodes. After excluding 233 un-executable post-game artifacts, the final dataset yielded 290 active, executable episodes". 279 in-game (median duration 16.0 s), 11 pre-game.
- Return and size (Table 7): "Across 290 active episodes, the aggregate capped profit was $559.59. While the median yield of 101.01 basis points ... In 76.9% of all episodes, the $100 budget could not be fully deployed, with the average executable size restricted to approximately 14.79 synthetic shares." Uncapped theoretical profit $2,032.75. The "Middle" jackpot never occurred.

Qualifiers:
- Sampling floor: "fetching the complete state across all active NBA markets requires a polling cycle of 3.6 to 5.5 seconds." The 3.6 s median equals the polling interval. Limitations: "The frequencies reported therefore represent a conservative lower bound on true market inefficiency, and the measured durations an upper bound on actual lifespans." This confirms the notes' remark that snapshot data may overstate lifespans.
- Fees (Appendix A): "Because Polymarket currently imposes zero trading fees on NBA markets, the raw mathematical threshold of Profit > $0.00 was maintained". Gas is not deducted. This conflicts with the notes' fee timeline (sports fees from 18 February 2026, inside the sample). Not resolved here.
- Top-of-book depth only, minimum $10 on the thinner leg, one month, one sport.
- Spreads (Table 2): median bid-ask spread 392.20 bps pre-game and 1,030.90 bps in-game.

### Claim 5. Gebele, Mutzel and Matthes, "Executable Arbitrage and Market Efficiency in Prediction Markets" (arXiv 2608.00666)

- URL opened: https://arxiv.org/abs/2608.00666, https://arxiv.org/pdf/2608.00666 and https://arxiv.org/html/2608.00666v1 (v1, 1 Aug 2026).
- Notes (structural_arbitrage.md lines 32 and 304, from a Substack recap): "2,098 YES-side violations with a median duration of 16.15 seconds versus 36 NO-side violations with a median of 7.99 seconds"; "the sample period was not retrievable".
- Status: CORRECTED. The four numbers are in the paper, but the recap joined counts and medians that belong to different samples, and left out that most observed episodes were long-lived.

What the paper says:
- Section 5.1 (counts): "In the CLOB sample, by contrast, positive episodes are overwhelmingly concentrated on the YES side: we observe 2,098 positive YES-side episodes but only 36 positive NO-side episodes."
- Section 5.2 (durations): "CLOB persistence is more difficult to assess under the hour-stratified sampling design. Of the 624 observed episodes, 366 (58.7%) [are observed in both the first and final five minutes of their observation window]. Their exact durations are unknown, but they must exceed 50 minutes. We therefore classify them as window-spanning and exclude them from the exact-duration survival curves." (The bracketed words are garbled in both the PDF text and the HTML; the meaning is fixed by Section 4.3, which defines window-spanning episodes that way.)
- Section 5.2, continued: "Among the remaining 258 episodes, observed durations generally remain below 50 minutes. The median is 16.15 seconds for the 253 YES-side episodes and 7.99 seconds for the five NO-side episodes. ... the extremely small NO-side sample does not support a reliable distributional comparison. Moreover, episode closure indicates only that the violation disappeared; it does not establish that an arbitrage trade caused the closure."
- The passages read do not reconcile the 2,134 positive episodes of Section 5.1 with the "624 observed episodes" of Section 5.2, and do not give the side split of the 366 long episodes.

Correct wording for the report: in hour-long order-book windows from 14 April to 19 May 2026, 58.7% of observed NegRisk violation episodes lasted at least 50 minutes. Among the 258 shorter ones, the median was 16.15 s on the YES side (253 episodes) and 7.99 s on the NO side (5 episodes). Positive violations are concentrated on the YES side, which the adapter cannot convert before settlement, so closing one means holding a basket until resolution.

Other qualifiers:
- Sample (Section 4.1): three separate panels.
  - Old FPMM regime: 51 outcome sets, 235 binary markets, about 53,000 trades.
  - Transactions: "32,702 Polymarket events and 259 million trades for events listed through 31 December 2025".
  - Level-2 order books: "a separate hour-stratified observation period from 14 April 2026 00:00 UTC to 19 May 2026 06:00 UTC".
- Realised profit (Section 5.3; fees included, gas omitted "because the relevant transactions are routed through Polymarket's relayer"): "approximately 1.118 million USDC in mechanism-linked profit. Converter-enabled arbitrage accounts for approximately 1.086 million USDC, while settlement-based basket formation accounts for 32,283 USDC." This confirms the $1.12M total and the 5,185 USDC FPMM benchmark quoted in the notes.
- Trend in profit per conversion (Section 5.3): "Through July 2024, median profit is approximately one USDC per conversion ... During late 2024 and 2025, the median declines to approximately 0.20 USDC ... By early 2026, median profit falls further to approximately 0.08 USDC", which the authors call "consistent with intensifying competition".

### Claim 6. Young, "OpenMarket: A Synchronized Polymarket-Binance Dataset for High-Frequency Prediction-Market Research" (arXiv 2607.26245)

- URL opened: https://arxiv.org/abs/2607.26245 and https://arxiv.org/pdf/2607.26245 (v1, 28 Jul 2026; single author; a data release).
- Notes (structural_arbitrage.md lines 164 and 308): 727,098,247 rows; 54 Polymarket days between 12 Feb and 15 May 2026; about 2.9 million lead-lag pairs; "an apparent 16 ms median lag", stable at about 16-19 ms with heavy tails; "Polymarket quotes responding to Binance moves of at least 5 basis points after a median 347 ms".
- Status: CONFIRMED.
- Abstract: "727,098,247 deduplicated rows across 202 archival snapshots, with event data on 54 observed Polymarket days (57 Binance days) between 2026-02-12 and 2026-05-15, including 2,936,031 explicit lead-lag pairs".
- 16 ms (Sections 5.2 and 10.2): "an apparent 16 ms median lag on venue source clocks". "Lead–lag pairs exhibit a compact apparent median (16 ms on venue source clocks) but heavy tails (5th/95th: -186 / 316 ms; Figure 5)." "Stratifying by |price_delta_bps| quintiles shows stable median lead–lag (16–19 ms)".
- 347 ms (Section 5.2): "we detect 15,148 large Binance moves (≥5 bps within 1 s) and match 4,272 of them to the first directionally consistent Polymarket UP-token best-bid change (≥1 tick) within 2 s. Measured entirely on the collector's single ingest clock ... the median quote response lag is 347 ms".

Qualifiers:
- The 16 ms figure is not an absolute latency: "The observed minimum-delay envelopes imply a conservative single-vantage ambiguity of roughly ±99 ms for source-clock lead–lag values, so the 16 ms median should be read as an apparent source-clock median rather than an absolute cross-venue latency."
- The 347 ms median is conditional. Only 4,272 of 15,148 large moves (28.2%, my division) had a matching one-tick change of the best bid within 2 s. It measures the first one-tick move, not full repricing.
- Scope: Polymarket BTC 15-minute markets against Binance BTC/USDT; one collector host.
- The paper's main result is a null (abstract): "out-of-sample, a walk-forward logistic model over 43 microstructure features does not beat, and slightly underperforms, the probability already implied by Polymarket's own order book, and simulated trading nets -0.116 normalized payoff units per attempted trade under stated fee and slippage assumptions". The body gives the assumptions as "1% fees and 0.5% slippage". Out-of-sample AUC is 0.8377 for the model against 0.8405 for the market mid.

### Claim 7. Gebele and Matthes, "When Certainty Is Not Worth It: Capital Lock-Up and Settlement Discounting in Prediction Markets" (arXiv 2605.31431)

- URL opened: https://arxiv.org/abs/2605.31431 and https://arxiv.org/pdf/2605.31431 (v1, 29 May 2026).
- Notes (structural_arbitrage.md lines 240 and 312; event_driven_fast_reaction.md line 165): "Adjusting prices for these discount curves removes about 48–88% of the near-certainty horizon gradient"; "$1,000 of NO at the observed price earns roughly 4.2%, but only after locking capital for most of a year".
- Status: CONFIRMED.
- Section 5.2: "Thus discount adjustment reduces the horizon gradient by roughly 48–88%, depending on the lower-tail frontier".
- Table 3 ("154,298 observations across 4,273 market clusters", prices of 0.9 or more, NegRisk markets excluded):

| Discount curve | Mean annualised wedge | Slope reduction | p-value of remaining slope |
|---|---|---|---|
| Minimum frontier | 3.06% | 47.8% | 0.0079 |
| 0.1-percentile frontier | 4.36% | 60.2% | 0.0425 |
| 0.5-percentile frontier | 6.89% | 87.6% | 0.5285 |

- Held-out check: "Event-level 5-fold cross-fitting ... Held-out slope reductions remain large (56.4–92.9%)".
- Illustration (Introduction, the "Will Jesus Christ return in 2025?" market): "for months, the complementary near-certain NO side traded around $0.96. A trader buying $1,000 of NO at that price would earn roughly 4.2% if the position paid $1 at settlement, but only after locking capital for most of the year."

Qualifiers:
- What shrinks is the slope of the gap between outcome and price against time to settlement, for prices of 0.9 or more. "Mostly a settlement discount" (line 312) overstates the lower end; "about half to nearly all of the maturity gradient" is closer.
- Sample (Section 4.1): "all Polymarket markets listed from platform inception through December 31, 2025", with event duration of at least 14 days, volume of at least 100, and one side at or above 0.90 "for seven consecutive daily snapshots".
- The discount curves are estimated from the prices themselves (an upper envelope of near-certain prices). The authors: "Remaining residual uncertainty biases ASWs upward and makes discount-adjusted calibration an attenuation test rather than exact latent-probability recovery." (ASW is their annualised settlement wedge.)
- Hourly quote midpoints, not executable prices.

### Claim 8. Akey, Grégoire, Harvie and Martineau

- Notes (event_driven_fast_reaction.md line 21; copy_trading_smart_money.md line 53): "no trade occurs in 99% of one-minute intervals, yet those intervals account for 76% of price variation; a VAR attributes at most 4% of efficient-price innovation variance to trades" (SSRN 7547106); "Nov 2022–Mar 2026, over 2.4 million users, $67 billion of volume. The top 1% of users with positive PnL capture 76.5% of profits, rising to about 80% in the lead-up to the election" (CEPR DP21615 / SSRN 6443103).
- One paper or two: two. The profit-concentration figures are in "Who Wins and Who Loses in Prediction Markets? Evidence from Polymarket". A full-text search of that paper finds no passage on one-minute intervals, price variation, efficient-price variance or quote updates, so the microstructure figures are not from it. The notes attribute them to a separate SSRN entry (7547106), which could not be opened.

**8a. Top 1% of winners take 76.5% of profits; 2.4M users; November 2022-March 2026. CONFIRMED.**
- URL opened: https://www.osc.ca/sites/default/files/2026-10/research-grant-competition-2026-who-wins-and-who-loses-in-prediction-markets.pdf (version dated August 28, 2026). The CEPR page returned HTTP 403 and was not retried.
- Abstract: "Using $67 billion in trade volume, we show that the gains are highly concentrated: the top 1% of users with positive PnL capture 76.5% of profits."
- Introduction: "Polymarket from November 11, 2022 through March 29, 2026, covering over 2.4 million users and $67 billion in trading volume." "the top 0.1% of users with positive PnL capture 51.2% of all gains and the top 1% capture 76.5%, yet roughly 69% of all users end the sample with a loss."
- Concentration section: "the top 5% captured 91.4%, and the top 25% accounted for 99.2%." Losses: "the top 0.1% of losers account for 43.7% of total losses, the top 1% for 68.1%".
- Over time: "Prior to the 2024 U.S. presidential election, the top 1% of winners captured approximately 40–50% of total gains. In the lead-up to the election ... the concentration of gains among the top 1% rose to approximately 80%." This confirms the notes' "about 80%".

Qualifiers:
- The 1% is of users with positive PnL, not of all users. With about 69% of users losing, that is roughly 0.3% of all accounts (my calculation).
- PnL is marked to market: "PnL = portfolio value + net USDC balance". The authors repeat the concentration result on fully resolved markets and on no-fee markets and report similar findings.
- Costs: "Polymarket did not charge trading fees on most markets during our sample period." "Our PnL definition does not net out Polygon gas costs."
- The sample ends the day before the broad fee roll-out (data section): "We end on that date because Polymarket introduced trading fees on all markets on March 30, 2026, which materially changes the economics of trading on the platform." The concentration result therefore describes the pre-fee regime.
- Mechanism and persistence (abstract): "Successful traders provide liquidity using limit orders that resolve favorably relative to realized outcomes while unsuccessful traders take liquidity using market orders. Monthly performance is modestly persistent, though this may reflect selection rather than skill." "44 percent of traders stop trading after a month".
- Independent academic study, funded in part by an Ontario Securities Commission research grant; the user-level data are public.
- The summary-statistics table gives totals of 588.3 million trades, $67,135.4 million of volume and 2,480,080 users. This confirms the "588 million trades ($67B of volume)" in liquidity_capacity_competition_venues.md line 180.
- Wash trading (Introduction): the authors state that their main findings "are not likely to be driven by wash trading".
- Gas (footnote 16): "Polymarket sponsors gas fees for users trading through the official website, so these costs are zero for the typical participant."

**8b. 99% of one-minute intervals have no trade yet account for 76% of price variation; trades explain at most 4% of efficient-price variance. COULD NOT OPEN.**
- URL tried: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7547106. SSRN returned HTTP 403 with a challenge page. Not retried.
- These three figures remain at search-snippet level. The 76% here (share of price variation) is a different statistic from the verified 76.5% (share of profits).

### Claim 9. Gómez-Cram, Guo, Jensen and Kung, "Prediction Market Accuracy: Crowd Wisdom or Informed Minority?" (SSRN 6617059)

- Notes (event_driven_fast_reaction.md line 22; copy_trading_smart_money.md lines 54 and 61): "roughly 3% of traders account for most price discovery; skilled traders react to news more quickly; the informed group (market makers plus skilled takers) is under 3.5% of accounts but takes over 30% of total gains"; "1.72 million accounts ... skilled 3.16% (54,325 accounts; press reports 3.14%)"; "44% (press) or 46% (reproduction's citation of the paper) of accounts classed as skilled in training stay skilled in test, against about 10% for mutual funds".
- URL opened: https://insights.som.yale.edu/insights/wisdom-of-the-few-prediction-markets-are-driven-by-small-number-of-skilled-traders (Yale SOM's article on the paper, by Anna Louie Sussman, dated June 10, 2026). The SSRN page was not requested, because SSRN had just refused the first request of the session.
- Status: PARTLY. The figures below were seen in the co-author's institution's summary, which quotes the paper once. None was seen in the paper itself.

Seen in the Yale article:
- Skilled share: "just 3% of accounts could be classified as "skilled," with significantly positive PnL that could not be explained by random chance. About twice as many accounts performed even worse than the benchmark".
- Gains (quoting the paper): the skilled group and market makers "represent fewer than 3.5% of all accounts, yet capture over 30% of total gains," the authors write. "Another 29% of traders, who the authors call "lucky winners," managed to make money without any statistically discernible skill".
- Sample: "two years of trading data, covering 1.72 million accounts whose owners collectively traded on 98,906 events and 210,322 markets, for a total trading volume of $13.76 billion."
- Persistence and how it was computed: "They divided the events that each trader bet on in half at random. A truly skilled trader would outperform the benchmark in both sets of trades—and indeed, they found that 44% of traders classified as skilled based on the first set of trades are also classified that way in the second. That's a significantly higher share than in, say, the mutual fund market, where just 10% of fund managers consistently outperform the overall market."
- Speed: "Skilled traders also reacted more quickly to news. For example, following FOMC meetings or corporate earnings announcements, skilled traders quickly bought contracts in the direction of the announcement before the contract settled."
- Price discovery: skilled traders "consistently moved contract prices in the direction of the final outcome, by buying more contracts that ultimately resolved Yes and selling contracts that ultimately resolved No."
- Insider trading (Jensen): "While we do find evidence of insider trading, it's sporadic, it's small, and it's not something that we think is systematically driving price discovery."

Not seen in any source opened here: the exact 3.16% (54,325 accounts), the 46% variant, "about 67% of accounts absorb most of the losses", and the sample dates 2023-2025.

Qualifiers:
- Skill is defined against a simulated coin-toss benchmark for each trader's own bets.
- The 44% comes from a random split of each trader's events into two halves, according to the article. That is a consistency check within the sample, not a test of whether last year's skilled accounts stay skilled next year. Jensen's quote in the same article speaks of "one period" and "the next period"; the paper was not opened to settle which design it uses. This matters for copy trading.
- The comparison with mutual funds (10%) is the article's.

### Claim 10. Valentin, "Right Before the News" (SSRN 7234098)

- Notes (event_driven_fast_reaction.md line 25): "64 single-stock corporate events"; "in 28 events Polymarket was already at least 80% priced on the correct side before the news existed"; "the post-release convergence trade loses 72–82% of stake"; "buying the stock on Polymarket's confidence lost money on 17 of 22 trades".
- Status: COULD NOT OPEN. The only URL in the notes is the SSRN abstract page. SSRN answered the first request of this session (abstract 7547106) with HTTP 403 and a challenge page, so this page was not requested and no other route was tried.
- All four figures remain at search-snippet level.
- To check if the paper becomes available: whether the 72-82% loss is per trade or cumulative, whether it is before or after spreads, how many trades it covers, and whether the test was pre-registered as the notes say.

### Claim 11. Angelini and De Angelis, "When Do Markets Fully Process Public Information? Evidence from Real-Time Prediction Markets" (arXiv 2606.07811)

- URL opened: https://arxiv.org/abs/2606.07811 and https://arxiv.org/pdf/2606.07811 (v1, 5 Jun 2026).
- Notes (event_driven_fast_reaction.md lines 23, 57 and 63): "live Kalshi NBA contracts, one-minute quotes merged with timestamped play-by-play"; prices "underreact on impact"; "thin markets adjust less completely"; "exploitability after spreads, fees and taker delays is not established"; size and half-life of underreaction "need the full texts".
- Status: CONFIRMED for the underreaction and the liquidity effect. CORRECTED on exploitability: the paper tests it and the result is negative.
- Data (Section 2, Table 1): "one-minute observations for NBA winner contracts" on Kalshi; "1,438 NBA games, 2,876 team-level contracts, and 409,512 contract-minute observations"; sample period "2025-04-15 to 2026-05-25". The price is the midpoint of the best YES bid and ask.
- Size of underreaction (Table 5): "The coefficient on ∆q is 0.630. Column 2 adds controls and yields a similar estimate of 0.638 ... a 10 percentage point increase in benchmark win probability is associated with only about a 6.4 percentage point contemporaneous increase in the Kalshi midpoint."
- Drift (Table 6): "At the five-minute horizon, a 10 percentage point initial updating gap predicts a 2.0 percentage point subsequent price change and a 4.6 percentage point price change net of benchmark updates. At the fifteen-minute horizon, the corresponding effects are 2.4 and 4.8 percentage points." Raw coefficients run from 0.150 at 1 minute to 0.236 at 15 minutes. No half-life is reported.
- Thin markets (Section 6): "The interaction between salience and illiquidity is positive and highly significant ... In liquid markets, salient information is incorporated relatively quickly. In illiquid markets, however, the same salient signals are associated with larger underreaction gaps."
- Exploitability (Introduction): "the predictable midpoint drift does not translate into a simple arbitrage opportunity once bid–ask costs are imposed."
- Table 11 (robustness appendix), five-minute directional returns after an underreaction gap, as printed:

| Gap threshold | Sample | Midpoint return | Executable-style return |
|---|---|---|---|
| 0 bp or more | All | 0.0039 | -0.0120 |
| 0 bp or more | High-quality | 0.0037 | -0.0078 |
| 100 bp or more | All | 0.0062 | -0.0101 |
| 200 bp or more | All | 0.0087 | -0.0092 |
| 200 bp or more | High-quality | 0.0082 | -0.0036 |

- The paper's reading of Table 11: "executable-style returns remain negative even for large gaps. Once transaction costs are incorporated, the apparent predictability is largely absorbed by the bid–ask spread."

Qualifiers:
- The benchmark is the authors' own win-probability model, "estimated out of sample using five-fold cross-fitting at the game level" (Brier score 0.164, the same as the Kalshi live midpoint). Part of the measured underreaction could be benchmark error; the authors use the drift test to address this.
- One-minute data cannot show reactions within the minute.
- Table 11 covers spreads only. Fees and order delay are not modelled, and they would lower the returns further.

### Claim 12. Lopez-Lira and Tang, "Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models" (arXiv 2304.07619)

- URL opened: https://arxiv.org/abs/2304.07619 and https://arxiv.org/pdf/2304.07619 (v6, 28 Oct 2025).
- Notes (event_driven_fast_reaction.md lines 245, 248 and 262): "about 34 bps/day long-short before costs"; stronger for small stocks and negative news; "strategy returns decline as LLM adoption rises"; "Precise decay numbers ... and the adoption proxy used were not retrieved".
- Status: CONFIRMED.
- Introduction: a "strategy based on GPT-4's assessments of overnight news generates average returns of 34 basis points (bps) per day before transaction costs."
- Results section: the drift strategy "has hit rates of 58% for overnight news and 55% for intraday news, and mean returns of 0.34% and 0.50%, respectively. These drift strategies achieve annualized pre-transaction-costs Sharpe ratios of 2.97 for overnight news and 2.63 for intraday news."
- Decay figures (Introduction): "we find some suggestive evidence: a general decline in the performance of the ChatGPT-based strategy during our sample period, over which GPT models' capabilities and adoption skyrocketed. For example, its annualized Sharpe ratio drops from 6.54 in 2021Q4 to 3.68 in 2022, 2.33 in 2023, and to 1.22 over January-May 2024."

Qualifiers:
- Sample: "from October 2021 to May 2024", 4,123 companies, after the model's September 2021 training cutoff. US equities, headline news.
- There is no adoption proxy. The evidence for "declines as adoption rises" is a time trend in Sharpe ratios, and the authors call it "suggestive".
- Costs: "Assuming a transaction cost of 5 bps round-trip, the strategy still earns a cumulative return of over 300% ... 10 bps round-trip, the cumulative return is still above 100%. A transaction cost of 20 bps round-trip makes the strategy unprofitable."
- Most of the return is on the short side: "the long leg has an average daily return of 8 bps ... the short leg has an average daily return of 26 bps".
- The 34 bps is the tradable drift. The roughly 90% hit rate in the abstract is for the "non-tradable initial reaction".
- The notes' "earlier version reported a pre-cost Sharpe ratio of 3.8" was not checked; v6 reports 2.97.

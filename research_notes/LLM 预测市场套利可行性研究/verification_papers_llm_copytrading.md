# Verification log: LLM-trading and copy-trading claims checked against primary sources

> **Status: IN PROGRESS (skeleton written 26 November 2026; entries are filled in as each source is opened).**
> Until a row below says CONFIRMED / CORRECTED / PARTLY / COULD NOT OPEN, treat it as not yet checked.
>
> **Method.** Each claim was traced to the URL cited in the earlier notes; the primary source was fetched with a plain `curl` request through the session proxy (no altered headers, no private APIs) and the figure was located in the source text. A claim is marked CONFIRMED only when the figure was seen in the source itself. Where a second-round researcher had already read the source in full, that entry is cited and labelled "second-round read", not re-downloaded.

## Summary table (provisional)

| # | Short claim | Status |
|---|---|---|
| 1 | Prediction Arena: six models, $10,000 each, all lost on Kalshi (−16.0% to −30.8%, mean −22.6%); Polymarket −1.1% | PENDING |
| 2 | Prophet Arena (ICLR 2026): Brier 0.18–0.22 vs market 0.187; ECE ≤ 0.05 vs 0.069; ablation 0.191 vs 0.169; live Gemini 3 run +80.33%, Sharpe 3.35 | PENDING |
| 3 | El Lahib et al.: date-filtered search leakage, Brier 0.242 → 0.108 | PENDING |
| 4 | Jia and Sun: Polymarket copy trading with live on-chain execution | PENDING |
| 5 | ForecastBench: 69.2 vs 68.8 (22 Sep 2026) and 69.5 vs 68.1 (25 Nov 2026) | PENDING |
| 6 | KalshiBench ECE 0.120–0.395; KellyBench all models lose, human +5.1%; PolyBench 5 of 7 negative | PENDING |
| 7 | Mitts and Ofir: about $143M anomalous profit; 152 wallets, about $8M in military markets | PENDING |
| 8 | Columbia wash-trading study: about 25% of volume; 45% sports, 3% crypto | PENDING |
| 9 | Bürgi, Deng and Whelan: −20% before fees, −22% after; favourite-longshot; maker vs taker | PENDING |
| 10 | Bartlett and O'Hara: makers won 63.4% of single-name contracts; Becker: ±2.65% at 50 cents, 72.1M trades | PENDING |
| 11 | Gu et al. (v3, 23 Sep 2026): significantly positive simulated score gaps for five newest model variants | PENDING |

(Detailed entries follow once sources are read.)

# Verification log: key claims checked against official sources

Checked on 26 November 2026. This log supersedes the earlier notes wherever the two differ. A claim is marked CONFIRMED only where I read the statement in the official source itself. "Mirror" means a third-party GitHub copy of Polymarket's developer docs (Etherdrake/PolymarketDocumentation, content as of about late August 2026); mirror text is reported but never counted as confirmation.

## Summary (corrections first)

| # | Claim | Status | What the report should say |
|---|---|---|---|
| 6 | Polymarket holding rewards of 4% | CORRECTED (official pages conflict) | The help-centre article dated 1 June 2026 says 3.25% annualised and lists 18 eligible events. The 4.00% figure was seen only in the mirror of the developer docs; the live docs page was refused today. Do not state 4% as fact. |
| 8 | Polymarket US fees and API rebate | PARTLY, with corrections | Taker tiers 0.095 / 0.085 / 0.075 / 0.0695 confirmed in the exchange notice effective 6 Nov 2026. API takers are charged 0.0695 whatever their tier and get 70% back (21 Nov to 31 Dec 2026), a net coefficient of about 0.0209. Makers pay zero except on combo athletic contracts, where a 0.03 maker coefficient applies from 14 Nov 2026. A CFTC filing of 10 Nov 2026 shows a different tier table (0.117 down to 0.065). |
| 2 | Polymarket rebate schedule | PARTLY, with a correction | Rates confirmed in the changelog: takers 10 / 25 / 40 / 50 / 60%, makers 0 / 3 / 7 / 10 / 15%. The "7 / 10 / 15%" version omits the 3% tier. Dollar thresholds were not seen in any official page opened today. |
| 10 | X API price and stream delay | PARTLY, with a correction | $0.005 per post read and the 3 million monthly cap confirmed in X's own docs repository. The same repository says 4-5 s at the 99th percentile in three files. The 6-7 s figure could not be checked (docs.x.com refused); do not use "4-7 s". |
| 3 | Polymarket taker delay | PARTLY, with a correction | Crypto: 50 ms from 17 Aug and 150 ms from 4 Sep 2026 confirmed; 150 ms is current. The 18 Feb removal and the June start of 250 ms are not in the official changelog. Sports: 3 s and a 1 s test are both help-centre statements (20 Apr 2026); the developer docs, as mirrored, give no number, only a per-market configured delay. |
| 7 | UMA resolution | PARTLY | 2-hour challenge period, $750 bond and the two-dispute escalation confirmed. Polymarket's own pages still say anyone may propose; UMA's UMIP-189 gives Polymarket control of a proposer whitelist. The count of 37 proposers and "a first dispute adds about 4 hours" were not found. |
| 9 | Kalshi fees, interest, rate limits | PARTLY | Interest (3.50% APY, $250 minimum) and rate-limit tiers confirmed. The fee schedule PDF could not be opened, so 0.07, 0.0175, the rounding rule and "no settlement fee" remain unverified. |
| 11 | CFTC advisory, Van Dyke, Spagnuolo | PARTLY | Charges and amounts confirmed from the DOJ charging documents. Announcement dates and everything on cftc.gov, including the 25 Feb 2026 advisory, could not be opened. |
| 5 | CLOB V2 cut-over, pUSD, client libraries | CONFIRMED | 28 Apr 2026 cut-over and pUSD confirmed. V1 clients are archived and non-functional, V2 clients are deprecated, and the unified SDKs are current. |
| 1 | Polymarket international fees from 20 Nov 2026 | CONFIRMED | Formula and all category rates confirmed. Add "Other / General" at 0.05. |
| 4 | Polymarket CLOB rate limits | CONFIRMED | All three figures confirmed in the changelog entries of 8 Apr and 1 Jun 2026. |
| 12 | DeFi Rate October 2026 table | CONFIRMED | All three figures confirmed. They are notional: one dollar per reported contract, not cash paid. |

## Access record

Method: plain `curl` through the session proxy with default headers, public pages only. One web search was used (of three allowed), to find the DOJ indictment URL.

| Host | Result |
|---|---|
| docs.polymarket.com | First four requests returned HTTP 200 (index, fee page, November page, changelog). The fifth returned HTTP 403 "Vercel Security Checkpoint". One later, slower request for a page not yet requested got the same 403, and the host was then dropped. Not opened: order lifecycle, rate limits, resolution, positions and tokens, taker rebates, maker rebates, SDK changelog. |
| docs.polymarket.us | Index opened; the fee page returned 403 (Vercel checkpoint). COULD NOT OPEN. |
| kalshi.com | Fee schedule PDF returned 403 (Vercel checkpoint). COULD NOT OPEN. |
| docs.x.com | 403 (Vercel checkpoint). COULD NOT OPEN. |
| docs.kalshi.com | Rate-limit page opened; a later request returned 403. |
| www.cftc.gov | 403 (Cloudflare challenge). COULD NOT OPEN. |
| www.justice.gov | The one press-release page requested returned a bot-verification page instead of content, so press releases are COULD NOT OPEN. Charging-document PDFs on the same site opened normally. |
| help.polymarket.com, help.kalshi.com, polymarketexchange.com, defirate.com, raw.githubusercontent.com, kalshi-public-docs.s3.amazonaws.com | Opened. |

Three cautions apply throughout. First, Polymarket's help centre lags its developer docs: the help articles "Trading Fees" (10 Jul 2026) and "Maker Rebates Program" (21 Jul 2026) still show the pre-November rates. Second, the GitHub API was not available for these repositories, so archive flags and the mirror's commit date were not checked. Third, downloaded copies are in `/tmp/claude-0/-home-user-hongjie-qiu/e1b14ff5-c349-500f-acaf-37657bee47dd/scratchpad/vos_dl/`.

## 1. Polymarket international fees from 20 November 2026: CONFIRMED

Notes' statement (platform_mechanics_costs_regulation.md, lines 14 and 59-62): fee = C × θ × p × (1 − p); from 20 Nov 2026 23:59 UTC θ is 0.01 for most crypto, non-election politics, mentions, economics, culture and weather, 0.05 for sports, finance and tech, election politics and BTC 5- and 15-minute markets, and 0 for geopolitics.

Sources opened:
- https://docs.polymarket.com/trading/fees.md (HTTP 200). The page carries no date of its own.
- https://docs.polymarket.com/programs/fee-and-rebate-changes-november-2026.md (HTTP 200). It now returns the same bytes as the fee page, so the announcement no longer exists as a separate text.
- https://docs.polymarket.com/changelog/predictions.md, entry "Nov 20, 2026": "Effective November 20, 2026 at 23:59 UTC on Polymarket.com: Taker fees: Category coefficients are 0.01 or 0.05; Geopolitics remains fee-free."

Exact rule: "fee = C × feeRate × p × (1 - p)", where "C = number of shares traded and p = price of the shares". "Makers are never charged fees. Only takers pay fees." "Fees are rounded to 5 decimal places. The smallest fee charged is 0.00001 USDC."

| Category | Taker rate |
|---|---|
| Crypto: BTC 5-minute and 15-minute up/down | 0.05 |
| Crypto: all other markets | 0.01 |
| Sports, including NFL and college football | 0.05 |
| Finance | 0.05 |
| Tech | 0.05 |
| Politics: elections | 0.05 |
| Politics: excluding elections and geopolitics | 0.01 |
| Economics, Culture, Weather, Mentions | 0.01 each |
| Geopolitics | 0 |
| Combos | 0.05 |
| Other / General | 0.05 |

Fee per share, computed from the formula (the official table gives the same values per 100 shares, rounded to the cent):

| Price | θ = 0.05 | θ = 0.01 | θ = 0 |
|---|---|---|---|
| 50 cents | 1.25 cents (2.5% of price) | 0.25 cents (0.5%) | 0 |
| 70 cents | 1.05 cents (1.5%) | 0.21 cents (0.3%) | 0 |
| 95 cents | 0.2375 cents (0.25%) | 0.0475 cents (0.05%) | 0 |

Qualifiers:
- "Other / General" at 0.05 is missing from the claim as listed.
- Combos pay 0.05 "whatever categories its legs come from".
- The NFL and college football sub-rate of $0.75 per 100 mentioned in the notes is not on the page; those markets are at 0.05.
- The changelog confirms two history items in the notes: Fee Structure V2 on 30 Mar 2026, and sports moving from 0.03 to 0.05 on 10 Jul 2026 (with the sports maker rebate cut from 25% to 15%).

## 2. Polymarket rebates: PARTLY, with a correction

Notes' statements: platform_mechanics_costs_regulation.md lines 60 and 63 give taker tiers Gold $200k 10%, Platinum $1M 25%, Diamond $4M 40%, Obsidian $10M 50%, Onyx $75M 60%, and maker tiers of 3 / 7 / 10 / 15% from $200k / $1M / $4M / $10M of 30-day weighted volume. structural_arbitrage.md lines 161 and 192 give maker rates of 7 / 10 / 15% at $1M / $4M / $10M.

Source opened: https://docs.polymarket.com/changelog/predictions.md, entries of 16 and 20 Nov 2026 (effective 20 Nov 2026, 23:59 UTC).
- "Taker rebates: Gold pays 10%, Platinum 25%, Diamond 40%, Obsidian 50%, and Onyx 60%. Bronze and Silver, category multipliers, and one-time level-up bonuses are removed. Price weighting stays."
- "Maker rebates: Volume tiers replace daily market-wide pools. Standard tier rates are 0%, 3%, 7%, 10%, or 15% of the taker fee eligible fills generate, before taker-tier rebates. Maker tiers are independent of taker tiers. Combos and fee-free trades do not qualify."
- "Makers continue to pay no platform trading fee. Maker rebates and Liquidity Rewards are separate programs."

Correct schedule as far as it could be established:
- All rates in the first file are confirmed.
- The second file's version is incomplete, because the official text has four paying maker tiers including 3%. The two versions are otherwise compatible.
- The dollar thresholds were not seen in an official page: the taker-rebate and maker-rebate pages were refused.
- The mirror's older copy of the taker page already put Gold, Platinum, Diamond and Obsidian at $200,000, $1,000,000, $4,000,000 and $10,000,000. That supports those four thresholds indirectly. The $75M Onyx threshold and the maker thresholds have no primary text behind them in this check.

Qualifiers:
- Weighted volume is far smaller than notional. The older official page (mirror) defined it as trade size × (1 − entry price) × category weight × bonuses, with trade size meaning dollars paid, and the changelog says the category weights were removed while price weighting stays. A fill of 1,000 shares at 50 cents ($500 paid) therefore adds $250, and at 95 cents each dollar paid adds 5 cents.
- regulation_access_conduct_tax.md line 204 already records the clause letting Polymarket remove rebates and tier status for wash trading and self-matching (mirror).

## 3. Polymarket taker delay: PARTLY, with a correction

Notes' statements: platform_mechanics_costs_regulation.md lines 41-47; event_driven_fast_reaction.md line 94 ("The help center (3 s) and developer docs (1 s) differ on the sports delay length").

Crypto markets, source https://docs.polymarket.com/changelog/predictions.md:
- "Aug 17, 2026 ... The taker delay on crypto markets is now `50ms`, down from `250ms`. The change took effect on August 17 at 11:00 UTC (7:00 AM ET)." CONFIRMED.
- "Sep 4, 2026 ... The taker delay on crypto markets is now `150ms`, up from `50ms`. The change took effect on September 4 at 14:00 UTC (10:00 AM ET)." CONFIRMED.
- No later delay entry exists up to the newest entry (25 Nov 2026), so 150 ms is the current published value.
- The removal of a 500 ms delay on 18 Feb 2026 and the start date of the 250 ms delay are not in the changelog. Its February entries cover fees only. The 250 ms level is confirmed only as the value before 17 Aug. The X posts cited in the notes were not opened.

Sports markets, source https://help.polymarket.com/en/articles/13364444-limit-orders (article dated 20 April 2026):
- "any outstanding limit orders are automatically cancelled once the game begins, clearing the entire order book at the official start time. Be aware, game start times can shift".
- "sports markets include a 3-second delay on the placement of marketable orders."
- "A 1-second taker delay is currently being tested on NBA and MLB markets, with others being added in the future."

Correction: both the 3 s and the 1 s figures come from the help centre. The developer docs' order-lifecycle page was refused today. The mirror copy gives no number: "Sports/game delay: enabled on configured sports markets around live game conditions. The order waits for the market's configured delay window before matching", and "During either delay, the order is pending and cannot be canceled." The current sports value is therefore per market and was not established. The help-centre article is seven months old and that site is known to lag.

## 4. Polymarket CLOB rate limits: CONFIRMED

Notes' statement (platform_mechanics_costs_regulation.md line 35): `POST /order` and `DELETE /order` 5,000 per 10 s burst and 120,000 per 10 minutes sustained; `POST /orders` 2,000 per 10 s burst and 21,000 per 10 minutes sustained.

Source opened: https://docs.polymarket.com/changelog/predictions.md.
- "April 8, 2026 ... CLOB POST /order - 5000 every 10s (500/s) - (BURST) ... CLOB POST /orders - 21000 every 10 minutes (35/s)".
- "Jun 1, 2026 ... CLOB POST /order - 120000 every 10 minutes (200/s) - (SUSTAINED) ... CLOB POST /orders - 2000 every 10s (200/s) - (BURST) ... CLOB DELETE /orders - 2000 every 10s (200/s) - (BURST)".

Qualifiers:
- The full rate-limit page was refused. The mirror copy shows the same order rows, plus `DELETE /orders` at 15,000 per 10 minutes and `DELETE /cancel-market-orders` at 1,500 per 10 s and 21,000 per 10 minutes.
- The mirror copy also says the limits are "IP-based and enforced using Cloudflare's throttling system" and that "CLOB order and cancellation requests also use separate per-signer token-bucket limits". That second layer has its own page, which was not opened.
- The two outdated figures flagged in the notes are explained by the changelog: 48,000 per 10 minutes was the 8 Apr 2026 value, and 500 per 10 s with 3,000 per 10 minutes was the 15 May 2025 value.

## 5. CLOB V2 cut-over, pUSD and client libraries: CONFIRMED

Notes' statement (platform_mechanics_costs_regulation.md lines 19-20): cut-over reported as 28 Apr 2026, about 11:00 UTC with about an hour of downtime; pUSD replaces USDC.e; resting orders cancelled.

Source opened: https://docs.polymarket.com/changelog/predictions.md.
- "Apr 17, 2026 ... Exchange upgrades go live April 28, 2026 at ~11:00 UTC with ~1 hour of downtime." "pUSD replaces USDC.e as the collateral token (standard ERC-20 on Polygon, backed by USDC, backing enforced onchain)".
- "Apr 28, 2026 CLOB V2 is live on production ... Legacy V1 SDKs and V1-signed orders are no longer supported on production ... Resting orders from before the cutover did not migrate and must be re-created with V2 signing."

Client libraries today (READMEs on the main branch of Polymarket's own GitHub repositories, plus the changelog):

| Library | Official status |
|---|---|
| `py-clob-client` and `clob-client` (V1) | "This repository has been archived and is no longer maintained. The client is no longer functional and should not be used for new or existing integrations." Each README points to the unified SDK (Polymarket/py-sdk, Polymarket/ts-sdk). |
| `py-clob-client-v2` and `clob-client-v2` | "This package is deprecated. Please migrate to the unified Polymarket SDK." Still released: `py-clob-client-v2 1.2.2` on 12 Nov 2026, when the changelog repeats "The Python CLOB client remains deprecated." |
| Unified SDKs `@polymarket/client` (TypeScript) and `polymarket-client` (Python) | Current. Version 0.20.1 is named in the 25 Nov 2026 changelog entry. |

Qualifiers:
- A further change is in progress: "Polymarket Protocol V2" markets on the Polygon Amoy test network (changelog, 12 Nov 2026).
- Other recent breaking changes in the changelog: Data API v1 retired on 2 Nov 2026; the relayer restricted to Polymarket and listed third-party contracts from 11 Nov 2026; three CLOB query deprecations take effect on 14 Dec 2026.
- regulation_access_conduct_tax.md line 343 describes pUSD wrapping and its pause gate from the mirror; nothing opened today contradicts it.

## 6. Polymarket holding rewards: CORRECTED (official pages conflict)

Notes' statement (platform_mechanics_costs_regulation.md line 69): "Holding rewards: 4.00% annualised on total position value in eligible markets; position value sampled randomly once per hour; paid daily; rate variable", attributed to the developer docs.

Source opened: https://help.polymarket.com/en/articles/13364459-holding-rewards (article dated 1 June 2026).
- "we're paying 3.25% annualized Holding Reward based on your total position value in certain Polymarkets. We anticipate rolling out a new reward and oracle-resolution system later this year".
- "The current rate is set at 3.25% and applies to all eligible positions. This rate is variable and subject to change at Polymarket's discretion. We also reserve the right to introduce limits to the total amount of rewards paid out at any time. This iteration of rewards is funded through the Polymarket Treasury."
- "Your total position value is randomly sampled once each hour, and the reward is distributed daily." Positions are valued at "the most recent mid-price for each outcome".
- Eligible events listed (18): Presidential Election Winner 2028; Republican Presidential Nominee 2028; Democratic Presidential Nominee 2028; Which party wins 2028 US Presidential Election?; Balance of Power: 2026 Midterms; Which party will win the Senate in 2026?; Which party will win the House in 2026?; Erdoğan out before 2027?; Zelenskyy out as Ukraine president before 2027?; Netanyahu out before 2027?; Xi Jinping out before 2027?; Putin out as President of Russia before 2027?; Russia x Ukraine ceasefire before 2027?; and "What price will ... hit in 2026?" for Bitcoin, Ethereum, Hyperliquid, Solana and XRP.

Not opened: https://docs.polymarket.com/concepts/positions-tokens.md (refused). The mirror copy reads "Polymarket pays a 4.00% annualized Holding Reward based on your total position value in eligible markets."

Assessment: two official pages disagree and I could open only one. The help-centre page is dated but the help centre is stale elsewhere; the docs page is undated. Safe wording: a variable rate, 3.25% on the help centre (1 June 2026) and 4.00% in the developer docs as last copied, limited to a short list of long-dated political, geopolitical and crypto-price events.

## 7. Polymarket resolution through UMA: PARTLY

Notes' statement (platform_mechanics_costs_regulation.md lines 180-182): a whitelisted proposer (37 proposers per a forum post, under UMIP-189) posts an outcome with a bond of about $750; an undisputed proposal finalises about 2 hours later; a first dispute adds roughly 4 hours; a second dispute goes to a UMA token-holder vote taking several days; no appeal.

Sources opened and what they say:

| Point | Official text | Source and date |
|---|---|---|
| Challenge period | "Once a market is proposed for resolution it goes into a challenge period of 2 hours." | Help centre, "How Are Markets Disputed?" (5 Apr 2026) and "How Are Prediction Markets Resolved?" (11 Jan 2026). Polymarket/uma-ctf-adapter README: liveness "currently about 2 hours". |
| Bond | "you will lose all of your $750 bond"; a disputer posts "a challenge bond of the same amount as the proposer bond (usually $750)" | Same help articles. The January article says the bond is "in USDC.e"; the mirror says "typically $750 pUSD". |
| First dispute | "The first time a request is disputed, the market is automatically `reset`, meaning, a new Optimistic Oracle request is sent out." | Polymarket/uma-ctf-adapter README |
| Second dispute | "If the request is disputed again ... the Optimistic Oracle falls back to UMA's DVM ... The DVM will return data after a 48 - 72 hour period." | Same README |
| Vote timing | A "debate period of 24-48 hours", then "Uma token holders vote (this process takes approximately 48 hours)" | Help centre (5 Apr 2026) |
| Vote outcomes | Proposer wins, Disputer wins, Too Early, or Unknown/50-50. The winner gets the bond back "plus half" the loser's bond. | Help centre (5 Apr 2026) |
| Finality | "Polymarket is non-custodial and cannot alter or reverse market resolutions. Once finalized by UMA, outcomes are immutable." | Help centre (5 Apr 2026) |
| Who may propose | Polymarket's pages describe proposing as open to the reader; the mirror says "Anyone can propose an outcome". UMIP-189 says the ManagedOptimisticOracleV2 "gives the integrator admin access to easily modify the bond, liveness, and who can propose for all of their requests", can "set the default proposer whitelist which applies all new requests", is "managed by Polymarket" and is "upgradable via a 2/2 multisig consisting of Polymarket and Risk Labs". | https://raw.githubusercontent.com/UMAprotocol/UMIPs/master/UMIPs/umip-189.md (status field not checked) |

Not confirmed: that the whitelist is in force today and has 37 members, and that a first dispute adds about 4 hours. Neither appears in a source opened.

Qualifiers from the changelog:
- 28 Sep 2026: the resolutions endpoint distinguishes `managed_proposal_expiration` and `proposal_expiration` (UMA challenge windows), `liveness` on "Polymarket's v2 oracle", and `dvm_round_estimate`. It adds that "a disputed vote can roll into a later round, and a proposal past its window that is still under review returns no estimate while `extended_review` is `true`." The 2-hour window is therefore not a hard deadline.
- A second, Polymarket-run oracle exists for the new V2 markets, which matches the "new reward and oracle-resolution system" announced in the holding-rewards article.
- Help centre, "How Are Markets Clarified?" (29 Jun 2026): "When a market is clarified, the order book is cleared and all resting orders cancelled at the time of clarification."

## 8. Polymarket US fees: PARTLY, with corrections

Notes' statement (platform_mechanics_costs_regulation.md lines 96 and 104-107): taker Θ tiered by trailing 30-day taker volume, 0.095 under $10k, 0.085 to $50k, 0.075 to $250k, 0.0695 above; makers pay nothing; a 70% taker-fee rebate on straight API trades from 21 Nov to 31 Dec 2026; effective date reported as 6 or 11 Nov.

docs.polymarket.us/fees was refused. The exchange's own site opened: https://polymarketexchange.com/notices.html, with files under https://polymarketexchange.com/files/notices/. The exchange is QCX LLC d/b/a Polymarket US.

| Document (file name on the site) | Exact content |
|---|---|
| "Exchange Notice - Taker Fee Tiers (2026.11.06).pdf", notice PMXN-2026-4 (file last modified 17 Nov 2026) | "Effective Friday, November 6, 2026 ... The taker fee tier is calculated daily using taker volume over the preceding 30 completed Eastern Time (ET) calendar days, excluding today." Tier 1 below $10,000: 0.095. Tier 2 $10,000 to less than $50,000: 0.085. Tier 3 $50,000 to less than $250,000: 0.075. Tier 4 $250,000 or more: 0.0695. "This tier sets Θ in both the standard taker fee formula, including Table Tennis, and the combo taker fee formula." |
| "Exchange Notice - Weekly Notification of Fee Schedule Change (2026.11.10).pdf", CFTC filing PMX-2026-63 | Fee = Θ × C × p × (1 − p). The filing replaces a flat +0.0695 with tiers from "Θ = +0.1170 for taker volume below $10,000 to Θ = +0.0650 for taker volume of $50,000,000 and above", effective 6 Nov 2026. Exhibit: 0.1170, 0.1100, 0.1000, 0.0700 ($250k), 0.0695 ($1M), 0.0690 ($10M), 0.0675 ($25M), 0.0650 ($50M+). "A new Participant pays Θ = +0.0695 for the first 7 days after their first trade". Combo taker fee = C × p × [Θ × (1 − p) + 0.06 × (1 − p)^4]. |
| "Exchange Notice - Fee Change for API Takers (2026.11.21).pdf", notice PMXN-2026-6 | "Effective Saturday, November 21, 2026 at 12:01 AM ET, all taker trades placed through the Polymarket US API will be charged a standard taker fee coefficient of 0.0695 and receive a 70% rebate on those fees. The program will run through December 31, 2026." |
| "Exchange Notice - Fee Change for Combination Athletic Event Contracts (2026.11.11).pdf", notice PMXN-2026-2 | From 14 Nov 2026, makers on combo athletic event contracts pay "Fee = 0.03 × C × p × (1 - p)"; before, "Makers pay zero fees per trade". |
| "Exchange Notice - Amendment to Taker and Maker Rebate Tiers (2026.10.23).pdf", effective 6 Nov 2026 | Taker rebate on trailing 30-day notional taker volume: $250,000 3%, $1,000,000 5%, $10,000,000 10%, $25,000,000 15%, $50,000,000 and above 30%. Standard maker rebate coefficient: −0.0035 from $10,000,000, −0.0070 from $50,000,000, −0.0104 from $200,000,000. "The maker fee is zero. Below $10,000,000, no standard tiered maker rebate applies". |
| "Exchange Notice - Fee Schedule Modification (2026.11.16).pdf", CFTC filing PMX-2026-74 | Deposit fees on deposits made on or after 1 Dec 2026: card, PayPal and Cash App Pay 2%; stablecoin 0.05%; waived on a participant's first deposit. |

Assessment:
- The four tiers and their thresholds match the exchange's public notice, and the effective date is 6 Nov 2026, not 11 Nov. CONFIRMED.
- The CFTC filing dated four days later lists higher coefficients for the three lowest tiers and extra tiers above $1M. I could not determine which document governs. The notes' figures follow the public notice.
- "Makers pay nothing" needs the combo exception from 14 Nov 2026.
- The API programme is confirmed for 21 Nov to 31 Dec 2026, but it is not a rebate on top of each tier. Every API taker is charged 0.0695 and gets 70% back, a net coefficient of 0.02085. At 50 cents that is 0.52 cents per contract, against 2.375 cents at tier 1 through the app. The inference at line 113 of the notes (0.0285 at the lowest tier) should be replaced.
- The notice says "all taker trades placed through the Polymarket US API". The word "straight" is not in it; whether combos are excluded was not verified.

Cost per contract at 50 cents: 2.375 cents at 0.095, 2.125 at 0.085, 1.875 at 0.075, 1.7375 at 0.0695.

History confirmed on the same site: the filing of 27 Mar 2026 set taker Θ = +0.05 and maker rebate Θ = −0.0125, and the 2 Oct 2026 filing replaced the uniform maker rebate with the three volume tiers.

## 9. Kalshi fee schedule, interest and rate limits: PARTLY

Notes' statement (platform_mechanics_costs_regulation.md lines 126, 131-135, 142-144 and 158): fee schedule titled "Fee Schedule for July 2026 - 7.7.26 Update"; taker 0.07 × C × P × (1 − P) rounded up, at most $1.75 per 100 contracts; maker 0.0175 × C × P × (1 − P) on listed series only; no settlement fee; 3.50% APY with a $250 minimum; token-bucket rate tiers.

Fee schedule: COULD NOT OPEN. https://kalshi.com/docs/kalshi-fee-schedule.pdf returned HTTP 403, and I did not find the document in the root or the regulatory folder of Kalshi's public document bucket. The only official fee text opened was https://help.kalshi.com/trading/fees: "Kalshi makes money by charging a transaction fee on the expected earnings on the contract", and maker fees "are only charged when a trade is ultimately executed, there are no fees associated with canceling a resting order." The coefficients, the rounding rule, the schedule date and the absence of a settlement fee therefore still rest on secondary sources. The $1.75 per 100 contracts is the formula's maximum at 50 cents, not a separately verified cap.

Interest: CONFIRMED. Source https://help.kalshi.com/en/articles/13823847-apy-on-kalshi (marked "Updated this week").
- "Rate: 3.50% APY. This rate is variable and can change at any time."
- "Your average monthly predictions balance, including cash and positions, must be at least $250."
- "Interest accrues daily and is paid monthly." Accrual uses the net portfolio value at 12am ET, with positions "based on last traded prices".
- "Interest programs are currently only available to eligible users in the United States and its territories." A Social Security Number is needed for interest above $10 a year.
- Perps accounts: 3.50% on cash, and 7% on open positions under a capped programme.

Rate limits: CONFIRMED. Source https://docs.kalshi.com/getting_started/rate_limits.md (HTTP 200, undated).

| Tier | Read tokens per second | Write tokens per second | How obtained |
|---|---|---|---|
| Basic | 200 | 100 | Account signup |
| Advanced | 300 | 300 | Call the upgrade endpoint; at least one of the latest 100 orders must have come through the API |
| Expert | 600 | 600 | Volume share 0.075% to earn, 0.05% to keep |
| Premier | 1,200 | 1,200 | 0.125% / 0.10% |
| Paragon | 2,400 | 2,400 | 0.25% / 0.20% |
| Prime | 4,800 | 4,800 | 0.50% / 0.40% |
| Prestige | 12,000 | 9,600 | 1.00% / 0.80% |

- "Most requests cost the default of 10 tokens", so Basic sustains about 20 reads and 10 order operations per second.
- Volume share is trailing 30-day volume, both sides counted, divided by twice the previous calendar month's exchange volume.
- Write buckets above Basic hold three seconds of budget. Batch items are billed individually: 10 tokens per created order, 2 per cancelled order.
- A breach returns HTTP 429 with no `Retry-After`: "There is no penalty or cooldown."
- regulation_access_conduct_tax.md line 191 records that Kalshi may change rate limits without notice (Developer Agreement).

## 10. X API pricing and stream latency: PARTLY, with a correction

Notes' statements: llm_realtime_latency_cost.md line 248 ("a 99th-percentile delay of about 4-7 s at $0.005 per post"), line 254 (4-5 s, from the docs repository), line 255 (a search summary of the live page said 6-7 s) and line 335; practitioner_implementation_risks.md line 60.

docs.x.com was refused. Opened instead: X's own documentation repository, main branch, on 26 Nov 2026.
- https://raw.githubusercontent.com/xdevplatform/docs/main/x-api/getting-started/pricing.mdx: "The X API uses pay-per-usage pricing. No subscriptions". "Posts: Read | $0.005 per resource"; "User: Read | $0.010 per resource". "Pay-per-usage plans are capped at 3 million Post reads per monthly billing cycle. If you need higher volume, upgrade to an Enterprise plan". Resources are de-duplicated within a 24-hour UTC day. CONFIRMED.
- https://raw.githubusercontent.com/xdevplatform/docs/main/x-api/posts/filtered-stream/introduction.mdx: "Filtered Stream prioritizes data hydration and delivery, with approximately 4-5 seconds of P99 latency. For lower latency requirements, see Powerstream." Pay-per-use allows 1,000 rules per project and 1 connection; Enterprise allows 25,000+ rules and multiple connections.
- The files `consuming-streaming-data.mdx` and `powerstream/introduction.mdx` in the same repository give the same figure ("P99 latency of approximately 4-5 seconds"); I read these two in copies another researcher fetched from the repository earlier today.

Correction: the official text I could read says 4-5 s in three places. The 6-7 s figure exists only as a search summary of the live page, which could not be opened. Use "about 4-5 s at the 99th percentile" and drop the "4-7 s" range.

## 11. Regulators: PARTLY

Notes' statements: copy_trading_smart_money.md lines 202-203 and 228; regulation_access_conduct_tax.md lines 248-249.

CFTC advisory of 25 February 2026 (release 9185-26 in the notes): COULD NOT OPEN. All of www.cftc.gov was refused, including release 9237-26 and both parallel CFTC complaints.

Van Dyke: charges and amount CONFIRMED from the indictment; announcement date not confirmed.
- Source: https://www.justice.gov/usao-sdny/media/1437781/dl (indictment, 14 pages, scanned; "26 Cr." number illegible).
- Counts: one, "Unlawful Use of Confidential Government Information for Personal Gain" (7 U.S.C. 6c(a)(3) and 13(a)(5)); two, "Theft of Nonpublic Government Information" (7 U.S.C. 6c(a)(4)(C) and 13(a)(5)); three, "Commodities Fraud" (7 U.S.C. 9(1) and 13(a)(5); 17 C.F.R. 180.1); four, "Wire Fraud" (18 U.S.C. 1343); five, a monetary transaction in criminally derived property (18 U.S.C. 1957), of about $300,000.
- Amounts: "more than $400,000 in illegal profits"; "In total, VAN DYKE profited approximately $409,881"; he "purchased approximately $33,934 worth of 'YES' shares" between about 27 Dec 2025 and 2 Jan 2026.
- The indictment refers to a brokerage balance of approximately $415,511 on "April 21, 2026", which is consistent with charges announced on 23 April 2026 but does not prove that date. The press release that would give it (https://www.justice.gov/usao-sdny/pr/us-soldier-charged-using-classified-information-profit-prediction-market-bets) was not requested, because the same site's press-release page for Spagnuolo returned a bot-verification page.

Spagnuolo: charges and amount CONFIRMED from the complaint; announcement date not confirmed.
- Source: https://www.justice.gov/d9/2026-05/u.s._v._spagnuolo_complaint.pdf (complaint 26 MAG 2020; sworn "this ___ day of May, 2026", with the day left blank).
- Counts: one, "Commodities Fraud" (7 U.S.C. 9(1) and 13(a)(5); 17 C.F.R. 180.1); two, "Wire Fraud" (18 U.S.C. 1343); three, "Money Laundering" (18 U.S.C. 1956).
- Amounts: he "personally profited more than approximately $1,200,000"; from 15 Oct to 4 Dec 2025 the AlphaRaccoon account "risked approximately $2,754,092 on approximately 25 Google Year in Search 2025 outcomes".
- The press release (https://www.justice.gov/usao-sdny/pr/google-employee-charged-insider-trading) was refused, so 27 May 2026 is not confirmed beyond "May 2026".

## 12. DeFi Rate October 2026 volume table: CONFIRMED

Notes' statement (platform_mechanics_costs_regulation.md lines 109, 218 and 243): $120.73B across eight US-regulated exchanges; Kalshi $98.15B; Polymarket US $14.77B.

Source opened: https://defirate.com/news/prediction-market-volume-reaches-120-7-billion-october/ (published 2 Nov 2026, by Cheryle Shepstone).
- "U.S. prediction market volume reached $120.73 billion in October 2026, up 64.1% from $73.58 billion in September, according to DeFi Rate's analysis of trading activity across eight exchanges."
- "Kalshi led with $98.15 billion, accounting for 81.3% of reported volume, followed by Polymarket US at $14.77 billion."

| Exchange | October 2026 | September 2026 |
|---|---|---|
| Kalshi | $98.15B | $60.85B |
| Polymarket US | $14.77B | $8.70B |
| Novig | $3.27B | $1.45B |
| Crypto.com / Nadex | $2.19B | $1.56B |
| Underdog Exchange | $1.98B | $721.5M |
| ProphetX | $306.3M | $240.7M |
| Gemini Titan | $42.1M | $44.1M |
| ForecastEx | $14.4M | $19.5M |
| Total | $120.73B | $73.58B |

Notional: yes. The methodology note reads "Trading volume is presented in U.S. dollars under the $1-per-reported-contract or native-volume-unit convention. The figures measure reported volume rather than cash exchanged at execution price."

Qualifiers:
- Combos (parlays) dominate: "at least $79.46 billion" of the total, including at least $66.86B on Kalshi (68.1% of its volume) and $8.60B on Polymarket US (58.2%).
- The table excludes the international Polymarket venue, and CME Group, ICE Futures U.S. and DKeX/Railbird, for which complete October totals were unavailable.

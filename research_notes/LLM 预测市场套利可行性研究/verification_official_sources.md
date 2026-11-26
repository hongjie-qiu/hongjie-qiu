# Verification log: key claims checked against official sources (PRELIMINARY - being updated)

Status of this file: work in progress, written 26 Nov 2026. Entries marked IN PROGRESS are not yet usable. A final version will replace this text.

Method: plain `curl` through the session proxy, default headers, public pages only. A host that answered with a bot checkpoint or challenge was not retried by other means.

## Summary so far

| # | Claim | Status |
|---|---|---|
| 1 | Polymarket international fee formula and theta by category, effective 20 Nov 2026 | CONFIRMED (official fee page + changelog); add "Other / General" = 0.05 |
| 2 | Polymarket rebate schedule | IN PROGRESS (rates confirmed in changelog; thresholds not yet seen in an official page) |
| 3 | Polymarket taker delay | PARTLY (50 ms on 17 Aug and 150 ms on 4 Sep 2026 confirmed in changelog; 18 Feb removal not in changelog; sports wording confirmed in help centre) |
| 4 | Polymarket CLOB rate limits | CONFIRMED via changelog entries of 8 Apr and 1 Jun 2026 |
| 5 | CLOB V2 cut-over 28 Apr 2026, pUSD | CONFIRMED (changelog); client-library status IN PROGRESS |
| 6 | Holding rewards 4% | IN PROGRESS |
| 7 | UMA resolution | IN PROGRESS |
| 8 | Polymarket US fees | IN PROGRESS (docs.polymarket.us fee page refused) |
| 9 | Kalshi fees, interest, rate limits | IN PROGRESS (interest 3.50% / $250 confirmed on help centre; fee PDF on kalshi.com refused) |
| 10 | X API pricing and stream latency | IN PROGRESS |
| 11 | CFTC advisory, Van Dyke, Spagnuolo | IN PROGRESS (cftc.gov and the DOJ press-release page refused) |
| 12 | DeFi Rate October 2026 table | IN PROGRESS |

## Claim 1 (confirmed)

- Source opened: https://docs.polymarket.com/trading/fees.md (HTTP 200, 26 Nov 2026). The URL https://docs.polymarket.com/programs/fee-and-rebate-changes-november-2026.md now returns the same bytes as the fee page.
- Effective date, from https://docs.polymarket.com/changelog/predictions.md entry "Nov 20, 2026": "Effective November 20, 2026 at 23:59 UTC on Polymarket.com".
- Formula as printed: `fee = C × feeRate × p × (1 - p)`, C = shares, p = price. "Makers are never charged fees. Only takers pay fees." Fees rounded to 5 decimal places; smallest fee 0.00001 USDC.
- Taker fee rate by category: Crypto BTC 5-minute and 15-minute up/down 0.05; Crypto all other 0.01; Sports including NFL and college football 0.05; Finance 0.05; Tech 0.05; Politics elections 0.05; Politics excluding elections and geopolitics 0.01; Economics 0.01; Culture 0.01; Weather 0.01; Mentions 0.01; Geopolitics 0; Combos 0.05; Other / General 0.05.
- Fee per share: theta 0.05 gives 1.25 cents at 50c, 1.05 cents at 70c, 0.2375 cents at 95c; theta 0.01 gives 0.25, 0.21 and 0.0475 cents; theta 0 gives nothing.

## Claims 3, 4, 5 (changelog quotes)

- "Aug 17, 2026 ... The taker delay on crypto markets is now `50ms`, down from `250ms`. The change took effect on August 17 at 11:00 UTC".
- "Sep 4, 2026 ... The taker delay on crypto markets is now `150ms`, up from `50ms`. The change took effect on September 4 at 14:00 UTC". No later delay entry up to 25 Nov 2026.
- "April 8, 2026 ... CLOB POST /order - 5000 every 10s (500/s) - (BURST)"; "Jun 1, 2026 ... CLOB POST /order - 120000 every 10 minutes (200/s) - (SUSTAINED) ... CLOB POST /orders - 2000 every 10s (200/s) - (BURST)".
- "Apr 28, 2026 CLOB V2 is live on production"; 17 Apr entry: "pUSD replaces USDC.e as the collateral token".

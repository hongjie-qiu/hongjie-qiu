# Direct verification of key track-record sources (added 2026-11-19, late in the session)

After the four research notes were written, network access to four hosts was approved and the pages below were
downloaded and read in full by the coordinator. Items in this file are therefore **read directly from the page**
and supersede the "[S] snippet only" grade that the same items carry in `track_record_verification.md` and
`strategy_rules.md`. What a page says is still only as good as the page: the press item is a named public-record
ranking; the book summary is a secondary relay of a book whose own numbers are self-reported to its authors.

## 1. Swedish income ranking, income year 2021 - VERIFIED ON PAGE

Source: Nyheter24, "De tjänade mest pengar 2021 – Bianca Ingrosso yngst på listan", published 2023-01-02
(https://nyheter24.se/nyheter/ekonomi/1118106-de-tjanade-mest-pengar-2021-bianca-ingrosso-yngst-pa-listan).
The article lists "de 100 personer med högst inkomst i Sverige under inkomståret 2021" (the 100 people with the
highest income in Sweden in income year 2021). Entry number 15 in the list reads verbatim:

> "Kristjan Kullamägi, 34, Nacka. 360 miljoner. Daytrader."

(SEK 360 million; neighbours in the list: no. 14 Åsa Christina Riisberg 388 million, no. 16 Jan Axel Bengtsson
359 million; no. 1 Märta Andreen 1,677 million.) This is a named, press-published ranking drawn from Swedish
public tax data. It confirms a very large taxable income for 2021; it does not by itself show account equity,
percentage returns, or anything about other years.

## 2. Unnamed trader, income year 2020 - VERIFIED ON PAGE (identity still an inference)

Source: Dagens PS, "Han hade högst lön i Sverige – 168 miljoner"
(https://www.dagensps.se/bors-finans/han-hade-hogst-lon-i-sverige-168-miljoner/). Verbatim:

> "... en börshandlare i 35-årsåldern som kvalar in på en tolfteplats över de högsta kapitalinkomsterna i Sverige
> med 304 miljoner."

(A stock trader aged about 35 who places twelfth among the highest capital incomes in Sweden with SEK 304
million.) The page does not name him and does not mention Arboga; the link to Kullamägi rests on his own
statement that he was a top-15 individual taxpayer two years running and on the match with the tax-derived
series. Treat as "consistent with, not proof of".

## 3. Summary of the Market Wizards chapter - VERIFIED ON PAGE (secondary relay of the book)

Source: Complete Trader's Edge, Louw van Riet, "Kristjan Kullamägi (Qullamaggie): The $105 Million That Lasted a
Few Days", dated 2026-08-16 (https://completetradersedge.com/kristjan-kullamagi-qullamaggie/). It presents itself
as an account of Chapter 1 ("From Living to Trade to Trading to Live") of *Market Wizards: The Next Generation*
(Schwager and Coyle, 2026) and states: "Figures as reported in Chapter 1 ... Complete Trader's Edge has not
audited the underlying statements." What the page says:

- Account curve as told in the chapter: spring 2011 about $5,000 (first live account, funded by security-guard
  shifts); 2011-2013 three blow-ups (two months, five months, almost a year); profitable from 2013 on the fourth
  attempt; **January 2020 $3.5 million; December 2020 $36 million** ("a gain close to 1,000% in a single year");
  **November 2021 $105 million** ("the last leg, $65m to $105m, took about six weeks"); **mid-2022 roughly $45
  million** ("approximately $60 million lost from the peak").
- Leverage at the top: "At the peak he was leveraged long to the tune of $150 million."
- 2022: "The market topped near the end of 2021. His own trend indicator turned. He ignored it, came into
  December 2021 aggressive, and stayed aggressive through a downtrending 2022, buying breakouts and episodic
  pivots in exactly the market condition where his own rule says not to." About half of the roughly $60 million
  was "the surrender of open profits"; the rest "an accumulation of small and mid-size losses", with "no single
  catastrophic trade". The article calls the regime filter "the rule whose abandonment cost him $60 million".
- After 2022: "He was profitable again in 2023 and 2024, but the returns were moderate"; he grades his own 2024
  "a D-minus" in what he calls "a five-star year full of episodic pivot opportunities"; he bought a yacht at the
  end of 2021 and has traded while travelling; "Distraction on market days costs money in a method where the
  entry window is the first five minutes."
- Verification as described there: "George Coyle, who co-wrote the book, reviewed the underlying statements and
  describes what he found: loss after loss after loss, with most trading days showing several unprofitable
  same-day entries and exits." (So: the co-author reviewed statements; this is not an audit and no
  return/drawdown table is given on the page.)
- Win rate: he "estimates that between 25% and 30% of his trades are winners".
- Risk rules as listed: "Risk 0.5% or less per trade, 1% at absolute maximum"; stop at the low of the day on
  longs / high of the day on shorts; "If the low of the day is further away than one average daily true range,
  he does not take the trade".
- Setups: "The episodic pivot. This is his main strategy now. He learned it from Pradeep Bonde of Stockbee"; he
  "does not want a fourth setup".
- Examples given: in February 2020 he bought mask makers APT and LAKE as episodic pivots and shorted them the
  following week; he held Tesla through its 2020 move.

## 4. Could not be read

- `app.qullamaggiedeepdive.com/stats` (the fan-run site with the tax-derived yearly series 2014-2022 and the
  journal statistics) is a JavaScript application; the downloaded HTML contains no data. Its figures remain
  third-party and unverified here. Note that its 2021 dollar figure (about $42 million) is what SEK 360 million
  converts to at 2021 exchange rates, and its 2020 figure (about $33 million) matches SEK 304 million, so the two
  press items above are consistent with that series for those two years.

## 5. A point of contact with the backtest

The chapter's own explanation of the 2022 loss - trading breakouts and EPs while the regime filter was off - can
be set beside the backtest (`own_backtest.md`): the rule-based breakout test has its worst years in 2022 (average
-0.39R per trade), 2011 and 2017, and its best in 2010, 2013 and 2020; mask-maker APT's February 2020 gap is among
the largest winners of the rule-based EP test (+155% in ten sessions).

# Free daily US-equity data reachable from this container

Checked 2026-11-19, 03:50–05:00 UTC, with real requests from this container (curl / git through the policy proxy).

Status legend: **VERIFIED** = the request succeeded here (HTTP code, bytes shown) · **GATED** = host reachable, file needs a login · **BLOCKED** = proxy refuses the host (CONNECT 403) · **NOT FOUND**.

## 0. Read this first

**Recommended stack**

| Need | Use | Why |
|---|---|---|
| OHLCV incl. delisted names, 2019 → 2026-01 | HF `siddharthmb/stocks-ohlcv` (+ `stocks-splits`, `stocks-symbols`) | Only reachable source with full OHLCV for names that later delisted. Raw prices, 1.21 GB CSV. |
| OHLCV 2026-01-29 → today, long history for survivors | HF `defeatbeta/yahoo-finance-data` `stock_prices.parquet`; Yahoo chart API for single tickers | Refreshed daily (last bar 2026-11-17). Survivors only. |
| Point-in-time universe, market cap, sector; close/volume of delisted names after 2026-01 | GitHub `rreichel3/US-Stock-Symbols` git history | One Nasdaq-screener snapshot per trading day since 2021-02. No open/high/low. |
| 2005–2018 history | qlib zip (1999 → 2020-11-10), HF Stooq mirror (2005-02-25 → 2026-02-18), pystock (2009 → 2017-03) | All survivor-biased before 2015; see §6. |
| Earnings dates with before-open / after-close | HF `ZipLime/earnings-calendar` | 458k SEC 8-K releases 2003 → 2026-11, delisted companies included. |
| Factors, benchmarks | Ken French library; Yahoo chart API | Both now reachable. |

**Network state now (differs from the brief)**

- Now reachable: `huggingface.co` (+ CDN `us.aws.cdn.hf.co`), `query1`/`query2.finance.yahoo.com`, `api.nasdaq.com`, `mba.tuck.dartmouth.edu`. The allowlist request evidently went through during this run.
- `stooq.com`: CONNECT is accepted but the TLS handshake is reset every time (3 attempts). Unusable; use the HF mirror in §4.
- Still BLOCKED: kaggle.com, sec.gov, data.sec.gov, zenodo.org, archive.org, jsdelivr, dolthub.com, `*.github.io`, gist.githubusercontent.com, fred.stlouisfed.org, cdn.cboe.com, nasdaqtrader.com, www.nasdaq.com, data.nasdaq.com, finance.yahoo.com (HTML), stooq.pl, datasets-server.huggingface.co.
- `api.github.com` and `codeload.github.com` answer 403 from the session's GitHub gateway ("not enabled for this session").
- Also reachable, nothing useful found there: gitlab.com, bitbucket.org, storage.googleapis.com, s3.amazonaws.com (the old Quantopian quandl bundle now returns 403 AccessDenied), media.githubusercontent.com (Git LFS).

**Tricks that work here**

- `https://raw.githubusercontent.com/<owner>/<repo>/HEAD/<path>` resolves the default branch; no guessing.
- `git ls-remote https://github.com/<owner>/<repo>` and `git clone --filter=blob:none --no-checkout --depth 1 …` work for public repos (about 200 KB each), then `git ls-tree -r --name-only HEAD` lists every file. Any commit is fetchable at `raw.githubusercontent.com/<owner>/<repo>/<sha>/<path>`.
- GitHub release assets and the HF CDN honour explicit byte ranges (`curl -L -r A-B`), so a zip central directory or parquet footer can be read without the whole file. Suffix ranges (`-r -N`) return 501 on GitHub release assets.
- HF file listing: `https://huggingface.co/api/datasets/<repo>/tree/main/<dir>?recursive=true&limit=1000` (paginate with the `Link: rel="next"` header).
- Yahoo chart API needs `-A 'Mozilla/5.0'`. curl's default UA and a `python-requests` UA get 429. Ten consecutive requests at 0.5 s spacing returned 200.
- `api.nasdaq.com` needs a browser UA plus `-H 'Accept: application/json, text/plain, */*'`.

**Limits of this survey**

- Web search was available for only 4 queries (the per-turn budget was exhausted by other agents). GitHub discovery after that relied on file-tree listings of about 50 repos I could name, curated awesome-lists on raw GitHub, and the HF Hub's own dataset catalogue API. A GitHub-hosted full-universe OHLCV dump for 2021–2026 may exist that I did not find.
- About 285 MB of data was downloaded in total (121.6 MB of it the three pystock initial tarballs, kept on disk), plus a 45 MB pyarrow wheel into the scratchpad. Large files were inspected by byte range only; row counts and date ranges for those come from footers, central directories and sampled slices.

## 1. pystock-data (GitHub) — VERIFIED

Base: `https://raw.githubusercontent.com/eliangcs/pystock-data/HEAD/` (default branch is `gh-pages`; `master` also resolves).

| Path | Status | Coverage | Symbols | Contents |
|---|---|---|---|---|
| `index.txt`, `<year>/index.txt` | 200 | lists years 2015, 2016, 2017 and every tarball | – | plain text, one name per line |
| `2015/0001_initial.tar.gz` | 200, 42,430,604 B | 2009-01-02 → 2015-03-20 | 1,980 | `prices.csv`, `reports.csv`, `symbols.txt` |
| `2015/0002_initial.tar.gz` | 200, 39,865,044 B | 2009-01-01 → 2015-03-20 | 2,061 | `prices.csv` only |
| `2015/0003_initial.tar.gz` | 200, 39,268,414 B | 2009-01-01 → 2015-03-20 | 2,066 | `prices.csv` only |
| `YYYY/YYYYMMDD.tar.gz` × 515 | all 200; median 290,555 B (min 154, max 760,173) | first `2015/20150323`, last `2017/20170331` | ~6,000 per day | `symbols.txt`, `prices.csv`, `reports.csv` |

- All 518 tarballs listed in the index files exist. Counts: 2015 = 3 initial + 199 daily, 2016 = 253, 2017 = 63. No year directories before 2015 or after 2017.
- Total size 270.3 MB (initial 121.6 MB + daily 148.7 MB).
- The 15 weekdays without a file are all NYSE holidays.
- A daily file is named after its last trading day and holds two trading days (that day and the previous one).
- There is **no `splits.csv` or `dividends.csv`**. Corporate actions must be inferred from `adj_close` (below).

Samples (prices.csv has CRLF line endings; symbols.txt is tab-separated):

```
symbols.txt   XXII<TAB>22nd Century Group
              FAX<TAB>Aberdeen Asia-Pacific Income Fund Inc
              IAF<TAB>Aberdeen Australia Equity Fund Inc
prices.csv    symbol,date,open,high,low,close,volume,adj_close
              ETF,2015-03-23,12.67,12.67,12.59,12.61,26000,12.61
              ETF,2015-03-20,12.69,12.69,12.57,12.60,22800,12.60
              FCO,2015-03-23,9.25,9.42,9.25,9.42,38100,9.42
reports.csv   symbol,end_date,amend,period_focus,fiscal_year,doc_type,revenues,op_income,net_income,eps_basic,eps_diluted,dividend,assets,cur_assets,cur_liab,cash,equity,cash_flow_op,cash_flow_inv,cash_flow_fin
              WGA,2014-12-31,False,FY,2014,10-K,21924000.0,-1896000.0,-5507000.0,-0.21,-0.21,0.0,13554000.0,13389000.0,2470000.0,6859000.0,11084000.0,873000.0,7120000.0,-1598000.0
```

**Adjustment behaviour**

- `open/high/low/close` are **raw, as traded**. AAPL 2014-06-06 close 645.57, 2014-06-09 close 93.70.
- `adj_close` is Yahoo's split- and dividend-adjusted close **as of the crawl date**. In the initial files that date is 2015-03-20 (AAPL 2009-01-02: close 90.75, adj_close 12.23).
- A daily file is crawled before the next open, so a split or dividend going ex on day T+1 already shows in the row for T. NFLX 7:1 on 2015-07-15: file `20150714` has `2015-07-14 close 702.60, adj_close 100.37`, and file `20150715` repeats that row. The README warns the adjustment may only appear one file later, so take `adj_close` from the newest file that mentions a date: event factor for T+1 = `adj_close(T) / close(T)`.
- `volume` is Yahoo's split-adjusted volume as of the crawl, so it is inconsistent with the raw prices before a split. AAPL 2014-06-04 shows 83,870,500 (7× the shares actually traded). For the last pre-split day the first file has raw volume and the next file the adjusted one (NFLX 2015-07-14: 2,811,200 then 19,736,500).

**Survivorship**

- The initial files hold only symbols listed on NASDAQ.com on 2015-03-20: 6,036 symbols with prices (6,121 in symbols.txt), 7,754,593 rows, no duplicate (symbol, date).
- Names delisted before March 2015 are absent (checked: EK, BBI, LEH, WYE, GENZ, HNZ, DELL, NYX, COV, FRX and others). So 2009 → 2015-03 is survivor-biased.
- 2015-03-23 → 2017-03-31 is genuinely point-in-time. FDO's last row is 2015-07-02 and it leaves symbols.txt on 2015-07-06. Of 6,093 symbols on 2015-03-23, 1,023 are gone by 2017-03-31.
- QQQ is present; SPY and IWM are not (the NASDAQ.com company list has no NYSE Arca ETFs).

**Defects found in the 38 daily files sampled**

- Empty archives: `2015/20150610`, `2016/20161117`, `2017/20170323`. The next day's file covers the missing day.
- `2015/20150406` contains its content three times, with a repeated header line.
- `2016/20161010` has an empty prices.csv (covered by `20161011`).
- Partial crawls: `20160822`, `20160824`, `20160901`, `20160902`, `20160906`, `20160907`, `20160908`. The next file repairs 08-22 and 08-24. For 2016-09-01, 09-02, 09-06 and 09-07 the best coverage across files is 4,982 / 5,183 / 5,183 / 5,553 of ~6,000 symbols (`20160909` was not sampled).
- Holiday files (e.g. `20150703`, `20161226`, `20170102`) add a few stray rows dated on the holiday.

## 2. GitHub-hosted price and universe data

| Source (raw URL pattern) | Status | Coverage | Symbols | Delisted? | Adjusted? | Format / notes |
|---|---|---|---|---|---|---|
| `rreichel3/US-Stock-Symbols` — `raw.githubusercontent.com/rreichel3/US-Stock-Symbols/<sha>/{nasdaq,nyse,amex}/<ex>_full_tickers.json` | VERIFIED 200; 1.5–1.9 MB + 1.1–1.2 MB + 0.1 MB per day (~380 KB with `--compressed`) | 1,496 commits on 1,461 dates, 2021-01-30 → 2026-11-19, one per trading day, no gap over 4 days | 7,144 (2021-03-04), 7,551 (2023-09-19), 7,290 (2026-11-17) | **Yes, point-in-time.** The 2021-03 snapshot has TWTR, SIVB, BBBY. 45% of 2021-03 symbols are gone by 2026-11. | Raw close and raw volume | JSON list: `symbol, name, lastsale, netchange, pctchange, volume, marketCap, country, ipoyear, industry, sector`. **No open/high/low.** Stocks only (no SPY). |
| `fulifeng/Temporal_Relational_Stock_Ranking` — `…/HEAD/data/google_finance/{NASDAQ,NYSE,NYSEAMERICAN}_<TICKER>_30Y.csv` | VERIFIED 200 (AAPL 455,971 B); 8,535 files, about 1.4 GB (estimate from 120 HEADs) | 1987-12-11 → 2017-12-08 | 3,273 + 3,162 + 2,100 | Only names delisted after Dec 2017 | Split-adjusted, not dividend-adjusted (AAPL 2014-06-05 = 92.48) | `,Open,High,Low,Close,Volume`; index like `2017-12-08 16:00:00-05:00`. About 12% of files are header-only. Open is 0.0 on old rows. |
| `SunsetWolf/qlib_dataset` — `github.com/SunsetWolf/qlib_dataset/releases/download/v2/qlib_data_us_1d_latest.zip` | VERIFIED 200, 450,094,816 B (central directory read by range) | 1999-12-31 → **2020-11-10** (5,250 days) | 8,994 | Mostly no: 8,904 end in Nov 2020; 90 end 2012–2019 (ex-S&P 500 members) | Not inspected here (qlib convention is adjusted prices, with `factor` to recover raw) | 7 `.day.bin` fields per symbol (open, close, high, low, volume, change, factor). Has SPY, QQQ, IWM, ^GSPC, ^NDX, ^DJI and `instruments/{all,sp500,nasdaq100}.txt`. Tags v0–v3 hold the same US file (v0: 450,260,422 B). |
| `eliangcs/pystock-data` | VERIFIED | see §1 | | | | |
| `yfiua/index-constituents` — `…/HEAD/docs/YYYY/MM/constituents-{sp500,nasdaq100,dowjones}.csv` | VERIFIED 200 (2026/11 sp500: 9,907 B) | 23 months between 2018-07 and 2020-12, nothing for 2021-01 → 2023-06, every month 2023-07 → 2026-11 | index members | historical membership | – | CSV and JSON |
| `fja05680/sp500` — `…/HEAD/S%26P%20500%20Historical%20Components%20%26%20Changes%20(Updated).csv`, `sp500_ticker_start_end.csv` | VERIFIED 200 (5,530,907 B; 28,058 B) | last commit 2026-09-07 | S&P 500 | yes (membership) | – | already known |
| `datasets/nasdaq-listings`, `datasets/nyse-other-listings`, `datasets/s-and-p-500-companies` — `…/HEAD/data/{nasdaq-listed,other-listed,constituents}.csv` | VERIFIED 200 (268,020 / 875,978 / 53,594 B) | current listing, refreshed Nov 2026 | all listed | no | – | CSV |
| `Pubmarks/datasets` — `…/HEAD/data/stocks/<TICKER>/<YEAR>/ohlcv.csv` | VERIFIED 200 | 1980 → 2026, updated daily | 16 megacaps only | no | not checked | too narrow |
| `QuantConnect/Lean` — `…/HEAD/Data/equity/usa/daily/<ticker>.zip` | VERIFIED 200 (spy.zip 103,363 B) | SPY 1998-01-02 → 2021-03-31 | 21 sample tickers | – | raw, prices × 10,000 | sample data only |
| Full-universe OHLCV on GitHub covering 2021–2026 | **NOT FOUND** | | | | | see the search limitation in §0 |

Notes on `US-Stock-Symbols`:

- The snapshot date must be calibrated. In 15 of 18 sampled commits the data is the close of the commit's US date (commits land about 00:15 UTC); in 3 (2025-03-25, 2026-11-11, 2026-11-19) it is the previous trading day's close. Match AAPL `lastsale` against a reference close (snippet in §7).
- The commits of 2021-01-30 are malformed (several JSON arrays concatenated). 2021-02-05 onwards parse cleanly.
- A full `git clone` is estimated at about 0.4 GB (12 commits packed to 3.2 MiB). Fetching by SHA with `--compressed` is about 0.57 GB for all days.

## 3. Factors, benchmarks, earnings dates

| Need | Source | Status | Coverage | Notes |
|---|---|---|---|---|
| FF 3 factors daily | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip` | VERIFIED 200, 178,326 B (modified 2026-10-27) | 1926-07-01 → 2026-09-30 | Percent units; text preamble, CRLF, copyright footer |
| Momentum (UMD) daily | `…/ftp/F-F_Momentum_Factor_daily_CSV.zip` | VERIFIED 200, 85,338 B | 1926-11-03 → 2026-09-30 | Column `Mom` |
| Other French files | `…/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip`, `F-F_ST_Reversal_Factor_daily_CSV.zip`, `F-F_LT_Reversal_Factor_daily_CSV.zip`, `10_Portfolios_Prior_12_2_Daily_CSV.zip`, `25_Portfolios_ME_Prior_12_2_Daily_CSV.zip`, `10_Industry_Portfolios_daily_CSV.zip` | VERIFIED 200 (HEAD) | same vintage | |
| FF daily on GitHub / PyPI | – | NOT FOUND | | Only monthly copies seen in repo trees (`bashtage/arch` `arch/data/frenchdata/frenchdata.csv.gz`, `bashtage/linearmodels` `linearmodels/datasets/french/french.csv.bz2`) |
| SPY / QQQ / IWM daily | `https://query1.finance.yahoo.com/v8/finance/chart/SPY?period1=0&period2=9999999999&interval=1d&events=div%2Csplits` with `-A 'Mozilla/5.0'` | VERIFIED 200 (SPY 860,788 B) | SPY 1993-01-29, QQQ 1999-03-10, IWM 2000-05-26, all → 2026-11-18 | JSON: split-adjusted OHLCV, `adjclose`, dividend and split events. Delisted tickers return 404 (TWTR). |
| same, alternative | `https://api.nasdaq.com/api/quote/SPY/historical?assetclass=etf&fromdate=2016-11-19&todate=2026-11-19&limit=9999` (stocks: `assetclass=stocks`) | VERIFIED 200, 2,513 rows | rolling 10 years only | Split-adjusted; delisted symbols return "Symbol not exists" |
| same, GitHub-hosted | qlib zip (SPY, QQQ, IWM, ^GSPC → 2020-11-10); `stefan-jansen/zipline-reloaded` `…/HEAD/src/zipline/resources/market_data/SPY_benchmark.csv` (returns, 1993-02-01 → 2018-04-27); LEAN `spy.zip` (→ 2021-03-31) | VERIFIED 200 | none reaches 2026 | |
| VIX daily | `https://raw.githubusercontent.com/datasets/finance-vix/HEAD/data/vix-daily.csv` | VERIFIED 200, 482,200 B | 1990-01-02 → 2026-09-22 | |
| Earnings dates (best) | HF `ZipLime/earnings-calendar` — see §4 | VERIFIED | 2003-04-25 → 2026-11-13 | Session flag and first tradeable session; delisted included |
| Earnings dates | HF `FinzData/sec-earnings-release-dates`, HF `siddharthmb/stocks-earnings-earnings_calendar`, HF `defeatbeta` — see §4 | VERIFIED | | |
| Earnings calendar by date | `https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD` | VERIFIED 200 (10–65 KB per day) | 2008-01 → future (2007-10-23 and earlier return 0 rows) | `symbol, eps, epsForecast, surprise, noOfEsts, fiscalQuarterEnding, time`. Only currently listed companies appear. `time` is `time-not-supplied` for past dates (pre-market / after-hours only for current dates). About 4,750 requests for full history. |
| Earnings dates on GitHub | pystock `reports.csv` only | VERIFIED | 2015-03 → 2017-03 | The file date in which a 10-Q/10-K first appears is roughly the filing date, not the announcement |

## 4. Hugging Face — reachable now, all checked with curl

File URL pattern: `https://huggingface.co/datasets/<repo>/resolve/main/<path>` (302 to `us.aws.cdn.hf.co`, ranges supported, about 5 MB/s measured).

### Prices

| Repo / path | Status, size | Coverage | Symbols | Delisted? | Adjusted? | Gated | Notes |
|---|---|---|---|---|---|---|---|
| `siddharthmb/stocks-ohlcv` / `ohlcv.csv` | 200, 1,210,415,158 B | 2011-01-03 → 2026-01-28 | per day: 3,949 (2011-06), 5,037 (2015-06), 6,040 (2017-12), 7,131 (2018-06), 7,550 (2019-06), 8,339 (2021-03); stocks and ETFs | **Yes from about 2019.** 2019-06-03 has CELG, RHT, APC, AGN, VIAB; 2021-03-04 has TWTR, SIVB, ATVI, XLNX, FRC and covers 98.5% of that day's Nasdaq-screener common stocks. 2018-06-01 lacks TWX, MON, AET, ESRX; 2015-06-01 lacks FDO, YHOO, CELG. | **Raw, unadjusted** (matches screener raw close for AAPL, TSLA, NVDA, AMZN, GOOGL, GME on 2021-03-04) | no | Sorted by date then symbol: `date,act_symbol,open,high,low,close,volume`. No dataset card or licence. Table names and schema match the DoltHub `post-no-preference` stocks database (inference). Static snapshot of 2026-01-29. |
| `siddharthmb/stocks-splits` / `split.csv` | 200, 109,667 B | 2014-03-28 → 2026-01-23, 3,385 rows | | | | no | `act_symbol,ex_date,to_factor,for_factor`. **Contains spurious earlier duplicates** (AMZN 2022-05-26 and 2022-06-06; GOOGL 2022-06-30 and 2022-07-18; DXCM ×3). Validate against the price jump. |
| `siddharthmb/stocks-dividends` / `dividend.csv` | 200, 10,979,056 B | not determined (sorted by symbol; first row is A 2006-11-01) | | | | no | `act_symbol,ex_date,amount` (first 300 bytes read) |
| `siddharthmb/stocks-symbols` / `symbol.csv` | 200, 2,230,769 B | `last_seen` 2017-10-26 → 2026-01-24 | 22,411 (16,094 non-ETF) | 10,129 with `last_seen` before 2026 | | no | `last_seen` is a delisting-date proxy (TWTR 2022-10-23, SIVB 2023-03-26, CELG 2019-11-17) |
| `defeatbeta/yahoo-finance-data` / `data/US/stock_prices.parquet` (old name `bwzheng2010/…` redirects) | 200, 475,822,445 B | 1994-11-30 → 2026-11-17, refreshed daily (`spec.json`) | 12,593 incl. units, warrants, preferreds, some ETFs; 37,492,636 rows | No. TWTR, SIVB, ATVI, VMW, SPLK, CELG absent. Names delisted since about 2025 stay as stale series (ZYXIQ ends 2026-03-26). | Split-adjusted, **not** dividend-adjusted (AAPL 1994-11-30 = 0.3326); volume split-adjusted | no (ODC-By) | `symbol, report_date(str), open, close, high, low (decimal128), volume`. Sorted by symbol, 375 row groups. QQQ is stale (ends 2026-09-11); SPY and IWM are current. |
| `defeatbeta/…` / `data/US/stock_split_events.parquet`, `stock_dividend_events.parquet` | 200, 70,142 B / 739,868 B | 1992 → 2026-11-17 / 1991 → 2026-11-17 | 4,560 / 5,110 | | | no | `symbol, report_date, split_factor ("7:1")` / `amount` |
| `autoprogrammer/historical_data` / `daily/us/{nasdaq stocks/{1,2,3}, nyse stocks/{1,2}, nysemkt stocks, nasdaq etfs, nyse etfs/{1,2}}/<ticker>.us.txt` (URL-encode the space) | 200 (aapl 757,455 B); about 11,900 files, 1.83 GB | 2005-02-25 → 2026-02-18 | about 8,400 stock files (48 empty) + about 3,500 ETF files | No (TWTR, SIVB, ATVI absent) | **Fully adjusted**, splits and dividends, volume too (SPY 2010-01-04 = 87.44) | no | Mirror of the Stooq US daily dump: `<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>`. Has SPY, QQQ, IWM. |
| `AYUSHKHAIRE/all-stock-market-data-daily-updates` / `<FIRST LETTER>/<TICKER>.csv` | 200 (AAPL 390,429 B); 19,700 files, 4.2 GB | 2010-01-04 → 2026-11-17 (card: updated 17 Nov 2026) | 16,878 per card, incl. OTC; no ETFs (SPY absent) | No | Split-adjusted (Yahoo) | no (CC0) | `open,volume,high,low,close,timestamp` (epoch seconds). Per-ticker files suit incremental refresh. |
| `Zihan1004/FNSPID` / `Stock_price/full_history.zip` | 200, 589,525,596 B (2.95 GB unzipped) | all files → 2020-07-02; a subset continues → 2023-12-28 | 7,693 | Names listed in July 2020 and delisted later (TWTR, BBBY, ATVI, VMW), mostly ending 2020-07-02 | Yahoo `close` + `adj close` | no (CC BY-NC 4.0) | **Splice defect**: the pre-2020-07 segment is not re-adjusted for later splits (AAPL 364.11 on 2020-07-02 → 93.46 on 2020-07-06). Column order differs between files; rows are newest first. |
| `metalwhale/stock_data` / `us.zip` | 200, 722,573,839 B (4.03 GB unzipped) | → 2024-07-22 | 10,549 | No (survivors of July 2024) | `close` split-adjusted + `adjclose`; some files add `dividends,splits` | no | qlib Yahoo-collector CSVs. Date format varies; some stamps are shifted (`2022-07-21 20:00:00-04:00` means 2022-07-22). |
| `Kicel/daily-stocks` / `train-stocks.parquet` (+ `test-stocks.parquet`) | 200, 435,167,700 B | 1962-01-02 → 2023-12-29 | 8,203 | No | no adj column | no | 18.2 M rows |
| `chuyin0321/timeseries-daily-stocks` / `data/train-0000{0,1}-of-00002-*.parquet` | 200, 146,600,928 B + 145,391,737 B | 1979-12-31 → 2023-09-08 | not counted | not checked | has `adj_close` | no | 8.4 M rows |
| `yimisiyang/us-stock-market-db` / `market.db.gz` | 200, 59,495,649 B | 2018-01-02 → 2026-11-18 per card | 647 (S&P 500 + Nasdaq 100) | No | Yahoo | no | SQLite; not downloaded |
| `Traders-Lab/TroveLedger` / `Stock/<SYM>/<SYM>.days.valid.parquet` | 200 (listing) | daily updates | 679 US symbols | No | adjusted | no (CC BY-NC-SA) | large caps only; also hourly and minute bars |
| `paperswithbacktest/Stocks-Daily-Price` | **GATED** — 401 `GatedRepo` | 1962 → 2026 per file names | – | – | – | manual approval | Their own list says "downloads are gated". |
| `HexQuant/Stocks-Daily-Price`, `doctor235/…`, `weib08/…` | 200 (HEAD only) | – | – | – | – | no | Ungated re-uploads of the gated dataset above. Deliberately not downloaded: the source is gated with licence "other". Your call. |
| WIKI/Quandl-prices mirror; anything named "stooq" or "delisted" | NOT FOUND via the Hub catalogue | | | | | | Hub search matches repo names only |

How much of each day's listed universe (from the screener snapshots) a source still carries:

| Source | common stocks listed 2021-03-04 | listed 2023-09-19 | listed 2026-11-17 |
|---|---|---|---|
| defeatbeta `stock_prices` (2026-11) | 74.1% | 89.7% | 99.7% |
| Stooq mirror (2026-02) | 65.6% | 76.5% | 90.9% |
| metalwhale `us.zip` (2024-07) | 73.7% | 90.4% | 78.1% |
| FNSPID (2020-07 base) | 83.0% | 64.5% | 54.2% |
| qlib US (2020-11) | 92.6% | 70.4% | 58.6% |

### Earnings and identifiers

| Repo / path | Status, size | Coverage | Rows / symbols | Delisted? | Notes |
|---|---|---|---|---|---|
| `ZipLime/earnings-calendar` / `data/announcements/part-00000.parquet` | 200, 15,411,299 B (downloaded) | 2003-04-25 → 2026-11-13 | 458,349 releases, 13,608 CIKs, 12,685 tickers | **Yes** (TWTR → 2022-07-22, SIVB → 2023-01-19, CELG → 2019-10-31, LEH → 2008-09-10) | SEC 8-K Item 2.02. Columns include `cik, ticker` (as of filing day), `ticker_confidence, announced_at, announced_date_et, announced_time_et, session, first_tradeable_session, form`. Sessions: 229,610 after_close, 140,006 pre_market, 88,134 market_hours. 24,203 rows have no ticker. Tickers are reused across companies (TWTR 2003–2007 is Tweeter), so key on `cik`. Apache-2.0. |
| `ZipLime/earnings-calendar` / `data/earnings/part-00000.parquet` | 200, 16,549,580 B (footer only) | 2009-01-09 → 2026-09-30 | 262,402 | yes | Adds EPS, revenue, year-on-year change, `sue` |
| `ZipLime/security-master` / `data/identifiers/part-00000.parquet`, `data/issuers/part-00000.parquet` | 200, 1,781,685 B / 724,202 B (downloaded) | spans 2006-01-03 → 2026-11-16 | 29,628 ticker spans, 26,939 tickers, 23,655 issuers | **Yes** (LEH → 2008-09-19, YHOO → 2017-06-15) | `cik, kind, value, valid_from, valid_to, is_current`. Free historical ticker master; span ends approximate delisting. |
| `ZipLime/corporate-actions` / `data/{splits,dividends,adjustment_factors}/part-00000.parquet` | 200 (HEAD: 124,430 / 3,900,147 / 76,655 B) | not inspected | | | |
| `FinzData/sec-earnings-release-dates` / `data/earnings_dates.parquet` | 200, 3,114,562 B (downloaded) | 2004-08-23 → 2026-11-13 | 229,885 rows, 4,330 tickers | No (GME, TWTR absent; "free sample") | `cik, ticker, report_date, filed, accepted_et, timing` (before_open / during_market / after_close) |
| `siddharthmb/stocks-earnings-earnings_calendar` / `earnings_calendar.csv` | 200, 3,230,781 B (downloaded) | 2020-01-22 → 2026-03-06 | 108,299 rows, 7,110 symbols | Yes (TWTR 2022-07-22) | `act_symbol,date,when`; `when` is blank in 26% of rows |
| `siddharthmb/stocks-earnings-eps_history` / `eps_history.csv` | 200, 3,984,073 B (first 500 bytes read) | not determined (first rows are A from 2016-10) | | | `act_symbol,period_end_date,reported,estimate` |
| `defeatbeta/…` / `data/US/stock_earning_call_transcripts.parquet` | 200, 2,310,073,774 B | call dates 2005-10-11 → 2026-11-23 | 242,997 calls, 6,645 symbols | No | Only `symbol, fiscal_year, fiscal_quarter, report_date` were pulled (1.56 MB by range) into `earnings_call_dates.csv` (§8). AAPL and NVDA 2024 dates match. 5.8% of dates fall on a weekend. |
| `defeatbeta/…` / `data/US/stock_earning_calendar.parquet` | 200, 209,075 B (downloaded) | 2023-01-03 → 2026-11-18 only | 74,126 rows, 5,397 symbols | No | `symbol, report_date, time, fiscal_quarter_ending` |
| `defeatbeta/…` / `data/US/stock_sec_filing.parquet` | 200, 92,959,679 B (footer only) | filings 1993-08-13 → 2026-11-17 | 7,988,527 | not checked | `form_type, filing_date, acceptance_date_time` |
| `paperswithbacktest/Stocks-Quarterly-Earnings` | GATED (catalogue flag `manual`) | | | | |

## 5. Anything else in the reachable set

| Item | Status | Value |
|---|---|---|
| `git clone` of any public GitHub repo | VERIFIED (ls-remote, blobless and depth-12 clones) | Whole-repo downloads: pystock-data (270 MB), the Google Finance set (about 1.4 GB of CSV), US-Stock-Symbols history (about 0.4 GB) |
| `skfolio/skfolio-datasets` — `…/HEAD/datasets/nasdaq_dataset.csv.gz` | VERIFIED 200, 4,684,863 B | Close-only panel of Nasdaq names (not opened); no OHLCV |
| `AI4Finance-Foundation/FinRL-Trading` — `…/HEAD/data/sp500_historical_constituents.csv` | VERIFIED 200, 5,507,564 B | Second source of S&P 500 membership history |
| `JerBouma/FinanceDatabase` — `database/equities/<EXCHANGE>.csv` | seen in tree | Sector / industry metadata |
| PyPI, npm, conda packages bundling substantial US equity history | NOT FOUND | Repo trees show only toy sets: `arch` (S&P 500 index to 2018), `zipline-reloaded` (SPY returns to 2018), `skfolio` (20 stocks), `mplfinance`, `PyPortfolioOpt`. Wheels were not downloaded. |
| `pip install pyarrow` from PyPI | VERIFIED (26.0.1) | Needed for the parquet files; not installed system-wide |
| Kaggle snapshots, SEC EDGAR, DoltHub live database, Stooq | BLOCKED / unusable | DoltHub (`www.dolthub.com`) would refresh the best OHLCV source past 2026-01-28; worth an allowlist request |

## 6. Where delisted names actually exist

| Period | Full OHLCV incl. delisted | Close / volume only | Nothing free and reachable |
|---|---|---|---|
| before 2015-03 | qlib has 90 ex-S&P 500 names only | – | all other names delisted before March 2015 (every source is a later snapshot) |
| 2015-03 → 2017-03 | pystock daily snapshots (raw OHLC) | – | |
| 2017-04 → about 2019-05 | partial: names alive in Dec 2017 (Google Finance set, to 2017-12-08); names alive in mid-2019 (DoltHub export backfill); ex-S&P names in qlib | – | names delisted in 2018 that fall outside those three |
| about 2019-06 → 2026-01-28 | HF `siddharthmb/stocks-ohlcv` (raw) | US-Stock-Symbols from 2021-02 | |
| 2026-01-29 → today | survivors only (defeatbeta, Yahoo); names delisted in 2025–26 stay in defeatbeta as stale series | US-Stock-Symbols | open/high/low for names delisted after 2026-01-28 |

The date when the DoltHub export becomes survivorship-free is bracketed by six probed days: not yet on 2018-06-01, clearly by 2019-06-03.

## 7. Download and parse (tested here on samples unless marked)

Parquet reading needs `python3 -m pip install pyarrow`. Run parsers with `python3 -I`.

### 7a. Raw OHLCV with delisted names (HF, DoltHub export)

```bash
D=/home/user/hongjie-qiu/backtest/data/hf_dolt; mkdir -p "$D"; H=https://huggingface.co/datasets/siddharthmb
curl -L --retry 5 -C - -o "$D/ohlcv.csv"    $H/stocks-ohlcv/resolve/main/ohlcv.csv        # 1.21 GB, about 5 min
curl -L --retry 5 -o "$D/split.csv"         $H/stocks-splits/resolve/main/split.csv
curl -L --retry 5 -o "$D/dividend.csv"      $H/stocks-dividends/resolve/main/dividend.csv
curl -L --retry 5 -o "$D/symbol.csv"        $H/stocks-symbols/resolve/main/symbol.csv
```

```python
import numpy as np, pandas as pd

def load_dolt_ohlcv(csv_path, start='2018-01-01', end='2100-01-01', chunksize=2_000_000):
    """ohlcv.csv is sorted by date; columns date,act_symbol,open,high,low,close,volume (RAW, unadjusted)."""
    parts = []
    for ch in pd.read_csv(csv_path, chunksize=chunksize, dtype={'act_symbol': 'string'}):
        if ch['date'].iloc[-1] < start: continue
        if ch['date'].iloc[0] > end: break
        parts.append(ch[(ch['date'] >= start) & (ch['date'] <= end)])
    df = pd.concat(parts, ignore_index=True).rename(columns={'act_symbol': 'symbol'})
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values(['symbol', 'date'], ignore_index=True)

def split_adjust(df, split_csv):
    """Back-adjust RAW o/h/l/c and volume. split.csv has spurious early duplicates, so a split is applied only if
    the raw close really jumps on the ex_date: the observed log jump must be closer to the split ratio than to zero."""
    sp = pd.read_csv(split_csv, dtype={'act_symbol': 'string'}).rename(columns={'act_symbol': 'symbol'})
    sp['date'] = pd.to_datetime(sp['ex_date']); sp['ratio'] = sp['to_factor'] / sp['for_factor']
    sp = sp.drop_duplicates(['symbol', 'date'])
    df = df.sort_values(['symbol', 'date'], ignore_index=True)
    df['prev_close'] = df.groupby('symbol')['close'].shift(1)
    m = df.merge(sp[['symbol', 'date', 'ratio']], on=['symbol', 'date'], how='left')
    jump = np.log(m['prev_close'] / m['close']); want = np.log(m['ratio'])
    ok = m['ratio'].notna() & ((jump - want).abs() < 0.5 * want.abs())
    m['f'] = 1.0; m.loc[ok, 'f'] = m.loc[ok, 'ratio']
    m['cum'] = m.iloc[::-1].groupby('symbol')['f'].cumprod().iloc[::-1] / m['f']   # splits strictly after each row
    for c in ('open', 'high', 'low', 'close'): m[c + '_adj'] = m[c] / m['cum']
    m['volume_adj'] = m['volume'] * m['cum']
    return m.drop(columns=['prev_close', 'ratio', 'f']).rename(columns={'cum': 'split_factor'})
```

- Tested: the loader on a file assembled from six day-slices; `split_adjust` on AMZN around 2022-06-06 (2,447.00 becomes 122.35; the bogus 2022-05-26 row is ignored) and on synthetic 3:2, 1:15 and 11:10 cases. **Not run on the full 1.21 GB file.**
- A split whose ex-day coincides with a price move larger than half the split's log ratio is rejected by the rule (matters only for small ratios such as 11:10).
- Against Yahoo-derived data, 1,149 sampled symbol-days agree within 0.5% on 98–99% of open/high/low. Bad prints exist (TSLA 2021-03-04 high 873.94 against 668.45 implied by Yahoo), and volume on a split day can be wrong (AMZN 2022-06-06: 431,103). Clip highs and lows that sit far from open and close.
- `split.csv` starts 2014-03-28, so splits before that are not adjusted. Dividends (`dividend.csv`) are not applied here.
- Memory: a year is roughly 2–2.5 M rows. Load a few years at a time with `start`/`end`; this container's memory limit is shared and a process was OOM-killed while the tests ran.

### 7b. Recent data for survivors (HF defeatbeta) and single tickers (Yahoo)

```bash
D=/home/user/hongjie-qiu/backtest/data/hf_defeatbeta; mkdir -p "$D"; B=https://huggingface.co/datasets/defeatbeta/yahoo-finance-data/resolve/main/data/US
curl -L --retry 5 -C - -o "$D/stock_prices.parquet"          $B/stock_prices.parquet           # 476 MB
curl -L --retry 5 -o "$D/stock_split_events.parquet"         $B/stock_split_events.parquet
curl -L --retry 5 -o "$D/stock_dividend_events.parquet"      $B/stock_dividend_events.parquet
curl -sS -A 'Mozilla/5.0' -o SPY.json 'https://query1.finance.yahoo.com/v8/finance/chart/SPY?period1=0&period2=9999999999&interval=1d&events=div%2Csplits'
```

```python
import json, pandas as pd, pyarrow as pa, pyarrow.parquet as pq, pyarrow.compute as pc

def read_decimal_parquet(path, date_col='report_date', start=None, read_dictionary=('symbol',)):
    """defeatbeta stores prices as decimal128 and dates as strings: cast in Arrow before going to pandas."""
    t = pq.read_table(path, read_dictionary=list(read_dictionary),
                      filters=[(date_col, '>=', start)] if start else None)
    cols = {n: (pc.cast(t[n], pa.float64()) if pa.types.is_decimal(t[n].type) else t[n]) for n in t.column_names}
    df = pa.table(cols).to_pandas()
    df[date_col] = pd.to_datetime(df[date_col])
    return df            # prices: symbol, report_date, open, close, high, low, volume (split-adjusted)

def parse_yahoo_chart(text):
    r = json.loads(text)['chart']['result'][0]; q = r['indicators']['quote'][0]
    idx = (pd.to_datetime(r['timestamp'], unit='s', utc=True)
             .tz_convert('America/New_York').normalize().tz_localize(None))
    df = pd.DataFrame({k: q[k] for k in ('open', 'high', 'low', 'close', 'volume')}, index=idx)
    adj = (r['indicators'].get('adjclose') or [{}])[0].get('adjclose')
    if adj: df['adj_close'] = adj
    df.index.name = 'date'
    return df.dropna(subset=['close'])
```

- Tested: `read_decimal_parquet` on the dividend and calendar files (same writer and types); `parse_yahoo_chart` on the saved SPY response (8,510 rows). **The 476 MB price file itself was read only by range** (footer, the symbol column, 20 row groups).
- `split_factor` strings parse as `a, b = s.split(':'); ratio = float(a) / float(b)`.
- Splicing the two price sources: defeatbeta is split-adjusted as of today, the DoltHub export is raw. Compare them on an overlap day per symbol (close ratio = cumulative split factor) before joining.

### 7c. Point-in-time universe and closes (GitHub US-Stock-Symbols)

```bash
D=/home/user/hongjie-qiu/backtest/data/uss; mkdir -p "$D/raw"
git clone --filter=blob:none --no-checkout https://github.com/rreichel3/US-Stock-Symbols "$D/meta"      # 1.5 MB: commits and trees only
git -C "$D/meta" log --reverse --format='%H %cd' --date=format:%Y-%m-%dT%H%M%SZ > "$D/commits.txt"
while read sha ts; do for ex in nasdaq nyse amex; do f="$D/raw/${ts}_${ex}.json"
  [ -s "$f" ] || curl -sS --compressed --retry 3 -o "$f" "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/$sha/$ex/${ex}_full_tickers.json"
done; done < "$D/commits.txt"                                                                              # about 0.57 GB on the wire
```

```python
import json, pandas as pd

def parse_screener_json(text, exchange):
    num = lambda s: pd.to_numeric(pd.Series(s, dtype='string').str.replace(r'[$,%]', '', regex=True), errors='coerce')
    rows = json.JSONDecoder().raw_decode(text.lstrip())[0]      # 2021-01-30 commits hold several concatenated arrays
    d = pd.DataFrame(rows)
    return pd.DataFrame({'symbol': d['symbol'].str.strip(), 'name': d['name'], 'exchange': exchange,
                         'close': num(d['lastsale']), 'net_change': num(d['netchange']), 'pct_change': num(d['pctchange']),
                         'volume': num(d['volume']), 'market_cap': num(d['marketCap']), 'sector': d.get('sector'),
                         'industry': d.get('industry'), 'ipo_year': d.get('ipoyear'), 'country': d.get('country')})

def snapshot_trade_date(snap, commit_utc, ref_close, symbol='AAPL', tol=0.011):
    """snap: parsed NASDAQ file; commit_utc: tz-aware commit time; ref_close: RAW closes of `symbol` by trading date.
    Returns the trading day the snapshot describes (the commit's US date, or sometimes the day before)."""
    px = snap.loc[snap['symbol'] == symbol, 'close']
    if px.empty: return pd.NaT
    us_day = (commit_utc.tz_localize(None) - pd.Timedelta(hours=5)).normalize()
    cand = ref_close[(ref_close.index <= us_day) & (ref_close.index >= us_day - pd.Timedelta(days=6))]
    hit = cand[(cand - float(px.iloc[0])).abs() < tol]
    return hit.index[-1] if len(hit) else pd.NaT
```

- Tested on 19 snapshot files; the date function resolved all 18 calibration commits. The clone and the per-SHA fetch were each run, but the full 1,496-commit loop was not.
- AAPL has had no split since 2020-08, so Yahoo's `close` is a valid raw reference for every snapshot. A symbol's last appearance is its delisting (or rename) date.

### 7d. Smaller parsers

```python
import io, re, tarfile, zipfile, pandas as pd

PYSTOCK_COLS = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
def read_pystock_tar(path):
    """Handles CRLF, repeated header lines (2015/20150406) and empty archives."""
    with tarfile.open(path, 'r:gz') as tf:
        try: raw = tf.extractfile('prices.csv').read()
        except KeyError: return pd.DataFrame(columns=PYSTOCK_COLS)
    if not raw.strip(): return pd.DataFrame(columns=PYSTOCK_COLS)
    df = pd.read_csv(io.BytesIO(raw), dtype={'symbol': 'string'}, na_values=['null'])
    df = df[df['date'] != 'date']
    for c in PYSTOCK_COLS[2:]: df[c] = pd.to_numeric(df[c], errors='coerce')
    return df[PYSTOCK_COLS]

def build_pystock(tar_paths):
    """tar_paths in chronological order, initial files first. Keeps each (symbol, date) row as first published
    (raw OHLC) and adds adj_close_latest from the newest file that mentions that date."""
    frames = []
    for i, p in enumerate(tar_paths):
        d = read_pystock_tar(p); d['src'] = i; frames.append(d)
    allr = pd.concat(frames, ignore_index=True).dropna(subset=['close']).sort_values('src')
    first = allr.drop_duplicates(['symbol', 'date'], keep='first')
    last = allr.drop_duplicates(['symbol', 'date'], keep='last')
    out = first.merge(last[['symbol', 'date', 'adj_close']], on=['symbol', 'date'], suffixes=('', '_latest'))
    return out.sort_values(['symbol', 'date'], ignore_index=True)   # event factor on D+1 = adj_close_latest(D) / close(D)

def read_french_daily(zip_path):
    z = zipfile.ZipFile(zip_path); txt = z.read(z.namelist()[0]).decode('latin1')
    rows = [l.split(',') for l in txt.splitlines() if re.match(r'^\s*\d{8}\s*,', l)]
    hdr = next(l for l in txt.splitlines() if l.startswith(',')).split(',')[1:]
    df = pd.DataFrame(rows, columns=['date'] + [h.strip() for h in hdr]).drop_duplicates('date')
    df['date'] = pd.to_datetime(df['date'].str.strip(), format='%Y%m%d')
    return df.set_index('date').astype(float) / 100.0                # percent to decimal

def read_stooq_txt(path):                                            # HF mirror autoprogrammer/historical_data
    df = pd.read_csv(path); df.columns = [c.strip('<>').lower() for c in df.columns]
    df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
    df['symbol'] = df['ticker'].str.replace('.US', '', regex=False)
    return df[['symbol', 'date', 'open', 'high', 'low', 'close', 'vol']].rename(columns={'vol': 'volume'})

# Earnings events incl. delisted companies: the session a gap can first trade in
ann = pd.read_parquet('/home/user/hongjie-qiu/backtest/data/scout_tmp/hf_ziplime_earnings_announcements/announcements.parquet',
                      columns=['cik', 'ticker', 'announced_date_et', 'session', 'first_tradeable_session', 'form'])
ann = ann[ann.ticker.notna() & (ann.form == '8-K')]
```

Tested: `build_pystock` on the three initial tarballs plus five daily ones (7,791,077 rows, no duplicates, NFLX split visible); `read_french_daily` on both downloaded zips; `read_stooq_txt` on the GME sample; the announcements filter (429,664 rows). `build_pystock` holds every row in memory several times over (several GB for the full set); build it once and write the result to disk.

pystock download: `for p in $(curl -s …/HEAD/2016/index.txt); do curl -sS --retry 3 -o "2016/$p" "…/HEAD/2016/$p"; done` for each of 2015, 2016, 2017, or `git clone --depth 1` the repo.

## 8. Files already on disk

Everything is under `/home/user/hongjie-qiu/backtest/data/scout_tmp/` (626 MB), one directory per download. Nothing in it was executed.

| Directory | Contents |
|---|---|
| `pystock_initial_0001/`, `_0002/`, `_0003/` | the three initial tarballs and their extracted CSVs in `x/` (508 MB) |
| `pystock_daily_<date>/` × 38 | sampled daily tarballs with extracted files in `x/` |
| `hf_ziplime_earnings_announcements/announcements.parquet` | 458,349 earnings releases 2003 → 2026 |
| `hf_ziplime_security_master/{identifiers,issuers}.parquet` | historical ticker spans |
| `hf_finzdata_earnings_dates/earnings_dates.parquet` | 229,885 8-K release times |
| `hf_defeatbeta_stock_earning_call_transcripts_peek/earnings_call_dates.csv` | 242,997 call dates extracted by range |
| `hf_defeatbeta_stock_{earning_calendar,split_events,dividend_events}/` | small parquet files |
| `hf_dolt_stocks_{splits,symbols}/`, `hf_dolt_stocks_earnings_earnings_calendar/` | `split.csv`, `symbol.csv`, `earnings_calendar.csv` |
| `hf_dolt_ohlcv_slices/`, `hf_dolt_ohlcv_splitcheck/` | six single-day slices and two 5-day windows of `ohlcv.csv` |
| `french_F-F_*/` | 3-factor and momentum daily zips |
| `yahoo_chart_SPY/SPY.json`, `yahoo_chart_AAPL/AAPL.json` | full SPY history; AAPL from 2020 |
| `uss_snapshot_*/`, `uss_calibration/`, `uss_git_depth12/` | 3 full screener snapshots, 18 Nasdaq-only ones, a 12-commit clone |
| `qlib_us_zip_peek/` | `day.txt`, `all.txt`, `sp500.txt`, `nasdaq100.txt` pulled from the qlib zip by range |
| `hf_fnspid_zip_peek/`, `hf_metalwhale_zip_peek/`, `hf_stooq_mirror_sample/`, `rsr_google_finance_sample/`, `lean_spy_daily/`, `zipline_spy_benchmark/`, `datasets_finance_vix/`, `hf_kicel_peek/`, `hf_defeatbeta_prices_peek/` | small samples and symbol-count JSONs |

# Qullamaggie 三大形态的规则化回测

本目录是研究报告 `reports/Qullamaggie 策略评估与回测.md` 所用的全部回测代码与结果。
方法、结果与局限的完整说明见 `research_notes/Qullamaggie 策略评估与回测/own_backtest.md`。

## 目录

| 路径 | 内容 |
|---|---|
| `src/build_panel.py` | 由 Hugging Face `defeatbeta/yahoo-finance-data` 构建主面板（1999-12 至 2026-11，仅含至今仍上市的股票） |
| `src/build_dolt_panel.py` | 由 `siddharthmb/stocks-ohlcv` 构建含退市股票的面板（2011-01 至 2026-01，未复权价格自行做拆股校验与复权） |
| `src/qm/data.py` | 面板加载与指标计算（均线、ADR、动量排名等，全部只用当日及之前的数据） |
| `src/qm/setups.py` | 三种形态的信号：突破、Episodic Pivot、抛物线做空；市场环境过滤 |
| `src/qm/sim.py` | 逐笔交易模拟（止损、分批止盈、保本、均线跟踪、做空融券费）与组合模拟 |
| `src/qm/clean.py`、`earnings.py`、`bench.py`、`run.py` | 数据清洗、财报日标记、基准、汇总 |
| `src/run_universe.py` | “领涨股”池本身的后续收益 |
| `src/run_breakout.py`、`run_ep.py`、`run_parabolic.py` | 三种形态的基准版本与参数变体 |
| `src/run_portfolio.py` | 组合层面的资金曲线、基准对比、因子回归、容量 |
| `src/make_charts.py` | 生成报告中的三张图 |
| `src/test_sim.py` | 用手工构造的 K 线对模拟器做的单元测试 |
| `results/` | 各实验的日志（`*_log*.txt`）与逐笔交易、分年、变体汇总 CSV；`_dolt` 为含退市数据、`_hfwin` 为同一区间的仅幸存者数据 |
| `data_sources.md` | 可用免费数据源的清单与下载方式 |
| `AUDIT.md` | 独立代码审查的结论（如已生成） |
| `data/` | 下载的原始数据与构建好的面板（体积数 GB，未纳入版本管理） |

## 复现

```
cd backtest
python3 -I src/build_panel.py data/hf_defeatbeta data/panel_hf
python3 -I src/build_dolt_panel.py data/hf_dolt data/hf_defeatbeta data/panel_dolt
python3 -I src/test_sim.py
python3 -I src/run_universe.py data/panel_hf 2005-01-03
python3 -I src/run_breakout.py data/panel_hf results
python3 -I src/run_ep.py data/panel_hf results --sec data/ziplime/announcements.parquet \
        --ident data/ziplime/identifiers.parquet --current --nasdaq data/nasdaq_earnings
python3 -I src/run_parabolic.py data/panel_hf results
python3 -I src/run_portfolio.py data/panel_hf results hf 2005-01-03 - data/hf_defeatbeta data/french \
        --sec data/ziplime/announcements.parquet --ident data/ziplime/identifiers.parquet --current
python3 -I src/make_charts.py results ../reports/figures
```

依赖：Python 3.13、numpy、pandas、numba、duckdb、pyarrow、matplotlib。一次只跑一个脚本（单个进程峰值内存约 6–8 GB）。

## 需要知道的局限

- 只有日线：他真实使用的“开盘区间高点入场 + 当日最低价止损”无法还原，入场当日的盘中先后顺序只能用悲观 / 折中 / 乐观三种假设夹逼。
- 规则是机械执行的：不包含他的主观选股、题材判断、加仓和仓位集中。
- 做空的融券可得性与费率是假设值，不是实测值。
- 主面板只含幸存股票；2019-07 之后已用含退市数据交叉验证，结论一致。

# Qullamaggie 三大形态的规则化回测

本目录是研究报告 `reports/Qullamaggie 策略评估与回测.md` 所用的全部回测代码与结果。
方法、结果与局限的完整说明见 `research_notes/Qullamaggie 策略评估与回测/own_backtest.md`。

## 目录

| 路径 | 内容 |
|---|---|
| `src/build_panel.py` | 由 Hugging Face `defeatbeta/yahoo-finance-data` 构建主面板（1999-12 至 2026-11，仅含至今仍上市的股票） |
| `src/build_dolt_panel.py` | 由 `siddharthmb/stocks-ohlcv` 构建含退市股票的面板（2011-01 至 2026-01；未复权价格逐一校验拆股后复权，交易日历取自主面板，代码被复用的公司分段处理） |
| `src/qm/data.py` | 面板加载与指标计算（均线、ADR、动量排名等，全部只用当日及之前的数据） |
| `src/qm/setups.py` | 三种形态的信号：突破、Episodic Pivot、抛物线做空；市场环境过滤 |
| `src/qm/sim.py` | 逐笔交易模拟（止损、分批止盈、保本、均线跟踪、做空融券费）与组合模拟 |
| `src/qm/clean.py`、`earnings.py`、`bench.py`、`run.py` | 数据清洗、财报日标记、基准、汇总 |
| `src/run_universe.py` | “领涨股”池本身的后续收益 |
| `src/run_breakout.py`、`run_ep.py`、`run_parabolic.py` | 三种形态的基准版本与参数变体 |
| `src/run_portfolio.py` | 组合层面的资金曲线、基准对比、因子回归、容量 |
| `src/make_charts.py`、`make_tables.py`、`run_clustered_t.py` | 生成报告中的三张图、笔记中的结果表、按月聚类的显著性 |
| `run_all.sh` | 依次运行全部实验 |
| `src/test_sim.py` | 用手工构造的 K 线对模拟器做的单元测试 |
| `results/` | 各实验的日志（`*_log*.txt`）与逐笔交易、分年、变体汇总 CSV；`_dolt` 为含退市数据、`_hfwin` 为同一区间的仅幸存者数据 |
| `data_sources.md` | 可用免费数据源的清单与下载方式 |
| `AUDIT.md` | 独立代码审查的完整记录（针对第一版代码；修复情况见下文“独立代码审查”一节） |
| `data/` | 下载的原始数据与构建好的面板（体积数 GB，未纳入版本管理） |

## 复现

```
cd backtest
python3 -I src/build_panel.py data/hf_defeatbeta data/panel_hf
python3 -I src/build_dolt_panel.py data/hf_dolt data/hf_defeatbeta data/panel_hf/dates.npy \
        data/ziplime/announcements.parquet data/panel_dolt
bash run_all.sh                          # 单元测试 + 两个面板上的全部实验 + 图表（逐个运行，约 30 分钟）
python3 -I src/make_tables.py results    # 把结果文件转成笔记中的表格
```

依赖：Python 3.13、numpy、pandas、numba、duckdb、pyarrow、matplotlib。一次只跑一个脚本（单个进程峰值内存约 6–8 GB）。

## 独立代码审查

第一版代码与结果由一位独立审查者检查（记录见 `AUDIT.md`）：未发现前视偏差或记账错误，全部结果可逐位复现；
但指出 8 个会使具体数字产生偏差的问题（入场当日假设的适用范围、去重误删、均线遇缺失数据失效、含退市面板的日历与拆股处理等）。
这些问题已全部修正并整体重跑，`results/` 与报告中的数字均为修正后的版本；逐项说明见
`research_notes/Qullamaggie 策略评估与回测/own_backtest.md` 第 5 节。

## 需要知道的局限

- 只有日线：他真实使用的“开盘区间高点入场 + 当日最低价止损”无法还原。按开盘价或收盘价成交的交易在日线上是精确的；盘中成交的交易只能给出上下界（最坏情形 / 以收盘判定的乐观端）。
- 规则是机械执行的：不包含他的主观选股、题材判断、加仓和仓位集中。
- 做空的融券可得性与费率是假设值，不是实测值。
- 主面板只含幸存股票，且幸存程度随时间不均匀（2024 年之后退市的在、更早退市的不在），所以分年代的比较不可靠；2019-07 之后已用含退市数据交叉验证，结论一致。

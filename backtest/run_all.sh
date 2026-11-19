#!/bin/bash
# Re-run every experiment, one process at a time (each needs several GB of memory).
# Usage: bash run_all.sh   (from the backtest/ directory, after the two panels have been built)
set -u
B="$(cd "$(dirname "$0")" && pwd)"
R="$B/results"; SEC="$B/data/ziplime/announcements.parquet"; IDENT="$B/data/ziplime/identifiers.parquet"
S=2019-07-01; E=2026-01-28
run() { echo "== $1"; shift; "$@" 2>&1 | grep -v Warning; }
run "unit tests"        python3 -I "$B/src/test_sim.py" > "$R/test_log.txt"
# main panel, 2005-2026
run "universe hf"       python3 -I "$B/src/run_universe.py" "$B/data/panel_hf" 2005-01-03 > "$R/universe_log_hf.txt"
run "breakout hf"       python3 -I "$B/src/run_breakout.py" "$B/data/panel_hf" "$R" > "$R/breakout_log.txt"
run "ep hf"             python3 -I "$B/src/run_ep.py" "$B/data/panel_hf" "$R" --sec "$SEC" --ident "$IDENT" --current --nasdaq "$B/data/nasdaq_earnings" > "$R/ep_log.txt"
run "parabolic hf"      python3 -I "$B/src/run_parabolic.py" "$B/data/panel_hf" "$R" > "$R/parabolic_log.txt"
run "portfolio hf"      python3 -I "$B/src/run_portfolio.py" "$B/data/panel_hf" "$R" hf 2005-01-03 - "$B/data/hf_defeatbeta" "$B/data/french" --sec "$SEC" --ident "$IDENT" --current > "$R/portfolio_log_hf.txt"
run "clustered hf"      python3 -I "$B/src/run_clustered_t.py" "$B/data/panel_hf" 2005-01-03 - --sec "$SEC" --ident "$IDENT" --current > "$R/clustered_t_hf.txt"
# delisting-inclusive panel, 2019-07 .. 2026-01
run "universe dolt"     python3 -I "$B/src/run_universe.py" "$B/data/panel_dolt" $S $E > "$R/universe_log_dolt.txt"
run "breakout dolt"     python3 -I "$B/src/run_breakout.py" "$B/data/panel_dolt" "$R" dolt $S $E > "$R/breakout_log_dolt.txt"
run "ep dolt"           python3 -I "$B/src/run_ep.py" "$B/data/panel_dolt" "$R" --label dolt --start $S --end $E --sec "$SEC" > "$R/ep_log_dolt.txt"
run "parabolic dolt"    python3 -I "$B/src/run_parabolic.py" "$B/data/panel_dolt" "$R" dolt $S $E > "$R/parabolic_log_dolt.txt"
run "portfolio dolt"    python3 -I "$B/src/run_portfolio.py" "$B/data/panel_dolt" "$R" dolt $S $E "$B/data/hf_defeatbeta" "$B/data/french" --sec "$SEC" > "$R/portfolio_log_dolt.txt"
run "clustered dolt"    python3 -I "$B/src/run_clustered_t.py" "$B/data/panel_dolt" $S $E --sec "$SEC" > "$R/clustered_t_dolt.txt"
# main panel restricted to the same window (survivors only)
run "breakout hfwin"    python3 -I "$B/src/run_breakout.py" "$B/data/panel_hf" "$R" hfwin $S $E > "$R/breakout_log_hfwin.txt"
run "ep hfwin"          python3 -I "$B/src/run_ep.py" "$B/data/panel_hf" "$R" --label hfwin --start $S --end $E --sec "$SEC" --ident "$IDENT" --current > "$R/ep_log_hfwin.txt"
run "parabolic hfwin"   python3 -I "$B/src/run_parabolic.py" "$B/data/panel_hf" "$R" hfwin $S $E > "$R/parabolic_log_hfwin.txt"
run "charts"            python3 -I "$B/src/make_charts.py" "$R" "$B/../reports/figures" > "$R/charts_log.txt"
echo "ALL DONE"; grep -l -i "Traceback" "$R"/*.txt 2>/dev/null | sed 's/^/TRACEBACK in /'

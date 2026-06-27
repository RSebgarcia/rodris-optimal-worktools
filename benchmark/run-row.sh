#!/usr/bin/env bash
# ROW Stack benchmark — wrapper around ponytail's agentic runner.
#
# Runs 3 arms (baseline, ponytail, row-stack) across product-focused tasks.
# Prereqs:
#   - ponytail repo cloned at $PONYTAIL_DIR (default: ~/.claude/ponytail)
#   - Python 3.10+  (pip install anthropic)
#   - ANTHROPIC_API_KEY set
#
# Usage:
#   ./run-row.sh [--selftest] [--runs N] [--tasks csv-summary,surgical-fix,...]
#
# Cost estimate: ~$0.50 per mini run (1 task × 3 arms × 2 runs)
#                ~$5-10 per full run (4 tasks × 3 arms × 4 runs)

set -euo pipefail

PONYTAIL_DIR="${PONYTAIL_DIR:-$HOME/.claude/ponytail}"
RUNNER="$PONYTAIL_DIR/benchmarks/agentic/run.py"
TASKS_MODULE="$(dirname "$0")/tasks/product-tasks.py"
ARMS_DIR="$(dirname "$0")/arms"
RESULTS_DIR="$(dirname "$0")/results"
JUDGE="$(dirname "$0")/judge/row-judge.py"

RUNS=2
TASKS="csv-summary,surgical-fix,idea-to-proto,ambiguous-clarify"
SELFTEST=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --selftest) SELFTEST=true; shift ;;
        --runs) RUNS="$2"; shift 2 ;;
        --tasks) TASKS="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

if [ ! -f "$RUNNER" ]; then
    echo "ERROR: ponytail runner not found at $RUNNER"
    echo "Set PONYTAIL_DIR env var or clone ponytail to ~/.claude/ponytail"
    exit 1
fi

mkdir -p "$RESULTS_DIR"

if $SELFTEST; then
    echo "=== Self-test (no API spend) ==="
    python "$RUNNER" --selftest --task-module "$TASKS_MODULE"
    exit 0
fi

STAMP=$(date +%Y-%m-%d-%H%M)
RUN_DIR="$RESULTS_DIR/$STAMP"

echo "=== ROW Stack Benchmark — $STAMP ==="
echo "Tasks: $TASKS"
echo "Arms:  baseline, ponytail, row-stack"
echo "Runs:  $RUNS per arm per task"
echo ""

python "$RUNNER" \
    --task-module "$TASKS_MODULE" \
    --tasks "$TASKS" \
    --arms "baseline,$ARMS_DIR/row-stack.md" \
    --runs "$RUNS" \
    --workers 3 \
    --out "$RUN_DIR"

echo ""
echo "=== Scoring with ROW judge ==="
python "$JUDGE" --run "$RUN_DIR"

echo ""
echo "Results saved to: $RUN_DIR"

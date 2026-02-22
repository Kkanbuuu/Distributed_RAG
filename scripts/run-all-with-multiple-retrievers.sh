#!/bin/bash

# Run all services with one retriever per label (proj_spec, tech_concept, dev_log, ops_ts).
# Ports: retrievers 8002-8005, generator 8001, orchestrator 8000.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"
RETRIEVER_DIR="${SCRIPT_DIR}/retriever"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found. Run ./setup-venv.sh first"
    exit 1
fi

# Check if tmp directory exists
if [ ! -d "$SCRIPT_DIR/tmp" ]; then
    mkdir -p "$SCRIPT_DIR/tmp"
fi

# Retriever labels and ports (must match orchestrator/.env)
declare -a LABELS=(proj_spec tech_concept dev_log ops_ts)
declare -a PORTS=(8002 8003 8004 8005)
declare -a RETRIEVER_PIDS=()

# Ensure tmp log files exist for each retriever + generator + orchestrator
for label in "${LABELS[@]}"; do
    if [ ! -f "$SCRIPT_DIR/tmp/retriever-${label}.log" ]; then
        touch "$SCRIPT_DIR/tmp/retriever-${label}.log"
    fi
done
for f in retriever.log generator.log orchestrator.log; do
    if [ ! -f "$SCRIPT_DIR/tmp/$f" ]; then
        touch "$SCRIPT_DIR/tmp/$f"
    fi
done

# Activate venv
source "$VENV_DIR/bin/activate"

echo "=== Starting All Services (one retriever per label) ==="
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping all services..."
    for pid in "${RETRIEVER_PIDS[@]}" $GENERATOR_PID $ORCHESTRATOR_PID; do
        kill $pid 2>/dev/null || true
    done
    exit
}

trap cleanup SIGINT SIGTERM

# Start one retriever per label
for i in "${!LABELS[@]}"; do
    label="${LABELS[$i]}"
    port="${PORTS[$i]}"
    echo "Starting Retriever (DOMAIN=${label}) on port ${port}..."
    cd "$RETRIEVER_DIR"
    DOMAIN="$label" uvicorn main:app --host 0.0.0.0 --port "$port" --reload \
        > "$SCRIPT_DIR/tmp/retriever-${label}.log" 2>&1 &
    RETRIEVER_PIDS+=($!)
    echo "  PID: ${RETRIEVER_PIDS[$i]}"
done

# Wait for retrievers to be up
sleep 2

# Start generator
echo "Starting Generator on port 8001..."
cd "${SCRIPT_DIR}/generator"
uvicorn main:app --host 0.0.0.0 --port 8001 --reload > "$SCRIPT_DIR/tmp/generator.log" 2>&1 &
GENERATOR_PID=$!
echo "Generator PID: $GENERATOR_PID"

sleep 2

# Start orchestrator
echo "Starting Orchestrator on port 8000..."
cd "${SCRIPT_DIR}/orchestrator"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload > "$SCRIPT_DIR/tmp/orchestrator.log" 2>&1 &
ORCHESTRATOR_PID=$!
echo "Orchestrator PID: $ORCHESTRATOR_PID"

echo ""
echo "=== All Services Started ==="
echo ""
echo "Retrievers (one per label):"
echo "  - proj_spec:   port 8002  log: tmp/retriever-proj_spec.log"
echo "  - tech_concept: port 8003  log: tmp/retriever-tech_concept.log"
echo "  - dev_log:     port 8004  log: tmp/retriever-dev_log.log"
echo "  - ops_ts:      port 8005  log: tmp/retriever-ops_ts.log"
echo "  - Generator:   port 8001  log: tmp/generator.log"
echo "  - Orchestrator: port 8000  log: tmp/orchestrator.log"
echo ""
echo "To view logs:"
echo "  tail -f $SCRIPT_DIR/tmp/retriever-proj_spec.log"
echo "  tail -f $SCRIPT_DIR/tmp/generator.log"
echo "  tail -f $SCRIPT_DIR/tmp/orchestrator.log"
echo ""
echo "To stop all services, press Ctrl+C"
echo ""

wait

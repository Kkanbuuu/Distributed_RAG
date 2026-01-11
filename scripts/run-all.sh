#!/bin/bash

# Run all services concurrently in the background
# Useful for testing the full system locally

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found. Run ./setup-venv.sh first"
    exit 1
fi

# Check if tmp directory exists
if [ ! -d "$SCRIPT_DIR/tmp" ]; then
    mkdir -p "$SCRIPT_DIR/tmp"
fi

# Check if tmp files exist
if [ ! -f "$SCRIPT_DIR/tmp/retriever.log" ]; then
    touch "$SCRIPT_DIR/tmp/retriever.log"
fi
if [ ! -f "$SCRIPT_DIR/tmp/generator.log" ]; then
    touch "$SCRIPT_DIR/tmp/generator.log"
fi
if [ ! -f "$SCRIPT_DIR/tmp/orchestrator.log" ]; then
    touch "$SCRIPT_DIR/tmp/orchestrator.log"
fi 

# Activate venv
source "$VENV_DIR/bin/activate"

echo "=== Starting All Services ==="
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping all services..."
    kill $RETRIEVER_PID $GENERATOR_PID $ORCHESTRATOR_PID 2>/dev/null || true
    exit
}

trap cleanup SIGINT SIGTERM

# Start retriever
echo "Starting Retriever on port 8002..."
cd "${SCRIPT_DIR}/retriever"
uvicorn main:app --host 0.0.0.0 --port 8002 --reload > $SCRIPT_DIR/tmp/retriever.log 2>&1 &
RETRIEVER_PID=$!
echo "Retriever PID: $RETRIEVER_PID"

# Wait a bit for retriever to start
sleep 2

# Start generator
echo "Starting Generator on port 8001..."
cd "${SCRIPT_DIR}/generator"
uvicorn main:app --host 0.0.0.0 --port 8001 --reload > $SCRIPT_DIR/tmp/generator.log 2>&1 &
GENERATOR_PID=$!
echo "Generator PID: $GENERATOR_PID"

# Wait a bit for generator to start
sleep 2

# Start orchestrator
echo "Starting Orchestrator on port 8000..."
cd "${SCRIPT_DIR}/orchestrator"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload > $SCRIPT_DIR/tmp/orchestrator.log 2>&1 &
ORCHESTRATOR_PID=$!
echo "Orchestrator PID: $ORCHESTRATOR_PID"

echo ""
echo "=== All Services Started ==="
echo ""
echo "Services are running in the background. Logs are in:"
echo "  - Retriever: /tmp/retriever.log"
echo "  - Generator: /tmp/generator.log"
echo "  - Orchestrator: /tmp/orchestrator.log"
echo ""
echo "To view logs:"
echo "  tail -f /tmp/retriever.log"
echo "  tail -f /tmp/generator.log"
echo "  tail -f /tmp/orchestrator.log"
echo ""
echo "To stop all services, press Ctrl+C"
echo ""

wait
#!/bin/bash

set -Eeuo pipefail

REPO_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

failure_message() {
    echo "Tests failed."
}
trap failure_message ERR

if [[ -f ".venv/bin/activate" ]]; then
    # Linux and macOS virtual environments.
    source ".venv/bin/activate"
    PYTHON_BIN="python"
elif [[ -f ".venv/Scripts/activate" ]]; then
    # Windows virtual environments used from Bash or WSL.
    source <(sed 's/\r$//' ".venv/Scripts/activate")
    PYTHON_BIN="$REPO_DIR/.venv/Scripts/python.exe"
elif [[ -f "venv/bin/activate" ]]; then
    source "venv/bin/activate"
    PYTHON_BIN="python"
elif [[ -f "venv/Scripts/activate" ]]; then
    source <(sed 's/\r$//' "venv/Scripts/activate")
    PYTHON_BIN="$REPO_DIR/venv/Scripts/python.exe"
else
    echo "Tests failed: no project virtual environment was found."
    exit 1
fi

echo "Running test suite..."

if "$PYTHON_BIN" -m pytest; then
    trap - ERR
    echo "All tests passed."
    exit 0
else
    trap - ERR
    echo "Tests failed."
    exit 1
fi

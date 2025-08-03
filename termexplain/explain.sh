#!/bin/bash
# termExplain Shell Wrapper
# This script runs the Homebrew-installed version of termExplain from its virtualenv

# Get the path of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to Homebrew-installed termExplain's Python binary
VENV_PY="$SCRIPT_DIR/../libexec/bin/python"

# Check if Python binary exists
if [ ! -x "$VENV_PY" ]; then
    echo "❌ Error: Python executable not found at $VENV_PY"
    exit 1
fi

# Run the CLI using the installed package entry point
exec "$VENV_PY" -m termexplain "$@"

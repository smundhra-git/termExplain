#!/bin/bash
# termExplain Shell Alias Script
# 
# This script provides a convenient way to run termExplain from anywhere.
# Add this to your shell profile (.bashrc, .zshrc, etc.) or run it directly.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to run termExplain
explain() {
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python 3 is not installed or not in PATH"
        return 1
    fi
    
    # Check if the main.py file exists
    if [ ! -f "$SCRIPT_DIR/main.py" ]; then
        echo "❌ Error: termExplain not found at $SCRIPT_DIR/main.py"
        return 1
    fi
    
    # Run termExplain with all arguments
    python3 "$SCRIPT_DIR/main.py" "$@"
}

# If this script is sourced, export the function
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    export -f explain
    echo "✅ termExplain function exported. Use 'explain <error>' to explain errors."
else
    # If run directly, execute the function with arguments
    explain "$@"
fi 
#!/bin/bash
# Activate the virtual environment for legal document processing

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
echo "Virtual environment activated. Python: $(which python3)"

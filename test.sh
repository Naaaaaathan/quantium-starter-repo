#!/bin/bash
set -e
trap 'printf 1; exit 1' ERR
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/project/Scripts/python.exe"
"$VENV_PYTHON" -m pip install pytest dash pandas >/dev/null 2>&1
"$VENV_PYTHON" -m pytest >/dev/null 2>&1
printf 0
exit 0
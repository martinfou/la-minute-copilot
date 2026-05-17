#!/bin/bash
# Générer la présentation à partir du JSON
cd "$(dirname "$0")/.."
source .venv/bin/activate
python3 scripts/parse.py "$@"

#!/bin/bash
# Générateur PowerPoint — lit un JSON, produit un .pptx
# Usage: ./generate.sh presentations/outlook.json
#        ./generate.sh presentations/outlook.json -o mon_fichier.pptx

set -e
cd "$(dirname "$0")"

# Installation moderne via pyproject.toml
if command -v uv &>/dev/null; then
    # uv est le gestionnaire python le plus rapide (Rust)
    [ ! -d .venv ] && uv venv --python 3.11
    uv sync
    source .venv/bin/activate
else
    # Fallback pip compatible
    [ ! -d .venv ] && python3 -m venv .venv
    source .venv/bin/activate
    pip install -e . -q
fi

python3 scripts/generate_pptx.py "$@"

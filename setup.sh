#!/usr/bin/env bash
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

echo ">>> Creating virtual environment (.venv)…"
python3 -m venv .venv

echo ">>> Activating virtual environment…"
# shellcheck disable=SC1091
source .venv/bin/activate

echo ">>> Upgrading pip…"
pip install --upgrade pip

echo ">>> Installing requirements…"
pip install -r requirements.txt

echo ">>> Done. Launching Streamlit app…"
streamlit run app.py

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

echo ">>> Checking for model weights..."
MODEL_DIR="Depth_Anything_V2/checkpoints"
MODEL_FILE="$MODEL_DIR/depth_anything_v2_vits.pth"
mkdir -p "$MODEL_DIR"

if [ ! -f "$MODEL_FILE" ]; then
    echo ">>> Downloading Depth-Anything-V2-Small model..."
    curl -L -o "$MODEL_FILE" "https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth?download=true"
fi

echo ">>> Done. Launching Streamlit app…"
streamlit run app.py

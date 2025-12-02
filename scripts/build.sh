#!/usr/bin/env bash
set -euo pipefail

# Build script: creates a runnable zipapp in ./dist
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"

mkdir -p "$DIST_DIR"

echo "Building zipapp..."

# Create a zipapp using top-level `app` module as entry point (app:main)
python3 -m zipapp "$ROOT_DIR" -m "app:main" -o "$DIST_DIR/flux_depth_generator.pyz"

echo "Built: $DIST_DIR/flux_depth_generator.pyz"

echo "To run: python3 $DIST_DIR/flux_depth_generator.pyz"

#!/bin/bash
# Build HTML from data/ into docs/.
# docs/ is the directory served by GitHub Pages.

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

TEMPLATES_DIR="$(cd "$(dirname "$0")" && pwd)/templates"
if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "Error: templates/ directory not found in build_html/!"
    exit 1
fi

if [ ! -d "data" ]; then
    echo "Error: data/ directory not found!"
    exit 1
fi

echo "0. Copying static files from templates/ to docs/..."
mkdir -p docs/css docs/js docs/grammar docs/data
cp -f  "$TEMPLATES_DIR/index.html"         docs/         2>/dev/null || true
cp -f  "$TEMPLATES_DIR/about.html"         docs/         2>/dev/null || true
cp -f  "$TEMPLATES_DIR/alphabet.html"      docs/         2>/dev/null || true
cp -f  "$TEMPLATES_DIR/favicon.png"        docs/         2>/dev/null || true
cp -rf "$TEMPLATES_DIR/css/"*              docs/css/     2>/dev/null || true
cp -rf "$TEMPLATES_DIR/js/"*               docs/js/      2>/dev/null || true
cp -f  "$TEMPLATES_DIR/grammar/index.html" docs/grammar/ 2>/dev/null || true

echo "1. Building vocabulary JSON from data/vocabulary/..."
python3 build_html/build_vocabulary.py

echo "2. Building grammar pages from data/grammar/..."
python3 build_html/build_grammar.py

echo "3. Building HTML pages from data/ directory..."
python3 build_html/build_from_data.py

echo "4. Building standalone version..."
python3 build_html/embed_vocabulary.py

echo "Build complete! Site is in docs/"

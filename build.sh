#!/bin/bash
# Build the Cyril Graham site into docs/.
# Source data lives in data/. docs/ is served by GitHub Pages.

set -e
cd "$(dirname "$0")"

build_html/build_html.sh

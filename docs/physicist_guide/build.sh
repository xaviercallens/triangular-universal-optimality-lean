#!/usr/bin/env bash
# Rebuild the physicist guide: figures and numbers from physics/results/, then the PDF.
# Needs python3 with numpy/scipy/mpmath/matplotlib and pdflatex. Run from anywhere.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$ROOT"
python3 docs/physicist_guide/make_figures.py > /dev/null
cd "$HERE"
pdflatex -interaction=nonstopmode -halt-on-error guide.tex > /dev/null
pdflatex -interaction=nonstopmode -halt-on-error guide.tex > build.log
if grep -E "^!|undefined|Overfull" build.log; then echo "LaTeX warnings above"; exit 1; fi
echo "built $HERE/guide.pdf ($(pdfinfo guide.pdf | awk '/Pages/{print $2}') pages)"

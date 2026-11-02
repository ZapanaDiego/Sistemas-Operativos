#!/usr/bin/env bash
set -e

echo "==> [1/4] Compilando primera pasada con pdflatex..."
pdflatex -interaction=nonstopmode main.tex > /dev/null

if grep -q '\\citation' main.aux 2>/dev/null; then
  echo "==> [2/4] Generando bibliografía con bibtex..."
  bibtex main > /dev/null
else
  echo "==> [2/4] Sin citas aún: se omite bibtex."
fi

echo "==> [3/4] Segunda pasada de pdflatex para resolver referencias cruzadas..."
pdflatex -interaction=nonstopmode main.tex > /dev/null

echo "==> [4/4] Pasada final de pdflatex..."
pdflatex -interaction=nonstopmode main.tex > /dev/null

echo "=========================================================="
echo " PDF generado exitosamente en: main.pdf"
echo "=========================================================="
texcount -inc -sub=none -total main.tex 2>/dev/null | grep -E "Words in text|Total"

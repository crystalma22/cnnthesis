#!/bin/bash
# Build script for LaTeX thesis
# Run from thesis_latex/ directory

echo "Building LaTeX thesis..."

# First pass
echo "Running pdflatex (pass 1)..."
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1

# Bibliography (if .bib file exists and has entries)
if [ -f references.bib ] && [ -s references.bib ]; then
    echo "Running bibtex..."
    bibtex thesis > /dev/null 2>&1
fi

# Second pass
echo "Running pdflatex (pass 2)..."
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1

# Third pass (resolve all references)
echo "Running pdflatex (pass 3)..."
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1

# Clean up auxiliary files (optional)
# Uncomment if you want to clean up:
# rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg

echo "Done! Check thesis.pdf"


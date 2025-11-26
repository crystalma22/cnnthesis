#!/bin/bash
# Script to convert Word document to LaTeX using Pandoc

if [ $# -eq 0 ]; then
    echo "Usage: ./convert_word_doc.sh <your_thesis.docx>"
    echo ""
    echo "This script converts a Word document to LaTeX format."
    echo "You'll need to install Pandoc first: brew install pandoc"
    exit 1
fi

WORD_FILE="$1"
OUTPUT_FILE="thesis_from_word.tex"

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "Error: Pandoc is not installed."
    echo "Install it with: brew install pandoc"
    exit 1
fi

# Check if Word file exists
if [ ! -f "$WORD_FILE" ]; then
    echo "Error: File '$WORD_FILE' not found"
    exit 1
fi

echo "Converting $WORD_FILE to LaTeX..."
echo ""

# Convert using pandoc
pandoc "$WORD_FILE" -o "$OUTPUT_FILE" \
    --wrap=none \
    --standalone \
    --toc \
    --number-sections

if [ $? -eq 0 ]; then
    echo "✅ Conversion complete!"
    echo ""
    echo "Output saved to: $OUTPUT_FILE"
    echo ""
    echo "NEXT STEPS:"
    echo "1. Open $OUTPUT_FILE and review the content"
    echo "2. Copy sections into the appropriate files in sections/"
    echo "3. Clean up formatting and citations"
    echo "4. Run ./build.sh to compile"
else
    echo "❌ Conversion failed. Check the error messages above."
    exit 1
fi


#!/usr/bin/env python3
"""
Helper script to convert Word document sections to LaTeX.
This script helps extract and convert content from Word to LaTeX format.
"""

import sys
import re
from pathlib import Path

def escape_latex(text):
    """Escape special LaTeX characters."""
    # Characters that need escaping in LaTeX
    replacements = {
        '\\': '\\textbackslash{}',
        '{': '\\{',
        '}': '\\}',
        '$': '\\$',
        '&': '\\&',
        '%': '\\%',
        '#': '\\#',
        '^': '\\textasciicircum{}',
        '_': '\\_',
        '~': '\\textasciitilde{}',
    }
    
    # But don't escape if already escaped
    for char, replacement in replacements.items():
        # Only replace if not already escaped
        text = text.replace(char, replacement)
    
    # Fix double escaping
    text = text.replace('\\\\textbackslash{}', '\\textbackslash{}')
    text = text.replace('\\\\%', '\\%')
    text = text.replace('\\\\&', '\\&')
    text = text.replace('\\\\$', '\\$')
    text = text.replace('\\\\#', '\\#')
    text = text.replace('\\\\_', '\\_')
    text = text.replace('\\\\{', '\\{')
    text = text.replace('\\\\}', '\\}')
    
    return text

def convert_word_formatting(text):
    """Convert common Word formatting patterns to LaTeX."""
    # Bold: **text** or Word's bold markers
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    
    # Italic: *text* or _text_
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\textit{\1}', text)
    text = re.sub(r'_(.+?)_', r'\\textit{\1}', text)
    
    # Remove extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def clean_latex(text):
    """Clean up common LaTeX issues."""
    # Remove Word-specific characters
    text = text.replace('\u2019', "'")  # Right single quotation mark
    text = text.replace('\u2018', "'")  # Left single quotation mark
    text = text.replace('\u201c', '"')  # Left double quotation mark
    text = text.replace('\u201d', '"')  # Right double quotation mark
    text = text.replace('\u2013', '--')  # En dash
    text = text.replace('\u2014', '---')  # Em dash
    
    # Remove extra blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def process_text(text):
    """Process text through all conversion steps."""
    text = convert_word_formatting(text)
    text = clean_latex(text)
    # Note: We don't escape here because user should review first
    # text = escape_latex(text)
    return text

def main():
    """Main function."""
    print("=" * 80)
    print("Word to LaTeX Conversion Helper")
    print("=" * 80)
    print()
    print("This script helps convert Word document content to LaTeX.")
    print()
    print("OPTIONS:")
    print("1. Use Pandoc (recommended):")
    print("   pandoc your_thesis.docx -o converted.tex --wrap=none")
    print()
    print("2. Manual copy-paste:")
    print("   - Copy text from Word")
    print("   - Paste into section .tex files")
    print("   - Run this script to clean formatting:")
    print("     python word_to_latex.py <input.txt> <output.tex>")
    print()
    print("3. Process existing LaTeX file:")
    print("   python word_to_latex.py --clean <file.tex>")
    print()
    
    if len(sys.argv) < 2:
        return
    
    if sys.argv[1] == '--clean' and len(sys.argv) >= 3:
        # Clean an existing LaTeX file
        input_file = Path(sys.argv[2])
        if not input_file.exists():
            print(f"Error: {input_file} not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned = process_text(content)
        
        output_file = input_file.with_suffix('.cleaned.tex')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"Cleaned file saved to: {output_file}")
        print("Review and manually edit before using in your thesis.")
    
    elif len(sys.argv) >= 3:
        # Convert text file to LaTeX
        input_file = Path(sys.argv[1])
        output_file = Path(sys.argv[2])
        
        if not input_file.exists():
            print(f"Error: {input_file} not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        converted = process_text(content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted)
        
        print(f"Converted file saved to: {output_file}")
        print("Review and manually edit before using in your thesis.")
        print()
        print("IMPORTANT: Check for:")
        print("  - Special characters that need escaping")
        print("  - Citations that need BibTeX format")
        print("  - Equations that need LaTeX math mode")
        print("  - Tables/figures (already included in thesis structure)")

if __name__ == '__main__':
    main()


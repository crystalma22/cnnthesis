#!/usr/bin/env python3
"""
Helper script to convert markdown content to LaTeX format.
This script helps convert your markdown documentation into LaTeX sections.
"""

import re
import sys
from pathlib import Path

def markdown_to_latex(markdown_text):
    """
    Convert markdown text to LaTeX format.
    Handles headers, bold, italic, lists, tables, and code blocks.
    """
    latex = markdown_text
    
    # Headers
    latex = re.sub(r'^# (.+)$', r'\\section{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^## (.+)$', r'\\subsection{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', latex, flags=re.MULTILINE)
    
    # Bold
    latex = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', latex)
    latex = re.sub(r'__(.+?)__', r'\\textbf{\1}', latex)
    
    # Italic
    latex = re.sub(r'\*(.+?)\*', r'\\textit{\1}', latex)
    latex = re.sub(r'_(.+?)_', r'\\textit{\1}', latex)
    
    # Code blocks (inline)
    latex = re.sub(r'`(.+?)`', r'\\texttt{\1}', latex)
    
    # Blockquotes
    latex = re.sub(r'^> (.+)$', r'\\begin{quote}\n\\1\n\\end{quote}', latex, flags=re.MULTILINE)
    
    # Lists (simple bullet points)
    lines = latex.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if re.match(r'^[-*+]\s+(.+)$', line):
            if not in_list:
                result_lines.append('\\begin{itemize}')
                in_list = True
            content = re.match(r'^[-*+]\s+(.+)$', line).group(1)
            result_lines.append(f'\\item {content}')
        elif re.match(r'^\d+\.\s+(.+)$', line):
            if not in_list:
                result_lines.append('\\begin{enumerate}')
                in_list = True
            content = re.match(r'^\d+\.\s+(.+)$', line).group(1)
            result_lines.append(f'\\item {content}')
        else:
            if in_list:
                result_lines.append('\\end{itemize}')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('\\end{itemize}')
    
    latex = '\n'.join(result_lines)
    
    # Escape special LaTeX characters
    latex = latex.replace('%', '\\%')
    latex = latex.replace('&', '\\&')
    latex = latex.replace('$', '\\$')
    latex = latex.replace('#', '\\#')
    latex = latex.replace('^', '\\textasciicircum{}')
    latex = latex.replace('_', '\\_')
    latex = latex.replace('{', '\\{')
    latex = latex.replace('}', '\\}')
    
    # Fix double escaping
    latex = latex.replace('\\\\%', '\\%')
    latex = latex.replace('\\\\&', '\\&')
    latex = latex.replace('\\\\$', '\\$')
    latex = latex.replace('\\\\#', '\\#')
    latex = latex.replace('\\\\_', '\\_')
    latex = latex.replace('\\\\{', '\\{')
    latex = latex.replace('\\\\}', '\\}')
    
    return latex

def convert_file(input_path, output_path):
    """Convert a markdown file to LaTeX."""
    with open(input_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    latex_content = markdown_to_latex(markdown_content)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"Converted: {input_path} -> {output_path}")

def main():
    """Main function to convert markdown files."""
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_latex.py <input.md> [output.tex]")
        print("\nOr convert multiple files:")
        print("  python markdown_to_latex.py --all")
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        # Convert all relevant markdown files
        base_dir = Path(__file__).parent.parent
        sections_dir = Path(__file__).parent / 'sections'
        sections_dir.mkdir(exist_ok=True)
        
        # Map markdown files to LaTeX sections
        conversions = {
            'docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md': 'sections/methodology_draft.tex',
            'docs/THESIS_RESULTS_SUMMARY.md': 'sections/results_draft.tex',
            'EW_VS_VW_EXPLAINED.md': 'sections/discussion_draft.tex',
        }
        
        for md_file, tex_file in conversions.items():
            input_path = base_dir / md_file
            output_path = Path(__file__).parent / tex_file
            if input_path.exists():
                convert_file(input_path, output_path)
            else:
                print(f"Warning: {input_path} not found")
    else:
        input_path = Path(sys.argv[1])
        if len(sys.argv) > 2:
            output_path = Path(sys.argv[2])
        else:
            output_path = input_path.with_suffix('.tex')
        
        if not input_path.exists():
            print(f"Error: {input_path} not found")
            sys.exit(1)
        
        convert_file(input_path, output_path)

if __name__ == '__main__':
    main()


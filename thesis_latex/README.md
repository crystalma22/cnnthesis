# LaTeX Thesis Conversion Guide

This directory contains the LaTeX structure for your thesis. Follow these steps to complete the conversion.

## Directory Structure

```
thesis_latex/
├── thesis.tex              # Main LaTeX document
├── sections/               # Individual section files
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── literature_review.tex
│   ├── methodology.tex
│   ├── data.tex
│   ├── results.tex
│   ├── discussion.tex
│   └── conclusion.tex
├── appendices/             # Appendices
│   ├── additional_tables.tex
│   ├── additional_figures.tex
│   └── robustness.tex
├── references.bib          # Bibliography file
├── markdown_to_latex.py    # Helper script for conversion
└── README.md               # This file
```

## Step-by-Step Conversion Process

### Step 1: Install LaTeX

**macOS:**
```bash
brew install --cask mactex
# Or use MacTeX distribution: https://www.tug.org/mactex/
```

**Linux:**
```bash
sudo apt-get install texlive-full
```

**Windows:**
Download and install MiKTeX or TeX Live.

### Step 2: Compile the Thesis

From the `thesis_latex/` directory:

```bash
# First compilation (generates .aux files)
pdflatex thesis.tex

# Generate bibliography (if you have references.bib entries)
bibtex thesis

# Second compilation (includes references)
pdflatex thesis.tex

# Third compilation (resolves all cross-references)
pdflatex thesis.tex
```

Or use a build script:
```bash
./build.sh
```

### Step 3: Fill in Content

#### 3.1 Abstract
Edit `sections/abstract.tex` - I've included a draft based on your master guide.

#### 3.2 Introduction
Edit `sections/introduction.tex`. Use content from:
- `⭐_THESIS_MASTER_GUIDE.md` (Research Question, Contributions)
- Your existing introduction drafts

#### 3.3 Literature Review
Edit `sections/literature_review.tex`. Use:
- `chatgpt_prompts/CHATGPT_PROMPT_FOR_INTRO_LIT_REWRITE.md`
- Your literature review notes

#### 3.4 Methodology
Edit `sections/methodology.tex`. Use:
- `chatgpt_prompts/CHATGPT_PROMPT_FOR_METHODOLOGY_FINAL.md`
- `METHODOLOGY_EXPLAINED_STEP_BY_STEP.md`
- `docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md`

#### 3.5 Data
Edit `sections/data.tex`. Table 1 is already included.

#### 3.6 Results
Edit `sections/results.tex`. All tables and figures are already included with proper references. Use:
- `chatgpt_prompts/CHATGPT_PROMPT_FOR_RESULTS_FINAL.md`
- `docs/THESIS_RESULTS_SUMMARY.md`
- `⭐_THESIS_MASTER_GUIDE.md` (Validated Results section)

#### 3.7 Discussion
Edit `sections/discussion.tex`. Use:
- `chatgpt_prompts/CHATGPT_PROMPT_FOR_DISCUSSION_FINAL.md`
- `EW_VS_VW_EXPLAINED.md`

#### 3.8 Conclusion
Edit `sections/conclusion.tex`. Use:
- `chatgpt_prompts/CHATGPT_PROMPT_FOR_CONCLUSION_FINAL.md`

### Step 4: Convert Markdown to LaTeX (Optional Helper)

The `markdown_to_latex.py` script can help convert your markdown files:

```bash
# Convert a single file
python markdown_to_latex.py ../docs/THESIS_RESULTS_SUMMARY.md sections/results_draft.tex

# Convert multiple files
python markdown_to_latex.py --all
```

**Note:** The conversion is not perfect. You'll need to:
1. Review and edit the converted LaTeX
2. Fix formatting issues
3. Add proper LaTeX commands for tables/figures
4. Ensure proper citation formatting

### Step 5: Add References

Edit `references.bib` and add all your citations in BibTeX format. Example:

```bibtex
@article{jiang2023,
  title={Deep Learning for Stock Return Prediction},
  author={Jiang, Hao and Kelly, Bryan and Xiu, Dacheng},
  journal={Journal of Finance},
  year={2023},
  volume={78},
  pages={1--50}
}
```

Then cite in your text:
```latex
As shown by \citet{jiang2023}, CNNs can predict stock returns.
```

### Step 6: Customize Formatting

#### Change Bibliography Style
Edit `thesis.tex` line with `\bibliographystyle{}`:
- `aer` - American Economic Review style
- `apalike` - APA-like style
- `plain` - Plain style
- Check your university requirements

#### Adjust Line Spacing
In `thesis.tex`, change:
- `\onehalfspacing` - 1.5 line spacing
- `\doublespacing` - 2.0 line spacing
- `\singlespacing` - 1.0 line spacing

#### Change Font
Add to preamble:
```latex
\usepackage{times}  % Times New Roman
% or
\usepackage{mathptmx}  % Times with math support
```

## Tables and Figures

### Tables
All tables are already included in the appropriate sections. They're loaded from:
```
../thesis_output/tables/table*.tex
```

### Figures
All figures are already included. They're loaded from:
```
../thesis_output/figures/figure*.pdf
```

**Note:** Make sure the paths are correct. The current setup assumes:
- LaTeX files are in `thesis_latex/`
- Output files are in `thesis_output/` (one level up)

If your structure is different, update the paths in the section files.

## Common LaTeX Commands

### Citations
```latex
\citet{jiang2023}        % Author (year)
\citep{jiang2023}        % (Author, year)
\cite{jiang2023}         % (year) or (Author, year) depending on style
```

### Cross-References
```latex
\ref{tab:sample_stats}   % Reference to table
\ref{fig:decile_performance}  % Reference to figure
\ref{sec:results}        % Reference to section
```

### Math
```latex
$R_{i,t}$                % Inline math
\[ R_{i,t} = \alpha + \beta X_{i,t} + \epsilon_{i,t} \]  % Display math
```

### Emphasis
```latex
\textbf{bold text}
\textit{italic text}
\emph{emphasized text}
```

## Troubleshooting

### "File not found" errors
- Check that paths to tables/figures are correct
- Use absolute paths if relative paths don't work
- Make sure `thesis_output/` exists

### Bibliography not showing
1. Run `bibtex thesis` after first `pdflatex`
2. Run `pdflatex` twice more
3. Check that `.bib` file has correct entries

### Tables/Figures not appearing
- Check that PDF files exist for figures
- Verify table `.tex` files are valid LaTeX
- Try using `[H]` placement (requires `float` package, already included)

### Compilation errors
- Check for unmatched braces `{}`
- Verify all packages are installed
- Look for special characters that need escaping

## Next Steps

1. ✅ Structure is set up
2. ✅ Tables and figures are included
3. ⏳ Fill in content for each section
4. ⏳ Add all references to `.bib` file
5. ⏳ Review and proofread
6. ⏳ Adjust formatting to match university requirements
7. ⏳ Final compilation and PDF generation

## Tips

- **Version Control:** Use git to track changes
- **Backup:** Keep copies of your markdown files
- **Incremental:** Write one section at a time, compile frequently
- **Spell Check:** Use LaTeX-aware spell checkers
- **Collaboration:** Share PDFs, not `.tex` files (unless collaborating on LaTeX)

## Resources

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
- [Overleaf Documentation](https://www.overleaf.com/learn)
- [BibTeX Guide](http://www.bibtex.org/Using/)

Good luck with your thesis!


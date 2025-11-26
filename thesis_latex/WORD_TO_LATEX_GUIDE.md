# Converting Word Document to LaTeX

Since you already have your thesis written in Word, here are the best ways to convert it to LaTeX.

## Option 1: Using Pandoc (Recommended - Automated)

Pandoc is the best tool for converting Word to LaTeX while preserving formatting.

### Step 1: Install Pandoc

**macOS:**
```bash
brew install pandoc
```

**Or download:** https://pandoc.org/installing.html

### Step 2: Convert Word to LaTeX

```bash
# Convert entire document
pandoc your_thesis.docx -o thesis_from_word.tex --wrap=none

# Or convert with better formatting
pandoc your_thesis.docx -o thesis_from_word.tex --wrap=none --standalone
```

### Step 3: Extract Sections

After conversion, you'll need to:
1. Copy content from `thesis_from_word.tex` 
2. Paste into the appropriate section files in `sections/`
3. Clean up formatting (pandoc sometimes adds extra commands)

## Option 2: Manual Copy-Paste (Most Reliable)

This gives you the most control and ensures proper formatting.

### Step-by-Step:

1. **Open your Word document**

2. **For each section, copy the text and paste into the corresponding `.tex` file:**
   - Abstract → `sections/abstract.tex`
   - Introduction → `sections/introduction.tex`
   - Literature Review → `sections/literature_review.tex`
   - Methodology → `sections/methodology.tex`
   - Data → `sections/data.tex`
   - Results → `sections/results.tex` (tables/figures already included!)
   - Discussion → `sections/discussion.tex`
   - Conclusion → `sections/conclusion.tex`

3. **Convert formatting as you paste:**
   - **Bold text** → `\textbf{bold text}`
   - *Italic text* → `\textit{italic text}`
   - Headers → Already handled by section structure
   - Citations → Convert to `\citet{author2023}` or `\citep{author2023}`
   - Math equations → Keep as-is or convert to LaTeX math mode

4. **Special characters to escape:**
   - `%` → `\%`
   - `&` → `\&`
   - `$` → `\$`
   - `#` → `\#`
   - `_` → `\_`
   - `{` → `\{`
   - `}` → `\}`

## Option 3: Hybrid Approach (Recommended)

1. Use Pandoc to get a rough conversion
2. Manually clean up and integrate into the section files
3. This saves time while ensuring quality

## Quick Reference: LaTeX Equivalents

| Word Formatting | LaTeX Command |
|----------------|---------------|
| **Bold** | `\textbf{text}` |
| *Italic* | `\textit{text}` |
| Heading 1 | `\section{Title}` |
| Heading 2 | `\subsection{Title}` |
| Heading 3 | `\subsubsection{Title}` |
| Bullet List | `\begin{itemize} \item ... \end{itemize}` |
| Numbered List | `\begin{enumerate} \item ... \end{enumerate}` |
| Citation | `\citet{key}` or `\citep{key}` |
| Math | `$equation$` or `\[equation\]` |

## Important Notes

### Tables and Figures
- **Don't copy tables/figures from Word!** 
- They're already included in `sections/results.tex` from your `thesis_output/` directory
- Just add the text around them

### Citations
- Convert Word citations to BibTeX format in `references.bib`
- Then cite using `\citet{key}` or `\citep{key}`

### Equations
- If you have equations in Word, convert them to LaTeX math notation
- Inline: `$E[R_{i,t}] = \alpha + \beta X_{i,t}$`
- Display: `\[ E[R_{i,t}] = \alpha + \beta X_{i,t} \]`

## Workflow Recommendation

1. **Start with Results section** - It already has all tables/figures, just add your text
2. **Then Methodology** - Usually straightforward to convert
3. **Then Introduction/Literature Review** - May need more formatting cleanup
4. **Finally Abstract/Conclusion** - Shortest sections

## Testing

After pasting each section:
```bash
cd thesis_latex
./build.sh
```

Check `thesis.pdf` to see how it looks. Fix any formatting issues as you go.

## Common Issues and Fixes

### Issue: Text appears as code
- **Fix:** Remove backticks or convert to `\texttt{}`

### Issue: Special characters break compilation
- **Fix:** Escape them (see table above)

### Issue: Citations not showing
- **Fix:** Make sure entries are in `references.bib` and run `bibtex thesis`

### Issue: Tables/figures missing
- **Fix:** Check file paths in section files match your directory structure

## Need Help?

If you get stuck:
1. Check the `.log` file after compilation for error messages
2. Comment out problematic sections temporarily to isolate issues
3. Test one section at a time

Good luck! 🎓


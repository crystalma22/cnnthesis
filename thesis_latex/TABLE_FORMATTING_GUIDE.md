# Table Formatting Guide - Finance/Economics Journal Style

This guide explains how to format tables in your thesis to match the standard used by top finance and economics journals.

## ✅ What's Already Updated

1. **Packages added to `thesis.tex`:**
   - `booktabs` - Professional horizontal rules
   - `siunitx` - Aligned numeric columns
   - `threeparttable` - Clean table notes

2. **Configuration:**
   - `siunitx` configured for proper numeric alignment
   - Significance star commands updated

## 📋 Table Formatting Rules

### 1. Visual Style

✅ **DO:**
- Use only three horizontal lines: `\toprule`, `\midrule`, `\bottomrule`
- Use `\cmidrule(lr){X-Y}` for partial lines under column headers
- Put caption **above** the table
- Put notes **below** the table in `\footnotesize`
- Use `S` columns from `siunitx` for numeric data

❌ **DON'T:**
- Use vertical lines (`|`)
- Use `\hline` (use `booktabs` commands instead)
- Put caption below table
- Use regular `c`, `l`, `r` columns for numbers (use `S`)

### 2. Column Formatting with siunitx

Use `S` columns for numeric data. Format: `S[table-format=X.Y]`

**Examples:**
```latex
S[table-format=1.2]    % 1 digit before, 2 after: 0.21, 1.37
S[table-format=-2.2]    % Negative numbers: -28.08, -1.55
S[table-format=3.0]     % Integers: 217, 125000
S[table-format=1.3]     % 1 before, 3 after: 0.045, 1.256
```

**For text columns, use regular `l`, `c`, `r`:**
```latex
\begin{tabular}{l S[table-format=1.2] S[table-format=1.2]}
%     ^text  ^number      ^number
```

### 3. Significance Stars

Always use math mode for significance stars:
```latex
0.21$^{***}$    % Correct
0.21***         % Wrong (won't format properly)
```

Or use the `\tnote{}` command with `threeparttable`:
```latex
0.21\tnote{***}
```

Then define in `\begin{tablenotes}`:
```latex
\item $^{*}$, $^{**}$, and $^{***}$ indicate significance at the 10\%, 5\%, and 1\% levels.
```

### 4. Table Notes

**Option 1: Simple (for short notes)**
```latex
\vspace{0.5em}
{\footnotesize
This table reports summary statistics...
}
```

**Option 2: threeparttable (for longer notes, recommended)**
```latex
\begin{threeparttable}
\begin{tabular}{...}
    % table content
\end{tabular}
\begin{tablenotes}
    \footnotesize
    \item Notes: Main description here.
    \item $^{*}$, $^{**}$, and $^{***}$ indicate significance...
\end{tablenotes}
\end{threeparttable}
```

## 🔧 How to Update Your Existing Tables

### Step 1: Identify the Table Type

- **Summary Statistics** → Use Template 1
- **Portfolio Performance** → Use Template 3
- **FOMC Event Study** → Use Template 4
- **Regression Results** → Use Template 2

### Step 2: Update Column Format

**Before (old format):**
```latex
\begin{tabular}{lccc}
    Decile & Annual Return (%) & Volatility (%) & Sharpe Ratio \\
    Low (1) & -28.08 & 18.07 & -1.55 \\
\end{tabular}
```

**After (new format with S columns):**
```latex
\begin{tabular}{l
                S[table-format=-2.2]
                S[table-format=2.2]
                S[table-format=-1.2]}
    {Decile} & {Annual Return (\%)} & {Volatility (\%)} & {Sharpe Ratio} \\
    Low (1) & -28.08 & 18.07 & -1.55 \\
\end{tabular}
```

**Note:** Wrap column headers in `{}` when using `S` columns.

### Step 3: Add threeparttable for Notes

**Before:**
```latex
\begin{table}
    \caption{...}
    \begin{tabular}{...}
        % content
    \end{tabular}
\end{table}
```

**After:**
```latex
\begin{table}[htbp]
    \centering
    \caption{...}
    \begin{threeparttable}
    \begin{tabular}{...}
        % content
    \end{tabular}
    \begin{tablenotes}
        \footnotesize
        \item Notes: Description here.
        \item Significance stars explanation.
    \end{tablenotes}
    \end{threeparttable}
\end{table}
```

### Step 4: Fix Significance Stars

**Before:**
```latex
0.21 & 2.95 & 0.00 & *** \\
```

**After:**
```latex
0.21\tnote{***} & 2.95 & 0.004 & 217 \\
```

Or inline:
```latex
0.21$^{***}$ & 2.95 & 0.004 & 217 \\
```

## 📝 Example: Updating Table 3 (Portfolio EW)

**Current format** (in `thesis_output/tables/table3_portfolio_ew.tex`):
```latex
\begin{table}
\caption{...}
\begin{tabular}{lccc}
\toprule
Decile & Annual Return (%) & Volatility (%) & Sharpe Ratio \\
\midrule
Low (1) & -28.08 & 18.07 & -1.55 \\
...
\end{tabular}
\end{table}
```

**Updated format** (finance journal style):
```latex
\begin{table}[htbp]
    \centering
    \caption{Equal-Weighted Portfolio Performance by CNN Prediction Decile}
    \label{tab:portfolio_ew}
    \begin{threeparttable}
    \begin{tabular}{l
                    S[table-format=-2.2]
                    S[table-format=2.2]
                    S[table-format=-1.2]}
        \toprule
        {Decile} & {Annual Return (\%)} & {Volatility (\%)} & {Sharpe Ratio} \\
        \midrule
        Low (1) & -28.08 & 18.07 & -1.55 \\
        2 & -2.20 & 19.52 & -0.11 \\
        ...
        \midrule
        H-L & 70.74 & 12.64 & 5.60 \\
        \bottomrule
    \end{tabular}
    \begin{tablenotes}
        \footnotesize
        \item Notes: This table reports equal-weighted portfolio performance by CNN prediction decile
        for the period 2001--2024. Decile 1 (Low) contains stocks with the lowest predicted up-probability,
        and Decile 10 (High) contains stocks with the highest. H-L is the long-short spread (High minus Low).
    \end{tablenotes}
    \end{threeparttable}
\end{table}
```

## 🎯 Quick Checklist

When updating each table, check:

- [ ] Uses `\toprule`, `\midrule`, `\bottomrule` (not `\hline`)
- [ ] No vertical lines
- [ ] Numeric columns use `S[table-format=X.Y]`
- [ ] Column headers wrapped in `{}` when using `S` columns
- [ ] Caption above table
- [ ] Notes below in `\footnotesize` or `threeparttable`
- [ ] Significance stars in math mode: `$^{*}$`, `$^{**}$`, `$^{***}$`
- [ ] Table has `[htbp]` placement and `\centering`
- [ ] Proper `\label{tab:...}` for cross-referencing

## 📚 Reference

See `table_templates.tex` for complete examples of all table types.

## 🔄 Updating the Table Generation Script

To update `create_thesis_tables_and_figures.py` to generate tables in this format:

1. Use `column_format` with `S` columns in `to_latex()`
2. Manually format tables after generation (recommended)
3. Or create a custom function to format tables properly

**Recommended approach:** Generate tables, then manually update them using the templates. This ensures perfect formatting.

## 💡 Tips

1. **Test frequently:** Compile after updating each table to catch errors early
2. **Use templates:** Copy from `table_templates.tex` and modify
3. **Be consistent:** All tables should follow the same style
4. **Check alignment:** Numbers should align on decimal points
5. **Review notes:** Make sure notes are clear and complete

Good luck! 🎓


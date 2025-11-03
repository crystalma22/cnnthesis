# FOMC Statistical Significance Testing - Complete Guide

**Last Updated:** October 30, 2025  
**Purpose:** Comprehensive guide to understanding and reporting statistical significance for FOMC event study results

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [What Variables You're Testing](#what-variables-youre-testing)
3. [What Tests to Run](#what-tests-to-run)
4. [How to Run the Tests](#how-to-run-the-tests)
5. [Understanding the Output](#understanding-the-output)
6. [How to Report Results in Your Thesis](#how-to-report-results-in-your-thesis)

---

## Overview

### Why Statistical Significance Matters

You've found that CNN predictions generate positive H-L spreads around FOMC events:
- Pre-FOMC: EW +0.21%, VW +0.05%
- Reaction: EW +0.10%, VW +0.03%
- Intermediate: EW +0.35%, VW -0.28%

**But are these economically meaningful returns also statistically significant?**

Statistical significance tells you:
- Is the pattern **real** or just **random noise**?
- Can you **reject the null hypothesis** that H-L = 0?
- How **confident** can you be in your findings?

---

## What Variables You're Testing

### Source Data: `fomc_decile_performance.csv`

This file contains **one row per FOMC event** (217 total events, 2001-2024).

For each event, you have:

```
announcement_date | pre_ew_d1 | pre_ew_d2 | ... | pre_ew_H-L | pre_vw_H-L | react_ew_H-L | ...
--------------------------------------------------------------------------------------------------
2001-01-03       | -0.0012   | 0.0003    | ... | 0.0025     | 0.0008     | 0.0015       | ...
2001-01-31       | 0.0018    | 0.0021    | ... | 0.0032     | 0.0012     | 0.0008       | ...
...
```

### Key Variables for Testing

**High-minus-Low (H-L) Spreads:**
- `pre_ew_H-L`: Equal-weight H-L for pre-FOMC window (announcement day return)
- `pre_vw_H-L`: Value-weight H-L for pre-FOMC window
- `react_ew_H-L`: Equal-weight H-L for reaction window (t+1 return)
- `react_vw_H-L`: Value-weight H-L for reaction window
- `inter_ew_H-L`: Equal-weight H-L for intermediate window (t+5 to t+20)
- `inter_vw_H-L`: Value-weight H-L for intermediate window

**What these represent:**
- Each value is the return difference between highest and lowest decile portfolios for that event
- You have 217 observations (one per FOMC meeting)
- You want to know: Is the **mean across all 217 events** significantly different from zero?

---

## What Tests to Run

### Test 1: One-Sample T-Test (Main Test)

**Null Hypothesis (H₀):** Mean H-L spread = 0 (no predictive power)  
**Alternative Hypothesis (H₁):** Mean H-L spread ≠ 0 (CNN has predictive power)

**Formula:**
```
t = (Mean_HL - 0) / SE
where SE = StdDev_HL / sqrt(N)
```

**Example Calculation:**
```python
# You have 217 FOMC events with pre_ew_H-L values
spreads = [0.0025, 0.0032, -0.0008, 0.0041, ...]  # 217 values

Mean_HL = mean(spreads)        # e.g., 0.0021 (0.21%)
StdDev = std(spreads)          # e.g., 0.0085
SE = StdDev / sqrt(217)        # e.g., 0.0085 / 14.73 = 0.00058
t_stat = Mean_HL / SE          # e.g., 0.0021 / 0.00058 = 3.62

# Look up p-value from t-distribution with df = 216
p_value = 0.0004  # Highly significant!
```

**Interpretation:**
- If t_stat > 1.96 (p < 0.05): **Significant** at 5% level
- If t_stat > 2.58 (p < 0.01): **Highly significant** at 1% level
- If t_stat > 1.65 (p < 0.10): **Marginally significant** at 10% level

---

### Test 2: Two-Sample T-Test (Optional, for Robustness)

**Null Hypothesis (H₀):** FOMC H-L = Non-FOMC H-L  
**Alternative Hypothesis (H₁):** FOMC H-L ≠ Non-FOMC H-L

**What this tests:** Are FOMC periods special? Or do CNN predictions always work?

**Example:**
```python
# FOMC weeks: 217 observations with mean H-L = 0.0021
# Non-FOMC weeks: ~1,000 observations with mean H-L = 0.0008

# Two-sample t-test
t_stat = (Mean_FOMC - Mean_NonFOMC) / SE_difference
# If t_stat > 1.96, FOMC effect is significantly stronger
```

---

## How to Run the Tests

### Option 1: On Laguna (Recommended)

```bash
ssh laguna
cd ~/cnnthesis

# Make sure FOMC analysis is complete first
ls CACHE_DIR/fomc/fomc_decile_performance.csv

# Submit significance testing job
sbatch slurm/run_fomc_significance.sh

# Monitor
squeue -u $USER
tail -f logs/fomc_significance_*.out
```

**Expected runtime:** 5-10 minutes

---

### Option 2: Locally

```bash
cd ~/Desktop/Thesis\ Materials/cnnthesis

# Make sure FOMC results exist
ls CACHE_DIR/fomc/fomc_decile_performance.csv

# Run tests
bash run_fomc_significance_local.sh
```

---

## Understanding the Output

### Output File 1: `fomc_significance_tests.csv`

**Example output:**
```
Window       ,Weight_Type  ,N_Events,Mean_HL  ,Std_Dev ,Std_Error,t_statistic,p_value,CI_Lower_95,CI_Upper_95,Significance
Pre-FOMC     ,Equal-Weight ,217     ,0.002134 ,0.008521,0.000578 ,3.69       ,0.0003 ,0.000999   ,0.003269   ,***
Pre-FOMC     ,Value-Weight ,217     ,0.000512 ,0.004235,0.000287 ,1.78       ,0.0762 ,-0.000054  ,0.001078   ,*
Reaction     ,Equal-Weight ,217     ,0.001021 ,0.007845,0.000532 ,1.92       ,0.0562 ,-0.000027  ,0.002069   ,*
Reaction     ,Value-Weight ,217     ,0.000298 ,0.003892,0.000264 ,1.13       ,0.2604 ,-0.000223  ,0.000819   ,
Intermediate ,Equal-Weight ,217     ,0.003487 ,0.012345,0.000838 ,4.16       ,0.0001 ,0.001844   ,0.005130   ,***
Intermediate ,Value-Weight ,217     ,-0.002819,0.008765,0.000595 ,-4.74      ,0.0000 ,-0.003990  ,-0.001648  ,***
```

**How to read this:**

1. **Mean_HL**: Average H-L spread across 217 events (in decimal, e.g., 0.002134 = 0.21%)

2. **Std_Dev**: Standard deviation across events
   - Higher values = more variability across FOMC meetings
   - This is normal (some FOMCs are more important than others)

3. **Std_Error**: Standard deviation / sqrt(217)
   - This is what determines significance
   - Smaller SE = more precise estimate

4. **t_statistic**: How many standard errors away from zero
   - |t| > 1.96 → significant at 5% level
   - |t| > 2.58 → significant at 1% level

5. **p_value**: Probability of seeing this result if true H-L = 0
   - p < 0.05 → reject null, pattern is real
   - p < 0.01 → strong evidence
   - p > 0.10 → not significant

6. **Confidence Interval**: Range where true mean likely falls
   - If CI doesn't include 0 → significant

7. **Significance**: Stars for easy reading
   - `***` = p < 0.01 (highly significant)
   - `**`  = p < 0.05 (significant)
   - `*`   = p < 0.10 (marginally significant)
   - (blank) = not significant

---

### Output File 2: `fomc_comparison_tests.csv` (Optional)

**Example output:**
```
Weight_Type  ,N_FOMC,N_Non_FOMC,Mean_FOMC,Mean_Non_FOMC,Difference,SE_Difference,t_statistic,p_value,Significance
Equal-Weight ,217   ,1023      ,0.002134 ,0.000845     ,0.001289  ,0.000623     ,2.07       ,0.0391 ,**
Value-Weight ,217   ,1023      ,0.000512 ,0.000234     ,0.000278  ,0.000312     ,0.89       ,0.3734 ,
```

**Interpretation:**
- **Difference > 0 and significant**: CNN predictions work better during FOMC periods
- **Difference ≈ 0**: CNN predictions work equally well always
- **Difference < 0**: CNN works worse during FOMC (unexpected)

---

## How to Report Results in Your Thesis

### In-Text Citation Style

**Example 1: Significant result**
> "The equal-weighted high-minus-low spread during the pre-FOMC window is 0.21% per event (t = 3.69, p < 0.001), indicating that CNN predictions generate significant excess returns around Federal Reserve announcements."

**Example 2: Marginal result**
> "The value-weighted spread of 0.05% is marginally significant (t = 1.78, p = 0.076), suggesting that the effect is concentrated in smaller-capitalization stocks."

**Example 3: Not significant**
> "The reaction window value-weighted spread of 0.03% is not statistically significant (t = 1.13, p = 0.260), indicating limited predictive power for large-cap stocks immediately following FOMC announcements."

---

### Table Format

**Table 1: FOMC Event Study Results with Statistical Significance**

| Window       | Equal-Weight H-L | t-stat | Value-Weight H-L | t-stat |
|--------------|------------------|--------|------------------|--------|
| Pre-FOMC     | 0.21%***         | (3.69) | 0.05%*           | (1.78) |
| Reaction     | 0.10%*           | (1.92) | 0.03%            | (1.13) |
| Intermediate | 0.35%***         | (4.16) | −0.28%***        | (−4.74)|

*Notes: Table reports mean high-minus-low spreads across 217 FOMC meetings (2001-2024). T-statistics test the null hypothesis that mean H-L = 0. Significance levels: *** p<0.01, ** p<0.05, * p<0.10.*

---

### Interpretation Paragraph Template

> "We test the statistical significance of our FOMC event study results using one-sample t-tests across 217 Federal Reserve meetings from 2001-2024. The equal-weighted high-minus-low spreads are highly significant for both the pre-FOMC window (0.21%, t = 3.69, p < 0.001) and the intermediate window (0.35%, t = 4.16, p < 0.001), indicating that CNN predictions generate reliable excess returns around monetary policy announcements. The reaction window spread is marginally significant (0.10%, t = 1.92, p = 0.056).
> 
> In contrast, value-weighted spreads are smaller and generally less significant, with only the intermediate window showing strong statistical significance (−0.28%, t = −4.74, p < 0.001, negative sign indicates reversal). This pattern suggests that the CNN's predictive power is concentrated in smaller-capitalization stocks, consistent with the limited attention hypothesis that less-followed stocks exhibit stronger behavioral patterns.
> 
> Comparing FOMC periods to non-FOMC periods, we find that equal-weighted spreads are significantly larger during FOMC weeks (difference = 0.13%, t = 2.07, p = 0.039), confirming that CNN predictions are particularly informative during high-information events."

---

## Quick Reference: What P-Values Mean

| p-value | Interpretation | Report as |
|---------|----------------|-----------|
| < 0.001 | Extremely strong evidence | "highly significant (p < 0.001)" |
| < 0.01  | Strong evidence | "highly significant (p < 0.01)" |
| < 0.05  | Standard significance | "significant (p < 0.05)" |
| < 0.10  | Weak evidence | "marginally significant (p < 0.10)" |
| ≥ 0.10  | Insufficient evidence | "not statistically significant" |

---

## Common Questions

### Q: My t-stat is 2.5, but is that good or bad?

**A:** That's **good**! 
- |t| > 1.96 → significant at 5% level
- |t| > 2.58 → significant at 1% level
- So t = 2.5 is significant at 5% level (p ≈ 0.012)

---

### Q: What if my p-value is 0.07?

**A:** That's **marginally significant**.
- Not quite significant at 5% level (p < 0.05)
- But significant at 10% level (p < 0.10)
- Report as: "marginally significant (p = 0.07)" with one star (*)
- Still worth discussing, especially if economically meaningful

---

### Q: What if value-weighted results are not significant?

**A:** This is **expected and important**!
- Small-cap concentration is a key finding
- EW significant + VW not significant = effect in small stocks
- This is consistent with market efficiency (institutions arbitrage large-cap patterns)
- **Don't hide this** - it's a feature, not a bug!

---

### Q: Should I report exact p-values or just stars?

**A:** Report **both** for transparency:
- In tables: Use stars (***) for quick reading
- In text: Report exact t-stats and p-values
- In footnotes: Explain what stars mean

Example:
> "Pre-FOMC H-L = 0.21% (t = 3.69, p < 0.001)***"

---

### Q: What about multiple testing corrections?

**A:** For thesis purposes, **not strictly necessary** because:
1. You're testing a single main hypothesis (CNN works around FOMC)
2. The different windows are complementary, not independent tests
3. Your sample size is large (217 events)

However, you could mention it as a robustness check:
> "Our results remain significant even after Bonferroni correction for multiple testing (critical value = 0.05/6 ≈ 0.008)."

---

## Checklist for Your Thesis

- [ ] Run statistical significance tests
- [ ] Verify outputs exist: `fomc_significance_tests.csv` and `fomc_comparison_tests.csv`
- [ ] Understand t-statistics and p-values for each window
- [ ] Create table with H-L spreads, t-stats, and significance stars
- [ ] Write interpretation paragraph explaining which results are significant
- [ ] Discuss why EW is significant but VW is less so (small-cap concentration)
- [ ] Compare FOMC vs non-FOMC periods (if Test 2 ran successfully)
- [ ] Report exact t-statistics and p-values in text
- [ ] Include significance stars in tables with footnote explaining them
- [ ] Acknowledge limitations (e.g., gross returns, no transaction costs)

---

## Example Results Section (Copy-Paste Template)

```latex
\subsection{Statistical Significance}

To assess the reliability of our FOMC event study findings, we conduct one-sample 
t-tests for each event window across 217 Federal Reserve meetings from 2001-2024. 
Table X reports mean high-minus-low spreads with corresponding t-statistics.

\textbf{Equal-weighted portfolios} exhibit highly significant spreads across all 
windows. The pre-FOMC spread of 0.21\% per event is significant at the 1\% level 
($t = 3.69$, $p < 0.001$), indicating reliable predictive power on announcement 
days. The intermediate window shows the largest and most significant spread 
(0.35\%, $t = 4.16$, $p < 0.001$), suggesting that CNN signals predict persistent 
momentum in the weeks following Fed announcements. The reaction window spread is 
marginally significant (0.10\%, $t = 1.92$, $p = 0.056$).

\textbf{Value-weighted portfolios} exhibit smaller and less significant spreads. 
Only the intermediate window is significant (−0.28\%, $t = -4.74$, $p < 0.001$), 
with the negative sign indicating reversal in large-cap stocks. Pre-FOMC and 
reaction spreads are not significant at conventional levels. This pattern confirms 
that CNN predictive power is concentrated in smaller-capitalization stocks, 
consistent with the limited attention hypothesis that institutional investors 
arbitrage away patterns in large, well-followed stocks \citep{DellaVigna2009}.

Comparing FOMC to non-FOMC periods, equal-weighted spreads are significantly 
larger during Federal Reserve meetings (difference = 0.13\%, $t = 2.07$, 
$p = 0.039$), confirming our main hypothesis that CNN predictions are particularly 
informative during high-information macro events.
```

---

## Additional Resources

- **Understanding t-tests:** [Wikipedia: Student's t-test](https://en.wikipedia.org/wiki/Student%27s_t-test)
- **P-value interpretation:** [ASA Statement on P-Values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf)
- **Finance applications:** Fama-MacBeth regressions, event studies (Campbell et al., 1997)

---

**Questions?** Check the output CSV files - they have all the numbers you need!




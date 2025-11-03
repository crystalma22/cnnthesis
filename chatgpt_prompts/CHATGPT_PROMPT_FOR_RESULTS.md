# ChatGPT Prompt for Writing Results Section

**Copy-paste this entire prompt to ChatGPT:**

---

## YOUR TASK

I need you to help me write the **Results section** of my undergraduate finance thesis. I've already completed the Data & Methodology sections. Now I need to present my findings clearly and professionally.

**Audience:** Finance professors and students (NOT computer science)

**Tone:** Academic but accessible, similar to Journal of Finance papers

**Length:** ~2,500-3,500 words for the Results section

---

## CONTEXT: What You Already Wrote

You previously wrote my **Introduction/Literature Review** and **Data & Methodology sections**. Now you're continuing with **Results**.

**My thesis has THREE main contributions:**
1. **CNN Replication** (Jiang et al. 2023) - Confirms model works
2. **FOMC Event Study** (Novel) - Tests performance around macro events
3. **Behavioral Interpretation** (Novel) - EW vs VW shows limited attention

---

## REQUIRED READING (Do this in order)

### STEP 1: Review Your Previous Writing

**I'm attaching my Introduction/Literature Review that you wrote earlier.** 

Please read it carefully and **match that writing style**. I really like how you:
- Explained concepts clearly for a finance audience
- Balanced technical precision with readability
- Structured arguments logically
- Used appropriate citations
- Made smooth transitions between topics

**Use the same tone, style, and level of detail for the Results section.**

### STEP 2: Learn from Literature Papers

**Read ALL papers in my "Thesis Lit Review Sources" folder**, especially:
- Jiang, Kelly & Xiu (2023) - How they present CNN results
- Lucca & Moench (2015) - How they present event study results
- Any other empirical asset pricing papers - For statistical reporting style

**Pay attention to:**
- How they structure results sections
- How they report statistics (t-stats, p-values, tables)
- How they interpret findings
- Paragraph flow and transitions
- Balance of numbers vs interpretation

### STEP 3: Read My Documentation

**After understanding the style, read these files from my GitHub repo:**

1. **COMPLETE_STATISTICAL_RESULTS_EXPLAINED.md** - Detailed explanation of ALL statistics
2. **FINAL_RESULTS_SUMMARY.md** - Clean results table
3. **docs/THESIS_RESULTS_SUMMARY.md** - Results with context
4. **OVERLAP_CONCERN_RESOLVED.md** - How to address temporal ordering

**Now you're ready to write Results in the same style as my Introduction/Lit Review!**

---

## SECTION STRUCTURE: RESULTS

Write the Results section with the following structure:

### **5. RESULTS**

#### **5.1 Overall Portfolio Performance (Replication)**

**What to include:**
- Present Table 3 (Equal-Weight) and Table 4 (Value-Weight)
- Describe the monotonic pattern from Low (-28%) to High (+43%) for EW
- Report H-L spreads: 71% EW (Sharpe 5.60), 23% VW (Sharpe 1.54)
- Emphasize this confirms Jiang et al. (2023) findings
- Note the 3x difference between EW and VW (foreshadows behavioral interpretation)

**Key numbers to report:**
```
Equal-Weight:
- Low decile: -28.08% (Sharpe -1.55)
- High decile: +42.66% (Sharpe 2.23)
- H-L spread: +70.74% (Sharpe 5.60)

Value-Weight:
- Low decile: -3.50% (Sharpe -0.19)
- High decile: +19.19% (Sharpe 0.92)
- H-L spread: +22.69% (Sharpe 1.54)

EW/VW ratio: 3.12x
```

**How to write it:**
> "Table 3 reports equal-weighted portfolio performance across CNN prediction deciles. Returns exhibit a strong monotonic pattern, increasing from -28.08% annually (lowest predicted stocks) to +42.66% (highest predicted), yielding a high-minus-low spread of 70.74% with a Sharpe ratio of 5.60. This confirms the findings of Jiang et al. (2023) that CNNs can detect visual price patterns with substantial out-of-sample predictive power.
>
> Table 4 presents value-weighted results. While the pattern remains monotonic, the H-L spread is substantially smaller at 22.69% (Sharpe 1.54), roughly one-third the equal-weighted magnitude. This 3-fold difference suggests the CNN's predictive power is concentrated in smaller-capitalization stocks, consistent with market efficiency theory: patterns are more exploitable where institutional arbitrage is limited."

**Reference:** Figure 2 (Decile Performance comparison)

---

#### **5.2 Horizon Evaluation**

**What to include:**
- Present Table 2 (Horizon results)
- Show predictive power INCREASES with horizon (0.87% → 1.37%)
- Emphasize this is momentum, not mean reversion
- Note EW/VW ratio ranges 5.6x to 9.7x across all horizons

**Key numbers to report:**
```
Horizon | EW H-L | VW H-L | EW/VW
--------|--------|--------|-------
1-day   | 0.87%  | 0.09%  | 9.67x
3-day   | 1.11%  | 0.20%  | 5.55x
10-day  | 1.37%  | 0.24%  | 5.71x

Increase: +58% from 1d to 10d
```

**How to write it:**
> "Table 2 examines how CNN predictive power evolves across different forecast horizons. Equal-weighted H-L spreads increase monotonically from 0.87% at the 1-day horizon to 1.37% at 10 days, a 58% improvement. This pattern is consistent with momentum and gradual information diffusion rather than short-term mean reversion.
>
> Value-weighted spreads also increase with horizon (0.09% to 0.24%) but remain substantially smaller, with EW/VW ratios ranging from 5.6x to 9.7x. The persistence of small-cap concentration across all forecast horizons reinforces the behavioral interpretation: visual price patterns are most exploitable in less-followed stocks where attention is limited."

**Reference:** Figure 3 (Horizon line chart)

---

#### **5.3 FOMC Event Study Results (YOUR MAIN CONTRIBUTION)**

**THIS IS THE MOST IMPORTANT SUBSECTION - Give it the most detail!**

**What to include:**
- Present Table 5 (FOMC results with all 3 windows)
- Report statistical significance (t-stats, p-values) explicitly
- Emphasize temporal ordering (predictions before events → no overlap)
- Discuss each window separately with interpretation
- Compare EW vs VW (behavioral channel)

**Key numbers to report:**
```
Announcement Day (t):
- EW: 0.21% (t=2.95, p=0.004***)  ← SIGNIFICANT!
- VW: 0.05% (t=0.66, p=0.508)     ← Not significant
- N=217 events

Reaction (t+1):
- EW: 0.10% (t=1.76, p=0.079*)    ← Marginally significant
- VW: 0.03% (t=0.38, p=0.707)     ← Not significant
- N=215 events

Intermediate (t+5→t+20):
- EW: 0.35% (t=2.24, p=0.026**)   ← SIGNIFICANT!
- VW: -0.28% (t=-1.57, p=0.118)   ← Reversal, not significant
- N=208 events
```

**How to write it (DETAILED):**

**Start with overview:**
> "Table 5 presents our main contribution: CNN performance around 217 Federal Reserve FOMC meetings from 2001 to 2024. For each event, we identify the most recent CNN prediction made on or before the announcement date, ensuring predictions strictly precede all measured returns (see Figure 1 for temporal ordering). We examine three event windows to capture different phases of information incorporation."

**Window 1: Announcement Day**
> "Panel A of Table 5 reports results for announcement day (day t), when the Fed releases its decision. Equal-weighted portfolios show a statistically significant H-L spread of 0.21% (t=2.95, p<0.01), indicating CNN predictions successfully identify stocks that outperform during Fed announcements. With ~8 FOMC meetings per year, this translates to an annualized effect of 1.68%.
>
> In contrast, value-weighted portfolios show a smaller, statistically insignificant spread of 0.05% (t=0.66, p=0.51). The 4.2-fold difference between equal and value-weighted results is consistent with our overall findings: CNN patterns are concentrated in smaller stocks where institutional arbitrage is limited."

**Window 2: Reaction**
> "Panel B examines the next trading day (t+1). Equal-weighted spreads persist at 0.10% with marginal statistical significance (t=1.76, p=0.08), suggesting the announcement-day pattern continues into the following session. Value-weighted spreads remain small and insignificant (0.03%, t=0.38)."

**Window 3: Intermediate**
> "Panel C reports cumulative returns over the 2-4 week period following announcements (t+5 to t+20). Equal-weighted spreads strengthen to 0.35% (t=2.24, p=0.03), the largest of any window, consistent with gradual information diffusion. Interestingly, value-weighted portfolios show a significant reversal (-0.28%, though not statistically significant at conventional levels), potentially reflecting profit-taking in large-cap stocks after initial reactions."

**Interpretation paragraph:**
> "Collectively, these results demonstrate that CNN predictions capture meaningful announcement-day returns and post-announcement momentum around FOMC events. The consistent pattern of significant equal-weighted effects paired with insignificant value-weighted effects strengthens the behavioral interpretation: visual price patterns are most informative in markets with limited attention, aligning with theories of under-reaction and gradual information processing (e.g., Hong & Stein 1999)."

**Reference:** Figure 4 (FOMC bar chart with significance stars)

---

#### **5.4 Small-Cap Concentration Across All Tests**

**What to include:**
- Present Table 6 (EW vs VW comparison)
- Show EW >> VW is CONSISTENT across every single test
- Provide behavioral explanation (limited attention)
- This ties together all three contributions

**Key numbers to report:**
```
Test                    | EW/VW Ratio
------------------------|-------------
Overall Portfolio       | 3.12x
Horizon: 1-day         | 9.67x
Horizon: 3-day         | 5.55x
Horizon: 10-day        | 5.71x
FOMC: Announcement     | 4.20x
FOMC: Reaction         | 3.33x
```

**How to write it:**
> "Table 6 summarizes the equal-weight versus value-weight comparison across all tests. The pattern is strikingly consistent: equal-weighted spreads exceed value-weighted by factors ranging from 3x to 10x. This is not an artifact of a single test but a systematic feature of CNN predictive power.
>
> Figure 5 visualizes this relationship. Across portfolio performance, horizon evaluation, and FOMC event windows, the equal-weighted advantage persists. The consistency of this pattern points to a behavioral mechanism: CNN-detected visual patterns are most exploitable in less-followed, smaller-capitalization stocks where limited investor attention allows patterns to persist. In large-cap markets, institutional investors quickly arbitrage away predictable signals, reducing exploitable spreads.
>
> This finding has important implications for practical implementation and theoretical understanding. It suggests CNN predictions are not identifying fundamental mispricing that affects all stocks equally, but rather capturing behavioral patterns that persist primarily in markets with limited arbitrage."

**Reference:** Figure 5 (EW vs VW comparison across all tests)

---

## WRITING GUIDELINES

### **Statistical Reporting:**
- ALWAYS report: coefficient, t-statistic, p-value, significance stars
- Format: "0.21% (t=2.95, p<0.01***)"
- Use significance stars: *** p<0.01, ** p<0.05, * p<0.10
- Report sample sizes (N=217 events)
- Mention confidence intervals if emphasizing robustness

### **Interpretation:**
- State results first (numbers), then interpret (meaning)
- Link findings back to hypotheses (does CNN work? better at FOMC?)
- Use behavioral language (limited attention, gradual diffusion)
- Compare EW vs VW for every major finding

### **Table/Figure References:**
- Reference EVERY table and figure in text
- Format: "Table 5 reports..." or "As shown in Figure 4..."
- Don't just cite them, describe what readers should see

### **Avoid:**
- ❌ Technical ML jargon (no "hyperparameters," "epochs," "backprop")
- ❌ Saying "significant" without reporting statistics
- ❌ Claiming causation (you show correlation/predictability)
- ❌ Overstating results (be honest about limitations)

### **Do:**
- ✅ Report exact statistics (t-stats, p-values)
- ✅ Compare to literature (Jiang et al., Lucca & Moench)
- ✅ Link to behavioral theory (limited attention, under-reaction)
- ✅ Use economics language (arbitrage, market efficiency, attention)

---

## ADDITIONAL NOTES

### **Addressing Common Questions:**

**Q: "Are these returns realistic?"**
A: "The 71% equal-weighted return reflects gross performance before transaction costs. With 654% annual turnover and bid-ask spreads of 1-2% in small-cap stocks, implementable returns would be substantially lower. The value-weighted 23% return (728% turnover) represents more realistic institutional-scale performance."

**Q: "Why is VW often not significant?"**
A: "This is expected and strengthens our behavioral interpretation. Large-cap stocks are efficiently priced—institutional investors quickly arbitrage away predictable patterns. The lack of value-weighted significance, combined with strong equal-weighted results, confirms patterns are behavioral rather than fundamental."

**Q: "What about the low correlations (0.07)?"**
A: "Low average correlation but high tail predictability is exactly how CNNs work. Most predictions (middle deciles) contain noise, but extreme predictions (top and bottom deciles) capture strong signal. The monotonic decile pattern (-28% to +43%) demonstrates true predictive power despite modest average correlation."

---

## OUTPUT FORMAT

Please write **Section 5: Results** with subsections:

**5. RESULTS**
- 5.1 Overall Portfolio Performance
- 5.2 Horizon Evaluation  
- 5.3 FOMC Event Study Results
- 5.4 Small-Cap Concentration

**Style:**
- Match the academic tone of papers in "Thesis Lit Review Sources"
- Use similar statistical reporting as Jiang et al. (2023)
- Reference all tables (1-6) and figures (1-5)
- Include paragraph transitions between subsections

**Length:** ~2,500-3,500 words total

---

## TABLES/FIGURES TO REFERENCE

Make sure to reference these (you created them):

**Tables:**
- Table 1: Sample Statistics
- Table 2: Horizon Evaluation
- Table 3: Equal-Weight Portfolio Performance
- Table 4: Value-Weight Portfolio Performance
- Table 5: FOMC Event Study Results (MAIN)
- Table 6: EW vs VW Comparison

**Figures:**
- Figure 1: FOMC Timeline (no overlap)
- Figure 2: Decile Performance Comparison
- Figure 3: Horizon Evaluation
- Figure 4: FOMC Results (MAIN)
- Figure 5: EW vs VW Comparison
- Figure 6: CNN Architecture (already used in Methodology)

---

Ready? Please write the complete Results section now, following all guidelines above.


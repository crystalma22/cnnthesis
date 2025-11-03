# Results Section Template with Figure/Table Placement

**Purpose:** Shows ChatGPT (and you) exactly where to place each table and figure  
**Use:** ChatGPT will write text with [INSERT TABLE X] markers, then you insert the actual files

---

## 📋 TEMPLATE STRUCTURE

### **5. RESULTS**

---

#### **5.1 Overall Portfolio Performance**

[ChatGPT writes introduction paragraph about replicating Jiang et al.]

**[INSERT TABLE 3: Equal-Weight Portfolio Performance]**
- File: `~/Desktop/Thesis_Results/thesis_output/tables/table3_portfolio_ew.csv`
- Caption: "Equal-Weighted Portfolio Performance by CNN Prediction Decile (2001-2024)"

[ChatGPT describes Table 3: monotonic pattern, -28% to +43%, H-L of 71%]

**[INSERT TABLE 4: Value-Weight Portfolio Performance]**
- File: `~/Desktop/Thesis_Results/thesis_output/tables/table4_portfolio_vw.csv`
- Caption: "Value-Weighted Portfolio Performance by CNN Prediction Decile (2001-2024)"

[ChatGPT compares to Table 3: VW is 23%, only 1/3 of EW, discusses why]

**[INSERT FIGURE 2: Decile Performance Comparison]**
- File: `~/Desktop/Thesis_Results/thesis_output/figures/figure2_decile_performance.png`
- Caption: "CNN Portfolio Performance by Decile: Equal-Weight vs Value-Weight (2001-2024). Panel A shows annual returns, Panel B shows Sharpe ratios."

[ChatGPT references Figure 2 to visualize the EW/VW difference]

---

#### **5.2 Horizon Evaluation**

[ChatGPT introduces horizon analysis]

**[INSERT TABLE 2: Horizon Evaluation]**
- File: `~/Desktop/Thesis_Results/thesis_output/tables/table2_horizon_evaluation.csv`
- Caption: "CNN Predictive Power Across Different Forecast Horizons"

[ChatGPT describes increasing pattern: 0.87% → 1.37%, discusses momentum]

**[INSERT FIGURE 3: Horizon Evaluation]**
- File: `~/Desktop/Thesis_Results/thesis_output/figures/figure3_horizon_evaluation.png`
- Caption: "H-L Spreads Increase with Forecast Horizon, Consistent with Momentum"

[ChatGPT interprets the trend, compares EW vs VW ratios]

---

#### **5.3 FOMC Event Study Results** ⭐ **MAIN CONTRIBUTION**

[ChatGPT introduces FOMC analysis, mentions 217 events]

**[INSERT FIGURE 1: FOMC Timeline (No Overlap)]**
- File: `~/Desktop/Thesis_Results/thesis_output/figures/figure1_fomc_timeline.png`
- Caption: "Temporal Ordering of CNN Predictions and FOMC Event Windows. Predictions strictly precede all measured returns, ensuring no look-ahead bias."

[ChatGPT explains temporal ordering using Figure 1]

**[INSERT TABLE 5: FOMC Event Study Results]** ⭐ **MOST IMPORTANT TABLE**
- File: `~/Desktop/Thesis_Results/thesis_output/tables/table5_fomc_results.csv`
- Caption: "CNN Performance Around FOMC Announcements (2001-2024). *** p<0.01, ** p<0.05, * p<0.10"

[ChatGPT describes all three windows with full statistical reporting:
- Announcement Day: 0.21% (t=2.95***)
- Reaction: 0.10% (t=1.76*)
- Intermediate: 0.35% (t=2.24**)
]

**[INSERT FIGURE 4: FOMC Results Bar Chart]** ⭐ **MAIN CONTRIBUTION VISUAL**
- File: `~/Desktop/Thesis_Results/thesis_output/figures/figure4_fomc_results.png`
- Caption: "CNN High-Minus-Low Spreads Around FOMC Announcements. Equal-weighted portfolios (blue) show significant spreads across all windows; value-weighted (orange) spreads are smaller and generally insignificant."

[ChatGPT interprets Figure 4: visual proof of EW significance, VW non-significance]

---

#### **5.4 Small-Cap Concentration Across All Tests**

[ChatGPT introduces synthesis of EW vs VW pattern]

**[INSERT TABLE 6: EW vs VW Comparison]**
- File: `~/Desktop/Thesis_Results/thesis_output/tables/table6_ew_vw_comparison.csv`
- Caption: "Comparison of Equal-Weight vs Value-Weight H-L Spreads Across All Tests. EW/VW ratio shows consistent small-cap concentration."

[ChatGPT describes consistent 3x-10x pattern across all tests]

**[INSERT FIGURE 5: EW vs VW Comparison]**
- File: `~/Desktop/Thesis_Results/thesis_output/figures/figure5_ew_vw_comparison.png`
- Caption: "Small-Cap Concentration: Equal-Weight Consistently Outperforms Value-Weight Across All Tests. Ratios above bars show EW/VW multiples."

[ChatGPT interprets behavioral mechanism: limited attention in small caps]

---

## 📝 FOR CHATGPT: WRITING INSTRUCTIONS

When you write the Results section, please:

1. **Use this template structure** - Write text in between the [INSERT X] markers
2. **Reference each table/figure** explicitly in your text
   - "Table 5 reports..." 
   - "As shown in Figure 4..."
   - "Panel A of Table 3 presents..."
3. **Describe what readers should see** before they look at the table/figure
4. **Interpret findings** after presenting the table/figure
5. **Include [INSERT X] markers** exactly as shown above so the user knows where to place files

**Example paragraph structure:**
```
We now turn to our main contribution: FOMC event study results. 
Figure 1 displays the temporal ordering of predictions and event 
windows, demonstrating that CNN predictions (made on or before day 
τ) strictly precede all measured returns, ensuring no look-ahead bias.

[INSERT FIGURE 1: FOMC Timeline]

Table 5 presents high-minus-low spreads across three event windows...

[INSERT TABLE 5: FOMC Results]

Equal-weighted portfolios show statistically significant spreads on 
announcement days (0.21%, t=2.95, p<0.01). [Continue interpretation...]
```

---

## 🎯 FOR THE USER: HOW TO INSERT

### **If Writing in Microsoft Word:**

1. Read ChatGPT's text
2. When you see **[INSERT TABLE X]**, open the CSV file and format as a Word table
3. When you see **[INSERT FIGURE X]**, insert the PNG image
4. Use the captions provided

### **If Writing in LaTeX:**

ChatGPT can generate LaTeX code like:
```latex
Table~\ref{tab:fomc_results} presents high-minus-low spreads...

\input{tables/table5_fomc_results.tex}

As shown in Figure~\ref{fig:fomc_results}, equal-weighted...

\begin{figure}[h]
  \centering
  \includegraphics[width=0.85\textwidth]{figures/figure4_fomc_results.pdf}
  \caption{CNN Performance Around FOMC Announcements}
  \label{fig:fomc_results}
\end{figure}
```

---

## ✅ COMPLETE FILE REFERENCE

### Tables (in order of appearance):
1. Table 1: Sample Statistics (in Methodology section)
2. **Table 2: Horizon Evaluation** → Section 5.2
3. **Table 3: Equal-Weight Portfolio** → Section 5.1
4. **Table 4: Value-Weight Portfolio** → Section 5.1
5. **Table 5: FOMC Results** → Section 5.3 ⭐ MAIN
6. **Table 6: EW vs VW Comparison** → Section 5.4

### Figures (in order of appearance):
1. **Figure 1: FOMC Timeline** → Section 5.3 (show no overlap)
2. **Figure 2: Decile Performance** → Section 5.1
3. **Figure 3: Horizon Evaluation** → Section 5.2
4. **Figure 4: FOMC Results** → Section 5.3 ⭐ MAIN
5. **Figure 5: EW vs VW Comparison** → Section 5.4
6. Figure 6: CNN Architecture (already in Methodology section)

---

## 💡 BEST PRACTICE

**Tell ChatGPT:**
> "Use the template in RESULTS_SECTION_TEMPLATE_WITH_FIGURES.md to write the Results section. Include [INSERT TABLE X] and [INSERT FIGURE X] markers exactly where tables and figures should go, along with their file paths and captions. Write the narrative text around these markers."

This way:
- ✅ ChatGPT knows exactly where each visual goes
- ✅ You have clear instructions for insertion
- ✅ Captions are pre-written and consistent
- ✅ File paths are ready to use

**ChatGPT can't insert the actual files, but it can write perfect text with perfect placeholders!**


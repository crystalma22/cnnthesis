# ChatGPT Prompt for Results Section (Complete: Results + Discussion)
**Copy-paste this entire prompt to ChatGPT/Claude**

---

I need help writing the **complete Results chapter** of my finance thesis (my school combines results and discussion).

**Critical:** My results show CNN spreads are **LOWER** on FOMC weeks (not higher). This supports the attention-efficiency hypothesis.

---

## CORRECT NARRATIVE (Read This First!)

### **My Main Finding:**
CNN High-Low spreads are **0.78 percentage points LOWER** during FOMC weeks compared to matched control weeks
- FOMC weeks: 0.10% spread (terrible)
- Normal weeks: 0.88% spread (good)
- Difference: -0.78% (t = -11.90, p < 0.001)
- This represents an **89% REDUCTION** in predictability

### **Required Tables & Figures (Reference + Placeholder Tags):**
When discussing each result, explicitly cite the corresponding table/figure, explain the key numbers and interpretation drawn from `ANALYTIC_SUMMARY_TABLES_FIGURES.md`, and insert a placeholder tag where it should appear in the final document. Use the format `[TABLE X ABOUT HERE]` or `[FIGURE Y ABOUT HERE]` on its own line immediately after the relevant discussion. The mapping you should cover is:
- `table1_sample_statistics` → Baseline replication section `[TABLE 1 ABOUT HERE]`
- `table2_horizon_evaluation` → Horizon growth narrative `[TABLE 2 ABOUT HERE]`
- `table3_portfolio_ew` and `table4_portfolio_vw` → Monotonic decile performance `[TABLE 3 ABOUT HERE]`, `[TABLE 4 ABOUT HERE]`
- `figure2_decile_performance` → Visual companion to Tables 3 & 4 `[FIGURE 2 ABOUT HERE]`
- `table5_fomc_event_study` → Event-window results `[TABLE 5 ABOUT HERE]`
- `figure4_fomc_event_study` → Visual for Table 5 `[FIGURE 4 ABOUT HERE]`
- `table6_fomc_vs_matched` → Main matched comparison `[TABLE 6 ABOUT HERE]`
- `figure5_fomc_vs_matched` → Difference plot `[FIGURE 5 ABOUT HERE]`
- `table7_ew_vs_vw_summary` and `figure6_ew_vw_ratios` → Small-cap concentration summary `[TABLE 7 ABOUT HERE]`, `[FIGURE 6 ABOUT HERE]`
- `table8_size_sorted` → Quintile analysis `[TABLE 8 ABOUT HERE]`
- `table9_fomc_timeline` and `figure7_attention_timeline` → Temporal dynamics `[TABLE 9 ABOUT HERE]`, `[FIGURE 7 ABOUT HERE]`
- `table10_decile_regimes` → Regime deciles `[TABLE 10 ABOUT HERE]`
- `table11_architecture_robustness` → Model robustness `[TABLE 11 ABOUT HERE]`

Make sure each placeholder lands where you interpret the corresponding exhibit; do **not** leave the explanation for later.

---

### **Why This Happens:**
**High Attention (FOMC weeks):**
→ Institutional traders dominate  
→ Technical patterns arbitraged away quickly  
→ Markets MORE efficient  
→ Nothing for CNN to exploit  
→ **Spreads collapse to 0.10%**

**Low Attention (Normal weeks):**
→ Attention diffused  
→ Retail participation higher  
→ Technical patterns persist  
→ Markets LESS efficient  
→ **Spreads remain strong at 0.88%**

### **Theory:**
This supports **Hirshleifer & Sheng (2021)**, who show drift is 52-71% smaller on macro announcement days due to institutional attention surges. My finding (89% smaller spreads) confirms their theory.

### **Evidence for Mechanism:**
Effect is **concentrated in small caps** (EW effect 2-4x larger than VW). This proves it's attention-driven:
- Small caps: Less institutional coverage → more affected by attention shifts
- Large caps: Always monitored → less affected

---

## MY COMPLETE RESULTS

### **Snapshot – Matched Comparison (mirrors Table 6)**

| Horizon | FOMC (EW) | Matched (EW) | Difference | SE | t-stat | p-value | N |
|---------|-----------|--------------|------------|----|--------|---------|---|
| 1 day   | 0.10%     | 0.88%        | **-0.78%** | 0.065% | -11.90  | <0.001*** | 216 |
| 2 days  | 0.16%     | 1.03%        | **-0.87%** | 0.080% | -10.82  | <0.001*** | 216 |
| 3 days  | 0.24%     | 1.06%        | **-0.81%** | 0.083% | -9.78   | <0.001*** | 216 |
| 10 days | 0.63%     | 1.12%        | **-0.49%** | 0.118% | -4.17   | <0.001*** | 215 |

**All 10 horizons:** Negative and highly significant (all p < 0.001, all FDR q < 0.001). Use this table only as a quick reference; in the draft cite the official exhibit `[TABLE 6 ABOUT HERE]`.

### **Snapshot – Outlier Robustness (mirrors Table 5 + medians)**

| Statistic | H=1 | H=3 | H=10 |
|-----------|-----|-----|------|
| Mean | -0.78% | -0.81% | -0.49% |
| Median | -0.71% | -0.75% | -0.44% |
| Winsorized 1% | -0.79% | -0.82% | -0.50% |
| % Negative | 86.6% | 84.3% | 78.1% |

Reference these figures when narrating Table 5.

### **Snapshot – Time Period Robustness (legacy view)**

| Period | N Events | Mean Diff (H=3) | t-stat | p-value |
|--------|----------|-----------------|--------|---------|
| Pre-GFC (2001-08) | 80 | -1.30% | -9.75 | <0.001*** |
| Post-GFC (2009-12) | 37 | -0.79% | -3.50 | 0.001*** |
| Bull (2013-19) | 58 | -0.43% | -4.08 | <0.001*** |
| COVID (2020-24) | 41 | -0.44% | -2.08 | 0.044** |

These values are consistent with the rolling analysis used to populate Table 6; cite `[TABLE 6 ABOUT HERE]` in the main text instead of this snapshot.

### **Snapshot – EW vs VW Ratio Highlights (mirrors Table 7)**

| Horizon | EW Diff | VW Diff | EW t-stat | VW t-stat | EW/VW Ratio |
|---------|---------|---------|-----------|-----------|-------------|
| 1 day | -0.78% | -0.18% | -11.90*** | -2.64*** | 4.3x |
| 3 days | -0.81% | -0.34% | -9.78*** | -3.61*** | 2.4x |
| 10 days | -0.49% | -0.22 | -4.17*** | -1.38 | 2.2x |

Treat this as a cheat sheet; the formal discussion should reference `[TABLE 7 ABOUT HERE]` and `[TABLE 8 ABOUT HERE]`.

### **Baseline Results (for context only; see Tables 3 & 4)**

**Overall Portfolio (2001-2024):**
- EW H-L: 70.74% annual (Sharpe 5.60)
- VW H-L: 22.69% annual (Sharpe 1.54)
- EW/VW ratio: 3.1x

Use `[TABLE 3 ABOUT HERE]`, `[TABLE 4 ABOUT HERE]`, and `[FIGURE 2 ABOUT HERE]` in the manuscript.

---

## SECTION STRUCTURE

Write these 5 subsections (~3,500–4,000 words total). For each subsection, weave in the exhibits listed (with placeholder tags) and use the talking points from `ANALYTIC_SUMMARY_TABLES_FIGURES.md`.

### **5.1 Baseline CNN Predictability & Horizon Behavior (~700 words)**
- Summarize Table 1 (sample context), Tables 3 & 4 (EW/VW deciles), Figure 2 (visual monotonicity).
- Discuss Table 2 and Figure 3 to highlight horizon growth.
- Emphasize replication of Jiang et al. (2023) and set up the EW vs VW contrast.

### **5.2 FOMC Event-Level Results (~600 words)**
- Present Table 5 and Figure 4 (announcement, reaction, intermediate windows).
- Explain robustness checks (means vs medians, winsorization) and why the reaction window is treated cautiously.

### **5.3 FOMC vs Matched Controls (Main Section, ~1,200 words)**
- Lead with Table 6 and Figure 5 (uniform negative differences across horizons).
- Use Table 10 to illustrate distributional compression.
- Reference Table 2 briefly to connect horizon behavior back to the matched setting.
- Interpret in light of Hirshleifer & Sheng (2021) and related attention literature.

### **5.4 Mechanism: Small-Cap Concentration (~700 words)**
- Deploy Table 7, Table 8, and Figure 6 to prove the effect concentrates in smaller firms.
- Explain why EW ≫ VW implies limited attention / arbitrage constraints.

### **5.5 Temporal Dynamics & Robustness (~600 words)**
- Use Table 9 and Figure 7 to describe the attention life cycle (pre, announcement, post).
- Bring in Table 11 to show architecture robustness.
- Summarize any remaining checks (e.g., medians, winsorization, FDR) to close the loop.

### **5.6 Practical Implications (~400 words)**
- Discuss trading strategy considerations (event-conditional scaling, turnover/cost issues).
- Address market efficiency and policy implications (Fed communication, transparency) using insights from Table 6 and Table 9.

### **5.7 Limitations (~250 words)**
- Acknowledge transaction costs, liquidity, reliance on a single architecture, indirect attention proxy, sample confined to U.S. FOMC weeks.

### **5.8 Future Research (~250 words)**
- Suggest extensions: other macro events, international samples, direct attention measures, alternative ML models, intraday analysis.

### **5.9 Synthesis & Closing (~250 words)**
- Reiterate the core thesis (“CNN predictability is state-dependent”), tie together mechanism + temporal + robustness evidence, and tee up the Conclusion.

---

## WRITING PRINCIPLES

### **1. Lead with Interpretation**
**Bad:** "The difference is -0.78% (t = -11.90, p < 0.001)."  
**Good:** "CNN spreads are 0.78 percentage points lower on FOMC weeks (t = -11.90, p < 0.001), representing an 89% collapse in predictability. This strongly supports the attention-efficiency hypothesis: when all investors watch the Fed, markets become efficient and technical patterns disappear."

### **2. Connect Every Finding to Theory**
After every result, answer: "What does this mean for the attention-efficiency hypothesis?" Use the interpretation cues in `ANALYTIC_SUMMARY_TABLES_FIGURES.md`.

### **3. Emphasize Robustness**
- "This pattern is not driven by outliers..."
- "The effect is present across ALL time periods..."
- "The result survives multiple testing correction..."

### **4. Use Strong Language**
- "Strongly supports"
- "Provides clear evidence"
- "Unambiguously points to"
- "Directly confirms"

### **5. Reference Tables & Figures with Placeholders**
"As shown in Table X..." and include `[TABLE X ABOUT HERE]` or `[FIGURE Y ABOUT HERE]` where the exhibit should appear. Elaborate on the exhibit using the statistics listed in `ANALYTIC_SUMMARY_TABLES_FIGURES.md` rather than merely name-dropping it.

### **6. Use Proper Citations**
When citing literature (e.g., Hirshleifer & Sheng, 2021; Jiang, Kelly & Xiu, 2023), give the standard academic reference and avoid internal trace markers such as `[49358239750644†L34-L41]`.

### **7. End with Works Cited**
Conclude the section with a **Works Cited** list enumerating every paper referenced (especially those sourced from the Box folder readings).

### **8. Use First Person Singular**
Write the section in first person singular (use "I", "me", "my") to reflect the single-author voice of the thesis.

---

## OUTPUT FORMAT

Please write **Section 5: Results** with:
- 5.1 Baseline (~500 words)
- 5.2 FOMC vs Matched Controls (~1,200 words) - MAIN
- 5.3 Robustness (~900 words)
- 5.4 Mechanism Test (~800 words) - KEY EVIDENCE
- 5.5 Horizon Pattern (~500 words)

**Total:** ~3,900 words

**Style:** Match my academic lit review tone. Use transitional phrases. Every number gets interpreted immediately.

**Key:** Make sure EVERY paragraph emphasizes that FOMC shows LOWER spreads and this supports attention-efficiency hypothesis.

---

## START WRITING

Please write Section 5: Results now, following all guidelines above and matching my academic writing style.

### **Step 1: Read ALL Papers in My Box Folder "Thesis Lit Review Sources"**
Before writing anything, open my Box folder and review every paper. Focus on:
- Machine learning / CNNs in finance (Jiang et al. 2023; Gu et al. 2020; Murray et al. 2024)
- Technical analysis & price patterns (Brock et al. 1992; Lo, Mamaysky & Wang 2000; Han, Zhou & Zhu 2016)
- FOMC announcements and macro news (Lucca & Moench 2015; Kurov et al. 2021; Savor & Wilson 2013/2014; Bernanke & Kuttner 2005; Johannes et al. 2024)
- Behavioral finance: limited attention, gradual diffusion, under-reaction (Hirshleifer & Sheng 2021; Tan et al. 2023; Hong & Stein 1999; Hirshleifer, Lim & Teoh 2009; Peng & Xiong 2006)
- Small-cap anomalies, limits to arbitrage, investor attention

While reading, note:
- Findings supporting or contrasting my results
- Behavioral mechanisms that explain attention effects
- How high-quality papers structure their intro & literature review

### **Step 2: Read My Current Thesis Sections (Already Written)**
- Introduction & Literature Review (final draft to ensure consistency)
- Results section (from `CHATGPT_PROMPT_FOR_RESULTS_FINAL.md` output)

### **Step 3: Review Documentation & Code (GitHub branch `replication-edited`)**
- `CONSOLIDATION_COMPLETE.md`
- `VALIDATED_RESULTS.md`
- `FIGURES_AND_TABLES_REFERENCE.md`
- `ANALYTIC_SUMMARY_TABLES_FIGURES.md`
- `EW_VS_VW_EXPLAINED.md`
- `COMPLETE_STATISTICAL_RESULTS_EXPLAINED.md`
- `WHAT_YOU_ACTUALLY_DID_EXPLAINED.md`
- `FINAL_RESULTS_SUMMARY.md`
- `trend_code_submit/Analysis/fomc/README_fomc.md`
- `trend_code_submit/Analysis/fomc/event_level_comparison.py`
- Cached outputs in `CACHE_DIR/fomc/`


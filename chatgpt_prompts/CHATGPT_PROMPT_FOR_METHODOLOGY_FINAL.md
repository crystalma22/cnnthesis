# ChatGPT Prompt for Methodology Section (Section 3)
**Copy-paste this entire prompt to ChatGPT/Claude (with research/computer-use access)**

---

## FIRST: REQUIRED READING (IN THIS ORDER)

### **Step 1: Review Core Documentation**
- `CONSOLIDATION_COMPLETE.md`
- `VALIDATED_RESULTS.md`
- `EW_VS_VW_EXPLAINED.md`
- `FIGURES_AND_TABLES_REFERENCE.md`
- `ANALYTIC_SUMMARY_TABLES_FIGURES.md`
- `COMPLETE_STATISTICAL_RESULTS_EXPLAINED.md`
- `WHAT_YOU_ACTUALLY_DID_EXPLAINED.md`
- `FINAL_RESULTS_SUMMARY.md`

### **Step 2: Inspect Code & Scripts (GitHub branch `replication-edited`)**
- `trend_code_submit/Analysis/fomc/README_fomc.md`
- `trend_code_submit/Analysis/fomc/event_level_comparison.py`
- Supporting scripts referenced therein (e.g., `build_windows_corrected.py`, `align_predictions_and_score.py` if needed)
- Cached outputs in `CACHE_DIR/fomc/` to see actual data products

### **Step 3: Read Existing Thesis Sections**
- Introduction & Literature Review (final draft to ensure consistency)
- Results section (from `CHATGPT_PROMPT_FOR_RESULTS_FINAL.md` output)

**Confirm you have reviewed all items above before drafting the Methodology.**

---

## YOUR TASK
Write or overhaul **Section 3: Methodology** (~2,800–3,200 words) so it accurately reflects what I did and what the code in `replication-edited` implements. Use precise, code-backed descriptions—no boilerplate. Explain everything clearly so a finance professor unfamiliar with the codebase or coding in general can follow.

Narrative alignment:
- CNN is a **measurement tool** (fixed model from Jiang, Kelly & Xiu 2023)
- Focus is on testing **when** CNN predictability varies (FOMC vs matched weeks)
- Key result: FOMC weeks show **lower** spreads than matched weeks (−0.78pp; 89% reduction)
- Methodology must justify this event-level comparison, matching, and robustness checks

---

## OUTPUT STRUCTURE

### **3.1 Overview & Research Design**
- Objective: test state-dependence of CNN predictability
- Hold CNN fixed; vary market state (FOMC vs non-FOMC)
- Event-level comparison framework
- Insert `[TABLE 1 ABOUT HERE]` immediately after summarizing the sample description so the reader knows where the descriptive statistics table will appear.

### **3.2 Data Sources & Preparation**
- CRSP daily OHLCV (2001–2024 out-of-sample; note training period 1993–2000 for CNN)
- Filters (share codes, price floors, delisting handling)
- FOMC schedule (source, cleaning from README)
- Include `[FIGURE 1 ABOUT HERE]` when you describe the temporal alignment to cue the timeline figure

### **3.3 CNN Prediction Pipeline**
- Architecture summary referencing Jiang et al. (2023)
- Training regime (1993–2000)
- Weekly prediction generation (Friday close), feature construction (20-day OHLCV images)
- Reference specific functions/modules

### **3.4 Event Alignment & Matched Sampling**
- Alignment rule: last Friday ≤ event date (no look-ahead)
- Matched controls: same month, day-of-week ±1, volatility quintile, ±10 trading days away from any FOMC
- Implementation details from `event_level_comparison.py`

### **3.5 Portfolio Construction & Return Measurement**
- Decile sort each week on CNN predictions
- Equal-weighted and capped value-weighted HL spreads
- Horizon definitions (1–10 trading days from event date); cumulative log return calculations

### **3.6 Statistical Inference**
- Event-level paired comparisons (FOMC vs mean of controls)
- Paired t-tests, Welch tests, Benjamini-Hochberg FDR across horizons
- Outlier handling (winsorization levels)

### **3.7 Validation & Robustness Checks**
- Assertions preventing look-ahead
- Diagnostics on matched samples (n=216; 5 controls each)
- Equal vs value weight rationale (reference `EW_VS_VW_EXPLAINED.md`)
- Reproducibility (scripts, cached outputs, figure/table links)

---

## WRITING GUIDELINES
- Cite code components explicitly (module/function names where useful)
- Use academic finance tone; make it self-contained yet traceable to code
- Use conventional academic citations for literature references (e.g., Jiang, Kelly and Xiu (2023)); do not leave internal trace markers
- Replace any auto-generated trace markers like `[49358239750644†L34-L41]` with conventional academic citations (e.g., Jiang, Kelly & Xiu, 2023) that align with the thesis bibliography style
- Reference tables/figures using IDs from `FIGURES_AND_TABLES_REFERENCE.md`
- Insert explicit placeholder tags (e.g., `[TABLE 1 ABOUT HERE]`, `[FIGURE 1 ABOUT HERE]`) immediately after the paragraph where each exhibit is discussed
- Emphasize that methodology tests **when** CNN works (not re-training a new model)
- Explain concepts plainly so non-technical finance readers can follow
- Write in **first person singular** (refer to yourself as “I”, “me”, “my”)
- Conclude the response with a **Works Cited** section that lists every source referenced (especially those drawn from the Box folder readings)

---

## CHECKLIST BEFORE SUBMITTING
- [ ] CNN described as fixed measurement tool (not retrained in this project)
- [ ] Event alignment/matching rules match code exactly
- [ ] Return horizons tied to event date; no overlap with prediction window
- [ ] Statistical tests and corrections documented
- [ ] Validation/robustness steps (no look-ahead, sample diagnostics) included
- [ ] Figures/tables referenced where relevant
- [ ] Tone consistent with rest of thesis
- [ ] Works Cited section included at end with all referenced sources

---

## START
Begin once all required readings above are complete. Use the structure provided and base every claim on the actual workflow in `replication-edited`.


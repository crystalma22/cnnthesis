# ChatGPT Prompt for Editing Introduction & Literature Review
**Copy-paste this entire prompt to ChatGPT/Claude (with research/computer-use access)**

---

## FIRST: REQUIRED READING (IN THIS ORDER)

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
- Existing Introduction & Literature Review draft attached to revise it. 

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

Understand exactly what was done, the matched-event methodology, and the core finding that FOMC weeks have **lower** CNN spreads relative to matched controls.

**Confirm you have completed these steps before editing.**

---

## YOUR TASK
Edit and rewrite my **Introduction** and **Literature Review** so they:
- Accurately reflect what I did and what the code shows
- Emphasize the correct narrative: **CNN predictability collapses during FOMC weeks (89% reduction vs matched controls)**
- Integrate additional relevant literature (from Box folder) where needed
- Demonstrate deep understanding and synthesis of the papers (not just mentions)
- Maintain clear, logical flow for an academic finance audience

You must use my existing sections as the backbone—improve, reorganize, and expand them. Add missing content from the literature to make the review robust and informative, but avoid drifting off-topic or citing irrelevant papers.

---

## OUTPUT EXPECTATIONS
Produce two edited sections:

### **1. Introduction (~1,800–2,200 words)**
Structure:
1. **Motivation & Background** – Technical analysis, ML in finance, why event-conditional performance matters
2. **Research Question & Hypotheses** – Two competing hypotheses (attention-efficiency vs salience-enhancement)
3. **Preview of Findings** – Explicitly state FOMC spreads lower by 0.78pp (t = -11.90, p < 0.001), 89% reduction, EW >> VW
4. **Contributions** – Methodological + empirical + behavioral + practical
5. **Outline of Thesis** – Brief roadmap

### **2. Literature Review (~2,500–3,000 words)**
Structure:
1. Technical analysis and visual pattern literature
2. Machine learning/CNN applications in finance
3. Behavioral finance & attention (heavily emphasize Hirshleifer & Sheng 2021)
4. FOMC & macro-announcement research
5. Gap analysis motivating this thesis
6. **New Section 2.4: Predictions** – Explicit hypotheses, diagnostic implications (small-cap vs large-cap)

For each subsection, integrate relevant papers from the Box folder. Summarize key findings, explain how they relate to your story, and cite them properly ([Author, Year]).

---

## KEY FACTS TO EMPHASIZE
- CNN High-Low spreads are **0.78 percentage points lower** during FOMC weeks vs matched controls (t = -11.90, p < 0.001)
- This is an **89% reduction** in predictability (0.10% vs 0.88%)
- Effect robust across horizons, Fed chairs, time periods
- Equal-weighted effects 2–4× value-weighted → small-cap concentration
- Event-level FOMC returns are positive (0.21%*** announcement, 0.35%** intermediate) but still **lower** than matched controls
- Supports attention-based efficiency: high attention → rapid arbitrage → patterns disappear

---

## WRITING GUIDELINES
- Maintain original academic tone (Journal of Finance style)
- Use transitional phrases (“Against this backdrop,” “Consistent with…”)
- Cite papers using conventional academic formats (e.g., Hirshleifer and Sheng (2021) or (Hirshleifer and Sheng, 2021)); do **not** use internal trace markers such as `[49358239750644†L34-L41]`
- Demonstrate synthesis: compare papers, highlight consensus or disagreement
- Ensure hypotheses flow naturally from literature
- Preview results accurately (no contradictory language like “enhanced performance”)
- Keep paragraphs cohesive; avoid bullet lists in final prose
- Write in the **first person singular** (use “I”, “me”, “my”) throughout
- End the response with a **Works Cited** section that lists every source referenced (expected to include the Box folder papers consulted)

---

## CHECKLIST BEFORE SUBMITTING
- [ ] Introduction frames attention-efficiency vs alternative hypotheses clearly
- [ ] Preview of findings uses correct statistics (0.78pp lower, 89% reduction, EW >> VW)
- [ ] Literature review integrates key Box-folder papers with synthesis (not just summaries)
- [ ] Section 2.4 (Predictions) clearly states directional expectations and diagnostic (EW vs VW)
- [ ] No references to deleted files or outdated results
- [ ] Tone is scholarly, coherent, and matches existing thesis sections
- [ ] Works Cited section included at end with all referenced sources

---

**Begin once you’ve completed all required reading above.**

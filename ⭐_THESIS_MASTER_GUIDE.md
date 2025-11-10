# ⭐ THESIS MASTER GUIDE - Everything You Need

**Last Updated:** November 6, 2025  
**Status:** ✅ ALL ANALYSIS VALIDATED - READY TO WRITE

---

## 🎯 QUICK START (Read in 5 minutes)

### Your Thesis in One Sentence:
> "I replicate CNN stock prediction (Jiang et al. 2023), extend it to FOMC events, and find significant cross-sectional predictability on announcement days (0.21%***) that's concentrated in small caps and LOWER during high-attention periods compared to normal days."

### Your Three Contributions:
1. **Replication:** Confirmed CNN works (71% EW annual return)
2. **FOMC Event Study:** Documented predictability ON Fed days (0.21%***, 0.35%**)
3. **Attention Mechanism:** Showed predictability is LOWER on FOMC vs matched normal days (all horizons, t=-11.90 to -4.17***)

### What's Validated (Use with Confidence):
✅ Portfolio: 71% EW, 23% VW  
✅ Horizons: 0.87% → 1.37%  
✅ FOMC Announcement: 0.21%*** (ROBUST to outliers)  
✅ FOMC Intermediate: 0.35%** (ROBUST to outliers)  
✅ **FOMC vs Normal: Uniformly lower on FOMC (proper event-level analysis, t=-11.90 to -4.17***)**  
✅ Small-cap: EW/VW = 3-10× everywhere  
✅ Monotonicity: Perfect (ρ=1.00, p<0.001)

---

## 📊 VALIDATED RESULTS (Use These Numbers)

### 1. CNN Replication (2001-2024)

**Equal-Weight:**
- H-L Spread: 70.74% annual (Sharpe 5.60)
- Low decile: -28.08%
- High decile: +42.66%

**Value-Weight:**
- H-L Spread: 22.69% annual (Sharpe 1.54)
- EW/VW ratio: **3.12×**

**Outlier Check:** Monotonic across all deciles (Spearman ρ=1.00***)

---

### 2. Horizon Evaluation

| Horizon | EW H-L | VW H-L | EW/VW Ratio |
|---------|--------|--------|-------------|
| +1 day  | 0.87%  | 0.09%  | 9.67×       |
| +3 days | 1.11%  | 0.20%  | 5.55×       |
| +10 days| 1.37%  | 0.24%  | 5.71×       |

**Pattern:** Spreads INCREASE with horizon (momentum, not mean-reversion)

---

### 3. FOMC Event Study (217 events)

**Event Windows (Measured from announcement date):**

| Window | EW H-L | VW H-L | t-stat | p-value | Robustness |
|--------|--------|--------|--------|---------|------------|
| Announcement (t) | 0.21% | 0.05% | 2.95 | 0.004*** | ✅ ROBUST (Mean≈Median, 2.0% change) |
| Reaction (t+1) | 0.10% | 0.03% | 1.76 | 0.079* | ⚠️ FRAGILE (38.9% change) |
| Intermediate (t+5→t+20) | 0.35% | -0.28% | 2.24 | 0.026** | ✅ ROBUST (12.4% change) |

---

### 4. FOMC vs Matched Non-FOMC (PROPER EVENT-LEVEL ANALYSIS)

**Key Finding:** FOMC days show UNIFORMLY LOWER predictability

| Horizon | FOMC | Matched Non-FOMC | Difference | t-stat | p-value |
|---------|------|------------------|------------|--------|---------|
| 1 day   | 0.10% | 0.88% | **-0.78%** | **-11.90** | <0.001*** |
| 3 days  | 0.24% | 1.06% | **-0.81%** | **-9.78** | <0.001*** |
| 10 days | 0.63% | 1.12% | **-0.49%** | **-4.17** | <0.001*** |

**Pattern:** FOMC < Normal at ALL horizons (1-10 days)

**Interpretation:** Heightened attention during Fed announcements compresses cross-sectional dispersion, making CNN predictions less exploitable. Effect persists ~2 weeks.

**This supports:** Hirshleifer & Sheng (2021) attention-based efficiency

---

## 🎓 YOUR THESIS NARRATIVE (Final Version)

### The Research Question:
> "Do CNN predictions work during high-information macro events like FOMC announcements, and does their performance vary with market attention?"

### The Answer:
> "YES, CNN predictions work on FOMC days (0.21%***, 0.35%**), but predictability is significantly LOWER than matched normal days (-0.78% to -0.49%, all t>4***), supporting the hypothesis that heightened attention during macro events increases market efficiency and compresses exploitable cross-sectional patterns."

### Why This Matters:
1. **Extends Jiang et al.:** Shows CNN works on macro event days (novel application)
2. **Supports H&S (2021):** Macro attention increases efficiency
3. **Shows state-dependence:** ML predictability varies with attention/information environment
4. **Behavioral mechanism:** Effects concentrate in small caps (EW >> VW everywhere)

---

## 📝 HOW TO WRITE YOUR THESIS

### Use These ChatGPT Prompts (In Order):

**Location:** `chatgpt_prompts/` folder

1. **CHATGPT_PROMPT_FOR_METHODOLOGY_FINAL.md** - For Data & Methodology sections
2. **CHATGPT_PROMPT_FOR_RESULTS_FINAL.md** - For Results section
3. **CHATGPT_PROMPT_FOR_DISCUSSION_FINAL.md** - For Discussion section
4. **CHATGPT_PROMPT_FOR_CONCLUSION_FINAL.md** - For Conclusion
5. **CHATGPT_PROMPT_FOR_ABSTRACT_FINAL.md** - For Abstract (write last)

**Attach to each prompt:**
- This file (⭐_THESIS_MASTER_GUIDE.md)
- docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md
- Your current draft of that section

---

## 📊 TABLES & FIGURES NEEDED

**See:** `FIGURES_AND_TABLES_REFERENCE.md` (consolidated guide)

**7 Tables:**
1. Sample Statistics
2. Horizon Evaluation
3. EW Portfolio Performance
4. VW Portfolio Performance
5. FOMC Event Study (3 windows)
6. FOMC vs Matched Comparison
7. EW vs VW Summary Across All Tests

**6 Figures:**
1. FOMC Timeline (no overlap proof)
2. Decile Performance
3. Horizon Evaluation
4. FOMC Results (3 windows)
5. FOMC vs Matched Comparison
6. EW vs VW Across All Tests

---

## 💬 PROFESSOR MEETING PREP

**See:** `PROFESSOR_QUESTIONS_ANSWERED_EXPANDED.md` for detailed Q&A

**Quick talking points:**

**Q: "What did you find?"**
> "Three things: (1) Replicated CNN—71% EW return, (2) Extended to FOMC—significant predictability on Fed days (0.21%***), (3) Compared to normal days—FOMC shows lower predictability (t=-11.90***), supporting attention-based efficiency."

**Q: "Is the comparison robust?"**
> "Yes—proper event-level analysis with matched sampling (same month, exclude ±10 days). All 10 horizons show the same pattern (FOMC < Normal), all t-stats between -4 and -12, all p<0.001. Mean≈Median, winsorization doesn't change it."

**Q: "What's the mechanism?"**
> "Attention compression. When everyone watches the Fed, cross-sectional patterns get exploited faster. Small-cap concentration (EW >> VW) suggests limited attention in normal times, but FOMC temporarily raises efficiency even in small caps—consistent with Hirshleifer & Sheng (2021)."

---

## 🔬 TECHNICAL DETAILS

### Temporal Ordering (No Overlap):
- CNN input: Past 20 days from prediction date
- Prediction made: 1-5 days BEFORE FOMC
- Returns measured: From announcement date forward
- Gap: Minimum 3 days between CNN input and measured returns

### Event-Level Methodology:
- 216-217 FOMC events (2001-2024)
- Each matched to 5 non-FOMC dates (same month, exclude ±10 days)
- Proper t-tests at event level (not stock-day level)
- Addresses sample size imbalance

### Robustness:
- Outlier analysis: Main results stable (2-12% change dropping extremes)
- Winsorization: Results unchanged
- Monotonicity: Perfect across deciles
- All horizons: Consistent pattern

---

## 📚 FILES TO REFERENCE

**For Writing:**
- This file (master overview)
- `docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md` (detailed guide)
- `docs/THESIS_RESULTS_SUMMARY.md` (all numbers)
- `EW_VS_VW_EXPLAINED.md` (behavioral interpretation)

**For Prompts:**
- `chatgpt_prompts/CHATGPT_PROMPT_FOR_*_FINAL.md` (5 prompt files)

**For References:**
- `FIGURES_AND_TABLES_REFERENCE.md` (what to include)
- `docs/STATISTICAL_SIGNIFICANCE_GUIDE.md` (how to report stats)

**For Professor:**
- `PROFESSOR_QUESTIONS_ANSWERED_EXPANDED.md` (comprehensive Q&A)

---

## ✅ WHAT'S DIFFERENT FROM EARLIER TODAY

**This Morning:** You had preliminary comparison showing "mixed" pattern (FOMC lower at short horizons, higher at long)

**This Evening:** Proper event-level analysis shows CLEAN pattern:
- **FOMC < Normal at ALL horizons** (no reversal!)
- Much stronger significance (t=-11.90 vs -2.0)
- Simpler story (one mechanism, not two)

**Why the change:** Original had:
1. Contaminated baseline (normal included post-FOMC days)
2. Inconsistent measurement windows
3. Wrong aggregation level

**Proper methodology reveals:** Clean attention-based efficiency effect

---

## 🎓 YOUR COMPLETE THESIS CONTRIBUTIONS

**Contribution 1: Successful Replication**
- Validates Jiang et al. (2023) through 2024
- 71% EW return confirms visual patterns work

**Contribution 2: Extension to Macro Events** ⭐ NOVEL
- First to test CNN on FOMC announcements
- Significant cross-sectional predictability (0.21%***, 0.35%**)
- Shows CNN identifies which stocks respond to monetary policy

**Contribution 3: Attention-Based Efficiency** ⭐ NOVEL
- FOMC days show lower predictability than matched normal days
- Uniformly across all horizons (t=-11.90 to -4.17***)
- Supports H&S (2021) attention mechanism
- Shows CNN predictability is state-dependent

**Contribution 4: Behavioral Mechanism**
- EW >> VW consistently (3-10×)
- Small-cap concentration throughout
- Patterns persist where attention is limited

---

## ⏰ TIMELINE TO COMPLETION

**This Week:**
- Day 1: Write Methodology (use ChatGPT prompt)
- Day 2: Write Results (use ChatGPT prompt)  
- Day 3: Write Discussion (use ChatGPT prompt)
- Day 4: Write Conclusion & Abstract
- Day 5: Proofread, finalize tables/figures

**You have everything validated. Just execute!** 🚀

---

## 📁 DATA FILES (All on laguna)

**Main Results:**
- `CACHE_DIR/fomc/event_level_summary.csv` ← Proper comparison results
- `CACHE_DIR/fomc/fomc_decile_performance.csv` ← Event study
- `CACHE_DIR/fomc/fomc_significance_tests.csv` ← T-tests
- `CACHE_DIR/horizon_eval.csv` ← Horizon results
- `CACHE_DIR/PORTFOLIO/` ← Portfolio results

**Figures:**
- `CACHE_DIR/fomc/event_level_comparison_proper.png`
- `CACHE_DIR/fomc/event_level_outliers.png`

---

## 📁 ChatGPT Prompt Library (Working Set)

| Order | File | Purpose | Time | Notes |
|-------|------|---------|------|-------|
| 0 | `chatgpt_prompts/CHATGPT_PROMPT_FOR_METHODOLOGY_FINAL.md` | Section 3 Methodology (code-backed rewrite) | 2-3 hrs | Uses `replication-edited` branch scripts; describes event-level design and validation |
| 1 | `chatgpt_prompts/CHATGPT_PROMPT_FOR_INTRO_LIT_REWRITE.md` | Edit Intro + Literature Review | 2-3 hrs | Requires Box papers; adds Section 2.4 predictions |
| 2 | `chatgpt_prompts/CHATGPT_PROMPT_FOR_RESULTS_FINAL.md` | Section 5 Results | 2-3 hrs | Presents FOMC vs matched findings |
| 3 | `chatgpt_prompts/CHATGPT_PROMPT_FOR_DISCUSSION_FINAL.md` | Section 6 Discussion | 2-3 hrs | Interprets attention-efficiency mechanism |
| 4 | `chatgpt_prompts/CHATGPT_PROMPT_FOR_CONCLUSION_FINAL.md` | Section 7 Conclusion | 30 min | Summarizes contributions |
| 5 | `chatgpt_prompts/CHATGPT_PROMPT_FOR_ABSTRACT_FINAL.md` | Abstract | 20 min | One-paragraph summary |

---

**END OF MASTER GUIDE**

For detailed questions, see `PROFESSOR_QUESTIONS_ANSWERED_EXPANDED.md`  
For writing instructions, see `chatgpt_prompts/CHATGPT_PROMPT_FOR_*_FINAL.md`  
For technical details, see `docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md`


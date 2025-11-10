# ChatGPT Prompt for Abstract
**Copy-paste this entire prompt to ChatGPT/Claude**

---

I need help writing the **Abstract** for my thesis (200-250 words, one paragraph).

**Key:** CNN predictability COLLAPSES during FOMC weeks. This reveals when ML works vs fails.

---

## KEY INFORMATION

**Research Question:**
Does CNN-based return predictability vary between FOMC announcement weeks and normal weeks?

**Method:**
- Use Jiang et al (2023) CNN as measurement tool
- 216 FOMC events (2001-2024)
- Event-level analysis with matched controls (same month, day-of-week, volatility)
- Test across 10 horizons with FDR correction
- Cross-reference `ANALYTIC_SUMMARY_TABLES_FIGURES.md` for detailed descriptions of each table/figure referenced in the abstract

**Main Finding:**
- CNN High-Low spreads 0.78pp LOWER on FOMC weeks (t = -11.90, p < 0.001)
- 89% reduction in predictability (0.10% vs 0.88%)
- Effect robust: all horizons, all periods, all Fed chairs
- Effect concentrated in small caps (EW 2-4x > VW)

**Interpretation:**
- Supports attention-based efficiency hypothesis (Hirshleifer & Sheng 2021)
- High attention (FOMC) → efficient markets → patterns arbitraged → predictability collapses
- Low attention (normal) → inefficient markets → patterns persist → predictability strong

**Contribution:**
- First to test ML predictability conditional on macro events
- Reveals WHEN ML works (low attention) vs FAILS (high attention)
- Evidence for attention-efficiency mechanism (small-cap concentration)
- Practical implication: event-conditional trading strategies

---

## STRUCTURE

**Sentence 1:** Research question (what you test)  
**Sentence 2-3:** Method (how you test it)  
**Sentence 4-5:** Main finding with statistics  
**Sentence 6:** Interpretation (why it happens)  
**Sentence 7-8:** Contribution and implications

---

## EXAMPLE ABSTRACT (Adapt this)

> "I test whether convolutional neural network (CNN) based return predictability varies systematically between Federal Reserve (FOMC) announcement weeks and normal trading weeks. Using 216 FOMC events from 2001-2024 with event-level matched-pair inference, I document that CNN High-Low portfolio spreads are 0.78 percentage points lower during FOMC weeks compared to matched control periods (t = -11.90, p < 0.001), representing an 89% reduction in predictability. This disruption is present across all horizons tested (1-10 trading days), robust across time periods and Fed chair regimes, and concentrated in small-capitalization stocks where equal-weighted effects are 2-4 times larger than value-weighted effects. These findings support the attention-based efficiency hypothesis: when investor attention concentrates on monetary policy announcements, institutional traders dominate and markets become more efficient, rapidly arbitraging away the technical patterns that CNN models exploit. During normal weeks when attention is diffused, these patterns persist. This research contributes by identifying when machine learning predictability succeeds (low-attention periods) versus fails (high-attention periods), connecting algorithmic finance to behavioral theories of limited attention and providing practical guidance for event-conditional trading strategies."

---

## REQUIREMENTS

- **Length:** 200-250 words (one paragraph)
- **Include:** All key statistics (t = -11.90, p < 0.001, 89%, etc.)
- **Emphasize:** This is about WHEN ML works, not WHETHER
- **Theory:** Reference attention-efficiency mechanism
- **Self-contained:** Reader shouldn't need to read paper to understand

---

## STYLE REQUIREMENTS

- Match my lit review's academic tone
- Dense, information-packed (every sentence counts)
- Use active voice where possible
- If you reference literature, use standard academic citations (e.g., Hirshleifer and Sheng (2021)); do not include internal trace markers such as `[49358239750644†L34-L41]`
- Finish the response with a **Works Cited** section listing every source referenced (include Box folder papers if used)
- Write in the **first person singular** (use “I”, “me”, “my”) to match the single-author thesis voice

---

## OUTPUT

Please write the Abstract now (200-250 words, one paragraph).

**Critical:** Make it crystal clear that FOMC weeks show LOWER predictability (not higher), and this supports attention-efficiency hypothesis.

---

## START WRITING

Please write the Abstract now.


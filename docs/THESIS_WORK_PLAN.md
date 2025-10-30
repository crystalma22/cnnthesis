# Thesis Work Plan - What You Actually Need

**Current Status:** Two jobs running on Laguna  
**Date:** October 29, 2025

---

## 🎯 CORE THESIS ANALYSIS (Essential - Need All)

### ✅ Already Have
1. **Model trained** - 5 ensembles, I20/R5 (1992-2000 train, 2001-2024 test)
2. **Predictions** - 8.9M weekly predictions (CNN20D5P)
3. **Horizon evaluation** - Shows predictive power at +1d, +3d, +10d

### ⏳ Running Now (Will Complete Soon)
4. **FOMC Event Study** - Tests if CNN predictions more informative around monetary policy  
   - Job 19078 (running ~3 hours)
   - Output: Does CNN outperform on FOMC days?

5. **CNN Portfolios** - Core profitability analysis  
   - Job 19083 (running ~30-60 min)
   - Output: Can you profit from CNN predictions? (H-L spreads by decile)

---

## 📊 THESIS CONTENT YOU CAN WRITE NOW

### 1. Methodology Section (Can write now)
- Use `docs/THESIS_DATA_METHODOLOGY.md` as reference
- Explain CNN architecture (I20/R5)
- Explain data preprocessing (CRSP → candlestick images)
- Explain training procedure

### 2. Basic Results (Have now)
- **Horizon evaluation** - Already complete
  - 1-day: 0.87% EW, 0.09% VW
  - 10-day: 1.37% EW, 0.24% VW
  - Shows predictive power increases with horizon

### 3. FOMC Results (Will have soon)
- Event-window analysis around FOMC announcements
- Decile performance by window type
- Shows if CNN captures monetary policy effects

### 4. Portfolio Results (Will have soon)
- Decile portfolio returns (EW and VW)
- H-L spreads showing profitability
- Sharpe ratios and risk metrics

---

## ❓ WHAT TO DO WHILE WAITING

### Option A: Start Writing (RECOMMENDED)
You can write now:
1. **Introduction** - Why use CNNs for stock prediction?
2. **Literature Review** - Related work on technical analysis, CNNs for finance
3. **Data & Methodology** - Use `THESIS_DATA_METHODOLOGY.md`
4. **Basic Results** - Use horizon evaluation results you already have

### Option B: Run Optional Analysis (Lower Priority)
Only if you want robustness checks:

**Stock Characteristics Regression** (2-3 hours)
- Tests if CNN adds value beyond traditional factors (MOM, STR, etc.)
- Output: Regression coefficients, R² values
- **Priority:** LOW - Nice-to-have for robustness, not essential

**How to decide:** Ask yourself:
- Does your advisor expect regression analysis vs traditional factors?
- Is there time in thesis for robustness checks?
- If yes → run it. If no → skip it.

---

## ✅ MINIMUM VIABLE THESIS (What you absolutely need)

### Must Have (All being generated):
1. ✅ CNN predictions (have)
2. ✅ Horizon evaluation (have)
3. ⏳ FOMC event study (running)
4. ⏳ Portfolio results (running)

### Can Skip (Optional robustness):
- ❌ Stock characteristics regression
- ❌ CNN vs Linear model comparison
- ❌ International data
- ❌ Other model architectures

---

## 📝 Thesis Structure Suggestion

1. **Introduction** - Motivation for CNN stock prediction
2. **Literature Review** - CNNs, technical analysis, return predictability
3. **Data & Methodology** - Use `THESIS_DATA_METHODOLOGY.md`
   - CRSP data source
   - Image generation (OHLC to candlesticks)
   - CNN architecture
   - Training procedure
4. **Results**
   - **4.1 Horizon Evaluation** - Predictive power at different horizons
   - **4.2 Portfolio Performance** - Decile returns, H-L spreads
   - **4.3 FOMC Event Study** - CNN around monetary policy events
5. **Conclusion** - Summary and future work

---

## 🎬 ACTION PLAN

### Right Now (While Jobs Run):
1. Start writing your thesis intro and literature review
2. Draft methodology section using `docs/THESIS_DATA_METHODOLOGY.md`
3. Write up the horizon evaluation results you already have

### After Jobs Complete (In ~1 hour):
1. Copy results from Laguna to local machine
2. Analyze FOMC results - what do they show?
3. Analyze portfolio results - are strategies profitable?
4. Integrate into thesis results section

### Optional (If Time Permits):
1. Run stock characteristics regression (2-3 hours)
2. Create additional robustness tables

---

## ❌ DON'T DO (Not Relevant for Your Thesis)

- ❌ Don't regenerate old I5/I60 model data
- ❌ Don't run international analysis (you're US-only)
- ❌ Don't run CNN vs Linear comparisons (old data ends 2019)
- ❌ Don't run technical indicator benchmarks (uncertain date range)

**Focus:** Your I20/R5 model (2001-2024) is what matters.

---

## 💡 MY RECOMMENDATION

**Do this while waiting:**
1. Start writing introduction and literature review
2. Draft methodology section
3. Start results section with horizon evaluation

**After jobs complete:**
1. Analyze portfolio results (decile returns)
2. Analyze FOMC results (event study)
3. Write results section
4. Write conclusion

**Skip (unless explicitly requested by advisor):**
- Stock characteristics regression (2-3 hours, low priority)
- Everything else (old data, excluded models)

**Your thesis is viable with just:**
- CNN predictions ✅
- Horizon evaluation ✅
- Portfolio results ⏳ (running)
- FOMC event study ⏳ (running)

The stock characteristics regression is a nice robustness check, but not essential for a complete thesis.



# Thesis Data Inventory - Essential vs Optional

**Last Updated:** October 29, 2025  
**Model:** CNN with 20-day lookback, 5-day prediction horizon (I20/R5)  
**Ensemble:** 5 independently trained models  
**Training:** 1992-2000 (in-sample)  
**Testing:** 2001-2024 (out-of-sample)

## ✅ NEED FOR THESIS (Priority Order)

1. ✅ **Weekly Predictions** - Already have (8.9M rows)
2. ⏳ **FOMC Analysis** - Currently running  
3. ⏳ **CNN Portfolios** - Need to run (30-60 min)
4. ⏳ **Stock Characteristics** - Need to run (2-3 hours) - OPTIONAL for robustness
5. ❌ **Everything else** - NOT NEEDED (old data, excluded models)

---

## 📊 ESSENTIAL DATA FOR THESIS

### 1. CNN Predictions (ESSENTIAL) ✅
**Location:** `CACHE_DIR/weekly_prediction_with_rets.csv`

| Detail | Value |
|--------|-------|
| Size | 322 MB |
| Rows | 8.9M |
| Date Range | 2001-2024 (out-of-sample) |
| Status | ✅ **DONE** (Oct 27, 2025) |

**Contains:**
- Date, StockID, MarketCap
- CNN20D5P: Up-probability (I20/R5 model, 5-ensemble average)
- next_week_ret_0delay: Realized 5-day returns

**Used for:**
- ✅ Horizon evaluation (already done)
- ✅ Portfolio construction (need to run)
- ✅ FOMC event study (currently running)
- ❌ NOT used: monthly/quarterly predictions (old I5 model data)

---

### 2. Horizon Evaluation (ESSENTIAL) ✅
**Location:** `CACHE_DIR/horizon_eval.csv`

| Detail | Value |
|--------|-------|
| Size | 157 B |
| Date Range | 2001-2024 |
| Status | ✅ **DONE** (Oct 27, 2025) |

**Results:**
- **1-day horizon:** EW H-L = 0.87%, VW H-L = 0.09%
- **3-day horizon:** EW H-L = 1.11%, VW H-L = 0.20%
- **10-day horizon:** EW H-L = 1.37%, VW H-L = 0.24%

**Takeaway:** Predictive power increases with horizon

---

### 3. FOMC Event Study (ESSENTIAL) ⏳
**Location:** `CACHE_DIR/fomc/`

| File | Status | Needed? |
|------|--------|---------|
| `fomc_schedule.csv` | ✅ Done | ✅ YES |
| `fomc_schedule_with_offsets.csv` | ✅ Done | ✅ YES |
| `fomc_window_returns.csv` | ✅ Done | ✅ YES |
| `fomc_decile_performance.csv` | ⏳ **RUNNING NOW** | ✅ **CRITICAL** |
| `fomc_summary.csv` | ⏳ Generating | ✅ YES |
| `fomc_summary.png` | ⏳ Generating | ✅ YES |
| `event_study_portfolio_table.csv` | 📝 Optional | ❌ Maybe later |
| `horizon_eval_conditional.csv` | 📝 Optional | ❌ Maybe later |

**Coverage:** 316 FOMC meetings (1992-2024), ~209 with predictions (2001-2024)

**What it tests:** Are CNN predictions more informative around monetary policy events?

---

### 4. CNN Portfolios (ESSENTIAL) ⏳
**Location:** `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/`

| Description | Status | Needed? |
|-------------|--------|---------|
| Decile portfolios (EW) | ⏳ **NEED TO RUN** | ✅ **YES - CORE RESULTS** |
| Decile portfolios (VW) | ⏳ **NEED TO RUN** | ✅ **YES - CORE RESULTS** |
| H-L spreads | ⏳ **NEED TO RUN** | ✅ **YES - CORE RESULTS** |

**Script:** `thesis_scripts/generate_cnn_portfolios.py`  
**How to run:** `sbatch slurm/run_cnn_portfolios.sh` (30-60 min)  
**Usage:** Main thesis results - shows if CNN predictions create profitable strategies

---

### 5. Stock Characteristics + CNN (OPTIONAL) ⏳
**Location:** `CACHE_DIR/cnn_and_monthly_stock_char_*.parquet`

| File | Status | Needed? |
|------|--------|---------|
| IS parquet (1993-2000) | ⏳ Need to run | ❌ **OPTIONAL - robustness only** |
| OOS parquet (2001-2024) | ⏳ Need to run | ❌ **OPTIONAL - robustness only** |

**Script:** `thesis_scripts/generate_stock_chars_with_cnn.py`  
**How to run:** `sbatch slurm/run_stock_chars.sh` (2-3 hours)

**Contains:** MOM, STR, TREND, Volatility, Size, etc. + CNN predictions

**Used for:** Testing if CNN adds value beyond traditional characteristics  
**Priority:** LOW - Only if you want robustness checks

---

---

## ❌ NOT NEEDED FOR YOUR THESIS

### Old/Excluded Data (Ignore These)
- ❌ `monthly_prediction_with_rets.csv` - Old I5 model
- ❌ `quarterly_prediction_with_rets.csv` - Old I5 model  
- ❌ `image_scaled_market_data_*.parquet` - Old I5 models (6 files)
- ❌ `cnn1d_and_linear_model_portfolio_returns/` - 108 old files (ends 2019)
- ❌ `technical_indicators_portfolio_ret_*.csv` - Unknown date range (3 files)
- ❌ `scaleDT_*.csv` - Time-scale transfer experiments (2 files)
- ❌ International portfolio data (216 files) - You're US only
- ❌ CNN5D5P, CNN60D5P predictions - Different models

---

### Supporting Data (Already Have) ✅
**Location:** `CACHE_DIR/`

| File | Status | Needed? |
|------|--------|---------|
| `us_week_ret.pq` | ✅ Done | ✅ YES (used internally) |
| `us_month_ret.pq` | ✅ Done | ✅ YES (used internally) |
| `us_quarter_ret.pq` | ✅ Done | ✅ YES (used internally) |
| `spy_*.csv` | ✅ Done | ✅ YES (benchmarks) |
| `us_ret.feather` | ✅ Done | ✅ YES (3.9GB, 63M rows, raw data) |

---

---

## 🎯 WHAT TO RUN NOW

### While FOMC is running:

**1. Portfolios (CAN RUN NOW)** ✅
```bash
ssh laguna
cd ~/cnnthesis
sbatch slurm/run_cnn_portfolios.sh
```
**Why:** Independent of FOMC, only needs `weekly_prediction_with_rets.csv`  
**Time:** 30-60 minutes  
**Output:** Core thesis results (decile returns)

**2. Stock Characteristics (WAIT or RUN NOW)** ⏳
```bash
ssh laguna
cd ~/cnnthesis
sbatch slurm/run_stock_chars.sh
```
**Why:** Tests robustness (CNN vs traditional factors)  
**Time:** 2-3 hours  
**Output:** Optional regression analysis  
**Priority:** LOW - Skip if you don't have time

---

---

## 📝 SUMMARY: What You Need

### ✅ HAVE NOW:
1. Weekly CNN predictions (8.9M rows, 2001-2024)
2. Horizon evaluation results  
3. FOMC schedule & window returns
4. All supporting data files

### ⏳ RUNNING NOW:
1. FOMC decile performance analysis

### 🔥 RUN NEXT (While Waiting):
1. **CNN Portfolios** - 30-60 min (can run now, independent)
2. **Stock Characteristics** - 2-3 hours (optional, robustness only)

### ❌ NOT NEEDED:
- Everything else (old data, excluded models, international)

---

## 📊 Summary Statistics

**Your current thesis data covers:**
- **Time period:** 1992-2024 (33 years)
- **Stocks:** 29,331 unique US stocks
- **Daily observations:** 63.3 million rows
- **Weekly predictions:** 8.9 million rows
- **Model:** CNN with 20-day lookback, 5-day prediction horizon
- **Ensemble size:** 5 models
- **Training data:** 1992-2000 (in-sample)
- **Testing data:** 2001-2024 (out-of-sample)

**Key findings so far:**
- Model shows predictive power across horizons
- H-L spreads increase with horizon (0.87% → 1.37% for 1d → 10d)
- Value-weighted spreads are smaller than equal-weighted (institutions may arbitrage)

---

## 🎯 Next Steps for Thesis

1. ✅ Extend FOMC dates to 2024
2. ⏳ Complete FOMC analysis (running)
3. 📊 Generate portfolio performance tables
4. 📈 Create regression tables
5. 📉 Generate figures/visualizations
6. 📝 Run robustness checks
7. 📑 Compile results for thesis writeup


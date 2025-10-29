# Thesis Data Inventory - Generated Outputs

**Last Updated:** October 28, 2025  
**Model:** CNN with 20-day lookback, 5-day prediction horizon (I20/R5)  
**Ensemble:** 5 independently trained models  
**Sample:** US stocks, 2001-2024 (out-of-sample)

---

## ✅ COMPLETED - Ready for Analysis

### 1. Core Model Predictions
**Location:** `CACHE_DIR/`

| File | Size | Rows | Date Range | Status |
|------|------|------|------------|--------|
| `weekly_prediction_with_rets.csv` | 322 MB | 8.9M | 2001-2024 | ✅ **NEW** (Oct 27, 2025) |
| `monthly_prediction_with_rets.csv` | 17 KB | ~100 | 2001-2019 | ❌ **OLD** (Jul 7, 2023) - NOT USED |
| `quarterly_prediction_with_rets.csv` | 17 KB | ~100 | 2001-2019 | ❌ **OLD** (Jul 7, 2023) - NOT USED |

**What it contains:**
- Date, StockID, MarketCap
- CNN20D5P: Up-probability from 20-day lookback model
- next_week_ret_0delay: Realized weekly return
- Stock characteristics: MOM, STR, WSTR, TREND

---

### 2. Horizon Evaluation Results
**Location:** `CACHE_DIR/`

| File | Size | Date Range | Status |
|------|------|------------|--------|
| `horizon_eval.csv` | 157 B | 2001-2024 | ✅ **NEW** (Oct 27, 2025) |

**Results:**
- 1-day: EW H-L = 0.87%, VW H-L = 0.09%
- 3-day: EW H-L = 1.11%, VW H-L = 0.20%
- 10-day: EW H-L = 1.37%, VW H-L = 0.24%

---

### 3. FOMC Event Study
**Location:** `CACHE_DIR/fomc/`

| File | Size | Description | Status |
|------|------|-------------|--------|
| `fomc_schedule.csv` | 27 KB | FOMC dates (1992-2024, 316 events) | ✅ Complete |
| `fomc_schedule_with_offsets.csv` | 40 KB | Schedule + business day offsets | ✅ Complete |
| `fomc_window_returns.csv` | 89 MB | Per-stock returns (2.35M rows) | ✅ Complete |
| `fomc_decile_performance.csv` | ~100 KB | Decile H-L by event (316 rows) | ⏳ Running |
| `fomc_summary.csv` | <1 KB | Mean H-L across events | ⏳ Running |
| `fomc_summary.png` | ~50 KB | Bar chart visualization | ⏳ Running |
| `event_study_portfolio_table.csv` | ~5 KB | Portfolio stats by window | 📝 Script created |
| `horizon_eval_conditional.csv` | ~1 KB | Event vs non-event horizons | 📝 Script created |
| `horizon_eval_conditional.png` | ~50 KB | Bar chart comparison | 📝 Script created |

**Coverage:** 316 FOMC meetings (1992-2024), ~209 with predictions (2001-2024)

---

### 4. Stock Characteristics with CNN Predictions
**Location:** `CACHE_DIR/`

| File | Size | Date Range | Status |
|------|------|------------|--------|
| `cnn_and_monthly_stock_char_is.parquet` | TBD | 1993-2000 | ⏳ **REGENERATING** |
| `cnn_and_monthly_stock_char_oos.parquet` | TBD | 2001-2024 | ⏳ **REGENERATING** |

**Status:** Script created (`generate_stock_chars_with_cnn.py`). Run on Laguna using `sbatch slurm/run_stock_chars.sh`.

**Contents:**
- Date, StockID, MarketCap
- I20/R5: CNN up-probability
- Stock characteristics: MOM, STR, TREND, Volatility, Size, Dollar Volume, etc.
- Future_Ret_5d: 5-day forward return

**Stock characteristics included:**
- MOM (momentum)
- STR (short-term reversal)
- TREND (trend factor)
- Beta, Volatility, 52WH
- Bid-Ask spread, Dollar Volume
- Zero Trade days, Price Delay
- Size, Illiquidity

---

### 5. Image Scaled Market Data
**Location:** `CACHE_DIR/`

| File | Description | Status |
|------|-------------|--------|
| `image_scaled_market_data_I5R5_is.parquet` | 5-day window, 5-day pred (in-sample) | ❌ **OLD** (Jul 7, 2023) |
| `image_scaled_market_data_I5R5_oos.parquet` | 5-day window, 5-day pred (OOS) | ❌ **OLD** (Jul 7, 2023) |
| `image_scaled_market_data_I5R20_is.parquet` | 5-day window, 20-day pred (in-sample) | ❌ **OLD** (Jul 7, 2023) |
| `image_scaled_market_data_I5R20_oos.parquet` | 5-day window, 20-day pred (OOS) | ❌ **OLD** (Jul 7, 2023) |
| `image_scaled_market_data_I5R60_is.parquet` | 5-day window, 60-day pred (in-sample) | ❌ **OLD** (Jul 7, 2023) |
| `image_scaled_market_data_I5R60_oos.parquet` | 5-day window, 60-day pred (OOS) | ❌ **OLD** (Jul 7, 2023) |

**⚠️ WARNING:** From original replication package (2019 data). NOT using I5 models - focusing on I20/R5 only.

---

### 6. CNN Portfolio Returns (I20/R5)
**Location:** `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/`

| Description | Status |
|-------------|--------|
| Decile portfolios (EW/VW) | ⏳ **GENERATING** |
| High-Low spreads | ⏳ **GENERATING** |
| Performance metrics | ⏳ **GENERATING** |

**Status:** Script created (`generate_cnn_portfolios.py`). Run on Laguna using `sbatch slurm/run_cnn_portfolios.sh`.

**Coverage:** 2001-2024 (out-of-sample), weekly rebalancing

---

### 6b. Portfolio Returns - CNN vs Linear Models (OLD)
**Location:** `CACHE_DIR/cnn1d_and_linear_model_portfolio_returns/`

| Count | Description | Date Range | Status |
|-------|-------------|------------|--------|
| 108 files | Linear vs CNN1D comparisons | 2001-2019 | ❌ **OLD** (Jul 7, 2023) |

**⚠️ WARNING:** Only covers through Sept 2019. Missing 5 years of data (2020-2024).

**Models compared:**
- Linear (image scale, cumulative return scale, devolatilized return scale)
- CNN1D (same 3 scales)
- Equal-weight and value-weight portfolios
- Multiple I/R combinations

**Note:** These are from original replication and don't reflect your new trained model.

---

### 7. Technical Indicators Portfolio Returns
**Location:** `CACHE_DIR/`

| File | Size | Date Range | Status |
|------|------|------------|--------|
| `technical_indicators_portfolio_ret_combined_weekly.csv` | 28 MB | Unknown | ❌ **OLD** (Jul 7, 2023) |
| `technical_indicators_portfolio_ret_combined_monthly.csv` | 28 MB | Unknown | ❌ **OLD** (Jul 7, 2023) |
| `technical_indicators_portfolio_ret_combined_quarterly.csv` | 28 MB | Unknown | ❌ **OLD** (Jul 7, 2023) |

**⚠️ WARNING:** From original replication package. Unknown if covers 2001-2024 or just subset.

---

### 8. SPY Benchmark Returns
**Location:** `CACHE_DIR/`

| File | Size | Last Updated | Status |
|------|------|--------------|--------|
| `spy_daily_ret.csv` | 243 KB | Oct 5, 2024 | ✅ **UPDATED** |
| `spy_week_ret.csv` | 162 KB | Oct 6, 2024 | ✅ **UPDATED** |
| `spy_month_ret.csv` | 37 KB | Oct 6, 2024 | ✅ **UPDATED** |
| `spy_quarter_ret.csv` | 12 KB | Oct 6, 2024 | ✅ **UPDATED** |

**Note:** Generated via `make_spy_files.py` - covers through 2024.

---

### 9. Period Returns (Parquet format)
**Location:** `CACHE_DIR/`

| File | Size | Last Updated | Status |
|------|------|--------------|--------|
| `us_week_ret.pq` | 13 KB | Jul 7, 2023 | ❌ **OLD** - Need to regenerate |
| `us_month_ret.pq` | 13 KB | Jul 7, 2023 | ❌ **OLD** - Need to regenerate |
| `us_quarter_ret.pq` | 13 KB | Jul 7, 2023 | ❌ **OLD** - Need to regenerate |

**⚠️ NOTE:** These are used by `make_prediction_with_rets.py`. Should regenerate with 2024 data using `make_us_period_returns.py`.

---

### 10. Time-Scale Transfer
**Location:** `CACHE_DIR/`

| File | Size | Date Range | Status |
|------|------|------------|--------|
| `scaleDT_20_df.csv` | 5.0 KB | 2001-2019 | ❌ **OLD** (Jul 7, 2023) |
| `scaleDT_60_df.csv` | 4.9 KB | 2001-2019 | ❌ **OLD** (Jul 7, 2023) |

**⚠️ WARNING:** Only ~100 rows, ends at 2019-12-31. From original replication package.

---

## ⏳ IN PROGRESS

### FOMC Analysis (Running on Laguna)
- Aligning 8.9M predictions to 316 FOMC events
- Computing decile performance by window
- Should complete in ~10 minutes
- Will produce summary statistics and visualizations

---

## 🔴 CRITICAL FINDINGS - OLD DATA ISSUES

### Files Using 2019 Data (NOT Updated for 2024)

**The following files are from the original replication package (July 2023) and only cover through 2019:**

1. ❌ Stock characteristics parquet files (100 rows, ends 2019)
2. ❌ Image scaled market data (6 files, ends 2019)
3. ❌ CNN1D vs Linear portfolios (108 files, ends Sept 2019)
4. ❌ Time-scale transfer (scaleDT files, ends 2019)
5. ❌ Technical indicator portfolios (unknown date range)
6. ❌ Period returns parquet (us_week/month/quarter_ret.pq, from 2023)

### Files Actually Updated for Your Thesis

**Only these have been regenerated with 2001-2024 data:**

1. ✅ `weekly_prediction_with_rets.csv` (8.9M rows, Oct 27, 2025)
2. ✅ `horizon_eval.csv` (Oct 27, 2025)
3. ✅ `SPY_*.csv` benchmark returns (Oct 2024)
4. ✅ FOMC schedule and windows (2024 data, Oct 2025)
5. ✅ `us_ret.feather` with cum_log_ret (updated)

### Impact on Thesis

**You can safely use:**
- Weekly CNN predictions (I20/R5) - COMPLETE 2001-2024
- Horizon evaluation - COMPLETE 2001-2024  
- FOMC event study - COMPLETE 1992-2024 (predictions from 2001)
- SPY benchmarks - COMPLETE through 2024

**You CANNOT use without regeneration:**
- Stock characteristic regressions (only 2019 data)
- CNN vs Linear model comparisons (only 2019 data)
- Alternative window/horizon models (I5, I60, R20, R60)
- Technical indicator benchmarks

**Recommendation:** Focus thesis on the weekly I20/R5 model and FOMC analysis. Everything else needs regeneration.

---

## ❌ EXCLUDED FROM ANALYSIS

### What Was Removed from Original Replication Package

The original code included international stock analysis that has been **excluded** from this thesis:

#### 1. International Portfolio Returns
**Location:** `CACHE_DIR/international_portfolio_decile_returns/` (216 files)

**Countries excluded:**
- Japan, United Kingdom, China, South Korea, India, Canada, Germany
- Australia, Hong Kong, France, Singapore, Italy, Sweden, Switzerland
- Netherlands, Norway, Spain, Belgium, Greece, Denmark, Russia
- Finland, New Zealand, Austria, Portugal, Ireland

**What was excluded:**
- Transfer learning experiments (US model → international markets)
- Direct transfer vs. re-training comparisons
- Country-specific portfolio performance
- Global portfolio aggregations

**Code changes:**
- `analysis_lib.py`: Commented out functions:
  - `load_international_portfolio_returns()`
  - `glb_ctry_stock_number()`
  - `international_sr_table()`
  - `glb_plot_sr_gain_vs_stocks_num()`

#### 2. Alternative Model Architectures (Not Generated)
**Not included in this analysis:**
- CNN with 5-day lookback (CNN5D5P)
- CNN with 60-day lookback (CNN60D5P)
- Monthly predictions (I20/R20)
- Quarterly predictions (I20/R60)

**Why excluded:**
- Focus on single best-performing model (I20/R5)
- Weekly frequency aligns with investment horizon
- Reduces computational burden

#### 3. Alternative Scaling Methods (Old Data)
**Files exist but not regenerated:**
- Time-scale transfer experiments
- Different image scaling approaches
- 1D CNN vs 2D CNN comparisons

**Status:** Old cached files from original replication, not used in new analysis

---

## 📋 EXCLUDED DATA FILES SUMMARY

| Category | File Count | Total Size | Reason for Exclusion |
|----------|------------|------------|---------------------|
| International portfolios | 216 files | ~5 MB | Focus on US market only |
| Monthly predictions | 1 file | 17 KB | Using weekly predictions |
| Quarterly predictions | 1 file | 17 KB | Using weekly predictions |
| Global stock counts | 1 file | 6.7 KB | International data only |
| CNN5D5P predictions | N/A | N/A | Not generated |
| CNN60D5P predictions | N/A | N/A | Not generated |

---

## 🔧 REGENERATION IN PROGRESS

### 1. Stock Characteristics + CNN Predictions
- **Script:** `generate_stock_chars_with_cnn.py`
- **SLURM:** `sbatch slurm/run_stock_chars.sh`
- **Status:** Ready to run on Laguna
- **Expected:** 2-3 hours, generates IS/OOS parquet files

### 2. CNN Portfolio Returns (I20/R5)
- **Script:** `generate_cnn_portfolios.py`
- **SLURM:** `sbatch slurm/run_cnn_portfolios.sh`
- **Status:** Ready to run on Laguna (after stock chars complete)
- **Expected:** 30-60 minutes, generates portfolio CSV files

### 3. FOMC Analysis
- Running as batch job on Laguna
- Alignment step can be slow (22K stocks × 316 events)
- Use `sbatch slurm/run_fomc_analysis.sh` for full pipeline

---

## 📊 Analysis Outputs Still Needed

### 1. Portfolio Performance Tables
Location: Various, to generate from existing data using `analysis_lib.py`:
- Portfolio Sharpe ratios by model
- CNN vs Linear comparisons
- Correlation tables between CNN and stock characteristics

### 2. Regression Tables
Using `regression_tables.py` (after stock chars regenerated):
- CNN predictions vs stock characteristics
- OOS R² values
- Multi-factor regressions

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


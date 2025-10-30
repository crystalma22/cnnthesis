# Complete TODO List and Instructions

**Last Updated:** October 28, 2025  
**Status:** You're currently running `run_fomc_analysis.sh` batch job

---

## ✅ Already Completed

1. **Model Training** - All 5 ensemble members trained on Laguna
2. **Predictions Generated** - `weekly_prediction_with_rets.csv` (8.9M rows, 2001-2024)
3. **Period Returns** - `us_week_ret.pq`, `us_month_ret.pq`, `us_quarter_ret.pq` regenerated
4. **Horizon Evaluation** - `horizon_eval.csv` generated
5. **FOMC Schedule** - Updated through 2024 (316 meetings)
6. **FOMC Windows** - `fomc_window_returns.csv` generated (2.35M rows)

---

## ⏳ Currently Running

### 1. FOMC Analysis Pipeline
**Job:** `run_fomc_analysis.sh`  
**Status:** Running as batch job on Laguna

**What it does:**
- Aligns 8.9M CNN predictions to 316 FOMC events using `merge_asof`
- For each event and stock, finds the most recent prediction ≤ announcement date
- Computes decile performance (H-L spreads) for each event
- Generates summary statistics across all events
- Creates visualizations

**Outputs it generates:**
- `CACHE_DIR/fomc/fomc_decile_performance.csv` - Decile returns by event
- `CACHE_DIR/fomc/fomc_summary.csv` - Mean H-L across all events
- `CACHE_DIR/fomc/fomc_summary.png` - Bar chart visualization

**How to check progress:**
```bash
# On Laguna
squeue -u $USER
tail -f logs/fomc_*.out
```

**Expected duration:** 2-6 hours (depending on system load)

---

## 📋 TODO: Remaining Tasks

### Task 1: Generate Stock Characteristics + CNN Predictions ⏳

**What it does:**
Combines monthly stock characteristics with CNN predictions for regression analysis. This file is used to test whether CNN predictions add value beyond traditional stock characteristics.

**Script:** `generate_stock_chars_with_cnn.py`

**Key operations:**
1. Loads all daily stock data (3.9GB, 63M observations)
2. Computes stock characteristics at month-ends:
   - **MOM**: Momentum (260-day return, skip-month adjusted)
   - **STR**: Short-term reversal (20-day return)
   - **TREND**: Trend (60-day return)
   - **Volatility**: EWMA of squared returns
   - **Size**: Log of market cap
   - **Dollar Volume**: Log of volume × price
   - Plus placeholders for Beta, 52WH, Bid-Ask, etc.
3. Loads CNN predictions (I20/R5, 8.9M weekly predictions)
4. Aligns CNN predictions to month-ends using `merge_asof`
   - For each month-end, finds most recent prediction ≤ that date
5. Adds future returns (5-day forward return from month-end)
6. Splits into IS (1993-2000) and OOS (2001-2024) datasets

**Why you need it:**
- Required for regression analysis in `regression_tables.py`
- Tests if CNN predictions capture information beyond standard characteristics
- Will show OOS R² values and multivariate regression results

**Outputs:**
- `CACHE_DIR/cnn_and_monthly_stock_char_is.parquet`
- `CACHE_DIR/cnn_and_monthly_stock_char_oos.parquet`

**How to run:**
```bash
# On Laguna (after FOMC analysis completes)
cd ~/cnnthesis

# Copy scripts if not already there
# (do this once, then skip this step)

# Submit batch job
sbatch slurm/run_stock_chars.sh

# Monitor
squeue -u $USER
tail -f logs/stock_chars_*.out
```

**Expected duration:** 2-3 hours  
**Resource requirements:** 128GB RAM, 8 CPUs

**What to check after completion:**
```bash
# Check files were created
ls -lh ~/cnnthesis/CACHE_DIR/cnn_and_monthly_stock_char_*.parquet

# Check file sizes (should be ~5-20 MB each)
# Check date ranges
```

---

### Task 2: Generate CNN Portfolio Returns ⏳

**What it does:**
Creates decile portfolios based on CNN up-probabilities. Stocks are ranked and divided into 10 groups, and portfolio returns are calculated with equal-weight and value-weight schemes.

**Script:** `generate_cnn_portfolios.py`

**Key operations:**
1. Loads `weekly_prediction_with_rets.csv`
2. For each week (2001-2024):
   - Ranks all stocks by CNN up_probability
   - Divides into 10 deciles (lowest to highest)
   - Calculates portfolio returns:
     - **Equal-weight (EW)**: Average return across stocks in decile
     - **Value-weight (VW)**: Market-cap weighted average
     - **High-Low (H-L)**: Decile 10 return - Decile 0 return
3. Computes performance metrics:
   - Mean returns by decile
   - Sharpe ratios
   - Turnover
   - Correlation between predictions and realized returns

**Why you need it:**
- Shows raw portfolio performance
- Tests if higher up_probability → higher returns
- Provides H-L spreads for comparison with FOMC results
- Required for portfolio performance tables

**Outputs:**
- `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/portfolio_ret_ew.csv`
- `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/portfolio_ret_vw.csv`
- Other performance metrics files

**How to run:**
```bash
# On Laguna (can run concurrently with Task 1, or after)
cd ~/cnnthesis

# Submit batch job
sbatch slurm/run_cnn_portfolios.sh

# Monitor
squeue -u $USER
tail -f logs/cnn_portfolios_*.out
```

**Expected duration:** 30-60 minutes  
**Resource requirements:** 64GB RAM, 4 CPUs

**What to check after completion:**
```bash
# Check output directory
ls -lh ~/cnnthesis/WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/
```

---

### Task 3: Run Additional Analysis Scripts 📊

After Tasks 1 and 2 complete, you can run analysis scripts to generate tables and figures.

#### 3a. Regression Analysis (Optional)

**What it does:**
Runs regressions of CNN predictions on stock characteristics to test incremental value.

**Script:** `trend_code_submit/Analysis/regression_tables.py`

**How to run:**
```bash
cd ~/cnnthesis
PYTHONPATH="$(pwd)/trend_code_submit" ~/cnnthesis/cnn_env/bin/python -c "
from Analysis import regression_tables as rt
import pandas as pd

# Load stock characteristics data
df_is = rt.load_cnn_and_monthly_stock_char('is')
df_oos = rt.load_cnn_and_monthly_stock_char('oos')

print('IS shape:', df_is.shape)
print('OOS shape:', df_oos.shape)
print('Columns:', df_is.columns.tolist())

# Run regression (uncomment to actually run)
# res = rt.cnn_and_ret_and_stock_char_regression(pw=5, ws_list=[20])
# print(res)
"
```

#### 3b. Correlation Analysis (Optional)

**What it does:**
Computes correlations between CNN predictions and stock characteristics.

**Script:** `trend_code_submit/Analysis/analysis_lib.py`

**How to run:**
```bash
cd ~/cnnthesis
PYTHONPATH="$(pwd)/trend_code_submit" ~/cnnthesis/cnn_env/bin/python -c "
from Analysis import analysis_lib as al
import pandas as pd

# Compute correlations
corr = al.corr_between_cnn_pred_and_stock_chars()
print(corr)
"
```

---

### Task 4: Copy Results Back to Local Machine 💾

After all analyses complete, copy results back to your local machine for thesis writing.

**What to copy:**
```bash
# From local machine, create a backup directory
mkdir -p ~/Desktop/Thesis_Results

# Copy FOMC results
scp -r laguna:~/cnnthesis/CACHE_DIR/fomc/* ~/Desktop/Thesis_Results/FOMC/

# Copy portfolio results
scp -r laguna:~/cnnthesis/WORK_SPACE/new_model_res/portfolio/cnn_weekly/ ~/Desktop/Thesis_Results/Portfolios/

# Copy stock characteristics
scp laguna:~/cnnthesis/CACHE_DIR/cnn_and_monthly_stock_char_*.parquet ~/Desktop/Thesis_Results/

# Copy prediction files
scp laguna:~/cnnthesis/CACHE_DIR/weekly_prediction_with_rets.csv ~/Desktop/Thesis_Results/

# Copy evaluation results
scp laguna:~/cnnthesis/CACHE_DIR/horizon_eval.csv ~/Desktop/Thesis_Results/
```

---

## 📊 Understanding Your Data Pipeline

### Input Data
1. **Raw Stock Data**: `us_920101-241231.csv.gz` (CRSP daily)
2. **FOMC Schedule**: `FOMC_Dates_1936.csv` (316 meetings)

### Processed Data
1. **Daily Panel**: `us_ret.feather` (3.9GB, 63M rows)
2. **Period Returns**: `us_week_ret.pq`, `us_month_ret.pq`, etc.
3. **CNN Predictions**: `weekly_prediction_with_rets.csv` (8.9M rows)

### Analysis Outputs
1. **FOMC Analysis**: Event-window returns and decile performance
2. **Stock Characteristics**: Monthly characteristics + CNN predictions
3. **Portfolio Returns**: Decile portfolios with performance metrics

---

## 🚨 Troubleshooting

### If stock characteristics script fails:

**Error:** "FileNotFoundError: us_week_ret.pq"
```bash
# Check if period returns exist
ls -lh ~/cnnthesis/CACHE_DIR/us_*_ret.pq

# If missing, regenerate them
cd ~/cnnthesis
PYTHONPATH="$(pwd)/trend_code_submit" ~/cnnthesis/cnn_env/bin/python make_us_period_returns.py
```

**Error:** "Out of memory"
```bash
# Edit slurm/run_stock_chars.sh to increase memory
# Change --mem=128G to --mem=192G or higher
```

**Error:** "No module named 'pandas'"
```bash
# Activate conda environment properly
source ~/cnnthesis/cnn_env/bin/activate
pip install pandas numpy pyarrow
```

### If portfolio script fails:

**Error:** "Missing weekly_prediction_with_rets.csv"
```bash
# Check if file exists
ls -lh ~/cnnthesis/CACHE_DIR/weekly_prediction_with_rets.csv

# If missing, regenerate (this should already be done)
cd ~/cnnthesis
PYTHONPATH="$(pwd)/trend_code_submit" ~/cnnthesis/cnn_env/bin/python make_prediction_with_rets.py
```

---

## 📝 Summary Checklist

- [x] Model trained (5 ensembles)
- [x] Predictions generated
- [x] Period returns regenerated
- [x] FOMC schedule updated to 2024
- [x] FOMC windows built
- [ ] **FOMC analysis complete** (currently running)
- [ ] Stock characteristics + CNN generated
- [ ] CNN portfolio returns generated
- [ ] Results copied to local machine
- [ ] Analysis tables generated (optional)
- [ ] Thesis data inventory updated

---

## 🎯 Priority Order

1. **Wait for FOMC analysis** to complete (already running)
2. **Run stock characteristics** generation (Task 1) - 2-3 hours
3. **Run portfolio generation** (Task 2) - 30-60 min (can run concurrently)
4. **Copy results** back to local (Task 4)
5. **Run optional analysis** (Task 3) if needed

---

## 📞 Next Steps

After your current FOMC batch job completes:

1. Check if it succeeded:
   ```bash
   ls -lh ~/cnnthesis/CACHE_DIR/fomc/
   cat ~/cnnthesis/logs/fomc_*.out
   ```

2. Submit the next batch job:
   ```bash
   sbatch slurm/run_stock_chars.sh
   ```

3. Optionally submit portfolio job concurrently:
   ```bash
   sbatch slurm/run_cnn_portfolios.sh
   ```

4. Monitor both:
   ```bash
   watch -n 30 'squeue -u $USER'
   ```

Good luck with your thesis! 🎓



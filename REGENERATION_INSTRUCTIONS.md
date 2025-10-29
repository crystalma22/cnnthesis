# Regeneration Instructions for Stock Characteristics + CNN Portfolios

## Overview

I've created scripts to regenerate:
1. **Stock Characteristics + CNN predictions** (`cnn_and_monthly_stock_char_is.parquet` and `cnn_and_monthly_stock_char_oos.parquet`)
2. **CNN Portfolio Returns** (decile portfolios for I20/R5 model)

## Scripts Created

### 1. `generate_stock_chars_with_cnn.py`
- Combines monthly stock characteristics (MOM, STR, TREND, etc.) with CNN predictions
- Aligns weekly CNN predictions to month-ends using merge_asof
- Adds future returns for regression analysis
- Splits into in-sample (1993-2000) and out-of-sample (2001-2024)

### 2. `generate_cnn_portfolios.py`
- Generates decile portfolios (EW and VW) based on CNN up-probabilities
- Creates portfolio performance metrics
- Outputs to `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/`

## Running on Laguna

**The local environment has dependency issues (pandas/dateutil). These scripts should be run on Laguna where the conda environment is properly configured.**

### Step 1: Copy scripts to Laguna

```bash
# From your local machine
scp generate_stock_chars_with_cnn.py laguna:~/cnnthesis/
scp generate_cnn_portfolios.py laguna:~/cnnthesis/
scp slurm/run_stock_chars.sh laguna:~/cnnthesis/slurm/
scp slurm/run_cnn_portfolios.sh laguna:~/cnnthesis/slurm/
```

### Step 2: Run Stock Characteristics Generation

```bash
# SSH to Laguna
ssh laguna

# Submit batch job
cd ~/cnnthesis
sbatch slurm/run_stock_chars.sh

# Monitor
squeue -u $USER
tail -f logs/stock_chars_*.out
```

**Expected output:**
- `CACHE_DIR/cnn_and_monthly_stock_char_is.parquet`
- `CACHE_DIR/cnn_and_monthly_stock_char_oos.parquet`

**Expected time:** 2-3 hours (needs to process all daily data and align to month-ends)

### Step 3: Run CNN Portfolio Generation

```bash
# On Laguna, after stock characteristics complete
sbatch slurm/run_cnn_portfolios.sh

# Monitor
squeue -u $USER
tail -f logs/cnn_portfolios_*.out
```

**Expected output:**
- Portfolio CSV files in `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/`
- Decile portfolios (0-9) for EW and VW
- High-Low spreads
- Performance metrics

**Expected time:** 30-60 minutes

## Troubleshooting

### If stock characteristics script fails:

1. **Check period returns file exists:**
   ```bash
   ls -lh ~/cnnthesis/CACHE_DIR/us_week_ret.pq
   ```
   If missing, run `make_us_period_returns.py` first (you mentioned you just regenerated these, so should be OK).

2. **Check CNN predictions exist:**
   ```bash
   ls -lh ~/cnnthesis/CACHE_DIR/weekly_prediction_with_rets.csv
   ```
   Should be ~322 MB with 8.9M rows.

3. **Check processed US data:**
   ```bash
   ls -lh ~/cnnthesis/WORK_SPACE/data/processed_data/us_ret.feather
   ```
   Should be ~3.9 GB.

### If portfolio generation fails:

1. **Check weekly predictions file:**
   ```bash
   ls -lh ~/cnnthesis/CACHE_DIR/weekly_prediction_with_rets.csv
   ```

2. **Check period returns:**
   ```bash
   ls -lh ~/cnnthesis/CACHE_DIR/us_week_ret.pq
   ```

## Output Files Summary

### Stock Characteristics + CNN:
- **File:** `CACHE_DIR/cnn_and_monthly_stock_char_is.parquet`
  - In-sample (1993-2000)
  - Columns: Date, StockID, MarketCap, I20/R5, MOM, STR, TREND, Volatility, etc., Future_Ret_5d
  - Expected size: ~5-10 MB

- **File:** `CACHE_DIR/cnn_and_monthly_stock_char_oos.parquet`
  - Out-of-sample (2001-2024)
  - Same columns as IS
  - Expected size: ~10-20 MB

### CNN Portfolios:
- **Directory:** `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/`
- **Files:**
  - `portfolio_ret_ew.csv` - Equal-weight decile returns
  - `portfolio_ret_vw.csv` - Value-weight decile returns
  - Other performance metrics files

## Next Steps

After successful generation:
1. Copy results back to local machine if needed
2. Update `THESIS_DATA_INVENTORY.md` with new file info
3. Run analysis scripts that depend on these files:
   - `trend_code_submit/Analysis/regression_tables.py` (for stock char regressions)
   - Portfolio performance analysis


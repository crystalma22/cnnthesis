# CNN Thesis - Stock Prediction Analysis

This repository contains code and analysis for a thesis on using Convolutional Neural Networks (CNN) to predict stock returns based on technical patterns.

## Model Specification

- **Architecture:** 2D Convolutional Neural Network
- **Input:** 20-day OHLC candlestick charts (I20)
- **Output:** Probability of positive return in next 5 days (R5)
- **Ensemble:** 5 independently trained models
- **Training:** 1992-2000 (in-sample)
- **Testing:** 2001-2024 (out-of-sample)

## Repository Structure

### `/docs` - Documentation
- **COMPLETE_TODO_AND_INSTRUCTIONS.md** - Complete instructions for running all analysis
- **THESIS_DATA_INVENTORY.md** - Inventory of all generated data files
- **FOMC_METHODOLOGY.md** - Methodology for FOMC event study analysis
- **REGENERATION_INSTRUCTIONS.md** - Instructions for regenerating data

### `/thesis_scripts` - Data Generation Scripts
- `generate_stock_chars_with_cnn.py` - Generate stock characteristics + CNN predictions
- `generate_cnn_portfolios.py` - Generate decile portfolio returns
- `make_prediction_with_rets.py` - Generate weekly predictions with realized returns
- `make_us_period_returns.py` - Generate period returns (week/month/quarter)
- `make_spy_files.py` - Generate SPY benchmark returns
- `scrape_fomc_calendar.py` - Scrape FOMC calendar from Federal Reserve
- `QUICK_START_SCRIPT.sh` - Interactive script to submit batch jobs on Laguna

### `/slurm` - SLURM Batch Job Scripts
- `run_fomc_analysis.sh` - Full FOMC event study pipeline
- `run_stock_chars.sh` - Generate stock characteristics
- `run_cnn_portfolios.sh` - Generate CNN portfolios
- `run_member.sh` - Train individual ensemble member
- `run_portfolios.sh` - Generate portfolios for all models

### `/trend_code_submit` - Core Analysis Code
- `/Analysis` - Analysis functions and FOMC pipeline
- `/Data` - Data loading and preprocessing
- `/Experiments` - Model training and evaluation
- `/Model` - CNN model architecture
- `/Portfolio` - Portfolio construction and performance

### `/CACHE_DIR` - Generated Data Files
- Model predictions, portfolio returns, evaluation results
- FOMC event study data
- Stock characteristics

### `/WORK_SPACE` - Training Results
- Model checkpoints
- Training logs
- Portfolio output files

## Quick Start

### 1. Setup Environment
```bash
# Create conda environment
conda env create -f trend_code_submit/cnn_env.yml -p ./cnn_env

# Activate environment
source cnn_env/bin/activate  # Linux/Mac
```

### 2. Train Model (on Laguna)
```bash
# Train all 5 ensemble members
for i in {0..4}; do
  sbatch --export=ENSEMBLE_ID=$i slurm/run_member.sh
done
```

### 3. Generate Predictions
```bash
PYTHONPATH="$(pwd)/trend_code_submit" python thesis_scripts/make_prediction_with_rets.py
```

### 4. Run Analysis
```bash
# On Laguna, use the quick start script
bash thesis_scripts/QUICK_START_SCRIPT.sh

# Or submit individual jobs
sbatch slurm/run_fomc_analysis.sh
sbatch slurm/run_stock_chars.sh
sbatch slurm/run_cnn_portfolios.sh
```

## Documentation

See `/docs` folder for complete documentation:
- **Start here:** `docs/COMPLETE_TODO_AND_INSTRUCTIONS.md`
- **Data inventory:** `docs/THESIS_DATA_INVENTORY.md`
- **FOMC methodology:** `docs/FOMC_METHODOLOGY.md`

## Key Files

- `FOMC_Dates_1936.csv` - FOMC meeting schedule (1936-2024)
- `trend_code_submit/cnn_env.yml` - Conda environment specification
- `CACHE_DIR/weekly_prediction_with_rets.csv` - Main prediction file (8.9M rows)

## Citation

If you use this code, please cite the original paper this is based on.

## License

[Your license here]


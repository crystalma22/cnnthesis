# Slurm Job Scripts

This folder contains ready-to-use Slurm scripts for model training, FOMC analysis, and data generation.

## Model Training Scripts

- `run_member.sh` (array job): trains one ensemble member per array task (0–4).
  Submitting the array launches 5 independent jobs; each writes its own checkpoint.
- `run_portfolios.sh`: runs OOS prediction + portfolios only (re-uses checkpoints).

## FOMC Analysis Scripts

- `run_fomc_analysis.sh`: runs the complete FOMC pipeline:
  - Ingests FOMC schedule (from `FOMC_Dates_1936.csv`)
  - Builds per-stock FOMC window returns
  - Aligns CNN predictions to FOMC events
  - Generates decile performance and summary statistics
  - Outputs: `fomc_decile_performance.csv`, `fomc_summary.csv`, `fomc_summary.png`

- `run_fomc_event_study.sh`: runs event study portfolio analysis:
  - Compares CNN H-L performance across different FOMC windows
  - Computes decile spreads for pre-announcement, reaction, intermediate, and non-event windows
  - Outputs: `event_study_portfolio_table.csv` (Return, Vol, SR, Turnover by window)

- `run_fomc_horizon_conditional.sh`: runs conditional horizon evaluation:
  - Compares 1-day, 3-day, 10-day H-L spreads separately for FOMC vs. non-FOMC days
  - Generates bar chart visualization
  - Outputs: `horizon_eval_conditional.csv`, `horizon_eval_conditional.png`

## Data Generation Scripts

- `run_regenerate_period_returns.sh`: regenerates period returns in parquet format:
  - Regenerates `us_week_ret.pq`, `us_month_ret.pq`, `us_quarter_ret.pq` with 2024 data
  - Uses `processed_US_data()` to compute period-end returns
  - Required for `make_prediction_with_rets.py` and other analyses

## Usage (from repo root: `~/cnnthesis`)

### Model Training Workflow

```
# 1) Submit the ensemble as an array (5 members: 0..4)
sbatch slurm/run_member.sh

# Monitor
squeue -u $USER

# 2) After all members finish, run portfolios
echo "Make sure weekly OOS images (2001–2024) exist before this step"
sbatch slurm/run_portfolios.sh

# Logs land in ./logs/
ls -l logs/
```

### FOMC Analysis Workflow

```
# 1) Run main FOMC pipeline (generates schedule, windows, decile performance)
sbatch slurm/run_fomc_analysis.sh

# 2) After pipeline completes, run additional analyses:
sbatch slurm/run_fomc_event_study.sh
sbatch slurm/run_fomc_horizon_conditional.sh
```

### Data Regeneration

```
# Regenerate period returns with updated data
sbatch slurm/run_regenerate_period_returns.sh
```

## Dependencies

- All scripts expect your project at `~/cnnthesis` with conda env at `./cnn_env`.
- FOMC scripts require `weekly_prediction_with_rets.csv` (from `make_prediction_with_rets.py`).
- Period returns script requires `processed_US_data()` to be available.

## Notes

- Adjust the `#SBATCH --partition=` line in the scripts to match your queue (compute/gpu).
- Logs are written to `./logs/` directory.
- FOMC event study and horizon conditional scripts depend on the main FOMC pipeline completing first.
- Portfolios only run after training finishes and checkpoints exist.


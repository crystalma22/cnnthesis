#!/bin/bash
#SBATCH --job-name=fomc_horizon_cond
#SBATCH --output=logs/fomc_horizon_cond_%j.out
#SBATCH --error=logs/fomc_horizon_cond_%j.err
#SBATCH --time=02:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --partition=compute

# FOMC Horizon Evaluation: Conditional on Event vs Non-Event Days
# Compares CNN performance during FOMC periods vs normal periods
# at different horizons (1d, 3d, 10d)

echo "Job started at $(date)"
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"

# Navigate to project directory
cd ~/cnnthesis || exit 1

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate conda environment
source ~/cnnthesis/cnn_env/bin/activate

# Set PYTHONPATH to include trend_code_submit
export PYTHONPATH="$(pwd)/trend_code_submit:$PYTHONPATH"

# Run horizon evaluation conditional on FOMC
echo "Running horizon evaluation conditional on FOMC events..."
python trend_code_submit/Analysis/fomc/horizon_eval_conditional.py

# Check if outputs were created
if [ -f "CACHE_DIR/fomc/horizon_eval_conditional.csv" ]; then
    echo "Success! Conditional horizon evaluation completed."
    echo "Output files:"
    ls -lh CACHE_DIR/fomc/horizon_eval_conditional.csv
    ls -lh CACHE_DIR/fomc/horizon_eval_conditional.png
    
    echo ""
    echo "Results preview:"
    head -20 CACHE_DIR/fomc/horizon_eval_conditional.csv
else
    echo "ERROR: Output files not found!"
    exit 1
fi

echo "Job completed at $(date)"

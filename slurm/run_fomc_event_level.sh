#!/bin/bash
#SBATCH --job-name=fomc_event_level
#SBATCH --output=logs/fomc_event_level_%j.out
#SBATCH --error=logs/fomc_event_level_%j.err
#SBATCH --time=02:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --partition=compute

# FOMC Event-Level Comparison
# Proper statistical methodology with event-level aggregation

echo "Job started at $(date)"
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"

# Navigate to project directory
cd ~/cnnthesis || exit 1

# Create logs directory if it doesn't exist
mkdir -p logs

# Set PYTHONPATH to include trend_code_submit
export PYTHONPATH="$(pwd)/trend_code_submit:$PYTHONPATH"

# Run event-level comparison using conda env python directly
echo "Running event-level FOMC vs non-FOMC comparison..."
~/cnnthesis/cnn_env/bin/python trend_code_submit/Analysis/fomc/event_level_comparison.py

# Check if outputs were created
if [ -f "CACHE_DIR/fomc/event_level_comparison.csv" ]; then
    echo "Success! Event-level comparison completed."
    echo "Output files:"
    ls -lh CACHE_DIR/fomc/event_level_*.csv
    ls -lh CACHE_DIR/fomc/event_level_*.png 2>/dev/null
else
    echo "ERROR: Output files not found!"
    exit 1
fi

echo "Job completed at $(date)"


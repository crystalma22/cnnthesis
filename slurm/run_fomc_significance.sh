#!/bin/bash
#SBATCH --job-name=fomc_significance
#SBATCH --output=logs/fomc_significance_%j.out
#SBATCH --error=logs/fomc_significance_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --partition=compute

# FOMC Statistical Significance Testing
# Computes t-statistics and p-values for FOMC event study results

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

# Run statistical significance tests
echo "Running statistical significance tests..."
python trend_code_submit/Analysis/fomc/statistical_significance.py

# Check if outputs were created
if [ -f "CACHE_DIR/fomc/fomc_significance_tests.csv" ]; then
    echo "Success! Significance tests completed."
    echo "Output files:"
    ls -lh CACHE_DIR/fomc/fomc_significance_tests.csv
    if [ -f "CACHE_DIR/fomc/fomc_comparison_tests.csv" ]; then
        ls -lh CACHE_DIR/fomc/fomc_comparison_tests.csv
    fi
else
    echo "ERROR: Output files not found!"
    exit 1
fi

echo "Job completed at $(date)"


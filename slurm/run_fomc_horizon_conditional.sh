#!/bin/bash
#SBATCH --job-name=fomc_horizon_cond
#SBATCH --partition=compute
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4
#SBATCH --time=4:00:00
#SBATCH --output=logs/fomc_horizon_cond_%j.out
#SBATCH --error=logs/fomc_horizon_cond_%j.err

set -euo pipefail

mkdir -p logs

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

echo "=========================================="
echo "Running FOMC Conditional Horizon Evaluation"
echo "Time: $(date)"
echo "=========================================="

# Run horizon eval conditional script
~/cnnthesis/cnn_env/bin/python trend_code_submit/Analysis/fomc/horizon_eval_conditional.py

echo "=========================================="
echo "Horizon Conditional Evaluation Complete"
echo "Time: $(date)"
echo "=========================================="

# Show output files
echo ""
echo "Generated files:"
if [ -f CACHE_DIR/fomc/horizon_eval_conditional.csv ]; then
    ls -lh CACHE_DIR/fomc/horizon_eval_conditional.csv
    echo ""
    echo "Results:"
    cat CACHE_DIR/fomc/horizon_eval_conditional.csv
fi
if [ -f CACHE_DIR/fomc/horizon_eval_conditional.png ]; then
    ls -lh CACHE_DIR/fomc/horizon_eval_conditional.png
fi


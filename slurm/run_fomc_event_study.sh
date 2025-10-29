#!/bin/bash
#SBATCH --job-name=fomc_event_study
#SBATCH --partition=compute
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4
#SBATCH --time=4:00:00
#SBATCH --output=logs/fomc_event_study_%j.out
#SBATCH --error=logs/fomc_event_study_%j.err

set -euo pipefail

mkdir -p logs

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

echo "=========================================="
echo "Running FOMC Event Study Portfolios"
echo "Time: $(date)"
echo "=========================================="

# Run event study portfolios script
~/cnnthesis/cnn_env/bin/python trend_code_submit/Analysis/fomc/event_study_portfolios.py

echo "=========================================="
echo "Event Study Complete"
echo "Time: $(date)"
echo "=========================================="

# Show output file
if [ -f CACHE_DIR/fomc/event_study_portfolio_table.csv ]; then
    echo ""
    echo "Generated file:"
    ls -lh CACHE_DIR/fomc/event_study_portfolio_table.csv
    echo ""
    echo "Preview:"
    head -20 CACHE_DIR/fomc/event_study_portfolio_table.csv
fi


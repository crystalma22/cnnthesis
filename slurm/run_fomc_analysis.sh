#!/bin/bash
#SBATCH --job-name=fomc_analysis
#SBATCH --partition=compute
#SBATCH --mem=128G
#SBATCH --cpus-per-task=8
#SBATCH --time=6:00:00
#SBATCH --output=logs/fomc_%j.out
#SBATCH --error=logs/fomc_%j.err

set -euo pipefail

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

echo "=========================================="
echo "Starting FOMC Pipeline"
echo "Time: $(date)"
echo "=========================================="

# Run the full FOMC pipeline using conda env python directly
~/cnnthesis/cnn_env/bin/python trend_code_submit/Analysis/fomc/run_fomc_pipeline.py \
    --schedule-path FOMC_Dates_1936.csv

echo "=========================================="
echo "FOMC Pipeline Complete"
echo "Time: $(date)"
echo "=========================================="

# Show output files
echo "Generated files:"
ls -lh CACHE_DIR/fomc/

# Show summary if it exists
if [ -f CACHE_DIR/fomc/fomc_summary.csv ]; then
    echo ""
    echo "FOMC Summary:"
    cat CACHE_DIR/fomc/fomc_summary.csv
fi

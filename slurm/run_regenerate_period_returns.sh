#!/bin/bash
#SBATCH --job-name=regenerate_period_returns
#SBATCH --partition=compute
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --time=2:00:00
#SBATCH --output=logs/regenerate_period_ret_%j.out
#SBATCH --error=logs/regenerate_period_ret_%j.err

set -euo pipefail

mkdir -p logs

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

echo "=========================================="
echo "Regenerating Period Returns (Week/Month/Quarter)"
echo "Time: $(date)"
echo "=========================================="

# Run make_us_period_returns.py
~/cnnthesis/cnn_env/bin/python make_us_period_returns.py

echo "=========================================="
echo "Period Returns Regeneration Complete"
echo "Time: $(date)"
echo "=========================================="

# Show output files
echo ""
echo "Generated files:"
ls -lh CACHE_DIR/us_*_ret.pq 2>/dev/null || echo "No period return files found"


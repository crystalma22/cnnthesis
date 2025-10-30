#!/bin/bash
#SBATCH --job-name=cnn_portfolios
#SBATCH --partition=compute
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --time=2:00:00
#SBATCH --output=logs/cnn_portfolios_%j.out
#SBATCH --error=logs/cnn_portfolios_%j.err

set -euo pipefail

mkdir -p logs

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

echo "=========================================="
echo "Generating CNN Portfolio Returns"
echo "Time: $(date)"
echo "=========================================="

# Run generate_cnn_portfolios.py
~/cnnthesis/cnn_env/bin/python generate_cnn_portfolios.py

echo "=========================================="
echo "Portfolio Generation Complete"
echo "Time: $(date)"
echo "=========================================="

# Show output files
echo ""
echo "Generated files:"
if [ -d "WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P" ]; then
    ls -lh WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/
fi

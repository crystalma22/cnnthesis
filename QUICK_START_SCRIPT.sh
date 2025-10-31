#!/bin/bash
# Quick start script for running all batch jobs on Laguna
# Usage: Copy this to Laguna and run: bash QUICK_START_SCRIPT.sh

echo "=========================================="
echo "CNN Thesis Data Generation Pipeline"
echo "=========================================="
echo ""
echo "Current status:"
squeue -u $USER
echo ""

cd ~/cnnthesis

echo "Checking required files..."
required_files=(
    "CACHE_DIR/weekly_prediction_with_rets.csv"
    "CACHE_DIR/fomc/fomc_window_returns.csv"
    "CACHE_DIR/us_week_ret.pq"
    "WORK_SPACE/data/processed_data/us_ret.feather"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo "  ✓ $file ($size)"
    else
        echo "  ✗ MISSING: $file"
        exit 1
    fi
done

echo ""
echo "=========================================="
echo "Job Status"
echo "=========================================="

# Check if FOMC analysis is running
fomc_jobs=$(squeue -u $USER | grep fomc | wc -l)
if [ "$fomc_jobs" -gt 0 ]; then
    echo "✓ FOMC analysis running"
else
    echo "✗ FOMC analysis not running"
    read -p "Submit FOMC analysis job? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sbatch slurm/run_fomc_analysis.sh
        echo "  Submitted FOMC job"
    fi
fi

# Check if stock chars is running
stock_chars_jobs=$(squeue -u $USER | grep stock_chars | wc -l)
if [ "$stock_chars_jobs" -gt 0 ]; then
    echo "✓ Stock characteristics running"
else
    echo "✗ Stock characteristics not running"
    if [ ! -f "CACHE_DIR/cnn_and_monthly_stock_char_is.parquet" ]; then
        read -p "Submit stock characteristics job? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sbatch slurm/run_stock_chars.sh
            echo "  Submitted stock characteristics job"
        fi
    else
        echo "  ✓ Stock characteristics already generated"
    fi
fi

# Check if portfolios are running
portfolio_jobs=$(squeue -u $USER | grep cnn_portfolios | wc -l)
if [ "$portfolio_jobs" -gt 0 ]; then
    echo "✓ CNN portfolios running"
else
    echo "✗ CNN portfolios not running"
    portfolio_dir="WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P"
    if [ ! -d "$portfolio_dir" ] || [ -z "$(ls -A $portfolio_dir 2>/dev/null)" ]; then
        read -p "Submit CNN portfolio job? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sbatch slurm/run_cnn_portfolios.sh
            echo "  Submitted CNN portfolio job"
        fi
    else
        echo "  ✓ CNN portfolios already generated"
    fi
fi

echo ""
echo "=========================================="
echo "Monitoring Commands"
echo "=========================================="
echo "Watch job queue:     watch -n 30 'squeue -u \$USER'"
echo "Watch FOMC logs:     tail -f logs/fomc_*.out"
echo "Watch stock chars:   tail -f logs/stock_chars_*.out"
echo "Watch portfolios:    tail -f logs/cnn_portfolios_*.out"
echo ""
echo "Check results:"
echo "  FOMC: ls -lh CACHE_DIR/fomc/"
echo "  Stock chars: ls -lh CACHE_DIR/cnn_and_monthly_stock_char_*.parquet"
echo "  Portfolios: ls -lh WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/"
echo ""



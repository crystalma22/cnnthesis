#!/bin/bash
# Local runner for FOMC statistical significance tests
# Run this after FOMC analysis is complete

echo "Running FOMC Statistical Significance Tests..."
echo "==============================================="

# Navigate to project directory
cd "$(dirname "$0")" || exit 1

# Activate conda environment
source cnn_env/bin/activate

# Set PYTHONPATH
export PYTHONPATH="$(pwd)/trend_code_submit:$PYTHONPATH"

# Run tests
python trend_code_submit/Analysis/fomc/statistical_significance.py

# Display results
echo ""
echo "==============================================="
echo "Results saved to:"
echo "  CACHE_DIR/fomc/fomc_significance_tests.csv"
echo "  CACHE_DIR/fomc/fomc_comparison_tests.csv"
echo "==============================================="

# Optionally display results
if [ -f "CACHE_DIR/fomc/fomc_significance_tests.csv" ]; then
    echo ""
    echo "T-test Results (first few rows):"
    head -n 10 CACHE_DIR/fomc/fomc_significance_tests.csv
fi




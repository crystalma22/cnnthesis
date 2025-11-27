#!/bin/bash
#SBATCH --job-name=table5a_announcement
#SBATCH --output=logs/table5a_announcement_%j.out
#SBATCH --error=logs/table5a_announcement_%j.err
#SBATCH --time=02:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --partition=compute

# Compute Table 5A: Announcement-Day Returns
# This computes H-L spreads for announcement-day returns (Day -1 close → Day 0 close)
# for all FOMC events in 2001-2024

echo "Job started at $(date)"
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"

# Navigate to project directory
cd ~/cnnthesis || exit 1

# Create logs directory if it doesn't exist
mkdir -p logs

# Set PYTHONPATH to include trend_code_submit
export PYTHONPATH="$(pwd)/trend_code_submit:$PYTHONPATH"

# Run the computation script
echo "Running compute_table5a_announcement_day.py..."
~/cnnthesis/cnn_env/bin/python compute_table5a_announcement_day.py

# Check if output was created
if [ -f "CACHE_DIR/fomc/table5a_announcement_day_results.csv" ]; then
    echo ""
    echo "✅ Success! Table 5A results generated."
    echo "Output file: CACHE_DIR/fomc/table5a_announcement_day_results.csv"
    echo ""
    echo "File size and line count:"
    ls -lh CACHE_DIR/fomc/table5a_announcement_day_results.csv
    wc -l CACHE_DIR/fomc/table5a_announcement_day_results.csv
    echo ""
    echo "First few lines:"
    head -5 CACHE_DIR/fomc/table5a_announcement_day_results.csv
else
    echo "❌ ERROR: Output file not found!"
    exit 1
fi

echo ""
echo "Job completed at $(date)"


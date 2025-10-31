#!/bin/bash
# Copy new FOMC analysis scripts to Laguna
# Run this from your local machine

echo "Copying new FOMC analysis files to Laguna..."

# Set the local directory (where you are now)
LOCAL_DIR="/Users/crystallion22/Desktop/Thesis Materials/cnnthesis"

# Set the remote directory on Laguna
REMOTE_DIR="~/cnnthesis"

# Copy new Python scripts
echo "1. Copying statistical_significance.py..."
scp "$LOCAL_DIR/trend_code_submit/Analysis/fomc/statistical_significance.py" \
    laguna:$REMOTE_DIR/trend_code_submit/Analysis/fomc/

echo "2. Copying create_thesis_figures.py..."
scp "$LOCAL_DIR/trend_code_submit/Analysis/fomc/create_thesis_figures.py" \
    laguna:$REMOTE_DIR/trend_code_submit/Analysis/fomc/

# Copy new SLURM scripts
echo "3. Copying SLURM scripts..."
scp "$LOCAL_DIR/slurm/run_fomc_significance.sh" \
    laguna:$REMOTE_DIR/slurm/

scp "$LOCAL_DIR/slurm/run_fomc_horizon_conditional.sh" \
    laguna:$REMOTE_DIR/slurm/

# Copy documentation (optional but helpful)
echo "4. Copying documentation..."
scp "$LOCAL_DIR/QUICK_ANSWER.md" \
    laguna:$REMOTE_DIR/

scp "$LOCAL_DIR/CONTRIBUTION_2_ACTION_PLAN.md" \
    laguna:$REMOTE_DIR/

scp "$LOCAL_DIR/COMPLETE_STATISTICS_AND_VISUALIZATION_PACKAGE.md" \
    laguna:$REMOTE_DIR/

scp "$LOCAL_DIR/docs/STATISTICAL_SIGNIFICANCE_GUIDE.md" \
    laguna:$REMOTE_DIR/docs/

scp "$LOCAL_DIR/docs/FOMC_ANALYSIS_OVERVIEW.md" \
    laguna:$REMOTE_DIR/docs/

scp "$LOCAL_DIR/docs/CONTRIBUTION_2_CHECKLIST.md" \
    laguna:$REMOTE_DIR/docs/

# Make scripts executable
echo "5. Making scripts executable on Laguna..."
ssh laguna "chmod +x ~/cnnthesis/slurm/run_fomc_significance.sh"
ssh laguna "chmod +x ~/cnnthesis/slurm/run_fomc_horizon_conditional.sh"

echo ""
echo "✅ All files copied to Laguna!"
echo ""
echo "Next steps:"
echo "1. ssh laguna"
echo "2. cd ~/cnnthesis"
echo "3. sbatch slurm/run_fomc_horizon_conditional.sh"
echo "4. Wait ~2 hours, then: sbatch slurm/run_fomc_significance.sh"
echo ""


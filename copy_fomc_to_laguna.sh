#!/bin/bash
# Script to copy FOMC-related files to Laguna
# Usage: ./copy_fomc_to_laguna.sh [laguna_hostname]

LAGUNA="${1:-laguna1}"  # Default to laguna1 if not provided
# Username - adjust if different. Your prompt showed CMa26@cmc.edu
REMOTE_USER="${2:-CMa26}"  # Change this if your Laguna username is different
REMOTE_DIR="~/cnnthesis"

echo "Copying FOMC files to ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}"
echo ""

# Copy SLURM scripts
echo "Copying SLURM scripts..."
scp slurm/run_fomc_event_study.sh ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}/slurm/
scp slurm/run_fomc_horizon_conditional.sh ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}/slurm/
scp slurm/run_regenerate_period_returns.sh ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}/slurm/
scp slurm/README.md ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}/slurm/

# Copy Python scripts (if they were modified/created)
echo "Copying Python analysis scripts..."
scp trend_code_submit/Analysis/fomc/event_study_portfolios.py ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}/trend_code_submit/Analysis/fomc/
scp trend_code_submit/Analysis/fomc/horizon_eval_conditional.py ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}/trend_code_submit/Analysis/fomc/

# Copy make_us_period_returns.py (used by run_regenerate_period_returns.sh)
echo "Copying make_us_period_returns.py..."
scp make_us_period_returns.py ${REMOTE_USER}@${LAGUNA}:${REMOTE_DIR}/

echo ""
echo "Done! Files copied to Laguna."
echo ""
echo "Next steps on Laguna:"
echo "  1. cd ~/cnnthesis"
echo "  2. chmod +x slurm/run_fomc*.sh slurm/run_regenerate*.sh"
echo "  3. sbatch slurm/run_fomc_event_study.sh"
echo "  4. sbatch slurm/run_fomc_horizon_conditional.sh"
echo "  5. sbatch slurm/run_regenerate_period_returns.sh"


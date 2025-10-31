#!/bin/bash
#SBATCH --job-name=fomc_align
#SBATCH --partition=compute
#SBATCH --mem=128G
#SBATCH --cpus-per-task=8
#SBATCH --time=24:00:00
#SBATCH --output=logs/fomc_align_%j.out
#SBATCH --error=logs/fomc_align_%j.err

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

echo "Running align_predictions_and_score.py..."
~/cnnthesis/cnn_env/bin/python -u trend_code_submit/Analysis/fomc/align_predictions_and_score.py

echo "Running build_summary..."
~/cnnthesis/cnn_env/bin/python -c "
import os, sys, pandas as pd
from Data import dgp_config as dcf

cache_dir = os.path.join(str(dcf.CACHE_DIR), 'fomc')
perf_path = os.path.join(cache_dir, 'fomc_decile_performance.csv')

if os.path.exists(perf_path):
    df = pd.read_csv(perf_path)
    # Use correct column names from align_predictions_and_score.py output
    summary = pd.DataFrame({
        'EW_H-L_pre': [df['pre_ew_H-L'].mean()],
        'EW_H-L_react': [df['react_ew_H-L'].mean()],
        'EW_H-L_intermediate': [df['inter_ew_H-L'].mean()],
        'VW_H-L_pre': [df['pre_vw_H-L'].mean()],
        'VW_H-L_react': [df['react_vw_H-L'].mean()],
        'VW_H-L_intermediate': [df['inter_vw_H-L'].mean()]
    })
    summary.to_csv(os.path.join(cache_dir, 'fomc_summary.csv'), index=False)
    print('Summary saved to fomc_summary.csv')
    print(summary)
else:
    print('Missing:', perf_path)
"



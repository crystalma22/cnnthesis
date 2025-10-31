#!/bin/bash
#SBATCH --job-name=cnn_weekly_member
#SBATCH --partition=gpu              # TODO: adjust to your GPU partition
#SBATCH --gres=gpu:1
#SBATCH --mem=128G
#SBATCH --time=7-00:00:00            # Increased to 7 days for full training
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --array=0-4                  # one task per ensemble member (0..4)

set -euo pipefail

mkdir -p logs

module load conda || true

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

# Create env if missing (first job only)
if [ ! -x ./cnn_env/bin/python ]; then
  conda env create -f trend_code_submit/cnn_env.yml -p ./cnn_env
  ./cnn_env/bin/python -m pip install --index-url https://download.pytorch.org/whl/cu118 torch torchvision
  ./cnn_env/bin/python -m pip install pyarrow lxml beautifulsoup4 requests python-dateutil pytz
fi

export IDX=${SLURM_ARRAY_TASK_ID}

./cnn_env/bin/python - << 'PY'
import os
from Experiments.cnn_experiment import train_us_model

idx = int(os.environ.get("IDX", "0"))

# Train a single ensemble member by restricting ensem_range
train_us_model(
    ws_list=[20],
    pw_list=[5],
    ensem=5,
    ensem_range=[idx],
    calculate_portfolio=False,
    ts1d_model=False,
    lr=1e-4,
)
PY

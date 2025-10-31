#!/bin/bash
#SBATCH --job-name=cnn_weekly_portfolios
#SBATCH --partition=gpu            # can also use a CPU queue; GPU not required here
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

set -euo pipefail

mkdir -p logs

module load conda || true

cd ~/cnnthesis
export PYTHONPATH="$(pwd)/trend_code_submit"

if [ ! -x ./cnn_env/bin/python ]; then
  conda env create -f trend_code_submit/cnn_env.yml -p ./cnn_env
  ./cnn_env/bin/python -m pip install --index-url https://download.pytorch.org/whl/cu118 torch torchvision
  ./cnn_env/bin/python -m pip install pyarrow lxml beautifulsoup4 requests python-dateutil pytz
fi

./cnn_env/bin/python - << 'PY'
from Experiments.cnn_experiment import train_us_model

# Reuse saved checkpoints; only generate OOS predictions & portfolios
train_us_model(
    ws_list=[20],
    pw_list=[5],
    ensem=5,
    calculate_portfolio=True,
    ts1d_model=False,
    from_ensem_res=True,
    lr=1e-4,
)
PY

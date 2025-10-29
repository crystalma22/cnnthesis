#!/bin/bash
#SBATCH --job-name=cnn_portfolios
#SBATCH --output=logs/cnn_portfolios_%j.out
#SBATCH --error=logs/cnn_portfolios_%j.err
#SBATCH --partition=compute
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4
#SBATCH --time=2:00:00

cd ~/cnnthesis
PYTHONPATH="$(pwd)/trend_code_submit" ~/cnnthesis/cnn_env/bin/python generate_cnn_portfolios.py


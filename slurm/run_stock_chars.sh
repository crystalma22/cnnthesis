#!/bin/bash
#SBATCH --job-name=stock_chars
#SBATCH --output=logs/stock_chars_%j.out
#SBATCH --error=logs/stock_chars_%j.err
#SBATCH --partition=compute
#SBATCH --mem=128G
#SBATCH --cpus-per-task=8
#SBATCH --time=4:00:00

cd ~/cnnthesis
PYTHONPATH="$(pwd)/trend_code_submit" ~/cnnthesis/cnn_env/bin/python thesis_scripts/generate_stock_chars_with_cnn.py


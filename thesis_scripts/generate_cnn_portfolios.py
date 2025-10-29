#!/usr/bin/env python3
"""
Generate CNN portfolio returns for I20/R5 model.

Creates decile portfolios (EW and VW) based on CNN up-probabilities.

Usage:
  PYTHONPATH="$(pwd)/trend_code_submit" python generate_cnn_portfolios.py
"""

import os
import sys

# Setup paths
repo_dir = os.path.dirname(__file__)
# Handle both cases: script in thesis_scripts/ or root
if "thesis_scripts" in repo_dir:
    # Running from thesis_scripts/
    base_dir = os.path.dirname(repo_dir)  # Go up to cnnthesis root
    code_dir = os.path.join(base_dir, "trend_code_submit")
else:
    # Running from root
    code_dir = os.path.join(repo_dir, "trend_code_submit")
os.chdir(code_dir)
sys.path.insert(0, code_dir)

from Analysis import analysis_lib
from Misc import config as cf

print("=" * 80)
print("Generating CNN Portfolio Returns")
print("=" * 80)
print("\nModel: I20/R5 (20-day lookback, 5-day prediction horizon)")
print("Frequency: Weekly")
print("Ensemble: 5 models")
print(f"OOS Years: {cf.OOS_YEARS[0]}-{cf.OOS_YEARS[-1]}")
print("\nThis will generate:")
print("  - Equal-weight (EW) decile portfolios")
print("  - Value-weight (VW) decile portfolios")
print("  - High-Low (H-L) spreads")
print("  - Portfolio performance metrics")
print("\nPortfolio directory: WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/")
print("\nStarting portfolio generation...\n")

# Generate portfolios for I20/R5 model
analysis_lib.portfolio_performance_helper(ws=20, pw=5)

print("\n" + "=" * 80)
print("✅ Portfolio generation complete!")
print("=" * 80)
print("\nCheck output directory for portfolio CSV files:")
print("  WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/")


#!/usr/bin/env python3
"""
Generate only VW (value-weight) portfolio for CNN I20/R5 model.
"""

import os
import sys

# Setup paths
repo_dir = os.path.dirname(__file__)
if "thesis_scripts" in repo_dir:
    base_dir = os.path.dirname(repo_dir)
    code_dir = os.path.join(base_dir, "trend_code_submit")
else:
    code_dir = os.path.join(repo_dir, "trend_code_submit")
os.chdir(code_dir)
sys.path.insert(0, code_dir)

from Portfolio.portfolio import PortfolioManager
from Data import dgp_config as dcf
from Misc import config as cf
import pandas as pd

print("Loading predictions...")
signal_df = pd.read_csv(dcf.CACHE_DIR / "weekly_prediction_with_rets.csv")
signal_df["Date"] = pd.to_datetime(signal_df["Date"])
signal_df["StockID"] = signal_df["StockID"].astype(str)
signal_df = signal_df.set_index(["Date", "StockID"])
df = signal_df.rename({"CNN20D5P": "up_prob"}, axis="columns")
df = df[["up_prob", "MarketCap"]].copy()

print("Creating VW portfolio...")
portfolio_dir = dcf.PORTFOLIO / "cnn_weekly" / "CNN20D5P"
portfolio = PortfolioManager(
    df,
    freq="week",
    portfolio_dir=portfolio_dir,
    start_year=cf.OOS_YEARS[0],
    end_year=cf.OOS_YEARS[-1],
)

# Only generate VW portfolio
print("Generating value-weight portfolio...")
portfolio.generate_portfolio()

print("✅ VW portfolio complete!")



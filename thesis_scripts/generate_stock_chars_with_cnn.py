#!/usr/bin/env python3
"""
Generate cnn_and_monthly_stock_char parquet files for I20/R5 model.

Combines CNN predictions with stock characteristics for regression analysis.

Outputs:
- CACHE_DIR/cnn_and_monthly_stock_char_is.parquet (in-sample: 1993-2000)
- CACHE_DIR/cnn_and_monthly_stock_char_oos.parquet (out-of-sample: 2001-2024)

Usage:
  PYTHONPATH="$(pwd)/trend_code_submit" python generate_stock_chars_with_cnn.py
"""

import os
import sys
import pandas as pd
import numpy as np
import time

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

from Data import dgp_config as dcf
from Data.equity_data import processed_US_data, get_spy_freq_rets
from Experiments.cnn_experiment import get_bl_exp_obj
from Misc import config as cf


def compute_stock_characteristics_at_dates(df: pd.DataFrame, target_dates: pd.DataFrame) -> pd.DataFrame:
    """
    Compute stock characteristics available as of target dates.
    
    Input: 
        - df: Daily stock panel with returns (MultiIndex: Date, StockID)
        - target_dates: DataFrame with columns (Date, StockID) - the prediction dates (τ)
    Output: Characteristics available at each target date
    """
    print("Computing stock characteristics at prediction dates...")
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["StockID", "Date"])
    
    target_dates = target_dates.copy()
    target_dates["Date"] = pd.to_datetime(target_dates["Date"])
    target_dates = target_dates.sort_values(["StockID", "Date"])
    
    print(f"  Target dates: {len(target_dates)} prediction dates")
    
    # Initialize output dataframe
    chars = target_dates.copy()
    chars = chars.set_index(["Date", "StockID"]).sort_index()
    
    # Merge in MarketCap from daily data (available at τ)
    marketcap_df = df.set_index(["Date", "StockID"])[["MarketCap"]]
    chars = chars.join(marketcap_df, how="left")
    
    # For each characteristic, we need to get the value available at τ (i.e., from date ≤ τ)
    # Use merge_asof to get most recent value ≤ target date
    
    # Reset for merge_asof
    target_reset = target_dates.sort_values(["StockID", "Date"])
    df_sorted = df.sort_values(["StockID", "Date"])
    
    # Momentum (12-month return skipping last month = Ret_260d, get from ~20 days before τ)
    if "Ret_260d" in df.columns:
        # Create adjusted dates (20 days before τ) for skip-month logic
        target_adjusted = target_reset.copy()
        target_adjusted["Date_adjusted"] = target_adjusted["Date"] - pd.Timedelta(days=20)
        
        mom_temp = pd.merge_asof(
            target_adjusted.sort_values(["StockID", "Date_adjusted"]),
            df_sorted[["Date", "StockID", "Ret_260d"]],
            left_on="Date_adjusted",
            right_on="Date",
            by="StockID",
            direction="backward"
        )
        chars["MOM"] = mom_temp["Ret_260d"].values
    else:
        chars["MOM"] = np.nan
    
    # Short-term reversal (1-month return = Ret_20d, get value from 1 day before τ)
    if "Ret_20d" in df.columns:
        str_temp = pd.merge_asof(
            target_reset.copy(),
            df_sorted[["Date", "StockID", "Ret_20d"]].assign(Date_adj=lambda x: x["Date"] - pd.Timedelta(days=1)),
            left_on="Date",
            right_on="Date_adj",
            by="StockID",
            direction="backward"
        )
        chars["STR"] = str_temp["Ret_20d"].values
    else:
        chars["STR"] = np.nan
    
    # Lag Weekly Return (Ret_5d, get value from 1 day before τ)
    if "Ret_5d" in df.columns:
        lag_week_temp = pd.merge_asof(
            target_reset.copy(),
            df_sorted[["Date", "StockID", "Ret_5d"]].assign(Date_adj=lambda x: x["Date"] - pd.Timedelta(days=1)),
            left_on="Date",
            right_on="Date_adj",
            by="StockID",
            direction="backward"
        )
        chars["Lag Weekly Return"] = lag_week_temp["Ret_5d"].values
    else:
        chars["Lag Weekly Return"] = np.nan
    
    # Trend (60-day return = Ret_60d, get value from 1 day before τ)
    if "Ret_60d" in df.columns:
        trend_temp = pd.merge_asof(
            target_reset.copy(),
            df_sorted[["Date", "StockID", "Ret_60d"]].assign(Date_adj=lambda x: x["Date"] - pd.Timedelta(days=1)),
            left_on="Date",
            right_on="Date_adj",
            by="StockID",
            direction="backward"
        )
        chars["TREND"] = trend_temp["Ret_60d"].values
    else:
        chars["TREND"] = np.nan
    
    # Volatility (EWMA, get value from 1 day before τ)
    if "EWMA_vol" in df.columns:
        vol_temp = pd.merge_asof(
            target_reset.copy(),
            df_sorted[["Date", "StockID", "EWMA_vol"]].assign(Date_adj=lambda x: x["Date"] - pd.Timedelta(days=1)),
            left_on="Date",
            right_on="Date_adj",
            by="StockID",
            direction="backward"
        )
        chars["Volatility"] = vol_temp["EWMA_vol"].values
    else:
        chars["Volatility"] = np.nan
    
    # Dollar Volume (log of volume * close, get value at τ)
    if "Vol" in df.columns and "Close" in df.columns:
        df["Dollar_Vol_temp"] = np.log(df["Vol"] * df["Close"] + 1)
        dollar_vol_temp = pd.merge_asof(
            target_reset.copy(),
            df_sorted[["Date", "StockID", "Dollar_Vol_temp"]],
            on="Date",
            by="StockID",
            direction="backward"
        )
        chars["Dollar Volume"] = dollar_vol_temp["Dollar_Vol_temp"].values
    else:
        chars["Dollar Volume"] = np.nan
    
    # Placeholders
    chars["52WH"] = np.nan  # Would need rolling max
    chars["Bid-Ask"] = np.nan  # Not available in CRSP daily
    chars["Zero Trade"] = np.nan  # Not directly available
    chars["Price Delay"] = np.nan  # Would need regression
    chars["Illiquidity"] = np.nan  # Would need Amihud calculation
    chars["Beta"] = 1.0  # Placeholder (would need market returns)
    
    # Size (log of MarketCap)
    chars["Size"] = np.log(chars["MarketCap"] + 1)
    
    print(f"  Computed characteristics for {len(chars)} prediction dates")
    return chars


def main():
    print("=" * 80)
    print("Generating CNN + Stock Characteristics Parquet Files")
    print("=" * 80)
    
    # 1. Load processed US data
    print("\n1. Loading processed US equity data...")
    start_time = time.time()
    daily_data = processed_US_data()
    print(f"   Loaded {len(daily_data):,} daily observations")
    print(f"   Date range: {daily_data.index.get_level_values('Date').min()} to {daily_data.index.get_level_values('Date').max()}")
    print(f"   Time: {(time.time() - start_time)/60:.2f} minutes")
    
    # 2. Load CNN predictions (I20/R5 model only) - these are our anchor dates (τ)
    print("\n2. Loading CNN ensemble predictions (I20/R5)...")
    start_time = time.time()
    ws, pw = 20, 5
    exp = get_bl_exp_obj(ws=ws, pw=pw, lr=1e-4, ensem=5)
    
    # Load predictions for both IS and OOS
    all_years = list(cf.IS_YEARS) + list(cf.OOS_YEARS)
    df_cnn = exp.load_ensem_res(year=all_years, multiindex=True, freq="week")
    
    # Rename up_prob to I20/R5 format
    df_cnn = df_cnn.rename(columns={"up_prob": f"I{ws}/R{pw}"})
    df_cnn = df_cnn[[f"I{ws}/R{pw}", "MarketCap"]].copy()
    
    print(f"   Loaded {len(df_cnn):,} CNN predictions")
    print(f"   Date range: {df_cnn.index.get_level_values('Date').min()} to {df_cnn.index.get_level_values('Date').max()}")
    print(f"   These prediction dates (τ) will anchor all calculations")
    print(f"   Time: {(time.time() - start_time)/60:.2f} minutes")
    
    # 3. Compute stock characteristics available as of each prediction date (τ)
    print("\n3. Computing stock characteristics at prediction dates (τ)...")
    start_time = time.time()
    
    # Get prediction dates as target dates
    df_cnn_reset = df_cnn.reset_index()
    target_dates = df_cnn_reset[["Date", "StockID"]].copy()
    
    # Compute characteristics available at each τ
    stock_chars = compute_stock_characteristics_at_dates(daily_data, target_dates)
    print(f"   Time: {(time.time() - start_time)/60:.2f} minutes")
    
    # 4. Merge stock characteristics with CNN predictions
    print("\n4. Merging stock characteristics with CNN predictions...")
    start_time = time.time()
    
    # Both are indexed by (Date, StockID) where Date = τ (prediction date)
    combined = stock_chars.join(df_cnn[[f"I{ws}/R{pw}"]], how="inner")
    print(f"   After merge: {len(combined):,} observations")
    print(f"   All aligned to prediction dates (τ)")
    print(f"   Time: {(time.time() - start_time)/60:.2f} minutes")
    
    # 5. Add future returns starting from prediction date (τ → τ+5)
    print("\n5. Adding future returns from prediction dates (τ → τ+5)...")
    start_time = time.time()
    
    # Future return is the 5-day return starting from prediction date τ (not month-end!)
    # Use cumulative log returns for accuracy
    if "cum_log_ret" in daily_data.columns:
        combined_reset = combined.reset_index()
        daily_reset = daily_data[["cum_log_ret"]].reset_index()
        daily_reset["Date"] = pd.to_datetime(daily_reset["Date"])
        daily_reset = daily_reset.sort_values(["StockID", "Date"])
        
        # For each prediction date τ, find 5 trading days later (τ+5)
        print(f"   Computing 5-day returns for {len(combined_reset):,} predictions...")
        
        # Merge to get cumulative return at τ
        combined_reset = pd.merge_asof(
            combined_reset.sort_values(["StockID", "Date"]),
            daily_reset[["Date", "StockID", "cum_log_ret"]].rename(columns={"cum_log_ret": "cum_log_ret_tau"}),
            on="Date",
            by="StockID",
            direction="backward"
        )
        
        # Calculate τ+5 date for each row
        combined_reset["tau_plus_5"] = combined_reset["Date"].apply(
            lambda x: pd.bdate_range(start=x, periods=pw+1)[pw] if len(pd.bdate_range(start=x, periods=pw+1)) > pw else None
        )
        
        # Merge to get cumulative return at τ+5
        combined_reset = combined_reset.sort_values(["StockID", "tau_plus_5"])
        daily_reset_plus5 = daily_reset.copy()
        daily_reset_plus5 = daily_reset_plus5.rename(columns={"Date": "tau_plus_5", "cum_log_ret": "cum_log_ret_tau_plus_5"})
        
        combined_reset = pd.merge_asof(
            combined_reset,
            daily_reset_plus5[["tau_plus_5", "StockID", "cum_log_ret_tau_plus_5"]],
            on="tau_plus_5",
            by="StockID",
            direction="backward",
            allow_exact_matches=True
        )
        
        # Calculate return: exp(cum_log_ret[τ+5] - cum_log_ret[τ]) - 1
        combined_reset["Future_Ret_5d"] = np.where(
            combined_reset["cum_log_ret_tau_plus_5"].notna() & combined_reset["cum_log_ret_tau"].notna(),
            np.exp(combined_reset["cum_log_ret_tau_plus_5"] - combined_reset["cum_log_ret_tau"]) - 1,
            np.nan
        )
        
        # Drop temporary columns and reset index
        combined_reset = combined_reset.drop(columns=["cum_log_ret_tau", "tau_plus_5", "cum_log_ret_tau_plus_5"])
        combined = combined_reset.set_index(["Date", "StockID"])
        
        print(f"   Computed returns: {combined['Future_Ret_5d'].notna().sum():,} non-NaN")
        print(f"   Return window: τ (prediction date) → τ+5 (5 trading days later)")
    else:
        print("   Error: cum_log_ret not available in daily data")
        combined["Future_Ret_5d"] = np.nan
    
    print(f"   Time: {(time.time() - start_time)/60:.2f} minutes")
    
    # 6. Optional: Filter to last prediction of each month (for monthly summary)
    print("\n6. Optional monthly filtering (keeping last τ of each month)...")
    combined_reset = combined.reset_index()
    combined_reset["Date"] = pd.to_datetime(combined_reset["Date"])
    combined_reset["YearMonth"] = combined_reset["Date"].dt.to_period("M")
    
    # Keep only the last prediction date (τ) in each month for each stock
    print(f"   Before monthly filter: {len(combined_reset):,} observations")
    monthly_last = combined_reset.sort_values(["StockID", "YearMonth", "Date"]).groupby(["StockID", "YearMonth"]).tail(1)
    print(f"   After keeping last τ per month: {len(monthly_last):,} observations")
    
    # Use monthly summary (uncomment to enable)
    # combined_reset = monthly_last.copy()
    # print(f"   Using monthly summary (last τ of each month)")
    
    # Drop temporary column
    combined_reset = combined_reset.drop(columns=["YearMonth"])
    
    # 7. Split into IS and OOS
    print("\n7. Splitting into in-sample and out-of-sample...")
    combined_reset["Date"] = pd.to_datetime(combined_reset["Date"])
    
    is_mask = combined_reset["Date"].dt.year.isin(cf.IS_YEARS)
    oos_mask = combined_reset["Date"].dt.year.isin(cf.OOS_YEARS)
    
    is_df = combined_reset[is_mask].copy()
    oos_df = combined_reset[oos_mask].copy()
    
    is_df = is_df.set_index(["Date", "StockID"])
    oos_df = oos_df.set_index(["Date", "StockID"])
    
    print(f"   In-sample (1993-2000): {len(is_df):,} observations")
    print(f"   Out-of-sample (2001-2024): {len(oos_df):,} observations")
    
    # 8. Save parquet files
    print("\n8. Saving parquet files...")
    is_path = os.path.join(dcf.CACHE_DIR, "cnn_and_monthly_stock_char_is.parquet")
    oos_path = os.path.join(dcf.CACHE_DIR, "cnn_and_monthly_stock_char_oos.parquet")
    
    is_df.reset_index().to_parquet(is_path, index=False)
    oos_df.reset_index().to_parquet(oos_path, index=False)
    
    print(f"   Saved: {is_path}")
    print(f"   Size: {os.path.getsize(is_path) / 1024:.1f} KB")
    print(f"   Saved: {oos_path}")
    print(f"   Size: {os.path.getsize(oos_path) / 1024:.1f} KB")
    
    # Print summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"In-sample columns: {list(is_df.columns)}")
    print(f"In-sample date range: {is_df.index.get_level_values('Date').min()} to {is_df.index.get_level_values('Date').max()}")
    print(f"Out-of-sample columns: {list(oos_df.columns)}")
    print(f"Out-of-sample date range: {oos_df.index.get_level_values('Date').min()} to {oos_df.index.get_level_values('Date').max()}")
    print("\n✅ Successfully generated stock characteristics + CNN parquet files!")


if __name__ == "__main__":
    main()

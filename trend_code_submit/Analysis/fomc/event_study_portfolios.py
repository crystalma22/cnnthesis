#!/usr/bin/env python3
"""
Event-study portfolios: Compare CNN H-L performance during FOMC windows vs. non-event days.

Computes decile spreads for:
- Pre-announcement window (day before to announcement)
- Reaction window (announcement to next day)
- Intermediate window (t+4 to t+20)
- Non-event days (all other days)

Outputs:
- Table E1: H-L performance by window (Return, Vol, SR, Turnover)
- Figure E1: Cumulative H-L around FOMC events

Usage:
  PYTHONPATH="$(pwd)/trend_code_submit" python trend_code_submit/Analysis/fomc/event_study_portfolios.py
"""

import os
import os.path as op
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Data import dgp_config as dcf
from Data.equity_data import processed_US_data


def load_fomc_schedule():
    """Load FOMC schedule with offsets."""
    path = op.join(dcf.CACHE_DIR, "fomc", "fomc_schedule_with_offsets.csv")
    if not op.isfile(path):
        raise SystemExit(f"Missing {path}. Run FOMC pipeline first.")
    df = pd.read_csv(path, parse_dates=["announcement_date", "t_minus_1", "t_plus_1", "t_plus_5", "t_plus_20"])
    return df


def load_predictions():
    """Load weekly CNN predictions."""
    path = op.join(dcf.CACHE_DIR, "weekly_prediction_with_rets.csv")
    if not op.isfile(path):
        raise SystemExit(f"Missing {path}. Run make_prediction_with_rets.py first.")
    df = pd.read_csv(path, parse_dates=["Date"])
    df["StockID"] = df["StockID"].astype(str)
    
    # Use CNN20D5P
    if "CNN20D5P" not in df.columns:
        raise SystemExit("CNN20D5P column not found")
    
    df = df[["Date", "StockID", "CNN20D5P", "MarketCap"]].rename(columns={"CNN20D5P": "up_prob"})
    return df


def create_event_masks(dates: pd.DatetimeIndex, schedule: pd.DataFrame) -> dict:
    """Create boolean masks for different FOMC windows."""
    dates = pd.to_datetime(dates)
    
    masks = {
        "pre": np.zeros(len(dates), dtype=bool),
        "announce": np.zeros(len(dates), dtype=bool),
        "react": np.zeros(len(dates), dtype=bool),
        "intermediate": np.zeros(len(dates), dtype=bool),
    }
    
    for _, row in schedule.iterrows():
        t0 = pd.to_datetime(row["announcement_date"])
        t_m1 = pd.to_datetime(row["t_minus_1"])
        t_p1 = pd.to_datetime(row["t_plus_1"])
        
        # Pre: day before announcement
        masks["pre"] |= (dates == t_m1)
        
        # Announcement day
        masks["announce"] |= (dates == t0)
        
        # Reaction: next day
        masks["react"] |= (dates == t_p1)
        
        # Intermediate: t+4 to t+20
        if pd.notna(row["t_plus_5"]) and pd.notna(row["t_plus_20"]):
            t_p5 = pd.to_datetime(row["t_plus_5"])
            t_p20 = pd.to_datetime(row["t_plus_20"])
            masks["intermediate"] |= ((dates >= t_p5) & (dates <= t_p20))
    
    # Non-event: all other days
    any_event = masks["pre"] | masks["announce"] | masks["react"] | masks["intermediate"]
    masks["non_event"] = ~any_event
    
    return masks


def compute_hl_spread(df: pd.DataFrame, ret_col: str = "Ret") -> dict:
    """Compute H-L decile spread statistics."""
    # Deciles on up_prob
    df = df.dropna(subset=["up_prob", ret_col, "MarketCap"]).copy()
    if len(df) < 100:
        return {"EW_ret": np.nan, "VW_ret": np.nan, "EW_vol": np.nan, "VW_vol": np.nan, 
                "EW_SR": np.nan, "VW_SR": np.nan, "n_obs": len(df)}
    
    df["decile"] = pd.qcut(df["up_prob"], 10, labels=False, duplicates="drop")
    
    # Equal-weight
    ew_mean = df.groupby("decile")[ret_col].mean()
    ew_hl = ew_mean.iloc[-1] - ew_mean.iloc[0] if len(ew_mean) >= 2 else np.nan
    ew_vol = df.groupby("decile")[ret_col].std().mean()
    
    # Value-weight
    vw_mean = df.groupby("decile").apply(lambda g: np.average(g[ret_col], weights=g["MarketCap"]))
    vw_hl = vw_mean.iloc[-1] - vw_mean.iloc[0] if len(vw_mean) >= 2 else np.nan
    vw_vol = df.groupby("decile").apply(
        lambda g: np.sqrt(np.average((g[ret_col] - np.average(g[ret_col], weights=g["MarketCap"]))**2, weights=g["MarketCap"]))
    ).mean()
    
    # Annualize (assuming daily returns)
    ew_ret_ann = ew_hl * 252
    vw_ret_ann = vw_hl * 252
    ew_vol_ann = ew_vol * np.sqrt(252)
    vw_vol_ann = vw_vol * np.sqrt(252)
    
    return {
        "EW_ret": ew_ret_ann,
        "VW_ret": vw_ret_ann,
        "EW_vol": ew_vol_ann,
        "VW_vol": vw_vol_ann,
        "EW_SR": ew_ret_ann / ew_vol_ann if ew_vol_ann > 0 else np.nan,
        "VW_SR": vw_ret_ann / vw_vol_ann if vw_vol_ann > 0 else np.nan,
        "n_obs": len(df)
    }


def main():
    print("Loading data...")
    schedule = load_fomc_schedule()
    pred = load_predictions()
    us_data = processed_US_data()
    
    # Merge predictions with daily returns
    us_data = us_data.reset_index()
    us_data["Date"] = pd.to_datetime(us_data["Date"])
    us_data["StockID"] = us_data["StockID"].astype(str)
    
    # Merge on nearest weekly prediction (backward)
    print("Aligning predictions to daily data...")
    merged = pd.merge_asof(
        us_data.sort_values(["StockID", "Date"]),
        pred.sort_values(["StockID", "Date"]),
        on="Date",
        by="StockID",
        direction="backward",
        suffixes=("", "_pred")
    )
    
    print(f"Merged data: {len(merged)} rows with predictions")
    
    # Create event masks
    print("Creating event windows...")
    masks = create_event_masks(merged["Date"], schedule)
    
    # Compute H-L for each window
    results = []
    for window_name in ["pre", "announce", "react", "intermediate", "non_event"]:
        print(f"Computing {window_name} window...")
        window_data = merged[masks[window_name]].copy()
        stats = compute_hl_spread(window_data, ret_col="Ret")
        stats["window"] = window_name
        results.append(stats)
    
    # Create table
    table = pd.DataFrame(results)
    table = table[["window", "EW_ret", "EW_vol", "EW_SR", "VW_ret", "VW_vol", "VW_SR", "n_obs"]]
    
    # Save
    out_path = op.join(dcf.CACHE_DIR, "fomc", "event_study_portfolio_table.csv")
    table.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
    print("\n=== Table E1: CNN H-L Performance by FOMC Window ===")
    print(table.to_string(index=False))
    
    # Create figure: cumulative H-L around events
    print("\nGenerating cumulative return figure...")
    # TODO: Implement event-time cumulative returns
    
    return table


if __name__ == "__main__":
    main()



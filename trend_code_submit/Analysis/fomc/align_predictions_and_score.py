#!/usr/bin/env python3
from __future__ import annotations

"""
Align weekly CNN predictions to FOMC announcement dates (last prediction date <= t)
and compute decile performance for pre, reaction, and intermediate windows.

Inputs:
  - CACHE_DIR/weekly_prediction_with_rets.csv
  - CACHE_DIR/fomc/fomc_window_returns.csv

Output:
  - CACHE_DIR/fomc/fomc_decile_performance.csv

Run: cnn_env/bin/python trend_code_submit/Analysis/fomc/align_predictions_and_score.py
"""

import os
import os.path as op
from typing import Tuple

import numpy as np
import pandas as pd

from Data import dgp_config as dcf


def cache_dir() -> str:
    d = op.join(str(dcf.CACHE_DIR), "fomc")
    os.makedirs(d, exist_ok=True)
    return d


def load_predictions() -> pd.DataFrame:
    pred_path = op.join(str(dcf.CACHE_DIR), "weekly_prediction_with_rets.csv")
    if not op.isfile(pred_path):
        raise SystemExit(
            f"Missing {pred_path}. Run make_prediction_with_rets.py after training."
        )
    df = pd.read_csv(pred_path, parse_dates=["Date"])
    df["StockID"] = df["StockID"].astype(str)
    
    # Validate we have enough predictions
    total_rows = len(df)
    unique_dates = df["Date"].nunique()
    unique_stocks = df["StockID"].nunique()
    print(f"\nPredictions file loaded: {total_rows:,} rows, {unique_dates} dates, {unique_stocks} stocks")
    
    if total_rows < 1000:
        print(f"WARNING: Very few predictions ({total_rows} rows). This may indicate:")
        print("  - Training not complete (need all 5 ensemble checkpoints)")
        print("  - Model failed to generate predictions")
        print("  - Data preprocessing issues")
    
    # Choose baseline signal: CNN20D5P (I20/R5). Adjust if you prefer another column.
    if "CNN20D5P" not in df.columns:
        # Fallback: pick any CNN*5P column
        cnn_cols = [c for c in df.columns if c.startswith("CNN") and c.endswith("5P")]
        if not cnn_cols:
            raise SystemExit(
                f"No CNN*5P columns found in predictions. Available columns: {df.columns.tolist()}"
            )
        sel = cnn_cols[0]
        print(f"Using {sel} instead of CNN20D5P")
    else:
        sel = "CNN20D5P"
    
    df = df[["Date", "StockID", sel, "MarketCap"]].rename(columns={sel: "up_prob"})
    df.sort_values(["StockID", "Date"], inplace=True)
    return df


def load_fomc_windows() -> pd.DataFrame:
    path = op.join(cache_dir(), "fomc_window_returns.csv")
    if not op.isfile(path):
        raise SystemExit(f"Missing {path}. Run build_windows.py first.")
    df = pd.read_csv(path, parse_dates=["announcement_date"])
    # Drop rows with NaN StockID first
    df = df[df["StockID"].notna()].copy()
    # Convert float to int to string: 10001.0 -> 10001 -> "10001"
    df["StockID"] = df["StockID"].astype(float).astype(int).astype(str)
    
    # Filter to prediction period only (2001-2024) - no CNN predictions before 2001
    print(f"Before filtering: {len(df):,} rows")
    df = df[df["announcement_date"] >= "2001-01-01"].copy()
    print(f"After filtering to 2001+: {len(df):,} rows")
    
    return df


def merge_asof_by_stock(pred: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "="*80)
    print("Starting merge_asof_by_stock")
    print("="*80)
    # Align predictions to events using merge_asof on (StockID, Date)
    print(f"Starting merge_asof for {pred['StockID'].nunique()} stocks in predictions")
    print(f"Events cover {events['StockID'].nunique()} stocks")
    
    # Drop MarketCap from events to avoid conflict (use prediction's MarketCap)
    ev_cols = [c for c in events.columns if c != "MarketCap"]
    events_clean = events[ev_cols].copy()
    
    # Rename for merge
    events_clean = events_clean.rename(columns={"announcement_date": "Date"})
    
    # Sort both dataframes for merge_asof
    print("Sorting dataframes for merge_asof...")
    # merge_asof with 'by' requires sorting: StockID first, then Date
    events_clean = events_clean.sort_values(["StockID", "Date"]).reset_index(drop=True)
    pred_sorted = pred.sort_values(["StockID", "Date"]).reset_index(drop=True)
    
    print(f"Events: {len(events_clean)} rows")
    print(f"Predictions: {len(pred_sorted)} rows")
    
    # merge_asof with 'by' parameter has issues with pandas 1.x
    # Workaround: loop by stock but use vectorized operations within each stock
    print("Merging predictions with events (grouped approach)...")
    
    res_list = []
    stock_count = 0
    unique_stocks = events_clean["StockID"].unique()
    total_stocks = len(unique_stocks)
    
    for sid in unique_stocks:
        stock_count += 1
        if stock_count % 1000 == 0:
            print(f"  Processed {stock_count}/{total_stocks} stocks...")
        
        ev_subset = events_clean[events_clean["StockID"] == sid]
        pred_subset = pred_sorted[pred_sorted["StockID"] == sid]
        
        if ev_subset.empty or pred_subset.empty:
            continue
        
        # Merge for this stock
        aligned_stock = pd.merge_asof(
            ev_subset,
            pred_subset[["Date", "up_prob", "MarketCap"]],
            on="Date",
            direction="backward",
            suffixes=("", "_pred")
        )
        res_list.append(aligned_stock)
    
    print(f"\nCompleted merging {len(res_list)} stocks")
    aligned = pd.concat(res_list, ignore_index=True) if res_list else events_clean.copy()
    
    # Rename back
    aligned = aligned.rename(columns={"Date": "announcement_date"})
    print(f"Merge complete! Result: {len(aligned)} rows")
    
    print(f"\nFinal merged data:")
    print(f"  Rows: {len(aligned):,}")
    print(f"  Columns: {aligned.columns.tolist()}")
    print(f"  Has up_prob: {'up_prob' in aligned.columns}")
    if 'up_prob' in aligned.columns:
        print(f"  Non-null up_prob: {aligned['up_prob'].notna().sum():,} / {len(aligned):,}")
    
    # Show first few rows for debugging
    print(f"\nFirst 3 rows of merged data:")
    print(aligned.head(3))
    
    return aligned


def decile_scores(df: pd.DataFrame, ret_col: str) -> Tuple[pd.Series, pd.Series]:
    # Compute EW and VW decile means and H-L for a single event
    d = df[["up_prob", ret_col, "MarketCap"]].dropna().copy()
    if d.empty:
        idx = ["d1","d2","d3","d4","d5","d6","d7","d8","d9","d10","H-L"]
        return pd.Series(index=idx, dtype=float), pd.Series(index=idx, dtype=float)
    d["decile"] = pd.qcut(d["up_prob"], 10, labels=False, duplicates="drop")
    ew = d.groupby("decile")[ret_col].mean()
    vw = (d.groupby("decile").apply(lambda x: np.average(x[ret_col], weights=x["MarketCap"]))
          if d["MarketCap"].notna().any() else ew)
    # Ensure 10 deciles
    for dec in range(10):
        if dec not in ew.index:
            ew.loc[dec] = np.nan
            vw.loc[dec] = np.nan
    ew = ew.sort_index()
    vw = vw.sort_index()
    idx = [f"d{i}" for i in range(1,11)] + ["H-L"]
    ew_series = pd.Series(list(ew.values) + [ew.iloc[-1] - ew.iloc[0]], index=idx)
    vw_series = pd.Series(list(vw.values) + [vw.iloc[-1] - vw.iloc[0]], index=idx)
    return ew_series, vw_series


def main() -> None:
    pred = load_predictions()
    print(f"Loaded predictions: {len(pred)} rows")
    print(f"Prediction columns: {pred.columns.tolist()}")
    
    win = load_fomc_windows()
    print(f"\nLoaded FOMC windows: {len(win)} rows")
    print(f"Window columns: {win.columns.tolist()}")

    # Align predictions to events by stock
    print("\nAligning predictions to events...")
    aligned = merge_asof_by_stock(pred, win)
    print(f"After alignment: {len(aligned)} rows")
    print(f"Aligned columns: {aligned.columns.tolist()}")
    
    if "up_prob" not in aligned.columns:
        print("\nERROR: 'up_prob' column missing after merge!")
        print("\nDiagnostic info:")
        print(f"  - Predictions date range: {pred['Date'].min()} to {pred['Date'].max()}")
        print(f"  - FOMC announcement dates: {win['announcement_date'].min()} to {win['announcement_date'].max()}")
        print(f"  - Unique stocks in predictions: {pred['StockID'].nunique()}")
        print(f"  - Unique stocks in FOMC windows: {win['StockID'].nunique()}")
        
        # Check date overlap
        pred_dates = set(pred['Date'].dt.date)
        fomc_dates = set(win['announcement_date'].dt.date)
        overlapping = pred_dates.intersection(fomc_dates)
        print(f"  - Date overlap: {len(overlapping)} dates overlap")
        
        print("\nSample of aligned data:")
        print(aligned.head())
        print("\nThis likely means predictions don't exist for these FOMC dates.")
        print("Possible causes:")
        print("  1. Prediction file is incomplete (only 100 rows found earlier)")
        print("  2. Training not complete - need to run on Laguna GPU")
        print("  3. Date alignment issue")
        raise SystemExit("Cannot proceed without valid predictions")

    # Compute event-level decile scores for each window
    rows = []
    for adate, g in aligned.groupby("announcement_date"):
        # Skip events without predictions (NaN up_prob from pre-2001 dates)
        g = g[g["up_prob"].notna()].copy()
        if g.empty:
            print(f"Skipping {adate} - no valid predictions")
            continue
        
        # Compute deciles for all 4 windows
        # Check which columns exist (backward compatibility)
        if "pre_fomc_ret" in g.columns:
            ew_pre, vw_pre = decile_scores(g, "pre_fomc_ret")
        elif "pre_ret" in g.columns:
            ew_pre, vw_pre = decile_scores(g, "pre_ret")
        else:
            ew_pre = vw_pre = pd.Series()
        
        if "announcement_day_ret" in g.columns:
            ew_ann, vw_ann = decile_scores(g, "announcement_day_ret")
        else:
            ew_ann = vw_ann = pd.Series()
        
        ew_rea, vw_rea = decile_scores(g, "react_ret") if "react_ret" in g.columns else (pd.Series(), pd.Series())
        ew_int, vw_int = decile_scores(g, "intermediate_ret") if "intermediate_ret" in g.columns else (pd.Series(), pd.Series())
        
        row = {"announcement_date": adate}
        
        # Store all windows
        for prefix, ew_s, vw_s in [
            ("pre_fomc", ew_pre, vw_pre),
            ("announcement", ew_ann, vw_ann),
            ("react", ew_rea, vw_rea),
            ("inter", ew_int, vw_int)
        ]:
            for k, v in ew_s.items():
                row[f"{prefix}_ew_{k}"] = v
            for k, v in vw_s.items():
                row[f"{prefix}_vw_{k}"] = v
        rows.append(row)

    out = pd.DataFrame(rows).sort_values("announcement_date")

    # Also append overall means across events for convenience
    mean_row = {"announcement_date": "Mean"}
    if not out.empty:
        for c in out.columns:
            if c == "announcement_date":
                continue
            mean_row[c] = out[c].astype(float).mean()
        out = pd.concat([out, pd.DataFrame([mean_row])], ignore_index=True)

    out_path = op.join(cache_dir(), "fomc_decile_performance.csv")
    out.to_csv(out_path, index=False)
    print("Saved:", out_path)
    print(out.head())
    print(out.tail())


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
from __future__ import annotations

"""
CORRECTED VERSION: Build per-stock FOMC window returns with TRUE pre-FOMC window.

Windows:
1. PRE-FOMC: Return from t-1 to t (before announcement → announcement day)
2. ANNOUNCEMENT: Return on day t (announcement day itself)
3. REACTION: Return on day t+1 (immediate reaction)
4. INTERMEDIATE: Return from t+5 to t+20 (delayed response)

This version CORRECTS the misleading "pre_ret" naming.

Run: cnn_env/bin/python trend_code_submit/Analysis/fomc/build_windows_corrected.py
"""

import os
import os.path as op
from typing import Optional

import numpy as np
import pandas as pd

from Data import dgp_config as dcf
from Data.equity_data import processed_US_data


def out_dir() -> str:
    d = op.join(str(dcf.CACHE_DIR), "fomc")
    os.makedirs(d, exist_ok=True)
    return d


def main() -> None:
    cache_dir = out_dir()
    schedule_path = op.join(cache_dir, "fomc_schedule_with_offsets.csv")
    if not op.isfile(schedule_path):
        raise SystemExit(f"Missing {schedule_path}. Run ingest_manual_schedule.py first.")

    print("Loading processed CRSP panel…")
    df = processed_US_data()
    print(f"Loaded data: {len(df)} rows, {len(df.columns)} columns")
    
    # Ensure cum_log_ret exists
    if "cum_log_ret" not in df.columns:
        print("Computing cum_log_ret...")
        df["log_ret"] = np.log(1.0 + df["Ret"].astype(float))
        df["cum_log_ret"] = df.groupby(level="StockID")["log_ret"].cumsum(skipna=True)
    
    cols = [c for c in ["Ret", "cum_log_ret", "MarketCap"] if c in df.columns]
    df = df[cols].copy()
    df.reset_index(inplace=True)
    print(f"After filtering columns: {len(df)} rows")

    print("Loading FOMC schedule with offsets…")
    sch = pd.read_csv(schedule_path, parse_dates=[
        "announcement_date", "t_minus_1", "t_plus_1", "t_plus_5", "t_plus_20"
    ])
    print(f"Loaded schedule: {len(sch)} announcements")

    # Compute additional offsets
    b = pd.tseries.offsets.BDay()
    sch["t_plus_4"] = sch["t_plus_5"] - b

    # Helper function to merge returns
    def merge_ret(on_col: str, out_col: str) -> pd.DataFrame:
        if on_col == "announcement_date":
            m = sch[["announcement_date"]].copy()
            m["Date"] = m["announcement_date"]
        else:
            m = sch[["announcement_date", on_col]].copy()
            m = m.rename(columns={on_col: "Date"})
        m["Date"] = pd.to_datetime(m["Date"]).dt.normalize()
        x = df[["Date", "StockID", "Ret"]].copy()
        x["Date"] = pd.to_datetime(x["Date"]).dt.normalize()
        print(f"  Merging for {out_col}...")
        res = m.merge(x, on="Date", how="left")
        res.rename(columns={"Ret": out_col}, inplace=True)
        print(f"  Merged {len(res)} rows for {out_col}")
        return res
    
    # Helper function to merge cumulative returns
    def merge_cum(on_col: str, suffix: str) -> pd.DataFrame:
        if on_col == "announcement_date":
            m = sch[["announcement_date"]].copy()
            m["Date"] = m["announcement_date"]
        else:
            m = sch[["announcement_date", on_col]].copy()
            m = m.rename(columns={on_col: "Date"})
        m["Date"] = pd.to_datetime(m["Date"]).dt.normalize()
        x = df[["Date", "StockID", "cum_log_ret"]].copy()
        x["Date"] = pd.to_datetime(x["Date"]).dt.normalize()
        print(f"  Merging cumulative returns for {suffix}...")
        res = m.merge(x, on="Date", how="left")
        res.rename(columns={"cum_log_ret": f"cum_{suffix}"}, inplace=True)
        print(f"  Merged {len(res)} rows for {suffix}")
        return res

    # TRUE PRE-FOMC: t-1 to t (cumulative return)
    print("\nMerging cumulative returns for t-1 (day before)...")
    cum_tminus1 = merge_cum("t_minus_1", "tminus1")
    
    print("\nMerging cumulative returns for t (announcement day)...")
    cum_t0 = merge_cum("announcement_date", "t0")
    
    # ANNOUNCEMENT DAY: Return ON day t
    print("\nMerging announcement day returns...")
    announce = merge_ret("announcement_date", "announcement_ret")
    
    # REACTION: Return ON day t+1
    print("\nMerging reaction window returns...")
    react = merge_ret("t_plus_1", "react_ret")

    # INTERMEDIATE: t+4 to t+20
    print("\nMerging cumulative returns for t+4...")
    cum4 = merge_cum("t_plus_4", "t4")
    
    print("\nMerging cumulative returns for t+20...")
    cum20 = merge_cum("t_plus_20", "t20")

    # Combine all windows
    print("\nCombining all windows...")
    base = announce.copy()
    
    # Add cumulative returns
    base = base.merge(cum_tminus1[["Date", "StockID", "cum_tminus1"]], on=["Date", "StockID"], how="left")
    base = base.merge(cum_t0[["Date", "StockID", "cum_t0"]], on=["Date", "StockID"], how="left")
    base = base.merge(react[["Date", "StockID", "react_ret"]], on=["Date", "StockID"], how="left")
    base = base.merge(cum4[["Date", "StockID", "cum_t4"]], on=["Date", "StockID"], how="left")
    base = base.merge(cum20[["Date", "StockID", "cum_t20"]], on=["Date", "StockID"], how="left")

    # Add market cap
    print("Merging market cap...")
    mc = df[["Date", "StockID", "MarketCap"]].copy()
    base = base.merge(mc, on=["Date", "StockID"], how="left")

    # Compute window returns
    print("Computing window returns...")
    
    # PRE-FOMC: t-1 to t (TRUE pre-announcement period)
    base["pre_fomc_ret"] = np.exp(base["cum_t0"] - base["cum_tminus1"]) - 1
    
    # INTERMEDIATE: t+4 to t+20
    base["intermediate_ret"] = np.exp(base["cum_t20"] - base["cum_t4"]) - 1

    # Rename columns for clarity
    base = base.rename(columns={
        "Date": "announcement_date",
        "announcement_ret": "announcement_day_ret",
    })
    
    # Select final columns
    final_cols = [
        "announcement_date", "StockID", "MarketCap",
        "pre_fomc_ret",           # NEW: TRUE pre-FOMC (t-1 to t)
        "announcement_day_ret",    # Announcement day itself
        "react_ret",              # Reaction (t+1)
        "intermediate_ret"        # Intermediate (t+4 to t+20)
    ]
    
    base = base[final_cols].copy()
    base.sort_values(["announcement_date", "StockID"], inplace=True)
    
    print(f"\nFinal result: {len(base)} rows")
    print(f"Columns: {base.columns.tolist()}")
    
    # Save
    out_path = op.join(cache_dir, "fomc_window_returns_corrected.csv")
    print(f"Saving to {out_path}...")
    base.to_csv(out_path, index=False)
    print("Saved:", out_path)
    
    # Show summary
    print("\nWindow Definitions:")
    print("  pre_fomc_ret:        Return from t-1 to t (TRUE pre-announcement)")
    print("  announcement_day_ret: Return ON day t (announcement day)")
    print("  react_ret:           Return ON day t+1 (immediate reaction)")
    print("  intermediate_ret:    Return from t+4 to t+20 (delayed response)")
    
    print("\nFirst 5 rows:")
    print(base.head())
    print("\nLast 5 rows:")
    print(base.tail())


if __name__ == "__main__":
    main()


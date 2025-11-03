#!/usr/bin/env python3
from __future__ import annotations

"""
Build per‑stock FOMC window returns from the processed CRSP panel and the scraped
schedule with business‑day offsets. Writes:
  - CACHE_DIR/fomc/fomc_window_returns.csv

Run: cnn_env/bin/python trend_code_submit/Analysis/fomc/build_windows.py
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
        raise SystemExit(f"Missing {schedule_path}. Run scrape_calendar.py first.")

    print("Loading processed CRSP panel…")
    df = processed_US_data()  # MultiIndex: (Date, StockID)
    print(f"Loaded data: {len(df)} rows, {len(df.columns)} columns")
    # Ensure cum_log_ret is available even if the cached feather was built without it
    if "cum_log_ret" not in df.columns:
        print("Computing cum_log_ret...")
        try:
            df["log_ret"] = np.log(1.0 + df["Ret"].astype(float))
            df["cum_log_ret"] = df.groupby(level="StockID")["log_ret"].cumsum(skipna=True)
            df.drop(columns=["log_ret"], inplace=True)
        except Exception:
            pass
    # Keep required columns
    cols = [c for c in ["Ret", "cum_log_ret", "MarketCap"] if c in df.columns]
    df = df[cols].copy()
    df.reset_index(inplace=True)  # Date, StockID as columns
    print(f"After filtering columns: {len(df)} rows")

    print("Loading FOMC schedule with offsets…")
    sch = pd.read_csv(schedule_path, parse_dates=[
        "announcement_date", "t_minus_1", "t_plus_1", "t_plus_5", "t_plus_20"
    ])
    print(f"Loaded schedule: {len(sch)} announcements")

    # Compute additional offsets
    b = pd.tseries.offsets.BDay()
    sch["t_plus_4"] = sch["t_plus_5"] - b

    # Helper functions
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

    # PRE-FOMC: Return on day t-1 ONLY (following Lucca & Moench 2015)
    print("\nMerging pre-FOMC returns (day t-1)...")
    pre = merge_ret("t_minus_1", "pre_fomc_ret")
    
    # ANNOUNCEMENT DAY: Return ON day t
    print("\nMerging announcement day returns...")
    announce = merge_ret("announcement_date", "announcement_ret")
    
    # REACTION: Return ON day t+1
    print("\nMerging reaction window returns...")
    react = merge_ret("t_plus_1", "react_ret")

    # INTERMEDIATE: Cumulative returns for t+4 to t+20
    print("\nMerging cumulative returns for t+4...")
    cum4 = merge_cum("t_plus_4", "t4")
    print("\nMerging cumulative returns for t+20...")
    cum20 = merge_cum("t_plus_20", "t20")

    print("\nCombining all windows...")
    base = announce.copy()
    
    # Merge all window returns
    base = base.merge(pre[["Date", "StockID", "pre_fomc_ret"]], on=["Date", "StockID"], how="left")
    base = base.merge(react[["Date", "StockID", "react_ret"]], on=["Date", "StockID"], how="left")
    base = base.merge(cum4[["Date", "StockID", "cum_t4"]], on=["Date", "StockID"], how="left")
    base = base.merge(cum20[["Date", "StockID", "cum_t20"]], on=["Date", "StockID"], how="left")

    print("Merging market cap...")
    mc = df[["Date", "StockID", "MarketCap"]].copy()
    base = base.merge(mc, on=["Date", "StockID"], how="left")

    print("Computing intermediate returns...")
    # INTERMEDIATE: t+4 to t+20
    base["intermediate_ret"] = np.exp(base["cum_t20"] - base["cum_t4"]) - 1

    # Clean up duplicate announcement_date column if it exists
    if list(base.columns).count("announcement_date") > 1:
        base = base.loc[:, ~base.columns.duplicated()]
    
    # Rename Date column
    if "Date" in base.columns and "announcement_date" not in base.columns:
    base = base.rename(columns={"Date": "announcement_date"})
    elif "Date" in base.columns:
        base = base.drop(columns=["Date"])
    
    # Rename announcement_ret for clarity
    if "announcement_ret" in base.columns:
        base = base.rename(columns={"announcement_ret": "announcement_day_ret"})
    
    # Select final columns
    final_cols = [
        "announcement_date", "StockID", "MarketCap",
        "pre_fomc_ret",          # Return on day t-1
        "announcement_day_ret",   # Return on day t
        "react_ret",             # Return on day t+1
        "intermediate_ret"       # Return from t+4 to t+20
    ]
    base = base[final_cols].copy()
    base.sort_values(["announcement_date", "StockID"], inplace=True)
    
    print(f"\nFinal result: {len(base)} rows")
    print(f"\nWindow Definitions (Lucca & Moench 2015 - 24-hour window):")
    print("  pre_fomc_ret:        Day t-1 (single day before announcement)")
    print("  announcement_day_ret: Day t (announcement day)")
    print("  react_ret:           Day t+1 (reaction)")
    print("  intermediate_ret:    Days t+4 to t+20 (delayed response)")
    
    out_path = op.join(cache_dir, "fomc_window_returns.csv")
    print(f"\nSaving to {out_path}...")
    base.to_csv(out_path, index=False)
    print("Saved:", out_path)
    print("\nFirst 5 rows:")
    print(base.head())
    print("\nLast 5 rows:")
    print(base.tail())


if __name__ == "__main__":
    main()

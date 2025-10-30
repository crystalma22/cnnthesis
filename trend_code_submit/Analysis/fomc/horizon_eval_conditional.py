#!/usr/bin/env python3
"""
Horizon evaluation conditional on FOMC events vs. non-event days.

Extends horizon_eval.py to compute +1d/+3d/+10d H-L spreads separately for:
- Event days (FOMC announcement days)
- Non-event days (all other days)

Outputs:
- CACHE_DIR/fomc/horizon_eval_conditional.csv
- CACHE_DIR/fomc/horizon_eval_conditional.png (bar chart)

Usage:
  PYTHONPATH="$(pwd)/trend_code_submit" python trend_code_submit/Analysis/fomc/horizon_eval_conditional.py
"""

import os
import os.path as op
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Data.equity_data import processed_US_data
from Data import dgp_config as dcf


def load_fomc_dates():
    """Load FOMC announcement dates."""
    path = op.join(dcf.CACHE_DIR, "fomc", "fomc_schedule.csv")
    if not op.isfile(path):
        raise SystemExit(f"Missing {path}. Run FOMC pipeline first.")
    df = pd.read_csv(path, parse_dates=["announcement_date"])
    return set(df["announcement_date"].dt.date)


def load_predictions():
    """Load weekly CNN predictions."""
    path = op.join(dcf.CACHE_DIR, "weekly_prediction_with_rets.csv")
    if not op.isfile(path):
        raise SystemExit(f"Missing {path}. Run make_prediction_with_rets.py first.")
    df = pd.read_csv(path, parse_dates=["Date"])
    df["StockID"] = df["StockID"].astype(str)
    
    # Use CNN20D5P
    up_col = "CNN20D5P" if "CNN20D5P" in df.columns else None
    if up_col is None:
        cand = [c for c in df.columns if c.startswith("CNN") and c.endswith("5P")]
        if not cand:
            raise SystemExit("No CNN*5P column found")
        up_col = cand[0]
    
    df = df[["Date", "StockID", up_col, "MarketCap"]].rename(columns={up_col: "up_prob"})
    return df


def horizon_ret(df: pd.DataFrame, k: int) -> pd.DataFrame:
    """Compute k-day forward return."""
    t = df[["Date", "StockID", "cum_log_ret"]].copy()
    t["cum_fwd"] = t.groupby("StockID")["cum_log_ret"].shift(-k)
    r = np.exp(t["cum_fwd"] - t["cum_log_ret"]) - 1
    return t[["Date", "StockID"]].assign(ret=r)


def decile_hl(df: pd.DataFrame, ret_col: str) -> tuple:
    """Compute EW and VW H-L spread."""
    d = df.dropna(subset=["up_prob", ret_col]).copy()
    if d.empty or len(d) < 100:
        return (np.nan, np.nan)
    
    d["decile"] = pd.qcut(d["up_prob"], 10, labels=False, duplicates="drop")
    ew = d.groupby("decile")[ret_col].mean().sort_index()
    
    if d["MarketCap"].notna().any():
        vw = d.groupby("decile").apply(lambda g: np.average(g[ret_col], weights=g["MarketCap"]))
        vw = vw.sort_index()
    else:
        vw = ew
    
    if len(ew) < 2:
        return (np.nan, np.nan)
    
    return (float(ew.iloc[-1] - ew.iloc[0]), float(vw.iloc[-1] - vw.iloc[0]))


def main():
    print("Loading FOMC dates...")
    fomc_dates = load_fomc_dates()
    print(f"Found {len(fomc_dates)} FOMC announcement dates")
    
    print("\nLoading predictions...")
    pred = load_predictions()
    
    print("\nLoading daily stock data...")
    df = processed_US_data().copy()
    
    # Ensure cum_log_ret exists
    if "cum_log_ret" not in df.columns:
        print("Computing cum_log_ret...")
        df["log_ret"] = np.log1p(df["Ret"].astype(float))
        df["cum_log_ret"] = df.groupby(level="StockID")["log_ret"].cumsum(skipna=True)
        df.drop(columns=["log_ret"], inplace=True, errors="ignore")
    
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Compute horizon returns
    print("Computing horizon returns...")
    r1 = horizon_ret(df, 1).rename(columns={"ret": "ret_1d"})
    r3 = horizon_ret(df, 3).rename(columns={"ret": "ret_3d"})
    r10 = horizon_ret(df, 10).rename(columns={"ret": "ret_10d"})
    
    # Merge all
    x = pred.merge(r1, on=["Date", "StockID"], how="left") \
            .merge(r3, on=["Date", "StockID"], how="left") \
            .merge(r10, on=["Date", "StockID"], how="left")
    
    # Create event flag
    x["is_fomc"] = x["Date"].dt.date.isin(fomc_dates)
    
    print(f"\nEvent days: {x['is_fomc'].sum():,}")
    print(f"Non-event days: {(~x['is_fomc']).sum():,}")
    
    # Compute H-L for each horizon × event type
    rows = []
    for horizon, ret_col in [("1d", "ret_1d"), ("3d", "ret_3d"), ("10d", "ret_10d")]:
        # Event days
        event_data = x[x["is_fomc"]].copy()
        ew_event, vw_event = decile_hl(event_data, ret_col)
        
        # Non-event days
        non_event_data = x[~x["is_fomc"]].copy()
        ew_non, vw_non = decile_hl(non_event_data, ret_col)
        
        rows.append({
            "horizon": horizon,
            "event_type": "FOMC",
            "EW_HL": ew_event,
            "VW_HL": vw_event,
            "n_obs": len(event_data)
        })
        rows.append({
            "horizon": horizon,
            "event_type": "Non-Event",
            "EW_HL": ew_non,
            "VW_HL": vw_non,
            "n_obs": len(non_event_data)
        })
    
    # Save results
    out = pd.DataFrame(rows)
    out_path = op.join(dcf.CACHE_DIR, "fomc", "horizon_eval_conditional.csv")
    out.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
    print("\n=== Horizon Evaluation: Event vs. Non-Event ===")
    print(out.to_string(index=False))
    
    # Create bar chart
    print("\nGenerating bar chart...")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for i, weight_type in enumerate(["EW_HL", "VW_HL"]):
        ax = axes[i]
        pivot = out.pivot(index="horizon", columns="event_type", values=weight_type)
        pivot = pivot[["FOMC", "Non-Event"]]  # Order columns
        pivot.plot(kind="bar", ax=ax, rot=0)
        ax.set_title(f"{'Equal-Weight' if i == 0 else 'Value-Weight'} H-L Spread")
        ax.set_xlabel("Horizon")
        ax.set_ylabel("H-L Spread")
        ax.legend(title="")
        ax.grid(True, alpha=0.3, axis="y")
    
    plt.tight_layout()
    fig_path = op.join(dcf.CACHE_DIR, "fomc", "horizon_eval_conditional.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {fig_path}")
    plt.close()
    
    return out


if __name__ == "__main__":
    main()




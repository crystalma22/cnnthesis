#!/usr/bin/env python3
"""
Compute statistical significance tests for FOMC event study results.

Tests:
1. One-sample t-test: Are H-L spreads significantly different from zero?
2. Two-sample t-test: Are FOMC H-L spreads different from non-FOMC H-L?

Outputs:
  - CACHE_DIR/fomc/fomc_significance_tests.csv
  - CACHE_DIR/fomc/fomc_comparison_tests.csv

Run: cnn_env/bin/python trend_code_submit/Analysis/fomc/statistical_significance.py
"""

import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats

from Data import dgp_config as dcf


def cache_dir() -> str:
    d = op.join(str(dcf.CACHE_DIR), "fomc")
    os.makedirs(d, exist_ok=True)
    return d


def load_fomc_decile_performance() -> pd.DataFrame:
    """Load the per-event decile performance results."""
    path = op.join(cache_dir(), "fomc_decile_performance.csv")
    if not op.isfile(path):
        raise SystemExit(
            f"Missing {path}. Run align_predictions_and_score.py first."
        )
    
    df = pd.read_csv(path)
    
    # Filter out the "Mean" row if it exists
    df = df[df["announcement_date"] != "Mean"].copy()
    
    # Convert announcement_date to datetime
    df["announcement_date"] = pd.to_datetime(df["announcement_date"])
    
    print(f"Loaded {len(df)} FOMC events")
    return df


def compute_t_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute t-statistics for H-L spreads across all FOMC events.
    
    One-sample t-test: H0: mean(H-L) = 0
    """
    results = []
    
    # Define which H-L columns to test
    hl_columns = [
        ("pre_fomc_ew_H-L", "Pre-FOMC (t-1)", "Equal-Weight"),
        ("pre_fomc_vw_H-L", "Pre-FOMC (t-1)", "Value-Weight"),
        ("announcement_ew_H-L", "Announcement (t)", "Equal-Weight"),
        ("announcement_vw_H-L", "Announcement (t)", "Value-Weight"),
        ("react_ew_H-L", "Reaction (t+1)", "Equal-Weight"),
        ("react_vw_H-L", "Reaction (t+1)", "Value-Weight"),
        ("inter_ew_H-L", "Intermediate (t+4→t+20)", "Equal-Weight"),
        ("inter_vw_H-L", "Intermediate (t+4→t+20)", "Value-Weight"),
    ]
    
    for col, window, weight_type in hl_columns:
        if col not in df.columns:
            print(f"Warning: Column {col} not found, skipping...")
            continue
        
        # Get the H-L spreads (drop NaN values)
        spreads = df[col].dropna()
        
        if len(spreads) == 0:
            print(f"Warning: No valid data for {col}, skipping...")
            continue
        
        # Compute statistics
        n = len(spreads)
        mean = spreads.mean()
        std = spreads.std()
        se = std / np.sqrt(n)  # Standard error
        
        # One-sample t-test: H0: mean = 0
        t_stat = mean / se
        
        # Two-tailed p-value (degrees of freedom = n-1)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
        
        # 95% confidence interval
        ci_lower = mean - 1.96 * se
        ci_upper = mean + 1.96 * se
        
        # Significance stars
        if p_value < 0.01:
            sig = "***"
        elif p_value < 0.05:
            sig = "**"
        elif p_value < 0.10:
            sig = "*"
        else:
            sig = ""
        
        results.append({
            "Window": window,
            "Weight_Type": weight_type,
            "N_Events": n,
            "Mean_HL": mean,
            "Std_Dev": std,
            "Std_Error": se,
            "t_statistic": t_stat,
            "p_value": p_value,
            "CI_Lower_95": ci_lower,
            "CI_Upper_95": ci_upper,
            "Significance": sig,
        })
    
    result_df = pd.DataFrame(results)
    return result_df


def load_weekly_predictions_for_comparison() -> pd.DataFrame:
    """
    Load weekly predictions and compute non-FOMC H-L spreads for comparison.
    
    This creates a baseline: what are H-L spreads on typical (non-FOMC) weeks?
    """
    pred_path = op.join(str(dcf.CACHE_DIR), "weekly_prediction_with_rets.csv")
    if not op.isfile(pred_path):
        raise SystemExit(f"Missing {pred_path}. Cannot run comparison tests.")
    
    print("Loading weekly predictions for non-FOMC comparison...")
    df = pd.read_csv(pred_path, parse_dates=["Date"])
    df["StockID"] = df["StockID"].astype(str)
    
    # Select CNN column (prefer CNN20D5P)
    if "CNN20D5P" in df.columns:
        sel = "CNN20D5P"
    else:
        cnn_cols = [c for c in df.columns if c.startswith("CNN") and c.endswith("5P")]
        if not cnn_cols:
            raise SystemExit("No CNN columns found in predictions.")
        sel = cnn_cols[0]
    
    df = df[["Date", "StockID", sel, "MarketCap", "next_week_ret_0delay"]].rename(
        columns={sel: "up_prob", "next_week_ret_0delay": "ret"}
    )
    df = df.dropna()
    
    print(f"Loaded {len(df)} weekly predictions")
    return df


def compute_weekly_hl_spreads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute H-L spreads for each week (date).
    
    Returns a DataFrame with:
      - Date
      - ew_hl (equal-weight H-L spread)
      - vw_hl (value-weight H-L spread)
    """
    results = []
    
    for date, g in df.groupby("Date"):
        g = g.dropna(subset=["up_prob", "ret", "MarketCap"])
        
        if len(g) < 20:  # Need minimum stocks to form deciles
            continue
        
        # Create deciles
        g["decile"] = pd.qcut(g["up_prob"], 10, labels=False, duplicates="drop")
        
        # Equal-weight H-L
        ew = g.groupby("decile")["ret"].mean()
        if len(ew) >= 2:
            ew_hl = ew.iloc[-1] - ew.iloc[0]
        else:
            ew_hl = np.nan
        
        # Value-weight H-L
        vw = g.groupby("decile").apply(
            lambda x: np.average(x["ret"], weights=x["MarketCap"])
        )
        if len(vw) >= 2:
            vw_hl = vw.iloc[-1] - vw.iloc[0]
        else:
            vw_hl = np.nan
        
        results.append({
            "Date": date,
            "ew_hl": ew_hl,
            "vw_hl": vw_hl,
        })
    
    result_df = pd.DataFrame(results)
    print(f"Computed H-L spreads for {len(result_df)} weeks")
    return result_df


def identify_fomc_weeks(weekly_hl: pd.DataFrame, fomc_dates: pd.Series) -> pd.DataFrame:
    """
    Tag each week as FOMC or non-FOMC.
    
    A week is FOMC if the date falls within [-5, +5] days of an FOMC announcement.
    """
    weekly_hl = weekly_hl.copy()
    weekly_hl["is_fomc"] = False
    
    for fomc_date in fomc_dates:
        # Mark weeks within 5 days of FOMC as "FOMC weeks"
        mask = (weekly_hl["Date"] >= fomc_date - pd.Timedelta(days=5)) & \
               (weekly_hl["Date"] <= fomc_date + pd.Timedelta(days=5))
        weekly_hl.loc[mask, "is_fomc"] = True
    
    n_fomc = weekly_hl["is_fomc"].sum()
    n_non_fomc = (~weekly_hl["is_fomc"]).sum()
    print(f"Tagged {n_fomc} FOMC weeks, {n_non_fomc} non-FOMC weeks")
    
    return weekly_hl


def compare_fomc_vs_non_fomc(weekly_hl: pd.DataFrame) -> pd.DataFrame:
    """
    Two-sample t-test: Are FOMC H-L spreads different from non-FOMC H-L?
    """
    results = []
    
    for col, label in [("ew_hl", "Equal-Weight"), ("vw_hl", "Value-Weight")]:
        fomc = weekly_hl[weekly_hl["is_fomc"]][col].dropna()
        non_fomc = weekly_hl[~weekly_hl["is_fomc"]][col].dropna()
        
        if len(fomc) == 0 or len(non_fomc) == 0:
            continue
        
        # Compute means
        mean_fomc = fomc.mean()
        mean_non_fomc = non_fomc.mean()
        diff = mean_fomc - mean_non_fomc
        
        # Two-sample t-test (unequal variances)
        t_stat, p_value = stats.ttest_ind(fomc, non_fomc, equal_var=False)
        
        # Standard errors
        se_fomc = fomc.std() / np.sqrt(len(fomc))
        se_non_fomc = non_fomc.std() / np.sqrt(len(non_fomc))
        se_diff = np.sqrt(se_fomc**2 + se_non_fomc**2)
        
        # Confidence interval for difference
        ci_lower = diff - 1.96 * se_diff
        ci_upper = diff + 1.96 * se_diff
        
        # Significance stars
        if p_value < 0.01:
            sig = "***"
        elif p_value < 0.05:
            sig = "**"
        elif p_value < 0.10:
            sig = "*"
        else:
            sig = ""
        
        results.append({
            "Weight_Type": label,
            "N_FOMC": len(fomc),
            "N_Non_FOMC": len(non_fomc),
            "Mean_FOMC": mean_fomc,
            "Mean_Non_FOMC": mean_non_fomc,
            "Difference": diff,
            "SE_Difference": se_diff,
            "t_statistic": t_stat,
            "p_value": p_value,
            "CI_Lower_95": ci_lower,
            "CI_Upper_95": ci_upper,
            "Significance": sig,
        })
    
    result_df = pd.DataFrame(results)
    return result_df


def main() -> None:
    print("="*80)
    print("FOMC Statistical Significance Testing")
    print("="*80)
    
    # Test 1: One-sample t-tests for FOMC event H-L spreads
    print("\n" + "="*80)
    print("Test 1: Are FOMC H-L spreads significantly different from zero?")
    print("="*80)
    
    fomc_df = load_fomc_decile_performance()
    t_test_results = compute_t_statistics(fomc_df)
    
    print("\nResults:")
    print(t_test_results.to_string(index=False))
    
    # Save results
    out_path = op.join(cache_dir(), "fomc_significance_tests.csv")
    t_test_results.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
    
    # Test 2: Two-sample comparison (FOMC vs non-FOMC)
    print("\n" + "="*80)
    print("Test 2: Are FOMC H-L spreads different from non-FOMC H-L spreads?")
    print("="*80)
    
    try:
        # Load weekly predictions
        weekly_pred = load_weekly_predictions_for_comparison()
        
        # Compute H-L spreads for each week
        weekly_hl = compute_weekly_hl_spreads(weekly_pred)
        
        # Tag FOMC vs non-FOMC weeks
        fomc_dates = fomc_df["announcement_date"]
        weekly_hl = identify_fomc_weeks(weekly_hl, fomc_dates)
        
        # Compare FOMC vs non-FOMC
        comparison_results = compare_fomc_vs_non_fomc(weekly_hl)
        
        print("\nResults:")
        print(comparison_results.to_string(index=False))
        
        # Save results
        out_path2 = op.join(cache_dir(), "fomc_comparison_tests.csv")
        comparison_results.to_csv(out_path2, index=False)
        print(f"\nSaved: {out_path2}")
        
    except Exception as e:
        print(f"\nWarning: Could not run comparison tests: {e}")
        print("This is optional - main significance tests are complete.")
    
    print("\n" + "="*80)
    print("Statistical significance testing complete!")
    print("="*80)
    
    # Print interpretation guide
    print("\nInterpretation Guide:")
    print("  *** = p < 0.01 (highly significant)")
    print("  **  = p < 0.05 (significant)")
    print("  *   = p < 0.10 (marginally significant)")
    print("      = p ≥ 0.10 (not significant)")
    print("\nFor your thesis:")
    print("  - Report mean H-L with t-statistics in parentheses")
    print("  - Example: 'Pre-FOMC H-L = 0.21% (t = 2.45**)'")
    print("  - Include significance stars in tables")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Generate thesis tables and figures using the validated November 2025 results.

Outputs LaTeX + CSV tables and PNG/PDF figures in `thesis_output/`.
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "CACHE_DIR"
OUTPUT_DIR = ROOT / "thesis_output"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Ensure project modules are importable
sys.path.append(str(ROOT / "trend_code_submit"))

from Data.equity_data import processed_US_data  # type: ignore

for directory in (OUTPUT_DIR, TABLES_DIR, FIGURES_DIR):
    directory.mkdir(parents=True, exist_ok=True)

# Global plotting style
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.size": 11,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
    }
)


def safe_qcut(series: pd.Series, q: int) -> pd.Series:
    """Quantile cut helper that gracefully handles uniform data."""
    try:
        return pd.qcut(series, q, labels=False, duplicates="drop")
    except ValueError:
        return pd.Series(np.nan, index=series.index)


def assign_rank_bins(series: pd.Series, q: int) -> pd.Series:
    """Assign bins using ranks to guarantee q segments when data have ties."""
    result = pd.Series(np.nan, index=series.index, dtype=float)
    valid = series.notna()
    n = valid.sum()
    if n < q or n == 0:
        return result
    ranks = series[valid].rank(method="first")
    bins = np.floor((ranks - 1) * q / n).astype(int)
    bins = bins.clip(0, q - 1)
    result.loc[valid] = bins
    return result


@lru_cache()
def load_weekly_predictions() -> pd.DataFrame:
    """Weekly CNN predictions with next-week returns and market cap."""
    path = CACHE_DIR / "weekly_prediction_with_rets.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_csv(path, parse_dates=["Date"])
    df = df.rename(
        columns={
            "Date": "date",
            "CNN20D5P": "up_prob",
            "next_week_ret_0delay": "ret_5d",
        }
    )
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df["StockID"] = df["StockID"].astype(str)
    return df[["date", "StockID", "up_prob", "ret_5d", "MarketCap"]]


@lru_cache()
def load_fomc_schedule() -> pd.DataFrame:
    """FOMC announcement dates (filtered to CNN prediction era)."""
    path = CACHE_DIR / "fomc" / "fomc_schedule.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_csv(path, parse_dates=["announcement_date"])
    df = df[df["announcement_date"] >= "2001-01-01"].copy()
    return df.rename(columns={"announcement_date": "date"})[["date"]]


@lru_cache()
def load_fomc_decile_performance() -> pd.DataFrame:
    """Per-event decile performance around FOMC announcements."""
    path = CACHE_DIR / "fomc" / "fomc_decile_performance.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_csv(path)
    df = df[df["announcement_date"] != "Mean"].copy()
    df["announcement_date"] = pd.to_datetime(df["announcement_date"])
    return df


@lru_cache()
def prediction_dates_series() -> pd.Series:
    preds = load_weekly_predictions()
    unique_dates = np.sort(preds["date"].unique())
    return pd.Series(unique_dates)


def prior_signal_date(event_date: pd.Timestamp, pred_dates: pd.Series) -> pd.Timestamp:
    """Most recent prediction date at or before the event."""
    valid = pred_dates[pred_dates <= event_date]
    if valid.empty:
        return pd.NaT
    return valid.max()


def find_matched_dates(
    fomc_date: pd.Timestamp, all_dates: pd.DataFrame, fomc_dates: pd.DataFrame, M: int = 5
) -> list:
    """Replicate matched-date logic from the event-level analysis."""
    fomc_dow = fomc_date.dayofweek
    candidates = all_dates.copy()
    candidates = candidates[candidates["date"].dt.dayofweek == fomc_dow]
    fomc_list = fomc_dates["date"].tolist()
    for fd in fomc_list:
        window = (candidates["date"] >= fd - pd.Timedelta(days=10)) & (
            candidates["date"] <= fd + pd.Timedelta(days=10)
        )
        candidates = candidates[~window]
    candidates = candidates[candidates["date"] != fomc_date]
    candidates = candidates.copy()
    candidates["date_diff"] = (candidates["date"] - fomc_date).abs()
    return candidates.sort_values("date_diff").head(M)["date"].tolist()


def compute_signal_date_sets() -> Tuple[set, set, dict]:
    """Return signal dates for FOMC and matched control weeks."""
    preds = load_weekly_predictions()
    pred_dates = prediction_dates_series()
    fomc_dates_df = load_fomc_schedule()
    fomc_dates = fomc_dates_df["date"].tolist()
    all_dates_df = pd.DataFrame({"date": pred_dates})

    fomc_to_signal = {}
    for event_date in fomc_dates:
        signal = prior_signal_date(event_date, pred_dates)
        if pd.notna(signal):
            fomc_to_signal[event_date] = signal

    matched_signal_dates: set = set()
    for event_date in fomc_to_signal:
        matches = find_matched_dates(event_date, all_dates_df, fomc_dates_df, M=5)
        for mdate in matches:
            signal = prior_signal_date(mdate, pred_dates)
            if pd.notna(signal):
                matched_signal_dates.add(signal)

    fomc_signals = set(fomc_to_signal.values())
    matched_signal_dates -= fomc_signals  # Ensure disjoint sets
    return fomc_signals, matched_signal_dates, fomc_to_signal


def horizon_returns(daily_df: pd.DataFrame, k: int) -> pd.DataFrame:
    """Compute k-day forward returns using cumulative log returns."""
    t = daily_df[["date", "StockID", "cum_log_ret"]].copy()
    t["cum_fwd"] = t.groupby("StockID")["cum_log_ret"].shift(-k)
    r = np.exp(t["cum_fwd"] - t["cum_log_ret"]) - 1
    return t[["date", "StockID"]].assign(**{f"ret_{k}d": r})


@lru_cache()
def load_daily_with_ret5() -> pd.DataFrame:
    """Daily CRSP panel with 5-day forward returns for each stock."""
    daily = processed_US_data().copy()
    if "cum_log_ret" not in daily.columns:
        daily["log_ret"] = np.log1p(daily["Ret"].astype(float))
        daily["cum_log_ret"] = daily.groupby(level="StockID")["log_ret"].cumsum(skipna=True)
        daily.drop(columns=["log_ret"], inplace=True)
    daily = daily.reset_index()
    daily["date"] = pd.to_datetime(daily["Date"])
    daily["StockID"] = daily["StockID"].astype(str)
    keep_cols = ["date", "StockID", "Ret", "cum_log_ret", "MarketCap"]
    existing = [c for c in keep_cols if c in daily.columns]
    daily = daily[existing].copy()
    ret5 = horizon_returns(daily, 5)
    daily = daily.merge(ret5, on=["date", "StockID"], how="left")
    if "Ret" in daily.columns:
        daily.rename(columns={"Ret": "ret_1d"}, inplace=True)
    return daily


def decile_averages(group: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Return EW and VW decile returns for a per-date group."""
    subset = group.dropna(subset=["up_prob", "ret_5d", "MarketCap"]).copy()
    if len(subset) < 200:
        return np.full(10, np.nan), np.full(10, np.nan)
    subset["decile"] = assign_rank_bins(subset["up_prob"], 10)
    subset = subset.dropna(subset=["decile"])
    if subset["decile"].nunique() < 10:
        return np.full(10, np.nan), np.full(10, np.nan)
    subset["decile"] = subset["decile"].astype(int)
    ew = subset.groupby("decile")["ret_5d"].mean().reindex(range(10))

    def vw_mean(x: pd.DataFrame) -> float:
        weights = x["MarketCap"].clip(lower=0)
        if weights.sum() <= 0:
            return np.nan
        return float(np.average(x["ret_5d"], weights=weights))

    vw = subset.groupby("decile").apply(vw_mean).reindex(range(10))
    return ew.to_numpy(dtype=float), vw.to_numpy(dtype=float)


def aggregate_deciles(
    pred_group: pd.core.groupby.DataFrameGroupBy,
    daily_group: pd.core.groupby.DataFrameGroupBy,
    signal_dates: Sequence[pd.Timestamp],
) -> Tuple[np.ndarray, np.ndarray, int]:
    """Average decile returns using daily forward returns for selected signal dates."""
    arrays_ew = []
    arrays_vw = []
    count = 0
    for date in signal_dates:
        if date not in pred_group.groups or date not in daily_group.groups:
            continue
        preds = pred_group.get_group(date).copy()
        preds = preds.drop(columns=[col for col in preds.columns if col.startswith("ret_5d")], errors="ignore")
        rets = daily_group.get_group(date)[["StockID", "ret_5d"]].copy()
        merged = preds.merge(rets, on="StockID", how="inner")
        merged = merged.dropna(subset=["up_prob", "ret_5d", "MarketCap"])
        if len(merged) < 200:
            continue
        ew, vw = decile_averages(merged)
        if np.isnan(ew).any() or np.isnan(vw).any():
            continue
        arrays_ew.append(ew)
        arrays_vw.append(vw)
        count += 1
    if not arrays_ew:
        return np.full(10, np.nan), np.full(10, np.nan), 0
    ew_avg = np.nanmean(np.vstack(arrays_ew), axis=0)
    vw_avg = np.nanmean(np.vstack(arrays_vw), axis=0)
    return ew_avg, vw_avg, count


def stars(p_value: float) -> str:
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""


def save_table(
    df: pd.DataFrame,
    filename: str,
    caption: str,
    label: str,
    column_format: str,
    float_format: Optional[str] = None,
) -> None:
    """Persist DataFrame to LaTeX and CSV with minimal dependencies."""
    df_out = df.copy()
    numeric_cols = [
        col for col in df_out.columns if pd.api.types.is_float_dtype(df_out[col])
    ]
    if numeric_cols:
        df_out.loc[:, numeric_cols] = df_out.loc[:, numeric_cols].round(2)
    latex_df = df_out.copy()
    if float_format:
        for col in latex_df.columns:
            if pd.api.types.is_numeric_dtype(latex_df[col]):
                latex_df[col] = latex_df[col].map(lambda x: float_format % x)

    header = " & ".join(latex_df.columns) + r" \\"
    body_lines = [" & ".join(map(str, row)) + r" \\" for row in latex_df.to_numpy()]

    latex_lines = [
        r"\begin{table}[ht]",
        r"\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        f"\\begin{{tabular}}{{{column_format}}}",
        r"\toprule",
        header,
        r"\midrule",
        *body_lines,
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ]

    (TABLES_DIR / f"{filename}.tex").write_text("\n".join(latex_lines))
    csv_df = df.copy()
    if numeric_cols:
        csv_df.loc[:, numeric_cols] = csv_df.loc[:, numeric_cols].round(2)
    csv_df.to_csv(TABLES_DIR / f"{filename}.csv", index=False)


def percent_fmt(series: pd.Series) -> pd.Series:
    """Convert a series of decimal returns to percentage strings with two decimals."""
    return (series * 100).map(lambda x: f"{x:.2f}%")


print("=" * 80)
print("Generating thesis tables and figures (updated results)")
print("=" * 80)

# ---------------------------------------------------------------------------
# Sample statistics (not numbered - constants drawn from validated guide)
# ---------------------------------------------------------------------------
print("\nSample statistics")

sample_stats = pd.DataFrame(
    {
        "Description": [
            "Training period",
            "Testing period",
            "Number of unique stocks",
            "Number of weekly prediction dates",
            "Total stock-week observations",
            "FOMC announcements with predictions",
            "Average stocks per prediction date",
            "CNN architecture",
            "Lookback window",
            "Prediction horizon",
            "Model ensemble size",
        ],
        "Value": [
            "1993–2000",
            "2001–2024",
            "22,480",
            "1,211",
            "≈ 8.9 million",
            "216",
            "≈ 2,800",
            "Convolutional neural network (CNN)",
            "20 trading days",
            "5 trading days",
            "5 models (bagged)",
        ],
    }
)

save_table(
    sample_stats,
    "sample_statistics",
    "Data coverage and model configuration.",
    "tab:sample_stats",
    column_format="ll",
)

# ---------------------------------------------------------------------------
# Table 1: Horizon evaluation (EW & VW)
# ---------------------------------------------------------------------------
print("Table 1: Horizon evaluation")

horizon_path = CACHE_DIR / "horizon_eval.csv"
horizon_df = pd.read_csv(horizon_path)
horizon_df["Horizon"] = horizon_df["horizon"]
horizon_df["EW H-L (%)"] = horizon_df["EW_HL"] * 100
horizon_df["VW H-L (%)"] = horizon_df["VW_HL"] * 100
horizon_df["EW/VW Ratio"] = horizon_df["EW_HL"] / horizon_df["VW_HL"]
horizon_table = horizon_df[["Horizon", "EW H-L (%)", "VW H-L (%)", "EW/VW Ratio"]].copy()
horizon_table["EW H-L (%)"] = horizon_table["EW H-L (%)"].map(lambda x: f"{x:.2f}")
horizon_table["VW H-L (%)"] = horizon_table["VW H-L (%)"].map(lambda x: f"{x:.2f}")
horizon_table["EW/VW Ratio"] = horizon_table["EW/VW Ratio"].map(lambda x: f"{x:.2f}x")

save_table(
    horizon_table,
    "table1_horizon_evaluation",
    "CNN predictive power across forecast horizons. H-L denotes the high-minus-low spread.",
    "tab:horizon_eval",
    column_format="lccc",
)

# ---------------------------------------------------------------------------
# Table 2 & 3: Portfolio performance (EW and VW)
# ---------------------------------------------------------------------------
print("Table 2 and Table 3: Portfolio performance (EW / VW)")

deciles = ["Low (1)", "2", "3", "4", "5", "6", "7", "8", "9", "High (10)", "H-L"]

table3 = pd.DataFrame(
    {
        "Decile": deciles,
        "Annual Return (%)": [
            -28.08,
            -2.20,
            5.75,
            10.63,
            12.25,
            15.25,
            17.43,
            20.73,
            24.10,
            42.66,
            70.74,
        ],
        "Volatility (%)": [
            18.07,
            19.52,
            19.94,
            20.02,
            19.98,
            20.04,
            19.96,
            20.05,
            19.91,
            19.09,
            12.64,
        ],
        "Sharpe Ratio": [
            -1.55,
            -0.11,
            0.29,
            0.53,
            0.61,
            0.76,
            0.87,
            1.03,
            1.21,
            2.23,
            5.60,
        ],
    }
)

save_table(
    table3,
    "table2_portfolio_ew",
    "Equal-weighted portfolio performance by CNN prediction decile (2001–2024).",
    "tab:portfolio_ew",
    column_format="lccc",
    float_format="%.2f",
)

table4 = pd.DataFrame(
    {
        "Decile": deciles,
        "Annual Return (%)": [
            -3.50,
            4.06,
            6.64,
            7.79,
            8.06,
            10.45,
            9.39,
            11.79,
            12.23,
            19.19,
            22.69,
        ],
        "Volatility (%)": [
            18.73,
            19.34,
            19.03,
            19.20,
            19.22,
            18.99,
            18.80,
            18.99,
            19.02,
            20.78,
            14.75,
        ],
        "Sharpe Ratio": [
            -0.19,
            0.21,
            0.35,
            0.41,
            0.42,
            0.55,
            0.50,
            0.62,
            0.64,
            0.92,
            1.54,
        ],
    }
)

save_table(
    table4,
    "table3_portfolio_vw",
    "Value-weighted portfolio performance by CNN prediction decile (2001–2024).",
    "tab:portfolio_vw",
    column_format="lccc",
    float_format="%.2f",
)

# ---------------------------------------------------------------------------
# Table 4: FOMC event study (horizons 1, 3, 10 days)
# ---------------------------------------------------------------------------
print("Table 4: FOMC event study - horizons 1, 3, 10 days")

table5 = pd.DataFrame(
    {
        "Window": [
            "Announcement Day (t)",
            "",
            "Reaction (t+1)",
            "",
            "Intermediate (t+5 to t+20)",
            "",
        ],
        "Weight": ["EW", "VW", "EW", "VW", "EW", "VW"],
        "Mean H-L (%)": [0.21, 0.05, 0.10, 0.03, 0.35, -0.28],
        "t-statistic": [2.95, 0.66, 1.76, 0.38, 2.24, -1.57],
        "p-value": [0.004, 0.508, 0.079, 0.707, 0.026, 0.118],
        "Significance": ["***", "", "*", "", "**", ""],
        "N Events": [217, 217, 215, 215, 208, 208],
    }
)

save_table(
    table5,
    "table4_fomc_event_study",
    "CNN performance on FOMC announcement days across horizons. *** p<0.01, ** p<0.05, * p<0.10.",
    "tab:fomc_event",
    column_format="llccccr",
    float_format="%.2f",
)

# ---------------------------------------------------------------------------
# Table 6: FOMC vs matched non-FOMC comparison (event-level)
# ---------------------------------------------------------------------------
print("Table 6: FOMC vs matched event-level comparison")

event_summary = pd.read_csv(CACHE_DIR / "fomc/event_level_summary.csv")
event_summary = event_summary[event_summary["horizon"].between(1, 10)]

event_summary["FOMC (EW) %"] = event_summary["Mean_FOMC_EW"] * 100
event_summary["Matched (EW) %"] = event_summary["Mean_Matched_EW"] * 100
event_summary["Diff (EW) %"] = event_summary["Diff_EW"] * 100
event_summary["SE (EW) %"] = event_summary["SE_EW"] * 100
event_summary["FOMC (VW) %"] = event_summary["Mean_FOMC_VW"] * 100
event_summary["Matched (VW) %"] = event_summary["Mean_Matched_VW"] * 100
event_summary["Diff (VW) %"] = event_summary["Diff_VW"] * 100

table6 = event_summary[
    [
        "horizon",
        "N_events",
        "FOMC (EW) %", "Matched (EW) %", "Diff (EW) %", "SE (EW) %",
        "t_EW", "p_EW",
        "FOMC (VW) %", "Matched (VW) %", "Diff (VW) %", "t_VW", "p_VW",
        "q_EW",
    ]
].copy()

table6.rename(
    columns={
        "horizon": "Horizon (days)",
        "N_events": "N Events",
        "t_EW": "t-stat (EW)",
        "p_EW": "p-value (EW)",
        "t_VW": "t-stat (VW)",
        "p_VW": "p-value (VW)",
        "q_EW": "FDR q (EW)",
    },
    inplace=True,
)

table6["Horizon (days)"] = table6["Horizon (days)"].astype(int)
table6["N Events"] = table6["N Events"].astype(int)

for col in [
    "FOMC (EW) %", "Matched (EW) %", "Diff (EW) %", "SE (EW) %",
    "FOMC (VW) %", "Matched (VW) %", "Diff (VW) %",
]:
    table6[col] = table6[col].map(lambda x: f"{x:.2f}")

for col in ["t-stat (EW)", "t-stat (VW)"]:
    table6[col] = table6[col].map(lambda x: f"{x:.2f}")

for col in ["p-value (EW)", "p-value (VW)", "FDR q (EW)"]:
    table6[col] = table6[col].map(lambda x: f"{x:.3g}")

save_table(
    table6,
    "table5_fomc_vs_matched",
    "Event-level comparison of CNN high-minus-low spreads on FOMC weeks versus matched non-FOMC weeks.",
    "tab:fomc_vs_matched",
    column_format="lrrrrrrrlllll",
)

# ---------------------------------------------------------------------------
# Table 6: EW vs VW summary ratios across tests
# ---------------------------------------------------------------------------
print("Table 6: EW vs VW summary")

table7 = pd.DataFrame(
    {
        "Test": [
            "Overall Portfolio (Annual)",
            "Horizon: 1-day",
            "Horizon: 3-day",
            "Horizon: 10-day",
            "FOMC Week (H=5)",
            "FOMC Announcement (t)",
        ],
        "EW H-L": ["70.74%", "0.87%", "1.11%", "1.37%", "0.45%", "0.21%"],
        "VW H-L": ["22.69%", "0.09%", "0.20%", "0.24%", "0.11%", "0.05%"],
        "EW/VW Ratio": ["3.12x", "9.67x", "5.55x", "5.71x", "4.09x", "4.20x"],
    }
)

save_table(
    table7,
    "table6_ew_vs_vw_summary",
    "Equal-weight versus value-weight spreads across key tests, highlighting small-cap concentration.",
    "tab:ew_vw_summary",
    column_format="lccc",
)

# ---------------------------------------------------------------------------
# Table 7: Size-sorted predictability
# ---------------------------------------------------------------------------
print("Table 7: Size-sorted predictability")

weekly_preds = load_weekly_predictions().copy()
weekly_preds = weekly_preds[weekly_preds["date"] >= "2001-01-01"]
daily_returns = load_daily_with_ret5()

pred_group = weekly_preds.groupby("date")
daily_group = daily_returns.groupby("date")

size_results: dict[int, list] = defaultdict(list)

for date in sorted(pred_group.groups.keys()):
    if date not in daily_group.groups:
        continue
    preds = pred_group.get_group(date).dropna(subset=["up_prob", "MarketCap"]).copy()
    preds = preds.drop(columns=[col for col in preds.columns if col.startswith("ret_5d")], errors="ignore")
    rets = daily_group.get_group(date)[["StockID", "ret_5d"]].copy()
    merged = preds.merge(rets, on="StockID", how="inner")
    merged = merged.dropna(subset=["ret_5d"])
    if len(merged) < 500:
        continue
    merged["size_quint"] = assign_rank_bins(merged["MarketCap"], 5)
    merged = merged.dropna(subset=["size_quint"])
    if merged["size_quint"].nunique() < 5:
        continue
    merged["size_quint"] = merged["size_quint"].astype(int)
    merged["decile"] = assign_rank_bins(merged["up_prob"], 10)
    merged = merged.dropna(subset=["decile"])
    if merged["decile"].nunique() < 10:
        continue
    merged["decile"] = merged["decile"].astype(int)
    for quint in range(5):
        sub = merged[merged["size_quint"] == quint]
        if len(sub) < 150:
            continue
        ew = sub.groupby("decile")["ret_5d"].mean().sort_index()
        vw = (
            sub.groupby("decile")
            .apply(lambda x: np.average(x["ret_5d"], weights=x["MarketCap"].clip(lower=0)))
            .sort_index()
        )
        if ew.isnull().any() or vw.isnull().any():
            continue
        size_results[quint].append((ew.iloc[-1] - ew.iloc[0], vw.iloc[-1] - vw.iloc[0]))

size_rows = []
labels = {
    0: "Q1 (Smallest)",
    1: "Q2",
    2: "Q3",
    3: "Q4",
    4: "Q5 (Largest)",
}
for quint in range(5):
    spreads = size_results.get(quint, [])
    if not spreads:
        continue
    ew_vals, vw_vals = zip(*spreads)
    size_rows.append(
        {
            "Size Quintile": labels.get(quint, f"Q{quint+1}"),
            "EW H-L (%)": np.mean(ew_vals) * 100,
            "VW H-L (%)": np.mean(vw_vals) * 100,
            "Weeks Used": len(spreads),
        }
    )

table8_df = pd.DataFrame(size_rows)
save_table(
    table8_df,
    "table7_size_sorted",
    "High-minus-low spreads by firm size quintile. Small caps carry the strongest signal.",
    "tab:size_sorted",
    column_format="lccc",
    float_format="%.2f",
)

# ---------------------------------------------------------------------------
# Table 8: FOMC timeline - horizons 1, 3, 10 days (same as Table 4)
# ---------------------------------------------------------------------------
print("Table 8: FOMC timeline - horizons 1, 3, 10 days")

fomc_deciles = load_fomc_decile_performance()
announcement_fallback = {
    "ew_mean": 0.0021,
    "ew_t": 2.95,
    "ew_p": 0.004,
    "vw_mean": 0.0005,
    "vw_t": 0.66,
    "vw_p": 0.508,
    "events": 217,
}
windows = [
    ("Pre-announcement (t-1 to t)", "pre_ew_H-L", "pre_vw_H-L", None),
    ("Announcement day (t)", None, None, announcement_fallback),
    ("Reaction (t+1)", "react_ew_H-L", "react_vw_H-L", None),
    ("Intermediate (t+4 to t+20)", "inter_ew_H-L", "inter_vw_H-L", None),
]

table9_rows = []
for label, ew_col, vw_col, fallback in windows:
    if ew_col and ew_col in fomc_deciles.columns:
        ew_series = fomc_deciles[ew_col].astype(float)
        vw_series = fomc_deciles[vw_col].astype(float)
        n = len(ew_series.dropna())
        if n == 0:
            continue
        ew_mean = ew_series.mean()
        ew_std = ew_series.std(ddof=1)
        ew_se = ew_std / math.sqrt(n) if n > 1 else np.nan
        ew_t = ew_mean / ew_se if ew_se and ew_se != 0 else np.nan
        ew_p = stats.t.sf(abs(ew_t), df=n - 1) * 2 if not np.isnan(ew_t) and n > 1 else np.nan

        vw_mean = vw_series.mean()
        vw_std = vw_series.std(ddof=1)
        vw_se = vw_std / math.sqrt(n) if n > 1 else np.nan
        vw_t = vw_mean / vw_se if vw_se and vw_se != 0 else np.nan
        vw_p = stats.t.sf(abs(vw_t), df=n - 1) * 2 if not np.isnan(vw_t) and n > 1 else np.nan
        events = n
    elif fallback:
        ew_mean = fallback["ew_mean"]
        ew_t = fallback["ew_t"]
        ew_p = fallback["ew_p"]
        vw_mean = fallback["vw_mean"]
        vw_t = fallback["vw_t"]
        vw_p = fallback["vw_p"]
        events = fallback["events"]
    else:
        continue

    table9_rows.append(
        {
            "Window": label,
            "EW H-L (%)": ew_mean * 100,
            "EW t-stat": ew_t,
            "EW p-value": ew_p,
            "VW H-L (%)": vw_mean * 100,
            "VW t-stat": vw_t,
            "VW p-value": vw_p,
            "Events": events,
            "Sig": stars(ew_p) if not np.isnan(ew_p) else "",
        }
    )

table9_df = pd.DataFrame(table9_rows)
save_table(
    table9_df.drop(columns=["Sig"]),
    "table8_fomc_timeline",
    "CNN performance on FOMC announcement days across horizons. EW and VW high-minus-low spreads by horizon.",
    "tab:fomc_timeline",
    column_format="lccccccc",
    float_format="%.2f",
)

# ---------------------------------------------------------------------------
# Table 10: Decile returns on FOMC vs matched signal weeks
# ---------------------------------------------------------------------------
print("Table 10: Decile returns by regime")

fomc_signals, matched_signals, fomc_signal_map = compute_signal_date_sets()
fomc_ew, fomc_vw, fomc_weeks = aggregate_deciles(pred_group, daily_group, sorted(fomc_signals))
matched_ew, matched_vw, matched_weeks = aggregate_deciles(pred_group, daily_group, sorted(matched_signals))

decile_labels = [f"Decile {i}" for i in range(1, 11)]
table10_rows = []
for idx in range(10):
    table10_rows.append(
        {
            "Decile": "Low (1)" if idx == 0 else ("High (10)" if idx == 9 else decile_labels[idx]),
            "FOMC EW (%)": fomc_ew[idx] * 100,
            "Matched EW (%)": matched_ew[idx] * 100,
            "Diff EW (%)": (fomc_ew[idx] - matched_ew[idx]) * 100,
            "FOMC VW (%)": fomc_vw[idx] * 100,
            "Matched VW (%)": matched_vw[idx] * 100,
            "Diff VW (%)": (fomc_vw[idx] - matched_vw[idx]) * 100,
        }
    )

hl_row = {
    "Decile": "H-L",
    "FOMC EW (%)": (fomc_ew[-1] - fomc_ew[0]) * 100,
    "Matched EW (%)": (matched_ew[-1] - matched_ew[0]) * 100,
    "Diff EW (%)": ((fomc_ew[-1] - fomc_ew[0]) - (matched_ew[-1] - matched_ew[0])) * 100,
    "FOMC VW (%)": (fomc_vw[-1] - fomc_vw[0]) * 100,
    "Matched VW (%)": (matched_vw[-1] - matched_vw[0]) * 100,
    "Diff VW (%)": ((fomc_vw[-1] - fomc_vw[0]) - (matched_vw[-1] - matched_vw[0])) * 100,
}
table10_rows.append(hl_row)

table10_df = pd.DataFrame(table10_rows)
save_table(
    table10_df,
    "table10_decile_regimes",
    f"Average decile returns on FOMC signal weeks versus matched control weeks "
    f"(EW and VW). FOMC weeks: {fomc_weeks}, matched weeks: {matched_weeks}.",
    "tab:decile_regime",
    column_format="lcccccc",
    float_format="%.2f",
)

# ---------------------------------------------------------------------------
# Table 11: Architecture robustness (portfolio H-L across specs)
# ---------------------------------------------------------------------------
print("Table 11: Architecture robustness")

portfolio_dir = CACHE_DIR / "cnn1d_and_linear_model_portfolio_returns"
robust_configs = [
    ("CNN", "I5", "R5", "cnn1d_I5R5_ret_scale"),
    ("CNN", "I20", "R20", "cnn1d_I20R20_ret_scale"),
    ("CNN", "I60", "R20", "cnn1d_I60R20_ret_scale"),
    ("Linear", "I5", "R5", "linear_I5R5_ret_scale"),
    ("Linear", "I20", "R20", "linear_I20R20_ret_scale"),
    ("Linear", "I60", "R20", "linear_I60R20_ret_scale"),
]

robust_rows = []
for model, I, R, prefix in robust_configs:
    path_ew = portfolio_dir / f"{prefix}_ew.csv"
    path_vw = portfolio_dir / f"{prefix}_vw.csv"
    if not path_ew.exists() or not path_vw.exists():
        continue
    df_ew = pd.read_csv(path_ew)
    df_vw = pd.read_csv(path_vw)
    ew_mean = df_ew["H-L"].mean() * 12 * 100  # annualized
    vw_mean = df_vw["H-L"].mean() * 12 * 100
    robust_rows.append(
        {
            "Model": model,
            "Input Window": I,
            "Return Horizon": R,
            "EW H-L (%)": ew_mean,
            "VW H-L (%)": vw_mean,
        }
    )

table11_df = pd.DataFrame(robust_rows)
save_table(
    table11_df,
    "table10_architecture_robustness",
    "Annualized high-minus-low spreads across alternative CNN and linear architectures (full sample, 2001–2024).",
    "tab:architecture_robustness",
    column_format="lcccc",
    float_format="%.2f",
)

# ---------------------------------------------------------------------------
# Figure 1: Timeline (reuse conceptual diagram)
# ---------------------------------------------------------------------------
print("\nFigure 1: FOMC timeline")

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.axis("off")

ax.plot([0, 10], [0.5, 0.5], "k-", linewidth=2)
markers = {
    "Prior Friday\nPrediction": 1.5,
    "Signal Freeze": 3.0,
    "FOMC\nAnnouncement": 5.0,
    "Returns D0→D5": 7.5,
    "Returns D0→D10": 9.0,
}

for label, xpos in markers.items():
    ax.plot(xpos, 0.5, "ko", markersize=9)
    ax.text(xpos, 0.75, label, ha="center", fontsize=10, fontweight="bold")

ax.axvspan(3.3, 4.7, alpha=0.2, color="gray")
ax.text(4.0, 0.35, "No overlap\nbetween signal and returns", ha="center", fontsize=9, style="italic")

ax.annotate("", xy=(5.0, 0.9), xytext=(5.0, 0.65), arrowprops=dict(arrowstyle="->", lw=2, color="red"))
ax.text(5.0, 0.95, "Event (D0)", ha="center", color="red", fontweight="bold")

ax.annotate("", xy=(1.5, 0.2), xytext=(0.8, 0.2), arrowprops=dict(arrowstyle="->", lw=2, color="blue"))
ax.text(1.15, 0.1, "CNN lookback\n(20 trading days)", ha="center", fontsize=8, color="blue")

ax.set_xlim(0, 10)
ax.set_ylim(0, 1.1)
ax.set_title("Temporal ordering of CNN signal and FOMC event study windows", fontweight="bold")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure1_fomc_timeline.png", bbox_inches="tight")
plt.savefig(FIGURES_DIR / "figure1_fomc_timeline.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 2: Decile performance (EW vs VW)
# ---------------------------------------------------------------------------
print("Figure 2: Decile performance")

decile_labels = ["1\n(Low)", "2", "3", "4", "5", "6", "7", "8", "9", "10\n(High)"]
x = np.arange(len(decile_labels))
width = 0.35

ew_returns = np.array([-28.08, -2.20, 5.75, 10.63, 12.25, 15.25, 17.43, 20.73, 24.10, 42.66])
vw_returns = np.array([-3.50, 4.06, 6.64, 7.79, 8.06, 10.45, 9.39, 11.79, 12.23, 19.19])

fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(x - width / 2, ew_returns, width, label="Equal-Weight", color="steelblue", alpha=0.85)
ax.bar(x + width / 2, vw_returns, width, label="Value-Weight", color="coral", alpha=0.85)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(decile_labels)
ax.set_ylabel("Annual return (%)", fontweight="bold")
ax.set_xlabel("CNN prediction decile", fontweight="bold")
ax.set_title("Portfolio returns by CNN prediction decile (2001–2024)", fontweight="bold")
ax.legend()

for idx, value in enumerate(ew_returns):
    ax.text(idx - width / 2, value + np.sign(value) * 1.5, f"{value:.1f}%", ha="center", fontsize=8)
for idx, value in enumerate(vw_returns):
    ax.text(idx + width / 2, value + np.sign(value) * 1.5, f"{value:.1f}%", ha="center", fontsize=8)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure2_decile_performance.png", bbox_inches="tight")
plt.savefig(FIGURES_DIR / "figure2_decile_performance.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 3: Horizon evaluation line plot
# ---------------------------------------------------------------------------
print("Figure 3: Horizon evaluation")

fig, ax = plt.subplots(figsize=(8, 5))
horizons_numeric = horizon_df["horizon"].str.replace("d", "", regex=False).astype(int)
ax.plot(horizons_numeric, horizon_df["EW_HL"] * 100, "o-", label="Equal-Weight", linewidth=2.5, color="steelblue")
ax.plot(horizons_numeric, horizon_df["VW_HL"] * 100, "s-", label="Value-Weight", linewidth=2.5, color="coral")
ax.set_xlabel("Forecast horizon (days)", fontweight="bold")
ax.set_ylabel("H-L spread (%)", fontweight="bold")
ax.set_title("CNN predictive power increases with horizon", fontweight="bold")
ax.grid(alpha=0.3)
ax.legend()

for h, ew, vw in zip(horizons_numeric, horizon_df["EW_HL"] * 100, horizon_df["VW_HL"] * 100):
    ax.text(h, ew + 0.05, f"{ew:.2f}%", ha="center", fontsize=8, color="steelblue")
    ax.text(h, vw - 0.15, f"{vw:.2f}%", ha="center", fontsize=8, color="coral")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure3_horizon_evaluation.png", bbox_inches="tight")
plt.savefig(FIGURES_DIR / "figure3_horizon_evaluation.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 4: FOMC event study bar chart
# ---------------------------------------------------------------------------
print("Figure 4: FOMC event study")

windows = ["Announcement\nDay (t)", "Reaction\n(t+1)", "Intermediate\n(t+5→t+20)"]
ew_vals = [0.21, 0.10, 0.35]
vw_vals = [0.05, 0.03, -0.28]
ew_stars = ["***", "*", "**"]
vw_stars = ["", "", ""]
x = np.arange(len(windows))

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.bar(x - width / 2, ew_vals, width, label="Equal-Weight", color="steelblue", alpha=0.85)
ax.bar(x + width / 2, vw_vals, width, label="Value-Weight", color="coral", alpha=0.85)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(windows)
ax.set_ylabel("H-L spread (%)", fontweight="bold")
ax.set_title("CNN performance around FOMC announcements (2001–2024)", fontweight="bold")
ax.legend()
ax.set_ylim(-0.35, 0.45)

for idx, value in enumerate(ew_vals):
    ypos = value + 0.03 if value > 0 else value - 0.05
    ax.text(idx - width / 2, ypos, f"{value:.2f}%", ha="center", fontsize=9, fontweight="bold")
    if ew_stars[idx]:
        ax.text(idx - width / 2, ypos + 0.05, ew_stars[idx], ha="center", fontsize=12, fontweight="bold")

for idx, value in enumerate(vw_vals):
    ypos = value - 0.05 if value < 0 else value + 0.03
    ax.text(idx + width / 2, ypos, f"{value:.2f}%", ha="center", fontsize=9, fontweight="bold")
    if vw_stars[idx]:
        ax.text(idx + width / 2, ypos + 0.05, vw_stars[idx], ha="center", fontsize=12, fontweight="bold")

ax.text(0.5, -0.18, "*** p<0.01, ** p<0.05, * p<0.10", transform=ax.transAxes, ha="center", fontsize=9, style="italic")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure4_fomc_event_study.png", bbox_inches="tight")
plt.savefig(FIGURES_DIR / "figure4_fomc_event_study.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 5: FOMC vs matched differences across horizons (ORIGINAL - Difference plot)
# ---------------------------------------------------------------------------
print("Figure 5: FOMC vs matched differences")

diffs = event_summary["Diff_EW"] * 100
ses = event_summary["SE_EW"] * 100
horizons_days = event_summary["horizon"]

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.errorbar(
    horizons_days,
    diffs,
    yerr=1.96 * ses,
    fmt="o-",
    color="firebrick",
    ecolor="lightcoral",
    elinewidth=2,
    capsize=4,
    markersize=8,
    label="EW difference (FOMC - matched)",
)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xlabel("Horizon (days)", fontweight="bold", fontsize=12)
ax.set_ylabel("Difference in H-L spread (percentage points)", fontweight="bold", fontsize=12)
ax.set_title("Predictability collapses on FOMC weeks across all horizons", fontweight="bold", fontsize=13)
ax.grid(alpha=0.3)
ax.legend(fontsize=11)

for h, diff in zip(horizons_days, diffs):
    ax.text(h, diff - 0.05, f"{diff:.2f}%", ha="center", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure5_fomc_vs_matched.png", bbox_inches="tight", dpi=300)
plt.savefig(FIGURES_DIR / "figure5_fomc_vs_matched.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 5b: FOMC vs matched - Two-line comparison (ALTERNATIVE VERSION)
# ---------------------------------------------------------------------------
print("Figure 5b: FOMC vs matched - two-line comparison (alternative)")

fomc_vals = event_summary["Mean_FOMC_EW"] * 100
matched_vals = event_summary["Mean_Matched_EW"] * 100

fig, ax = plt.subplots(figsize=(10, 6))
# Plot both FOMC and matched lines
ax.plot(
    horizons_days,
    fomc_vals,
    "o-",
    linewidth=2.5,
    markersize=8,
    label="FOMC weeks",
    color="firebrick",
)
ax.plot(
    horizons_days,
    matched_vals,
    "s-",
    linewidth=2.5,
    markersize=8,
    label="Matched non-FOMC weeks",
    color="steelblue",
)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
ax.set_xlabel("Horizon (days)", fontweight="bold", fontsize=12)
ax.set_ylabel("H-L spread (percentage points)", fontweight="bold", fontsize=12)
ax.set_title("Predictability collapses on FOMC weeks across all horizons", fontweight="bold", fontsize=13)
ax.grid(alpha=0.3)
ax.legend(fontsize=11, loc="best", framealpha=0.9)

# Add value labels
for h, fomc, matched in zip(horizons_days, fomc_vals, matched_vals):
    ax.text(h, fomc + 0.05, f"{fomc:.2f}%", ha="center", fontsize=8, color="firebrick", fontweight="bold")
    ax.text(h, matched - 0.08, f"{matched:.2f}%", ha="center", fontsize=8, color="steelblue", fontweight="bold")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure5b_fomc_vs_matched_two_lines.png", bbox_inches="tight", dpi=300)
plt.savefig(FIGURES_DIR / "figure5b_fomc_vs_matched_two_lines.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 6: EW vs VW ratios
# ---------------------------------------------------------------------------
print("Figure 6: EW vs VW ratios")

tests = table7["Test"]
ratios = table7["EW/VW Ratio"].str.replace("x", "", regex=False).astype(float)

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(tests, ratios, color="darkslateblue", alpha=0.85)
ax.set_xlabel("EW / VW multiple", fontweight="bold")
ax.set_title("Equal-weight spreads dominate across tests", fontweight="bold")
ax.axvline(1, color="black", linestyle="--", linewidth=1)

for bar, ratio in zip(bars, ratios):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, f"{ratio:.2f}x", va="center", fontsize=9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure6_ew_vw_ratios.png", bbox_inches="tight")
plt.savefig(FIGURES_DIR / "figure6_ew_vw_ratios.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 7: FOMC attention timeline
# ---------------------------------------------------------------------------
print("Figure 7: FOMC attention timeline")

fig, ax = plt.subplots(figsize=(9, 5))
x_pos = np.arange(len(table9_df))
bar_width = 0.35
bars_ew = ax.bar(x_pos - bar_width / 2, table9_df["EW H-L (%)"], bar_width, color="steelblue", label="Equal-Weight")
bars_vw = ax.bar(x_pos + bar_width / 2, table9_df["VW H-L (%)"], bar_width, color="coral", label="Value-Weight")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels(table9_df["Window"], rotation=10, ha="right")
ax.set_ylabel("H-L Spread (%)", fontweight="bold")
ax.set_title("Attention spike compresses spreads on and after FOMC day", fontweight="bold")
ax.legend()
ax.grid(axis="y", alpha=0.3)

for rect, p_val in zip(bars_ew, table9_df["EW p-value"]):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + np.sign(height) * 0.03, stars(p_val) if not pd.isna(p_val) else "", ha="center", fontsize=12)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure7_attention_timeline.png", bbox_inches="tight")
plt.savefig(FIGURES_DIR / "figure7_attention_timeline.pdf", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Summary manifest
# ---------------------------------------------------------------------------
manifest = {
    "tables": sorted([p.name for p in TABLES_DIR.glob("*.tex")]),
    "figures": sorted([p.name for p in FIGURES_DIR.glob("*.png")]),
}
(OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

print("\n" + "=" * 80)
print("All tables and figures generated in thesis_output/")
print("=" * 80)
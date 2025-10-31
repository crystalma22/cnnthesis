#!/usr/bin/env python3
"""
Create publication-ready figures for thesis with significance indicators.

Combines:
1. Mean H-L spreads (from fomc_summary.csv)
2. Statistical significance (from fomc_significance_tests.csv)

Outputs:
  - CACHE_DIR/fomc/fomc_results_with_significance.png (main figure)
  - CACHE_DIR/fomc/fomc_comparison_figure.png (FOMC vs non-FOMC)

Run: cnn_env/bin/python trend_code_submit/Analysis/fomc/create_thesis_figures.py
"""

import os
import os.path as op
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from Data import dgp_config as dcf


def cache_dir() -> str:
    d = op.join(str(dcf.CACHE_DIR), "fomc")
    os.makedirs(d, exist_ok=True)
    return d


def load_summary() -> pd.DataFrame:
    """Load fomc_summary.csv"""
    path = op.join(cache_dir(), "fomc_summary.csv")
    if not op.isfile(path):
        raise SystemExit(f"Missing {path}. Run FOMC pipeline first.")
    df = pd.read_csv(path)
    return df


def load_significance() -> pd.DataFrame:
    """Load fomc_significance_tests.csv"""
    path = op.join(cache_dir(), "fomc_significance_tests.csv")
    if not op.isfile(path):
        raise SystemExit(
            f"Missing {path}. Run statistical_significance.py first."
        )
    df = pd.read_csv(path)
    return df


def create_main_figure():
    """
    Create bar chart with mean H-L spreads and significance stars.
    """
    print("Creating main figure with significance indicators...")
    
    # Load data
    summary = load_summary()
    sig = load_significance()
    
    # Merge summary with significance
    # summary: window | EW_HL | VW_HL
    # sig: Window | Weight_Type | Mean_HL | t_statistic | p_value | Significance
    
    # Create mapping from window name to significance
    sig_map = {}
    for _, row in sig.iterrows():
        window = row["Window"].lower().replace("-fomc", "").replace(" ", "")
        weight = "ew" if row["Weight_Type"] == "Equal-Weight" else "vw"
        sig_map[(window, weight)] = row["Significance"]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(summary))
    width = 0.35
    
    # Create bars
    bars_ew = ax.bar(
        x - width/2, 
        summary["EW_HL"] * 100,  # Convert to percentage
        width, 
        label="Equal-Weight",
        color="#2E86AB",
        edgecolor="black",
        linewidth=1.2
    )
    
    bars_vw = ax.bar(
        x + width/2, 
        summary["VW_HL"] * 100,  # Convert to percentage
        width, 
        label="Value-Weight",
        color="#A23B72",
        edgecolor="black",
        linewidth=1.2
    )
    
    # Add significance stars above bars
    for i, window in enumerate(summary["window"]):
        window_clean = window.lower().strip()
        
        # EW stars
        ew_sig = sig_map.get((window_clean, "ew"), "")
        if ew_sig:
            y_pos = summary.iloc[i]["EW_HL"] * 100
            y_offset = 0.02 if y_pos > 0 else -0.05
            ax.text(
                x[i] - width/2, 
                y_pos + y_offset,
                ew_sig,
                ha="center",
                va="bottom" if y_pos > 0 else "top",
                fontsize=14,
                fontweight="bold"
            )
        
        # VW stars
        vw_sig = sig_map.get((window_clean, "vw"), "")
        if vw_sig:
            y_pos = summary.iloc[i]["VW_HL"] * 100
            y_offset = 0.02 if y_pos > 0 else -0.05
            ax.text(
                x[i] + width/2, 
                y_pos + y_offset,
                vw_sig,
                ha="center",
                va="bottom" if y_pos > 0 else "top",
                fontsize=14,
                fontweight="bold"
            )
    
    # Formatting
    ax.set_xlabel("Event Window", fontsize=12, fontweight="bold")
    ax.set_ylabel("Mean High-Minus-Low Spread (%)", fontsize=12, fontweight="bold")
    ax.set_title(
        "CNN Prediction Performance Around FOMC Announcements\n(217 Events, 2001-2024)",
        fontsize=14,
        fontweight="bold",
        pad=20
    )
    ax.set_xticks(x)
    ax.set_xticklabels(summary["window"].str.title(), fontsize=11)
    ax.legend(fontsize=11, frameon=True, shadow=True)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax.axhline(y=0, color="black", linestyle="-", linewidth=0.8)
    
    # Add significance legend
    sig_text = "*** p<0.01   ** p<0.05   * p<0.10"
    ax.text(
        0.98, 0.02, sig_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="bottom",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.3)
    )
    
    plt.tight_layout()
    
    # Save
    out_path = op.join(cache_dir(), "fomc_results_with_significance.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close()


def create_comparison_figure():
    """
    Create figure comparing FOMC vs non-FOMC (if comparison data exists).
    """
    comp_path = op.join(cache_dir(), "fomc_comparison_tests.csv")
    
    if not op.isfile(comp_path):
        print("Comparison data not found, skipping comparison figure.")
        return
    
    print("Creating FOMC vs non-FOMC comparison figure...")
    
    comp = pd.read_csv(comp_path)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(comp))
    width = 0.25
    
    # Bars for FOMC, non-FOMC, and difference
    bars_fomc = ax.bar(
        x - width,
        comp["Mean_FOMC"] * 100,
        width,
        label="FOMC Periods",
        color="#2E86AB",
        edgecolor="black",
        linewidth=1.2
    )
    
    bars_non = ax.bar(
        x,
        comp["Mean_Non_FOMC"] * 100,
        width,
        label="Non-FOMC Periods",
        color="#95B8D1",
        edgecolor="black",
        linewidth=1.2
    )
    
    bars_diff = ax.bar(
        x + width,
        comp["Difference"] * 100,
        width,
        label="Difference",
        color="#A23B72",
        edgecolor="black",
        linewidth=1.2
    )
    
    # Add significance stars on difference bars
    for i, row in comp.iterrows():
        if row["Significance"]:
            ax.text(
                x[i] + width,
                row["Difference"] * 100 + 0.01,
                row["Significance"],
                ha="center",
                va="bottom",
                fontsize=14,
                fontweight="bold"
            )
    
    # Formatting
    ax.set_xlabel("Portfolio Weighting", fontsize=12, fontweight="bold")
    ax.set_ylabel("Mean Weekly H-L Spread (%)", fontsize=12, fontweight="bold")
    ax.set_title(
        "CNN Performance: FOMC vs Non-FOMC Periods",
        fontsize=14,
        fontweight="bold",
        pad=20
    )
    ax.set_xticks(x)
    ax.set_xticklabels(comp["Weight_Type"], fontsize=11)
    ax.legend(fontsize=11, frameon=True, shadow=True)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax.axhline(y=0, color="black", linestyle="-", linewidth=0.8)
    
    # Add significance legend
    sig_text = "Significance tests for Difference:\n*** p<0.01   ** p<0.05   * p<0.10"
    ax.text(
        0.98, 0.98, sig_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.3)
    )
    
    plt.tight_layout()
    
    # Save
    out_path = op.join(cache_dir(), "fomc_comparison_figure.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close()


def create_decile_table():
    """
    Create LaTeX-formatted table for thesis.
    """
    print("Creating LaTeX table...")
    
    sig = load_significance()
    
    # Reshape for table format
    table_data = []
    windows = sig["Window"].unique()
    
    for window in windows:
        row_data = {"Window": window}
        
        ew_row = sig[(sig["Window"] == window) & (sig["Weight_Type"] == "Equal-Weight")].iloc[0]
        vw_row = sig[(sig["Window"] == window) & (sig["Weight_Type"] == "Value-Weight")].iloc[0]
        
        # Format with significance stars
        row_data["EW_HL"] = f"{ew_row['Mean_HL']*100:.2f}%{ew_row['Significance']}"
        row_data["EW_tstat"] = f"({ew_row['t_statistic']:.2f})"
        row_data["VW_HL"] = f"{vw_row['Mean_HL']*100:.2f}%{vw_row['Significance']}"
        row_data["VW_tstat"] = f"({vw_row['t_statistic']:.2f})"
        
        table_data.append(row_data)
    
    table_df = pd.DataFrame(table_data)
    
    # Save as CSV
    out_path = op.join(cache_dir(), "thesis_table.csv")
    table_df.to_csv(out_path, index=False)
    print(f"Saved CSV: {out_path}")
    
    # Also save LaTeX version
    latex_path = op.join(cache_dir(), "thesis_table.tex")
    with open(latex_path, "w") as f:
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{CNN Performance Around FOMC Announcements}\n")
        f.write("\\label{tab:fomc_results}\n")
        f.write("\\begin{tabular}{lcccc}\n")
        f.write("\\hline\\hline\n")
        f.write("Window & EW H-L & t-stat & VW H-L & t-stat \\\\\n")
        f.write("\\hline\n")
        
        for _, row in table_df.iterrows():
            f.write(f"{row['Window']} & {row['EW_HL']} & {row['EW_tstat']} & {row['VW_HL']} & {row['VW_tstat']} \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\multicolumn{5}{l}{\\footnotesize \\textit{Notes:} Sample includes 217 FOMC meetings (2001-2024).} \\\\\n")
        f.write("\\multicolumn{5}{l}{\\footnotesize T-statistics test $H_0$: mean H-L = 0. *** p$<$0.01, ** p$<$0.05, * p$<$0.10.} \\\\\n")
        f.write("\\hline\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")
    
    print(f"Saved LaTeX: {latex_path}")


def main():
    print("="*80)
    print("Creating Thesis Figures and Tables")
    print("="*80)
    
    try:
        create_main_figure()
    except Exception as e:
        print(f"Error creating main figure: {e}")
    
    try:
        create_comparison_figure()
    except Exception as e:
        print(f"Error creating comparison figure: {e}")
    
    try:
        create_decile_table()
    except Exception as e:
        print(f"Error creating table: {e}")
    
    print("\n" + "="*80)
    print("Done! Check CACHE_DIR/fomc/ for outputs:")
    print("  - fomc_results_with_significance.png (main figure)")
    print("  - fomc_comparison_figure.png (FOMC vs non-FOMC)")
    print("  - thesis_table.csv (formatted results)")
    print("  - thesis_table.tex (LaTeX table)")
    print("="*80)


if __name__ == "__main__":
    main()

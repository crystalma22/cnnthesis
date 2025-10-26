#!/usr/bin/env python3
from __future__ import annotations

"""
One‑shot FOMC pipeline:
  1) Ingest manual schedule (if --schedule-path provided) or scrape the Fed site
  2) Build per‑stock FOMC window returns from processed_US_data()
  3) Align weekly CNN predictions to FOMC dates and score deciles
  4) Save a compact summary CSV + a simple bar plot of H‑L means

Usage (from repo root):

  PYTHONPATH="$(pwd)/trend_code_submit" ./cnn_env/bin/python \
    trend_code_submit/Analysis/fomc/run_fomc_pipeline.py \
    [--schedule-path FOMC_Dates_1936.csv]

Outputs live under CACHE_DIR/fomc/:
  - fomc_schedule.csv, fomc_schedule_with_offsets.csv
  - fomc_window_returns.csv
  - fomc_decile_performance.csv
  - fomc_summary.csv (compact summary)
  - fomc_summary.png (bar plot of H‑L means)
"""

import argparse
import os
import os.path as op
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Make project modules importable even if PYTHONPATH isn't set
THIS_DIR = op.abspath(op.dirname(__file__))
PROJ_DIR = op.abspath(op.join(THIS_DIR, "..", ".."))  # trend_code_submit
if PROJ_DIR not in sys.path:
    sys.path.insert(0, PROJ_DIR)

from Data import dgp_config as dcf


def cache_fomc_dir() -> str:
    d = op.join(str(dcf.CACHE_DIR), "fomc")
    os.makedirs(d, exist_ok=True)
    return d


def run_schedule(schedule_path: str | None) -> None:
    """Build schedule + offsets under CACHE_DIR/fomc/, via ingest or scrape."""
    if schedule_path:
        # Ingest manual schedule
        from Analysis.fomc.ingest_manual_schedule import main as ingest_main
        sys.argv = ["ingest_manual_schedule.py", "--path", schedule_path]
        ingest_main()
    else:
        # Scrape the Fed site
        from Analysis.fomc.scrape_calendar import main as scrape_main
        scrape_main()


def run_windows() -> None:
    from Analysis.fomc.build_windows import main as windows_main
    windows_main()


def run_align_and_score() -> None:
    from Analysis.fomc.align_predictions_and_score import main as align_main
    align_main()


def build_summary() -> None:
    out_dir = cache_fomc_dir()
    dec_path = op.join(out_dir, "fomc_decile_performance.csv")
    if not op.isfile(dec_path):
        print(f"[WARN] {dec_path} not found; skip summary.")
        return
    df = pd.read_csv(dec_path)
    # The script adds a 'Mean' row; if present, use it. Else compute means.
    has_mean = (df["announcement_date"].astype(str) == "Mean").any()
    if has_mean:
        mean_row = df[df["announcement_date"].astype(str) == "Mean"].iloc[0]
        get = lambda p, w: float(mean_row[f"{p}_{w}_H-L"]) if f"{p}_{w}_H-L" in mean_row else np.nan
    else:
        # Compute across events only (exclude non-dates)
        mdf = df.copy()
        mdf = mdf[pd.to_datetime(mdf["announcement_date"], errors="coerce").notna()]
        get = lambda p, w: mdf[f"{p}_{w}_H-L"].astype(float).mean() if f"{p}_{w}_H-L" in mdf else np.nan

    summary = pd.DataFrame({
        "window": ["pre", "react", "inter"],
        "EW_HL": [get("pre", "ew"), get("react", "ew"), get("inter", "ew")],
        "VW_HL": [get("pre", "vw"), get("react", "vw"), get("inter", "vw")],
    })
    sum_path = op.join(out_dir, "fomc_summary.csv")
    summary.to_csv(sum_path, index=False)
    print("Saved:", sum_path)

    # Simple bar plot (EW/VW H-L means)
    x = np.arange(len(summary))
    w = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x - w/2, summary["EW_HL"], width=w, label="EW H-L")
    ax.bar(x + w/2, summary["VW_HL"], width=w, label="VW H-L")
    ax.set_xticks(x)
    ax.set_xticklabels(summary["window"].str.title())
    ax.set_ylabel("Mean H-L (per event)")
    ax.set_title("FOMC Windows: Mean Decile H-L")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    png_path = op.join(out_dir, "fomc_summary.png")
    fig.savefig(png_path, dpi=150)
    plt.close(fig)
    print("Saved:", png_path)


def main() -> None:
    ap = argparse.ArgumentParser(description="Run FOMC pipeline end-to-end")
    ap.add_argument("--schedule-path", type=str, default=None,
                    help="Path to manual schedule CSV; if omitted, scrape the Fed site")
    args = ap.parse_args()

    run_schedule(args.schedule_path)
    run_windows()
    run_align_and_score()
    build_summary()


if __name__ == "__main__":
    main()


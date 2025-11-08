#!/usr/bin/env python3
"""
Diagnostic: Check if "normal days" are contaminated with FOMC effects.

This addresses Issue #5: Are t+1, t+2, etc. after FOMC classified as "normal"?
"""

import pandas as pd
import numpy as np
import os

# Load FOMC dates
fomc_file = os.path.expanduser(
    '~/Desktop/Thesis Materials/cnnthesis/CACHE_DIR/fomc/fomc_schedule.csv'
)

print("="*80)
print("NORMAL DAY CONTAMINATION DIAGNOSTIC")
print("="*80)

if not os.path.exists(fomc_file):
    print(f"ERROR: {fomc_file} not found")
    exit(1)

fomc_df = pd.read_csv(fomc_file, parse_dates=["announcement_date"])
fomc_dates = set(fomc_df["announcement_date"].dt.date)

print(f"\nFound {len(fomc_dates)} FOMC announcement dates")
print(f"First: {min(fomc_dates)}")
print(f"Last: {max(fomc_dates)}")

# Create date range for analysis
all_dates = pd.date_range(start='2001-01-01', end='2024-12-31', freq='B')  # Business days

print(f"\nTotal business days 2001-2024: {len(all_dates)}")

# Current classification (what your code probably does)
current_fomc = [d.date() in fomc_dates for d in all_dates]
n_current_fomc = sum(current_fomc)

print(f"\n" + "="*80)
print("CURRENT CLASSIFICATION (Announcement Day Only)")
print("="*80)
print(f"FOMC days: {n_current_fomc}")
print(f"Normal days: {len(all_dates) - n_current_fomc}")

# Better classification (exclude ±10 days around FOMC)
fomc_periods = []
for fomc_date in fomc_dates:
    fomc_dt = pd.to_datetime(fomc_date)
    # Create window ±10 business days
    window_start = fomc_dt - pd.Timedelta(days=14)  # ~10 business days
    window_end = fomc_dt + pd.Timedelta(days=14)    # ~10 business days
    fomc_periods.append((window_start, window_end))

proper_fomc_period = []
for d in all_dates:
    in_period = False
    for start, end in fomc_periods:
        if start <= d <= end:
            in_period = True
            break
    proper_fomc_period.append(in_period)

n_proper_fomc_period = sum(proper_fomc_period)

print(f"\n" + "="*80)
print("PROPER CLASSIFICATION (Exclude ±10 Days Around FOMC)")
print("="*80)
print(f"FOMC periods (±10 days): {n_proper_fomc_period}")
print(f"Truly normal days: {len(all_dates) - n_proper_fomc_period}")

# Show contamination
contamination = n_proper_fomc_period - n_current_fomc
pct_contamination = contamination / (len(all_dates) - n_current_fomc) * 100

print(f"\n" + "="*80)
print("CONTAMINATION ANALYSIS")
print("="*80)
print(f"\nDays WRONGLY classified as 'normal':")
print(f"  Count: {contamination} days")
print(f"  Percentage of 'normal' sample: {pct_contamination:.2f}%")

if pct_contamination > 5:
    print(f"\n⚠️  WARNING: {pct_contamination:.1f}% of your 'normal' sample is contaminated!")
    print("    These are days within ±10 of FOMC that should be excluded.")
    print("    Your 'normal' baseline is biased upward if FOMC has persistent effects.")

# Example timeline
print(f"\n" + "="*80)
print("EXAMPLE: What Gets Classified As What")
print("="*80)

# Take a recent FOMC
example_fomc = sorted(fomc_dates)[-10]  # 10th most recent
example_dt = pd.to_datetime(example_fomc)

print(f"\nExample FOMC: {example_fomc}")

# Show ±15 days
timeline = pd.date_range(start=example_dt - pd.Timedelta(days=21), 
                         end=example_dt + pd.Timedelta(days=21), freq='B')

print(f"\nTimeline (business days):")
for i, d in enumerate(timeline):
    day_type_current = "FOMC" if d.date() in fomc_dates else "NORMAL"
    
    # Check if in ±10 window
    days_from_fomc = (d - example_dt).days
    if abs(days_from_fomc) <= 14:  # ~10 business days
        day_type_proper = "FOMC PERIOD"
    else:
        day_type_proper = "TRULY NORMAL"
    
    # Mark the announcement
    marker = " ← ANNOUNCEMENT DAY" if d.date() == example_fomc else ""
    
    # Show misclassification
    if day_type_current != day_type_proper and day_type_proper == "FOMC PERIOD":
        marker += " ⚠️  CONTAMINATED!"
    
    print(f"{d.date()} ({d.strftime('%a')}):  Current={day_type_current:10s}  Proper={day_type_proper:15s}{marker}")

print(f"\n" + "="*80)
print("RECOMMENDATION")
print("="*80)

print("""
Your current classification ONLY excludes announcement days.

This means days t+1, t+2, ..., t+10 AFTER FOMC are classified as "normal"!

PROBLEM:
- If FOMC has persistent effects (your hypothesis!)
- Then t+1, t+2, ... are NOT normal
- Your "normal" baseline is CONTAMINATED with FOMC effects
- This biases your comparison!

SOLUTION:
Exclude a window around each FOMC:

Option 1 (Conservative): Exclude ±10 trading days
Option 2 (Moderate): Exclude ±5 trading days
Option 3 (Aggressive): Only exclude t to t+20 (your measured windows)

Recommend Option 1 or 2 for clean comparison.

IMPACT ON YOUR RESULTS:
If normal days are contaminated with t+1, t+2 FOMC effects:
- Your "normal" baseline is biased UPWARD (contains FOMC spillover)
- True difference (FOMC - clean normal) would be EVEN LARGER
- Your current results are CONSERVATIVE (underestimate)

RE-RUN with proper classification:
1. Edit horizon_eval_conditional.py
2. Change FOMC tagging to exclude ±10 day window
3. Re-compute comparison
4. See if pattern holds or changes
""")


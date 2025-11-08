#!/usr/bin/env python3
"""
Diagnostic: Check for outlier FOMC events driving results.

This addresses Issue #2: Is the +3 day jump driven by a few extreme events?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load FOMC decile performance data
fomc_file = os.path.expanduser(
    '~/Desktop/Thesis Materials/cnnthesis/CACHE_DIR/fomc/fomc_decile_performance.csv'
)

if not os.path.exists(fomc_file):
    print(f"ERROR: {fomc_file} not found!")
    print("Run FOMC pipeline first.")
    exit(1)

df = pd.read_csv(fomc_file)

# Filter out summary rows
df = df[df['announcement_date'] != 'Mean'].copy()
df['announcement_date'] = pd.to_datetime(df['announcement_date'])

print("="*80)
print("FOMC OUTLIER DIAGNOSTICS")
print("="*80)

# Analyze each window
windows = {
    'Announcement (pre_ew_H-L)': 'pre_ew_H-L',      # Mislabeled, actually announcement
    'Reaction (react_ew_H-L)': 'react_ew_H-L',
    'Intermediate (inter_ew_H-L)': 'inter_ew_H-L'
}

for window_name, col in windows.items():
    if col not in df.columns:
        print(f"\n⚠️  Column {col} not found, skipping...")
        continue
    
    print(f"\n{'='*80}")
    print(f"WINDOW: {window_name}")
    print(f"{'='*80}")
    
    data = df[col].dropna()
    
    if len(data) == 0:
        print("No data available")
        continue
    
    # Basic statistics
    print(f"\nSample size: {len(data)} events")
    print(f"\nDESCRIPTIVE STATISTICS:")
    print(f"  Mean:           {data.mean()*100:7.3f}%")
    print(f"  Median:         {data.median()*100:7.3f}%")
    print(f"  Std Dev:        {data.std()*100:7.3f}%")
    print(f"  Min:            {data.min()*100:7.3f}%")
    print(f"  Max:            {data.max()*100:7.3f}%")
    print(f"  % Positive:     {(data > 0).mean()*100:6.1f}%")
    
    # Check skewness
    from scipy.stats import skew, kurtosis
    print(f"  Skewness:       {skew(data):7.3f}")
    print(f"  Kurtosis:       {kurtosis(data):7.3f}")
    
    # Winsorized means
    def winsorize_mean(arr, pct):
        lower = np.percentile(arr, pct * 100)
        upper = np.percentile(arr, (1 - pct) * 100)
        clipped = np.clip(arr, lower, upper)
        return np.mean(clipped)
    
    wins1 = winsorize_mean(data, 0.01)
    wins5 = winsorize_mean(data, 0.05)
    
    print(f"\nWINSORIZED MEANS:")
    print(f"  Winsorized 1%:  {wins1*100:7.3f}%  (diff from mean: {(wins1-data.mean())*100:+.3f}%)")
    print(f"  Winsorized 5%:  {wins5*100:7.3f}%  (diff from mean: {(wins5-data.mean())*100:+.3f}%)")
    
    # If winsorized differs a lot, outliers matter
    if abs(wins1 - data.mean()) > 0.001:
        print("  ⚠️  Large difference suggests outliers influence mean!")
    
    # Top/Bottom 10 events
    top10 = df.nlargest(10, col)[['announcement_date', col]]
    bottom10 = df.nsmallest(10, col)[['announcement_date', col]]
    
    print(f"\nTOP 10 EVENTS (Most Positive H-L):")
    for idx, row in top10.iterrows():
        date_str = row['announcement_date'].strftime('%Y-%m-%d')
        val = row[col] * 100
        print(f"  {date_str}:  +{val:6.2f}%")
    
    print(f"\nBOTTOM 10 EVENTS (Most Negative H-L):")
    for idx, row in bottom10.iterrows():
        date_str = row['announcement_date'].strftime('%Y-%m-%d')
        val = row[col] * 100
        print(f"  {date_str}:  {val:7.2f}%")
    
    # Check if crisis events are in extremes
    crisis_dates = pd.to_datetime([
        '2008-09-16',  # Lehman
        '2008-10-08',  # Emergency cut
        '2008-10-29',  # Crisis peak
        '2008-12-16',  # Zero rates
        '2020-03-03',  # COVID emergency cut
        '2020-03-15',  # COVID Sunday emergency
        '2020-03-23',  # Peak panic
    ])
    
    print(f"\nCRISIS/EXTREME EVENTS IN DATA:")
    for crisis_date in crisis_dates:
        match = df[df['announcement_date'] == crisis_date]
        if len(match) > 0:
            val = match[col].values[0] * 100
            print(f"  {crisis_date.date()}:  {val:7.2f}%  ← Crisis period")
    
    # Contribution analysis
    sorted_data = data.sort_values(ascending=False)
    top10_contribution = sorted_data.head(10).mean()
    bottom10_contribution = sorted_data.tail(10).mean()
    middle_contribution = sorted_data.iloc[10:-10].mean() if len(data) > 20 else np.nan
    
    print(f"\nCONTRIBUTION ANALYSIS:")
    print(f"  Top 10 events average:    {top10_contribution*100:7.3f}%")
    print(f"  Bottom 10 events average: {bottom10_contribution*100:7.3f}%")
    if not np.isnan(middle_contribution):
        print(f"  Middle events average:    {middle_contribution*100:7.3f}%")
    
    # Removal test
    mean_full = data.mean()
    mean_without_top5 = data.sort_values(ascending=False).iloc[5:].mean()
    mean_without_bottom5 = data.sort_values(ascending=False).iloc[:-5].mean()
    mean_without_extremes = data.sort_values(ascending=False).iloc[5:-5].mean()
    
    print(f"\nSTABILITY TEST (dropping extreme events):")
    print(f"  Full sample mean:           {mean_full*100:7.3f}%")
    print(f"  Drop top 5 events:          {mean_without_top5*100:7.3f}%  (change: {(mean_without_top5-mean_full)*100:+.3f}%)")
    print(f"  Drop bottom 5 events:       {mean_without_bottom5*100:7.3f}%  (change: {(mean_without_bottom5-mean_full)*100:+.3f}%)")
    print(f"  Drop top AND bottom 5:      {mean_without_extremes*100:7.3f}%  (change: {(mean_without_extremes-mean_full)*100:+.3f}%)")
    
    # If dropping extremes changes mean by >20%, outliers dominate
    if abs(mean_without_extremes - mean_full) / abs(mean_full) > 0.20:
        print("  ⚠️  WARNING: Dropping 10 events changes mean by >20%!")
        print("      → Results are HEAVILY influenced by outliers")
        print("      → Consider using median or winsorized mean instead")

# Create distribution plots
print("\n" + "="*80)
print("CREATING DISTRIBUTION PLOTS")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for idx, (window_name, col) in enumerate(list(windows.items())[:3]):  # First 3 windows
    if col not in df.columns:
        continue
    
    row = idx // 2
    col_idx = idx % 2
    ax = axes[row, col_idx]
    
    data = df[col].dropna().values * 100
    
    # Histogram with mean and median
    ax.hist(data, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
    ax.axvline(np.mean(data), color='red', linestyle='--', linewidth=2.5, 
               label=f'Mean: {np.mean(data):.2f}%')
    ax.axvline(np.median(data), color='green', linestyle='--', linewidth=2.5, 
               label=f'Median: {np.median(data):.2f}%')
    ax.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    ax.set_xlabel('H-L Spread (%)', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title(f'{window_name}\n({len(data)} events)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

# Last panel: Q-Q plot for announcement day
ax = axes[1, 1]
if 'pre_ew_H-L' in df.columns:
    data = df['pre_ew_H-L'].dropna().values
    from scipy import stats as sp_stats
    sp_stats.probplot(data, dist="norm", plot=ax)
    ax.set_title('Q-Q Plot: Announcement Day\n(Tests for normality)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

plt.tight_layout()

output_path = os.path.expanduser(
    '~/Desktop/Thesis Materials/cnnthesis/CACHE_DIR/fomc/outlier_diagnostics.png'
)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {output_path}")

print("\n" + "="*80)
print("OUTLIER DIAGNOSTICS COMPLETE")
print("="*80)
print("\nRECOMMENDATIONS:")
print("1. If mean ≈ median and winsorized ≈ mean → Outliers not driving results ✅")
print("2. If mean >> median or winsorized << mean → Outliers dominate ⚠️")
print("3. If stability test shows >20% change → Results fragile ⚠️")
print("4. If crisis events in top 10 → Consider excluding crisis periods")
print("\nSee figure for visual assessment of distributions.")


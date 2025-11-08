#!/usr/bin/env python3
"""
Test ALL horizons from 1 to 20 days (no cherry-picking).

This addresses Issue #8: Are you only reporting specific horizons that show your pattern?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys

# Add path for imports
sys.path.insert(0, os.path.expanduser('~/Desktop/Thesis Materials/cnnthesis/trend_code_submit'))

from Data.equity_data import processed_US_data
from Data import dgp_config as dcf

print("="*80)
print("COMPREHENSIVE HORIZON TESTING (1-20 Days)")
print("No Cherry-Picking - Test Everything!")
print("="*80)

# Load FOMC dates
fomc_file = os.path.join(str(dcf.CACHE_DIR), "fomc", "fomc_schedule.csv")
fomc_df = pd.read_csv(fomc_file, parse_dates=["announcement_date"])
fomc_dates = set(fomc_df["announcement_date"].dt.date)

print(f"\nFOMC events: {len(fomc_dates)}")

# Load predictions
pred_file = os.path.join(str(dcf.CACHE_DIR), "weekly_prediction_with_rets.csv")
pred = pd.read_csv(pred_file, parse_dates=["Date"])
pred["StockID"] = pred["StockID"].astype(str)
pred = pred[["Date", "StockID", "CNN20D5P", "MarketCap"]].rename(
    columns={"Date": "date", "CNN20D5P": "up_prob"}
)

print(f"Predictions: {len(pred):,}")

# Load daily data
print("\nLoading daily returns...")
df = processed_US_data().copy()

if "cum_log_ret" not in df.columns:
    df["log_ret"] = np.log1p(df["Ret"].astype(float))
    df["cum_log_ret"] = df.groupby(level="StockID")["log_ret"].cumsum(skipna=True)
    df.drop(columns=["log_ret"], inplace=True, errors="ignore")

df = df.reset_index()
df["date"] = pd.to_datetime(df["Date"])

# Compute ALL horizons (1-20 days)
print("\nComputing returns for horizons 1-20 days...")

def horizon_ret(k):
    t = df[["date", "StockID", "cum_log_ret"]].copy()
    t["cum_fwd"] = t.groupby("StockID")["cum_log_ret"].shift(-k)
    r = np.exp(t["cum_fwd"] - t["cum_log_ret"]) - 1
    return t[["date", "StockID"]].assign(**{f"ret_{k}d": r})

# Merge all horizon returns
x = pred.copy()
for h in range(1, 21):
    if h % 5 == 0:
        print(f"  Computing {h}-day returns...")
    ret_h = horizon_ret(h)
    x = x.merge(ret_h, left_on=["date", "StockID"], right_on=["date", "StockID"], how="left")

# Tag FOMC days
x["is_fomc"] = x["date"].dt.date.isin(fomc_dates)

print(f"\nFOMC observations: {x['is_fomc'].sum():,}")
print(f"Non-FOMC observations: {(~x['is_fomc']).sum():,}")

# Compute H-L for each horizon
def decile_hl(data, ret_col):
    d = data.dropna(subset=["up_prob", ret_col]).copy()
    if len(d) < 100:
        return np.nan
    d["decile"] = pd.qcut(d["up_prob"], 10, labels=False, duplicates="drop")
    ew = d.groupby("decile")[ret_col].mean().sort_index()
    return float(ew.iloc[-1] - ew.iloc[0])

results = []

print("\nComputing H-L spreads for all horizons...")

for h in range(1, 21):
    ret_col = f"ret_{h}d"
    
    # FOMC
    fomc_data = x[x["is_fomc"]].copy()
    hl_fomc = decile_hl(fomc_data, ret_col)
    
    # Non-FOMC  
    normal_data = x[~x["is_fomc"]].copy()
    hl_normal = decile_hl(normal_data, ret_col)
    
    diff = hl_fomc - hl_normal if not (np.isnan(hl_fomc) or np.isnan(hl_normal)) else np.nan
    
    results.append({
        "horizon": h,
        "FOMC_EW": hl_fomc,
        "Normal_EW": hl_normal,
        "Difference": diff,
        "FOMC_higher": diff > 0 if not np.isnan(diff) else None
    })
    
    print(f"  {h:2d} days: FOMC={hl_fomc*100:6.2f}%  Normal={hl_normal*100:6.2f}%  Diff={diff*100:+6.2f}%")

# Create results dataframe
results_df = pd.DataFrame(results)

# Save
out_path = os.path.expanduser(
    '~/Desktop/Thesis Materials/cnnthesis/CACHE_DIR/fomc/all_horizons_comparison.csv'
)
results_df.to_csv(out_path, index=False)
print(f"\n✅ Saved: {out_path}")

# Analysis
print("\n" + "="*80)
print("PATTERN ANALYSIS")
print("="*80)

# Count how many horizons show each pattern
fomc_higher = results_df[results_df["FOMC_higher"] == True]
normal_higher = results_df[results_df["FOMC_higher"] == False]

print(f"\nHorizons where FOMC > Normal: {len(fomc_higher)}/20")
print(f"Horizons where Normal > FOMC: {len(normal_higher)}/20")

# Check for consistent pattern
print(f"\n✅ CONSISTENCY CHECK:")
print(f"Days 1-2: {results_df[results_df['horizon'] <= 2]['FOMC_higher'].value_counts().to_dict()}")
print(f"Days 3-5: {results_df[(results_df['horizon'] >= 3) & (results_df['horizon'] <= 5)]['FOMC_higher'].value_counts().to_dict()}")
print(f"Days 6-10: {results_df[(results_df['horizon'] >= 6) & (results_df['horizon'] <= 10)]['FOMC_higher'].value_counts().to_dict()}")
print(f"Days 11-20: {results_df[results_df['horizon'] >= 11]['FOMC_higher'].value_counts().to_dict()}")

# Transition point
first_fomc_higher = results_df[results_df["FOMC_higher"] == True]["horizon"].min()
print(f"\nFirst horizon where FOMC > Normal: Day {first_fomc_higher}")

# Plot
print("\nCreating comprehensive plot...")

fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Plot 1: H-L spreads
ax1 = axes[0]
horizons = results_df["horizon"].values
fomc_vals = results_df["FOMC_EW"].values * 100
normal_vals = results_df["Normal_EW"].values * 100

ax1.plot(horizons, fomc_vals, 'o-', linewidth=2, markersize=6, label='FOMC Days', color='red')
ax1.plot(horizons, normal_vals, 's-', linewidth=2, markersize=6, label='Non-FOMC Days', color='blue')
ax1.axhline(0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
ax1.set_xlabel('Horizon (days)', fontsize=12)
ax1.set_ylabel('H-L Spread (%)', fontsize=12)
ax1.set_title('H-L Spreads: All Horizons (1-20 Days)', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11, loc='best')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(1, 21))

# Mark your originally reported horizons
for h in [1, 3, 10]:
    ax1.axvline(h, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    ax1.text(h, ax1.get_ylim()[1]*0.95, f'{h}d\n(reported)', ha='center', fontsize=8)

# Plot 2: Difference (FOMC - Normal)
ax2 = axes[1]
diff_vals = results_df["Difference"].values * 100

# Color code by sign
colors = ['red' if d > 0 else 'blue' if d < 0 else 'gray' for d in diff_vals]
ax2.bar(horizons, diff_vals, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
ax2.axhline(0, color='black', linestyle='-', linewidth=2)
ax2.set_xlabel('Horizon (days)', fontsize=12)
ax2.set_ylabel('Difference: FOMC - Normal (%)', fontsize=12)
ax2.set_title('Difference by Horizon (Red=FOMC Higher, Blue=Normal Higher)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_xticks(range(1, 21))

# Mark transition point
if not np.isnan(first_fomc_higher):
    ax2.axvline(first_fomc_higher, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax2.text(first_fomc_higher, ax2.get_ylim()[1]*0.9, 
             f'Transition\nat day {first_fomc_higher}', ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.tight_layout()

fig_path = os.path.expanduser(
    '~/Desktop/Thesis Materials/cnnthesis/CACHE_DIR/fomc/all_horizons_plot.png'
)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {fig_path}")

plt.close()

# Assessment
print("\n" + "="*80)
print("ASSESSMENT")
print("="*80)

print("""
WHAT TO LOOK FOR:

✅ GOOD SIGNS (Pattern is real):
- Clear transition at specific horizon (e.g., day 2 or 3)
- Consistent within phases (days 1-2 all Normal>FOMC, days 3-10 all FOMC>Normal)
- Smooth progression (no wild jumps)

⚠️  WARNING SIGNS (Might be noise):
- No clear pattern (alternates randomly)
- Wild jumps between adjacent horizons
- Only 1-2 horizons show the pattern you want
- Results at days 1,3,10 are outliers compared to neighbors

❌ BAD SIGNS (Likely cherry-picking):
- Days 2,4,5,6,7,8,9 show opposite pattern
- Only your pre-selected horizons (1,3,10) show effect
- No consistency across horizon ranges

NEXT STEPS:
1. Look at the plot
2. Check if pattern is smooth and consistent
3. If yes → Your results hold up! ✅
4. If no → You may have cherry-picked horizons ⚠️
""")


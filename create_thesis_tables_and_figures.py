#!/usr/bin/env python3
"""
Create all tables and figures for thesis
Generates publication-ready tables (LaTeX format) and figures (PNG/PDF)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for publication-quality figures matching thesis (Times New Roman)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']  # Times New Roman
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Create output directories
OUTPUT_DIR = Path("thesis_output")
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"

for dir in [OUTPUT_DIR, TABLES_DIR, FIGURES_DIR]:
    dir.mkdir(exist_ok=True)

print("=" * 80)
print("CREATING THESIS TABLES AND FIGURES")
print("=" * 80)
print()

# ============================================================================
# TABLE 1: SAMPLE STATISTICS
# ============================================================================
print("Creating Table 1: Sample Statistics...")

sample_stats = {
    'Description': [
        'Sample Period (Training)',
        'Sample Period (Testing)',
        'Number of Stocks',
        'Number of Weekly Predictions',
        'Number of Stock-Week Observations',
        'Number of FOMC Meetings',
        'Average Stocks per Week',
        'CNN Model Type',
        'Lookback Window',
        'Prediction Horizon',
        'Ensemble Size'
    ],
    'Value': [
        '1993-2000',
        '2001-2024',
        '22,480',
        '~1,200',
        '8,900,000',
        '217',
        '2,500-3,500',
        'Convolutional Neural Network',
        '20 days',
        '5 days',
        '5 models'
    ]
}

df_sample = pd.DataFrame(sample_stats)

# Save as LaTeX
latex_sample = df_sample.to_latex(
    index=False,
    caption='Sample Description and Data Summary',
    label='tab:sample_stats',
    column_format='lc',
    escape=False
)

with open(TABLES_DIR / "table1_sample_statistics.tex", 'w') as f:
    f.write(latex_sample)

print(f"  ✅ Saved: {TABLES_DIR}/table1_sample_statistics.tex")

# Also save as CSV for reference
df_sample.to_csv(TABLES_DIR / "table1_sample_statistics.csv", index=False)

# ============================================================================
# TABLE 2: HORIZON EVALUATION
# ============================================================================
print("\nCreating Table 2: Horizon Evaluation...")

horizon_data = {
    'Horizon': ['1-day', '3-day', '10-day'],
    'EW H-L (%)': [0.87, 1.11, 1.37],
    'VW H-L (%)': [0.09, 0.20, 0.24],
    'EW/VW Ratio': [9.67, 5.55, 5.71]
}

df_horizon = pd.DataFrame(horizon_data)

latex_horizon = df_horizon.to_latex(
    index=False,
    caption='CNN Predictive Power Across Different Forecast Horizons. H-L represents the high-minus-low portfolio spread.',
    label='tab:horizon_eval',
    column_format='lccc',
    float_format='%.2f',
    escape=False
)

with open(TABLES_DIR / "table2_horizon_evaluation.tex", 'w') as f:
    f.write(latex_horizon)

print(f"  ✅ Saved: {TABLES_DIR}/table2_horizon_evaluation.tex")
df_horizon.to_csv(TABLES_DIR / "table2_horizon_evaluation.csv", index=False)

# ============================================================================
# TABLE 3: PORTFOLIO PERFORMANCE (EQUAL-WEIGHT)
# ============================================================================
print("\nCreating Table 3: Portfolio Performance (Equal-Weight)...")

ew_data = {
    'Decile': ['Low (1)', '2', '3', '4', '5', '6', '7', '8', '9', 'High (10)', 'H-L'],
    'Annual Return (%)': [-28.08, -2.20, 5.75, 10.63, 12.25, 15.25, 17.43, 20.73, 24.10, 42.66, 70.74],
    'Volatility (%)': [18.07, 19.52, 19.94, 20.02, 19.98, 20.04, 19.96, 20.05, 19.91, 19.09, 12.64],
    'Sharpe Ratio': [-1.55, -0.11, 0.29, 0.53, 0.61, 0.76, 0.87, 1.03, 1.21, 2.23, 5.60]
}

df_ew = pd.DataFrame(ew_data)

latex_ew = df_ew.to_latex(
    index=False,
    caption='Equal-Weighted Portfolio Performance by CNN Prediction Decile (2001-2024). Decile 1 (Low) contains stocks with lowest predicted up-probability, Decile 10 (High) contains highest. H-L is the long-short spread (High minus Low).',
    label='tab:portfolio_ew',
    column_format='lccc',
    float_format='%.2f',
    escape=False
)

with open(TABLES_DIR / "table3_portfolio_ew.tex", 'w') as f:
    f.write(latex_ew)

print(f"  ✅ Saved: {TABLES_DIR}/table3_portfolio_ew.tex")
df_ew.to_csv(TABLES_DIR / "table3_portfolio_ew.csv", index=False)

# ============================================================================
# TABLE 4: PORTFOLIO PERFORMANCE (VALUE-WEIGHT)
# ============================================================================
print("\nCreating Table 4: Portfolio Performance (Value-Weight)...")

vw_data = {
    'Decile': ['Low (1)', '2', '3', '4', '5', '6', '7', '8', '9', 'High (10)', 'H-L'],
    'Annual Return (%)': [-3.50, 4.06, 6.64, 7.79, 8.06, 10.45, 9.39, 11.79, 12.23, 19.19, 22.69],
    'Volatility (%)': [18.73, 19.34, 19.03, 19.20, 19.22, 18.99, 18.80, 18.99, 19.02, 20.78, 14.75],
    'Sharpe Ratio': [-0.19, 0.21, 0.35, 0.41, 0.42, 0.55, 0.50, 0.62, 0.64, 0.92, 1.54]
}

df_vw = pd.DataFrame(vw_data)

latex_vw = df_vw.to_latex(
    index=False,
    caption='Value-Weighted Portfolio Performance by CNN Prediction Decile (2001-2024). Portfolios weighted by market capitalization. H-L spread is substantially smaller than equal-weight, indicating effect is concentrated in smaller stocks.',
    label='tab:portfolio_vw',
    column_format='lccc',
    float_format='%.2f',
    escape=False
)

with open(TABLES_DIR / "table4_portfolio_vw.tex", 'w') as f:
    f.write(latex_vw)

print(f"  ✅ Saved: {TABLES_DIR}/table4_portfolio_vw.tex")
df_vw.to_csv(TABLES_DIR / "table4_portfolio_vw.csv", index=False)

# ============================================================================
# TABLE 5: FOMC EVENT STUDY (MAIN CONTRIBUTION)
# ============================================================================
print("\nCreating Table 5: FOMC Event Study Results...")

fomc_data = {
    'Window': [
        'Announcement Day (t)',
        '',
        'Reaction (t+1)',
        '',
        'Intermediate (t+5 to t+20)',
        ''
    ],
    'Weight': ['EW', 'VW', 'EW', 'VW', 'EW', 'VW'],
    'Mean H-L (%)': [0.21, 0.05, 0.10, 0.03, 0.35, -0.28],
    't-statistic': [2.95, 0.66, 1.76, 0.38, 2.24, -1.57],
    'p-value': [0.004, 0.508, 0.079, 0.707, 0.026, 0.118],
    'Significance': ['***', '', '*', '', '**', ''],
    'N Events': [217, 217, 215, 215, 208, 208]
}

df_fomc = pd.DataFrame(fomc_data)

latex_fomc = df_fomc.to_latex(
    index=False,
    caption='CNN Performance Around FOMC Announcements (2001-2024). H-L represents high-minus-low portfolio spread. Announcement Day (t) is the day the Fed releases its decision. Reaction (t+1) is the next trading day. Intermediate (t+5 to t+20) is the cumulative return 5-20 days after announcement. *** p<0.01, ** p<0.05, * p<0.10.',
    label='tab:fomc_results',
    column_format='llccccr',
    float_format='%.2f',
    escape=False
)

with open(TABLES_DIR / "table5_fomc_results.tex", 'w') as f:
    f.write(latex_fomc)

print(f"  ✅ Saved: {TABLES_DIR}/table5_fomc_results.tex")
df_fomc.to_csv(TABLES_DIR / "table5_fomc_results.csv", index=False)

# ============================================================================
# TABLE 6: COMPARISON EW vs VW ACROSS ALL TESTS
# ============================================================================
print("\nCreating Table 6: EW vs VW Comparison...")

comparison_data = {
    'Test': [
        'Overall Portfolio (Annual)',
        'Horizon: 1-day',
        'Horizon: 3-day',
        'Horizon: 10-day',
        'FOMC: Announcement',
        'FOMC: Reaction',
        'FOMC: Intermediate'
    ],
    'EW H-L': ['70.74%', '0.87%', '1.11%', '1.37%', '0.21%***', '0.10%*', '0.35%**'],
    'VW H-L': ['22.69%', '0.09%', '0.20%', '0.24%', '0.05%', '0.03%', '-0.28%'],
    'EW/VW Ratio': [3.12, 9.67, 5.55, 5.71, 4.20, 3.33, None]
}

df_comparison = pd.DataFrame(comparison_data)

latex_comparison = df_comparison.to_latex(
    index=False,
    caption='Comparison of Equal-Weight vs Value-Weight H-L Spreads Across All Tests. Ratio shows EW/VW multiple. Consistently higher EW spreads indicate effect is concentrated in small-capitalization stocks. *** p<0.01, ** p<0.05, * p<0.10.',
    label='tab:ew_vw_comparison',
    column_format='lccc',
    escape=False
)

with open(TABLES_DIR / "table6_ew_vw_comparison.tex", 'w') as f:
    f.write(latex_comparison)

print(f"  ✅ Saved: {TABLES_DIR}/table6_ew_vw_comparison.tex")
df_comparison.to_csv(TABLES_DIR / "table6_ew_vw_comparison.csv", index=False)

# ============================================================================
# FIGURE 1: TIMELINE DIAGRAM (No Overlap)
# ============================================================================
print("\nCreating Figure 1: FOMC Timeline (No Overlap)...")

fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('off')

# Timeline
timeline_y = 0.5
ax.plot([0, 10], [timeline_y, timeline_y], 'k-', linewidth=2)

# Key dates
dates = {
    'June 5': 1,
    'June 12': 3,
    'June 15': 5,
    'June 16': 6,
    'June 19': 7,
    'July 13': 9
}

# Labels and descriptions
labels = {
    1: ('June 5\n(pred?)', 0.25),
    3: ('June 12\n(pred?)', 0.25),
    5: ('June 15\n(t)', 0.75),
    6: ('June 16\n(t+1)', 0.75),
    7: ('June 19\n(t+5)', 0.75),
    9: ('July 13\n(t+20)', 0.75)
}

# Plot markers
for date, x in dates.items():
    ax.plot(x, timeline_y, 'ko', markersize=10)

# Add labels
for x, (label, y) in labels.items():
    ax.text(x, y, label, ha='center', va='center', fontsize=9)

# Add spans
# Prediction made here
ax.annotate('', xy=(3, 0.4), xytext=(3, 0.15),
            arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
ax.text(3, 0.05, 'PREDICTION\nMADE HERE', ha='center', fontsize=10,
        fontweight='bold', color='blue')

# CNN Lookback
ax.plot([1, 3], [0.35, 0.35], 'b-', linewidth=3, alpha=0.7)
ax.text(2, 0.28, 'CNN Lookback\n(20 days)', ha='center', fontsize=8, color='blue')

# FOMC Event
ax.annotate('', xy=(5, 0.85), xytext=(5, 0.6),
            arrowprops=dict(arrowstyle='->', lw=2, color='red'))
ax.text(5, 0.95, 'FOMC\nANNOUNCEMENT', ha='center', fontsize=10,
        fontweight='bold', color='red')

# Returns measured
ax.plot([5, 9], [0.85, 0.85], 'g-', linewidth=4, alpha=0.7)
ax.text(7, 0.92, 'Returns Measured →→→', ha='center', fontsize=9,
        fontweight='bold', color='green')

# No overlap region
ax.axvspan(3.2, 4.8, alpha=0.2, color='gray')
ax.text(4, 0.5, 'GAP\n(No Overlap)', ha='center', fontsize=9,
        style='italic')

ax.set_xlim(0, 10)
ax.set_ylim(0, 1)
ax.set_title('FOMC Event Study Timeline: Temporal Ordering (No Overlap)',
             fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure1_fomc_timeline.png", bbox_inches='tight', dpi=300)
plt.savefig(FIGURES_DIR / "figure1_fomc_timeline.pdf", bbox_inches='tight')
plt.close()

print(f"  ✅ Saved: {FIGURES_DIR}/figure1_fomc_timeline.png/.pdf")

# ============================================================================
# FIGURE 2: DECILE PERFORMANCE COMPARISON
# ============================================================================
print("\nCreating Figure 2: Decile Performance...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Annual Returns
deciles = ['1\n(Low)', '2', '3', '4', '5', '6', '7', '8', '9', '10\n(High)']
x = np.arange(len(deciles))
width = 0.35

ew_returns = [-28.08, -2.20, 5.75, 10.63, 12.25, 15.25, 17.43, 20.73, 24.10, 42.66]
vw_returns = [-3.50, 4.06, 6.64, 7.79, 8.06, 10.45, 9.39, 11.79, 12.23, 19.19]

ax1.bar(x - width/2, ew_returns, width, label='Equal-Weight', alpha=0.8, color='steelblue')
ax1.bar(x + width/2, vw_returns, width, label='Value-Weight', alpha=0.8, color='coral')

ax1.set_xlabel('CNN Prediction Decile', fontweight='bold')
ax1.set_ylabel('Annual Return (%)', fontweight='bold')
ax1.set_title('Panel A: Portfolio Returns by Decile', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(deciles)
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Panel B: Sharpe Ratios
ew_sharpe = [-1.55, -0.11, 0.29, 0.53, 0.61, 0.76, 0.87, 1.03, 1.21, 2.23]
vw_sharpe = [-0.19, 0.21, 0.35, 0.41, 0.42, 0.55, 0.50, 0.62, 0.64, 0.92]

ax2.bar(x - width/2, ew_sharpe, width, label='Equal-Weight', alpha=0.8, color='steelblue')
ax2.bar(x + width/2, vw_sharpe, width, label='Value-Weight', alpha=0.8, color='coral')

ax2.set_xlabel('CNN Prediction Decile', fontweight='bold')
ax2.set_ylabel('Sharpe Ratio', fontweight='bold')
ax2.set_title('Panel B: Risk-Adjusted Performance', fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(deciles)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.suptitle('CNN Portfolio Performance (2001-2024)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure2_decile_performance.png", bbox_inches='tight', dpi=300)
plt.savefig(FIGURES_DIR / "figure2_decile_performance.pdf", bbox_inches='tight')
plt.close()

print(f"  ✅ Saved: {FIGURES_DIR}/figure2_decile_performance.png/.pdf")

# ============================================================================
# FIGURE 3: HORIZON EVALUATION
# ============================================================================
print("\nCreating Figure 3: Horizon Evaluation...")

fig, ax = plt.subplots(figsize=(10, 6))

horizons = [1, 3, 10]
ew_hl = [0.87, 1.11, 1.37]
vw_hl = [0.09, 0.20, 0.24]

ax.plot(horizons, ew_hl, 'o-', linewidth=3, markersize=10, label='Equal-Weight', color='steelblue')
ax.plot(horizons, vw_hl, 's-', linewidth=3, markersize=10, label='Value-Weight', color='coral')

ax.set_xlabel('Forecast Horizon (Days)', fontweight='bold', fontsize=12)
ax.set_ylabel('H-L Spread (%)', fontweight='bold', fontsize=12)
ax.set_title('CNN Predictive Power Increases with Forecast Horizon', fontweight='bold', fontsize=13)
ax.set_xticks(horizons)
ax.legend(fontsize=11)
ax.grid(alpha=0.3)

# Add annotations
for i, (h, ew, vw) in enumerate(zip(horizons, ew_hl, vw_hl)):
    ax.text(h, ew + 0.05, f'{ew:.2f}%', ha='center', fontweight='bold', color='steelblue')
    ax.text(h, vw + 0.05, f'{vw:.2f}%', ha='center', fontweight='bold', color='coral')

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure3_horizon_evaluation.png", bbox_inches='tight', dpi=300)
plt.savefig(FIGURES_DIR / "figure3_horizon_evaluation.pdf", bbox_inches='tight')
plt.close()

print(f"  ✅ Saved: {FIGURES_DIR}/figure3_horizon_evaluation.png/.pdf")

# ============================================================================
# FIGURE 4: FOMC RESULTS
# ============================================================================
print("\nCreating Figure 4: FOMC Event Study Results...")

fig, ax = plt.subplots(figsize=(10, 6))

windows = ['Announcement\nDay (t)', 'Reaction\n(t+1)', 'Intermediate\n(t+5 to t+20)']
x = np.arange(len(windows))
width = 0.35

ew_fomc = [0.21, 0.10, 0.35]
vw_fomc = [0.05, 0.03, -0.28]

# Significance stars
ew_sig = ['***', '*', '**']
vw_sig = ['', '', '']

bars1 = ax.bar(x - width/2, ew_fomc, width, label='Equal-Weight', alpha=0.8, color='steelblue')
bars2 = ax.bar(x + width/2, vw_fomc, width, label='Value-Weight', alpha=0.8, color='coral')

ax.set_xlabel('Event Window', fontweight='bold', fontsize=12)
ax.set_ylabel('H-L Spread (%)', fontweight='bold', fontsize=12)
ax.set_title('CNN Performance Around FOMC Announcements (217 Events, 2001-2024)',
             fontweight='bold', fontsize=13)
ax.set_xticks(x)
ax.set_xticklabels(windows)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Add significance stars
for i, (ew, sig) in enumerate(zip(ew_fomc, ew_sig)):
    if sig:
        y_pos = ew + 0.03 if ew > 0 else ew - 0.03
        ax.text(i - width/2, y_pos, sig, ha='center', fontsize=14, fontweight='bold')

# Add value labels
for i, (ew, vw) in enumerate(zip(ew_fomc, vw_fomc)):
    ax.text(i - width/2, ew + 0.02, f'{ew:.2f}%', ha='center', fontsize=9, fontweight='bold')
    ax.text(i + width/2, vw + 0.02, f'{vw:.2f}%', ha='center', fontsize=9, fontweight='bold')

# Add note
ax.text(0.5, -0.35, '*** p<0.01, ** p<0.05, * p<0.10',
        ha='center', transform=ax.transAxes, fontsize=9, style='italic')

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure4_fomc_results.png", bbox_inches='tight', dpi=300)
plt.savefig(FIGURES_DIR / "figure4_fomc_results.pdf", bbox_inches='tight')
plt.close()

print(f"  ✅ Saved: {FIGURES_DIR}/figure4_fomc_results.png/.pdf")

# ============================================================================
# FIGURE 5: EW vs VW COMPARISON ACROSS ALL TESTS
# ============================================================================
print("\nCreating Figure 5: EW vs VW Comparison...")

fig, ax = plt.subplots(figsize=(12, 6))

tests = ['Overall\n(Annual)', '1-day', '3-day', '10-day',
         'FOMC:\nAnnounce', 'FOMC:\nReact', 'FOMC:\nInter']
x = np.arange(len(tests))
width = 0.35

ew_all = [70.74, 0.87, 1.11, 1.37, 0.21, 0.10, 0.35]
vw_all = [22.69, 0.09, 0.20, 0.24, 0.05, 0.03, -0.28]

bars1 = ax.bar(x - width/2, ew_all, width, label='Equal-Weight (Small Caps)', alpha=0.8, color='steelblue')
bars2 = ax.bar(x + width/2, vw_all, width, label='Value-Weight (Large Caps)', alpha=0.8, color='coral')

ax.set_xlabel('Test', fontweight='bold', fontsize=12)
ax.set_ylabel('H-L Spread (%)', fontweight='bold', fontsize=12)
ax.set_title('Small-Cap Concentration: EW Consistently Outperforms VW Across All Tests',
             fontweight='bold', fontsize=13)
ax.set_xticks(x)
ax.set_xticklabels(tests)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax.legend(fontsize=11, loc='upper left')
ax.grid(axis='y', alpha=0.3)

# Add ratio annotations for first 4 bars
ratios = [3.12, 9.67, 5.55, 5.71]
for i, ratio in enumerate(ratios):
    y_max = max(ew_all[i], vw_all[i])
    ax.text(i, y_max + 2, f'{ratio:.1f}x', ha='center', fontsize=9,
            fontweight='bold', color='darkgreen')

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure5_ew_vw_comparison.png", bbox_inches='tight', dpi=300)
plt.savefig(FIGURES_DIR / "figure5_ew_vw_comparison.pdf", bbox_inches='tight')
plt.close()

print(f"  ✅ Saved: {FIGURES_DIR}/figure5_ew_vw_comparison.png/.pdf")

# ============================================================================
# FIGURE 6: CNN ARCHITECTURE (SIMPLIFIED DIAGRAM)
# ============================================================================
print("\nCreating Figure 6: CNN Architecture Diagram...")

fig, ax = plt.subplots(figsize=(14, 6))
ax.axis('off')
ax.set_xlim(0, 14)
ax.set_ylim(0, 6)

# Title
ax.text(7, 5.5, 'CNN Architecture for Stock Return Prediction', ha='center',
        fontsize=14, fontweight='bold')

# Input layer
ax.add_patch(plt.Rectangle((0.5, 2), 1.5, 2, fill=True, color='lightblue', alpha=0.7))
ax.text(1.25, 3, 'INPUT\n20-day\nPrice Chart\n(32×32)', ha='center', va='center',
        fontsize=9, fontweight='bold')
ax.text(1.25, 1.5, 'Example:\nMay 18 -\nJune 12', ha='center', fontsize=7, style='italic')

# Conv layers
conv_positions = [(2.5, 2.25), (4.5, 2.25), (6.5, 2.25)]
conv_labels = ['Conv Layer 1\n+ Pooling', 'Conv Layer 2\n+ Pooling', 'Conv Layer 3\n+ Pooling']

for i, (x, y) in enumerate(conv_positions):
    ax.add_patch(plt.Rectangle((x, y), 1.2, 1.5, fill=True, color='lightcoral', alpha=0.7))
    ax.text(x + 0.6, y + 0.75, conv_labels[i], ha='center', va='center',
            fontsize=8, fontweight='bold')
    ax.text(x + 0.6, y - 0.3, 'Detects\nPatterns', ha='center', fontsize=7, style='italic')

# Fully connected layers
fc_positions = [(8.5, 2.5), (10.5, 2.5)]
fc_labels = ['Fully\nConnected\nLayer 1', 'Fully\nConnected\nLayer 2']

for i, (x, y) in enumerate(fc_positions):
    ax.add_patch(plt.Rectangle((x, y), 1.2, 1, fill=True, color='lightgreen', alpha=0.7))
    ax.text(x + 0.6, y + 0.5, fc_labels[i], ha='center', va='center',
            fontsize=8, fontweight='bold')

# Output layer
ax.add_patch(plt.Rectangle((12.5, 2.5), 1.2, 1, fill=True, color='gold', alpha=0.7))
ax.text(13.1, 3, 'OUTPUT\nUp-Prob\n(0 to 1)', ha='center', va='center',
        fontsize=9, fontweight='bold')
ax.text(13.1, 1.9, 'Example:\n0.73', ha='center', fontsize=7, style='italic')

# Arrows
arrow_props = dict(arrowstyle='->', lw=2, color='black')
for i in range(len(conv_positions) - 1):
    ax.annotate('', xy=(conv_positions[i+1][0], 3), xytext=(conv_positions[i][0] + 1.2, 3),
                arrowprops=arrow_props)

ax.annotate('', xy=(fc_positions[0][0], 3), xytext=(conv_positions[-1][0] + 1.2, 3),
            arrowprops=arrow_props)
ax.annotate('', xy=(fc_positions[1][0], 3), xytext=(fc_positions[0][0] + 1.2, 3),
            arrowprops=arrow_props)
ax.annotate('', xy=(12.5, 3), xytext=(fc_positions[1][0] + 1.2, 3),
            arrowprops=arrow_props)
ax.annotate('', xy=(conv_positions[0][0], 3), xytext=(2, 3),
            arrowprops=arrow_props)

# Add bottom annotation
ax.text(7, 0.5, 'Like how a radiologist detects patterns in X-rays,\nCNN detects visual patterns in stock price charts',
        ha='center', fontsize=10, style='italic', color='darkblue')

plt.tight_layout()
plt.savefig(FIGURES_DIR / "figure6_cnn_architecture.png", bbox_inches='tight', dpi=300)
plt.savefig(FIGURES_DIR / "figure6_cnn_architecture.pdf", bbox_inches='tight')
plt.close()

print(f"  ✅ Saved: {FIGURES_DIR}/figure6_cnn_architecture.png/.pdf")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY: ALL TABLES AND FIGURES CREATED")
print("=" * 80)
print()
print(f"📁 Output Directory: {OUTPUT_DIR}/")
print()
print("📊 TABLES (LaTeX + CSV):")
print("  1. table1_sample_statistics")
print("  2. table2_horizon_evaluation")
print("  3. table3_portfolio_ew")
print("  4. table4_portfolio_vw")
print("  5. table5_fomc_results (MAIN CONTRIBUTION)")
print("  6. table6_ew_vw_comparison")
print()
print("📈 FIGURES (PNG + PDF):")
print("  1. figure1_fomc_timeline (no overlap)")
print("  2. figure2_decile_performance")
print("  3. figure3_horizon_evaluation")
print("  4. figure4_fomc_results (MAIN CONTRIBUTION)")
print("  5. figure5_ew_vw_comparison")
print("  6. figure6_cnn_architecture")
print()
print("✅ All files saved in: thesis_output/")
print("   - tables/ (LaTeX .tex files for direct inclusion)")
print("   - figures/ (PNG for Word, PDF for LaTeX)")
print()
print("🎯 NEXT STEPS:")
print("   1. Review all tables/figures")
print("   2. Include in your thesis")
print("   3. For LaTeX: Use \\input{tables/table1_sample_statistics.tex}")
print("   4. For Word: Insert PNG files from figures/")
print()
print("=" * 80)


#!/usr/bin/env python3
"""
Create a composite figure showing example CNN input images
Shows what the CNN "sees" when making predictions
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

# Set style for Times New Roman
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['font.size'] = 10

# Output directory
OUTPUT_DIR = Path("~/Desktop/Thesis_Results/thesis_output/figures").expanduser()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Sample image directory
SAMPLE_DIR = Path("WORK_SPACE/data/stocks_dataset/sample_images")

# Select diverse examples
examples = [
    ("20d_week_has_vb_[20]_ma_2013_10001_20130104.png", "Uptrend Pattern\n(2013)"),
    ("20d_week_has_vb_[20]_ma_2008_10001_20080104.png", "Downtrend Pattern\n(2008 Crisis)"),
    ("20d_week_has_vb_[20]_ma_2020_10026_20200103.png", "High Volatility\n(2020 COVID)"),
    ("20d_week_has_vb_[20]_ma_2005_10001_20050107.png", "Sideways Pattern\n(2005)"),
]

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

for idx, (filename, label) in enumerate(examples):
    img_path = SAMPLE_DIR / filename
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        axes[idx].imshow(img, cmap='gray')
        axes[idx].set_title(label, fontweight='bold', fontsize=11)
        axes[idx].axis('off')
    else:
        # If file doesn't exist, show alternative
        axes[idx].text(0.5, 0.5, 'Image not available', ha='center', va='center')
        axes[idx].set_title(label, fontweight='bold', fontsize=11)
        axes[idx].axis('off')

# Overall title
fig.suptitle('Examples of 20-Day Price Chart Images Used as CNN Input\n(32×32 pixels, grayscale)', 
             fontsize=13, fontweight='bold', y=0.98)

# Add note at bottom
fig.text(0.5, 0.02, 
         'Each image represents 20 trading days of normalized price movements.\n'
         'CNN learns to recognize visual patterns (trends, reversals, support/resistance) that predict future returns.',
         ha='center', fontsize=9, style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 0.96])

# Save
output_path = OUTPUT_DIR / "figure9_sample_price_charts.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "figure9_sample_price_charts.pdf", dpi=300, bbox_inches='tight')
plt.close()

print("=" * 80)
print("SAMPLE PRICE CHART FIGURE CREATED")
print("=" * 80)
print()
print(f"✅ Saved: {output_path}")
print(f"✅ Saved: {OUTPUT_DIR / 'figure9_sample_price_charts.pdf'}")
print()
print("📊 Figure shows 4 example price charts:")
print("  1. Uptrend pattern (2013)")
print("  2. Downtrend pattern (2008 crisis)")
print("  3. High volatility (2020 COVID)")
print("  4. Sideways pattern (2005)")
print()
print("💡 Use this in your Methodology section to show what CNN input looks like!")
print()
print("Suggested caption:")
print("  'Figure X: Examples of 20-Day Price Chart Images Used as CNN Input.")
print("   Each 32×32 pixel grayscale image represents normalized price movements")
print("   over 20 trading days. The CNN learns to detect visual patterns—such as")
print("   trends, reversals, and support/resistance levels—that predict future returns.'")
print()
print("=" * 80)


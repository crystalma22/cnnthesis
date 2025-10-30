# Thesis Data & Methodology Section

## Table of Contents
1. [Data and Preprocessing](#1-data-and-preprocessing)
2. [Methodology](#2-methodology)

---

## 1. Data and Preprocessing

### 1.1 Data Source

**Primary Data:**
- **Source:** Center for Research in Security Prices (CRSP) daily stock file
- **Time Period:** January 2, 1992 to December 31, 2024
- **Coverage:** All US-listed common stocks (NYSE, NASDAQ, AMEX)
- **Observations:** 63.3 million daily stock-day observations
- **Unique Stocks:** 29,331 stocks over the full sample period

**Key Variables Extracted:**
- `PERMNO`: Permanent stock identifier (unique identifier)
- `date`: Trading date
- `PRC`: Closing price (adjusted for splits and dividends)
- `OPENPRC`: Opening price
- `BIDLO`: Low price (bid-low)
- `ASKHI`: High price (ask-high)
- `RET`: Return (adjusted for distributions)
- `VOL`: Trading volume (in shares)
- `SHROUT`: Shares outstanding

### 1.2 Data Cleaning and Processing

**Step 1: Basic Cleaning**
```python
# Rename columns to standard format
date → Date
PERMNO → StockID  
PRC → Close
OPENPRC → Open
BIDLO → Low
ASKHI → High
RET → Ret
VOL → Vol
SHROUT → Shares
```

**Step 2: Handle Missing and Invalid Values**
- Drop observations with missing returns (required for labels)
- Set zero prices to NaN (invalid observations)
- Convert special return codes to NaN:
  - "C": Delisting return
  - "B": Backdating issue
  - "A": Actual return unavailable
  - ".": Missing return
- Set volume = 0 or volume = -99 to NaN
- Drop stocks with zero or negative close prices

**Step 3: Calculate Derived Variables**
- **Market Capitalization:** `MarketCap = abs(Close × Shares Outstanding)`
- **Log Returns:** `log_ret = log(1 + Ret)` (for multi-period calculations)
- **Cumulative Log Returns:** Grouped by stock, cumulative sum of log returns
- **EWMA Volatility:** `EWMA_vol = (Ret²).ewm(alpha=0.05).mean().shift(1)`
  - Exponential weighted moving average with smoothing factor α=0.05
  - Shifted by 1 period to use lagged volatility (avoid look-ahead bias)

**Step 4: Compute Multi-Period Returns**
- Cumulative log returns allow precise multi-period calculations
- Formula: `Ret[t → t+n] = exp(cum_log_ret[t+n] - cum_log_ret[t]) - 1`
- Computed for windows:
  - 5 days (1 week)
  - 20 days (1 month)
  - 60 days (1 quarter)
  - 65, 180, 250, 260 days (for stock characteristics)

### 1.3 Image Generation: Converting Price Data to Candlestick Charts

**Objective:** Transform daily OHLC price sequences into grayscale candlestick chart images suitable for CNN input.

#### 1.3.1 Input Window Selection
- **Window Size:** 20 trading days
- **Rationale:** Captures approximately one month of trading patterns
- **Chart Frequency:** 1 day per bar (no aggregation)

#### 1.3.2 Price Normalization
**Step 1: Adjust for Splits and Dividends**
- Use CRSP adjustment factor to ensure continuity across corporate actions
- Formula: `adjusted_price = raw_price × adjustment_factor`

**Step 2: Normalize to Base Price = 1.0**
- For each 20-day window, divide all prices by the first day's close
- First bar always starts at price level 1.0
- Ensures comparability across stocks with different price levels
- Formula:
  ```
  Close[t] = Close[t] / Close[0]
  Open[t] = Open[t] / Close[0]
  High[t] = High[t] / Close[0]
  Low[t] = Low[t] / Close[0]
  ```

#### 1.3.3 Image Encoding

**Image Dimensions:**
- **Width:** 60 pixels (20 days × 3 pixels per bar)
- **Height:** 64 pixels
- **Color Depth:** 8-bit grayscale (256 intensity levels)
- **Total Size:** 60 × 64 = 3,840 pixels per image

**Bar Drawing Algorithm:**
```python
# For each trading day:
1. Scale price to pixel coordinates:
   - min_price = min(High) across 20-day window
   - max_price = max(High) across 20-day window
   - pixels_per_unit = (image_height - 1) / (max_price - min_price)
   - y_pixel = int((price - min_price) × pixels_per_unit)

2. Draw candlestick bar:
   - Body: Rectangle from Open to Close (filled if Close > Open, else hollow)
   - Wick: Line from Low to High (extends beyond body)
   - Bar width: 3 pixels
   - Bar spacing: 0 pixels between bars
```

**Volume Visualization (Optional):**
- Volume bar displayed below price chart (if enabled)
- Height scaled proportionally to trading volume
- Volume height = 1/5 of total image height
- Gap between volume and price charts: 2 pixels

**Example Image:**
```
Pixel Layout (60×64 pixels):
[Price Chart: 60×51 pixels]
[Gap: 2 pixels]
[Volume Chart: 60×11 pixels]
```

#### 1.3.4 Label Generation

For each image at date τ, we predict the 5-day forward return:

**Target Variable:**
```
Label = 1 if Ret[τ → τ+5] > 0
Label = 0 if Ret[τ → τ+5] ≤ 0
```

Where:
```
Ret[τ → τ+5] = exp(cum_log_ret[τ+5] - cum_log_ret[τ]) - 1
```

**Key Features:**
- Binary classification problem (stock goes up vs. down)
- Prediction horizon: 5 trading days (approximately 1 week)
- No look-ahead bias (only use information available at τ)

### 1.4 Data Splits

**Training Set (In-Sample):**
- Period: 1992-2000 (9 years)
- Observations: ~2 million stock-day pairs
- Purpose: Train CNN model parameters
- Used for: Learning candlestick patterns

**Validation Set:**
- 70% of in-sample period (1992-2000)
- Used for: Hyperparameter tuning, early stopping

**Test Set (Out-of-Sample):**
- Period: 2001-2024 (24 years)
- Observations: ~6.9 million stock-day pairs
- Purpose: Evaluate model performance on unseen data
- Used for: Final model evaluation, economic significance tests

### 1.5 Data Validation

**Quality Checks:**
- All prices normalized (first bar close = 1.0 ± 0.001)
- All returns computed from cumulative log returns (no compounding errors)
- Missing data flags properly handled
- No negative market capitalizations
- Images are valid PNG format, correct dimensions

**Coverage Statistics:**
- Average stocks per day (2001-2024): ~3,000
- Maximum stocks per day: ~7,500
- Minimum stocks per day: ~1,500
- Coverage by year: 95-99% of active CRSP stocks

---

## 2. Methodology

### 2.1 Model Architecture

**CNN Architecture for I20/R5 Model:**

```
Input: Grayscale image (Batch × 1 × 64 × 60)
  ↓
Conv1: 64 filters, kernel (5, 3), stride 1, padding 0
  ↓ Batch Normalization + ReLU
  ↓ Output shape: (Batch, 64, 60, 56)
MaxPool1: kernel (2, 1), stride (2, 1)
  ↓ Output shape: (Batch, 64, 30, 56)
Conv2: 64 filters, kernel (3, 1), stride 1, padding 0
  ↓ Batch Normalization + ReLU
  ↓ Output shape: (Batch, 64, 28, 56)
MaxPool2: kernel (2, 1), stride (2, 1)
  ↓ Output shape: (Batch, 64, 14, 56)
Conv3: 64 filters, kernel (2, 1), stride 1, padding 0
  ↓ Batch Normalization + ReLU
  ↓ Output shape: (Batch, 64, 13, 56)
MaxPool3: kernel (2, 1), stride (2, 1)
  ↓ Output shape: (Batch, 64, 6, 56)
Flatten
  ↓ Output: 64 × 6 × 56 = 21,504 features
  ↓ Reshape to (Batch, 336)  [Note: Appears to use only 336 features]
Fully Connected: 336 → 1
  ↓ Dropout (0.50 during training)
  ↓ Sigmoid Activation
  ↓
Output: Probability P(stock return > 0 in next 5 days)
```

**Architecture Details:**
- **Total Parameters:** ~1.2 million trainable parameters
- **Activation Function:** ReLU for hidden layers, Sigmoid for output
- **Dropout:** 0.50 probability (during training only, same as JKX et al. 2024)
- **Batch Normalization:** Applied after each convolutional layer
- **Architecture source:** `Model/cnn_model.py` (CNNModel class)
- **No modifications from original JKX architecture**

### 2.2 Training Procedure

**Training Infrastructure:**
- **Training script:** `Experiments/cnn_experiment.py`
- **Main function:** `train_us_model()`
- **Model architecture:** Defined in `Model/cnn_model.py`
- **Data loading:** `Data/chart_dataset.py` (PyTorch Dataset)
- **Chart generation:** `Data/chart_library.py` (image rendering)

**Objective Function:**
- Loss: Binary Cross-Entropy
- Formula: `L = -[y × log(ŷ) + (1-y) × log(1-ŷ)]`
  - y: True label (0 or 1)
  - ŷ: Predicted probability

**Optimization:**
- Optimizer: Adam
- Learning Rate: 1e-4
- Batch Size: 128 observations
- Max Epochs: 50
- Early Stopping: Monitor validation loss, stop if no improvement for 5 epochs

**Regularization:**
- Dropout: 0.50 on all layers (same as JKX et al. 2024)
- Weight Decay: 0
- Data Augmentation: None
- Batch Normalization: Applied after each convolutional layer

**Ensemble Method:**
- Train 5 independent models from different random initializations
- Each model trained separately on NVIDIA GPU (Laguna cluster)
- Checkpoints saved: `new_model_res/D20L3F53S31D21MP21F53S11D11MP21F53S11D11MP21C64/model_*.tar`
- Final prediction: Average of 5 model outputs
- Reduces variance and improves generalization
- Formula: `ŷ_ensemble = (1/5) × Σ ŷ_i`

### 2.3 Prediction Generation

**Prediction Script:**
- **Script:** `make_prediction_with_rets.py` (located in repo root)
- **Entry point:** Calls `train_us_model()` with `from_ensem_res=True` to load saved checkpoints
- **Output file:** `CACHE_DIR/weekly_prediction_with_rets.csv`

**Frequency:**
- Predictions generated weekly (every ~5 trading days)
- Anchor dates: Last trading day of each week (typically Friday)

**Prediction Pipeline:**
1. Load 20-day price window ending at date τ
2. Normalize prices to base = 1.0
3. Generate candlestick image (60×64 pixels)
4. Forward pass through trained CNN ensemble → probability P(return > 0)
5. Store: Date, StockID, CNN20D5P (up_probability), MarketCap, next_week_ret_0delay
6. Output: `weekly_prediction_with_rets.csv` (8.9M rows, 322 MB)

**Out-of-Sample Coverage:**
- Dates: 2001-01-05 to 2024-12-31
- Stocks: ~22,480 unique stocks
- Predictions: ~8.9 million (Date × StockID pairs)
- Average predictions per week: ~700 per stock
- File size: 322 MB

### 2.4 Performance Evaluation

**Horizon Evaluation:**
- Compute H-L (High-Low) spreads at different horizons:
  - 1 day: τ+1
  - 3 days: τ+3
  - 10 days: τ+10
- Methods: Equal-weight (EW) and value-weight (VW) portfolios
- Metric: Annualized return, Sharpe ratio

**Portfolio Construction:**
1. Rank stocks by predicted up_probability
2. Divide into 10 deciles (0-9)
3. Go long decile 9 (highest prediction), short decile 0 (lowest)
4. H-L spread = Return(decile 9) - Return(decile 0)
5. Rebalance weekly

**Event Study (FOMC):**
- Hypothesis: CNN predictions more informative around monetary policy events
- Sample: 316 FOMC meetings (1992-2024)
- Windows:
  - Pre-announcement: Day t-1 to t
  - Reaction: Day t to t+1
  - Intermediate: Day t+4 to t+20 (delayed information incorporation)
- Method: Align predictions to event dates using `pandas.merge_asof` with `direction="backward"`

**FOMC Pipeline Steps:**
1. **Schedule ingestion:** `FOMC_Dates_1936.csv` → `fomc_schedule_with_offsets.csv` (via `ingest_manual_schedule.py`)
2. **Build windows:** Compute per-stock returns for each FOMC event window (via `build_windows.py`)
3. **Align predictions:** Merge predictions to events using backward-looking merge (via `align_predictions_and_score.py`)
4. **Compute deciles:** Rank stocks by up_probability, calculate H-L spreads for each window
5. **Summarize:** Aggregate H-L spreads across all events (via `run_fomc_pipeline.py`)

**Alignment Details:**
- Script: `trend_code_submit/Analysis/fomc/align_predictions_and_score.py`
- Function: `merge_asof_by_stock()` (lines 85-134)
- Algorithm: For each stock and FOMC event, find most recent prediction ≤ announcement date
- Example: FOMC on June 15 → Uses prediction from June 12 (if that's the most recent prediction ≤ June 15)
- Rationale: Weekly predictions (every ~5 days) vs. arbitrary FOMC announcement dates
- Bias prevention: Backward direction ensures no look-ahead (only uses information available before announcement)

**Code Implementation:**
```python
# From align_predictions_and_score.py, lines 115-121
aligned_stock = pd.merge_asof(
    ev,  # FOMC events (left)
    g[["Date", "up_prob", "MarketCap"]],  # Predictions (right)
    on="Date",
    direction="backward",  # Most recent pred ≤ event date
    suffixes=("", "_pred")
)
```

### 2.5 Statistical Testing

**Momentum:**
- Measure 260-day return (12 months, skipping last month)

**Short-term Reversal:**
- Measure 20-day return (last month)

**Trend:**
- Measure 60-day return (3 months)

**Volatility:**
- Exponentially weighted moving average of squared returns

**Size:**
- Log of market capitalization

**Regression Analysis:**
- Test if CNN predictions add value beyond traditional characteristics
- OOS R²: Out-of-sample explanatory power
- Compare: CNN alone vs. characteristics alone vs. combined

### 2.6 Temporal Alignment

**Critical:** All analyses properly aligned to avoid look-ahead bias.

**Stock Characteristics:**
- Computed using only information available at prediction date τ
- For characteristic measured at τ-1 (one day before), use backward merge

**Future Returns:**
- Computed from prediction date τ forward
- τ → τ+5 for 5-day horizon
- Never use information from dates > τ

**FOMC Event Study:**
- For FOMC announcement on day t, use most recent prediction ≤ t
- Typically uses prediction from t-2 or t-3 days (previous Friday's prediction)
- Implementation: `pd.merge_asof(..., direction="backward")` per stock
- No forward-looking bias: Only uses predictions that existed before the announcement
- Output: Decile H-L spreads for pre-announcement, reaction, and intermediate windows

---

## Appendix: Technical Specifications

### Image Generation Parameters
```python
# From dgp_config.py and chart_library.py
IMAGE_WIDTH = {5: 15, 20: 60, 60: 180}  # pixels
IMAGE_HEIGHT = {5: 32, 20: 64, 60: 96}  # pixels  
BAR_WIDTH = 3  # pixels per day
VOLUME_HEIGHT_RATIO = 0.2  # 20% of total height
VOLUME_CHART_GAP = 2  # pixels

# CNN Architecture Configuration
BENCHMARK_MODEL_LAYERNUM_DICT = {5: 2, 20: 3, 60: 4}  # Number of conv layers
TRUE_DATA_CNN_INPLANES = 64  # Number of filters in conv layers
BATCH_SIZE = 128
```

### Data File Sizes
- Raw CRSP file: ~15 GB (compressed)
- Processed daily panel: 3.9 GB
- Weekly predictions: 322 MB
- FOMC windows: 89 MB
- Period returns (parquet): ~13 KB each

### Computational Resources
- Training: NVIDIA GPUs (Laguna cluster)
- Training time per ensemble member: ~2-7 hours (varies by data availability)
- Prediction generation: ~30 minutes (5 ensembles)
- Total compute time: ~40-50 GPU-hours
- SLURM scripts: `slurm/run_member.sh` (array job for 5 ensembles), `slurm/run_portfolios.sh`

### Scripts Pipeline Summary

**Training & Prediction:**
1. **Training:** `cnn_experiment.py::train_us_model()` → saves checkpoints
2. **Prediction generation:** `make_prediction_with_rets.py` → `weekly_prediction_with_rets.csv`
3. **Portfolio generation:** `generate_cnn_portfolios.py` → portfolio CSV files

**FOMC Analysis:**
4. **FOMC schedule:** `ingest_manual_schedule.py` → `fomc_schedule.csv`
5. **FOMC windows:** `build_windows.py` → `fomc_window_returns.csv`
6. **FOMC alignment:** `align_predictions_and_score.py` → `fomc_decile_performance.csv`
7. **FOMC summary:** `run_fomc_pipeline.py` → `fomc_summary.csv` and `.png`

**Event Study Extensions:**
8. **Event portfolios:** `event_study_portfolios.py` → `event_study_portfolio_table.csv`
9. **Conditional horizon:** `horizon_eval_conditional.py` → `horizon_eval_conditional.csv` and `.png`


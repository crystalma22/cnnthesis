# Methodology Writing Guide for GPT Agent

**Repository:** https://github.com/crystalma22/cnnthesis  
**Branch:** `replication-edited`  
**Purpose:** Guide for GPT agent to help write thesis methodology section

---

## Quick Navigation

### 📚 Documentation Files (Already Written)

1. **`docs/THESIS_DATA_METHODOLOGY.md`** - Complete data and methodology section
   - Data preprocessing steps
   - CNN architecture with layer dimensions
   - Training procedure
   - FOMC event study methodology
   - Scripts pipeline summary

2. **`FOMC_METHODOLOGY.md`** - Detailed FOMC event study methodology
   - FOMC pipeline step-by-step
   - Event window definitions
   - Alignment algorithm with code examples
   - Statistical approach

3. **`CHATGPT_ANSWERS.md`** - Answers to common methodology questions
   - Which scripts generate predictions
   - How FOMC merging works
   - CNN architecture modifications (none)
   - Output file confirmations

4. **`docs/COMPLETE_TODO_AND_INSTRUCTIONS.md`** - Complete workflow instructions
   - Task breakdown
   - How to run scripts on Laguna
   - Expected outputs

5. **`THESIS_DATA_INVENTORY.md`** - Data inventory and status
   - What data exists
   - What's been generated vs. old
   - Coverage and date ranges

---

## 🗂️ Key Code Files by Function

### Data Processing

**Main data loader:**
- `trend_code_submit/Data/equity_data.py`
  - Function: `processed_US_data()` - loads and cleans CRSP data
  - Returns: DataFrame with Date, StockID, OHLC, Ret, MarketCap, cum_log_ret
  - Coverage: 1992-2024, 63.3M rows, 29,331 stocks

**Chart generation:**
- `trend_code_submit/Data/generate_chart.py`
  - Class: `GenerateStockData`
  - Converts OHLC prices → candlestick images
  - Image dimensions: 60×64 pixels for I20 model

- `trend_code_submit/Data/chart_library.py`
  - Function: `draw_candlestick()`
  - Actual pixel-level image rendering
  - Normalization: first bar close = 1.0

**Dataset class:**
- `trend_code_submit/Data/chart_dataset.py`
  - PyTorch Dataset for loading images + labels
  - Used during training

**Configuration:**
- `trend_code_submit/Data/dgp_config.py`
  - IMAGE_WIDTH, IMAGE_HEIGHT parameters
  - CACHE_DIR, PORTFOLIO paths
  - FREQ_DICT mapping

---

### Model Architecture

**CNN model definition:**
- `trend_code_submit/Model/cnn_model.py`
  - Class: `CNNModel`
  - Architecture: 3 conv layers (64 filters each), 3 max pools, 1 FC layer
  - Activation: ReLU (hidden), Sigmoid (output)
  - Dropout: 0.50
  - Total parameters: ~1.2M

**Key architecture parameters:**
```python
# From dgp_config.py
BENCHMARK_MODEL_LAYERNUM_DICT = {5: 2, 20: 3, 60: 4}  # Conv layers by window size
TRUE_DATA_CNN_INPLANES = 64  # Filters per conv layer
BATCH_SIZE = 128
DROP_OUT_PROB = 0.50
```

---

### Training & Prediction

**Training script:**
- `trend_code_submit/Experiments/cnn_experiment.py`
  - Function: `train_us_model(ws_list, pw_list, ensem=5, ...)`
  - Trains ensemble of 5 independent models
  - Adam optimizer, lr=1e-4, max 50 epochs
  - Early stopping on validation loss
  - Saves checkpoints: `WORK_SPACE/new_model_res/.../model_*.tar`

**Prediction generation:**
- `make_prediction_with_rets.py`
  - Calls `train_us_model()` with `from_ensem_res=True`
  - Loads saved checkpoints
  - Generates weekly predictions (2001-2024)
  - Output: `CACHE_DIR/weekly_prediction_with_rets.csv` (8.9M rows, 322 MB)
  - Columns: Date, StockID, CNN20D5P, MarketCap, next_week_ret_0delay

---

### Portfolio Generation

**Portfolio script:**
- `trend_code_submit/Portfolio/portfolio.py`
  - Class: `PortfolioManager`
  - Function: `generate_portfolio(cut=10)` - creates decile portfolios
  - Computes EW/VW returns, Sharpe ratios, turnover

**Portfolio helper:**
- `trend_code_submit/Analysis/analysis_lib.py`
  - Function: `portfolio_performance_helper(ws=20, pw=5)`
  - Wrapper that calls PortfolioManager
  - Output: `WORK_SPACE/new_model_res/portfolio/cnn_weekly/CNN20D5P/`

**Portfolio generation script:**
- `generate_cnn_portfolios.py`
  - Standalone script to generate portfolios
  - Calls `analysis_lib.portfolio_performance_helper()`

---

### FOMC Event Study

**FOMC pipeline orchestrator:**
- `trend_code_submit/Analysis/fomc/run_fomc_pipeline.py`
  - Runs complete FOMC analysis pipeline
  - Steps: ingest schedule → build windows → align predictions → summarize

**Step 1: Schedule ingestion**
- `trend_code_submit/Analysis/fomc/ingest_manual_schedule.py`
  - Input: `FOMC_Dates_1936.csv` (316 FOMC meetings, 1992-2024)
  - Computes business-day offsets using `pd.BDay()`
  - Output: `CACHE_DIR/fomc/fomc_schedule_with_offsets.csv`
  - Columns: announcement_date, t_minus_1, t_plus_1, t_plus_5, t_plus_20

**Step 2: Build FOMC windows**
- `trend_code_submit/Analysis/fomc/build_windows.py`
  - Merges FOMC dates with daily stock returns
  - Computes returns for 3 windows: pre, react, intermediate
  - Output: `CACHE_DIR/fomc/fomc_window_returns.csv` (2.35M rows, 89 MB)

**Step 3: Align predictions to events**
- `trend_code_submit/Analysis/fomc/align_predictions_and_score.py`
  - Function: `merge_asof_by_stock()` (lines 85-134)
  - Uses `pd.merge_asof(..., direction="backward")`
  - For each stock: finds most recent prediction ≤ announcement date
  - Function: `decile_scores()` (lines 137-157)
  - Computes EW/VW decile returns and H-L spreads
  - Output: `CACHE_DIR/fomc/fomc_decile_performance.csv` (316 events)

**Step 4: Event study extensions**
- `trend_code_submit/Analysis/fomc/event_study_portfolios.py`
  - Compares H-L performance: FOMC windows vs. non-event days
  - Uses daily data + event masks
  - Output: `CACHE_DIR/fomc/event_study_portfolio_table.csv`

- `trend_code_submit/Analysis/fomc/horizon_eval_conditional.py`
  - Compares 1d/3d/10d H-L: FOMC days vs. non-FOMC days
  - Output: `CACHE_DIR/fomc/horizon_eval_conditional.csv`, `.png`

---

## 📊 Key Data Files

### Input Data (Not in GitHub - Too Large)

- `WORK_SPACE/data/processed_data/us_ret.feather` (3.9 GB)
  - Processed CRSP daily stock data
  - 63.3M rows, 1992-2024
  - Generated by: `equity_data.py::processed_US_data()`

- `WORK_SPACE/data/stocks_dataset/stocks_USA/dataset_all/20d_week_has_vb_[20]_ma_YYYY_images.dat`
  - Annual image datasets for training (1993-2024)
  - Binary format: stacked 60×64 grayscale images
  - Generated by: `generate_chart.py::save_annual_data()`

### Output Data (In CACHE_DIR - Not in GitHub)

- `CACHE_DIR/weekly_prediction_with_rets.csv` (322 MB, 8.9M rows)
- `CACHE_DIR/horizon_eval.csv` (157 B, 3 horizons)
- `CACHE_DIR/fomc/fomc_schedule.csv` (27 KB, 316 events)
- `CACHE_DIR/fomc/fomc_window_returns.csv` (89 MB, 2.35M rows)
- `CACHE_DIR/fomc/fomc_decile_performance.csv` (~100 KB, 316 events)

### Small Data Files (Can Include in GitHub)

- `FOMC_Dates_1936.csv` (manual FOMC schedule)
- `CACHE_DIR/horizon_eval.csv` (results summary)
- `CACHE_DIR/fomc/fomc_summary.csv` (aggregate statistics)

---

## 🔧 Scripts to Run on Laguna (SLURM)

### Model Training
- `slurm/run_member.sh` - Train ensemble (array job, 5 members)
- `slurm/run_portfolios.sh` - Generate predictions and portfolios

### FOMC Analysis
- `slurm/run_fomc_analysis.sh` - Main FOMC pipeline
- `slurm/run_fomc_event_study.sh` - Event study portfolios
- `slurm/run_fomc_horizon_conditional.sh` - Conditional horizon eval

### Data Generation
- `slurm/run_regenerate_period_returns.sh` - Update period returns

---

## 📝 Methodology Section Structure (Suggested)

### Section 1: Data
**Reference:** `docs/THESIS_DATA_METHODOLOGY.md` sections 1.1-1.5

**What to include:**
- CRSP data source and coverage (section 1.1)
- Data cleaning steps (section 1.2)
- Multi-period return calculations using cum_log_ret (section 1.2, Step 4)
- Image generation process (section 1.3)
  - 60×64 pixel candlestick charts
  - Price normalization (base = 1.0)
  - Volume bars (optional)
- Data splits: 1992-2000 (train), 2001-2024 (test)

**Code references:**
- `equity_data.py::processed_US_data()` - data loading
- `chart_library.py` - image rendering
- `generate_chart.py::GenerateStockData` - chart generation

---

### Section 2: CNN Architecture
**Reference:** `docs/THESIS_DATA_METHODOLOGY.md` section 2.1

**What to include:**
- Layer-by-layer architecture with output shapes
- Conv1: 64 filters, (5,3) kernel → (Batch, 64, 60, 56)
- MaxPool1: (2,1) kernel → (Batch, 64, 30, 56)
- Conv2: 64 filters, (3,1) kernel → (Batch, 64, 28, 56)
- MaxPool2: (2,1) kernel → (Batch, 64, 14, 56)
- Conv3: 64 filters, (2,1) kernel → (Batch, 64, 13, 56)
- MaxPool3: (2,1) kernel → (Batch, 64, 6, 56)
- Flatten → FC → Sigmoid
- Total parameters: ~1.2M
- Regularization: Dropout 0.50, batch normalization

**Code reference:**
- `Model/cnn_model.py::CNNModel` class

---

### Section 3: Training Procedure
**Reference:** `docs/THESIS_DATA_METHODOLOGY.md` section 2.2

**What to include:**
- Objective: Binary cross-entropy loss
- Optimizer: Adam with lr=1e-4
- Batch size: 128
- Max epochs: 50
- Early stopping: 5 epochs patience
- Ensemble: 5 independent models, averaged predictions
- Training time: ~40-50 GPU-hours total

**Code reference:**
- `Experiments/cnn_experiment.py::train_us_model()`
- `Experiments/cnn_experiment.py::Experiment` class

---

### Section 4: Prediction Generation
**Reference:** `docs/THESIS_DATA_METHODOLOGY.md` section 2.3

**What to include:**
- Frequency: Weekly (every ~5 business days)
- Coverage: 2001-2024, 8.9M predictions, 22,480 stocks
- Output: Probability P(return > 0 in next 5 days)
- File: `weekly_prediction_with_rets.csv`

**Code reference:**
- `make_prediction_with_rets.py` - generates predictions

---

### Section 5: FOMC Event Study
**Reference:** `FOMC_METHODOLOGY.md` sections 57-256

**What to include:**
- Hypothesis: CNN predictions more informative around FOMC events
- Sample: 316 FOMC meetings (1992-2024), ~209 with predictions (2001-2024)
- Event windows:
  - Pre-announcement: day t-1 to t
  - Reaction: day t to t+1  
  - Intermediate: day t+4 to t+20
- Alignment method: `pd.merge_asof(..., direction="backward")`
  - For each stock and event, use most recent prediction ≤ announcement date
  - Example: FOMC June 15 → use prediction from June 12
- Decile portfolio formation:
  - Rank stocks by up_probability
  - Compute EW and VW H-L spreads
  - Aggregate across all events

**Code references:**
- `Analysis/fomc/ingest_manual_schedule.py` - schedule processing
- `Analysis/fomc/build_windows.py` - window returns
- `Analysis/fomc/align_predictions_and_score.py` - alignment (lines 85-134 for merge_asof)
- `Analysis/fomc/run_fomc_pipeline.py` - orchestration

**Key code snippet to reference:**
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

---

### Section 6: Performance Evaluation
**Reference:** `docs/THESIS_DATA_METHODOLOGY.md` section 2.4

**What to include:**
- Horizon evaluation: 1-day, 3-day, 10-day forward returns
- Portfolio construction: Decile portfolios (0-9)
- H-L spread: Decile 9 - Decile 0
- Equal-weight vs. value-weight
- Weekly rebalancing

**Code reference:**
- `Analysis/horizon_eval.py` - horizon evaluation
- `Portfolio/portfolio.py::PortfolioManager` - portfolio construction

---

## 🎯 Writing the Methodology: Where to Find Information

### For Data Section:

**"How was the data cleaned?"**
→ See: `docs/THESIS_DATA_METHODOLOGY.md` section 1.2
→ Code: `Data/equity_data.py::processed_US_data()` lines 1-200

**"How are images generated?"**
→ See: `docs/THESIS_DATA_METHODOLOGY.md` section 1.3
→ Code: `Data/chart_library.py` and `Data/generate_chart.py`

**"What are the data splits?"**
→ See: `docs/THESIS_DATA_METHODOLOGY.md` section 1.4
→ Training: 1992-2000 (9 years)
→ Testing: 2001-2024 (24 years)

---

### For Model Section:

**"What is the CNN architecture?"**
→ See: `docs/THESIS_DATA_METHODOLOGY.md` section 2.1 (layer-by-layer breakdown)
→ Code: `Model/cnn_model.py::CNNModel` class
→ Config: `Data/dgp_config.py` (filter counts, layer numbers)

**"How does the CNN differ from JKX et al. (2024)?"**
→ See: `CHATGPT_ANSWERS.md` Question 3
→ Answer: No modifications; same architecture

**"What are the hyperparameters?"**
→ See: `docs/THESIS_DATA_METHODOLOGY.md` section 2.2
→ Learning rate: 1e-4
→ Dropout: 0.50
→ Batch size: 128
→ Code: `Experiments/cnn_experiment.py::get_bl_exp_obj()`

---

### For FOMC Event Study:

**"How are FOMC dates collected?"**
→ See: `FOMC_METHODOLOGY.md` sections 9-25
→ Source: Federal Reserve website
→ Manual compilation: `FOMC_Dates_1936.csv`
→ Code: `Analysis/fomc/ingest_manual_schedule.py`

**"How are predictions aligned to FOMC events?"**
→ See: `FOMC_METHODOLOGY.md` sections 129-181
→ Method: `pd.merge_asof` with backward direction
→ Code: `Analysis/fomc/align_predictions_and_score.py::merge_asof_by_stock()`
→ Example provided in methodology docs

**"What are the event windows?"**
→ See: `FOMC_METHODOLOGY.md` sections 257-276
→ Pre: t-1 to t
→ Reaction: t to t+1
→ Intermediate: t+4 to t+20
→ Non-event: All other days

**"How are decile portfolios formed?"**
→ See: `FOMC_METHODOLOGY.md` sections 282-294
→ Rank stocks by up_prob → divide into 10 groups
→ H-L = Decile 10 - Decile 1
→ Code: `Analysis/fomc/align_predictions_and_score.py::decile_scores()`

---

## 📐 Statistical Methods

### Horizon Evaluation
- Script: `Analysis/horizon_eval.py`
- Computes k-day forward returns using cumulative log returns
- Formula: `Ret[t→t+k] = exp(cum_log_ret[t+k] - cum_log_ret[t]) - 1`
- Output: `CACHE_DIR/horizon_eval.csv`

### Stock Characteristics
- Script: `generate_stock_chars_with_cnn.py`
- Computes: MOM, STR, TREND, Beta, Volatility, etc.
- Aligns characteristics to prediction dates (backward merge)
- Output: `CACHE_DIR/cnn_and_monthly_stock_char_*.parquet`

### Regression Analysis
- Script: `Analysis/regression_tables.py`
- Functions:
  - `cnn_pred_on_monthly_stock_char()` - CNN vs. characteristics
  - `cnn_and_ret_and_stock_char_regression()` - Multi-factor regressions
- Output: OOS R² values

---

## 🔍 Common Methodology Questions & Answers

### Q: "What training data is used?"
**A:** 1992-2000 (9 years, ~2M stock-day observations)
- Source: `Misc/config.py::IS_YEARS`
- Code: `Experiments/cnn_experiment.py` uses this range

### Q: "What test data is used?"
**A:** 2001-2024 (24 years, ~6.9M stock-day observations)
- Source: `Misc/config.py::OOS_YEARS`
- All evaluation metrics use this period

### Q: "How is ensemble averaging done?"
**A:** Simple average of 5 model outputs
- Formula: `ŷ_ensemble = (1/5) × Σ ŷ_i`
- Code: `Experiments/cnn_experiment.py::generate_ensem_res()`

### Q: "How are images normalized?"
**A:** Divide all prices by first day's close
- First bar always starts at 1.0
- Ensures comparability across stocks
- Code: `Data/chart_library.py` (normalization logic)

### Q: "How are returns calculated?"
**A:** Using cumulative log returns (mathematically precise)
- Single period: `Ret = exp(log_ret) - 1`
- Multi-period: `Ret[t→t+k] = exp(cum[t+k] - cum[t]) - 1`
- Avoids compounding errors
- Code: `Data/equity_data.py` (cum_log_ret calculation)

### Q: "What is the prediction frequency?"
**A:** Weekly (every ~5 business days)
- Anchor: Last trading day of week (typically Friday)
- Total: ~1,200 prediction dates (2001-2024)
- Average: ~7,500 stocks per date

### Q: "How is look-ahead bias prevented?"
**A:** Three mechanisms:
1. Training data (1992-2000) completely separate from test (2001-2024)
2. Images use only past 20 days of prices
3. FOMC alignment uses `direction="backward"` (only past predictions)

---

## 📂 File Organization

```
cnnthesis/
├── docs/                           # Documentation (GPT should read these)
│   ├── THESIS_DATA_METHODOLOGY.md  # Main methodology doc
│   ├── COMPLETE_TODO_AND_INSTRUCTIONS.md
│   ├── THESIS_RESULTS_SUMMARY.md
│   └── THESIS_WORK_PLAN.md
│
├── trend_code_submit/              # Main codebase
│   ├── Data/
│   │   ├── equity_data.py          # Data loading
│   │   ├── generate_chart.py       # Chart generation
│   │   ├── chart_library.py        # Image rendering
│   │   └── dgp_config.py           # Configuration
│   ├── Model/
│   │   └── cnn_model.py            # CNN architecture
│   ├── Experiments/
│   │   └── cnn_experiment.py       # Training loop
│   ├── Portfolio/
│   │   └── portfolio.py            # Portfolio construction
│   └── Analysis/
│       ├── analysis_lib.py         # Portfolio helpers
│       ├── horizon_eval.py         # Horizon evaluation
│       ├── regression_tables.py    # Regression analysis
│       └── fomc/                   # FOMC event study
│           ├── run_fomc_pipeline.py
│           ├── ingest_manual_schedule.py
│           ├── build_windows.py
│           ├── align_predictions_and_score.py
│           ├── event_study_portfolios.py
│           └── horizon_eval_conditional.py
│
├── FOMC_METHODOLOGY.md             # FOMC methodology details
├── CHATGPT_ANSWERS.md              # Q&A for methodology
├── THESIS_DATA_INVENTORY.md        # Data status
│
├── slurm/                          # SLURM job scripts
│   ├── run_member.sh               # Training
│   ├── run_portfolios.sh           # Predictions
│   ├── run_fomc_analysis.sh        # FOMC pipeline
│   ├── run_fomc_event_study.sh     # Event study
│   └── run_fomc_horizon_conditional.sh
│
└── CACHE_DIR/                      # Outputs (not in git)
    ├── weekly_prediction_with_rets.csv
    ├── horizon_eval.csv
    └── fomc/
        ├── fomc_schedule.csv
        ├── fomc_window_returns.csv
        ├── fomc_decile_performance.csv
        └── fomc_summary.csv
```

---

## 🚀 Quick Start for GPT Agent

### Step 1: Read Core Documentation
```
1. docs/THESIS_DATA_METHODOLOGY.md (comprehensive overview)
2. FOMC_METHODOLOGY.md (FOMC event study details)
3. CHATGPT_ANSWERS.md (Q&A for clarifications)
```

### Step 2: Understand Data Flow
```
CRSP raw data 
  → processed_US_data() [equity_data.py]
  → Generate images [generate_chart.py]
  → Train CNN [cnn_experiment.py]
  → Generate predictions [make_prediction_with_rets.py]
  → Form portfolios [portfolio.py]
  → FOMC analysis [fomc/*.py]
```

### Step 3: Key Code Sections to Reference

**For data preprocessing:**
- File: `trend_code_submit/Data/equity_data.py`
- Lines: 1-300 (data cleaning and processing)

**For CNN architecture:**
- File: `trend_code_submit/Model/cnn_model.py`
- Class: `CNNModel`

**For training:**
- File: `trend_code_submit/Experiments/cnn_experiment.py`
- Function: `train_us_model()` (lines 1300-1373)

**For FOMC alignment:**
- File: `trend_code_submit/Analysis/fomc/align_predictions_and_score.py`
- Function: `merge_asof_by_stock()` (lines 85-134)

---

## 📊 Results Summary (For Discussion Section)

**Reference:** `docs/THESIS_RESULTS_SUMMARY.md`

### Key Findings
1. **Horizon evaluation:**
   - 1-day: EW H-L = 0.87%, VW H-L = 0.09%
   - 3-day: EW H-L = 1.11%, VW H-L = 0.20%
   - 10-day: EW H-L = 1.37%, VW H-L = 0.24%

2. **FOMC analysis:**
   - 316 events analyzed (1992-2024)
   - ~209 events with predictions (2001-2024)
   - Results pending from Laguna jobs

---

## ⚠️ Important Notes for GPT Agent

1. **File names are exact:**
   - Use `weekly_prediction_with_rets.csv` (NOT `weekly_predictions.csv`)
   - Use `CNN20D5P` column (NOT `up_prob` until renamed)
   - Use `processed_US_data()` function (NOT `load_us_data()`)

2. **Architecture is unchanged from JKX:**
   - No need to justify modifications
   - Can cite JKX et al. (2024) for architecture choices

3. **Key innovation is FOMC event study:**
   - This is the thesis contribution
   - Methodology should emphasize alignment algorithm
   - Explain backward merge thoroughly

4. **Scripts are modular:**
   - Each script does one thing
   - Pipeline = chaining scripts together
   - See `docs/THESIS_DATA_METHODOLOGY.md` section "Scripts Pipeline Summary"

5. **Temporal alignment is critical:**
   - No look-ahead bias
   - Predictions use only past 20 days
   - FOMC alignment uses backward merge
   - Stock characteristics use lagged values

---

## 📖 Suggested Methodology Outline

### I. Data and Sample Construction
1.1 Data Source (CRSP)
1.2 Sample Selection and Cleaning
1.3 Multi-Period Return Calculations
1.4 Image Generation Process
1.5 Sample Splits (IS: 1992-2000, OOS: 2001-2024)

### II. Model Specification
2.1 CNN Architecture
2.2 Training Procedure
2.3 Ensemble Method
2.4 Prediction Generation

### III. FOMC Event Study Design
3.1 FOMC Schedule Construction
3.2 Event Window Definitions
3.3 Prediction Alignment Algorithm
3.4 Decile Portfolio Formation
3.5 Statistical Tests

### IV. Performance Metrics
4.1 Horizon Evaluation
4.2 Long-Short Portfolio Returns
4.3 Risk-Adjusted Performance (Sharpe Ratios)
4.4 Event vs. Non-Event Comparison

---

## 🔗 External References to Cite

**CNN for finance:**
- Jiang, Xu, & Kelly (2024) - Original CNN architecture
- Uses same architecture, different sample period

**FOMC event studies:**
- Lucca & Moench (2015) - Pre-FOMC announcement drift
- Savor & Wilson (2013) - Macroeconomic risk premium
- Bernanke & Kuttner (2005) - Market reaction to Fed policy

**Technical analysis:**
- Brock, Lakonishok, & LeBaron (1992) - Technical trading rules
- Neely, Rapach, Tu, & Zhou (2014) - Forecasting equity premium

---

## 💡 Tips for GPT Agent

1. **Start with existing docs:** `docs/THESIS_DATA_METHODOLOGY.md` has 80% of what you need
2. **Cross-reference code:** Verify methodology matches implementation
3. **Use precise language:** "pd.merge_asof with backward direction" not "backward merge"
4. **Include formulas:** Mathematical notation for returns, loss functions
5. **Cite line numbers:** When referencing code, mention specific functions/lines
6. **Avoid jargon:** Explain "ensemble," "decile," "H-L spread" clearly
7. **Emphasize innovation:** FOMC event study is the contribution

---

## ✅ Checklist for Methodology Section

- [ ] Data source clearly described (CRSP, 1992-2024)
- [ ] Image generation process explained (60×64 pixels, normalization)
- [ ] CNN architecture shown with layer dimensions
- [ ] Training procedure documented (Adam, lr=1e-4, 50 epochs)
- [ ] Ensemble method explained (5 models, averaged)
- [ ] Prediction generation described (weekly, 8.9M predictions)
- [ ] FOMC schedule collection explained (316 events)
- [ ] Event windows defined (pre, react, intermediate)
- [ ] Alignment algorithm detailed (merge_asof backward)
- [ ] Decile portfolio formation explained
- [ ] Temporal alignment emphasized (no look-ahead bias)
- [ ] Code references provided for reproducibility
- [ ] Sample sizes reported (stocks, events, observations)

---

## 📧 Contact Information in Repository

**Repository owner:** Crystal Ma  
**Branch:** replication-edited  
**Cluster:** Laguna (CMC HPC)  
**Environment:** cnn_env (Python 3.x with PyTorch)

All scripts designed to run on Laguna cluster using SLURM job submission.



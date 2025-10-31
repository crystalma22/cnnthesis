# FOMC Event Study Methodology

## Overview

This analysis examines whether CNN-generated stock return predictions exhibit enhanced predictive power around Federal Open Market Committee (FOMC) announcements, testing the hypothesis that technical patterns become more informative during periods of heightened market uncertainty and information flow.

---

## Data Sources

### 1. FOMC Schedule (1992-2024)
**Source:** Federal Reserve website (federalreserve.gov/monetarypolicy/fomccalendars.htm)

**Data collected:**
- Announcement dates: 316 FOMC meetings
- Meeting start/end dates
- Statement release times (Eastern Time)
- Scheduled vs. unscheduled (emergency) meetings
- Press conference indicators (post-2011)

**Coverage:**
- Start: January 9, 1992
- End: December 17, 2024
- Frequency: ~8 meetings per year

**IMPORTANT - Window Definitions (Following Lucca & Moench 2015):**
- **Pre-FOMC:** Day t-1 ONLY (24-hour window before announcement)
- **Announcement:** Day t (announcement day)
- **Reaction:** Day t+1 (next-day response)
- **Intermediate:** Days t+4 to t+20 (delayed response)

### 2. Stock Return Data
**Source:** CRSP daily stock file via processed_US_data()

**Coverage:**
- 63.3 million daily observations
- 29,331 unique stocks
- January 2, 1992 to December 31, 2024

**Key variables:**
- Daily returns (Ret)
- Market capitalization (MarketCap)
- Cumulative log returns (cum_log_ret)

### 3. CNN Predictions
**Source:** Trained ensemble model predictions

**Model specification:**
- Architecture: 2D Convolutional Neural Network
- Input: 20-day OHLC candlestick charts
- Output: Probability stock return > 0 in next 5 days
- Ensemble: 5 independently trained models (averaged)
- Training: 1992-2000 (in-sample)
- Testing: 2001-2024 (out-of-sample)

**Prediction file:**
- 8.9 million weekly predictions
- Coverage: All stocks, weekly frequency
- Variable: CNN20D5P (up-probability)

---

## FOMC Pipeline - Step-by-Step

### Step 1: Schedule Ingestion and Offset Calculation

**Input:** `FOMC_Dates_1936.csv` (manual compilation from Fed website)

**Process:**
1. Load FOMC announcement dates and meeting details
2. Compute business-day offsets using pandas BDay():
   - `t_minus_1`: 1 business day before announcement
   - `t_plus_1`: 1 business day after announcement  
   - `t_plus_5`: 5 business days after announcement
   - `t_plus_20`: 20 business days after announcement
   - `t_plus_4`: `t_plus_5` - 1 business day (for intermediate window calculation)

**Output:** 
- `CACHE_DIR/fomc/fomc_schedule.csv`
- `CACHE_DIR/fomc/fomc_schedule_with_offsets.csv`

**Code:** `trend_code_submit/Analysis/fomc/ingest_manual_schedule.py`

---

### Step 2: Build FOMC Window Returns

**Input:**
- FOMC schedule with offsets
- `us_ret.feather` (63M daily stock returns)

**Process:**

For each of 316 FOMC announcements and ~29,000 stocks:

1. **Pre-FOMC return** (`pre_fomc_ret`):
   - Cumulative return from t-5 to t-1 (5 days BEFORE announcement)
   - EXCLUDES announcement day (matches Lucca & Moench 2015 definition)
   - Captures anticipation and positioning before Fed decision

2. **Announcement day return** (`announcement_day_ret`):
   - Return ON day t (announcement day only)
   - Captures immediate impact of FOMC announcement

3. **Reaction return** (`react_ret`):
   - Return on t+1 (first trading day after announcement)
   - Captures overnight digestion of FOMC information

3. **Cumulative log returns:**
   - `cum_t4`: Cumulative log return at t+4
   - `cum_t20`: Cumulative log return at t+20
   
4. **Intermediate return** (`intermediate_ret`):
   - Formula: exp(cum_t20 - cum_t4) - 1
   - Captures delayed response (days 5-20)
   - Tests if markets slowly incorporate FOMC information

**Merge strategy:**
- Left merge FOMC dates with daily stock panel
- Each announcement × stock combination gets return data
- Missing data (NaN) occurs when:
  - Stock not trading on that specific date
  - Date falls outside available data range
  - Future dates (t+20 beyond Dec 2024)

**Output:** `CACHE_DIR/fomc/fomc_window_returns.csv`
- 2.35 million rows (316 events × ~7,500 stocks per event)
- 89 MB file

**Code:** `trend_code_submit/Analysis/fomc/build_windows.py`

**Technical notes:**
- Uses cumulative log returns for mathematically accurate multi-period returns
- Log return formula: ln(1 + R)
- Multi-period return: exp(cum[t2] - cum[t1]) - 1
- This avoids compounding errors from chaining simple returns

---

### Step 3: Align Predictions to FOMC Events

**Input:**
- `weekly_prediction_with_rets.csv` (8.9M CNN predictions)
- `fomc_window_returns.csv` (2.35M event-stock observations)

**Process:**

**Challenge:** CNN predictions are weekly (every ~5 business days), but FOMC announcements occur on arbitrary dates. Need to match each FOMC event to the most recent available prediction.

**Solution:** `merge_asof` with backward direction

For each stock and FOMC announcement:
1. Find all CNN predictions for that stock
2. Identify the most recent prediction date ≤ announcement date
3. Assign that prediction's up_prob to the event

**Example:**
```
FOMC announcement: June 15, 2020
Stock XYZ predictions: June 5, June 12, June 19, June 26
→ Use June 12 prediction (most recent ≤ June 15)
```

**Edge cases handled:**
- Pre-2001 FOMC events: No predictions exist (training starts 2001)
  - Solution: Filter out rows with NaN up_prob
- Stocks without predictions on nearby dates:
  - Solution: Skip in decile calculations (handled by dropna())
- StockID format mismatches (10001 vs 10001.0):
  - Solution: Convert float → int → string

**Alignment algorithm:**
```python
for each stock:
    events_for_stock = filter FOMC events for this stock
    predictions_for_stock = filter CNN predictions for this stock
    
    aligned = merge_asof(
        left=events_for_stock,
        right=predictions_for_stock,
        on="Date",
        direction="backward"
    )
```

**Output dimensions:**
- Input: 2.35M event-stock pairs
- After filtering NaN up_prob: ~1.8M valid pairs (events from 2001-2024)
- Lost 23% due to pre-2001 events and missing predictions

**Code:** `trend_code_submit/Analysis/fomc/align_predictions_and_score.py`

---

### Step 4: Compute Decile Performance

**Input:** Aligned data (event × stock × prediction)

**Process:**

For each FOMC announcement:

1. **Rank stocks into deciles** based on up_prob:
   - Decile 1: Lowest 10% (most bearish predictions)
   - Decile 10: Highest 10% (most bullish predictions)

2. **Compute average returns** for each decile:
   - Equal-weight: Simple average across stocks
   - Value-weight: Weighted by market capitalization

3. **Calculate H-L spread**:
   - H-L = Decile 10 return - Decile 1 return
   - Positive H-L = Model has predictive power
   - Larger H-L = Stronger signal

4. **Repeat for three windows:**
   - Pre-announcement (pre_ret)
   - Reaction (react_ret)
   - Intermediate (intermediate_ret)

**Decile calculation:**
```python
for each announcement_date:
    stocks = all stocks with predictions on that date
    stocks["decile"] = qcut(stocks["up_prob"], q=10)
    
    for window in [pre, react, intermediate]:
        EW_HL = mean(decile_10_returns) - mean(decile_1_returns)
        VW_HL = weighted_mean(decile_10) - weighted_mean(decile_1)
```

**Output:** `CACHE_DIR/fomc/fomc_decile_performance.csv`
- One row per FOMC event (316 rows)
- Columns: announcement_date, pre_ew_H-L, pre_vw_H-L, react_ew_H-L, react_vw_H-L, inter_ew_H-L, inter_vw_H-L
- Plus individual decile returns (d1-d10) for each window

**Code:** `align_predictions_and_score.py` (decile_scores function)

---

### Step 5: Summary Statistics

**Input:** Decile performance across all events

**Process:**

1. **Aggregate across events:**
   - Mean H-L spread across all 316 FOMC announcements
   - Standard deviation of spreads
   - Statistical significance tests

2. **Create summary table:**
   - Rows: [pre-window, reaction, intermediate]
   - Columns: [EW H-L, VW H-L]

3. **Visualizations:**
   - Bar chart comparing window performance
   - Shows where predictive power concentrates

**Output:**
- `CACHE_DIR/fomc/fomc_summary.csv`
- `CACHE_DIR/fomc/fomc_summary.png`

**Code:** `run_fomc_pipeline.py` (build_summary function)

---

## Event Windows Defined (Following Lucca & Moench 2015)

### Pre-FOMC Window
**Definition:** Day t-1 ONLY (single day before announcement)  
**Captures:** The famous "pre-FOMC drift" - anticipatory positioning in 24 hours before Fed decision  
**Hypothesis:** If CNN detects anticipation patterns, H-L should be positive on t-1  
**Literature:** Lucca & Moench (2015) show most drift occurs in final 24 hours (not spread over multiple days)

### Announcement Day Window
**Definition:** Day t (announcement day)  
**Captures:** Immediate impact when FOMC statement is released  
**Hypothesis:** CNN predicts which stocks react to monetary policy changes

### Reaction Window  
**Definition:** Day t+1 (next trading day)  
**Captures:** Overnight digestion and next-day response  
**Hypothesis:** CNN predictions align with continued market response

### Intermediate Window
**Definition:** Days t+4 to t+20 (2-4 weeks after)  
**Captures:** Gradual information diffusion and delayed price discovery  
**Hypothesis:** If markets slowly digest FOMC implications, H-L persists

### Non-Event Days
**Definition:** All trading days not in any FOMC window  
**Purpose:** Baseline comparison to assess event-specific predictive power

---

## Statistical Approach

### Decile Portfolio Formation

**At each event:**
1. Rank all available stocks by CNN up_prob
2. Divide into 10 equal groups (deciles)
3. For stocks in decile i, compute:
   - EW return: (1/N) Σ R_i
   - VW return: Σ(w_i × R_i), where w_i = MarketCap_i / Σ MarketCap

**Long-short spread:**
- Go long decile 10 (highest up_prob)
- Go short decile 1 (lowest up_prob)
- H-L = R_10 - R_1

### Aggregation Across Events

**Mean H-L:**
- Average spread across all FOMC events
- Interpretation: Expected H-L per event

**Sharpe-like metric:**
- Mean(H-L) / Std(H-L)
- Measures consistency of predictive power

**Event-time analysis:**
- Align all events to relative time (t-20 to t+20)
- Compute cumulative H-L spread
- Shows temporal pattern of predictive power

---

## Key Assumptions

1. **Prediction availability:**
   - Weekly predictions align with Friday close
   - Most FOMC announcements are Wednesday 2pm
   - Prediction from previous Friday (2-3 days before) is used

2. **Trading feasibility:**
   - Portfolios formed at close on announcement day
   - Returns measured from next open
   - Ignores transaction costs (robustness check needed)

3. **Data quality:**
   - Stocks with missing returns on event dates are excluded
   - Events before 2001 have no predictions (excluded)
   - Last ~20 events may have incomplete intermediate windows

4. **Independence:**
   - FOMC events treated as independent observations
   - Potential autocorrelation in H-L spreads (clustered in time)
   - Could use Newey-West standard errors for significance tests

---

## Computational Details

### Performance Optimizations

1. **Pre-filtering:**
   - Load only necessary columns (Date, StockID, up_prob, MarketCap, returns)
   - Reduces memory footprint from 3.9 GB to ~500 MB

2. **Vectorized merge:**
   - Original: Loop through 22,480 stocks (extremely slow)
   - Optimized: Process in batches of 1,000 stocks
   - Runtime: 5-10 minutes vs. hours

3. **NaN handling:**
   - Drop NaN StockIDs before merge (prevents sort errors)
   - Filter NaN up_prob before decile formation (prevents KeyError)
   - Skip events with <100 valid predictions (insufficient for deciles)

### Resource Requirements

**Build windows:**
- Memory: ~16 GB (loads full stock panel)
- CPU time: 10-15 minutes
- I/O: Reads 3.9 GB feather file

**Align and score:**
- Memory: ~8 GB (predictions + events)
- CPU time: 5-10 minutes
- Bottleneck: Stock-by-stock merge

**Total pipeline:**
- Wall time: 20-30 minutes on compute node (8 cores, 128 GB RAM)
- Could parallelize by year for 5-10x speedup if needed

---

## Output Interpretation

### Table Format (fomc_decile_performance.csv)

| Column | Description |
|--------|-------------|
| announcement_date | FOMC meeting date |
| pre_ew_d1 ... pre_ew_d10 | Equal-weight returns for deciles 1-10 (pre-window) |
| pre_ew_H-L | EW long-short spread (pre-window) |
| pre_vw_d1 ... pre_vw_H-L | Value-weight version |
| react_ew_* | Reaction window metrics |
| inter_ew_* | Intermediate window metrics |

### Summary Statistics (fomc_summary.csv)

| Window | EW_HL | VW_HL |
|--------|-------|-------|
| pre | Mean H-L in pre-announcement window |
| react | Mean H-L in reaction window |
| inter | Mean H-L in intermediate window |

**Interpretation:**
- **Positive H-L:** CNN successfully predicts which stocks outperform
- **Larger magnitude:** Stronger predictive signal
- **EW > VW:** Effect stronger in smaller stocks (liquidity effect)
- **React > Pre:** Information revealed by FOMC, not leaked beforehand

### Comparison to Literature

**Prior findings (Savor & Wilson, 2013; Lucca & Moench, 2015):**
- Market drift before FOMC announcements
- Volatility spike at announcement
- Gradual price adjustment post-announcement

**This analysis tests:**
- Do technical patterns (via CNN) predict which stocks benefit most?
- Is predictive power higher during FOMC windows?
- Does information diffusion pattern align with literature?

---

## Robustness Checks (To Implement)

### 1. Scheduled vs. Unscheduled Meetings
- Emergency meetings may have different dynamics
- Compare H-L for scheduled==1 vs. scheduled==0

### 2. Press Conference Effect
- Post-2011 meetings with press conferences have more information
- Compare H-L for has_press_conference==1 vs. 0

### 3. Monetary Policy Regime
- Different Fed chairs (Greenspan, Bernanke, Yellen, Powell)
- Compare H-L across regimes

### 4. Market Volatility
- Condition on VIX levels
- High volatility periods may amplify or dampen CNN signals

### 5. Rate Change Events
- Compare H-L when Fed changes rates vs. no change
- Larger moves may create stronger technical patterns

---

## Extensions for Thesis

### 1. Event-Study Portfolios (In Progress)

**Script:** `event_study_portfolios.py`

**Approach:**
- Form portfolios using PortfolioManager
- Separate samples: FOMC days vs. non-event days
- Compare Sharpe ratios, turnover, max drawdown

**Deliverable:** Table E1 with full portfolio statistics

### 2. Horizon Evaluation Conditional on Events (In Progress)

**Script:** `horizon_eval_conditional.py`

**Approach:**
- Compute 1d/3d/10d H-L spreads separately for:
  - Event days (FOMC announcements)
  - Non-event days
- Bar chart comparison

**Hypothesis:** Event days show stronger short-horizon predictability

### 3. Event-Time Cumulative Returns

**To implement:**
- Align all events to relative time: t-20 to t+20
- Compute cumulative H-L spread in event time
- Plot shows when predictive power peaks

**Expected pattern:**
- Flat before t-5 (no information)
- Jump at announcement (t=0 to t+1)
- Gradual increase t+1 to t+10 (delayed adjustment)
- Plateau after t+10 (information fully incorporated)

---

## Data Quality and Limitations

### Known Issues

1. **Early FOMC events (1992-2000):**
   - No CNN predictions (training period)
   - 107 events excluded from analysis
   - Remaining: 209 events with predictions

2. **Recent events (late 2024):**
   - `intermediate_ret` is NaN (no data 20 days forward)
   - Affects last ~5 events
   - Can still analyze pre and reaction windows

3. **StockID formatting:**
   - CSV save/load converted integers to floats (10001 → 10001.0)
   - Fixed with: float → int → string conversion
   - Critical for merge success

4. **Missing returns:**
   - Not all stocks trade on all FOMC dates
   - Illiquid stocks may have NaN returns
   - Dropped from decile calculations (affects decile sizes)

### Sample Size by Window

**Expected observations per event:**
- Total stocks in universe: ~7,500 per event (varies by year)
- Stocks with predictions: ~6,000 (80%)
- Stocks with valid returns: ~5,500 (90% of predicted)
- Final sample per event: ~5,000 stocks per decile calculation

**Across all events:**
- Total potential observations: 316 events × 7,500 stocks = 2.37M
- After filtering: ~1.8M valid observations
- Attrition: 24% (pre-2001 events + missing data)

---

## Validation Checks

### 1. Data Integrity
- ✅ All FOMC dates validated against Fed website
- ✅ Business day offsets verified (no weekends/holidays)
- ✅ Return windows properly calculated
- ✅ No duplicate announcement dates

### 2. Prediction Quality
- ✅ 8.9M predictions cover expected date range (2001-2024)
- ✅ CNN20D5P values in [0,1] range
- ✅ No missing values in prediction file
- ✅ Market cap non-negative

### 3. Merge Accuracy
- Diagnostic output shows:
  - Number of stocks matched
  - Date range overlaps
  - StockID type consistency
- Random sample inspection confirms correct alignment

---

## For Thesis Methodology Section

**Suggested text:**

"To examine whether CNN-generated return predictions exhibit enhanced performance during Federal Open Market Committee (FOMC) announcements, I conduct an event study covering 316 FOMC meetings from 1992 to 2024. For each announcement, I construct three return windows: pre-announcement (day t-1 to t), reaction (t to t+1), and intermediate (t+4 to t+20). 

I align the most recent weekly CNN prediction (from the I20/R5 model) to each event using a backward-looking merge, ensuring predictions available before the announcement. For each event and window, I sort stocks into deciles based on predicted up-probability and compute equal-weight and value-weight long-short spreads (decile 10 minus decile 1).

The sample includes 209 events with available predictions (2001-2024) and approximately 5,000 stocks per event, totaling 1.8 million stock-event observations after excluding missing returns. I test whether H-L spreads are significantly larger during FOMC windows compared to non-event days, providing evidence that technical patterns (as captured by CNNs) become more informative during periods of heightened macroeconomic uncertainty."

---

## References

- Lucca, D. O., & Moench, E. (2015). The pre-FOMC announcement drift. *Journal of Finance*, 70(1), 329-371.
- Savor, P., & Wilson, M. (2013). How much do investors care about macroeconomic risk? *Journal of Financial Economics*, 109(3), 716-754.
- Bernanke, B. S., & Kuttner, K. N. (2005). What explains the stock market's reaction to Federal Reserve policy? *Journal of Finance*, 60(3), 1221-1257.




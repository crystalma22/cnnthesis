# Thesis Presentation: CNN Predictions and FOMC Events

**Duration:** 5 minutes + Q&A  
**Slides:** 5  
**Focus:** Methodology and Data

---

## Slide 1: Research Question and Hypothesis

**Background:**
- Recent work (Jiang, Xu, & Kelly, 2024) shows CNNs trained on stock price charts can predict returns
- Technical patterns contain information not fully captured by traditional factors

**Research Question:**
**Are CNN-based stock return predictions more informative around Federal Reserve monetary policy announcements (FOMC meetings)?**

**Hypothesis:**
- Market attention and information processing around FOMC meetings amplifies the predictive power of technical patterns
- CNN predictions should show stronger portfolio performance during FOMC event windows compared to non-event periods

**Contribution:**
- First study to examine CNN return predictions in event study context
- Tests whether technical analysis-based predictions interact with macroeconomic attention

---

## Slide 2: Model Specification - CNN Return Prediction

**Replication Model (Jiang, Xu, & Kelly, 2024):**

\[
P(R_{i,t \to t+5} > 0) = f_{CNN}(\text{Chart}_{i,t-20:t})
\]

**Definitions:**
- **Outcome Variable:** Binary indicator for positive 5-day forward return (Y_i,t = 1 if R_{i,t→t+5} > 0)
- **Input:** 60×64 pixel candlestick chart image (20 trading days of OHLC data)
- **Output:** CNN20D5P - Probability that stock i's return from day t to t+5 is positive

**CNN Architecture:**
- 3 convolutional layers (64 filters each, ReLU activation)
- 3 max-pooling layers for dimensionality reduction
- Fully connected layer → sigmoid output
- Dropout (0.50) for regularization
- Total parameters: ~1.2M

**Training:**
- 5 independent models (ensemble averaging)
- Adam optimizer (learning rate = 1e-4)
- Binary cross-entropy loss
- Early stopping (patience = 5 epochs)

---

## Slide 3: FOMC Event Study Specification

**Event Study Model:**

For each FOMC announcement j, compute decile portfolio returns:

\[
R^{H-L}_{j,\text{window}} = R^{\text{Decile 10}}_{j,\text{window}} - R^{\text{Decile 0}}_{j,\text{window}}
\]

**Event Windows (relative to FOMC announcement day t):**
1. **Pre-announcement:** Close of day t-1 → close of day t (captures pre-FOMC positioning)
2. **Reaction:** Close of day t → close of day t+1 (immediate market reaction)
3. **Intermediate:** Cumulative return from day t+5 → t+20 (post-event momentum)

**Portfolio Construction:**
- At each FOMC date, rank all stocks by CNN20D5P (up-probability)
- Form 10 decile portfolios (Decile 0 = lowest probability, Decile 10 = highest)
- Compute equal-weight (EW) and value-weight (VW) returns
- Primary variable of interest: H-L spread

**Prediction Alignment:**
- Use most recent CNN prediction available **before** each FOMC announcement
- Implemented via `pd.merge_asof()` with backward direction (prevents look-ahead bias)
- Example: FOMC meeting June 15 → use prediction from June 12

**Hypothesis Test:**
\[
H_0: R^{H-L}_{\text{FOMC}} = R^{H-L}_{\text{non-FOMC}}
\]
\[
H_A: R^{H-L}_{\text{FOMC}} > R^{H-L}_{\text{non-FOMC}}
\]

---

## Slide 4: Data Sources and Sample Construction

**Primary Data Sources:**

1. **CRSP Daily Stock File (1992-2024)**
   - All US common stocks (share codes 10, 11)
   - Daily OHLC prices, returns, volume, market capitalization
   - Coverage: 29,331 unique stocks, 63.3M daily observations

2. **FOMC Schedule (Federal Reserve Website)**
   - 316 FOMC meetings manually compiled (1992-2024)
   - Announcement dates, times, policy decisions

**Data Cleaning Filters:**
1. Price ≥ $5 (remove penny stocks)
2. Market cap ≥ $50M (remove micro-caps)
3. Daily volume ≥ 100,000 shares (ensure liquidity)
4. Winsorize returns at 1st/99th percentiles (reduce outlier impact)

**Image Generation:**
- Convert daily OHLC data → 60×64 pixel candlestick charts
- Normalize prices: first day close = 1.0
- 20-day rolling window

**Sample Splits:**
- **Training (in-sample):** 1992-2000 (9 years) - train CNN
- **Testing (out-of-sample):** 2001-2024 (24 years) - all analysis

**Prediction Frequency:**
- Weekly predictions (~every 5 business days)
- Generate predictions for all stocks meeting liquidity filters

---

## Slide 5: Sample Summary and Coverage

**CNN Prediction Sample (2001-2024, Out-of-Sample):**

| Metric | Value |
|--------|-------|
| Prediction weeks | ~1,200 |
| Total stock-week predictions | 8.9 million |
| Unique stocks covered | 22,480 |
| Average stocks per week | ~7,500 |
| File size | 322 MB |

**FOMC Event Coverage:**

| Period | Total FOMC Meetings | Meetings with CNN Predictions |
|--------|---------------------|-------------------------------|
| 1992-2000 (training) | 99 | 0 |
| 2001-2024 (testing) | 217 | 217 (100%) |
| **Total** | **316** | **217** |

**Outcome Variables:**
- Multi-horizon forward returns: 1-day, 3-day, 5-day, 10-day
- Portfolio returns: equal-weight (EW) and value-weight (VW)
- High-minus-Low (H-L) decile spreads
- Event window returns: pre-FOMC, reaction, intermediate

**Statistical Power:**
- Large cross-section (~7,500 stocks per prediction date)
- Long time series (24 years out-of-sample)
- Comprehensive FOMC coverage (217 events spanning 4 Fed Chairs)

---

## Speaking Notes (~5 minutes)

**Slide 1 (45 sec):**
"Building on recent work showing that CNNs can predict stock returns using price charts, my thesis asks: are these predictions MORE informative around FOMC meetings? The hypothesis is that when market attention is focused on Fed policy, technical patterns might be more predictive as investors process macroeconomic information."

**Slide 2 (90 sec):**
"I replicate the CNN model from Jiang, Xu, and Kelly 2024. The model takes a 20-day candlestick chart as input and outputs the probability of a positive return over the next 5 days. It uses three convolutional layers to extract visual patterns from the price charts. I train five independent models and average their predictions to reduce overfitting. The key outcome variable is CNN20D5P—the probability of an upward move."

**Slide 3 (90 sec):**
"For the FOMC event study, I form decile portfolios at each Fed meeting based on the CNN predictions. I examine three windows: pre-announcement to capture positioning, reaction to capture immediate market response, and intermediate to capture post-event momentum. The critical methodological point is the alignment—I use only the most recent prediction BEFORE each announcement to avoid look-ahead bias. I test whether the high-minus-low spread is larger during FOMC windows compared to normal trading days."

**Slide 4 (60 sec):**
"I use CRSP daily data from 1992 to 2024 and manually compiled FOMC dates from the Federal Reserve website. After applying standard filters for price, market cap, and liquidity, I have 63 million daily observations covering about 29,000 stocks. I convert the price data into candlestick chart images. The sample is split chronologically: 1992-2000 for training the CNN, and 2001-2024 for all out-of-sample testing."

**Slide 5 (30 sec):**
"This construction gives me 8.9 million weekly stock predictions over 24 years, covering about 22,000 stocks. For the event study, I have 217 FOMC meetings with CNN predictions. This large sample provides strong statistical power to detect differences between FOMC and non-FOMC periods."

---

## Anticipated Q&A

**Q: Why weekly predictions instead of daily?**
A: Following JKX (2024), weekly frequency balances computational cost with adequate sampling. The 5-day prediction horizon aligns with typical rebalancing frequencies in practice.

**Q: How do you prevent look-ahead bias in the FOMC alignment?**
A: I use `pd.merge_asof()` with backward direction, which strictly takes the most recent prediction BEFORE the event. For example, if FOMC is June 15, I use the prediction from June 12, never from June 16 or later.

**Q: Why ensemble 5 models?**
A: Neural networks are sensitive to random initialization. Averaging 5 independent models reduces this variance and improves out-of-sample robustness, following standard practice in ML.

**Q: What if there are no predictions close to an FOMC date?**
A: The backward merge can go back up to 5 business days (one week). If no prediction exists within a week, that stock-event pair is dropped. This affects less than 2% of observations.

**Q: Are the CNN predictions truly out-of-sample?**
A: Yes. The CNN is trained only on 1992-2000 data. All predictions for 2001-2024 are generated from the trained model without any retraining or parameter updates.

**Q: Why separate equal-weight and value-weight?**
A: EW captures the cross-sectional average effect, while VW shows if the effect is economically significant for large-cap investors. Often, predictability is stronger in small caps.


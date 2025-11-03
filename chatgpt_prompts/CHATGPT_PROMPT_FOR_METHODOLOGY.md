# ChatGPT Prompt for Writing Methodology Sections

**Copy-paste this entire prompt to ChatGPT:**

---

## YOUR TASK

I need you to help me write the **Data & Methodology sections** of my undergraduate finance thesis. I'm replicating and extending Jiang et al. (2023)'s CNN-based stock return prediction to FOMC events.

**Audience:** Finance professors and students (NOT computer science - avoid technical jargon)

**Tone:** Academic but accessible, similar to standard finance papers

**Length:** ~3,000-4,000 words total for both sections

---

## REQUIRED READING (Do this in order)

### STEP 1: Read Research Papers for Style and Structure

**First, read ALL papers in the "Thesis Lit Review Sources" folder to learn:**
- Academic writing style for finance
- How to structure data and methodology sections
- How similar papers describe their methods
- Appropriate level of technical detail
- Citation practices

**Pay special attention to:**
- Jiang, Kelly & Xiu (2023) - This is what I'm replicating
- Lucca & Moench (2015) - Pre-FOMC drift literature
- Any other event study papers - For FOMC methodology structure

### STEP 2: Read My Documentation

**After understanding the academic style, read these files from my repo:**

1. **docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md** - Comprehensive guide (READ THIS FIRST)
   - Section 3: "CNN Model Explained (For Finance Audience)"
   - Section 4: "Your Complete Pipeline"
   - Section 5: "What's Original vs What You Replicated"

2. **docs/THESIS_DATA_METHODOLOGY.md** - Detailed data methodology

3. **FOMC_METHODOLOGY.md** - FOMC event study methodology

4. **docs/METHODOLOGY_GUIDE_FOR_GPT.md** - Code structure reference

5. **FINAL_RESULTS_SUMMARY.md** - Final results for context

6. **OVERLAP_CONCERN_RESOLVED.md** - How to address temporal overlap concerns

---

## SECTION 1: DATA (Write This First)

### What to Include:

**3.1 Stock Return Data**
- Source: CRSP daily stock file via Wharton Research Data Services (WRDS)
- Sample period: 2001-2024 (chosen to match CNN prediction availability)
- Stock universe: Common stocks (share codes 10, 11) on NYSE, AMEX, NASDAQ
- Filters applied:
  * Exclude stocks priced < $5 (avoid penny stocks)
  * Exclude stocks with market cap < NYSE 20th percentile (liquidity)
  * Require 200+ trading days in past year (data availability)
- Variables: Daily returns, market capitalization, volume
- Return calculation: Log returns for multi-period aggregation
- **Mention:** This follows standard asset pricing filters (e.g., Fama-French)

**3.2 Price Chart Data**
- Source: Daily OHLC (Open, High, Low, Close) from CRSP
- Image construction:
  * 20-day lookback window
  * Normalized to start at 1.0 (relative price movements)
  * Converted to 32×32 grayscale images
  * Resembles candlestick charts familiar to traders
- **Emphasize:** Images capture visual patterns humans see when charting
- **Mention:** This is Jiang et al.'s approach - we replicate their exact method

**3.3 FOMC Announcement Schedule**
- Source: Federal Reserve Board website (official schedule)
- Coverage: 316 scheduled FOMC meetings (1992-2024)
- Used period: 217 meetings (2001-2024) with CNN prediction availability
- Frequency: ~8 meetings per year
- **Key point:** We use scheduled meetings only (exclude unscheduled emergency meetings)

**3.4 Sample Construction**
- Final sample: ~8.9 million weekly stock-week observations (2001-2024)
- Weekly frequency: Predictions made on Fridays (or last trading day of week)
- Cross-sectional coverage: ~2,500-3,500 stocks per week
- **Mention:** Weekly frequency balances data sufficiency with computational feasibility

---

## SECTION 2: METHODOLOGY (Write This After Data Section)

### What to Include:

**4.1 CNN Model Architecture (Jiang et al. 2023 Replication)**

**Important:** Use the explanation from "Section 3: CNN Model Explained" in COMPLETE_THESIS_GUIDE_FOR_WRITING.md. Write for FINANCE audience, NOT computer science.

Include:
- What CNN does: Detects visual patterns in price charts (like momentum, reversals, support/resistance)
- Input: 20-day price chart (32×32 grayscale image)
- Output: Probability that stock will rise over next 5 days (0 to 1)
- Architecture: 3 convolutional layers → pooling → fully connected layers → sigmoid output
- **Analogy:** "Like how a radiologist detects patterns in X-rays, CNN detects patterns in price charts"
- Training: Ensemble of 5 independently trained models (average predictions for stability)
- Training period: 1993-2000 (out-of-sample testing: 2001-2024)
- **Key point:** We use Jiang et al.'s EXACT architecture and code (replication)

**What NOT to include:**
- ❌ Don't describe convolution operations in detail
- ❌ Don't use terms like "kernels," "activation functions," "backpropagation"
- ❌ Don't include mathematical formulas for CNN layers
- ✅ DO focus on economic intuition: CNN learns which visual patterns predict returns

**4.2 Portfolio Construction**

Include:
- Weekly rebalancing (every Friday)
- Decile ranking: Sort stocks by CNN prediction (up_prob), form 10 equal groups
- Two weighting schemes:
  * Equal-weight (EW): Each stock gets 1/N weight in its decile
  * Value-weight (VW): Weight by market capitalization
- Long-short strategy: Long decile 10 (highest predicted), short decile 1 (lowest predicted)
- **Rationale for EW vs VW:** EW captures small-cap effects, VW represents institutional-scale feasibility
- Performance metrics: Annual return, volatility, Sharpe ratio, turnover

**4.3 Horizon Evaluation**

Include:
- Test prediction accuracy at three horizons: 1-day, 3-day, 10-day
- Purpose: Understand how prediction strength evolves over time
- Hypothesis: If CNN detects momentum, spreads should increase with horizon
- Measurement: High-minus-low (H-L) spread at each horizon

**4.4 FOMC Event Study**

**THIS IS YOUR MAIN CONTRIBUTION - Spend most time here!**

**Timeline First (Critical for Addressing Overlap Concern):**
Use the timeline from OVERLAP_CONCERN_RESOLVED.md:

"For each FOMC announcement, we identify the most recent CNN prediction made on or before the announcement date using a backward-looking merge algorithm (pandas merge_asof with direction='backward'). For example, if an FOMC announcement occurs on June 15, 2020, we use the prediction from June 12, 2020 (or the most recent Friday before that). This ensures predictions strictly precede all measured returns, eliminating look-ahead bias."

**Event Window Definitions:**

Based on FOMC_METHODOLOGY.md, describe the THREE windows:

1. **Announcement Day (t):** Return on the day Fed releases its decision
   - Captures immediate market reaction to FOMC statement
   - Measured: Open to close on day t

2. **Reaction (t+1):** Return on next trading day
   - Captures overnight digestion and continued response
   - Measured: Open to close on day t+1

3. **Intermediate (t+5 to t+20):** Cumulative return 5-20 days after announcement
   - Captures gradual information diffusion over 2-4 weeks
   - Measured: Close(t+4) to Close(t+20) using cumulative log returns

**Why These Windows (Address Professor's Concern):**
"We focus on announcement-day forward windows where temporal ordering is unambiguous: CNN predictions (made 1-5 days before FOMC) strictly precede all measured returns. Testing pre-announcement drift (Lucca & Moench 2015, days t-5 to t-1) would require predictions made at least 2 days before announcements, limiting sample size and creating potential overlap concerns. Our approach tests whether CNN predictions (made before FOMC) predict announcement-related returns, directly addressing our hypothesis about enhanced performance during macro events."

**Decile Performance:**
- For each window, rank stocks into deciles by CNN prediction
- Compute equal-weighted and value-weighted returns for each decile
- Calculate high-minus-low (H-L) spread
- Test statistical significance using one-sample t-tests (H0: mean H-L = 0)

**Statistical Testing:**
- One-sample t-test: Is mean H-L significantly different from zero?
- N = 217 FOMC events (2001-2024)
- Standard errors account for cross-event variation
- Report: t-statistics, p-values, 95% confidence intervals
- Significance levels: *** p<0.01, ** p<0.05, * p<0.10

---

## KEY POINTS TO EMPHASIZE

1. **Replication vs Extension:**
   - Sections 4.1-4.3 are REPLICATION (Jiang et al. 2023)
   - Section 4.4 is YOUR EXTENSION (novel contribution)
   - Be VERY clear about this distinction

2. **No Overlap Issues:**
   - Predictions made BEFORE all measured windows
   - Use timeline visualization from OVERLAP_CONCERN_RESOLVED.md
   - Emphasize this addresses common event study concerns

3. **Finance Focus:**
   - CNN is a tool for detecting visual patterns (like technical analysis)
   - Avoid deep CS/ML jargon
   - Use economic intuition throughout

4. **EW vs VW Interpretation:**
   - EW = small-cap/retail-driven effects
   - VW = institutional-scale/large-cap patterns
   - This tests behavioral hypothesis (limited attention in small caps)

---

## WHAT NOT TO DO

❌ Don't copy-paste code or technical implementation details  
❌ Don't use machine learning jargon without explanation  
❌ Don't include mathematical formulas for CNN operations  
❌ Don't discuss hyperparameters, batch sizes, learning rates  
❌ Don't make it sound like a computer science paper  

✅ DO make it sound like a standard finance paper (like papers in JF, JFE)  
✅ DO emphasize economic intuition  
✅ DO clearly separate replication from your contribution  
✅ DO address the temporal ordering/overlap concern explicitly  

---

## OUTPUT FORMAT

Please write TWO sections in standard academic format:

**Section 3: Data**
- 3.1 Stock Return Data
- 3.2 Price Chart Data
- 3.3 FOMC Announcement Schedule
- 3.4 Sample Construction

**Section 4: Methodology**
- 4.1 CNN Model (Replication of Jiang et al. 2023)
- 4.2 Portfolio Construction
- 4.3 Horizon Evaluation
- 4.4 FOMC Event Study (Novel Contribution)

**Style Guidelines:**
- Match the writing style and structure of the papers in "Thesis Lit Review Sources"
- Use academic tone similar to Journal of Finance, Journal of Financial Economics
- Include citations where appropriate (Jiang et al. 2023, Lucca & Moench 2015, etc.)
- Use clear transitions between subsections
- Balance technical precision with readability (like the papers you read)
- For event study methodology, follow the structure you saw in similar papers

---

## ADDITIONAL CONTEXT

**My thesis question:**
"Does allowing a CNN to interpret price trends confer an edge particularly during high-information events like FOMC announcements, potentially due to behavioral dynamics?"

**My three contributions:**
1. Replication of Jiang et al. (2023) CNN predictions
2. Event-conditioned performance analysis around FOMC announcements
3. Behavioral interpretation (limited attention, EW vs VW)

**Sample size:**
- Weekly predictions: 8.9M stock-week observations (2001-2024)
- FOMC events: 217 meetings
- Stocks per week: ~2,500-3,500

---

Ready? Please write the Data & Methodology sections now, following all the guidelines above.


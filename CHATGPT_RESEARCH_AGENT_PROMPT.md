# ChatGPT Research Agent Prompt - Find Additional Literature
**Copy-paste this to ChatGPT with research/web search capabilities**

---

## YOUR TASK

I need you to find additional academic papers to strengthen my finance thesis. 

**CRITICAL:** First check my existing Box folder "Thesis Lit Review Sources" to avoid recommending papers I already have.

---

## MY THESIS SUMMARY

### **Research Question:**
Does convolutional neural network (CNN) based return predictability vary between FOMC announcement weeks and normal weeks?

### **Main Finding:**
CNN High-Low spreads are **0.78 percentage points LOWER** during FOMC weeks compared to matched control periods (t = -11.90, p < 0.001), representing an **89% reduction in predictability**.

### **Interpretation:**
This supports the **attention-based efficiency hypothesis**:
- **High attention (FOMC weeks):** Institutional traders dominate → Technical patterns arbitraged quickly → Markets efficient → CNN predictability collapses (0.10% spread)
- **Low attention (normal weeks):** Attention diffused → Retail participation higher → Patterns persist → Markets inefficient → CNN predictability strong (0.88% spread)

### **Key Evidence:**
- Effect concentrated in **small caps** (EW effect 2-4x larger than VW)
- Robust across all horizons (1-10 days), time periods, Fed chairs
- Declining over time: -1.70% (Greenspan) → -0.37% (Powell)

### **Theoretical Foundation:**
Primary: **Hirshleifer & Sheng (2021)** - show drift is 52-71% smaller on macro announcement days due to institutional attention surges

---

## PAPERS I ALREADY HAVE (Box Folder: "Thesis Lit Review Sources")

**Please check this folder FIRST before recommending papers!**

### **Core Papers I'm Already Citing:**

**Attention & Behavioral Finance:**
- Hirshleifer & Sheng (2021) - Macro news and drift reduction [PRIMARY THEORY]
- Tan, Zhang & Zhou (2023) - Anomalies on FOMC days
- Peng & Xiong (2006) - Category learning and attention
- Hong & Stein (1999) - Gradual information diffusion
- Hirshleifer, Lim & Teoh (2009) - Limited attention and earnings drift
- Kacperczyk, Van Nieuwerburgh & Veldkamp (2016) - Information choice
- Barber & Odean (2008) - Attention-grabbing stocks
- Daniel, Hirshleifer & Subrahmanyam (1998) - Overconfidence
- Barberis, Shleifer & Vishny (1998) - Investor sentiment model
- Stambaugh, Yu & Yuan (2012) - Mispricing and sentiment

**FOMC & Macro Events:**
- Lucca & Moench (2015) - Pre-FOMC drift
- Kurov, Wolfe & Gilbert (2021) - FOMC drift evolution and press conferences
- Savor & Wilson (2013) - Macro announcements and equity risk premia
- Savor & Wilson (2014) - Asset pricing seasonal effects
- Bernanke & Kuttner (2005) - Fed policy and stock market reaction
- Johannes, Kaeck & Seeger (2024) - FOMC event risk in options
- Boguth, Gregoire & Martineau (2019) - Sharpening the pre-FOMC drift

**Technical Analysis:**
- Brock, Lakonishok & LeBaron (1992) - Technical trading rules work
- Lo, Mamaysky & Wang (2000) - Foundations of technical analysis and chart patterns
- Han, Zhou & Zhu (2016) - Trend factor
- Neely et al (2014) - Forecasting equity premium with technical indicators
- Detzel et al (2020) - Learning and predictability via technical analysis

**Machine Learning in Finance:**
- Jiang, Kelly & Xiu (2023) - CNN and chart images [WHAT I REPLICATE]
- Gu, Kelly & Xiu (2020) - Empirical asset pricing via machine learning
- Kozak, Nagel & Santosh (2020) - Shrinking the cross-section
- Krauss, Do & Huck (2017) - Deep neural networks and statistical arbitrage
- Hu et al (2018) - Deep learning for portfolio optimization with candlestick patterns
- Kim & Kim (2019) - CNN-LSTM for stock prediction
- Murray, Xia & Xiao (2024) - Critiques and extensions of JKX

---

## WHAT I NEED

Find **10-15 additional papers** in these categories that would strengthen my thesis. For each paper, explain HOW it supports my narrative.

---

## CATEGORY 1: Attention-Based Market Efficiency (HIGH PRIORITY)

**What I need:** Papers showing attention affects market efficiency, price discovery speed, or drift magnitude

**Specifically useful papers about:**
- How institutional vs retail investors affect efficiency
- Attention concentration during scheduled events
- Information processing speed varying with attention
- Limited attention creating exploitable patterns
- Attention shocks and efficiency changes

**Why I need them:** 
To strengthen theoretical foundation that high attention → efficiency → pattern elimination

**Papers I DON'T already have that might exist:**
- DellaVigna & Pollet on attention and earnings
- Cohen & Frazzini on attention constraints
- Engelberg & Parsons on media attention
- Da, Engelberg & Gao on attention measures
- Any other attention → efficiency papers

---

## CATEGORY 2: Event-Conditional Return Predictability (HIGH PRIORITY)

**What I need:** Papers showing how anomalies, factors, or predictability varies around scheduled macro events

**Specifically useful papers about:**
- Anomaly returns on announcement days (employment, CPI, GDP, Fed)
- Time-varying predictability around events
- Cross-sectional pattern changes during macro news
- Conditional asset pricing around events
- Event-study designs for testing predictability

**Why I need them:**
My contribution is showing CNN predictability is event-conditional. Need more papers showing other signals are also event-conditional.

**Possible papers:**
- Ai & Bansal on risk and return around macro announcements
- Jiang, Li & Wang on short-term reversals and macro news
- Cieslak, Morse & Vissing-Jorgensen on Fed information effects
- Gilbert, Scotti, Strasser & Vega on macro news and asset prices
- Any papers showing predictability varies with scheduled events

---

## CATEGORY 3: Small-Cap Effects and Limited Arbitrage (MEDIUM PRIORITY)

**What I need:** Papers explaining why patterns concentrate in small caps

**Specifically useful papers about:**
- Small cap inefficiency vs large cap efficiency
- Institutional coverage and arbitrage limits
- Retail investor concentration in small caps
- Transaction costs and liquidity effects by firm size
- Why anomalies stronger in small/illiquid stocks

**Why I need them:**
My key evidence is EW >> VW (2-4x). Need papers explaining why small caps are more behaviorally-driven.

**Possible papers:**
- Hou & Moskowitz on market frictions and pricing
- Nagel on short-sale constraints  
- Pontiff on costly arbitrage
- Lee, Shleifer & Thaler on closed-end funds and investor sentiment (small vs large)
- Any papers on size-dependent market efficiency

---

## CATEGORY 4: ML Model Limitations & State-Dependence (MEDIUM PRIORITY)

**What I need:** Papers discussing when ML models fail or showing performance is state-dependent

**Specifically useful papers about:**
- Machine learning failures in finance
- Regime-dependent model performance
- When algorithms break down (crises, volatility, events)
- Overfitting and out-of-sample failures
- Conditions for ML success vs failure in markets

**Why I need them:**
My contribution is showing CNN performance is NOT uniform—it depends on market state (attention level). Need papers discussing ML limitations.

**Possible papers:**
- Kelly, Malamud & Zhou on model instability
- Avramov, Cheng & Metzker on machine learning and anomalies
- Messmer on deep learning pitfalls
- Any papers on conditional ML performance
- Papers on algorithm competition and efficiency

---

## CATEGORY 5: Market Microstructure During Events (LOWER PRIORITY)

**What I need:** Papers on how microstructure changes during macro events

**Specifically useful papers about:**
- Bid-ask spreads around FOMC
- Liquidity and trading volume around Fed announcements
- Investor composition shifts (institutional vs retail) during events
- High-frequency trading around macro news
- Price discovery mechanisms during scheduled events

**Why I need them:**
Could help explain HOW patterns disappear (through what trading mechanisms)

---

## SEARCH INSTRUCTIONS

### **Step 1: Check My Box Folder**
Access folder: **"Thesis Lit Review Sources"**

List all papers currently in the folder. I've listed the main ones above, but there may be others.

### **Step 2: Search Google Scholar / SSRN / Finance Journals**

**Search terms to try:**
- "attention market efficiency macro announcements"
- "FOMC institutional trading retail investors"
- "event-conditional asset pricing predictability"
- "limited attention anomaly returns"
- "small cap efficiency arbitrage limits"
- "machine learning state-dependent finance"
- "scheduled macro news stock returns"
- "investor attention information diffusion"

**Top journals to check:**
- Journal of Finance
- Journal of Financial Economics
- Review of Financial Studies
- Journal of Financial and Quantitative Analysis
- Management Science
- Review of Asset Pricing Studies

### **Step 3: For Each Paper You Find**

**Provide:**
1. **Full citation** (authors, year, title, journal)
2. **Main finding** (1-2 sentences)
3. **Why it's useful for my thesis** (how it supports attention-efficiency narrative)
4. **Where to cite it** (Introduction? Lit review? Discussion?)
5. **Key quote or statistic** I could use
6. **Is it in my Box folder already?** (Yes/No - check first!)

### **Step 4: Prioritize Papers**

**Rank papers by usefulness:**
- **Tier 1 (Must have):** Directly supports attention-efficiency or event-conditional predictability
- **Tier 2 (Very useful):** Supports mechanism (small caps, institutional effects, etc.)
- **Tier 3 (Nice to have):** General support or interesting extension

---

## OUTPUT FORMAT

Please provide:

### **Summary**
- Total papers found: X
- Papers I already have (checked Box folder): Y
- **New papers recommended: Z**

### **For Each New Paper:**

```
Paper #1: [Tier 1]
Citation: Author(s) (Year). "Title". Journal, Vol(Issue), pages.
Main Finding: [1-2 sentences]
Why Useful: [How it supports my attention-efficiency narrative]
Where to Cite: [Introduction/Lit Review/Discussion]
Key Quote/Stat: [Something I can cite]
Available: [Link to paper or where to find it]
```

### **Papers by Category:**
- Attention-based efficiency: X papers
- Event-conditional predictability: Y papers
- Small-cap effects: Z papers
- ML limitations: A papers
- Microstructure: B papers

---

## PRIORITY GUIDANCE

**Most valuable papers would:**
1. Show other signals/anomalies also decline during high-attention events
2. Explain WHY attention causes efficiency (mechanism papers)
3. Document small-cap vs large-cap differences in efficiency
4. Show ML performance varies with market conditions
5. Provide additional evidence for institutional attention surges

**Less valuable papers:**
- General ML in finance (I have enough from Gu et al, JKX)
- General FOMC effects (I have Lucca & Moench, Savor & Wilson)
- Papers about pre-FOMC drift specifically (I don't test this)

---

## EXAMPLE OUTPUT (What I Want)

```
Paper #1: [Tier 1 - Must Have]
Citation: Cohen, L., & Frazzini, A. (2008). "Economic Links and Predictable Returns". 
Journal of Finance, 63(4), 1977-2011.

Main Finding: Investors with limited attention fail to incorporate information from 
economically linked firms, creating predictable cross-firm return patterns. The effect 
is stronger for stocks with less analyst coverage.

Why Useful: Directly supports your mechanism that limited attention creates exploitable 
patterns, and that these patterns concentrate where coverage is limited (small caps). 
Provides theoretical foundation for why CNN patterns should disappear when attention is high.

Where to Cite: Literature Review Section 2.3 (Behavioral Finance), Discussion Section 6.2

Key Quote: "When attention is limited, investors focus on information about individual 
firms and fail to process information about related firms... This leads to predictable 
cross-firm return dynamics."

Available: JSTOR, published paper
```

---

## START SEARCHING

Please search now and provide 10-15 new papers (not already in my Box folder) that would strengthen my thesis, following the format above.

**Focus on Tier 1 papers** (directly support attention-efficiency or event-conditional predictability).


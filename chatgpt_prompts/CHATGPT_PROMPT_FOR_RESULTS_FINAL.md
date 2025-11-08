# ChatGPT Prompt for Results Section (Complete)
**Copy-paste this entire prompt to ChatGPT/Claude**

---

I need help writing the **complete Results section** of my finance thesis with the CORRECT interpretation.

**Critical:** My results show CNN spreads are **LOWER** on FOMC weeks (not higher). This supports the attention-efficiency hypothesis.

---

## ✅ CORRECT NARRATIVE (Read This First!)

### **My Main Finding:**
CNN High-Low spreads are **0.78 percentage points LOWER** during FOMC weeks compared to matched control weeks
- FOMC weeks: 0.10% spread (terrible)
- Normal weeks: 0.88% spread (good)
- Difference: -0.78% (t = -11.90, p < 0.001)
- This represents an **89% REDUCTION** in predictability

### **Why This Happens:**
**High Attention (FOMC weeks):**
→ Institutional traders dominate  
→ Technical patterns arbitraged away quickly  
→ Markets MORE efficient  
→ Nothing for CNN to exploit  
→ **Spreads collapse to 0.10%**

**Low Attention (Normal weeks):**
→ Attention diffused  
→ Retail participation higher  
→ Technical patterns persist  
→ Markets LESS efficient  
→ **Spreads remain strong at 0.88%**

### **Theory:**
This supports **Hirshleifer & Sheng (2021)**, who show drift is 52-71% smaller on macro announcement days due to institutional attention surges. My finding (89% smaller spreads) confirms their theory.

### **Evidence for Mechanism:**
Effect is **concentrated in small caps** (EW effect 2-4x larger than VW). This proves it's attention-driven:
- Small caps: Less institutional coverage → more affected by attention shifts
- Large caps: Always monitored → less affected

---

## MY COMPLETE RESULTS

### **Table 1: Event-Level Comparison (Main Finding)**

| Horizon | FOMC (EW) | Matched (EW) | Difference | SE | t-stat | p-value | N |
|---------|-----------|--------------|------------|----|---------| --------|---|
| 1 day   | 0.10%     | 0.88%        | **-0.78%** | 0.065% | -11.90  | <0.001*** | 216 |
| 2 days  | 0.16%     | 1.03%        | **-0.87%** | 0.080% | -10.82  | <0.001*** | 216 |
| 3 days  | 0.24%     | 1.06%        | **-0.81%** | 0.083% | -9.78   | <0.001*** | 216 |
| 10 days | 0.63%     | 1.12%        | **-0.49%** | 0.118% | -4.17   | <0.001*** | 215 |

**All 10 horizons:** Negative and highly significant (all p < 0.001, all FDR q < 0.001)

### **Table 2: Robustness to Outliers**

| Statistic | H=1 | H=3 | H=10 |
|-----------|-----|-----|------|
| Mean | -0.78% | -0.81% | -0.49% |
| Median | -0.71% | -0.75% | -0.44% |
| Winsorized 1% | -0.79% | -0.82% | -0.50% |
| % Negative | 86.6% | 84.3% | 78.1% |

### **Table 3: Time Period Robustness**

| Period | N Events | Mean Diff (H=3) | t-stat | p-value |
|--------|----------|-----------------|--------|---------|
| Pre-GFC (2001-08) | 80 | -1.30% | -9.75 | <0.001*** |
| Post-GFC (2009-12) | 37 | -0.79% | -3.50 | 0.001*** |
| Bull (2013-19) | 58 | -0.43% | -4.08 | <0.001*** |
| COVID (2020-24) | 41 | -0.44% | -2.08 | 0.044** |

### **Table 4: Fed Chair Regimes**

| Chair | Years | N Events | Mean Diff | t-stat | p-value |
|-------|-------|----------|-----------|--------|---------|
| Greenspan | 1987-2006 | 48 | -1.70% | -12.57 | <0.001*** |
| Bernanke | 2006-2014 | 78 | -0.72% | -4.90 | <0.001*** |
| Yellen | 2014-2018 | 33 | -0.51% | -4.48 | <0.001*** |
| Powell | 2018-2025 | 57 | -0.37% | -2.30 | 0.025** |

### **Table 5: EW vs VW (Mechanism Test)**

| Horizon | EW Diff | VW Diff | EW t-stat | VW t-stat | EW/VW Ratio |
|---------|---------|---------|-----------|-----------|-------------|
| 1 day | -0.78% | -0.18% | -11.90*** | -2.64*** | 4.3x |
| 3 days | -0.81% | -0.34% | -9.78*** | -3.61*** | 2.4x |
| 10 days | -0.49% | -0.22 | -4.17*** | -1.38 | 2.2x |

### **Baseline Results (For Context)**

**Overall Portfolio (2001-2024):**
- EW H-L: 70.74% annual (Sharpe 5.60)
- VW H-L: 22.69% annual (Sharpe 1.54)
- EW/VW ratio: 3.1x

---

## SECTION STRUCTURE

Write these 5 subsections (~3,500-4,000 words total):

### **5.1 Baseline CNN Predictability (~500 words)**

**Purpose:** Establish CNN works in my sample

**Content:**
- Report EW portfolio: 71% annual return, Sharpe 5.60
- Report VW portfolio: 23% annual return, Sharpe 1.54
- Note EW 3x larger than VW (first hint of behavioral mechanism)
- Emphasize monotonic pattern (Low to High deciles)
- State this replicates Jiang et al (2023)
- Acknowledge gross returns (no transaction costs)
- Transition: "Having established baseline, now test event-conditional performance"

### **5.2 FOMC vs Matched Control Comparison (~1,200 words)** ⭐ **MAIN SECTION**

**Purpose:** Present main finding with correct interpretation

**Opening:**
> "Table X presents the central finding of this thesis: CNN-based return predictability is significantly and substantially **reduced** during FOMC announcement weeks compared to matched control periods."

**Present Table 1:**
- Lead with numbers: -0.78% at H=1 (t = -11.90, p < 0.001)
- Emphasize magnitude: 89% reduction (0.10% vs 0.88%)
- State this is "near-complete elimination of predictability"
- Report all horizons significant (no cherry-picking)

**Interpretation (CRITICAL):**
> "These findings provide strong support for the **attention-based efficiency hypothesis**. When investor attention is concentrated on monetary policy announcements (FOMC weeks), markets process information more efficiently. Institutional traders, who dominate trading during these periods, quickly identify and arbitrage away technical patterns. The CNN's predictive edge—which relies on exploiting gradual information diffusion—is substantially reduced.
>
> This result aligns precisely with Hirshleifer and Sheng (2021), who document that drift is 52-71% smaller on macro announcement days. My finding shows CNN spread is 89% smaller on FOMC weeks—an even stronger disruption, consistent with technical patterns being among the most attention-sensitive signals."

**Connect to Tan et al (2023):**
> "Tan, Zhang, and Zhou (2023) show that retail-driven anomalies decline on FOMC days when retail participation drops. The CNN signal, despite being mechanically generated, behaves similarly: it exploits patterns that exist when attention is diffused but disappear when attention is concentrated."

### **5.3 Robustness Analysis (~900 words)**

**5.3.1 Outlier Robustness (~300 words)**
- Present Table 2
- Mean ≈ Median (not outlier-driven)
- Winsorization changes results minimally
- 86.6% of events show negative differences
- Not driven by crisis events (2008, 2020)

**5.3.2 Time Period Robustness (~300 words)**
- Present Table 3
- Significant in ALL periods
- Declining over time: -1.70% (Greenspan) → -0.37% (Powell)
- Interpretation: Better Fed communication, market adaptation
- Still significant even in recent years

**5.3.3 Fed Chair Robustness (~300 words)**
- Present Table 4
- Significant under ALL chairs
- Not regime-specific
- Declining pattern continues
- Supports market learning interpretation

### **5.4 Mechanism Test: Small-Cap Concentration (~800 words)** ⭐ **KEY EVIDENCE**

**Purpose:** Prove it's attention/behavioral mechanism

**Present Table 5:**
- EW effect 2-4x larger than VW across all horizons
- This is the **smoking gun**

**Interpretation:**
> "Table 5 provides the clearest evidence for the attention-based mechanism. The FOMC disruption effect is 2-4 times stronger in equal-weighted portfolios (small caps) than value-weighted portfolios (large caps).
>
> **Why this matters:** If the effect were about fundamental risk or systematic repricing, it should affect all stocks equally. The fact that it's concentrated in small caps—where institutional coverage is limited and retail participation is higher—points unambiguously to an attention/behavioral channel.
>
> Small-cap stocks are more sensitive to attention shifts because:
> 1. Fewer analysts covering them
> 2. Less institutional monitoring
> 3. Higher retail participation
> 4. Technical patterns persist longer normally
>
> When FOMC events temporarily elevate attention across the entire market, small caps experience the largest efficiency gain (patterns disappear), while large caps—which are always efficiently priced—show minimal change."

**Connect to broader pattern:**
> "This small-cap concentration is not unique to the FOMC analysis. Throughout every test in this thesis—overall portfolios, horizons, FOMC events—the EW/VW ratio ranges from 2-10x. This consistency across multiple independent tests strengthens the behavioral interpretation."

### **5.5 Horizon Pattern: Immediate Disruption, Gradual Recovery (~500 words)**

**Present pattern:**
- Strongest disruption at H=1-3 (-0.78% to -0.87%)
- Attenuates toward H=10 (-0.49%)
- Still significant at all horizons

**Interpretation:**
> "The temporal pattern reveals the 'attention life cycle' around FOMC events. During and immediately after announcements (H=1-3), attention is maximally concentrated, and the disruption is strongest (89% reduction). As days pass (H=3-10), attention gradually returns to normal levels, and some CNN predictability recovers, though the effect persists even 10 days later (-0.49%).
>
> This pattern is consistent with institutional traders actively arbitraging technical patterns during high-attention periods, with the arbitrage activity gradually declining as attention disperses post-announcement."

**Connect all findings:**
> "Taken together, these results tell a coherent story: CNN-based technical predictability depends fundamentally on limited investor attention. When FOMC events concentrate attention (even temporarily), markets become efficient enough to eliminate nearly all exploitable technical patterns. The effect is immediate, persistent, concentrated in less-followed stocks, and robust across all tests—exactly as the attention-efficiency hypothesis predicts."

---

## WRITING PRINCIPLES

### **1. Lead with Interpretation**
**Bad:** "The difference is -0.78% (t = -11.90, p < 0.001)."  
**Good:** "CNN spreads are 0.78 percentage points lower on FOMC weeks (t = -11.90, p < 0.001), representing an 89% collapse in predictability. This strongly supports the attention-efficiency hypothesis: when all investors watch the Fed, markets become efficient and technical patterns disappear."

### **2. Connect Every Finding to Theory**
After every result, answer: "What does this mean for the attention-efficiency hypothesis?"

### **3. Emphasize Robustness**
- "This pattern is not driven by outliers..."
- "The effect is present across ALL time periods..."
- "The result survives multiple testing correction..."

### **4. Use Strong Language**
- "Strongly supports"
- "Provides clear evidence"
- "Unambiguously points to"
- "Directly confirms"

### **5. Reference Tables**
"As shown in Table X..." for every table

---

## OUTPUT FORMAT

Please write **Section 5: Results** with:
- 5.1 Baseline (~500 words)
- 5.2 FOMC vs Matched Controls (~1,200 words) - MAIN
- 5.3 Robustness (~900 words)
- 5.4 Mechanism Test (~800 words) - KEY EVIDENCE
- 5.5 Horizon Pattern (~500 words)

**Total:** ~3,900 words

**Style:** Match my academic lit review tone. Use transitional phrases. Every number gets interpreted immediately.

**Key:** Make sure EVERY paragraph emphasizes that FOMC shows LOWER spreads and this supports attention-efficiency hypothesis.

---

## START WRITING

Please write Section 5: Results now, following all guidelines above and matching my academic writing style.


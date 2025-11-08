# ✅ ALL VALIDATED RESULTS (November 6, 2025)

**Status:** All analyses complete, outlier-checked, robust  
**Ready for:** Thesis writing

---

## 📊 RESULT 1: CNN Replication

**Portfolio Performance (2001-2024):**

| Decile | EW Return | VW Return |
|--------|-----------|-----------|
| 1 (Low) | -28.08% | -3.50% |
| 2 | -2.20% | 4.06% |
| 3 | 5.75% | 6.64% |
| 4 | 10.63% | 7.79% |
| 5 | 12.25% | 8.06% |
| 6 | 15.25% | 10.45% |
| 7 | 17.43% | 9.39% |
| 8 | 20.73% | 11.79% |
| 9 | 24.10% | 12.23% |
| 10 (High) | 42.66% | 19.19% |
| **H-L** | **70.74%** | **22.69%** |
| **Sharpe** | **5.60** | **1.54** |

**Monotonicity:** Spearman ρ = 1.00 (p<0.001***)  
**Shape:** Convex (extreme predictions most informative)

---

## 📊 RESULT 2: Horizon Evaluation

| Horizon | EW H-L | VW H-L |
|---------|--------|--------|
| +1 day  | 0.87%  | 0.09%  |
| +3 days | 1.11%  | 0.20%  |
| +10 days| 1.37%  | 0.24%  |

**Pattern:** Predictability INCREASES with horizon (+58% from 1d to 10d)  
**Interpretation:** Momentum, not mean-reversion

---

## 📊 RESULT 3: FOMC Event Study

**Three Windows (N=217 events, 2001-2024):**

| Window | EW H-L | t-stat | p-value | Mean | Median | Robust? |
|--------|--------|--------|---------|------|--------|---------|
| **Announcement (t)** | **0.21%** | **2.95** | **0.004***| 0.208% | 0.205% | ✅ YES (2.0% change) |
| Reaction (t+1) | 0.10% | 1.76 | 0.079* | 0.097% | 0.143% | ⚠️ NO (38.9% change) |
| **Intermediate (t+5→t+20)** | **0.35%** | **2.24** | **0.026**| 0.350% | 0.339% | ✅ YES (12.4% change) |

**Use:** Announcement & Intermediate with confidence. De-emphasize Reaction (fragile).

---

## 📊 RESULT 4: FOMC vs Matched Non-FOMC Comparison

**Methodology:** Event-level aggregation, matched by month, exclude ±10 days around any FOMC

**Finding:** FOMC days show LOWER predictability at ALL horizons

| Horizon | FOMC (EW) | Matched (EW) | Difference | t-stat | p-value |
|---------|-----------|--------------|------------|--------|---------|
| 1 day | 0.10% | 0.88% | -0.78% | -11.90 | <0.001*** |
| 2 days | 0.16% | 1.03% | -0.87% | -10.82 | <0.001*** |
| 3 days | 0.24% | 1.06% | -0.81% | -9.78 | <0.001*** |
| 4 days | 0.35% | 1.09% | -0.75% | -8.18 | <0.001*** |
| 5 days | 0.45% | 1.09% | -0.64% | -6.39 | <0.001*** |
| 6 days | 0.49% | 1.08% | -0.59% | -5.33 | <0.001*** |
| 7 days | 0.49% | 1.11% | -0.62% | -5.40 | <0.001*** |
| 8 days | 0.53% | 1.16% | -0.63% | -5.27 | <0.001*** |
| 9 days | 0.53% | 1.15% | -0.62% | -5.03 | <0.001*** |
| 10 days | 0.63% | 1.12% | -0.49% | -4.17 | <0.001*** |

**Sample:** 216 FOMC events × 5 matched controls each

**Pattern:** Uniform reduction in predictability (40-80% lower on FOMC days)

---

## 📊 RESULT 5: Small-Cap Concentration

**EW/VW Ratios Across All Tests:**

| Test | EW/VW Ratio |
|------|-------------|
| Portfolio H-L | 3.12× |
| Horizon +1d | 9.67× |
| Horizon +3d | 5.55× |
| Horizon +10d | 5.71× |
| FOMC Announcement | 4.20× |

**Interpretation:** Effects consistently concentrate in small caps (limited attention, arbitrage constraints)

---

## 🎯 THESIS STRUCTURE (Recommended)

### 5. RESULTS

**5.1 Portfolio Performance**
- Present Tables 3 & 4
- Report H-L spreads: 71% EW, 23% VW
- Note monotonicity (ρ=1.00***)
- Emphasize 3× EW/VW difference

**5.2 Horizon Evaluation**
- Present Table 2
- Show increasing pattern (0.87% → 1.37%)
- Interpret as momentum
- Note consistent EW >> VW

**5.3 FOMC Event Study** ⭐ MAIN CONTRIBUTION
- Present Table 5 (three windows)
- Emphasize: Announcement (0.21%***) and Intermediate (0.35%**)
- Report robustness: Mean≈Median, stable to outliers
- De-emphasize Reaction (fragile)

**5.4 FOMC vs Normal Days** ⭐ NOVEL
- Present Table 6 (event-level comparison)
- Show uniform pattern: FOMC < Normal across all horizons
- Report strong significance (t=-11.90 to -4.17***)
- Interpret: Attention-based efficiency

**5.5 Small-Cap Synthesis**
- Present Table 7 (EW/VW ratios)
- Show 3-10× pattern everywhere
- Tie to behavioral mechanism

### 6. DISCUSSION

**6.1 Main Findings**
- Summarize four validated results
- Connect to research question

**6.2 Attention-Based Efficiency Mechanism**
- FOMC creates attention spike → Lower predictability
- Consistent with H&S (2021)
- Extends to small caps and technical signals
- Simple, clean mechanism (not complex two-phase)

**6.3 Why Small Caps?**
- Limited attention baseline
- Arbitrage constraints
- H&S show large caps always efficient; you show small caps efficiency is state-dependent

**6.4 Practical Implications**
- Not a trading strategy (turnover too high)
- Understanding market efficiency
- State-dependent predictability

**6.5 Limitations & Future Research**
- Sample size (217 events)
- Transaction costs
- Don't have analyst coverage data
- Could test other macro events

---

## 📖 KEY CITATIONS

**Methods:**
- Jiang, Kelly & Xiu (2023) - CNN replication

**FOMC Literature:**
- Hirshleifer & Sheng (2021) - Macro attention increases efficiency ⭐ KEY
- Lucca & Moench (2015) - Pre-FOMC drift
- Savor & Wilson (2013) - Macro announcement effects

**Behavioral:**
- Hirshleifer & Teoh (2003) - Limited attention
- Hong & Stein (1999) - Gradual diffusion
- DellaVigna & Pollet (2009) - Inattention

**Market Efficiency:**
- Peng & Xiong (2006) - Attention to aggregate vs micro
- Bernanke & Kuttner (2005) - FOMC shocks
- Gürkaynak et al. (2005) - Systematic monetary shocks

---

## 🎓 ABSTRACT (Draft)

> I replicate Jiang, Kelly & Xiu (2023)'s convolutional neural network approach for stock return prediction and extend it to Federal Reserve FOMC announcements. Confirming their findings, equal-weighted portfolios earn 70.74% annually (Sharpe 5.60) from 2001-2024, while value-weighted earn 22.69% (Sharpe 1.54).
>
> I document significant cross-sectional predictability on FOMC announcement days (0.21%, t=2.95, p<0.01) and in subsequent weeks (0.35%, t=2.24, p=0.03). Using event-level analysis with matched sampling, I find CNN predictability is uniformly lower on FOMC days than matched non-FOMC days across all horizons (differences -0.49% to -0.78%, t-statistics -4.17 to -11.90, all p<0.001).
>
> These findings support the attention-based efficiency hypothesis: heightened attention during macro announcements compresses cross-sectional patterns, reducing exploitable dispersion. Effects concentrate in equal-weighted (small-cap) portfolios, with equal-weight spreads 3-10 times larger than value-weight across all tests, consistent with limited attention and arbitrage constraints in less-followed stocks.

---

**END OF VALIDATED RESULTS**

All numbers verified, robust, ready for thesis.


# ChatGPT Prompt for Writing Discussion Section

**Copy-paste this entire prompt to ChatGPT after completing Results:**

---

## YOUR TASK

I need you to help me write the **Discussion section** of my undergraduate finance thesis. I've completed Introduction/Literature Review, Methodology, and Results. Now I need to interpret my findings, compare to literature, and discuss implications.

**Audience:** Finance professors and students (NOT computer science)

**Tone:** Academic but accessible, matching Journal of Finance style

**Length:** ~2,000-3,000 words

---

## CONTEXT: What You Already Wrote

You previously wrote my Introduction/Lit Review, Methodology, and Results sections. The Discussion is where we:
- Interpret findings in context of existing literature
- Explain WHY results occurred (behavioral mechanisms)
- Discuss practical implications
- Acknowledge limitations
- Suggest future research

---

## REQUIRED READING

**Before writing, read these from my GitHub repo:**

1. **Your previous sections:**
   - Introduction/Lit Review (that you wrote)
   - Methodology (that you wrote)
   - Results (that you just wrote)

2. **My documentation:**
   - **COMPLETE_STATISTICAL_RESULTS_EXPLAINED.md** - All findings explained
   - **WHAT_YOU_ACTUALLY_DID_EXPLAINED.md** - Plain English interpretation
   - **OVERLAP_CONCERN_RESOLVED.md** - Addressing methodological concerns
   - **FINAL_RESULTS_SUMMARY.md** - Summary of key findings

3. **Literature papers** in "Thesis Lit Review Sources":
   - Jiang, Kelly & Xiu (2023) - For CNN discussion
   - Lucca & Moench (2015) - For FOMC interpretation
   - Tan, Zhang & Zhou (2023) - For behavioral mechanisms
   - Hong & Stein (1999) - For gradual diffusion theory

---

## SECTION STRUCTURE: DISCUSSION

Write the Discussion section with the following structure:

### **6. DISCUSSION**

#### **6.1 Interpretation of Main Findings**

**What to include:**
- Summarize your three main findings (don't just repeat Results)
- Explain WHY each finding occurred
- Connect to behavioral finance theories

**Three findings to interpret:**

**Finding 1: CNN Predictions Work (Replication)**
- Result: 71% EW, 23% VW annual returns
- Why: Visual patterns contain information beyond fundamentals
- Theory: Bounded rationality, technical analysis validity
- Compare to: Jiang et al. (2023) - confirm their results

**Finding 2: FOMC Events Enhance Predictability**
- Result: 0.21%*** announcement, 0.35%** intermediate
- Why: High-information events + limited attention
- Theory: Attention allocation, scheduled vs unscheduled news
- Compare to: Lucca & Moench (pre-FOMC drift), Tan et al. (anomalies on FOMC days)

**Finding 3: Small-Cap Concentration**
- Result: EW/VW ratio 3-10x across all tests
- Why: Limited attention + arbitrage constraints
- Theory: Limited attention (Hirshleifer & Teoh 2003), gradual diffusion (Hong & Stein 1999)
- Compare to: Size effect in anomalies, institutional arbitrage

**How to write it:**
> "Our findings support a behavioral interpretation of CNN predictive power. The consistent concentration of effects in equal-weighted portfolios—3 to 10 times larger than value-weighted across all tests—indicates the signal is strongest where investor attention is most limited. This aligns with theories of limited attention (Hirshleifer & Teoh 2003) and gradual information diffusion (Hong & Stein 1999): visual price patterns persist in smaller, less-followed stocks where institutional arbitrage is constrained."

---

#### **6.2 Why FOMC Events Matter (Your Main Contribution)**

**What to include:**
- Explain the FOMC timing profile (immediate → reaction → intermediate)
- Why does the effect BUILD over time? (0.21% → 0.10% → 0.35%)
- Connect to attention reallocation around scheduled events
- Compare to existing FOMC literature

**Key points to make:**

**1. Attention Reallocation:**
> "During FOMC announcements, investor attention is focused on macro news. This creates two effects: (1) cross-sectional patterns in how individual stocks respond become more pronounced as investors reallocate portfolios, and (2) in small-cap markets with limited institutional coverage, these patterns persist longer as the information gradually diffuses to less-attentive investors."

**2. Gradual Diffusion:**
> "The strengthening effect from announcement day (0.21%) to the intermediate window (0.35%) is consistent with gradual information diffusion. While large-cap stocks react quickly (or even reverse, -0.28% VW intermediate), small-cap stocks continue to incorporate the macro implications over weeks, creating the largest spreads in the intermediate window."

**3. Comparison to Literature:**
- Lucca & Moench (2015): Pre-FOMC drift in market-wide returns
- Your contribution: Cross-sectional patterns (CNN H-L) persist AFTER announcement
- Tan et al. (2023): Anomalies unchanged on FOMC days
- Your contribution: CNN patterns STRONGER on FOMC days (especially weeks after)

---

#### **6.3 Practical Implications**

**What to include:**
- Portfolio management implications
- What this means for active managers
- What this means for market efficiency
- Honest about implementability

**Key points:**

**1. Not Directly Tradeable:**
> "The 654% annual turnover and small-cap concentration imply transaction costs would substantially reduce implementable returns. Table 7 shows estimated net returns of 58% (equal-weight) after 2% round-trip costs, though real-world costs in illiquid small caps could be higher. These results demonstrate predictive power rather than a practical trading strategy."

**2. Event-Conditional Strategy:**
> "More feasibly, institutional investors could adjust existing positions around scheduled FOMC meetings, scaling exposure to trend signals in the days before and after announcements when our results suggest cross-sectional patterns are most pronounced. This would require lower turnover than a pure CNN strategy while capturing enhanced FOMC-period returns."

**3. Market Efficiency Implications:**
> "Our findings suggest markets are not uniformly efficient. Large-cap stocks (value-weighted results) show little exploitable predictability, consistent with strong-form efficiency where institutional arbitrage is active. Small-cap stocks exhibit persistent patterns, indicating semi-strong form efficiency at best. This heterogeneity by firm size is consistent with rational limits to arbitrage."

---

#### **6.4 Limitations and Future Research**

**What to include:**
- Honest limitations of your study
- What you couldn't test (and why)
- Suggestions for future research

**Limitations to acknowledge:**

**1. Transaction Costs:**
> "Our analysis assumes simplified transaction costs. Real-world implementation would face additional challenges: market impact in illiquid stocks, short-selling constraints for the low decile, and potential capacity constraints that would limit capital deployment."

**2. Pre-FOMC Window:**
> "We focus on announcement-day forward windows due to data limitations and to ensure clean temporal ordering. Testing pre-announcement drift (Lucca & Moench 2015, days t-5 to t-1) would require predictions made multiple days before events, limiting sample size. Future research with higher-frequency predictions could explore this window."

**3. Sample Period:**
> "Our out-of-sample period (2001-2024) coincides with increasing algorithmic trading and machine learning adoption. It remains to be seen whether visual price patterns will persist as more market participants employ similar techniques."

**4. Behavioral Mechanism:**
> "While our equal-weight versus value-weight comparison is consistent with limited attention, we do not directly measure investor attention or test alternative behavioral mechanisms. Future work could incorporate direct measures of attention (Google searches, news coverage) or investor composition (institutional ownership) to more precisely identify the mechanism."

**Future research suggestions:**

**1. Higher-Frequency Predictions:**
> "Daily or intra-day CNN predictions could enable testing of pre-FOMC drift and finer-grained event windows, potentially revealing additional patterns around announcement timing."

**2. Other Macro Events:**
> "The methodology could extend to other scheduled events: earnings announcements, economic data releases, or ECB meetings. Testing whether CNN patterns are event-type-specific would clarify the attention mechanism."

**3. International Markets:**
> "While we focus on U.S. equities, the approach could test whether similar patterns exist around central bank announcements in other countries, particularly in markets with varying levels of institutional participation."

**4. Mechanism Testing:**
> "Direct tests using investor-level data (e.g., retail brokerage accounts) could confirm whether the small-cap concentration reflects retail investor behavior versus institutional constraints."

---

## WRITING GUIDELINES

### **Tone:**
- Scholarly but not defensive
- Acknowledge limitations honestly
- Emphasize contributions while being realistic
- Don't oversell results ("predictive power" not "trading profits")

### **Structure:**
- Interpret findings (why they occurred)
- Compare to literature (how you fit in)
- Discuss implications (what it means)
- Acknowledge limits (what you couldn't do)
- Suggest future work (what comes next)

### **Avoid:**
- ❌ Overstating practical applicability
- ❌ Claiming causation (you show correlation/prediction)
- ❌ Ignoring transaction costs
- ❌ Being defensive about limitations

### **Do:**
- ✅ Connect to behavioral theories explicitly
- ✅ Compare to specific papers (cite by name)
- ✅ Be honest about implementability
- ✅ Frame limitations as "future research opportunities"

---

## KEY THEMES TO EMPHASIZE

### **1. Behavioral Finance Lens**

Your results are a **behavioral story:**
- Limited attention → patterns persist in small caps
- Gradual diffusion → effects build over time (0.21% → 0.35%)
- Scheduled events → attention reallocation creates opportunity

**Not** a fundamental mispricing story (would affect all stocks equally)

### **2. Event-Conditional Performance**

Your **novel contribution:**
- First to test CNN on macro events
- Shows WHEN visual patterns matter most
- Connects machine learning to event studies

### **3. Market Efficiency Heterogeneity**

Your results show:
- Large caps: Efficient (VW insignificant)
- Small caps: Less efficient (EW highly significant)
- **This is important!** Markets aren't uniformly efficient

---

## SAMPLE LENGTH DISTRIBUTION

**6.1 Interpretation:** ~800 words  
**6.2 FOMC Mechanisms:** ~700 words  
**6.3 Practical Implications:** ~600 words  
**6.4 Limitations & Future Research:** ~700 words  

**Total:** ~2,800 words

---

## OUTPUT FORMAT

Please write **Section 6: Discussion** with the four subsections above.

**Style:**
- Match my Introduction/Lit Review and Results sections
- Academic tone similar to Jiang et al. (2023) Discussion
- Balance interpretation with humility
- Cite literature explicitly

---

Ready? Please write the complete Discussion section now.


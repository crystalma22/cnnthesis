# Thesis-Ready Paragraphs for All Tables and Figures

**Purpose:** Copy-paste ready text for every table and figure in your thesis  
**Usage:** Insert these paragraphs where you reference each table/figure  
**Style:** Academic, finance-appropriate, uses "I" (single author)

---

## 📊 **SECTION 3: DATA**

### **Table 1: Sample Statistics**

**Where:** End of Section 3 (Data) or beginning of Section 4 (Methodology)

**Paragraph:**

> Table 1 summarizes the sample characteristics and model specifications. My analysis covers U.S. common stocks from 2001 to 2024, with CNN model training conducted on data from 1993 to 2000. The final dataset comprises approximately 8.9 million weekly stock-week observations across 22,480 unique stocks, with an average of 2,500 to 3,500 stocks per week. I employ an ensemble of five independently trained CNN models using a 20-day lookback window to predict 5-day forward returns, following the I20/R5 specification of Jiang et al. (2023).

**[INSERT TABLE 1: Sample Statistics]**

---

## 📊 **SECTION 4: METHODOLOGY**

### **Figure 6: CNN Architecture**

**Where:** Section 4.1 (CNN Model description)

**Paragraph:**

> Following Jiang et al. (2023), I employ a convolutional neural network to detect visual patterns in historical price charts. Figure 6 illustrates the CNN architecture. The model processes 20-day price sequences rendered as 32×32 pixel grayscale images, where each pixel's intensity represents normalized price levels relative to the starting price. The architecture consists of three convolutional layers with max-pooling operations that progressively extract visual features, followed by two fully connected layers that combine these features to output a probability score between 0 and 1. This score represents the predicted likelihood of a positive return over the subsequent five trading days. The convolutional structure allows the network to detect translation-invariant patterns—such as trends, reversals, and support levels—analogous to how a radiologist detects patterns in medical images.

**[INSERT FIGURE 6: CNN Architecture]**

---

### **Figure 9: Sample Price Charts**

**Where:** Section 4.1 (CNN Model), immediately after Figure 6

**Paragraph:**

> Figure 9 displays representative examples of the 20-day price chart images used as CNN input. Each 32×32 pixel grayscale image captures normalized price movements over 20 trading days, with all series starting at 1.0. The four panels illustrate different visual patterns the CNN encounters: uptrends (Panel A, 2013), downtrends (Panel B, 2008 financial crisis), high volatility (Panel C, 2020 pandemic), and sideways movements (Panel D, 2005). The CNN is trained to recognize which of these visual patterns—such as momentum trends, reversals, and consolidation phases—are associated with positive or negative subsequent returns, analogous to how technical analysts identify chart patterns but through automated pattern recognition rather than pre-specified rules.

**[INSERT FIGURE 9: Sample Price Charts]**

---

## 📊 **SECTION 5: RESULTS**

### **Section 5.1: Overall Portfolio Performance**

#### **Tables 3 & 4: Portfolio Performance**

**Paragraphs:**

> Table 3 reports equal-weighted portfolio performance across CNN prediction deciles for the out-of-sample period 2001 to 2024. Returns exhibit a strong monotonic pattern, increasing from -28.08% annually for the lowest-predicted decile to +42.66% for the highest-predicted decile. The high-minus-low spread of 70.74% with a Sharpe ratio of 5.60 confirms the findings of Jiang et al. (2023) that CNNs can detect visual price patterns with substantial predictive power. The monotonic relationship across all ten deciles—with no reversals or anomalies—suggests the CNN's probabilistic rankings are informative throughout the distribution, not merely at the extremes.

**[INSERT TABLE 3: Equal-Weight Portfolio Performance]**

> Table 4 presents value-weighted portfolio results, where stocks are weighted by market capitalization. While the decile pattern remains monotonic, ranging from -3.50% (low) to +19.19% (high), the high-minus-low spread is substantially smaller at 22.69% with a Sharpe ratio of 1.54. This represents roughly one-third the equal-weighted magnitude. The 3.1-fold difference between equal-weighted and value-weighted results provides initial evidence that CNN predictive power is concentrated in smaller-capitalization stocks, a pattern I explore in detail in Section 5.4. Nevertheless, even the value-weighted Sharpe ratio of 1.54 exceeds typical equity benchmarks, indicating the CNN signal contains information relevant across the market-capitalization spectrum, albeit with diminishing strength for larger firms.

**[INSERT TABLE 4: Value-Weight Portfolio Performance]**

---

#### **Figure 2: Decile Performance Comparison**

**Paragraph:**

> Figure 2 visualizes the portfolio performance patterns from Tables 3 and 4. Panel A compares annual returns across deciles: equal-weighted portfolios (blue bars) exhibit substantially larger spreads than value-weighted portfolios (orange bars), with the difference most pronounced in the extreme deciles. The monotonic increase from low to high deciles is clear for both weighting schemes, confirming the statistical pattern reported in the tables. Panel B presents Sharpe ratios, demonstrating that equal-weighted portfolios achieve superior risk-adjusted performance (Sharpe ranging from -1.55 to +2.23) compared to value-weighted (Sharpe ranging from -0.19 to +0.92). The consistent equal-weighted advantage in both raw returns and risk-adjusted metrics indicates the effect is not merely higher volatility but represents genuine predictive power concentrated in smaller stocks.

**[INSERT FIGURE 2: Decile Performance Comparison]**

---

#### **Table 7: Transaction Costs & Net Returns**

**Paragraph:**

> To address implementability concerns, Table 7 reports estimated net returns after transaction costs. With annual turnover of 654% for equal-weighted and 728% for value-weighted portfolios, I assume conservative round-trip transaction costs of 2%, reflecting bid-ask spreads, market impact, and commissions typical in small-cap trading. Under these assumptions, equal-weighted net returns decline from 70.74% to 57.66% annually (net Sharpe 4.56), while value-weighted net returns fall from 22.69% to 8.13% (net Sharpe 0.55). While transaction costs substantially reduce gross profitability, the net returns remain positive and economically meaningful, particularly for the equal-weighted strategy. These estimates likely represent lower bounds, as real-world implementation in illiquid small-cap stocks could face additional costs. Nevertheless, the analysis demonstrates that CNN predictive power persists even after accounting for realistic trading frictions.

**[INSERT TABLE 7: Transaction Costs & Net Returns]**

---

#### **Figure 7: Cumulative Returns Over Time**

**Paragraph:**

> Figure 7 displays cumulative high-minus-low portfolio returns from 2001 through 2024. Equal-weighted portfolios (blue line) generate consistent positive cumulative returns over the entire period, reaching approximately 2,000% by 2024. Value-weighted portfolios (orange line) show more modest but still positive cumulative gains of roughly 500%. Both strategies weather the 2008-2009 financial crisis (shaded region) and continue generating returns in subsequent years, demonstrating the CNN signal is not concentrated in a single favorable period but persists across varying market regimes. The steady upward trajectory of both lines, with equal-weighted consistently outpacing value-weighted, visually confirms the robustness and consistency of the patterns documented in Tables 3 and 4.

**[INSERT FIGURE 7: Cumulative Returns Over Time]**

---

#### **Figure 8: Prediction Distribution**

**Paragraph:**

> Figure 8 displays the distribution of CNN predicted probabilities across a typical week. The histogram reveals that most predictions cluster around 0.5 (neutral), with approximately symmetric tails extending toward 0 and 1. The vertical dashed lines mark decile cutoffs, dividing the distribution into ten groups. This distribution explains an apparent paradox in my results: while the average correlation between predictions and returns is modest (Spearman ρ ≈ 0.07), decile-sorted portfolios generate large return spreads. As the figure illustrates, predictive power is concentrated in the tails—extreme predictions (low and high deciles) contain strong signals, while middle predictions contain primarily noise. This tail-concentration is characteristic of machine learning classifiers: the model assigns high confidence (extreme probabilities) only when visual patterns are unambiguous, making confidence-sorted portfolios more informative than the average prediction.

**[INSERT FIGURE 8: Prediction Distribution]**

---

### **Section 5.2: Horizon Evaluation**

#### **Table 2: Horizon Evaluation**

**Paragraph:**

> Table 2 examines how CNN predictive power evolves across different forecast horizons. Equal-weighted high-minus-low spreads increase monotonically from 0.87% at the 1-day horizon to 1.37% at 10 days, representing a 58% improvement in predictive power. Value-weighted spreads also increase with horizon (0.09% to 0.24%) but remain substantially smaller, with equal-to-value-weight ratios ranging from 5.6× to 9.7×. This pattern is consistent with momentum and gradual information diffusion: visual price patterns take time to fully materialize in realized returns. The increasing horizon profile contradicts a mean-reversion interpretation—if the CNN merely captured transient noise, predictive power would decay with longer horizons. Instead, the strengthening signal over time suggests the CNN identifies persistent trends that unfold gradually, particularly in smaller stocks where information diffusion is slower.

**[INSERT TABLE 2: Horizon Evaluation]**

---

#### **Figure 3: Horizon Evaluation**

**Paragraph:**

> Figure 3 visualizes the horizon evaluation results from Table 2. Equal-weighted spreads (blue line) increase steadily from 0.87% at 1 day to 1.37% at 10 days, with values labeled at each horizon. Value-weighted spreads (orange line) also increase but remain substantially lower, visually confirming the persistent small-cap concentration documented throughout my results. The positive slopes of both lines demonstrate momentum characteristics: CNN-detected patterns strengthen rather than reverse over time. This contrasts sharply with mean-reversion patterns, which would produce downward-sloping lines. The visual divergence between the two lines reinforces that the CNN signal is most powerful in less-followed, smaller-capitalization stocks.

**[INSERT FIGURE 3: Horizon Evaluation]**

---

### **Section 5.3: FOMC Event Study Results** ⭐ **MAIN CONTRIBUTION**

#### **Figure 1: FOMC Timeline (No Overlap)**

**Paragraph:**

> To ensure clean temporal ordering, Figure 1 illustrates the typical timeline for an FOMC event. For a hypothetical June 15, 2020 announcement, I identify the most recent CNN prediction made on or before the announcement date—in this example, June 12, 2020. The CNN's 20-day lookback window (blue bar) extends from May 18 to June 12, ending before the announcement. I then measure returns starting from the announcement day (June 15) and forward across three windows: announcement day (green region), reaction (next day), and intermediate (weeks after). The gray shaded area between June 12 and June 15 represents the temporal gap ensuring no overlap between CNN inputs and measured returns. This backward-looking merge approach guarantees predictions strictly precede all measurements, eliminating potential look-ahead bias.

**[INSERT FIGURE 1: FOMC Timeline]**

---

#### **Table 5: FOMC Event Study Results** ⭐ **MOST IMPORTANT**

**Paragraph (DETAILED - This is your main contribution!):**

> Table 5 reports high-minus-low spreads around 217 Federal Reserve FOMC announcements from 2001 to 2024, representing my main empirical contribution. For each event, I identify the most recent CNN prediction made on or before the announcement date using a backward-looking merge, ensuring predictions strictly precede all measured returns (see Figure 1 for temporal ordering).
>
> Equal-weighted portfolios exhibit a statistically significant spread of 0.21% on announcement days (t=2.95, p=0.004), indicating the CNN's pre-announcement signals successfully identify stocks that react more favorably to monetary policy news. With approximately eight FOMC meetings per year, this translates to an annualized contribution of roughly 1.7%. The effect persists into the subsequent trading day with a marginally significant 0.10% spread (t=1.76, p=0.079), suggesting partial under-reaction that continues overnight. Most notably, the intermediate window (days t+5 to t+20) shows the largest and most statistically significant spread of 0.35% (t=2.24, p=0.026), consistent with gradual information diffusion over the two-to-four weeks following announcements.
>
> In sharp contrast, value-weighted portfolios exhibit small and statistically insignificant spreads across all windows: 0.05% on announcement day (t=0.66), 0.03% on reaction day, and -0.28% in the intermediate window (suggesting reversal in large caps). The systematic pattern of significant equal-weighted effects paired with insignificant value-weighted effects indicates the CNN captures behavioral patterns concentrated in smaller-capitalization stocks where attention and arbitrage constraints are most binding. This heterogeneity by firm size strengthens the behavioral interpretation: visual price patterns remain exploitable where institutional monitoring is limited, but are arbitraged away in efficiently-priced large-cap markets.

**[INSERT TABLE 5: FOMC Event Study Results]**

---

#### **Figure 4: FOMC Results Bar Chart**

**Paragraph:**

> Figure 4 visualizes the FOMC event study results from Table 5. Equal-weighted portfolios (blue bars) show positive spreads across all three windows, with significance stars marking statistical confidence levels. The intermediate window (0.35%, two stars) exhibits the largest effect, visually confirming that CNN patterns strengthen over the weeks following FOMC announcements. Value-weighted portfolios (orange bars) show substantially smaller spreads, with the intermediate window actually reversing to -0.28%. The stark visual contrast between blue and orange bars across all windows provides graphical evidence for the behavioral mechanism: CNN predictive power is concentrated in small caps (blue bars with stars) and largely absent in large caps (orange bars without stars). The pattern of increasing equal-weighted spreads from announcement (0.21%) to intermediate (0.35%) is consistent with gradual information diffusion, particularly in less-followed stocks.

**[INSERT FIGURE 4: FOMC Results Bar Chart]**

---

### **Section 5.4: Small-Cap Concentration**

#### **Table 6: EW vs VW Comparison**

**Paragraph:**

> Table 6 synthesizes the equal-weight versus value-weight comparison across all tests, revealing a strikingly consistent pattern. Equal-weighted high-minus-low spreads exceed value-weighted by factors ranging from 3.1× (overall annual portfolio) to 9.7× (1-day horizon). Across portfolio performance, horizon evaluation, and FOMC event windows, the equal-weighted advantage persists without exception. This is not an artifact of a single test or favorable period but a systematic feature of CNN predictive power. The consistency of this relationship across every dimension of my analysis points to a unified behavioral mechanism: CNN-detected visual patterns are most exploitable in less-followed, smaller-capitalization stocks where limited investor attention allows patterns to persist. In large-cap markets, institutional investors monitor price movements continuously and arbitrage away predictable signals, reducing or eliminating exploitable spreads.

**[INSERT TABLE 6: EW vs VW Comparison]**

---

#### **Figure 5: EW vs VW Comparison (Two Panels)**

**Paragraph:**

> Figure 5 provides a comprehensive visual summary of the small-cap concentration finding. Panel A displays the overall portfolio high-minus-low spread: equal-weighted portfolios generate 70.74% annually compared to 22.69% for value-weighted (3.1× ratio). Panel B demonstrates this pattern extends to all shorter-horizon and event-window tests, with equal-to-value-weight ratios ranging from 3.3× to 9.7× (green labels above bars). The visual consistency across both panels—equal-weighted bars (blue) consistently tower over value-weighted bars (orange)—illustrates that small-cap concentration is not confined to a single test but characterizes every aspect of CNN performance. The systematic nature of this pattern, visible across seven independent comparisons spanning different methodologies and time horizons, provides strong evidence for a behavioral mechanism operating consistently throughout the sample period.

**[INSERT FIGURE 5: EW vs VW Comparison]**

---

## 📊 **ADDITIONAL CONTEXT PARAGRAPHS** (Use as needed)

### **For Section 5.1: After Tables 3 & 4, Before Transaction Costs**

**Connecting paragraph:**

> The substantial difference between equal-weighted and value-weighted results warrants further investigation. To assess whether these gross return differentials survive realistic trading costs, I examine turnover and estimate net performance after transaction frictions.

---

### **For Section 5.3: Before Table 5 (FOMC Introduction)**

**Introductory paragraph:**

> Having established that CNN predictions generate substantial out-of-sample returns concentrated in small-cap stocks, I now examine my main contribution: whether these patterns are particularly pronounced around scheduled Federal Reserve FOMC announcements. I analyze 217 FOMC meetings from January 2001 through December 2024 (Table 5 reports 216-217 events depending on data availability for each window). For each announcement, I identify the most recent CNN prediction made on or before the announcement date, ensuring temporal precedence.

---

### **For Section 5.2: Horizon Introduction**

**Introductory paragraph:**

> To understand how CNN predictive power evolves over different forecast horizons, I compute high-minus-low spreads at 1-day, 3-day, and 10-day intervals. This horizon evaluation tests whether the CNN captures momentum (predictive power increasing with horizon) or mean reversion (predictive power decreasing with horizon).

---

### **For Section 5.4: Small-Cap Synthesis Introduction**

**Introductory paragraph:**

> A consistent theme emerges across all analyses: equal-weighted portfolios exhibit substantially larger spreads than value-weighted portfolios. To synthesize this finding and assess its consistency, I compare the equal-to-value-weight ratio across all tests—overall performance, horizon evaluation, and FOMC event windows.

---

## 📝 **SPECIAL PARAGRAPH: COPY-PASTE FOR FOMC (From Enhanced Analysis)**

**Alternative FOMC paragraph (more detailed, includes all stats):**

> Table 5 reports high-minus-low spreads around 217 Federal Reserve FOMC announcements from 2001 to 2024. Equal-weighted portfolios exhibit a statistically significant spread of 0.21% on announcement days (t=2.95, p=0.004, 95% CI [0.07%, 0.35%]), suggesting the CNN's pre-announcement signals identify stocks that react more favorably to monetary policy news. The effect persists into the subsequent trading day with a marginally significant 0.10% spread (t=1.76, p=0.079, N=215) and strengthens over the intermediate two-to-four week window (0.35%, t=2.24, p=0.026, N=208), consistent with gradual information diffusion described by Hong and Stein (1999). The strengthening time profile—from 0.21% immediate to 0.35% delayed—indicates markets do not instantly incorporate all cross-sectional implications of FOMC announcements, particularly in smaller stocks where investor attention is limited.
>
> In contrast, value-weighted spreads are small and statistically insignificant across all windows (0.05% on announcement day with t=0.66, p=0.51), indicating the effect is concentrated in smaller-capitalization stocks where attention and arbitrage constraints are more binding. The intermediate-window reversal in value-weighted portfolios (-0.28%, t=-1.57) may reflect profit-taking in large caps following initial reactions. These results are consistent with a behavioral mechanism: the CNN captures visual price patterns that remain exploitable in less-followed stocks, especially when macro information is being incorporated into prices over an extended period.

**[INSERT TABLE 5: FOMC Event Study Results]**

---

## 🎯 **USAGE INSTRUCTIONS:**

### **How to Use These Paragraphs:**

1. **Copy the paragraph(s)** for each table/figure
2. **Paste into your thesis** at the appropriate location
3. **Edit as needed** to match your writing style
4. **Insert the actual table/figure** where marked with [INSERT...]
5. **Adjust transitions** between paragraphs

### **Customization Tips:**

- **Make shorter:** Delete middle sentences for brevity
- **Make longer:** Add more interpretation from COMPLETE_STATISTICAL_RESULTS_EXPLAINED.md
- **Change emphasis:** Reorder sentences to highlight different points
- **Match style:** Adjust to match ChatGPT's writing style for your other sections

### **All paragraphs:**
- ✅ Use first-person singular ("I")
- ✅ Include specific numbers
- ✅ Report statistics (t-stats, p-values when relevant)
- ✅ Interpret findings
- ✅ Connect to thesis narrative
- ✅ Academic tone
- ✅ Finance-appropriate language

---

## 📋 **CHECKLIST: Make Sure You:**

For each table/figure:
- [ ] Have introductory text BEFORE the table/figure
- [ ] Insert the actual table/figure
- [ ] Have interpretation text AFTER (can be same paragraph or next)
- [ ] Reference by number in text ("Table 5 reports...", "As shown in Figure 4...")
- [ ] Include caption with the table/figure

---

## ✅ **YOU NOW HAVE:**

**Thesis-ready paragraphs for:**
- ✅ Table 1 (Sample Statistics)
- ✅ Tables 3 & 4 (Portfolio Performance)
- ✅ Table 5 (FOMC Results - with detailed version!)
- ✅ Table 6 (EW vs VW Comparison)
- ✅ Table 7 (Transaction Costs)
- ✅ Figure 2 (Decile Performance)
- ✅ Figure 3 (Horizon Evaluation)
- ✅ Figure 4 (FOMC Results)
- ✅ Figure 5 (EW vs VW)
- ✅ Figure 6 (CNN Architecture)
- ✅ Figure 7 (Cumulative Returns)
- ✅ Figure 8 (Distribution)
- ✅ Figure 9 (Sample Charts)

**Plus transition/intro paragraphs for each subsection!**

**All ready to copy-paste into your thesis!** 📝


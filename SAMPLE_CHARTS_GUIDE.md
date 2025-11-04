# Using Sample Price Chart Images in Your Thesis

**You now have:** Figure 9 - Sample Price Charts (4 examples)

**Location:** `~/Desktop/Thesis_Results/thesis_output/figures/figure9_sample_price_charts.png`

---

## 📊 **WHAT THE FIGURE SHOWS:**

**4 example 20-day price chart images:**

1. **Uptrend Pattern (2013)**
   - Shows steady upward movement
   - Example of "bullish" signal CNN would recognize

2. **Downtrend Pattern (2008 Financial Crisis)**
   - Shows declining prices
   - Example of "bearish" signal CNN would recognize

3. **High Volatility (2020 COVID)**
   - Shows erratic price movements
   - Example of uncertain/volatile pattern

4. **Sideways Pattern (2005)**
   - Shows range-bound trading
   - Example of neutral signal

**Each image:** 32×32 pixels, grayscale, normalized to start at 1.0

---

## 📝 **WHERE TO USE THIS IN YOUR THESIS:**

### **BEST PLACE: Methodology Section (Section 4.1 - CNN Model)**

**Insert after describing the CNN architecture, before portfolio construction.**

**Suggested text:**

> "Figure 9 displays representative examples of the 20-day price chart images used as CNN input. Each 32×32 pixel grayscale image captures normalized price movements over 20 trading days, resembling candlestick charts familiar to technical analysts. Panel A shows an uptrend pattern (2013), Panel B a downtrend during the 2008 financial crisis, Panel C high volatility during the 2020 COVID pandemic, and Panel D a sideways pattern (2005). The CNN learns to recognize which visual patterns—such as momentum trends, reversals, and support/resistance levels—are associated with subsequent returns."

---

## 🎨 **CAPTION (For Your Thesis):**

**Full caption:**
> "Figure 9: Examples of 20-Day Price Chart Images Used as CNN Input. Each 32×32 pixel grayscale image represents normalized price movements over 20 trading days, with price levels normalized to 1.0 at the start of the window. Panel A shows an uptrend pattern, Panel B a downtrend, Panel C high volatility, and Panel D a sideways/range-bound pattern. The CNN is trained to detect visual patterns in these images that predict 5-day forward returns."

---

## 💡 **WHY THIS FIGURE IS VALUABLE:**

### **Helps Readers Understand:**
1. **What is the CNN actually seeing?** → Literal price charts!
2. **Why call it "image-based"?** → Visual proof
3. **What patterns does it detect?** → Trends, volatility, ranges
4. **Why might this work?** → Looks like what technical analysts study

### **Addresses Common Questions:**
- **Q:** "What does a 20-day lookback window look like?"
  - **A:** See Figure 9 - actual examples

- **Q:** "How is this different from traditional analysis?"
  - **A:** Figure 9 shows it's similar to candlestick charts humans use

- **Q:** "What kind of patterns does CNN find?"
  - **A:** Figure 9 shows uptrends, downtrends, volatility, sideways

---

## 📋 **HOW TO INSERT IN YOUR THESIS:**

### **For Microsoft Word:**
1. Insert the PNG file at the appropriate spot in Methodology
2. Add caption below
3. Reference in text: "As shown in Figure 9..."

### **For LaTeX:**
```latex
As shown in Figure~\ref{fig:sample_charts}, each CNN input is a 32×32 
pixel grayscale image...

\begin{figure}[h]
  \centering
  \includegraphics[width=0.85\textwidth]{figures/figure9_sample_price_charts.pdf}
  \caption{Examples of 20-Day Price Chart Images Used as CNN Input. 
  Each 32×32 pixel grayscale image represents normalized price movements 
  over 20 trading days. Panel A shows an uptrend, Panel B a downtrend, 
  Panel C high volatility, and Panel D a sideways pattern.}
  \label{fig:sample_charts}
\end{figure}
```

---

## 🎯 **UPDATED FIGURE COUNT:**

**You now have 9 figures total:**

1. FOMC Timeline (No Overlap)
2. Decile Performance
3. Horizon Evaluation
4. FOMC Results ⭐ MAIN
5. EW vs VW Comparison
6. CNN Architecture (diagram)
7. Cumulative Returns
8. Prediction Distribution
9. **Sample Price Charts** ⭐ **NEW - Shows actual CNN input**

---

## 📚 **WHERE EACH FIGURE GOES:**

**In Methodology:**
- Figure 6: CNN Architecture (how it works)
- **Figure 9: Sample Charts** (what it sees) ⭐ **NEW**

**In Results:**
- Figure 1: FOMC Timeline
- Figure 2: Decile Performance
- Figure 3: Horizon Evaluation
- Figure 4: FOMC Results
- Figure 5: EW vs VW Comparison
- Figure 7: Cumulative Returns
- Figure 8: Prediction Distribution

---

## 💡 **PRO TIP:**

**Place Figure 9 right after you explain the CNN architecture (Figure 6).**

**Flow:**
1. Describe CNN architecture (text + Figure 6 diagram)
2. **Show what CNN sees (Figure 9 - actual images)** ⭐
3. Explain training process
4. Move to portfolio construction

**This creates a natural visual progression:**
- Architecture (how) → Input (what) → Process (training) → Output (portfolios)

---

## ✅ **FIGURE 9 IS READY!**

**Location:** `~/Desktop/Thesis_Results/thesis_output/figures/figure9_sample_price_charts.png`

**Use:** In Methodology section (Section 4.1) after CNN architecture

**Caption:** Pre-written above

**This makes your CNN explanation much more concrete and visual!** 🎨


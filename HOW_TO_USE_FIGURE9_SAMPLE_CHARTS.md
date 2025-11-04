# How to Use Figure 9 (Sample Charts) in Your Thesis

**Quick Answer:**
- **Where:** Methodology section (4.1 - CNN Model description)
- **When:** Right after explaining CNN architecture (after Figure 6)
- **Describe signals:** Keep it SIMPLE - just mention trends/patterns, don't get technical

---

## 📍 **EXACT PLACEMENT IN YOUR THESIS:**

### **Section 4: Methodology**

**Subsection 4.1: CNN Model (Replication of Jiang et al. 2023)**

**Flow:**
1. **Describe CNN architecture** (what the model is)
   - 3 convolutional layers
   - Input: 32×32 images
   - Output: Up-probability
   - **Reference Figure 6** (architecture diagram)

2. **Show what CNN input looks like** ⭐ **INSERT FIGURE 9 HERE**
   - "Figure 9 displays examples..."
   - Brief description of the 4 patterns
   - What CNN learns from these

3. **Explain training process**
   - Trained 1993-2000
   - Ensemble of 5 models
   - Out-of-sample 2001-2024

4. **Move to next subsection** (4.2 Portfolio Construction)

---

## 📝 **HOW TO DESCRIBE IT (Keep Simple!):**

### **RECOMMENDED (Simple, Finance-Friendly):**

> "Figure 9 displays representative examples of the 20-day price chart images used as CNN input. Each 32×32 pixel grayscale image captures normalized price movements over 20 trading days, resembling the candlestick charts used by technical analysts. The four panels illustrate different visual patterns the CNN encounters: uptrends (Panel A), downtrends (Panel B), high volatility (Panel C), and sideways/range-bound movements (Panel D). The CNN is trained to recognize which of these visual patterns—such as momentum trends, reversals, and consolidation phases—are associated with positive or negative subsequent returns."

**Length:** ~100 words  
**Level:** Perfect for finance audience  
**Technical detail:** Just right (not too deep, not too shallow)

---

## ❌ **DON'T DO THIS (Too Technical):**

**Don't describe technical signals in detail:**

❌ "Panel A shows a rising trend with higher highs and higher lows, breaking through resistance at the 50-day moving average. The MACD indicator would show bullish divergence here, and the RSI suggests momentum..."

**Why not:**
- Too technical for your thesis
- Your CNN doesn't use these indicators (it learns patterns directly)
- Not your contribution (you're replicating, not explaining technical analysis)
- Distracts from your behavioral story

---

## ✅ **DO THIS (Just Right):**

**Keep it general:**

✅ "Uptrends, downtrends, and volatility patterns"  
✅ "Momentum trends and reversals"  
✅ "Visual patterns similar to those technical analysts study"  
✅ "Support and resistance levels" (if you mention briefly)

**Why this works:**
- Finance audience understands these concepts
- Not too technical (no MACD, RSI, Bollinger Bands)
- Connects to familiar ideas (technical analysis)
- Focuses on the KEY POINT: CNN learns from visual patterns

---

## 💡 **SUGGESTED PARAGRAPH (Copy-Paste Ready):**

**Option 1: Minimal Technical Detail (Recommended):**

> "Figure 9 displays representative examples of the 20-day price chart images used as CNN input. Each image is a 32×32 pixel grayscale representation of normalized price movements, where darker pixels indicate lower prices and lighter pixels higher prices. The four panels illustrate different market conditions the CNN encounters: an upward trend (Panel A, 2013), a downward trend during the 2008 financial crisis (Panel B), high volatility during the 2020 pandemic (Panel C), and a range-bound pattern (Panel D, 2005). Through supervised learning on historical data, the CNN identifies which visual patterns are associated with subsequent price increases or decreases, analogous to how technical analysts recognize chart patterns but in an automated, data-driven manner."

**Length:** 120 words  
**Technical level:** Light (just trends, no indicators)

---

**Option 2: Slightly More Detail (If You Want):**

> "Figure 9 displays representative examples of the 20-day price chart images. Each 32×32 pixel grayscale image represents normalized price movements over 20 trading days, with all series starting at 1.0. Panel A shows an upward momentum pattern where the CNN would learn to assign high up-probability. Panel B displays a downtrend from the 2008 financial crisis, a pattern associated with low up-probability. Panel C illustrates the high volatility characteristic of the 2020 pandemic period. Panel D shows a sideways, range-bound pattern with no clear directional trend. The CNN learns to distinguish these visual patterns and associate them with forward returns, capturing information that technical analysts might recognize as trends, reversals, and consolidation phases."

**Length:** 130 words  
**Technical level:** Medium (mentions momentum, consolidation, trends)

---

**Option 3: Most General (Safest):**

> "Figure 9 shows four examples of the 20-day price chart images used as CNN input. These 32×32 pixel grayscale images capture how stock prices move over 20 trading days, normalized to start at 1.0. The CNN is trained to recognize visual patterns in these charts—such as rising trends, falling trends, or volatile movements—that predict whether prices will increase over the next 5 days. This image-based approach allows the CNN to detect patterns similar to those used in technical analysis, but learned directly from data rather than pre-specified rules."

**Length:** 90 words  
**Technical level:** Minimal (perfect for general audience)

---

## 🎯 **MY RECOMMENDATION:**

**Use Option 3 (Most General)** - Here's why:

### **Your thesis is about:**
1. ✅ CNN predictions work (replication)
2. ✅ They work better on FOMC days (your contribution)
3. ✅ Small-cap concentration (behavioral)

### **Your thesis is NOT about:**
- ❌ Which specific technical patterns work best
- ❌ How technical analysis indicators work
- ❌ Deep dive into pattern recognition

### **So keep Figure 9 description simple:**
- Shows what 20-day lookback looks like ✅
- Shows different market conditions ✅
- Mentions trends as examples ✅
- Doesn't go deep into technical signals ✅

**This keeps focus on YOUR contributions (FOMC events + behavioral), not on technical analysis minutiae!**

---

## 📋 **FINAL PLACEMENT GUIDE:**

### **Your Methodology Section 4.1 should flow:**

**Paragraph 1:** Introduce CNN approach (replicating Jiang et al.)

**Paragraph 2:** Describe architecture
- 3 convolutional layers → pooling → fully connected → sigmoid
- **Reference Figure 6** (architecture diagram)

**Paragraph 3:** Show what CNN input looks like ⭐ **INSERT FIGURE 9 HERE**
- "Figure 9 shows four examples..."
- Use Option 3 (simple description)
- Emphasize it's like technical analysis charts

**Paragraph 4:** Explain training
- 1993-2000 training period
- Ensemble of 5 models
- Out-of-sample 2001-2024

**Then move to 4.2:** Portfolio Construction

---

## ✅ **BOTTOM LINE:**

**Figure 9:** ✅ Great addition!  
**Where:** Methodology 4.1 (after architecture, before training)  
**Description:** Keep simple (Option 3 recommended)  
**Technical signals:** DON'T describe in detail (just say "trends and patterns")  

**This makes your CNN explanation much clearer without getting lost in technical details!** 📊

**Ready to push to GitHub?**
```bash
git push origin replication-edited
```

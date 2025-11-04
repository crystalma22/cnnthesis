# Table and Figure Placement Guide

**Purpose:** Shows exactly where each table/figure goes in your thesis sections  
**Use this:** When writing your thesis to place tables/figures correctly

---

## 📋 **SUMMARY: Not All Go in Results!**

- **Data Section (Section 3):** 1 table
- **Methodology Section (Section 4):** 3 figures
- **Results Section (Section 5):** 6 tables + 6 figures

**Total:** 7 tables + 9 figures = 16 items

---

## 📊 **SECTION 3: DATA**

### **Table 1: Sample Statistics**
**Location:** End of Section 3 (Data) or beginning of Section 4 (Methodology)  
**Purpose:** Describes dataset, sample size, model specification  
**When to use:** After describing data sources, before methodology details

```
Section 3: Data
├─ Data sources description
├─ Sample period and coverage
├─ [INSERT TABLE 1: Sample Statistics] ← HERE
└─ Transition to Methodology
```

---

## 📊 **SECTION 4: METHODOLOGY**

### **Figure 6: CNN Architecture**
**Location:** Section 4.1 (CNN Model description)  
**Purpose:** Shows the neural network structure  
**When to use:** When explaining how the CNN works

```
Section 4: Methodology
├─ 4.1 CNN Model
│  ├─ Overview of CNN approach
│  ├─ [INSERT FIGURE 6: CNN Architecture] ← HERE
│  └─ Explanation of layers
```

---

### **Figure 9: Sample Price Charts**
**Location:** Section 4.1 (CNN Model), immediately after Figure 6  
**Purpose:** Shows example input images to the CNN  
**When to use:** After explaining architecture, to show what the CNN "sees"

```
Section 4: Methodology
├─ 4.1 CNN Model
│  ├─ [INSERT FIGURE 6: CNN Architecture]
│  ├─ [INSERT FIGURE 9: Sample Price Charts] ← HERE
│  └─ Explanation of image preprocessing
```

---

### **Figure 1: FOMC Timeline**
**Location:** Section 4.2 (FOMC Event Study Methodology) or Section 4.3 (Event Window Definitions)  
**Purpose:** Explains temporal ordering to prevent look-ahead bias  
**When to use:** When describing how FOMC windows are constructed

```
Section 4: Methodology
├─ 4.2 FOMC Event Study Design
│  ├─ Event window definitions
│  ├─ Temporal alignment explanation
│  ├─ [INSERT FIGURE 1: FOMC Timeline] ← HERE
│  └─ Backward-looking merge methodology
```

---

## 📊 **SECTION 5: RESULTS**

### **Section 5.1: Overall Portfolio Performance**

#### **Table 3: Equal-Weight Portfolio Performance**
**Location:** Section 5.1, first results table  
**Purpose:** Shows decile performance with equal weighting  
**When to use:** Right after introducing portfolio formation methodology

```
Section 5: Results
├─ 5.1 Overall Portfolio Performance
│  ├─ Portfolio formation methodology
│  ├─ [INSERT TABLE 3: Equal-Weight Performance] ← HERE
│  └─ Interpretation of EW results
```

---

#### **Table 4: Value-Weight Portfolio Performance**
**Location:** Section 5.1, immediately after Table 3  
**Purpose:** Shows decile performance with value weighting  
**When to use:** After Table 3, to contrast with equal-weight

```
Section 5: Results
├─ 5.1 Overall Portfolio Performance
│  ├─ [INSERT TABLE 3: Equal-Weight Performance]
│  ├─ [INSERT TABLE 4: Value-Weight Performance] ← HERE
│  └─ EW vs VW comparison discussion
```

---

#### **Figure 2: Decile Performance Comparison**
**Location:** Section 5.1, after Tables 3 & 4  
**Purpose:** Visualizes the decile patterns from both tables  
**When to use:** After presenting both tables, to summarize visually

```
Section 5: Results
├─ 5.1 Overall Portfolio Performance
│  ├─ [INSERT TABLE 3: Equal-Weight Performance]
│  ├─ [INSERT TABLE 4: Value-Weight Performance]
│  ├─ [INSERT FIGURE 2: Decile Comparison] ← HERE
│  └─ Interpretation of patterns
```

---

#### **Table 7: Transaction Costs & Net Returns**
**Location:** Section 5.1, after discussing gross returns  
**Purpose:** Shows implementability after trading costs  
**When to use:** After showing gross returns, to address practical concerns

```
Section 5: Results
├─ 5.1 Overall Portfolio Performance
│  ├─ Gross returns discussion
│  ├─ Transaction cost considerations
│  ├─ [INSERT TABLE 7: Transaction Costs] ← HERE
│  └─ Net returns interpretation
```

---

#### **Figure 7: Cumulative Returns Over Time**
**Location:** Section 5.1, after Table 7 or at end of subsection  
**Purpose:** Shows time series of portfolio performance  
**When to use:** To demonstrate robustness over time, after transaction costs

```
Section 5: Results
├─ 5.1 Overall Portfolio Performance
│  ├─ [INSERT TABLE 7: Transaction Costs]
│  ├─ [INSERT FIGURE 7: Cumulative Returns] ← HERE
│  └─ Time series robustness discussion
```

---

#### **Figure 8: Prediction Distribution**
**Location:** Section 5.1, after portfolio results or in methodology subsection  
**Purpose:** Shows distribution of CNN predictions  
**When to use:** To explain why decile sorting works despite modest average correlation

```
Section 5: Results
├─ 5.1 Overall Portfolio Performance
│  ├─ Portfolio results
│  ├─ [INSERT FIGURE 8: Prediction Distribution] ← HERE
│  └─ Discussion of tail concentration
```

---

### **Section 5.2: Horizon Evaluation**

#### **Table 2: Horizon Evaluation**
**Location:** Section 5.2, first table in subsection  
**Purpose:** Shows how predictive power varies with forecast horizon  
**When to use:** Right after introducing horizon evaluation methodology

```
Section 5: Results
├─ 5.2 Horizon Evaluation
│  ├─ Methodology for horizon tests
│  ├─ [INSERT TABLE 2: Horizon Evaluation] ← HERE
│  └─ Interpretation of horizon patterns
```

---

#### **Figure 3: Horizon Evaluation**
**Location:** Section 5.2, after Table 2  
**Purpose:** Visualizes the horizon results from Table 2  
**When to use:** After Table 2, to show the trend visually

```
Section 5: Results
├─ 5.2 Horizon Evaluation
│  ├─ [INSERT TABLE 2: Horizon Evaluation]
│  ├─ [INSERT FIGURE 3: Horizon Visualization] ← HERE
│  └─ Momentum vs mean-reversion discussion
```

---

### **Section 5.3: FOMC Event Study Results** ⭐ **MAIN CONTRIBUTION**

#### **Table 5: FOMC Event Study Results** ⭐ **MOST IMPORTANT**
**Location:** Section 5.3, first table in subsection  
**Purpose:** Shows your main contribution - FOMC event effects  
**When to use:** Right after introducing FOMC methodology, this is your KEY RESULT

```
Section 5: Results
├─ 5.3 FOMC Event Study Results
│  ├─ FOMC methodology recap
│  ├─ [INSERT TABLE 5: FOMC Results] ← HERE (YOUR MAIN CONTRIBUTION!)
│  └─ Detailed interpretation
```

---

#### **Figure 4: FOMC Results Bar Chart**
**Location:** Section 5.3, immediately after Table 5  
**Purpose:** Visualizes FOMC results from Table 5  
**When to use:** After Table 5, to show the pattern graphically

```
Section 5: Results
├─ 5.3 FOMC Event Study Results
│  ├─ [INSERT TABLE 5: FOMC Results]
│  ├─ [INSERT FIGURE 4: FOMC Bar Chart] ← HERE
│  └─ Behavioral interpretation
```

---

### **Section 5.4: Small-Cap Concentration (EW vs VW Synthesis)**

#### **Table 6: EW vs VW Comparison**
**Location:** Section 5.4, synthesis table  
**Purpose:** Compares equal-weight vs value-weight across all tests  
**When to use:** To synthesize the small-cap finding across all analyses

```
Section 5: Results
├─ 5.4 Small-Cap Concentration
│  ├─ Introduction to EW vs VW pattern
│  ├─ [INSERT TABLE 6: EW vs VW Comparison] ← HERE
│  └─ Behavioral mechanism discussion
```

---

#### **Figure 5: EW vs VW Comparison (Two Panels)**
**Location:** Section 5.4, after Table 6  
**Purpose:** Visualizes the EW vs VW comparison  
**When to use:** After Table 6, to show the pattern across all tests

```
Section 5: Results
├─ 5.4 Small-Cap Concentration
│  ├─ [INSERT TABLE 6: EW vs VW Comparison]
│  ├─ [INSERT FIGURE 5: EW vs VW Visualization] ← HERE
│  └─ Conclusion of small-cap finding
```

---

## 📋 **COMPLETE SECTION BREAKDOWN**

### **Section 3: Data**
```
✅ Table 1: Sample Statistics
```

### **Section 4: Methodology**
```
✅ Figure 6: CNN Architecture
✅ Figure 9: Sample Price Charts
✅ Figure 1: FOMC Timeline
```

### **Section 5: Results**

#### **Subsection 5.1: Overall Portfolio Performance**
```
✅ Table 3: Equal-Weight Portfolio Performance
✅ Table 4: Value-Weight Portfolio Performance
✅ Figure 2: Decile Performance Comparison
✅ Table 7: Transaction Costs & Net Returns
✅ Figure 7: Cumulative Returns Over Time
✅ Figure 8: Prediction Distribution
```

#### **Subsection 5.2: Horizon Evaluation**
```
✅ Table 2: Horizon Evaluation
✅ Figure 3: Horizon Evaluation
```

#### **Subsection 5.3: FOMC Event Study Results** ⭐
```
✅ Table 5: FOMC Event Study Results ⭐ MAIN CONTRIBUTION
✅ Figure 4: FOMC Results Bar Chart
```

#### **Subsection 5.4: Small-Cap Concentration**
```
✅ Table 6: EW vs VW Comparison
✅ Figure 5: EW vs VW Comparison
```

---

## 🎯 **QUICK REFERENCE: Which Section?**

| Item | Section | Subsection |
|------|---------|------------|
| Table 1 | Data (3) | - |
| Figure 6 | Methodology (4) | 4.1 CNN Model |
| Figure 9 | Methodology (4) | 4.1 CNN Model |
| Figure 1 | Methodology (4) | 4.2 FOMC Design |
| Table 3 | Results (5) | 5.1 Portfolio Performance |
| Table 4 | Results (5) | 5.1 Portfolio Performance |
| Figure 2 | Results (5) | 5.1 Portfolio Performance |
| Table 7 | Results (5) | 5.1 Portfolio Performance |
| Figure 7 | Results (5) | 5.1 Portfolio Performance |
| Figure 8 | Results (5) | 5.1 Portfolio Performance |
| Table 2 | Results (5) | 5.2 Horizon Evaluation |
| Figure 3 | Results (5) | 5.2 Horizon Evaluation |
| **Table 5** ⭐ | **Results (5)** | **5.3 FOMC Event Study** |
| **Figure 4** ⭐ | **Results (5)** | **5.3 FOMC Event Study** |
| Table 6 | Results (5) | 5.4 Small-Cap Concentration |
| Figure 5 | Results (5) | 5.4 Small-Cap Concentration |

---

## 📝 **TYPICAL THESIS STRUCTURE:**

```
Chapter 1: Introduction
Chapter 2: Literature Review
Chapter 3: Data
    └─ Table 1
Chapter 4: Methodology
    ├─ 4.1 CNN Model
    │   ├─ Figure 6
    │   └─ Figure 9
    └─ 4.2 FOMC Event Study
        └─ Figure 1
Chapter 5: Results
    ├─ 5.1 Overall Portfolio Performance
    │   ├─ Table 3
    │   ├─ Table 4
    │   ├─ Figure 2
    │   ├─ Table 7
    │   ├─ Figure 7
    │   └─ Figure 8
    ├─ 5.2 Horizon Evaluation
    │   ├─ Table 2
    │   └─ Figure 3
    ├─ 5.3 FOMC Event Study ⭐
    │   ├─ Table 5 ⭐
    │   └─ Figure 4
    └─ 5.4 Small-Cap Concentration
        ├─ Table 6
        └─ Figure 5
Chapter 6: Discussion
Chapter 7: Conclusion
```

---

## ✅ **KEY TAKEAWAYS:**

1. **Not all go in Results!**
   - 1 table in Data
   - 3 figures in Methodology
   - 12 items in Results

2. **Methodology figures explain HOW:**
   - Figure 6: How CNN works (architecture)
   - Figure 9: What CNN sees (sample inputs)
   - Figure 1: How FOMC windows work (temporal ordering)

3. **Results tables/figures show WHAT you found:**
   - Portfolio performance (Tables 3, 4, 7; Figures 2, 7, 8)
   - Horizon patterns (Table 2; Figure 3)
   - FOMC effects (Table 5 ⭐; Figure 4)
   - Small-cap concentration (Table 6; Figure 5)

4. **Table 5 is your MAIN CONTRIBUTION:**
   - Goes in Results Section 5.3
   - This is what makes your thesis unique
   - Spend most time interpreting this!

---

## 🎯 **WHEN WRITING YOUR THESIS:**

**For each table/figure:**
1. Check this guide for section placement
2. Read the paragraph from `THESIS_READY_PARAGRAPHS_ALL_FIGURES_TABLES.md`
3. Insert the table/figure at the right location
4. Use the paragraph text (or adapt it)
5. Reference by number in your text ("Table 5 reports...", "As shown in Figure 4...")

---

**You're all set! This guide shows exactly where everything goes.** 📊


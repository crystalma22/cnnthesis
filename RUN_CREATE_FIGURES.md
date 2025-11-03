# How to Generate All Thesis Tables and Figures

**Script:** `create_thesis_tables_and_figures.py`  
**Generates:** 6 tables (LaTeX + CSV) + 6 figures (PNG + PDF)  
**Font:** Times New Roman (matches your thesis)

---

## 🚀 **OPTION 1: Run on Your Mac (Recommended)**

### Step 1: Install Required Packages
```bash
pip3 install pandas matplotlib seaborn
```

### Step 2: Run the Script
```bash
cd "/Users/crystallion22/Desktop/Thesis Materials/cnnthesis"
python3 create_thesis_tables_and_figures.py
```

### Step 3: Check Output
All files will be in `thesis_output/`:
- `tables/` - LaTeX and CSV files
- `figures/` - PNG and PDF files

---

## 🖥️ **OPTION 2: Run on Laguna (If Mac doesn't work)**

### Step 1: Copy Script to Laguna
```bash
scp create_thesis_tables_and_figures.py laguna:~/cnnthesis/
```

### Step 2: SSH and Run
```bash
ssh laguna
cd ~/cnnthesis
~/cnnthesis/cnn_env/bin/python create_thesis_tables_and_figures.py
```

### Step 3: Download Results
```bash
# From your Mac
scp -r laguna:~/cnnthesis/thesis_output ~/Desktop/
```

---

## 📊 **WHAT YOU'LL GET:**

### **6 TABLES:**
1. **Table 1: Sample Statistics** - Data summary (sample period, stocks, etc.)
2. **Table 2: Horizon Evaluation** - 1d, 3d, 10d results
3. **Table 3: Portfolio Performance (EW)** - Decile returns, Sharpe ratios
4. **Table 4: Portfolio Performance (VW)** - Value-weighted version
5. **Table 5: FOMC Event Study** ⭐ **MAIN CONTRIBUTION** - All 3 windows with significance
6. **Table 6: EW vs VW Comparison** - Shows small-cap concentration

### **6 FIGURES:**
1. **Figure 1: FOMC Timeline** - Visual proof of no overlap
2. **Figure 2: Decile Performance** - Bar charts comparing EW vs VW
3. **Figure 3: Horizon Evaluation** - Line chart showing momentum
4. **Figure 4: FOMC Results** ⭐ **MAIN CONTRIBUTION** - Event study bar chart
5. **Figure 5: EW vs VW Comparison** - Small-cap concentration across all tests
6. **Figure 6: CNN Architecture** - Simplified diagram for readers

---

## 📝 **HOW TO USE IN YOUR THESIS:**

### For LaTeX:
```latex
\input{tables/table5_fomc_results.tex}

\begin{figure}[h]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/figure4_fomc_results.pdf}
  \caption{CNN Performance Around FOMC Announcements}
  \label{fig:fomc_results}
\end{figure}
```

### For Microsoft Word:
1. Open Excel
2. Import CSV files from `tables/` for easy formatting
3. Insert PNG images from `figures/`

---

## ✅ **ALL FONTS ARE TIMES NEW ROMAN**

Figures will match your thesis formatting perfectly!


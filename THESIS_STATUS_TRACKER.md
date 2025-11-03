# Thesis Status Tracker

**Last Updated:** October 30, 2025  
**Model:** CNN I20/R5 (20-day lookback, 5-day forecast)  
**Sample:** US stocks, 2001-2024 (out-of-sample)

---

## ✅ COMPLETED (Ready to Use)

### Contribution 1: CNN Replication
- [x] **Model Training** - 5 ensemble models trained (1992-2000)
  - Architecture: Same as Jiang et al. (2023) - NO MODIFICATIONS
  - Training time: ~50 GPU-hours
  - Location: `WORK_SPACE/new_model_res/`

- [x] **Predictions Generated** - 8.9M weekly predictions (2001-2024)
  - File: `CACHE_DIR/weekly_prediction_with_rets.csv` (322 MB)
  - Coverage: 22,480 stocks, ~1,200 weeks
  - Variable: CNN20D5P (up-probability)

- [x] **Horizon Evaluation** - Predictive power across different horizons
  - File: `CACHE_DIR/horizon_eval.csv`
  - Results:
    * 1-day: EW 0.87%, VW 0.09%
    * 3-day: EW 1.11%, VW 0.20%
    * 10-day: EW 1.37%, VW 0.24%
  - **Finding:** Predictive power increases with horizon ✅

- [x] **Portfolio Performance** - Decile portfolios (2001-2024)
  - Files: `CACHE_DIR/PORTFOLIO/cnn_weekly/CNN20D5P/ew.csv`, `vw.csv`
  - Results:
    * EW H-L: 71% annual, Sharpe 5.60, Turnover 654%
    * VW H-L: 23% annual, Sharpe 1.54, Turnover 728%
  - **Finding:** Strong predictive power, concentrated in small caps ✅

---

## ⏳ IN PROGRESS (Need to Run)

### Contribution 2: FOMC Event Study

- [x] **FOMC Schedule** - 316 meetings collected
  - File: `CACHE_DIR/fomc/fomc_schedule_with_offsets.csv`
  - Coverage: 1992-2024
  - Offsets calculated: t-1, t+1, t+4, t+20

- [ ] **FOMC Window Returns** - Need to re-run with corrected windows
  - File: `CACHE_DIR/fomc/fomc_window_returns.csv` (will be regenerated)
  - Status: Code fixed (Oct 30), copied to Laguna ✅
  - **Action Required:** Submit `sbatch slurm/run_fomc_analysis.sh`
  - Time: ~5 hours
  - Issue: Previous run had wrong window definitions (pre_ret was day t, not t-1)

- [ ] **FOMC Decile Performance** - After window returns complete
  - File: `CACHE_DIR/fomc/fomc_decile_performance.csv`
  - Will contain: 217 events × 4 windows × 10 deciles
  - Windows: Pre-FOMC (t-1), Announcement (t), Reaction (t+1), Intermediate (t+4 to t+20)

- [ ] **Statistical Significance** - After decile performance complete
  - File: `CACHE_DIR/fomc/fomc_significance_tests.csv`
  - Will contain: T-stats, p-values for all windows
  - Status: Code ready on Laguna ✅
  - **Action Required:** Run after main FOMC job completes

---

## ❌ NOT NEEDED (Skip These)

### Optional Robustness (Low Priority):
- [ ] Stock characteristics regressions (test if CNN adds value beyond factors)
- [ ] Time-period stability (check if results hold in subperiods)
- [ ] Comparison to other macro events (ECB, BoJ, employment reports)
- [ ] Volatility-conditional analysis

**Recommendation:** Skip unless committee specifically requests

---

## 📊 What Results You Have

### Location: Laguna
```
~/cnnthesis/CACHE_DIR/
├── weekly_prediction_with_rets.csv (8.9M predictions) ✅
├── horizon_eval.csv (horizon results) ✅
├── PORTFOLIO/cnn_weekly/CNN20D5P/
│   ├── ew.csv (equal-weight results) ✅
│   ├── vw.csv (value-weight results) ✅
│   └── pf_data/ (time-series returns) ✅
└── fomc/
    ├── fomc_schedule_with_offsets.csv ✅
    ├── fomc_window_returns.csv (⏳ need to regenerate)
    ├── fomc_decile_performance.csv (⏳ need to generate)
    └── fomc_significance_tests.csv (⏳ need to generate)
```

### What's Missing:
- FOMC analysis results (will have after re-running)

---

## 📋 Action Plan (Next 24 Hours)

### Today (Your Time: 5 minutes):
```bash
ssh laguna
cd ~/cnnthesis
sbatch slurm/run_fomc_analysis.sh
```

### Tonight/Tomorrow (Computer Time: ~5 hours):
- Job runs automatically
- Check status: `squeue -u $USER`
- Monitor: `tail -f logs/fomc_align_*.out`

### Tomorrow Morning (Your Time: 10 minutes):
```bash
# After main job completes
sbatch slurm/run_fomc_significance.sh
# Wait 10 minutes

# Download results
scp -r laguna:~/cnnthesis/CACHE_DIR/fomc ~/Desktop/Thesis_Results/
```

### Tomorrow Afternoon (Your Time: 4 hours):
- Review results
- Update thesis with FOMC findings
- Create final tables and figures

---

## 🎯 Thesis Writing Timeline

### Data & Analysis: ⏳ 1 day (waiting for FOMC jobs)

### Writing:
- Introduction & Literature Review: 2-3 days
- Methodology: 2 days (use docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md)
- Results: 2 days (after FOMC results arrive)
- Discussion: 1-2 days
- Conclusion: 1 day

**Total: ~2 weeks** (with FOMC results in hand)

---

## 📚 Documentation for GPT Agent

**When you ask GPT to help write thesis, point it to these files:**

**For methodology section:**
- `docs/COMPLETE_THESIS_GUIDE_FOR_WRITING.md` - Comprehensive guide
- `FOMC_METHODOLOGY.md` - FOMC technical details
- `METHODOLOGY_GUIDE_FOR_GPT.md` - Code structure reference

**For results section:**
- `THESIS_DATA_INVENTORY.md` - What data you have
- `docs/THESIS_RESULTS_SUMMARY.md` - Current results
- `docs/STATISTICAL_SIGNIFICANCE_GUIDE.md` - How to report stats

**For understanding current status:**
- `THESIS_STATUS_TRACKER.md` - This file (what's done, what's pending)

---

## ⚠️ Known Issues & Limitations

### Acknowledged Limitations:

1. **High Gross Returns (EW 71%)**
   - Transaction costs would reduce substantially
   - Small-cap concentration means high bid-ask spreads
   - 654% turnover = frequent rebalancing
   - Interpret as "predictive power" not "trading profits"

2. **Statistical Power**
   - 217 FOMC events is moderate sample
   - High variance during macro announcements
   - May not detect small effects (<0.1%)
   - Economic significance emphasized

3. **Pre-FOMC Overlap**
   - Day t-1 in both CNN lookback and measurement window
   - Represents realistic trading (use closing prices)
   - Acknowledge in methodology

4. **No Direct Behavioral Tests**
   - Don't test attention/sentiment directly
   - Use small-cap concentration as indirect evidence
   - Suggest for future research

---

## ✅ Bottom Line

**Completed:** Contributions 1 (CNN replication)  
**In Progress:** Contribution 2 (FOMC analysis) - waiting on one job  
**Ready:** All code fixed, documentation organized  
**Timeline:** Results tomorrow, thesis draft in 2 weeks  

**Submit that job and you're on track!** 🎓




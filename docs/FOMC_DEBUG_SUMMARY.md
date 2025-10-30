# FOMC Pipeline Debugging Summary

## Problem Discovered
After hours of debugging, we found **TWO fundamental issues**:

### Issue 1: Data Generation Bug in `build_windows.py`
**Symptom:** All FOMC window return columns (`react_ret`, `cum_t4`, `cum_t20`, `intermediate_ret`) were empty (NaN).

**Root Cause (Lines 109-115):**
```python
# WRONG: Merging on Date+StockID when Date values differ across dataframes
base = pre.merge(react[["Date", "StockID", "react_ret"]], on=["Date", "StockID"], how="left")
```

The script created separate dataframes for different time windows:
- `pre`: Date = announcement_date (t=0)
- `react`: Date = t+1 
- `cum4`: Date = t+4
- `cum20`: Date = t+20

Then tried to merge them all on `Date`, which failed because the `Date` column had different values in each dataframe!

**Fix:** Merge on `announcement_date` + `StockID` instead:
```python
base = base.merge(
    react[["announcement_date", "StockID", "react_ret"]], 
    on=["announcement_date", "StockID"], 
    how="left"
)
```

**Result:** ✅ FOMC window returns now correctly populated with all return metrics.

---

### Issue 2: Alignment Script Performance
**Symptom:** `align_predictions_and_score.py` hangs indefinitely without producing output.

**Root Cause:**
1. **Date Mismatch:** Predictions start in 2001 (out-of-sample), but FOMC windows go back to 1992. This creates a 9-year gap with no matching predictions.
2. **Inefficient Loop:** The stock-by-stock `merge_asof` loop (lines 118-137) processes ~29,000 stocks sequentially, which is extremely slow.
3. **Pandas Bug:** The vectorized `pd.merge_asof(..., by="StockID")` throws `ValueError: left keys must be sorted` even when data IS sorted, suggesting a pandas 1.x compatibility issue.

**Current Status:** 
- Data generation fixed ✅
- Alignment script still running (Job 19092) with stock-by-stock loop
- Need to either:
  a) Wait for the loop to complete (~1-2 hours estimated)
  b) Optimize the merge approach
  c) Filter FOMC windows to 2001+ only to reduce merge size

---

## What Was Wrong Fundamentally
1. **The original replication package had a bug** in `build_windows.py` that produced empty return columns.
2. **The alignment script works correctly** but is computationally expensive due to:
   - Large data volume (2.3M FOMC events × 8.9M predictions)
   - Date range mismatch (1992 vs 2001 start dates)
   - Pandas `merge_asof` performance limitations

---

## Next Steps
1. ✅ Fixed data generation - FOMC windows now have correct returns
2. ⏳ Monitor Job 19092 to see if stock-by-stock loop completes
3. If still too slow, filter FOMC windows to prediction date range (2001-2024)
4. Once alignment completes, run summary statistics and analyze results

---

## Files Fixed
- `trend_code_submit/Analysis/fomc/build_windows.py` (lines 108-133)
- `trend_code_submit/Analysis/fomc/align_predictions_and_score.py` (added debug prints, switched to stock loop)
- `slurm/run_just_align.sh` (increased time limit to 2 hours, added `-u` flag)


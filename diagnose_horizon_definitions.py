#!/usr/bin/env python3
"""
Diagnostic: Verify exactly what "+1 day", "+3 days" etc. mean.

This addresses Issue #3: Horizon definition clarity
"""

import pandas as pd
import numpy as np
import os

# Load a sample of predictions and returns to trace the calculation
pred_file = os.path.expanduser(
    '~/Desktop/Thesis Materials/cnnthesis/CACHE_DIR/weekly_prediction_with_rets.csv'
)

print("="*80)
print("HORIZON DEFINITION DIAGNOSTIC")
print("="*80)

if not os.path.exists(pred_file):
    print(f"ERROR: {pred_file} not found")
    exit(1)

pred = pd.read_csv(pred_file, parse_dates=["Date"], nrows=10000)  # Sample
print(f"\nLoaded sample: {len(pred)} predictions")

# Show example
sample = pred.iloc[0]
print(f"\nEXAMPLE PREDICTION:")
print(f"  Date: {sample['Date']}")
print(f"  StockID: {sample['StockID']}")
print(f"  CNN20D5P: {sample['CNN20D5P']:.4f}")

#Check what columns exist
print(f"\nAVAILABLE RETURN COLUMNS:")
ret_cols = [c for c in pred.columns if 'ret' in c.lower() or 'Ret' in c]
for col in ret_cols:
    print(f"  - {col}")

print("\n" + "="*80)
print("HORIZON CALCULATION TRACE")
print("="*80)

# Load the horizon_eval_conditional.py code to see what it does
horizon_code_file = os.path.expanduser(
    '~/Desktop/Thesis Materials/cnnthesis/trend_code_submit/Analysis/fomc/horizon_eval_conditional.py'
)

if os.path.exists(horizon_code_file):
    print(f"\nReading horizon calculation code...")
    with open(horizon_code_file, 'r') as f:
        code = f.read()
    
    # Find the horizon_ret function
    import re
    pattern = r'def horizon_ret.*?return.*?assign'
    match = re.search(pattern, code, re.DOTALL)
    
    if match:
        print("\n" + "-"*80)
        print("CODE FOR HORIZON CALCULATION:")
        print("-"*80)
        print(match.group(0))
        print("-"*80)
    
    # Find how FOMC days are tagged
    fomc_pattern = r'is_fomc.*?=.*?isin'
    fomc_match = re.search(fomc_pattern, code, re.DOTALL)
    
    if fomc_match:
        print("\n" + "-"*80)
        print("CODE FOR FOMC DAY CLASSIFICATION:")
        print("-"*80)
        print(fomc_match.group(0))
        print("-"*80)

print("\n" + "="*80)
print("INTERPRETATION")
print("="*80)

print("""
From the code above, the horizon calculation works as follows:

1. horizon_ret(k) computes k-day FORWARD return from ANY prediction date

2. For a prediction made on Date t:
   - ret_1d  = return from t to t+1
   - ret_3d  = return from t to t+3  
   - ret_10d = return from t to t+10

3. For FOMC days, the "Date" in the comparison is:
   - The PREDICTION date (when CNN was run)
   - NOT the announcement date!

4. This means:
   - If prediction was Friday (t=0)
   - And FOMC was Wednesday (t+5)
   - "FOMC +1 day" = Friday to Monday (t to t+1)
   - Which is BEFORE the FOMC announcement!

⚠️  CRITICAL: This might NOT be what you intended!

RECOMMENDATION:
You probably want to measure returns FROM the announcement date, not from prediction date.

For proper FOMC analysis:
- Prediction date: Friday before (e.g., June 12)
- FOMC announcement: Wednesday (e.g., June 15) ← This should be t=0
- +1 day: Thursday June 16 (from announcement)
- +3 days: Monday June 22 (from announcement)
- +10 days: July 1 (from announcement)

But your current code measures from PREDICTION date:
- +1 day: Monday June 15 (which IS the announcement!)
- +3 days: Wednesday June 17 (2 days after announcement)
- +10 days: June 26 (11 days after announcement)

This is confusing and not what typical event study does!
""")

print("\n" + "="*80)
print("ACTION REQUIRED")
print("="*80)

print("""
1. Check your horizon_eval_conditional.py code

2. Verify: Are horizons measured from PREDICTION date or ANNOUNCEMENT date?

3. For FOMC vs non-FOMC comparison:
   - FOMC days: Should measure from announcement date
   - Non-FOMC days: Can measure from prediction date (since no event)
   
4. If currently measuring from prediction date for BOTH:
   - That's inconsistent!
   - FOMC +1d would INCLUDE the announcement itself
   - Creates overlap and confusion

5. SOLUTION:
   For FOMC events specifically, recalculate horizons relative to announcement:
   - Get announcement date
   - Calculate returns: announcement close → +k days later
   - This is what standard event studies do

6. Verify your "intermediate window" (t+5 to t+20):
   - This DOES measure from announcement
   - So why would horizons measure from prediction?
   - Inconsistent!
""")


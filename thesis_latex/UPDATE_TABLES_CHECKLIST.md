# Checklist: Updating Tables to Finance Journal Style

Use this checklist to systematically update all your tables.

## 📋 Tables to Update

### Main Results Tables

- [ ] **Table 1: Sample Statistics** (`table1_sample_statistics.tex`)
  - Current: Simple table with `lc` columns
  - Update: Add `threeparttable`, use `S` columns for numbers if applicable
  - Status: ⏳ Pending

- [ ] **Table 2: Horizon Evaluation** (`table2_horizon_evaluation.tex`)
  - Current: `lccc` columns, notes in caption
  - Update: Use `S` columns, move notes to `threeparttable`
  - Example: See `table2_horizon_evaluation_UPDATED.tex`
  - Status: ⏳ Pending

- [ ] **Table 3: Portfolio EW** (`table3_portfolio_ew.tex`)
  - Current: `lccc` columns
  - Update: Use `S[table-format=-2.2]` for returns, `S[table-format=2.2]` for volatility
  - Status: ⏳ Pending

- [ ] **Table 4: Portfolio VW** (`table4_portfolio_vw.tex`)
  - Current: Similar to Table 3
  - Update: Same format as Table 3
  - Status: ⏳ Pending

- [ ] **Table 5: FOMC Event Study** (`table5_fomc_event_study.tex`)
  - Current: Has significance stars, but needs formatting
  - Update: Use `S` columns, proper star formatting, `threeparttable`
  - Status: ⏳ Pending

- [ ] **Table 5a: Announcement Day** (`table5a_announcement_day.tex`)
  - Current: Needs review
  - Update: Format to match Table 5 style
  - Status: ⏳ Pending

- [ ] **Table 6: FOMC vs Matched** (`table6_fomc_vs_matched.tex`)
  - Current: Needs review
  - Update: Use `S` columns, proper formatting
  - Status: ⏳ Pending

- [ ] **Table 6: EW vs VW Comparison** (`table6_ew_vw_comparison.tex`)
  - Current: Needs review
  - Update: Format consistently
  - Status: ⏳ Pending

- [ ] **Table 7: EW vs VW Summary** (`table7_ew_vs_vw_summary.tex`)
  - Current: Needs review
  - Update: Format consistently
  - Status: ⏳ Pending

- [ ] **Table 7: Transaction Costs** (`table7_transaction_costs.tex`)
  - Current: Needs review
  - Update: Format consistently
  - Status: ⏳ Pending

- [ ] **Table 8: Size-Sorted** (`table8_size_sorted.tex`)
  - Current: Needs review
  - Update: Format consistently
  - Status: ⏳ Pending

- [ ] **Table 9: FOMC Timeline** (`table9_fomc_timeline.tex`)
  - Current: Needs review
  - Update: Format consistently
  - Status: ⏳ Pending

- [ ] **Table 10: Decile Regimes** (`table10_decile_regimes.tex`)
  - Current: Needs review
  - Update: Format consistently
  - Status: ⏳ Pending

## ✅ Update Steps for Each Table

For each table, follow these steps:

1. **Open the table file** in `thesis_output/tables/`

2. **Check current format:**
   - What columns does it use? (`l`, `c`, `r`, or `S`)
   - Does it have notes? Where are they?
   - Does it use significance stars? How are they formatted?

3. **Update column format:**
   - Replace numeric columns with `S[table-format=X.Y]`
   - Wrap column headers in `{}` when using `S` columns
   - Keep text columns as `l`, `c`, or `r`

4. **Add table structure:**
   - Add `[htbp]` placement
   - Add `\centering`
   - Wrap in `threeparttable` if you have notes

5. **Update notes:**
   - Move notes from caption to `\begin{tablenotes}`
   - Use `\footnotesize`
   - Add significance star explanation if needed

6. **Fix significance stars:**
   - Use `$^{*}$`, `$^{**}$`, `$^{***}$` or `\tnote{***}`
   - Add explanation in notes section

7. **Test compilation:**
   ```bash
   cd thesis_latex
   ./build.sh
   ```
   - Check that table compiles without errors
   - Verify alignment looks correct
   - Check notes display properly

8. **Mark as complete:**
   - Update this checklist
   - Commit changes to git

## 🎯 Priority Order

Update in this order for maximum impact:

1. **High Priority** (Main results):
   - Table 3 (Portfolio EW) - Most important result
   - Table 4 (Portfolio VW) - Second most important
   - Table 5 (FOMC Event Study) - Key contribution
   - Table 6 (FOMC vs Matched) - Key contribution

2. **Medium Priority** (Supporting results):
   - Table 2 (Horizon Evaluation)
   - Table 5a (Announcement Day)
   - Table 7 (EW vs VW Summary)
   - Table 8 (Size-Sorted)

3. **Lower Priority** (Additional tables):
   - Table 1 (Sample Statistics)
   - Table 7 (Transaction Costs)
   - Table 9 (FOMC Timeline)
   - Table 10 (Decile Regimes)

## 📝 Notes

- **Don't update all at once:** Do 2-3 tables, test, then continue
- **Use templates:** Copy from `table_templates.tex` as starting point
- **Be consistent:** All tables should look similar
- **Test frequently:** Compile after each update

## 🔗 Resources

- **Templates:** `table_templates.tex`
- **Formatting Guide:** `TABLE_FORMATTING_GUIDE.md`
- **Example Update:** `table2_horizon_evaluation_UPDATED.tex`

Good luck! 🎓


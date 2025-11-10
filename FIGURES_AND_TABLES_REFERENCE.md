# Tables & Figures Reference (Updated November 2025)

**Purpose:** Give myself a single, trustworthy map for every table and figure that will appear in the thesis. Each entry below explains the content, the key numbers, how to interpret it, where it should appear, and the placeholder tag to drop into the draft (e.g., `[TABLE 3 ABOUT HERE]`).

---

##  Tables (11 total)

### Table 1 – Sample Statistics `[TABLE 1 ABOUT HERE]`
- **Content:** Out-of-sample period (2001–2024), number of unique stocks (22,480), weekly prediction dates (1,211), FOMC meetings with signals (216), CNN architecture summary (20-day lookback, 5-day horizon, 5-model ensemble).
- **Use:** Methodology Section 3.2 when I describe the dataset and model scope; cite again briefly in Results 5.1 if needed.
- **Key message:** Establishes breadth of coverage and confirms I am using the Jiang–Kelly–Xiu CNN “as-is”.

### Table 2 – Horizon Evaluation `[TABLE 2 ABOUT HERE]`
- **Content:** EW and VW high-minus-low spreads at 1-, 3-, and 10-day horizons (0.87% → 1.37% EW; 0.09% → 0.24% VW).
- **Use:** Results 5.2 to show predictability increases with horizon (momentum); mention in Discussion 6.1 when contrasting diffusion across horizons.
- **Key message:** Predictability strengthens as returns are allowed to compound; VW barely moves, foreshadowing the small-cap narrative.

### Table 3 – Equal-Weight Decile Performance `[TABLE 3 ABOUT HERE]`
- **Content:** Annual returns, volatilities, Sharpe ratios for deciles 1–10 plus H–L (−28.08% → 42.66%; H–L = 70.74%; Sharpe = 5.60).
- **Use:** Results 5.1 baseline replication.
- **Key message:** CNN ranks the cross-section monotonically; the economic magnitude is massive for small caps.

### Table 4 – Value-Weight Decile Performance `[TABLE 4 ABOUT HERE]`
- **Content:** Same layout as Table 3 but value-weighted (−3.50% → 19.19%; H–L = 22.69%; Sharpe = 1.54).
- **Use:** Results 5.1 alongside Table 3.
- **Key message:** Predictability persists but is attenuated in large caps; sets up EW versus VW comparisons.

### Table 5 – FOMC Event Study `[TABLE 5 ABOUT HERE]`
- **Content:** Announcement day (0.21%, t=2.95, robust), Reaction day (0.10%, fragile), Intermediate window (0.35%, t=2.24, robust). Includes medians and winsorized checks.
- **Use:** Results 5.3; cite again in Discussion 6.1.
- **Key message:** CNN still finds positive spreads on FOMC days when viewed in isolation—important nuance before the matched comparison.

### Table 6 – FOMC vs Matched Non-FOMC `[TABLE 6 ABOUT HERE]`
- **Content:** Event-level mean spreads for horizons 1–10 (FOMC averages 0.10%–0.63% vs matched 0.88%–1.16%; differences −0.49% to −0.87%; t = −4.17 to −11.90, all q-values ≪ 0.001).
- **Use:** Results 5.2 main contribution; revisit in Discussion 6.1 and 6.2.
- **Key message:** Predictability collapses during FOMC weeks across every horizon.

### Table 7 – EW vs VW Summary `[TABLE 7 ABOUT HERE]`
- **Content:** EW/VW ratios for the overall portfolio, horizon tests, and FOMC windows (3× to 10× multiples).
- **Use:** Results 5.4 (mechanism) and Discussion 6.1.
- **Key message:** Predictability is concentrated in small caps—consistent with limited attention/limited arbitrage.

### Table 8 – Size-Sorted Predictability `[TABLE 8 ABOUT HERE]`
- **Content:** Quintile-level EW and VW H–L spreads (Q1 = 2.57% / 2.33%; Q5 = 0.31% / 0.33%; 1,210 weeks per quintile).
- **Use:** Results 5.4 and Discussion 6.1.
- **Key message:** Direct evidence that spreads taper smoothly with firm size, validating the small-cap interpretation.

### Table 9 – FOMC Timeline Decomposition `[TABLE 9 ABOUT HERE]`
- **Content:** Pre-announcement (t−1→t), announcement (t), reaction (t+1), and intermediate (t+4→t+20) spreads, t-stats, and p-values for EW/VW.
- **Use:** Results 5.5, Discussion 6.2 (attention life-cycle).
- **Key message:** Predictability is already decaying before the announcement, compresses sharply right after, and gradually re-expands.

### Table 10 – Decile Returns by Regime `[TABLE 10 ABOUT HERE]`
- **Content:** Decile averages for FOMC weeks vs matched weeks plus H–L differences (tails compress toward zero during FOMC weeks).
- **Use:** Results 5.2 (visual evidence) and Discussion 6.2.
- **Key message:** The entire cross-sectional distribution tightens during FOMC weeks, not just the mean spread.

### Table 11 – Architecture Robustness `[TABLE 11 ABOUT HERE]`
- **Content:** EW and VW spreads for alternate CNN configurations and linear baselines (I5/R5, I20/R20, I60/R20 for CNN; linear benchmarks for comparison).
- **Use:** Results 5.3 robustness subsection; Discussion 6.4.
- **Key message:** The attention-based effect survives architecture changes; CNN materially outperforms linear models.

---

##  Figures (7 total)

### Figure 1 – FOMC Timeline `[FIGURE 1 ABOUT HERE]`
- **Use:** Methodology 3.4 to demonstrate no look-ahead; reference again in Discussion 6.2.
- **Key message:** The CNN signal (prior Friday), the FOMC event, and measurement windows are strictly ordered.

### Figure 2 – Decile Performance `[FIGURE 2 ABOUT HERE]`
- **Use:** Results 5.1 immediately after Tables 3 & 4.
- **Key message:** Visualize the monotonic decile pattern and the EW vs VW contrast.

### Figure 3 – Horizon Evaluation `[FIGURE 3 ABOUT HERE]`
- **Use:** Results 5.2.
- **Key message:** EW spreads slope upward with horizon; VW stays near zero.

### Figure 4 – FOMC Event Study Bars `[FIGURE 4 ABOUT HERE]`
- **Use:** Results 5.3 alongside Table 5.
- **Key message:** Graphically show announcement/intermediate significance vs muted VW response.

### Figure 5 – FOMC minus Matched Differences `[FIGURE 5 ABOUT HERE]`
- **Use:** Results 5.2 with Table 6.
- **Key message:** Error bars (95% CI) sit entirely below zero at every horizon.

### Figure 6 – EW/VW Ratios `[FIGURE 6 ABOUT HERE]`
- **Use:** Results 5.4 (mechanism), Discussion 6.1.
- **Key message:** Summarizes the 3–10× small-cap overlay in one glance.

### Figure 7 – Attention Timeline `[FIGURE 7 ABOUT HERE]`
- **Use:** Results 5.5 and Discussion 6.2.
- **Key message:** Stylized visualization of attention build-up, announcement spike, and post-event normalization.

---

##  Placement Cheat Sheet

| Location | Exhibits to Insert | Notes |
|----------|-------------------|-------|
| **Methodology 3.2–3.5** | `[TABLE 1 ABOUT HERE]`, `[FIGURE 1 ABOUT HERE]` | Use after describing data universe and alignment rule. |
| **Results 5.1** | `[TABLE 3 ABOUT HERE]`, `[TABLE 4 ABOUT HERE]`, `[FIGURE 2 ABOUT HERE]` | Pair the tables and figure to emphasize monotonicity and EW vs VW. |
| **Results 5.2 (Horizon + Matched)** | `[TABLE 2 ABOUT HERE]`, `[TABLE 6 ABOUT HERE]`, `[TABLE 10 ABOUT HERE]`, `[FIGURE 3 ABOUT HERE]`, `[FIGURE 5 ABOUT HERE]` | Start with Table 2 and Figure 3, then transition to the matched comparison tables and figure. |
| **Results 5.3 (Event Study)** | `[TABLE 5 ABOUT HERE]`, `[FIGURE 4 ABOUT HERE]` | Discuss robustness and the nuance that event-level spreads remain positive. |
| **Results 5.4 (Mechanism)** | `[TABLE 7 ABOUT HERE]`, `[TABLE 8 ABOUT HERE]`, `[FIGURE 6 ABOUT HERE]` | Use Table 8 for the direct size evidence and Figure 6 for the summary ratios. |
| **Results 5.5 (Temporal Dynamics)** | `[TABLE 9 ABOUT HERE]`, `[FIGURE 7 ABOUT HERE]` | Tie spreads over time to the attention story. |
| **Robustness Appendix / Text** | `[TABLE 11 ABOUT HERE]` | Mention in-text and/or appendix when reporting alternative architectures. |

Remember to drop each placeholder on its own line immediately after the paragraph that interprets the corresponding exhibit.

---

## ️ Writing Reminders
- Discuss the exhibit before presenting the placeholder (“As shown in Table 6…” then add `[TABLE 6 ABOUT HERE]`).
- When referencing numbers, mirror the exact values shown in **`VALIDATED_RESULTS.md`** and **`ANALYTIC_SUMMARY_TABLES_FIGURES.md`** so everything stays consistent.
- Update the Works Cited section in each chapter whenever a new paper is mentioned in relation to an exhibit.

---

**This reference is current as of November 2025. If new tables/figures are generated, update this file and the prompts immediately.**



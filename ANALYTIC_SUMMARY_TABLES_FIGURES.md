# Analytical Notes on Tables & Figures (Detailed Guide)

Use this sheet while drafting the Results section. Each table/figure entry lists the numbers that must be quoted, the interpretation to emphasize, any caveats, and suggested phrasing + placement cues.

---

## Tables

### Table 1 – Sample Statistics `[TABLE 1 ABOUT HERE]`
- **Numbers to mention:** 22,480 unique stocks; 1,211 weekly prediction dates (Fridays); ~8.9 million stock-week observations; 216 FOMC announcements with valid signals.
- **Story:** Establish scope and that the CNN model is a fixed measurement tool (20-day lookback, 5-day forecast, 5-model ensemble trained 1993–2000).
- **Caution:** Keep this descriptive—no inference. Use it in Methodology §3.2 and briefly remind the reader in Results §5.1 that the model is pre-trained.

### Table 2 – Horizon Evaluation `[TABLE 2 ABOUT HERE]`
- **Numbers:** EW H–L = 0.87% (1d), 1.11% (3d), 1.37% (10d); VW H–L = 0.09%, 0.20%, 0.24%; EW/VW ratios ≈ 10×, 5.6×, 5.7×.
- **Interpretation:** Predictability compounds with horizon; VW’s flat profile previews the small-cap concentration. Mention the ~58% growth from 1-day to 10-day.
- **Use:** Results §5.2 before moving into the matched comparison.

### Table 3 – Equal-Weight Portfolio Performance `[TABLE 3 ABOUT HERE]`
- **Numbers:** Decile 1 = −28.08%, Decile 10 = +42.66%, H–L = 70.74%, Sharpe = 5.60, volatility roughly 19–20% across deciles.
- **Interpretation:** CNN organizes the cross-section monotonically; highlight that extreme deciles drive the spread but the slope is smooth.
- **Caution:** Note gross returns (no costs) if questioned later.

### Table 4 – Value-Weight Portfolio Performance `[TABLE 4 ABOUT HERE]`
- **Numbers:** Decile 1 = −3.50%, Decile 10 = +19.19%, H–L = 22.69%, Sharpe = 1.54.
- **Interpretation:** Predictability persists but is diluted when large caps dominate; sets up the EW vs VW contrast.
- **Suggested line:** “Even when capital-weighted, the CNN signal produces a 22.69% annual spread, though it is roughly one third of the equal-weighted effect.”

### Table 5 – FOMC Event Study `[TABLE 5 ABOUT HERE]`
- **Numbers:** Announcement (t): 0.21%, t=2.95, p=0.004; Reaction (t+1): 0.10%, t=1.76, p=0.079; Intermediate (t+5→t+20): 0.35%, t=2.24, p=0.026. Means ≈ medians; winsorization changes <12%.
- **Interpretation:** Even in isolation, FOMC days show positive spreads—important nuance before presenting the matched comparison.
- **Caution:** Call the reaction window “fragile” (large mean-median gap) and avoid over-selling it.

### Table 6 – FOMC vs Matched Non-FOMC `[TABLE 6 ABOUT HERE]`
- **Numbers:** Differences range −0.49% to −0.87% across horizons; t-statistics −4.17 to −11.90; all p < 0.001 and FDR q ≪ 0.001.
- **Interpretation:** The heart of the paper—predictability collapses uniformly during FOMC weeks relative to matched normal weeks.
- **Suggested phrasing:** “Across all ten horizons the FOMC-minus-normal spread is negative, highly significant, and economically large (≈ −0.5 to −0.9 p.p.).”

### Table 7 – EW vs VW Summary `[TABLE 7 ABOUT HERE]`
- **Numbers:** EW/VW ratios: 3.12× (portfolio), 9.67× (H+1d), 5.55× (H+3d), 5.71× (H+10d), 4.20× (FOMC announcement), 3.33× (reaction), −1.25× (intermediate because VW turns negative).
- **Interpretation:** Crystalizes the small-cap concentration; drives the behavioral narrative.
- **Note:** Explain the negative ratio for intermediate VW as evidence of large-cap reversal.

### Table 8 – Size-Sorted Predictability `[TABLE 8 ABOUT HERE]`
- **Numbers:** EW H–L from 2.57% (Q1) → 0.31% (Q5); VW mirrors 2.33% → 0.33%.
- **Interpretation:** Direct size test—spreads decline smoothly with firm size.
- **Use:** Mechanism subsection; say “The effect is ~8× stronger in the smallest quintile than the largest.”

### Table 9 – FOMC Timeline Decomposition `[TABLE 9 ABOUT HERE]`
- **Numbers:** EW = 0.21% in pre window, 0.21% on announcement, 0.10% reaction, 0.35% intermediate. VW mostly 0–0.05%, intermediate −0.28%.
- **Interpretation:** Describes the attention life-cycle: build-up, compression, gradual re-expansion.
- **Caution:** Mention reaction window softness and that VW becomes negative later (large caps mean-revert slightly).

### Table 10 – Decile Returns by Regime `[TABLE 10 ABOUT HERE]`
- **Numbers:** FOMC EW H–L = 1.61%; matched EW H–L = 1.79%; long leg shrinks (0.73% vs 0.69%), short leg becomes less negative (−0.88% vs −1.10%). VW flips from −0.34% to +0.32%.
- **Interpretation:** Both tails compress toward zero on FOMC weeks—visual evidence of reduced dispersion.
- **Use:** When describing the mechanics of Table 6; helps illustrate that the difference is driven by both legs moving.

### Table 11 – Architecture Robustness `[TABLE 11 ABOUT HERE]`
- **Numbers:** CNN EW spreads = 30.46%, 27.47%, 22.24% (for I5/R5, I20/R20, I60/R20); linear models only 7–10% and unstable VW (even negative).
- **Interpretation:** Confirms state dependence is not contingent on one architecture; CNN clearly outperforms linear baselines.
- **Use:** Mention briefly in Results robustness subsection and expand in Discussion §6.4 when noting limitations.

---

## Figures

### Figure 1 – FOMC Timeline `[FIGURE 1 ABOUT HERE]`
- **Purpose:** Illustrate the ordering “Prediction Friday ≤ Event Day ≤ Return Window”.
- **Talking point:** “This visual confirms the signal is always formed before the event and before I start measuring returns.”

### Figure 2 – Decile Performance `[FIGURE 2 ABOUT HERE]`
- **Purpose:** Visual companion to Tables 3 & 4; highlight the steep EW slope vs subdued VW slope.
- **Talking point:** “Panel A shows EW returns climbing steadily, Panel B reveals how value weighting flattens the profile.”

### Figure 3 – Horizon Evaluation `[FIGURE 3 ABOUT HERE]`
- **Purpose:** Reinforce Table 2 with a line chart.
- **Talking point:** “EW spreads fan out with horizon whereas VW remains nearly flat, underscoring momentum concentrated in small caps.”

### Figure 4 – FOMC Event Study `[FIGURE 4 ABOUT HERE]`
- **Purpose:** Visualize Table 5; show announcement/intermediate bars with significance stars.
- **Talking point:** “The blue (EW) bars are positive and significant on announcement and intermediate windows; the orange (VW) bars hover near zero.”

### Figure 5 – FOMC vs Matched Differences `[FIGURE 5 ABOUT HERE]`
- **Purpose:** Display the negative differences with 95% confidence intervals below zero.
- **Talking point:** “Every point sits below zero with tight error bars—visually undeniable evidence of the collapse.”

### Figure 6 – EW vs VW Ratios `[FIGURE 6 ABOUT HERE]`
- **Purpose:** Summarize small-cap dominance across tests.
- **Talking point:** “Ratios from 3× to 10× make the small-cap mechanism immediately obvious.”

### Figure 7 – Attention Timeline `[FIGURE 7 ABOUT HERE]`
- **Purpose:** Conceptual illustration of attention build-up, announcement spike, and normalization.
- **Talking point:** “This figure ties the temporal pattern (Table 9) back to the behavioral story.”

---

## Quick Writing Tips
- Reference the table/figure **before** dropping the placeholder tag.
- Always pair key numbers with interpretation (e.g., “−0.78 p.p., t = −11.90***, meaning…”).
- Cross-reference other tables/figures when reinforcing a point (e.g., “Consistent with Table 8, Figure 6 shows…”).
- Mention robustness (medians, winsorization, FDR) where relevant, citing Table 5 or Table 6 directly.
- Keep `VALIDATED_RESULTS.md` open to ensure numerical consistency.

This guide plus the prompts should produce a richer, more analytical Results chapter. 


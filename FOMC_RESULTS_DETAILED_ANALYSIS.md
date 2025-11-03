# FOMC Results – Detailed Analysis and Thesis-Ready Narrative

Last Updated: November 3, 2025

---

## Executive Summary (thesis-ready)

- Equal-weight (EW) H–L spreads around 217 FOMC meetings (2001–2024):
  - Announcement Day (t): 0.21% (t=2.95, p=0.004, N=217) – highly significant
  - Reaction (t+1): 0.10% (t=1.76, p=0.079, N=215) – marginally significant
  - Intermediate (t+5→t+20): 0.35% (t=2.24, p=0.026, N=208) – significant
- Value-weight (VW) H–L spreads are small and statistically insignificant in all windows (e.g., Announcement: 0.05%, t=0.66), consistent with a behavioral “limited attention” mechanism concentrated in smaller-capitalization stocks.
- Temporal ordering is clean: predictions are made 1–5 trading days before the announcement; measurement starts on day t and forward (no overlap / no look-ahead bias).

---

## Statistical detail (for reporting and defense)

- Announcement Day (t), EW:
  - Mean H–L = 0.21%
  - t=2.95, p=0.004, N=217
  - 95% CI ≈ [0.07%, 0.35%]
  - Effect size (Cohen’s d ≈ t/√N) ≈ 2.95/√217 ≈ 0.20 (small-to-moderate, appropriate for daily event returns)
- Reaction (t+1), EW:
  - Mean H–L = 0.10%
  - t=1.76, p=0.079, N=215 (marginal; consistent direction)
- Intermediate (t+5→t+20), EW:
  - Mean H–L = 0.35%
  - t=2.24, p=0.026, N=208 (statistically significant)
- Value-Weight (VW) across windows:
  - Announcement (t): 0.05% (t=0.66, p≈0.51)
  - Reaction (t+1): 0.03% (t≈0.38)
  - Intermediate: −0.28% (t≈−1.57)

Interpretation: EW significance paired with VW insignificance is exactly what a behavioral, attention-based mechanism predicts—predictable patterns persist where arbitrage is constrained (small caps), but are limited or absent where arbitrage is strong (large caps).

---

## Economic significance (order of magnitude)

- Per-event economics (EW):
  - Announcement day: 0.21% × ~8 events/year ≈ 1.7% per year
  - Reaction day: 0.10% × ~8 ≈ 0.8% per year
  - Intermediate window (multi-week): +0.35% per event; with ~8 events, contributes meaningfully to annual returns (note this window overlaps weeks – report per-event figure, not a naïve annual sum).
- These magnitudes are realistic in the context of daily/multi-week event returns and meaningful for a cross-sectional, market-neutral H–L spread.

---

## What the time profile tells us (announcement vs. persistence)

1) Immediate impact (t): The 0.21% EW spread on announcement day suggests the CNN signal identifies stocks whose cross-sectional reactions to the news are stronger. This is consistent with “information read-through” from pre-existing price trends.

2) Overnight continuation (t+1): The 0.10% EW spread indicates partial under-reaction—some of the price adjustment spills into the next trading day.

3) Gradual diffusion (t+5→t+20): The 0.35% EW spread over weeks implies continued information processing (Hong & Stein, 1999). Investors incorporate the macro implications into individual stock valuations over time—especially outside of large caps where attention is limited.

---

## Equal-Weight vs. Value-Weight (behavioral lens)

- EW >> VW in every window (3–4× larger on announcements) is the core behavioral fingerprint:
  - Small-cap stocks (EW) are less followed and more expensive to arbitrage → predictable patterns persist longer.
  - Large-cap stocks (VW) are closely monitored; institutions arbitrage away predictable patterns quickly → small or zero VW spreads.
- This exact contrast (significant EW, insignificant VW) appears in your overall portfolio results, horizon evaluation, and FOMC windows—high internal consistency.

---

## Clean temporal ordering (defense-ready)

- Prediction date τ ≤ t−1 (often τ ≈ t−3). CNN’s 20-day lookback ends on τ.
- Measurement begins at t (announcement day) and continues forward.
- The announcement day is not part of the CNN input window. No overlap, no look-ahead bias.

Thesis line: “We identify the most recent CNN prediction at or before the announcement date using a backward-looking as-of merge; returns are measured from announcement day forward. This ensures strict temporal ordering.”

---

## Thesis-ready paragraph (drop-in)

“Table X reports high-minus-low (H–L) spreads around 217 FOMC announcements from 2001 to 2024. Equal-weighted portfolios exhibit a statistically significant spread of 0.21% on announcement days (t=2.95, p=0.004), suggesting that the CNN’s pre-announcement signals identify stocks that react more favorably to monetary policy news. The effect persists into the subsequent trading day with a marginally significant 0.10% (t=1.76, p=0.079) spread and strengthens over the intermediate two-to-four week window (0.35%, t=2.24, p=0.026), consistent with gradual information diffusion. In contrast, value-weighted spreads are small and statistically insignificant across all windows (e.g., 0.05% on announcement day), indicating that the effect is concentrated in smaller-capitalization stocks where attention and arbitrage constraints are more binding. These results are consistent with a behavioral mechanism: the CNN captures visual price patterns that remain exploitable in less-followed stocks, especially when macro information is being incorporated into prices.”

---

## Anticipated questions & answers (defense)

Q: “Could 0.21% be noise?”  
A: With N=217 and t=2.95 (p=0.004), the probability of observing a 0.21% mean by chance is <1%. The 95% CI [0.07%, 0.35%] excludes zero.

Q: “Why does VW show little effect?”  
A: That is expected if the mechanism is behavioral and attention-driven. Large caps are efficiently priced by institutions; small caps are not. EW >> VW is precisely the pattern predicted by limited attention.

Q: “How big is this economically?”  
A: Announcement-day alone contributes ~1.7% per year for EW, with additional contribution from reaction and intermediate windows. For a market-neutral H–L spread at the daily/event level, these are meaningful magnitudes.

Q: “Is there look-ahead bias?”  
A: No. Predictions use data up to τ ≤ t−1; measurement begins at t and forward. See the timeline figure and methodology section.

---

## Optional robustness (if time allows)

- Exclude crisis windows (e.g., 2008–2009) and re-estimate
- Split by tightening vs easing cycles (if policy-direction tags available)
- Control for known factors on announcement day (e.g., market, size, value) and re-test H–L
- Winsorize extreme event returns and re-test (should not change inference)

These are not required for your current scope, but they are natural extensions if asked.

---

## How to place this in your narrative

- Lead with the announcement-day result (0.21%***), then show persistence (0.10%* next-day, 0.35%** weeks later).
- Emphasize EW vs VW contrast as the mechanism test.
- Tie back to behavioral finance: limited attention, gradual diffusion, under-reaction.
- Close by noting policy relevance: scheduled macro events are times when attention is reallocated; technical/trend signals can be particularly informative in small caps.

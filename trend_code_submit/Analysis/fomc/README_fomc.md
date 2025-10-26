# FOMC Analysis Toolkit

This folder contains small, idempotent utilities to scrape the Federal Reserve's
FOMC calendar, build per‑stock FOMC event window returns from your processed CRSP panel,
and (optionally) align your weekly CNN predictions to FOMC dates to produce decile
performance around announcements.

## Files

- `scrape_calendar.py` — Scrapes FOMC calendars (1992–2024‑12‑31) from the Fed and saves
  two CSVs under `CACHE_DIR/fomc/`:
  - `fomc_schedule.csv`
  - `fomc_schedule_with_offsets.csv` (adds business‑day offsets t−1, t+1, t+5, t+20)

- `build_windows.py` — Uses `processed_US_data()` and the schedule to build per‑stock
  FOMC window returns (pre, reaction, intermediate) and saves:
  - `CACHE_DIR/fomc/fomc_window_returns.csv`

- `align_predictions_and_score.py` — Aligns your weekly CNN predictions to the last
  available prediction date on or before each FOMC announcement and computes decile
  performance for the three windows. Saves:
  - `CACHE_DIR/fomc/fomc_decile_performance.csv`

## Usage

Run from the repo root (`cnnthesis`), using the same Python env as the project:

1) Scrape and build the schedule

```
cnn_env/bin/python trend_code_submit/Analysis/fomc/scrape_calendar.py
```

2) Build per‑stock FOMC window returns from your processed CRSP panel

```
cnn_env/bin/python trend_code_submit/Analysis/fomc/build_windows.py
```

3) (Optional) Align weekly CNN predictions and score deciles around FOMC events

First make sure you have `CACHE_DIR/weekly_prediction_with_rets.csv` (run the
`make_prediction_with_rets.py` helper after training). Then:

```
cnn_env/bin/python trend_code_submit/Analysis/fomc/align_predictions_and_score.py
```

All outputs will be written under `CACHE_DIR/fomc/`.

## Notes
- Scripts are idempotent and safe to rerun — they overwrite their outputs.
- They import project modules directly; no need to activate the env — just use the
  interpreter path under `cnn_env/bin/python`.
- If you need a different date range, adjust `MIN_YEAR` / `MAX_DATE` in `scrape_calendar.py`.


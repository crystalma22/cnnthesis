#!/usr/bin/env python3
from __future__ import annotations

"""
Ingest a user-provided CSV of FOMC announcement dates (e.g., FOMC_Dates_1936.csv),
normalize it to the project's schedule schema, and write the two canonical files
under CACHE_DIR/fomc/:

  - fomc_schedule.csv
  - fomc_schedule_with_offsets.csv (adds business-day offsets)

Usage (from repo root):

  cnn_env/bin/python trend_code_submit/Analysis/fomc/ingest_manual_schedule.py \
      --path FOMC_Dates_1936.csv

This script is idempotent and safe to rerun. It filters rows to 1992-01-01 through
2024-12-31 inclusive and deduplicates by announcement_date, keeping the richest row
(preferring explicit time and URLs when present).
"""

import argparse
import os
import os.path as op
import re
from typing import Dict, List, Optional

import pandas as pd
import pytz
from dateutil import parser as dtparser

from Data import dgp_config as dcf


MIN_DATE = "1992-01-01"
MAX_DATE = "2024-12-31"
NY_TZ = pytz.timezone("America/New_York")


def out_dir() -> str:
    d = op.join(str(dcf.CACHE_DIR), "fomc")
    os.makedirs(d, exist_ok=True)
    return d


def find_first_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    cols = {c.lower(): c for c in df.columns}
    for name in candidates:
        if name in cols:
            return cols[name]
    # try pattern contains
    for c in df.columns:
        cl = c.lower()
        if any(name in cl for name in candidates):
            return c
    return None


def normalize_date(text: str, default_year: Optional[int] = None) -> Optional[str]:
    if pd.isna(text) or text is None:
        return None
    t = str(text).strip()
    try:
        dt = dtparser.parse(t, fuzzy=True, default=None)
    except Exception:
        if default_year and re.search(r"\b\d{1,2}\b", t):
            try:
                dt = dtparser.parse(f"{t} {default_year}", fuzzy=True, default=None)
            except Exception:
                return None
        else:
            return None
    if dt.tzinfo is None:
        dt = NY_TZ.localize(dt)
    else:
        dt = dt.astimezone(NY_TZ)
    return dt.date().isoformat()


def normalize_time(text: Optional[str]) -> str:
    if not text or pd.isna(text):
        return "14:00"
    t = str(text).strip()
    # remove timezone words and am/pm markers
    t = re.sub(r"\b(ET|EST|EDT|Eastern|p\.m\.|a\.m\.|PM|AM)\b", "", t, flags=re.I)
    t = t.replace("p.m.", "").replace("a.m.", "")
    t = re.sub(r"\s+", " ", t).strip()
    try:
        dt = dtparser.parse(t, fuzzy=True, default=dtparser.parse("14:00"))
        hhmm = f"{dt.hour:02d}:{dt.minute:02d}"
        return hhmm if ":" in t or dt.hour else "14:00"
    except Exception:
        return "14:00"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest manual FOMC dates CSV")
    parser.add_argument("--path", type=str, default="FOMC_Dates_1936.csv",
                        help="Path to the user-provided CSV (default: FOMC_Dates_1936.csv in repo root)")
    args = parser.parse_args()

    src_path = args.path
    if not op.isabs(src_path):
        # resolve relative to repo root (two levels up from this script)
        repo_dir = op.abspath(op.join(op.dirname(__file__), "..", "..", ".."))
        src_path = op.join(repo_dir, src_path)
    if not op.isfile(src_path):
        raise SystemExit(f"Input not found: {src_path}")

    df = pd.read_csv(src_path)
    # Identify columns heuristically
    ann_col = find_first_column(df, ["announcement_date", "announcement", "date", "statement", "decision"])
    start_col = find_first_column(df, ["start", "meeting_start", "begin", "began"])
    end_col = find_first_column(df, ["end", "meeting_end", "ended"])
    time_col = find_first_column(df, ["time", "statement_time", "release_time"])
    url_col = find_first_column(df, ["url", "statement_url", "press release", "link"])
    pc_col = find_first_column(df, ["press conference", "press_conf", "pc"])
    unsched_col = find_first_column(df, ["unscheduled", "emergency", "type", "notes"])
    minutes_col = find_first_column(df, ["minutes", "minutes_release", "minutes release date"]) 

    if not ann_col:
        raise SystemExit("Could not infer announcement_date column from the CSV. Please add a column named 'announcement_date' or 'date'.")

    # Normalize dates/times
    out = pd.DataFrame()
    out["announcement_date"] = df[ann_col].apply(lambda x: normalize_date(x))
    # derive year for start/end parsing if only month/day present
    years = pd.to_datetime(out["announcement_date"], errors="coerce").dt.year
    if start_col:
        out["meeting_start_date"] = [normalize_date(df[start_col].iloc[i], default_year=int(y) if not pd.isna(y) else None)
                                       for i, y in enumerate(years)]
    else:
        out["meeting_start_date"] = out["announcement_date"]
    if end_col:
        out["meeting_end_date"] = [normalize_date(df[end_col].iloc[i], default_year=int(y) if not pd.isna(y) else None)
                                     for i, y in enumerate(years)]
    else:
        out["meeting_end_date"] = out["announcement_date"]

    out["statement_time_eastern"] = df[time_col].apply(normalize_time) if time_col else "14:00"

    # Flags and URLs
    is_sched = []
    has_pc = []
    for i in range(len(df)):
        txt = " ".join(str(df[col].iloc[i]) for col in [unsched_col] if col)
        val = 0 if re.search(r"unscheduled|emergency", txt, re.I) else 1
        is_sched.append(val)
        pc_txt = str(df[pc_col].iloc[i]) if pc_col else ""
        has_pc.append(1 if re.search(r"press\s*conference|yes|true|1", pc_txt, re.I) else 0)
    out["is_scheduled"] = is_sched
    out["has_press_conference"] = has_pc

    out["statement_url"] = df[url_col].astype(str) if url_col else ""
    out["press_conf_url"] = ""
    out["minutes_release_date"] = df[minutes_col].apply(lambda x: normalize_date(x)) if minutes_col else ""

    # Filter to [MIN_DATE, MAX_DATE]
    ad = pd.to_datetime(out["announcement_date"], errors="coerce")
    mask = (ad >= pd.to_datetime(MIN_DATE)) & (ad <= pd.to_datetime(MAX_DATE))
    out = out[mask].copy()
    out.sort_values("announcement_date", inplace=True)

    # Deduplicate by announcement_date; keep row with explicit time or URL if duplicates exist
    def score_row(r: pd.Series) -> int:
        s = 0
        if isinstance(r.get("statement_url"), str) and r["statement_url"]:
            s += 2
        if r.get("statement_time_eastern") and r["statement_time_eastern"] != "14:00":
            s += 1
        return s
    if not out.empty:
        out["_s"] = out.apply(score_row, axis=1)
        out = out.sort_values(["announcement_date", "_s"], ascending=[True, False])
        out = out.drop_duplicates(subset=["announcement_date"], keep="first")
        out.drop(columns=["_s"], inplace=True, errors="ignore")

    # Write schedule and offsets
    outdir = out_dir()
    sched_path = op.join(outdir, "fomc_schedule.csv")
    out.to_csv(sched_path, index=False)
    print("Saved:", sched_path, "rows:", len(out))
    if len(out) > 0:
        print(out.head().to_string(index=False))
        print(out.tail().to_string(index=False))

    # Offsets
    b = pd.tseries.offsets.BDay()
    dt = pd.to_datetime(out["announcement_date"], errors="coerce")
    off = out.copy()
    off["t_minus_1"] = (dt - b).dt.date.astype(str)
    off["t_plus_1"] = (dt + b).dt.date.astype(str)
    off["t_plus_5"] = (dt + 5 * b).dt.date.astype(str)
    off["t_plus_20"] = (dt + 20 * b).dt.date.astype(str)
    off_path = op.join(outdir, "fomc_schedule_with_offsets.csv")
    off.to_csv(off_path, index=False)
    print("Saved:", off_path)


if __name__ == "__main__":
    main()


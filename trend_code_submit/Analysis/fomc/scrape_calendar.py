#!/usr/bin/env python3
from __future__ import annotations

"""
Scrape FOMC calendars (1992–2024‑12‑31) from the Federal Reserve website and write
two CSVs under CACHE_DIR/fomc/:
  - fomc_schedule.csv
  - fomc_schedule_with_offsets.csv

Run: cnn_env/bin/python trend_code_submit/Analysis/fomc/scrape_calendar.py
"""

import os
import re
import time
from typing import Dict, List, Optional, Tuple

import pandas as pd
import pytz
import requests
from bs4 import BeautifulSoup, Tag
from dateutil import parser as dtparser

# Project config for CACHE_DIR
from Data import dgp_config as dcf


ROOT_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)
NY_TZ = pytz.timezone("America/New_York")
MIN_YEAR = 1992
MAX_DATE = "2024-12-31"


def _out_dir() -> str:
    outdir = os.path.join(str(dcf.CACHE_DIR), "fomc")
    os.makedirs(outdir, exist_ok=True)
    return outdir


def fetch(url: str, tries: int = 3, backoff: float = 0.75) -> Optional[requests.Response]:
    for i in range(tries):
        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=20)
            if resp.status_code == 200:
                return resp
        except requests.RequestException:
            pass
        time.sleep(backoff * (2 ** i))
    return None


def abs_url(base: str, href: str) -> str:
    if not href:
        return ""
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("/"):
        return f"https://www.federalreserve.gov{href}"
    if base.endswith("/"):
        return base + href
    return base.rsplit("/", 1)[0] + "/" + href


def clean_text(x: str) -> str:
    return re.sub(r"\s+", " ", x).strip()


def _safe_soup(html: str) -> BeautifulSoup:
    """Parse with lxml, fall back to html.parser if structure seems empty."""
    soup = BeautifulSoup(html, "lxml")
    if not soup.find(["table", "ul", "ol", "section", "article", "div"]):
        soup = BeautifulSoup(html, "html.parser")
    return soup


def normalize_date(text: str, default_year: Optional[int] = None) -> Optional[str]:
    if not text:
        return None
    try:
        dt = dtparser.parse(text, fuzzy=True, default=None)
    except Exception:
        if default_year and re.search(r"\b\d{1,2}\b", text):
            try:
                dt = dtparser.parse(f"{text} {default_year}", fuzzy=True, default=None)
            except Exception:
                return None
        else:
            return None
    if dt.tzinfo is None:
        dt = NY_TZ.localize(dt)
    else:
        dt = dt.astimezone(NY_TZ)
    return dt.date().isoformat()


def normalize_time_eastern(text: Optional[str]) -> str:
    if not text:
        return "14:00"
    t = text.strip()
    t = re.sub(r"\b(ET|EST|EDT|Eastern|p\.m\.|a\.m\.|PM|AM)\b", "", t, flags=re.I)
    t = t.replace("p.m.", "").replace("a.m.", "")
    t = re.sub(r"\s+", " ", t).strip()
    try:
        dt = dtparser.parse(t, fuzzy=True, default=dtparser.parse("14:00"))
        return f"{dt.hour:02d}:{dt.minute:02d}" if ":" in t or dt.hour else "14:00"
    except Exception:
        return "14:00"


def split_date_range(text: str, year: int) -> Tuple[Optional[str], Optional[str]]:
    if not text:
        return None, None
    txt = clean_text(text)
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?(?:,\s*(\d{4}))?", txt)
    if not m:
        start = normalize_date(txt, default_year=year)
        return start, start
    month, d1, d2, y = m.groups()
    y = int(y) if y else year
    d1 = int(d1)
    d2 = int(d2) if d2 else d1
    start = normalize_date(f"{month} {d1} {y}", default_year=y)
    end = normalize_date(f"{month} {d2} {y}", default_year=y)
    return start, end


def extract_links(cells: List[Tag], base_url: str) -> Tuple[str, str, str]:
    statement_url = ""
    press_conf_url = ""
    minutes_url = ""
    for c in cells:
        for a in c.find_all("a", href=True):
            href = abs_url(base_url, a["href"])
            text = clean_text(a.get_text(" "))
            if re.search(r"statement|press release|policy statement", text, re.I):
                statement_url = statement_url or href
            elif re.search(r"press conference|Chair.*Press", text, re.I):
                press_conf_url = press_conf_url or href
            elif re.search(r"minutes", text, re.I):
                minutes_url = minutes_url or href
    return statement_url, press_conf_url, minutes_url


def parse_minutes_date(cells: List[Tag], default_year: int) -> Optional[str]:
    text = " ".join(clean_text(c.get_text(" ")) for c in cells)
    m = re.search(r"Minutes.*?(?:released\s*)?([A-Za-z]+\s+\d{1,2},?\s*\d{4})", text, re.I)
    if m:
        return normalize_date(m.group(1), default_year=default_year)
    m = re.search(r"([A-Za-z]+\s+\d{1,2},?\s*\d{4})", text)
    if m:
        return normalize_date(m.group(1), default_year=default_year)
    return None


def determine_time_and_flags(cells: List[Tag]) -> Tuple[str, int, int]:
    text = " ".join(clean_text(c.get_text(" ")) for c in cells)
    time_match = re.search(r"(\d{1,2}:?\d{0,2}\s*(?:a\.m\.|p\.m\.|AM|PM|ET|EST|EDT|Eastern))", text, re.I)
    stmt_time = normalize_time_eastern(time_match.group(1) if time_match else None)
    is_sched = 0 if re.search(r"unscheduled|emergency", text, re.I) else 1
    has_pc = 1 if re.search(r"press conference", text, re.I) else 0
    return stmt_time, is_sched, has_pc


def parse_year_tables(soup: BeautifulSoup, base_url: str, year: int) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []
    tables = soup.find_all("table")
    for tbl in tables:
        for tr in tbl.find_all("tr"):
            tds = tr.find_all(["td", "th"])  # headers may carry data on older pages
            if len(tds) < 2:
                continue
            row_text = " ".join(clean_text(td.get_text(" ")) for td in tds)
            if not re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\b", row_text):
                continue

            date_cell = clean_text(tds[0].get_text(" "))
            start_date, end_date = split_date_range(date_cell, year)
            announcement_date = end_date or start_date

            stmt_url, pc_url, _ = extract_links(tds, base_url)
            minutes_date = parse_minutes_date(tds, default_year=year)
            stmt_time, is_sched, has_pc = determine_time_and_flags(tds)

            if not (start_date or end_date or announcement_date):
                continue

            rec: Dict[str, str] = {
                "announcement_date": announcement_date or "",
                "meeting_start_date": start_date or announcement_date or "",
                "meeting_end_date": end_date or announcement_date or "",
                "statement_time_eastern": stmt_time,
                "is_scheduled": str(is_sched),
                "has_press_conference": str(has_pc),
                "statement_url": stmt_url,
                "press_conf_url": pc_url,
                "minutes_release_date": minutes_date or "",
            }
            records.append(rec)

    lists = soup.find_all(["ul", "ol"])
    for ul in lists:
        for li in ul.find_all("li", recursive=False):
            text = clean_text(li.get_text(" "))
            if not re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\b", text):
                continue
            start_date, end_date = split_date_range(text, year)
            announcement_date = end_date or start_date
            stmt_url, pc_url, _ = extract_links([li], base_url)
            minutes_date = parse_minutes_date([li], default_year=year)
            stmt_time, is_sched, has_pc = determine_time_and_flags([li])
            rec = {
                "announcement_date": announcement_date or "",
                "meeting_start_date": start_date or announcement_date or "",
                "meeting_end_date": end_date or announcement_date or "",
                "statement_time_eastern": stmt_time,
                "is_scheduled": str(is_sched),
                "has_press_conference": str(has_pc),
                "statement_url": stmt_url,
                "press_conf_url": pc_url,
                "minutes_release_date": minutes_date or "",
            }
            records.append(rec)

    return records


def find_years_and_pages(root_html: str, base_url: str) -> Dict[int, str]:
    """Prefer direct per-year URLs (fomccalendarsYYYY.htm). Fall back to root-discovered links."""
    year_to_url: Dict[int, str] = {}
    base_dir = "https://www.federalreserve.gov/monetarypolicy"
    for y in range(MIN_YEAR, int(MAX_DATE[:4]) + 1):
        year_to_url[y] = f"{base_dir}/fomccalendars{y}.htm"

    # Also include any links discovered on the root page as potential alternates
    soup = _safe_soup(root_html)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        label = clean_text(a.get_text(" "))
        ym = re.search(r"\b(19\d{2}|20\d{2})\b", label)
        if ym and re.search(r"fomc|calendar|schedule|meeting", href, re.I):
            y = int(ym.group(1))
            if MIN_YEAR <= y <= int(MAX_DATE[:4]):
                year_to_url[y] = abs_url(base_url, href)
    return year_to_url


def dedupe_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["announcement_date", "meeting_start_date", "meeting_end_date", "minutes_release_date"]:
        df[col] = df[col].astype(str).replace({"None": "", "nan": ""})
    df["statement_time_eastern"] = df["statement_time_eastern"].astype(str)
    for bcol in ["is_scheduled", "has_press_conference"]:
        df[bcol] = df[bcol].astype(int)

    def _rank_row(row: pd.Series) -> int:
        score = 0
        if row.get("statement_url"):
            score += 2
        if row.get("press_conf_url"):
            score += 1
        if row.get("statement_time_eastern") and row["statement_time_eastern"] != "14:00":
            score += 1
        return score

    if not df.empty:
        df["_score"] = df.apply(_rank_row, axis=1)
        df.sort_values(["announcement_date", "_score"], ascending=[True, False], inplace=True)
        df = df.drop_duplicates(subset=["announcement_date"], keep="first")
        df.drop(columns=["_score"], inplace=True, errors="ignore")
    return df


def validate(df: pd.DataFrame) -> None:
    sched = df[df["is_scheduled"] == 1].copy()
    for _, r in sched.iterrows():
        try:
            ad = pd.to_datetime(r["announcement_date"]).date()
            sd = pd.to_datetime(r["meeting_start_date"]).date() if r["meeting_start_date"] else ad
            ed = pd.to_datetime(r["meeting_end_date"]).date() if r["meeting_end_date"] else ad
            assert sd <= ad <= ed
        except Exception:
            pass
    assert not df["announcement_date"].duplicated().any(), "Duplicate announcement_date detected"


def main() -> None:
    outdir = _out_dir()
    root_resp = fetch(ROOT_URL)
    if not root_resp:
        raise SystemExit(f"Failed to fetch root page: {ROOT_URL}")

    year_to_url = find_years_and_pages(root_resp.text, ROOT_URL)
    records: List[Dict[str, str]] = []

    for year, url in sorted(year_to_url.items()):
        if year < MIN_YEAR or year > int(MAX_DATE[:4]):
            continue
        try:
            resp = fetch(url)
            if not resp:
                print(f"[WARN] Failed to fetch year {year} page: {url}")
                continue
            soup = _safe_soup(resp.text)
            recs = parse_year_tables(soup, url, year)
            if not recs and url != ROOT_URL:
                recs = parse_year_tables(_safe_soup(root_resp.text), ROOT_URL, year)
            for r in recs:
                ad = r.get("announcement_date") or ""
                try:
                    y = int(ad.split("-")[0]) if ad else 0
                except Exception:
                    y = 0
                if y < MIN_YEAR:
                    continue
                if ad and ad > MAX_DATE:
                    continue
                records.append(r)
        except Exception as e:
            print(f"[ERROR] Year {year}: {e}")
            continue

    cols = [
        "announcement_date",
        "meeting_start_date",
        "meeting_end_date",
        "statement_time_eastern",
        "is_scheduled",
        "has_press_conference",
        "statement_url",
        "press_conf_url",
        "minutes_release_date",
    ]
    df = pd.DataFrame.from_records(records, columns=cols)
    # Enforce bounds and clean
    if not df.empty:
        dt_ad = pd.to_datetime(df["announcement_date"], errors="coerce")
        mask = (dt_ad.dt.year >= MIN_YEAR) & (dt_ad <= pd.to_datetime(MAX_DATE))
        df = df[mask].copy()
    df = dedupe_and_enrich(df)
    df = df.sort_values("announcement_date").reset_index(drop=True)

    # Save schedule CSVs under CACHE_DIR/fomc/
    schedule_path = os.path.join(outdir, "fomc_schedule.csv")
    df.to_csv(schedule_path, index=False)
    print("Saved:", schedule_path)
    print(df.head())
    print(df.tail())

    # Offsets CSV
    dt = pd.to_datetime(df["announcement_date"]) ; b = pd.tseries.offsets.BDay()
    df2 = df.copy()
    df2["t_minus_1"] = (dt - b).dt.date.astype(str)
    df2["t_plus_1"] = (dt + b).dt.date.astype(str)
    df2["t_plus_5"] = (dt + 5 * b).dt.date.astype(str)
    df2["t_plus_20"] = (dt + 20 * b).dt.date.astype(str)
    offsets_path = os.path.join(outdir, "fomc_schedule_with_offsets.csv")
    df2.to_csv(offsets_path, index=False)
    print("Saved:", offsets_path)


if __name__ == "__main__":
    main()

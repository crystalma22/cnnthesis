#!/usr/bin/env python3
from __future__ import annotations

"""
Evaluate the weekly CNN up_prob against +1d / +3d / +10d realized returns (EW/VW H-L).

Reads:
  - CACHE_DIR/weekly_prediction_with_rets.csv (from make_prediction_with_rets.py)
  - processed_US_data() (us_ret.feather) for daily returns / cum_log_ret

Writes:
  - CACHE_DIR/horizon_eval.csv with columns: horizon, EW_HL, VW_HL

Run (from repo root):
  PYTHONPATH="$(pwd)/trend_code_submit" ./cnn_env/bin/python trend_code_submit/Analysis/horizon_eval.py
"""

import os
import numpy as np
import pandas as pd

from Data.equity_data import processed_US_data
from Data import dgp_config as dcf


def main() -> None:
    pred_path = os.path.join(dcf.CACHE_DIR, "weekly_prediction_with_rets.csv")
    if not os.path.isfile(pred_path):
        raise SystemExit(f"Missing {pred_path}. Run make_prediction_with_rets.py first.")

    pred = pd.read_csv(pred_path, parse_dates=["Date"]).sort_values(["StockID", "Date"])
    pred["StockID"] = pred["StockID"].astype(str)
    # Pick the weekly baseline column (I20/R5)
    up_col = "CNN20D5P" if "CNN20D5P" in pred.columns else None
    if up_col is None:
        cand = [c for c in pred.columns if c.startswith("CNN") and c.endswith("5P")]
        if not cand:
            raise SystemExit("No weekly up_prob column (CNN*5P) found in predictions CSV")
        up_col = cand[0]
    pred = pred[["Date", "StockID", up_col, "MarketCap"]].rename(columns={up_col: "up_prob"})

    # Load daily panel and (re)compute cum_log_ret if missing
    df = processed_US_data().copy()
    if "cum_log_ret" not in df.columns:
        df["log_ret"] = np.log1p(df["Ret"].astype(float))
        df["cum_log_ret"] = df.groupby(level="StockID")["log_ret"].cumsum(skipna=True)
        df.drop(columns=["log_ret"], inplace=True, errors="ignore")
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])  # ensure datetime

    def horizon_ret(k: int) -> pd.DataFrame:
        t = df[["Date", "StockID", "cum_log_ret"]].copy()
        t["cum_fwd"] = t.groupby("StockID")["cum_log_ret"].shift(-k)
        r = np.exp(t["cum_fwd"] - t["cum_log_ret"]) - 1
        return t[["Date", "StockID"]].assign(ret=r)

    r1 = horizon_ret(1).rename(columns={"ret": "ret_1d"})
    r3 = horizon_ret(3).rename(columns={"ret": "ret_3d"})
    r10 = horizon_ret(10).rename(columns={"ret": "ret_10d"})

    x = pred.merge(r1, on=["Date", "StockID"], how="left") \
            .merge(r3, on=["Date", "StockID"], how="left") \
            .merge(r10, on=["Date", "StockID"], how="left")

    def decile_hl(df: pd.DataFrame, ret_col: str) -> tuple[float, float]:
        d = df.dropna(subset=["up_prob", ret_col]).copy()
        if d.empty:
            return (np.nan, np.nan)
        # 10 deciles on up_prob
        d["decile"] = pd.qcut(d["up_prob"], 10, labels=False, duplicates="drop")
        ew = d.groupby("decile")[ret_col].mean().sort_index()
        if d["MarketCap"].notna().any():
            vw = d.groupby("decile").apply(lambda g: np.average(g[ret_col], weights=g["MarketCap"]))
            vw = vw.sort_index()
        else:
            vw = ew
        return (float(ew.iloc[-1] - ew.iloc[0]), float(vw.iloc[-1] - vw.iloc[0]))

    rows = []
    for rc, name in [("ret_1d", "1d"), ("ret_3d", "3d"), ("ret_10d", "10d")]:
        hl_ew, hl_vw = decile_hl(x, rc)
        rows.append({"horizon": name, "EW_HL": hl_ew, "VW_HL": hl_vw})

    out = pd.DataFrame(rows)
    out_path = os.path.join(dcf.CACHE_DIR, "horizon_eval.csv")
    out.to_csv(out_path, index=False)
    print("Saved:", out_path)
    print(out)


if __name__ == "__main__":
    main()


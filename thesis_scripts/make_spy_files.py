import os
import sys
import pandas as pd


def main():
    base = os.path.join(os.path.dirname(__file__), "CACHE_DIR")
    src = os.path.join(base, "spy_daily_ret.csv")
    if not os.path.isfile(src):
        print(f"Input not found: {src}")
        sys.exit(1)

    df = pd.read_csv(src)
    df.columns = [c.lower() for c in df.columns]

    if "caldt" in df.columns:
        df["date"] = pd.to_datetime(df["caldt"])
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    else:
        raise ValueError("spy_daily_ret.csv must have 'caldt' or 'date' column")

    ew_col = "ewretx" if "ewretx" in df.columns else "ewretd" if "ewretd" in df.columns else None
    vw_col = "vwretx" if "vwretx" in df.columns else "vwretd" if "vwretd" in df.columns else None
    if ew_col is None or vw_col is None:
        raise ValueError("spy_daily_ret.csv must contain ewretx/vwretx (or ewretd/vwretd)")

    daily = df[["date", ew_col, vw_col]].sort_values("date").set_index("date")

    def periodize(rule: str, out_name: str):
        agg = daily.resample(rule).apply(lambda x: (1.0 + x).prod() - 1.0)
        out = agg.rename(columns={ew_col: "ewretx", vw_col: "vwretx"}).reset_index()
        out["nxt_freq_ewret"] = out["ewretx"].shift(-1)
        out["nxt_freq_vwret"] = out["vwretx"].shift(-1)
        dst = os.path.join(base, out_name)
        out.to_csv(dst, index=False)
        print(
            f"Wrote {out_name}: {out['date'].min().date()} -> {out['date'].max().date()} (rows={len(out)})"
        )

    periodize("W-FRI", "spy_week_ret.csv")
    periodize("M", "spy_month_ret.csv")
    periodize("Q-DEC", "spy_quarter_ret.csv")


if __name__ == "__main__":
    main()


import os
import sys
import pandas as pd


def main():
    # Ensure we can import project modules
    repo_dir = os.path.dirname(__file__)
    code_dir = os.path.join(repo_dir, "trend_code_submit")
    # Ensure relative paths in Misc.config (e.g., "../WORK_SPACE") resolve correctly
    os.chdir(code_dir)
    sys.path.insert(0, code_dir)

    from Data.equity_data import processed_US_data
    from Data import dgp_config as dcf

    df = processed_US_data()
    # We only need period-end rows where Ret_{freq} is defined, plus MarketCap
    freq_map = {"week": "W-FRI", "month": "M", "quarter": "Q-DEC"}
    for freq in ["week", "month", "quarter"]:
        col = f"Ret_{freq}"
        sub = df[["MarketCap", col]].copy()
        sub = sub[~sub[col].isna()].copy()
        sub = sub.rename(columns={col: f"next_{freq}_ret_0delay"})
        # Provide a non-delayed alias as in sample parquet (not used by code but harmless)
        sub[f"next_{freq}_ret"] = sub[f"next_{freq}_ret_0delay"]
        # Save parquet with Date/StockID as columns (the loader will set them as index)
        out = sub.reset_index()
        save_path = os.path.join(dcf.CACHE_DIR, f"us_{freq}_ret.pq")
        out.to_parquet(save_path, index=False)
        print(f"Wrote {save_path}: rows={len(out)} range={out['Date'].min().date()} -> {out['Date'].max().date()}")


if __name__ == "__main__":
    main()

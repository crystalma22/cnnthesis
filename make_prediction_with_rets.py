import os
import sys
import pandas as pd


def build_prediction_with_rets():
    repo_dir = os.path.dirname(__file__)
    code_dir = os.path.join(repo_dir, "trend_code_submit")
    os.chdir(code_dir)
    sys.path.insert(0, code_dir)

    # Imports from project
    from Experiments.cnn_experiment import get_bl_exp_obj
    from Data import dgp_config as dcf
    import numpy as np

    # Map predict window to frequency label/file names
    freq_map = {5: "week", 20: "month", 60: "quarter"}

    # Restrict to the model(s) you have trained on this machine.
    # Option A: weekly I20/R5 only.
    pw_list = [5]

    for pw in pw_list:
        freq = freq_map[pw]
        # Load ensemble OOS predictions for ws in [5,20,60]
        up_prob_cols = {}
        market_cap = None
        index = None
        # Weekly baseline: 20‑day input window only
        for ws in [20]:
            # Use the same lr as your trained checkpoints and aggregate full ensemble
            exp = get_bl_exp_obj(ws=ws, pw=pw, lr=1e-4, ensem=5)
            # Load OOS ensemble results across years (must have been trained)
            df = exp.load_ensem_res(year=exp.oos_years, multiindex=True, freq=freq)
            # Ensure consistent index and columns
            df.index.names = ["Date", "StockID"]
            df = df.sort_index()
            col_name = f"CNN{ws}D{pw}P"
            up_prob_cols[col_name] = df["up_prob"].astype(float)
            # Capture MarketCap once
            if market_cap is None:
                market_cap = df["MarketCap"].astype(float)
                index = df.index

        # Build combined frame
        res = pd.DataFrame(index=index)
        res["MarketCap"] = market_cap
        for k, v in up_prob_cols.items():
            res[k] = v.reindex(index)

        # Join future returns for convenience (with_rets)
        try:
            from Data import equity_data as eqd
            period_ret = eqd.get_period_ret(freq, country="USA")
        except Exception:
            from Portfolio.portfolio import PortfolioManager
            # Reuse PortfolioManager's fallback to compute if parquet missing
            pm = get_bl_exp_obj(ws=20, pw=pw, lr=1e-4, ensem=5).load_portfolio_obj(load_signal=False)
            period_ret = pm._load_period_returns_with_fallback()
        period_ret = period_ret[[f"next_{freq}_ret_0delay"]]
        res = res.join(period_ret, how="left")

        # Save to CACHE_DIR/{freq}ly_prediction_with_rets.csv
        out_path = os.path.join(dcf.CACHE_DIR, f"{freq}ly_prediction_with_rets.csv")
        res.reset_index().to_csv(out_path, index=False)
        print(f"Wrote {out_path} with shape {res.shape}")


if __name__ == "__main__":
    build_prediction_with_rets()

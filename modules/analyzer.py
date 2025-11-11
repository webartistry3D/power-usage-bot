# handles consumption calculations

import pandas as pd

def analyze_usage(file_path="data/usage_log.csv"):
    df = pd.read_csv(file_path, names=["date", "units_start", "units_end", "usage"])
    avg_usage = df["usage"].tail(7).mean()
    balance = df["units_end"].iloc[-1]
    days_left = balance / avg_usage if avg_usage else 0

    summary = {
        "average_usage": round(avg_usage, 2),
        "balance": round(balance, 2),
        "days_left": round(days_left, 1)
    }
    return summary

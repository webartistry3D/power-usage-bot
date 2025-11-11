# handles fetching or simulating usage data

import pandas as pd
import random
import datetime
from config.settings import DISCO_API_URL, METER_ID

def fetch_usage_data():
    """Simulates fetching data from DisCo or API"""
    today = datetime.date.today()
    units_start = random.uniform(50, 100)
    units_end = units_start - random.uniform(1.5, 5.0)  # simulate usage

    entry = {
        "date": today,
        "units_start": round(units_start, 2),
        "units_end": round(units_end, 2),
        "usage": round(units_start - units_end, 2)
    }

    df = pd.DataFrame([entry])
    df.to_csv("data/usage_log.csv", mode="a", index=False, header=False)
    return entry

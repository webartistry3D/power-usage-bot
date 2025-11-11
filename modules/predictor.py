# ML-based forecasting

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle
import os

MODEL_PATH = "data/model.pkl"
DATA_PATH = "data/usage_log.csv"

def train_model(file_path=DATA_PATH):
    if not os.path.exists(file_path):
        print(f"CSV file not found: {file_path}")
        return None

    df = pd.read_csv(file_path, names=["date", "units_start", "units_end", "usage"])
    
    if df.empty:
        print("No data available to train the model.")
        return None

    X = np.arange(len(df)).reshape(-1, 1)
    y = df["usage"].values

    if len(X) == 0 or len(y) == 0:
        print("No valid rows for training.")
        return None

    model = LinearRegression().fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Model trained successfully.")
    return model


def predict_next_day_usage():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Train the model first.")
        return None

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    if not os.path.exists(DATA_PATH):
        print(f"CSV file not found: {DATA_PATH}")
        return None

    df = pd.read_csv(DATA_PATH, names=["date", "units_start", "units_end", "usage"])

    if df.empty:
        print("No data available to make predictions.")
        return None

    next_day = np.array([[len(df)]])
    prediction = model.predict(next_day)[0]
    return round(prediction, 2)

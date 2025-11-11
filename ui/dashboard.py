import sys
import os

# Add the project root folder to the Python path BEFORE importing modules
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import streamlit as st
import pandas as pd
import datetime
from modules.analyzer import analyze_usage
from modules.predictor import predict_next_day_usage, train_model
from modules.data_collector import fetch_usage_data

# --- Paths ---
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "usage_log.csv")

# --- Page Config ---
st.set_page_config(
    page_title="PowerPal ⚡",
    page_icon="🔋",
    layout="wide"
)

# --- Title Section ---
st.title("⚡ PowerUsage Dashboard")
st.markdown("### _Monitor your power usage, track your balance, and predict when your units will finish._")

# --- Check if data exists ---
if not os.path.exists(DATA_PATH):
    st.warning("No data found. Click **Generate Sample Data** to begin tracking.")
    if st.button("Generate Sample Data"):
        for _ in range(10):
            fetch_usage_data()
        st.success("✅ Sample data generated. Refresh to view.")
    st.stop()

# --- Load Data ---
df = pd.read_csv(DATA_PATH, names=["date", "units_start", "units_end", "usage"])
df["date"] = pd.to_datetime(df["date"])

# --- Train model on load ---
model = train_model()
prediction = None
summary = None

if model is not None:
    prediction = predict_next_day_usage()
    summary = analyze_usage()

# --- Safeguard summary values ---
summary_safe = {
    "balance": summary.get("balance", 0) if summary else 0,
    "average_usage": summary.get("average_usage", 0) if summary else 0,
    "days_left": summary.get("days_left", 0) if summary else 0
}

# --- Layout Sections ---
col1, col2, col3 = st.columns(3)
col1.metric("💡 Current Balance", f"{summary_safe['balance']} units")
col2.metric("📉 Avg Daily Usage", f"{summary_safe['average_usage']} units/day")
col3.metric("🕒 Estimated Days Left", f"{summary_safe['days_left']} days")

st.divider()

# --- Consumption History Chart ---
st.subheader("📊 Power Consumption History")
st.line_chart(df, x="date", y="usage", use_container_width=True)

st.markdown(f"🔮 **Predicted Next-Day Usage:** {prediction if prediction is not None else 'N/A'} units")

st.divider()

# --- Usage Insights ---
total_week = df.tail(7)["usage"].sum()
total_month = df.tail(30)["usage"].sum() if len(df) >= 30 else df["usage"].sum()

col4, col5 = st.columns(2)
col4.metric("This Week’s Total Usage", f"{round(total_week, 2)} units")
col5.metric("This Month’s Total Usage", f"{round(total_month, 2)} units")

st.divider()

# --- Manual Entry Section ---
st.subheader("🧭 Add Meter Reading")
with st.form("manual_entry"):
    units_start = st.number_input("Units at Start of Day", min_value=0.0, step=0.1)
    units_end = st.number_input("Units at End of Day", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        if units_start > units_end:
            new_entry = {
                "date": datetime.date.today(),
                "units_start": round(units_start, 2),
                "units_end": round(units_end, 2),
                "usage": round(units_start - units_end, 2)
            }
            pd.DataFrame([new_entry]).to_csv(DATA_PATH, mode="a", index=False, header=False)
            st.success("✅ Entry added successfully! Refresh to update dashboard.")
        else:
            st.error("⚠️ 'Units start' must be greater than 'units end'.")

st.markdown(
    """
    <p style='text-align:center;'>
    Built with 💚 using Python | © 2025 PowerUsageBot.<br>
    🔌 Powered by Webartistry Creations®
    </p>
    """,
    unsafe_allow_html=True
)

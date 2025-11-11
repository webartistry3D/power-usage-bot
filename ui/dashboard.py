# ui/dashboard.py
import sys
import os
import json
import datetime

# --- Project root & module path (must be before importing your modules) ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import streamlit as st
import pandas as pd
from modules.analyzer import analyze_usage
from modules.predictor import predict_next_day_usage, train_model
from modules.data_collector import fetch_usage_data

# --- Paths ---
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "usage_log.csv")

# --- Streamlit page config ---
st.set_page_config(
    page_title="PowerUsage ⚡ — Neon",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Inject Cyberpunk CSS (neon gradients, glass cards, animations) ---
st.markdown(
    """
    <style>
    :root{
      --bg:#05030a;
      --glass: rgba(255,255,255,0.03);
      --neon-1: #00e6ff;
      --neon-2: #ff00d0;
      --accent: linear-gradient(90deg,var(--neon-1),var(--neon-2));
      --card-shadow: 0 6px 30px rgba(0,0,0,0.6);
    }
    html, body, [class*="css"]  {
      background: radial-gradient(circle at 10% 10%, rgba(0,230,255,0.06), transparent 10%),
                  radial-gradient(circle at 90% 90%, rgba(255,0,208,0.06), transparent 10%),
                  var(--bg) !important;
      color: #e6f7ff;
    }
    .neon-title{
      font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial;
      font-weight:700;
      font-size:34px;
      letter-spacing:1px;
      background: -webkit-linear-gradient(90deg, #00e6ff, #ff00d0);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 10px rgba(0,230,255,0.06);
    }
    .subtle{
      color: #a7cfe6;
    }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.03);
      border-radius: 14px;
      padding: 18px;
      box-shadow: var(--card-shadow);
      transition: transform .18s ease, box-shadow .18s ease;
    }
    .card:hover { transform: translateY(-6px); box-shadow: 0 18px 40px rgba(0,0,0,0.75); }
    .neon-card {
      border-left: 4px solid transparent;
      background-image: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)), 
                        linear-gradient(90deg, rgba(0,230,255,0.08), rgba(255,0,208,0.06));
      background-origin: border-box;
      background-clip: padding-box, border-box;
    }
    .metric-value { font-size: 20px; font-weight:700; color: #e6f7ff; }
    .muted { color: #9fbcd6; font-size:12px; }
    .sparkline { height:48px; }
    /* subtle animated glow line */
    .glow-line {
      height: 4px;
      border-radius: 8px;
      background: linear-gradient(90deg, rgba(0,230,255,0.25), rgba(255,0,208,0.25));
      box-shadow: 0 6px 20px rgba(0,230,255,0.06), 0 6px 20px rgba(255,0,208,0.03);
      animation: slide 3s linear infinite;
      background-size: 200% 100%;
    }
    @keyframes slide { 0% { background-position:0% 50%; } 100% { background-position:100% 50%; } }
    /* small help text */
    .help-box { font-size:12px; color:#8fb6d6; margin-top:6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header / Title (neon) ---
st.markdown('<div style="display:flex;align-items:center;gap:18px;">'
            '<div style="width:56px;height:56px;border-radius:12px;background:linear-gradient(135deg,#00e6ff,#ff00d0);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 30px rgba(255,0,208,0.08);">'
            '<span style="font-weight:800;color:#05030a;">⚡</span></div>'
            f'<div><div class="neon-title">PowerUsage — Neon</div><div class="subtle">Smart prepaid meter monitoring · predictions · alerts</div></div></div>',
            unsafe_allow_html=True)

st.write("")  # spacing

# --- Load or create DataFrame with defaults (all zeros by default) ---
def load_or_create_dataframe(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df0 = pd.DataFrame([{
            "date": datetime.date.today(),
            "units_start": 0.0,
            "units_end": 0.0,
            "usage": 0.0
        }])
        df0.to_csv(path, index=False, header=False)
        return df0
    else:
        df = pd.read_csv(path, names=["date", "units_start", "units_end", "usage"])
        if df.empty:
            return pd.DataFrame([{
                "date": datetime.date.today(),
                "units_start": 0.0,
                "units_end": 0.0,
                "usage": 0.0
            }])
        df["date"] = pd.to_datetime(df["date"], errors="coerce").fillna(pd.Timestamp(datetime.date.today()))
        return df

df = load_or_create_dataframe(DATA_PATH)

# --- Safe model/prediction (do not raise) ---
try:
    model = train_model()
except Exception:
    model = None

try:
    prediction = predict_next_day_usage() if model is not None else 0
except Exception:
    prediction = 0

try:
    summary = analyze_usage()
except Exception:
    summary = {"balance": 0, "average_usage": 0, "days_left": 0}

# Ensure numeric defaults
balance = float(summary.get("balance", 0) or 0)
avg_usage = float(summary.get("average_usage", 0) or 0)
days_left = float(summary.get("days_left", 0) or 0)
prediction = float(prediction or 0)

# --- Top cards (neon) ---
c1, c2, c3, c4 = st.columns([1.6,1,1,0.6], gap="large")

with c1:
    st.markdown('<div class="card neon-card">'
                '<div style="display:flex;justify-content:space-between;align-items:center;">'
                '<div><div style="font-size:13px;color:#9fbcd6">CURRENT BALANCE</div>'
                f'<div style="font-size:28px;font-weight:800;margin-top:6px;">{balance:,.2f} <span style="font-size:14px;color:#9fbcd6">units</span></div>'
                '</div>'
                '<div style="text-align:right;">'
                '<div style="font-size:12px;color:#a7cfe6">Predicted →</div>'
                f'<div style="font-size:18px;font-weight:700;color:#00e6ff">{prediction:.2f}</div>'
                '</div></div>'
                '<div style="margin-top:10px;"><div class="glow-line"></div></div>'
                '</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">'
                '<div style="font-size:12px;color:#9fbcd6">AVG DAILY USAGE</div>'
                f'<div style="font-size:22px;font-weight:800;margin-top:8px;">{avg_usage:.2f} <span style="font-size:12px;color:#9fbcd6">units/day</span></div>'
                '<div class="help-box">Average of recent usage — used to estimate days left.</div>'
                '</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">'
                '<div style="font-size:12px;color:#9fbcd6">ESTIMATED DAYS LEFT</div>'
                f'<div style="font-size:22px;font-weight:800;margin-top:8px;">{days_left:.1f} <span style="font-size:12px;color:#9fbcd6">days</span></div>'
                '<div class="help-box">Balance ÷ Avg daily usage</div>'
                '</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card" style="text-align:center;padding-top:16px;padding-bottom:16px;">'
                '<div style="font-size:12px;color:#9fbcd6">SYSTEM</div>'
                '<div style="font-size:20px;font-weight:800;margin-top:6px;color:#ff00d0">ONLINE</div>'
                '<div style="font-size:11px;color:#9fbcd6;margin-top:6px">Last sync</div>'
                f'<div style="font-size:12px;color:#9fbcd6">{pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}</div>'
                '</div>', unsafe_allow_html=True)

st.write("")  # spacing

# --- Main layout: chart (big), table (right) ---
chart_col, right_col = st.columns([2.2,1], gap="large")

with chart_col:
    st.markdown('<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;"><div>'
                '<div style="font-weight:700">Consumption History</div>'
                '<div style="font-size:12px;color:#9fbcd6">Daily usage over time</div>'
                '</div>'
                '<div style="font-size:12px;color:#9fbcd6">Live · Streaming</div>'
                '</div><div style="margin-top:10px;">', unsafe_allow_html=True)

    # Use Streamlit's line_chart for simplicity and stable dependencies
    st.line_chart(df.set_index("date")["usage"])

    st.markdown('</div></div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card"><div style="font-weight:700">Recent Readings</div>'
                '<div style="font-size:12px;color:#9fbcd6;margin-top:6px">Latest meter entries</div>', unsafe_allow_html=True)

    # show recent rows in a compact table
    recent = df.copy().tail(8).reset_index(drop=True)
    recent["date"] = recent["date"].dt.strftime("%Y-%m-%d")
    st.table(recent.rename(columns={
        "date": "Date",
        "units_start": "Start",
        "units_end": "End",
        "usage": "Usage"
    }))

    st.markdown('<div style="margin-top:10px;" class="muted">Tip: Click "Add Meter Reading" to append today\'s usage.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")  # spacing

# --- Manual Entry Section ---
st.subheader("🧭 Add Meter Reading")

# Use session_state to trigger automatic update if needed
if "manual_update" not in st.session_state:
    st.session_state.manual_update = False

with st.form("manual_entry", clear_on_submit=True):
    units_start = st.number_input("Units at Start of Day", min_value=0.0, step=0.1)
    units_end = st.number_input("Units at End of Day", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        if units_start > units_end:
            usage = round(units_start - units_end, 2)
            # Make sure 'date' is a proper datetime
            new_entry = pd.DataFrame([{
                "date": pd.Timestamp.today(),
                "units_start": round(units_start, 2),
                "units_end": round(units_end, 2),
                "usage": usage
            }])

            # Append to CSV
            new_entry.to_csv(DATA_PATH, mode="a", index=False, header=False)

            # Update in-memory dataframe
            df = pd.concat([df, new_entry], ignore_index=True)

            # Toggle session_state to trigger rerun-like behavior
            st.session_state.manual_update = not st.session_state.manual_update

            # Temporary success message
            msg_placeholder = st.empty()
            msg_placeholder.success(f"✅ Added: {usage} units used today.")
        else:
            st.error("⚠️ 'Units at Start' must be greater than 'Units at End'.")



st.markdown('</div>', unsafe_allow_html=True)

# --- Scroll to Top Arrow ---
st.markdown(
    """
    <div style="position:fixed;bottom:20px;right:20px;z-index:999;">
        <a href="/" onclick="window.scrollTo({top: 0, behavior: 'smooth'});" 
           style="text-decoration:none;font-size:32px;color:#00e6ff;">
            ⬆️
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


# --- Footer / Credits (small neon) ---
st.markdown(
    f"""
    <div style="margin-top:18px;text-align:center;color:#8fb6d6;font-size:12px;">
      Built with 💚 | © 2025 PowerUsageBot · Webartistry Creations® · <span style="color:#00e6ff">Neon UI</span>
    </div>
    """,
    unsafe_allow_html=True
)

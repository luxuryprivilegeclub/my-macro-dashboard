import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go

# Title and Branding
st.set_page_config(page_title="Macro Dashboard", layout="wide")
st.title("📊 Live Economic Dashboard")
st.markdown("Developed for **Rollic Trades**")

# API Setup
API_KEY = "7907dc084d9aa52bbe59276c20691708" # <--- Apni key yahan likhein
fred = Fred(api_key=API_KEY)

# Indicators to track
indicators = {
    'CPI (Inflation)': 'CPIAUCSL',
    'NFP (Jobs)': 'PAYEMS',
    'Unemployment Rate': 'UNRATE',
    'Fed Interest Rate': 'FEDFUNDS'
}

# 2-Column Layout
col1, col2 = st.columns(2)

for i, (name, s_id) in enumerate(indicators.items()):
    data = fred.get_series(s_id)
    latest = data.iloc[-1]
    previous = data.iloc[-2]
    
    # Logic for DXY Impact
    if name == 'CPI (Inflation)':
        msg, bias, color = ("Inflation up hai.", "DXY: BULLISH", "red") if latest > previous else ("Inflation down hai.", "DXY: BEARISH", "green")
    elif name == 'NFP (Jobs)':
        msg, bias, color = ("Strong Jobs Data.", "DXY: BULLISH", "green") if latest > previous else ("Weak Jobs Data.", "DXY: BEARISH", "red")
    else:
        msg, bias, color = ("Data updated.", "Check Trend", "blue")

    # Display in Columns
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest,
            title = {'text': name},
            gauge = {'bar': {'color': color}}
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"**Analysis:** {msg} | **Impact:** {bias}")

import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades | Macro & COT Terminal", layout="wide")

# 2. Centered Logo
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{logo_url}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

# 3. Professional Header
st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
    <h1 style="margin: 0; font-family: 'Arial Black', sans-serif;">ROLLIC TRADES MACRO & COT TERMINAL</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Grade Analysis | 2026 Trader Edition</p>
</div>""", unsafe_allow_html=True)

# 4. API Setup
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except:
    st.error("API Key missing! Check Streamlit Secrets.")
    st.stop()

# --- Helper Function to Keep UI Consistent ---
def draw_meter(col, name, latest, prev, info_next, msg, dxy_b, gold_b, color, bg, height=260):
    with col:
        # Meter Title with spacing
        st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -35px; color: #000; font-size: 16px;'>{name}</p>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, gauge={'bar': {'color': color}}))
        fig.update_layout(height=height, margin=dict(l=30, r=30, t=55, b=0))
        st.plotly_chart(fig, use_container_width=True)
        # Analysis Box
        st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:12px; border-radius:12px; text-align:center; margin:-35px auto 35px auto; max-width: 290px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <p style="margin:0; font-size:12px; font-weight:500; color:#333;">{msg}</p>
            <div style="margin-top:8px;">
                <span style="background:#1e3c72; color:white; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{dxy_b}</span>
                <span style="background:#d4af37; color:black; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{gold_b}</span>
            </div>
            <p style="margin-top:10px; color:#000; font-size:11px; font-weight:bold;">📅 Next: {info_next}</p>
        </div>""", unsafe_allow_html=True)

# --- SECTION 1: PRIMARY MACRO (2 Columns) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📌 Primary Gold & DXY Drivers</h2>", unsafe_allow_html=True)
cols1 = st.columns(2)
main_ind = {
    'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'},
    'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'},
    'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'},
    'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'}
}
for i, (name, info) in enumerate(main_ind.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388

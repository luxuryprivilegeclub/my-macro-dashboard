import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades Macro Terminal", layout="wide")

# 2. Logo Section
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{logo_url}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

# 3. Professional Header
st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
    <h1 style="margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 1px;">ROLLIC TRADES MACRO TERMINAL</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Smart Money Concept & Macro Sentiment Analysis | 2026 Pro Version</p>
</div>""", unsafe_allow_html=True)

# 4. API Setup
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except:
    st.error("API Key missing in Streamlit Secrets!")
    st.stop()

# --- DATA STRUCTURES ---
main_indicators = {
    'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'},
    'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'},
    'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'},
    'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'}
}

liquidity_indicators = {
    'PCE Inflation (Fed Fav)': {'id': 'PCEPI', 'next': 'Feb 27, 2026'},
    'M2 Money Supply': {'id': 'WM2NS', 'next': 'Weekly (Tuesday)'},
    'Yield Curve (10Y-2Y)': {'id': 'T10Y2Y', 'next': 'Daily'},
    'Consumer Sentiment': {'id': 'UMCSENT', 'next': 'Feb 20, 2026'}
}

yield_indicators = {
    'US 10Y Yield': {'id': 'DGS10', 'next': 'Daily'},
    '10Y Breakeven': {'id': 'T10YIE', 'next': 'Daily'},
    'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}
}

# --- HELPER FUNCTION FOR METERS ---
def create_meter(name, latest, previous, color, next_date, msg, bias, bg, col_obj, size=220):
    with col_obj:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 16}}, gauge={'bar': {'color': color}}))
        fig.update_layout(height=size, margin=dict(l=20, r=20, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:10px; border-radius:12px; text-align:center; margin: -20px auto 30px auto; max-width: 320px;">
            <p style="margin:0; font-size:12px; color: #444; font-weight: 500;">{msg}</p>
            <div style="background:{color}; color:white; padding:2px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block; margin-top:5px;">{bias}</div>
            <p style="margin-top:8px; color:#000000; font-size:11px; font-weight:bold;">📅 Next: {next_date}</p>
        </div>""", unsafe_allow_html=True)

# --- SECTION 1: KEY ECONOMIC INDICATORS ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📌 Primary Macro Indicators</h2>", unsafe_allow_html=True)
cols1 = st.columns(2)
for i, (name, info) in enumerate(main_indicators.items()):
    data = fred.get_series(info['id'])
    latest, prev = data.iloc[-1], data.iloc[-2]
    if 'CPI' in name or 'NFP' in name:
        color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
        msg = "Inflation barh rahi hai" if 'CPI' in name and latest > prev else "Jobs strong hain"
        bias = "DXY: BULLISH" if latest > prev else "DXY: BEARISH"
    else:
        color, bg, msg, bias = ("#1976d2", "#e3f2fd", "Fed policy data updated.", "Neutral/Trend")
    create_meter(name, latest, prev, color, info['next'], msg, bias, bg, cols1[i%2])

st.markdown("---")

# --- SECTION 2: ADVANCED LIQUIDITY & POLICY ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🌊 Liquidity & Recession Risk</h2>", unsafe_allow_html=True)
cols2 = st.columns(4)
for i, (name, info) in enumerate(liquidity_indicators.items()):
    data = fred.get_series(info['id'])
    latest, prev = data.iloc[-1], data.iloc[-2]
    
    # Logic for Inversion & Liquidity
    if 'Yield Curve' in name:
        color, bias = ("#d32f2f", "Recession Risk") if latest < 0 else ("#388e3c", "Normal")
        msg = "Curve Inverted!" if latest < 0 else "Curve Healthy"
    elif 'M2' in name:
        color, bias = ("#1976d2", "Bullish Assets") if latest > prev else ("#fb8c00", "Tight Liquidity")
        msg = "Money Printing Up" if latest > prev else "Liquidity Drying"
    else:
        color, bias, msg = ("#455a64", "Sentiment Check", "Data Updated")
        
    create_meter(name, latest, prev, color, info['next'], msg, bias, "#fafafa", cols2[i], size=160)

st.markdown("---")

# --- SECTION 3: MARKET SENTIMENT & YIELDS ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📊 Yields & Target Tracking</h2>", unsafe_allow_html=True)
cols3 = st.columns(4)
for i, (name, info) in enumerate(yield_indicators.items()):
    data = fred.get_series(info['id'])
    latest, prev = data.iloc[-1], data.iloc[-2]
    color = "#1565c0" if latest > prev else "#fb8c00"
    create_meter(name, latest, prev, color, info['next'], "Yields trend follow karein", "USD Driver", "#fafafa", cols3[i], size=160)

# 4th Meter: Fed Target
cpi_data = fred.get_series('CPIAUCSL')
curr_inf = ((cpi_data.iloc[-1] - cpi_data.iloc[-13]) / cpi_data.iloc[-13]) * 100
create_meter("Inf. vs 2% Target", curr_inf, 2.0, "red" if curr_inf > 2 else "green", "Feb 13", f"Gap: {curr_inf-2:.2f}% Over", "Hawkish Fed", "#fafafa", cols3[3], size=160)

# Footer
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

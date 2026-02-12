import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades | Gold & Macro Terminal", layout="wide")

# 2. Logo Section
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{logo_url}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

# 3. Professional Header
st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
    <h1 style="margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 1px;">ROLLIC TRADES GOLD TERMINAL</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">XAUUSD Sentiment & Macro Analysis | SMC/ICT Logic</p>
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
    'PCE Inflation': {'id': 'PCEPI', 'next': 'Feb 27, 2026'},
    'M2 Money Supply': {'id': 'WM2NS', 'next': 'Weekly'},
    'Yield Curve (10Y-2Y)': {'id': 'T10Y2Y', 'next': 'Daily'},
    'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}
}

# --- HELPER FUNCTION FOR METERS ---
def create_meter(name, latest, previous, color, next_date, msg, dxy_bias, gold_bias, bg, col_obj, size=220):
    with col_obj:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 16}}, gauge={'bar': {'color': color}}))
        fig.update_layout(height=size, margin=dict(l=20, r=20, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:10px; border-radius:12px; text-align:center; margin: -20px auto 30px auto; max-width: 320px;">
            <p style="margin:0; font-size:12px; color: #444; font-weight: 500;">{msg}</p>
            <div style="background:#1e3c72; color:white; padding:2px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block; margin-top:5px;">{dxy_bias}</div>
            <div style="background:#d4af37; color:black; padding:2px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block; margin-top:5px;">{gold_bias}</div>
            <p style="margin-top:8px; color:#000000; font-size:11px; font-weight:bold;">📅 Next: {next_date}</p>
        </div>""", unsafe_allow_html=True)

# --- SECTION 1: PRIMARY MACRO (GOLD IMPACT) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📌 Primary Gold Drivers</h2>", unsafe_allow_html=True)
cols1 = st.columns(2)
for i, (name, info) in enumerate(main_indicators.items()):
    data = fred.get_series(info['id'])
    latest, prev = data.iloc[-1], data.iloc[-2]
    
    if 'CPI' in name:
        color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
        msg = "Inflation high hai, Fed rates barha sakta hai." if latest > prev else "Inflation cooling hai."
        dxy_bias = "DXY: BULLISH" if latest > prev else "DXY: BEARISH"
        gold_bias = "GOLD: BEARISH" if latest > prev else "GOLD: BULLISH"
    elif 'NFP' in name:
        color, bg = ("#388e3c", "#f1f8e9") if latest > prev else ("#d32f2f", "#fff5f5")
        msg = "Jobs data strong hai, economy stable hai." if latest > prev else "Jobs market weak hai."
        dxy_bias = "DXY: BULLISH" if latest > prev else "DXY: BEARISH"
        gold_bias = "GOLD: BEARISH" if latest > prev else "GOLD: BULLISH"
    elif 'Unemployment' in name:
        color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
        msg = "Berozgari barh rahi hai." if latest > prev else "Berozgari kam hai."
        dxy_bias = "DXY: BEARISH" if latest > prev else "DXY: BULLISH"
        gold_bias = "GOLD: BULLISH" if latest > prev else "GOLD: BEARISH"
    else: # Fed Rate
        color, bg = ("#1976d2", "#e3f2fd")
        msg = f"Current Interest Rate: {latest}%"
        dxy_bias = "DXY: STRONG" if latest > 4 else "DXY: NEUTRAL"
        gold_bias = "GOLD: PRESSURE" if latest > 4 else "GOLD: STABLE"
        
    create_meter(name, latest, prev, color, info['next'], msg, dxy_bias, gold_bias, bg, cols1[i%2])

st.markdown("---")

# --- SECTION 2: LIQUIDITY & YIELDS (GOLD'S BIGGEST DRIVERS) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🌊 Smart Money Sentiment (XAUUSD Focus)</h2>", unsafe_allow_html=True)
cols2 = st.columns(4)
for i, (name, info) in enumerate(liquidity_indicators.items()):
    data = fred.get_series(info['id'])
    latest, prev = data.iloc[-1], data.iloc[-2]
    
    if 'Real Yield' in name:
        # Real Yields and Gold have 90% Inverse Correlation
        color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
        msg = "Real Yields barh rahi hain."
        dxy_bias = "DXY: BULLISH" if latest > prev else "DXY: BEARISH"
        gold_bias = "GOLD: STRONG SELL" if latest > prev else "GOLD: STRONG BUY"
    elif 'Yield Curve' in name:
        color, bg = ("#d32f2f", "#fff5f5") if latest < 0 else ("#388e3c", "#f1f8e9")
        msg = "Curve Inverted (Recession Risk)" if latest < 0 else "Normal Curve"
        dxy_bias = "DXY: UNCERTAIN"
        gold_bias = "GOLD: SAFE HAVEN BUY" if latest < 0 else "GOLD: NEUTRAL"
    elif 'M2' in name:
        color, bg = ("#1976d2", "#e3f2fd") if latest > prev else ("#fb8c00", "#fff3e0")
        msg = "Money Supply barh rahi hai."
        dxy_bias = "DXY: DEVALUATION" if latest > prev else "DXY: TIGHT"
        gold_bias = "GOLD: BULLISH" if latest > prev else "GOLD: BEARISH"
    else: # PCE
        color, bg = ("#455a64", "#eceff1")
        msg = "Fed ka favorite inflation data."
        dxy_bias = "DXY: TRENDING"
        gold_bias = "GOLD: TRENDING"
        
    create_meter(name, latest, prev, color, info['next'], msg, dxy_bias, gold_bias, bg, cols2[i], size=160)

# Footer
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

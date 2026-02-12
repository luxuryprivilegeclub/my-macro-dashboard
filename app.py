import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades | Macro & COT Terminal", layout="wide")

# 2. Logo Section
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{logo_url}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

# 3. Header
st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;">
    <h1 style="margin: 0; font-family: 'Arial Black', sans-serif;">ROLLIC TRADES MACRO TERMINAL</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Grade Analysis | XAUUSD & DXY Focus</p>
</div>""", unsafe_allow_html=True)

# 4. API Setup
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except:
    st.error("API Key missing in Streamlit Secrets!")
    st.stop()

# --- Helper Function for Professional Meters ---
def display_professional_meter(col, name, latest, previous, next_date, msg, dxy_bias, gold_bias, color, bg_color, height=280):
    with col:
        # Title above meter
        st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -40px; color: #333;'>{name}</p>", unsafe_allow_html=True)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest,
            gauge = {
                'axis': {'range': [min(latest, previous)*0.9, max(latest, previous)*1.1]},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 1,
            }
        ))
        fig.update_layout(height=height, margin=dict(l=30, r=30, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis Box with Badges
        st.markdown(f"""
            <div style="background:{bg_color}; border:1px solid {color}44; padding:12px; border-radius:12px; text-align:center; margin: -30px auto 30px auto; max-width: 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <p style="margin:0; font-size:13px; color: #444; font-weight: 500;">{msg}</p>
                <div style="margin-top: 8px;">
                    <span style="background:#1e3c72; color:white; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{dxy_bias}</span>
                    <span style="background:#d4af37; color:black; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{gold_bias}</span>
                </div>
                <p style="margin-top:10px; color:#000000; font-size:11px; font-weight:bold;">📅 Next: {next_date}</p>
            </div>
        """, unsafe_allow_html=True)

# --- SECTION 1: PRIMARY MACRO (2 Columns) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📌 Primary Gold & DXY Drivers</h2>", unsafe_allow_html=True)
cols1 = st.columns(2)
main_indicators = {
    'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'},
    'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'},
    'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'},
    'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'}
}

for i, (name, info) in enumerate(main_indicators.items()):
    data = fred.get_series(info['id'])
    latest, prev = data.iloc[-1], data.iloc[-2]
    
    if 'CPI' in name:
        color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
        msg = "Inflation barh rahi hai." if latest > prev else "Inflation cooling hai."
        d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
    elif 'NFP' in name:
        color, bg = ("#388e3c", "#f1f8e9") if latest > prev else ("#d32f2f", "#fff5f5")
        msg = "Jobs data strong hai." if latest > prev else "Jobs market weak hai."
        d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
    elif 'Unemployment' in name:
        color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
        msg = "Berozgari barh rahi hai." if latest > prev else "Berozgari kam hui hai."
        d_b, g_b = ("DXY: BEARISH", "GOLD: BULLISH") if latest > prev else ("DXY: BULLISH", "GOLD: BEARISH")
    else: # Fed Rate
        color, bg = ("#1976d2", "#e3f2fd")
        msg = f"Current Rate: {latest}%"
        d_b, g_b = ("DXY: STABLE", "GOLD: PRESSURE")
    
    display_professional_meter(cols1[i%2], name, latest, prev, info['next'], msg, d_b, g_b, color, bg)

st.markdown("<hr>", unsafe_allow_html=True)

# --- SECTION 2: LIQUIDITY & RECESSION (4 Columns) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🌊 Liquidity & Recession Risk</h2>", unsafe_allow_html=True)
cols2 = st.columns(4)
liq_ind = {
    'M2 Money Supply': {'id': 'WM2NS', 'next': 'Weekly'},
    'Yield Curve (10Y-2Y)': {'id': 'T10Y2Y', 'next': 'Daily'},
    'PCE Inflation': {'id': 'PCEPI', 'next': 'Feb 27, 2026'},
    'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}
}

for i, (name, info) in enumerate(liq_ind.items()):
    data = fred.get_series(info['id'])
    latest, prev = data.iloc[-1], data.iloc[-2]
    color = "#1976d2"
    d_b, g_b = "DXY: TREND", "GOLD: TREND"
    
    if 'Real Yield' in name:
        color = "#d32f2f" if latest > prev else "#388e3c"
        d_b, g_b = ("DXY: BULLISH", "GOLD: STRONG SELL") if latest > prev else ("DXY: BEARISH", "GOLD: STRONG BUY")
    elif 'Curve' in name:
        color = "#d32f2f" if latest < 0 else "#388e3c"
        d_b, g_b = ("DXY: UNCERTAIN", "GOLD: SAFE BUY") if latest < 0 else ("DXY: NORMAL", "GOLD: NEUTRAL")

    display_professional_meter(cols2[i], name, latest, prev, info['next'], "Market data check.", d_b, g_b, color, "#fafafa", height=200)

# --- SECTION 3: COT ANALYSIS ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #d4af37;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)
cot_data = [{"date": "Feb 06, 2026", "longs": 285000, "shorts": 45000, "analysis": "Smart Money bullish hai. ICT order blocks par long setups talash karein."}]
report = cot_data[0]
sentiment = (report['longs'] / (report['longs'] + report['shorts'])) * 100

col_l, col_r = st.columns([1, 1.5])
with col_l:
    fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=sentiment, title={'text': "Bullish Sentiment %"}, gauge={'bar': {'color': "#d4af37"}}))
    fig_cot.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=0))
    st.plotly_chart(fig_cot, use_container_width=True)
with col_r:
    st.markdown(f"""<div style="background:white; border:2px solid #d4af37; padding:20px; border-radius:15px; margin-top:20px;">
        <h3 style="color:#d4af37; margin-top:0;">Expert Analysis</h3>
        <p style="font-size:14px; color:#333;">{report['analysis']}</p>
        <div style="display:flex; justify-content:space-around; text-align:center; margin-top:15px;">
            <div><p style="margin:0; font-size:10px;">Net Position</p><b>{report['longs']-report['shorts']:,}</b></div>
        </div>
    </div>""", unsafe_allow_html=True)

# Footer
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

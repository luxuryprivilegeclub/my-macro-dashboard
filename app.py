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

# --- Helper Function for Consistent UI ---
def draw_meter(col, name, latest, prev, info_next, msg, dxy_b, gold_b, color, bg, height=280):
    with col:
        # Title adjustments to prevent cutting off
        st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -40px; color: #000; font-size: 16px; position: relative; z-index: 10;'>{name}</p>", unsafe_allow_html=True)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number", 
            value=latest, 
            gauge={
                'bar': {'color': color},
                'axis': {'range': [min(latest, prev)*0.9, max(latest, prev)*1.1]}
            }
        ))
        # Increased margins to fix "cutting off" issue
        fig.update_layout(height=height, margin=dict(l=30, r=30, t=60, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis Box
        st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:12px; border-radius:12px; text-align:center; margin:-30px auto 35px auto; max-width: 290px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
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
        
        # Logic Fixes
        if 'CPI' in name:
            color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
            msg = "Inflation barh rahi hai." if latest > prev else "Inflation cooling hai."
            d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
        elif 'NFP' in name:
            color, bg = ("#388e3c", "#f1f8e9") if latest > prev else ("#d32f2f", "#fff5f5")
            msg = "Jobs data strong hai." if latest > prev else "Jobs weak hai."
            d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
        elif 'Unemployment' in name:
            color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
            msg = "Berozgari barh rahi hai." if latest > prev else "Berozgari kam hui hai."
            d_b, g_b = ("DXY: BEARISH", "GOLD: BULLISH") if latest > prev else ("DXY: BULLISH", "GOLD: BEARISH")
        else: # Fed Rate
            color, bg = ("#1976d2", "#e3f2fd")
            msg = f"Current Rate: {latest}%"
            d_b, g_b = ("DXY: STABLE", "GOLD: PRESSURE")
            
        draw_meter(cols1[i%2], name, latest, prev, info['next'], msg, d_b, g_b, color, bg, 280)
    except: st.error(f"Error loading {name}")

# --- SECTION 2: LIQUIDITY & RECESSION (4 Columns) ---
st.markdown("<hr><h2 style='text-align: center; color: #2c3e50;'>🌊 Liquidity & Recession Risk</h2>", unsafe_allow_html=True)
cols2 = st.columns(4)
liq_ind = {
    'M2 Money Supply': {'id': 'WM2NS', 'next': 'Weekly'},
    'Yield Curve (10Y-2Y)': {'id': 'T10Y2Y', 'next': 'Daily'},
    'PCE Inflation': {'id': 'PCEPI', 'next': 'Feb 27, 2026'},
    'Consumer Sentiment': {'id': 'UMCSENT', 'next': 'Feb 20, 2026'}
}

for i, (name, info) in enumerate(liq_ind.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        
        color = "#1976d2"
        d_b, g_b = "DXY: TREND", "GOLD: TREND"
        
        if 'Curve' in name:
            color = "#d32f2f" if latest < 0 else "#388e3c"
            d_b, g_b = ("DXY: RISK", "GOLD: BUY") if latest < 0 else ("DXY: OK", "GOLD: HOLD")
            
        draw_meter(cols2[i], name, latest, prev, info['next'], "Macro trend.", d_b, g_b, color, "#fafafa", 200)
    except: st.write(f"Error {name}")

# --- SECTION 3: YIELDS & TARGET (4 Columns) ---
st.markdown("<hr><h2 style='text-align: center; color: #2c3e50;'>📊 Yields & Fed Target</h2>", unsafe_allow_html=True)
cols3 = st.columns(4)
yield_ind = {
    'US 10Y Yield': {'id': 'DGS10', 'next': 'Daily'},
    '10Y Breakeven': {'id': 'T10YIE', 'next': 'Daily'},
    'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}
}

for i, (name, info) in enumerate(yield_ind.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
        draw_meter(cols3[i], name, latest, prev, info['next'], "Yield Analysis", d_b, g_b, "#1e3c72", "#fafafa", 200)
    except: st.write(f"Error {name}")

# Fed Target Meter (4th Column in Section 3)
try:
    cpi_data = fred.get_series('CPIAUCSL')
    curr_inf = ((cpi_data.iloc[-1] - cpi_data.iloc[-13]) / cpi_data.iloc[-13]) * 100
    draw_meter(cols3[3], "Inf. vs 2% Target", curr_inf, 2.0, "Feb 13", f"Gap: {curr_inf-2:.2f}%", "Fed Goal", "Macro Bias", "red", "#fafafa", 200)
except: st.write("Target Error")

# --- SECTION 4: COT REPORT (DROPDOWN & EXPERT ANALYSIS) ---
st.markdown("<hr><h2 style='text-align: center; color: #d4af37;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)
cot_reports = [
    {"date": "Feb 06, 2026", "longs": 285000, "shorts": 45000, "analysis": "Smart Money ne mazeed longs add kiye hain. Gold par bullish pressure barh raha hai kyunke shorts cover ho rahay hain. ICT order block par buy setups talash karein."},
    {"date": "Jan 30, 2026", "longs": 270000, "shorts": 52000, "analysis": "Institutions ne positions hold ki hui hain. Price consolidation mein hai lekin bias abhi bhi bullish hai."},
    {"date": "Jan 23, 2026", "longs": 260000, "shorts": 60000, "analysis": "Longs mein thori kami aayi hai, shayad profit taking ho rahi hai. Deep retracement expected hai."}
]
sel_date = st.selectbox("Select COT Date", [d['date'] for d in cot_reports])
rep = next(d for d in cot_reports if d['date'] == sel_date)
sentiment = (rep['longs'] / (rep['longs'] + rep['shorts'])) * 100

col_l, col_r = st.columns([1, 1.5])
with col_l:
    st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -30px; color: #000; font-size: 16px;'>Bullish Sentiment Index</p>", unsafe_allow_html=True)
    fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=sentiment, gauge={'bar': {'color': "#d4af37"}, 'axis': {'range': [0, 100]}}))
    fig_cot.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=0))
    st.plotly_chart(fig_cot, use_container_width=True)

with col_r:
    st.markdown(f"""<div style="background:white; border:2px solid #d4af37; padding:25px; border-radius:15px; margin-top:20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color:#d4af37; margin-top:0;">Expert Analysis (XAUUSD)</h3>
        <p style="font-size:14px; color:#333; line-height:1.6;">{rep['analysis']}</p>
        <hr><div style="display:flex; justify-content:space-around; text-align:center;">
            <div><p style="margin:0; font-size:11px; color:#777;">Longs</p><b style="color:#388e3c; font-size:16px;">{rep['longs']:,}</b></div>
            <div><p style="margin:0; font-size:11px; color:#777;">Shorts</p><b style="color:#d32f2f; font-size:16px;">{rep['shorts']:,}</b></div>
            <div><p style="margin:0; font-size:11px; color:#777;">Net</p><b style="color:#1e3c72; font-size:16px;">{rep['longs']-rep['shorts']:,}</b></div>
        </div></div>""", unsafe_allow_html=True)

# Footer
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:60px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades | Macro Terminal Pro", layout="wide")

# 2. Logo Section
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{logo_url}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

# 3. Header
st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
    <h1 style="margin: 0; font-family: 'Arial Black', sans-serif;">ROLLIC TRADES MACRO TERMINAL</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Sentiment & Gold Analysis</p>
</div>""", unsafe_allow_html=True)

# 4. API Setup
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except:
    st.error("API Key missing!")
    st.stop()

# --- DATA CONFIGURATION ---
main_ind = {
    'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'},
    'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'},
    'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'},
    'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'}
}

liquidity_ind = {
    'M2 Money Supply': {'id': 'WM2NS', 'next': 'Weekly'},
    'Yield Curve (10Y-2Y)': {'id': 'T10Y2Y', 'next': 'Daily'},
    'PCE Inflation': {'id': 'PCEPI', 'next': 'Feb 27, 2026'},
    'Consumer Sentiment': {'id': 'UMCSENT', 'next': 'Feb 20, 2026'}
}

yield_ind = {
    'US 10Y Yield': {'id': 'DGS10', 'next': 'Daily'},
    '10Y Breakeven': {'id': 'T10YIE', 'next': 'Daily'},
    'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}
}

# --- SECTION 1: PRIMARY MACRO (2 Cols) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📌 Primary Gold & DXY Drivers</h2>", unsafe_allow_html=True)
cols1 = st.columns(2)
for i, (name, info) in enumerate(main_ind.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        color = "#d32f2f" if latest > prev else "#388e3c"
        msg = "Data updated."
        if 'CPI' in name: msg = "Inflation barh rahi hai." if latest > prev else "Inflation cooling hai."
        elif 'NFP' in name: msg = "Jobs barh rahi hain, economy strong hai." if latest > prev else "Jobs kam hui hain."
        
        with cols1[i%2]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 18}}, gauge={'bar': {'color': color}}))
            fig.update_layout(height=250, margin=dict(l=30, r=30, t=50, b=0)) # Increased height
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="background:#fafafa; border:1px solid #ddd; padding:10px; border-radius:12px; text-align:center; margin:-20px auto 30px auto; max-width: 320px;">
                <p style="margin:0; font-size:13px; font-weight:500;">{msg}</p>
                <p style="margin-top:8px; color:#000000; font-size:12px; font-weight:bold;">📅 Next Release: {info['next']}</p>
            </div>""", unsafe_allow_html=True)
    except: st.write("Error")

# --- SECTION 2: LIQUIDITY & RECESSION (4 Cols) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🌊 Liquidity & Recession Risk</h2>", unsafe_allow_html=True)
cols2 = st.columns(4)
for i, (name, info) in enumerate(liquidity_ind.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        color = "#1976d2"
        if 'Curve' in name: color = "#d32f2f" if latest < 0 else "#388e3c"

        with cols2[i]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 14}}, gauge={'bar': {'color': color}}))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=40, b=0)) # Fixed cutting height
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="text-align:center; border:1px solid #ddd; border-radius:10px; padding:5px; background:#fff;">
                <p style="margin:0; font-size:11px; font-weight:bold; color:#000000;">📅 Next: {info['next']}</p>
            </div>""", unsafe_allow_html=True)
    except: st.write("Error")

# --- SECTION 3: YIELDS & TARGET (4 Cols) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📊 Yields & Target Tracking</h2>", unsafe_allow_html=True)
cols3 = st.columns(4)
for i, (name, info) in enumerate(yield_ind.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        with cols3[i]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 14}}, gauge={'bar': {'color': "#1e3c72"}}))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="text-align:center; border:1px solid #ddd; border-radius:10px; padding:5px; background:#fff;">
                <p style="margin:0; font-size:11px; font-weight:bold; color:#000000;">📅 Next: {info['next']}</p>
            </div>""", unsafe_allow_html=True)
    except: st.write("Error")

# Fed Target Meter (4th column in Section 3)
try:
    cpi_data = fred.get_series('CPIAUCSL')
    curr_inf = ((cpi_data.iloc[-1] - cpi_data.iloc[-13]) / cpi_data.iloc[-13]) * 100
    with cols3[3]:
        fig_fed = go.Figure(go.Indicator(mode="gauge+number", value=curr_inf, title={'text': "Inf. vs 2% Target", 'font': {'size': 14}}, gauge={'bar': {'color': "red" if curr_inf > 2 else "green"}, 'threshold': {'line': {'color': "black", 'width': 2}, 'value': 2}}))
        fig_fed.update_layout(height=200, margin=dict(l=10, r=10, t=40, b=0))
        st.plotly_chart(fig_fed, use_container_width=True)
        st.markdown(f"""<div style="text-align:center; border:1px solid #ddd; border-radius:10px; padding:5px; background:#fff;">
            <p style="margin:0; font-size:11px; font-weight:bold; color:#000000;">Gap: {curr_inf-2:.2f}% Over</p>
        </div>""", unsafe_allow_html=True)
except: st.write("Error")

# --- SECTION 4: COT ANALYSIS ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #d4af37;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)
cot_data = [
    {"date": "Feb 06, 2026", "longs": 285000, "shorts": 45000, "analysis": "Smart Money ne mazeed longs add kiye hain. Gold par bullish pressure barh raha hai. ICT order block par buy setups talash karein."},
    {"date": "Jan 30, 2026", "longs": 270000, "shorts": 52000, "analysis": "Institutions ne positions hold ki hui hain. Price consolidation mein hai lekin bias abhi bhi bullish hai."}
]
selected_date = st.selectbox("Select COT Report Date", [d['date'] for d in cot_data])
report = next(item for item in cot_data if item["date"] == selected_date)
sentiment = (report['longs'] / (report['longs'] + report['shorts'])) * 100

col_l, col_r = st.columns([1, 1.5])
with col_l:
    fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=sentiment, title={'text': "Bullish Sentiment %"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#d4af37"}}))
    fig_cot.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=0))
    st.plotly_chart(fig_cot, use_container_width=True)
with col_r:
    st.markdown(f"""<div style="background:white; border:2px solid #d4af37; padding:20px; border-radius:15px; margin-top:20px;">
        <h3 style="color:#d4af37; margin-top:0;">Expert Analysis</h3>
        <p style="font-size:14px; color:#333;">{report['analysis']}</p>
        <hr>
        <div style="display:flex; justify-content:space-around; text-align:center;">
            <div><p style="margin:0; font-size:10px;">Longs</p><b>{report['longs']:,}</b></div>
            <div><p style="margin:0; font-size:10px;">Shorts</p><b>{report['shorts']:,}</b></div>
            <div><p style="margin:0; font-size:10px;">Net</p><b>{report['longs']-report['shorts']:,}</b></div>
        </div>
    </div>""", unsafe_allow_html=True)

# Footer
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades Macro Dashboard Pro", layout="wide")

# 2. Logo Section (Centered)
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{logo_url}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

# 3. Header
st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
    <h1 style="margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 1px;">MACRO ECONOMIC PRO DASHBOARD</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Advanced Sentiment Analysis | Rollic Trades</p>
</div>""", unsafe_allow_html=True)

# 4. API Setup
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except:
    st.error("API Key missing in Streamlit Secrets!")
    st.stop()

# Data Schedule
main_indicators = {
    'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'},
    'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'},
    'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'},
    'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'}
}

yield_indicators = {
    'US 10Y Yield': {'id': 'DGS10', 'next': 'Daily'},
    '10Y Breakeven': {'id': 'T10YIE', 'next': 'Daily'},
    'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}
}

# --- SECTION 1: MAIN INDICATORS (2 Columns) ---
st.subheader("📌 Key Economic Indicators")
cols1 = st.columns(2)
for i, (name, info) in enumerate(main_indicators.items()):
    try:
        data = fred.get_series(info['id'])
        latest, previous = data.iloc[-1], data.iloc[-2]
        
        # Simple Logic
        if 'CPI' in name:
            msg, bias, color, bg = ("Inflation barh rahi hai.", "DXY: BULLISH", "#d32f2f", "#fff5f5") if latest > previous else ("Inflation kam ho rahi hai.", "DXY: BEARISH", "#388e3c", "#f1f8e9")
        elif 'NFP' in name:
            msg, bias, color, bg = ("Strong Jobs Data.", "DXY: BULLISH", "#388e3c", "#f1f8e9") if latest > previous else ("Weak Jobs Data.", "DXY: BEARISH", "#d32f2f", "#fff5f5")
        elif 'Unemployment' in name:
            msg, bias, color, bg = ("Berozgari barh rahi hai.", "DXY: BEARISH", "#d32f2f", "#fff5f5") if latest > previous else ("Berozgari kam hui hai.", "DXY: BULLISH", "#388e3c", "#f1f8e9")
        else:
            msg, bias, color, bg = (f"Current Rate: {latest}%", "FED POLICY", "#1976d2", "#e3f2fd")

        with cols1[i % 2]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 16}}, gauge={'bar': {'color': color}}))
            fig.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:10px; border-radius:10px; text-align:center; margin-bottom:20px;">
                <p style="margin:0; font-size:13px;">{msg}</p>
                <div style="background:{color}; color:white; padding:2px 10px; border-radius:5px; font-size:11px; font-weight:bold; display:inline-block; margin-top:5px;">{bias}</div>
                <p style="margin-top:8px; color:#000000; font-size:11px; font-weight:bold;">📅 Next Release: {info['next']}</p>
            </div>""", unsafe_allow_html=True)
    except: st.write(f"Error loading {name}")

st.markdown("---")

# --- SECTION 2: YIELDS & FED TARGET (4 Columns - Smaller Size) ---
st.subheader("📊 Market Sentiment & Yields")
cols2 = st.columns(4)

# 1-3: Yields
for i, (name, info) in enumerate(yield_indicators.items()):
    try:
        data = fred.get_series(info['id'])
        latest, previous = data.iloc[-1], data.iloc[-2]
        color = "#1565c0" if latest > previous else "#fb8c00"
        
        with cols2[i]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 14}}, gauge={'bar': {'color': color}}))
            fig.update_layout(height=160, margin=dict(l=10, r=10, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="text-align:center; padding:5px; border:1px solid #ddd; border-radius:8px; background:#fafafa;">
                <p style="margin:0; font-size:10px; font-weight:bold; color:#000000;">DXY Impact: {"Strong" if latest > previous else "Weak"}</p>
                <p style="margin:0; font-size:10px; font-weight:bold; color:#000000;">📅 Next: {info['next']}</p>
            </div>""", unsafe_allow_html=True)
    except: st.write("Error")

# 4: Fed Target Meter
try:
    cpi_data = fred.get_series('CPIAUCSL')
    curr_inf = ((cpi_data.iloc[-1] - cpi_data.iloc[-13]) / cpi_data.iloc[-13]) * 100
    with cols2[3]:
        fig_fed = go.Figure(go.Indicator(mode="gauge+number", value=curr_inf, title={'text': "Inf. vs 2% Target", 'font': {'size': 14}}, gauge={'bar': {'color': "red" if curr_inf > 2 else "green"}, 'threshold': {'line': {'color': "black", 'width': 2}, 'value': 2}}))
        fig_fed.update_layout(height=160, margin=dict(l=10, r=10, t=30, b=0))
        st.plotly_chart(fig_fed, use_container_width=True)
        st.markdown(f"""<div style="text-align:center; padding:5px; border:1px solid #ddd; border-radius:8px; background:#fafafa;">
            <p style="margin:0; font-size:10px; font-weight:bold; color:#000000;">Gap: {curr_inf-2:.2f}% Over</p>
            <p style="margin:0; font-size:10px; font-weight:bold; color:#000000;">📅 Next: Feb 13</p>
        </div>""", unsafe_allow_html=True)
except: st.write("Error")

# Footer
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

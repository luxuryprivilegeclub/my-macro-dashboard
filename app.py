import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades | Macro & COT Terminal", layout="wide")

# 2. Logo Section (Centered)
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{logo_url}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

# 3. Main Header
st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
    <h1 style="margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 1px;">ROLLIC TRADES MACRO & COT TERMINAL</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Grade Analysis | XAUUSD & DXY Focus</p>
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

# --- SECTION 1: PRIMARY MACRO INDICATORS (2 Columns) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50; font-family: Arial;'>📌 Primary Gold & DXY Drivers</h2>", unsafe_allow_html=True)
cols1 = st.columns(2)
for i, (name, info) in enumerate(main_indicators.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        
        if 'CPI' in name:
            color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
            msg, dxy_b, gold_b = ("Inflation barh rahi hai.", "DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("Inflation cooling hai.", "DXY: BEARISH", "GOLD: BULLISH")
        elif 'NFP' in name:
            color, bg = ("#388e3c", "#f1f8e9") if latest > prev else ("#d32f2f", "#fff5f5")
            msg, dxy_b, gold_b = ("Jobs data strong hai.", "DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("Jobs market weak hai.", "DXY: BEARISH", "GOLD: BULLISH")
        elif 'Unemployment' in name:
            color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
            msg, dxy_b, gold_b = ("Berozgari barh rahi hai.", "DXY: BEARISH", "GOLD: BULLISH") if latest > prev else ("Berozgari kam hui hai.", "DXY: BULLISH", "GOLD: BEARISH")
        else:
            color, bg, msg, dxy_b, gold_b = ("#1976d2", "#e3f2fd", f"Current Rate: {latest}%", "DXY: STABLE", "GOLD: PRESSURE")

        with cols1[i % 2]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 16}}, gauge={'bar': {'color': color}}))
            fig.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:10px; border-radius:12px; text-align:center; margin: -20px auto 30px auto; max-width: 320px;">
                <p style="margin:0; font-size:12px; color: #444; font-weight: 500;">{msg}</p>
                <div style="background:#1e3c72; color:white; padding:2px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block; margin-top:5px;">{dxy_b}</div>
                <div style="background:#d4af37; color:black; padding:2px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block; margin-top:5px;">{gold_b}</div>
                <p style="margin-top:8px; color:#000000; font-size:11px; font-weight:bold;">📅 Next: {info['next']}</p>
            </div>""", unsafe_allow_html=True)
    except: st.write(f"Error loading {name}")

st.markdown("<hr>", unsafe_allow_html=True)

# --- SECTION 2: LIQUIDITY & YIELDS (4 Columns - Smaller) ---
st.markdown("<h2 style='text-align: center; color: #2c3e50; font-family: Arial;'>📊 Sentiment & Yield Analysis</h2>", unsafe_allow_html=True)
cols2 = st.columns(4)
for i, (name, info) in enumerate(liquidity_indicators.items()):
    try:
        data = fred.get_series(info['id'])
        latest, prev = data.iloc[-1], data.iloc[-2]
        color = "#d32f2f" if latest > prev else "#388e3c"
        
        # Gold Bias Logic for Yields
        gold_b = "GOLD: BEARISH" if latest > prev else "GOLD: BULLISH"
        if 'Yield Curve' in name:
            gold_b = "GOLD: SAFE BUY" if latest < 0 else "GOLD: NEUTRAL"

        with cols2[i]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, title={'text': name, 'font': {'size': 14}}, gauge={'bar': {'color': color}}))
            fig.update_layout(height=160, margin=dict(l=10, r=10, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="text-align:center; padding:8px; border:1px solid #ddd; border-radius:10px; background:#fafafa; margin: 0 auto; max-width: 200px;">
                <p style="margin:0; font-size:10px; font-weight:bold; color:#d4af37;">{gold_b}</p>
                <p style="margin:4px 0 0 0; font-size:10px; font-weight:bold; color:#000000;">📅 Next: {info['next']}</p>
            </div>""", unsafe_allow_html=True)
    except: st.write("Data Error")

# --- SECTION 3: COT REPORT SUMMARY (GOLD) ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #d4af37; font-family: Arial;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)

cot_data = [
    {"date": "Feb 06, 2026", "longs": 285000, "shorts": 45000, "analysis": "Smart Money ne mazeed longs add kiye hain. Gold par bullish pressure barh raha hai kyunke shorts cover ho rahay hain. ICT order block par buy setups talash karein."},
    {"date": "Jan 30, 2026", "longs": 270000, "shorts": 52000, "analysis": "Institutions ne positions hold ki hui hain. Price consolidation mein hai lekin bias abhi bhi bullish hai."},
    {"date": "Jan 23, 2026", "longs": 260000, "shorts": 60000, "analysis": "Longs mein thori kami aayi hai, shayad profit taking ho rahi hai. Deep retracement expected hai."},
    {"date": "Jan 16, 2026", "longs": 290000, "shorts": 40000, "analysis": "Extreme Bullish Sentiment! Gold ne liquidity sweep ki hai aur institutions heavy buy kar rahay hain."},
    {"date": "Jan 09, 2026", "longs": 275000, "shorts": 55000, "analysis": "Initial build-up phase. Smart Money long side par accumulate kar rahi hai."}
]

selected_date = st.selectbox("Select COT Report Date", [d['date'] for d in cot_data])
current_report = next(item for item in cot_data if item["date"] == selected_date)
total = current_report['longs'] + current_report['shorts']
sentiment_score = (current_report['longs'] / total) * 100

col_cot_l, col_cot_r = st.columns([1, 1.5])
with col_cot_l:
    fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=sentiment_score, title={'text': "Bullish Sentiment %"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#d4af37"}, 'steps': [{'range': [0, 50], 'color': "#ffebee"}, {'range': [50, 100], 'color': "#e8f5e9"}]}))
    fig_cot.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=0))
    st.plotly_chart(fig_cot, use_container_width=True)

with col_cot_r:
    st.markdown(f"""
        <div style="background-color: white; border: 2px solid #d4af37; padding: 20px; border-radius: 15px; margin-top: 20px;">
            <h3 style="color: #d4af37; margin-top: 0;">Expert Analysis (XAUUSD)</h3>
            <p style="font-size: 14px; color: #333; line-height: 1.6;">{current_report['analysis']}</p>
            <hr style="border: 0.5px solid #eee;">
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div><p style="margin:0; font-size:10px; color:#777;">Longs</p><b style="color:#388e3c;">{current_report['longs']:,}</b></div>
                <div><p style="margin:0; font-size:10px; color:#777;">Shorts</p><b style="color:#d32f2f;">{current_report['shorts']:,}</b></div>
                <div><p style="margin:0; font-size:10px; color:#777;">Net</p><b style="color:#1e3c72;">{current_report['longs']-current_report['shorts']:,}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. Footer
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

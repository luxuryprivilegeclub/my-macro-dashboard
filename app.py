import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades Macro Dashboard", layout="wide")

# 2. Logo Section (Perfectly Centered)
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"

st.markdown(
    f"""
    <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 10px;">
        <img src="{logo_url}" width="200" style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Header Section
st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;">
        <h1 style="margin: 0; font-family: Arial;">Macro Economic Live Dashboard</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">FRED API Live Tracking | Developed for Rollic Trades</p>
    </div>
""", unsafe_allow_html=True)

# 4. API Key Setup (Using Secrets)
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except Exception as e:
    st.error("API Key ka masla hai! Streamlit Secrets mein 'FRED_API_KEY' check karein.")
    st.stop()

# 5. Indicators Dictionary
indicators = {
    'CPI Inflation': 'CPIAUCSL',
    'NFP (Jobs Data)': 'PAYEMS',
    'Unemployment Rate': 'UNRATE',
    'Fed Interest Rate': 'FEDFUNDS'
}

# 6. Grid Layout (2 Columns)
col1, col2 = st.columns(2)

for i, (name, s_id) in enumerate(indicators.items()):
    try:
        # Fetching Data
        data = fred.get_series(s_id)
        latest = data.iloc[-1]
        previous = data.iloc[-2]
        
        # UI Logic & Roman Urdu Analysis
        impact_msg = ""
        bias = ""
        color = ""
        bg_light = ""

        if 'CPI' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Inflation barh rahi hai. Fed rates high rakh sakta hai.", "DXY Impact: BULLISH", "#d32f2f", "#fff5f5"
            else:
                impact_msg, bias, color, bg_light = "Inflation kam ho rahi hai. Rate cut ke chances hain.", "DXY Impact: BEARISH", "#388e3c", "#f1f8e9"
        
        elif 'NFP' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Jobs barh rahi hain, economy strong hai.", "DXY Impact: BULLISH", "#388e3c", "#f1f8e9"
            else:
                impact_msg, bias, color, bg_light = "Jobs kam hui hain, economy weak ho rahi hai.", "DXY Impact: BEARISH", "#d32f2f", "#fff5f5"
                
        elif 'Unemployment' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Berozgari barh rahi hai, USD par pressure aa sakta hai.", "DXY Impact: BEARISH", "#d32f2f", "#fff5f5"
            else:
                impact_msg, bias, color, bg_light = "Berozgari kam hui hai, USD strong ho sakta hai.", "DXY Impact: BULLISH", "#388e3c", "#f1f8e9"
                
        else: # Interest Rate
            impact_msg, bias, color, bg_light = f"Current Fed Funds Rate {latest}% hai.", "FED POLICY STATUS", "#1976d2", "#e3f2fd"

        # Displaying in Grid
        target_col = col1 if i % 2 == 0 else col2
        
        with target_col:
            # Gauge Meter Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = latest,
                title = {'text': name, 'font': {'size': 20, 'color': '#333'}},
                gauge = {
                    'bar': {'color': color},
                    'axis': {'range': [previous*0.95, latest*1.05]},
                    'bgcolor': "white",
                    'borderwidth': 1
                }
            ))
            fig.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=0))
            st.plotly_chart(fig, use_container_width=True)

            # Centered Analysis Box (Roman Urdu)
            st.markdown(f"""
                <div style="font-family: Arial; padding: 15px; border-radius: 12px; background-color: {bg_light}; 
                            border: 1px solid {color}44; max-width: 380px; margin: -20px auto 40px auto; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <p style="margin: 0; color: #444; font-size: 14px; font-weight: 500;">{impact_msg}</p>
                    <div style="margin-top: 10px; padding: 5px 20px; background-color: {color}; color: white; 
                                border-radius: 8px; font-size: 13px; font-weight: bold; display: inline-block;">
                        {bias}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"{name} ka data fetch nahi ho saka.")

# 7. Footer Section
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"""
    <hr>
    <p style='text-align: center; color: #888; font-size: 13px;'>
        Last Updated: {now} (Data updates automatically on page refresh)
    </p>
""", unsafe_allow_html=True)

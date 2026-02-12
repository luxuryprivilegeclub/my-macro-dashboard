import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# Page setup
st.set_page_config(page_title="Macro Dashboard", layout="wide")

# --- Logo Section (New) ---
# Google Drive direct link format
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"

# Use columns to center the logo
# [1, 2, 1] ratio means the middle column is twice as wide as side columns
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Display logo in the middle column. Adjust width as needed.
    st.image(logo_url, width=250)

# --- Title Section ---
# Custom CSS for Title (Updated margin-top for spacing below logo)
st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px; margin-top: 20px;">
        <h1 style="margin: 0;">Macro Economic Live Dashboard</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">FRED API Live Data Tracking | Rollic Trades</p>
    </div>
""", unsafe_allow_html=True)

# API Key Setup (Using Streamlit Secrets for security)
# Make sure you have added FRED_API_KEY in Streamlit Cloud Settings -> Secrets
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except Exception as e:
    st.error("API Key not found! Please set FRED_API_KEY in Streamlit Secrets.")
    st.stop()

# Indicators
indicators = {
    'CPI Inflation': 'CPIAUCSL',
    'NFP (Jobs)': 'PAYEMS',
    'Unemployment': 'UNRATE',
    'Interest Rate': 'FEDFUNDS'
}

# 2-Column Grid
col1, col2 = st.columns(2)

for i, (name, s_id) in enumerate(indicators.items()):
    # Data Fetching with Error Handling
    try:
        data = fred.get_series(s_id)
        latest = data.iloc[-1]
        previous = data.iloc[-2]
    except Exception as e:
        st.warning(f"Could not fetch data for {name}. Check API Key or FRED service.")
        continue
    
    # Logic Settings
    impact_msg = ""
    bias = ""
    color = ""
    bg_light = ""

    # Specific Logic for each indicator
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

    # Display in Columns
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest,
            title = {'text': name, 'font': {'size': 20}},
            gauge = {'bar': {'color': color}, 'axis': {'range': [previous*0.9, latest*1.1]}}
        ))
        fig.update_layout(height=250, margin=dict(l=30, r=30, t=50, b=0))
        st.plotly_chart(fig, use_container_width=True)

        # Centered Analysis Box (Like Colab)
        st.markdown(f"""
            <div style="font-family: Arial; padding: 12px; border-radius: 10px; background-color: {bg_light}; 
                        border: 1px solid {color}44; max-width: 350px; margin: -10px auto 40px auto; text-align: center;">
                <p style="margin: 0; color: #444; font-size: 13px;">{impact_msg}</p>
                <div style="margin-top: 8px; padding: 4px 15px; background-color: {color}; color: white; 
                            border-radius: 5px; font-size: 12px; font-weight: bold; display: inline-block;">
                    {bias}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer with Last Update
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<hr><p style='text-align: center; color: gray;'>Last Updated: {now} (Auto-refresh on page reload)</p>", unsafe_allow_html=True)

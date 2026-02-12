import streamlit as st
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Rollic Trades Macro Dashboard Pro", layout="wide")

# 2. Logo Section (Perfectly Centered)
logo_url = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"

st.markdown(
    f"""
    <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 10px;">
        <img src="{logo_url}" width="180" style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Header Section
st.markdown("""
    <div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 25px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;">
        <h1 style="margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: 2px;">MACRO ECONOMIC PRO DASHBOARD</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 16px;">Advanced Market Sentiment & Yield Analysis | Rollic Trades</p>
    </div>
""", unsafe_allow_html=True)

# 4. API Key Setup
try:
    API_KEY = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=API_KEY)
except Exception as e:
    st.error("API Key missing! Streamlit Secrets mein 'FRED_API_KEY' add karein.")
    st.stop()

# 5. Indicators & Schedule
indicators = {
    'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'},
    'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'},
    'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'},
    'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'},
    'US 10Y Yield': {'id': 'DGS10', 'next': 'Daily (Market Hours)'},
    '10Y Breakeven': {'id': 'T10YIE', 'next': 'Daily (Market Hours)'},
    'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily (Market Hours)'}
}

# 6. Grid Layout (3 Columns for better fit)
cols = st.columns(2)

for i, (name, info) in enumerate(indicators.items()):
    s_id = info['id']
    next_date = info['next']
    
    try:
        data = fred.get_series(s_id)
        latest = data.iloc[-1]
        previous = data.iloc[-2]
        
        impact_msg = ""
        bias = ""
        color = ""
        bg_light = ""

        # Logic for each indicator
        if 'CPI' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Inflation barh rahi hai. Fed rates high rakh sakta hai.", "DXY Impact: BULLISH", "#d32f2f", "#fff5f5"
            else:
                impact_msg, bias, color, bg_light = "Inflation kam ho rahi hai. Rate cut ke chances hain.", "DXY Impact: BEARISH", "#388e3c", "#f1f8e9"
        
        elif 'NFP' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Strong Economy. Jobs market strong hai.", "DXY Impact: BULLISH", "#388e3c", "#f1f8e9"
            else:
                impact_msg, bias, color, bg_light = "Economy weak ho rahi hai. Jobs data kam hai.", "DXY Impact: BEARISH", "#d32f2f", "#fff5f5"
        
        elif '10Y Yield' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Yields barh rahi hain. Investors USD buy kar sakty hain.", "DXY Impact: BULLISH", "#1565c0", "#e3f2fd"
            else:
                impact_msg, bias, color, bg_light = "Yields gir rahi hain. USD attractive nahi raha.", "DXY Impact: BEARISH", "#fb8c00", "#fff3e0"

        elif 'Real Yield' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Real returns barh rahay hain. USD strong hoga.", "DXY Impact: BULLISH", "#2e7d32", "#e8f5e9"
            else:
                impact_msg, bias, color, bg_light = "Real returns kam ho rahay hain.", "DXY Impact: BEARISH", "#c62828", "#ffebee"

        elif 'Breakeven' in name:
            if latest > previous:
                impact_msg, bias, color, bg_light = "Market inflation expectations barh rahi hain.", "DXY: BULLISH (Hawkish)", "#8e24aa", "#f3e5f5"
            else:
                impact_msg, bias, color, bg_light = "Inflation expectations kam ho rahi hain.", "DXY: BEARISH (Dovish)", "#00acc1", "#e0f7fa"
                
        else: # Default/Unemployment
            impact_msg, bias, color, bg_light = "Data updated. Trend follow karein.", "Check Market Sentiment", "#455a64", "#eceff1"

        # Display in Grid
        with cols[i % 2]:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = latest,
                title = {'text': name, 'font': {'size': 18}},
                gauge = {
                    'bar': {'color': color},
                    'axis': {'range': [min(latest, previous)*0.9, max(latest, previous)*1.1]}
                }
            ))
            fig.update_layout(height=250, margin=dict(l=30, r=30, t=50, b=0))
            st.plotly_chart(fig, use_container_width=True)

            # Analysis Box
            st.markdown(f"""
                <div style="font-family: Arial; padding: 15px; border-radius: 12px; background-color: {bg_light}; 
                            border: 1px solid {color}44; max-width: 380px; margin: -20px auto 40px auto; text-align: center;">
                    <p style="margin: 0; color: #444; font-size: 13px; font-weight: 500;">{impact_msg}</p>
                    <div style="margin-top: 10px; padding: 5px 15px; background-color: {color}; color: white; 
                                border-radius: 8px; font-size: 12px; font-weight: bold; display: inline-block;">
                        {bias}
                    </div>
                    <p style="margin-top: 10px; color: #777; font-size: 11px;">📅 Next Release: {next_date}</p>
                </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.write(f"Indicator {name} fetch nahi ho saka.")

# --- SPECIAL METER: FED TARGET DISTANCE ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>Fed Inflation Target Distance</h2>", unsafe_allow_html=True)
try:
    # Calculating YoY Inflation from CPI
    cpi_data = fred.get_series('CPIAUCSL')
    current_inflation = ((cpi_data.iloc[-1] - cpi_data.iloc[-13]) / cpi_data.iloc[-13]) * 100
    distance = current_inflation - 2.0
    
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        fig_fed = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_inflation,
            delta = {'reference': 2.0, 'position': "top", 'increasing': {'color': "red"}},
            title = {'text': "Current Inflation vs 2% Target"},
            gauge = {
                'axis': {'range': [0, 10]},
                'bar': {'color': "#d32f2f" if current_inflation > 2 else "#388e3c"},
                'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 2.0}
            }
        ))
        fig_fed.update_layout(height=300)
        st.plotly_chart(fig_fed, use_container_width=True)
        
        st.markdown(f"""
            <div style="text-align: center; background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">
                <p style="margin: 0; color: #333;">Fed Target <b>2.0%</b> hai. Current Inflation <b>{current_inflation:.2f}%</b> hai.</p>
                <p style="color: {'red' if distance > 0 else 'green'}; font-weight: bold;">
                    Fed Target se {abs(distance):.2f}% {'upar' if distance > 0 else 'niche'} hai.
                </p>
            </div>
        """, unsafe_allow_html=True)
except:
    st.write("Target data calculate nahi ho saka.")

# Footer
st.markdown(f"<hr><p style='text-align: center; color: gray;'>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)

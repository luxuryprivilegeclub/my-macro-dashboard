import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Rollic Trades Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🪙"
)

# --- 2. DARK THEME & SMART CARDS CSS ---
st.markdown("""
    <style>
    /* Navbar Styling (Dark Gradient) */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-bottom: 2px solid #d4af37;
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    
    /* Smart Cards (Compact & Dark) */
    .smart-card {
        background: #1e1e1e; /* Dark Grey */
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .smart-card:hover {
        border-color: #d4af37; /* Gold Border on Hover */
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(212, 175, 55, 0.2);
    }
    .card-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }
    .card-title {
        color: white;
        font-size: 18px;
        font-weight: bold;
        margin: 0;
    }
    .card-desc {
        color: #aaa;
        font-size: 12px;
        margin-top: 5px;
    }

    /* Buttons Override (Gold Accent) */
    div.stButton > button {
        background-color: #262730;
        color: white;
        border: 1px solid #555;
        border-radius: 8px;
    }
    div.stButton > button:hover {
        border-color: #d4af37;
        color: #d4af37;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GLOBAL VARIABLES ---
ADMIN_USER = "admin"
ADMIN_PASS = "Rollic@786"
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_role' not in st.session_state: st.session_state['user_role'] = None
if 'username' not in st.session_state: st.session_state['username'] = None
if 'current_page' not in st.session_state: st.session_state['current_page'] = 'home'
if 'pdf_archive' not in st.session_state: st.session_state['pdf_archive'] = {} 
if 'users_db' not in st.session_state:
    # Dummy DB
    data = {"Username": ["admin", "user"], "Password": ["Rollic@786", "123"], "Role": ["Admin", "User"], "Status": ["Active", "Active"]}
    st.session_state['users_db'] = pd.DataFrame(data)

# --- 5. NAVIGATION BAR (DARK) ---
def render_navbar():
    st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True) # Spacer
    with st.container():
        # Using columns to simulate a sticky navbar content
        st.markdown(f"""
            <div class="navbar">
                <span style="color: #d4af37; font-weight: bold; font-size: 18px; margin-right: 20px;">🪙 ROLLIC TRADES</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Buttons below the visual navbar strip
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            if st.button("🏠 Home", use_container_width=True): st.session_state['current_page'] = 'home'; st.rerun()
        with col2:
            if st.button("📊 Macro", use_container_width=True): st.session_state['current_page'] = 'macro'; st.rerun()
        with col3:
            if st.button("📄 Reports", use_container_width=True): st.session_state['current_page'] = 'reports'; st.rerun()
        with col4:
            if st.session_state['user_role'] == 'Admin':
                if st.button("⚙️ Admin", use_container_width=True): st.session_state['current_page'] = 'admin'; st.rerun()
        with col5:
            if st.button("Log Out", use_container_width=True): st.session_state['logged_in'] = False; st.rerun()
    st.markdown("---")

# ==========================================
# PAGE: LOGIN
# ==========================================
def login_page():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 50px;">
                <img src="{LOGO_URL}" width="150" style="border-radius: 50%; border: 3px solid #d4af37;">
                <h2 style="color: white; margin-top: 15px;">ROLLIC TRADES</h2>
            </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login Access", use_container_width=True):
            db = st.session_state['users_db']
            match = db[(db['Username'] == username) & (db['Password'] == password)]
            if not match.empty:
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = match.iloc[0]['Role']
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Access Denied")

# ==========================================
# PAGE: HOME (SMART BOXES)
# ==========================================
def home_page():
    st.markdown(f"<h2 style='text-align:center; color:white;'>Welcome, {st.session_state['username']}</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid Layout for Smart Boxes (4 Columns - Future Proof)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div class="smart-card">
            <div class="card-icon">📊</div>
            <p class="card-title">Macro Terminal</p>
            <p class="card-desc">Live Data & Yields</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Terminal", key="btn_macro", use_container_width=True):
            st.session_state['current_page'] = 'macro'
            st.rerun()
            
    with c2:
        st.markdown("""
        <div class="smart-card">
            <div class="card-icon">📄</div>
            <p class="card-title">Daily Reports</p>
            <p class="card-desc">PDF Analysis & Levels</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Reports", key="btn_reports", use_container_width=True):
            st.session_state['current_page'] = 'reports'
            st.rerun()
            
    # Future Placeholders (Empty for now)
    with c3:
        st.markdown("""
        <div class="smart-card" style="opacity: 0.5;">
            <div class="card-icon">🚀</div>
            <p class="card-title">Signals (Coming Soon)</p>
            <p class="card-desc">Live Trade Alerts</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown("""
        <div class="smart-card" style="opacity: 0.5;">
            <div class="card-icon">🎓</div>
            <p class="card-title">Academy (Coming Soon)</p>
            <p class="card-desc">Learning Resources</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE: ADMIN PANEL
# ==========================================
def admin_panel():
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>ADMIN CONSOLE</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📄 Upload Reports", "👥 User DB"])
    
    with tab1:
        st.markdown("### Upload Daily PDF")
        uploaded_file = st.file_uploader("Select PDF", type="pdf")
        report_date = st.date_input("Date", datetime.now())
        
        if st.button("Upload Report"):
            if uploaded_file:
                bytes_data = uploaded_file.getvalue()
                b64 = base64.b64encode(bytes_data).decode('utf-8')
                date_key = report_date.strftime("%Y-%m-%d")
                st.session_state['pdf_archive'][date_key] = b64
                st.success(f"Uploaded for {date_key}")
    
    with tab2:
        st.dataframe(st.session_state['users_db'], use_container_width=True)

# ==========================================
# PAGE: REPORTS PAGE
# ==========================================
def reports_page():
    st.markdown("## 📄 Daily Market Reports")
    col1, col2 = st.columns([1, 4])
    with col1:
        dates = list(st.session_state['pdf_archive'].keys())
        if dates:
            sel_date = st.selectbox("Select Date", dates)
        else:
            sel_date = None
            st.warning("No Reports")
            
    with col2:
        if sel_date:
            b64_pdf = st.session_state['pdf_archive'][sel_date]
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}#toolbar=0" width="100%" height="800"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

# ==========================================
# PAGE: MACRO DASHBOARD (FULL CODE)
# ==========================================
def macro_dashboard():
    # --- HEADER ---
    st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
        <h1 style="margin: 0; font-family: 'Arial Black', sans-serif;">ROLLIC TRADES MACRO TERMINAL</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Grade Analysis</p>
    </div>""", unsafe_allow_html=True)

    try:
        API_KEY = st.secrets["FRED_API_KEY"]
        fred = Fred(api_key=API_KEY)
    except:
        st.error("API Key Missing")
        st.stop()

    def draw_meter(col, name, latest, prev, info_next, msg, dxy_b, gold_b, color, bg, height=280):
        with col:
            st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -40px; color: #ffffff; font-size: 16px; position: relative; z-index: 10;'>{name}</p>", unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, gauge={'bar': {'color': color}, 'axis': {'range': [min(latest, prev)*0.9, max(latest, prev)*1.1]}}))
            fig.update_layout(height=height, margin=dict(l=30, r=30, t=60, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:12px; border-radius:12px; text-align:center; margin:-30px auto 35px auto; max-width: 290px;">
                <p style="margin:0; font-size:12px; font-weight:500; color:#333;">{msg}</p>
                <div style="margin-top:8px;">
                    <span style="background:#1e3c72; color:white; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{dxy_b}</span>
                    <span style="background:#d4af37; color:black; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{gold_b}</span>
                </div>
                <p style="margin-top:10px; color:#000; font-size:11px; font-weight:bold;">📅 Next: {info_next}</p>
            </div>""", unsafe_allow_html=True)

    # Section 1
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📌 Primary Gold & DXY Drivers</h2>", unsafe_allow_html=True)
    cols1 = st.columns(2)
    main_ind = {'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'}, 'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'}, 'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'}, 'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'}}
    for i, (name, info) in enumerate(main_ind.items()):
        try:
            data = fred.get_series(info['id'])
            latest, prev = data.iloc[-1], data.iloc[-2]
            if 'CPI' in name: color, bg, msg, d_b, g_b = ("#d32f2f", "#fff5f5", "Inflation barh rahi hai." if latest > prev else "Inflation cooling hai.", "DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("#388e3c", "#f1f8e9", "Inflation cooling hai.", "DXY: BEARISH", "GOLD: BULLISH")
            elif 'NFP' in name: color, bg, msg, d_b, g_b = ("#388e3c", "#f1f8e9", "Jobs data strong hai.", "DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("#d32f2f", "#fff5f5", "Jobs weak hai.", "DXY: BEARISH", "GOLD: BULLISH")
            elif 'Unemployment' in name: color, bg, msg, d_b, g_b = ("#d32f2f", "#fff5f5", "Berozgari barh rahi hai.", "DXY: BEARISH", "GOLD: BULLISH") if latest > prev else ("#388e3c", "#f1f8e9", "Berozgari kam hui hai.", "DXY: BULLISH", "GOLD: BEARISH")
            else: color, bg, msg, d_b, g_b = ("#1976d2", "#e3f2fd", f"Current Rate: {latest}%", "DXY: STABLE", "GOLD: PRESSURE")
            draw_meter(cols1[i%2], name, latest, prev, info['next'], msg, d_b, g_b, color, bg, 280)
        except: st.error(f"Error {name}")

    # Section 2
    st.markdown("<hr><h2 style='text-align: center; color: #2c3e50;'>🌊 Liquidity & Recession Risk</h2>", unsafe_allow_html=True)
    cols2 = st.columns(4)
    liq_ind = {'M2 Money Supply': {'id': 'WM2NS', 'next': 'Weekly'}, 'Yield Curve (10Y-2Y)': {'id': 'T10Y2Y', 'next': 'Daily'}, 'PCE Inflation': {'id': 'PCEPI', 'next': 'Feb 27, 2026'}, 'Consumer Sentiment': {'id': 'UMCSENT', 'next': 'Feb 20, 2026'}}
    for i, (name, info) in enumerate(liq_ind.items()):
        try:
            data = fred.get_series(info['id'])
            latest, prev = data.iloc[-1], data.iloc[-2]
            color, d_b, g_b = "#1976d2", "DXY: TREND", "GOLD: TREND"
            if 'Curve' in name: color, d_b, g_b = ("#d32f2f", "DXY: RISK", "GOLD: BUY") if latest < 0 else ("#388e3c", "DXY: OK", "GOLD: HOLD")
            draw_meter(cols2[i], name, latest, prev, info['next'], "Macro trend.", d_b, g_b, color, "#fafafa", 200)
        except: st.write(f"Error {name}")

    # Section 3
    st.markdown("<hr><h2 style='text-align: center; color: #2c3e50;'>📊 Yields & Fed Target</h2>", unsafe_allow_html=True)
    cols3 = st.columns(4)
    yield_ind = {'US 10Y Yield': {'id': 'DGS10', 'next': 'Daily'}, '10Y Breakeven': {'id': 'T10YIE', 'next': 'Daily'}, 'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}}
    for i, (name, info) in enumerate(yield_ind.items()):
        try:
            data = fred.get_series(info['id'])
            latest, prev = data.iloc[-1], data.iloc[-2]
            d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
            draw_meter(cols3[i], name, latest, prev, info['next'], "Yield Analysis", d_b, g_b, "#1e3c72", "#fafafa", 200)
        except: st.write(f"Error {name}")

    try:
        cpi_data = fred.get_series('CPIAUCSL')
        curr_inf = ((cpi_data.iloc[-1] - cpi_data.iloc[-13]) / cpi_data.iloc[-13]) * 100
        draw_meter(cols3[3], "Inf. vs 2% Target", curr_inf, 2.0, "Feb 13", f"Gap: {curr_inf-2:.2f}%", "Fed Goal", "Macro Bias", "red", "#fafafa", 200)
    except: st.write("Target Error")

    # Section 4
    st.markdown("<hr><h2 style='text-align: center; color: #d4af37;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)
    cot_reports = [{"date": "Feb 06, 2026", "longs": 285000, "shorts": 45000, "analysis": "Smart Money ne mazeed longs add kiye hain. Gold par bullish pressure barh raha hai kyunke shorts cover ho rahay hain. ICT order block par buy setups talash karein."}]
    report = cot_reports[0]
    sentiment = (report['longs'] / (report['longs'] + report['shorts'])) * 100
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -30px; color: #ffffff; font-size: 16px;'>Bullish Sentiment Index</p>", unsafe_allow_html=True)
        fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=sentiment, gauge={'bar': {'color': "#d4af37"}, 'axis': {'range': [0, 100]}}))
        fig_cot = go.Figure(data=[go.Pie(values=[sentiment, 100-sentiment], hole=.75, direction='clockwise', sort=False, marker=dict(colors=['#d4af37', '#f0f0f0']), textinfo='none', hoverinfo='none')])
        fig_cot.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=300, annotations=[dict(text=f"{int(sentiment)}%", x=0.5, y=0.55, font_size=40, showarrow=False, font_family="Arial Black", font_color="#d4af37"), dict(text="BULLISH POWER", x=0.5, y=0.42, font_size=12, showarrow=False, font_color="#555", font_weight="bold")])
        st.plotly_chart(fig_cot, use_container_width=True)
    with col_r:
        st.markdown(f"""<div style="background:white; border:2px solid #d4af37; padding:25px; border-radius:15px; margin-top:20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><h3 style="color:#d4af37; margin-top:0;">Expert Analysis (XAUUSD)</h3><p style="font-size:14px; color:#333; line-height:1.6;">{report['analysis']}</p><hr><div style="display:flex; justify-content:space-around; text-align:center;"><div><p style="margin:0; font-size:11px; color:#777;">Longs</p><b style="color:#388e3c; font-size:16px;">{report['longs']:,}</b></div><div><p style="margin:0; font-size:11px; color:#777;">Shorts</p><b style="color:#d32f2f; font-size:16px;">{report['shorts']:,}</b></div><div><p style="margin:0; font-size:11px; color:#777;">Net</p><b style="color:#1e3c72; font-size:16px;">{report['longs']-report['shorts']:,}</b></div></div></div>""", unsafe_allow_html=True)

# ==========================================
# MAIN CONTROLLER
# ==========================================

import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime
import base64
import time
import streamlit.components.v1 as components  # Required for rendering HTML reports

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Rollic Trades Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🪙"
)

# --- 2. DARK PREMIUM CSS ---
st.markdown("""
    <style>
    /* Navbar */
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-bottom: 2px solid #d4af37; z-index: 99999;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    
    /* Footer Styling */
    .footer {
        width: 100%;
        background-color: #0e1117;
        padding: 40px 20px;
        border-top: 1px solid #333;
        margin-top: 50px;
        color: #666;
        font-size: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .footer-logo-row {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    /* Smart Cards */
    .smart-card {
        background: #1e1e1e; border: 1px solid #333; border-radius: 12px;
        padding: 20px; text-align: center; transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .smart-card:hover {
        border-color: #d4af37; transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(212, 175, 55, 0.2);
    }
    .card-title { color: white; font-size: 18px; font-weight: bold; margin: 0; }
    .card-desc { color: #aaa; font-size: 12px; margin-top: 5px; }

    /* Buttons Override */
    div.stButton > button {
        background-color: #262730; color: white; border: 1px solid #555; border-radius: 8px;
    }
    div.stButton > button:hover { border-color: #d4af37; color: #d4af37; }
    </style>
""", unsafe_allow_html=True)

# --- 3. GLOBAL VARIABLES ---
ADMIN_USER = "admin"
ADMIN_PASS = "Rollic@786"
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"

# --- DEFAULT GOLD REPORT HTML (Your provided code) ---
DEFAULT_REPORT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gold Institutional Analysis | GC1! H4</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root { --gold-primary: #D4AF37; --gold-light: #F5D769; --bg-primary: #000000; --bg-card: #111111; --text-primary: #FFFFFF; --red: #FF453A; --green: #30D158; }
        body { font-family: 'Inter', sans-serif; background: var(--bg-primary); color: var(--text-primary); overflow-x: hidden; }
        .main-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .hero-section { text-align: center; padding: 50px 20px; }
        .hero-title { font-size: 40px; font-weight: 800; color: var(--gold-primary); margin-bottom: 10px; }
        .hero-subtitle { font-size: 18px; color: #aaa; }
        .section { margin-bottom: 40px; padding: 20px; background: var(--bg-card); border-radius: 20px; border: 1px solid rgba(212, 175, 55, 0.15); }
        .section-header { font-size: 22px; font-weight: 700; color: white; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
        .stat-card { background: #0a0a0a; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center; }
        .stat-value { font-size: 24px; font-weight: bold; color: var(--gold-primary); }
        .stat-label { font-size: 12px; color: #777; margin-bottom: 5px; }
        .logic-box { background: rgba(212, 175, 55, 0.05); border: 1px solid rgba(212, 175, 55, 0.2); padding: 15px; border-radius: 10px; margin-top: 15px; }
        .confluence-table { width: 100%; border-collapse: collapse; }
        .confluence-table th, .confluence-table td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
        .confluence-table th { color: var(--gold-primary); font-size: 14px; }
        .check-icon { color: var(--green); }
        .scenarios-container { display: flex; flex-direction: column; gap: 15px; }
        .scenario-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-left: 4px solid var(--gold-primary); }
        .scenario-title { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
        .bottom-line { text-align: center; padding: 30px; background: linear-gradient(135deg, rgba(212,175,55,0.1), transparent); border-radius: 20px; border: 1px solid var(--gold-primary); }
    </style>
</head>
<body>
    <div class="main-container">
        <section class="hero-section">
            <h1 class="hero-title">Gold Institutional Analysis</h1>
            <p class="hero-subtitle">Smart Money Positioning & Liquidity Decode — <strong>APR 26 Contract</strong></p>
        </section>

        <section class="section">
            <div class="section-header">📊 Step A — Futures Data</div>
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-label">Current Price</div><div class="stat-value" style="color:#FF453A">5,086.3</div></div>
                <div class="stat-card"><div class="stat-label">Total Volume</div><div class="stat-value">129,968</div></div>
                <div class="stat-card"><div class="stat-label">OI Change</div><div class="stat-value" style="color:#FF453A">+1,199</div></div>
                <div class="stat-card"><div class="stat-label">Block Trades</div><div class="stat-value">475</div></div>
            </div>
            <div class="logic-box">
                <strong>Logic:</strong> Price DOWN + OI UP = 🔴 <strong>SHORT BUILDUP</strong>. Smart Money is adding fresh shorts.
            </div>
        </section>

        <section class="section">
            <div class="section-header">🎯 Trade Scenarios</div>
            <div class="scenarios-container">
                <div class="scenario-card">
                    <div class="scenario-title">Scenario A: Sell the Rally (70% Prob)</div>
                    <p>Agar price <strong>5269-5311</strong> zone test kare, toh SHORT entry dekhna. Target: 5020 (Liquidity Sweep).</p>
                </div>
                <div class="scenario-card" style="border-left-color: #FF453A;">
                    <div class="scenario-title">Scenario B: Continuation Short</div>
                    <p>Break below <strong>5036</strong> -> Direct fall to 4979.</p>
                </div>
            </div>
        </section>

        <section class="bottom-line">
            <h3>🎯 VERDICT: BEARISH</h3>
            <p>Smart Money is actively building shorts. <strong>Best Trade:</strong> Short rallies into 5280 zone targeting 5020.</p>
        </section>
    </div>
</body>
</html>
"""

# --- YOUR CALCULATOR HTML CODE ---
CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root { --bg-color: #1A1A1A; --text-color: #D4AF37; --primary-color: #B8860B; --input-border: #B8860B; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Montserrat', sans-serif; }
        body { background-color: transparent; padding: 20px; display: flex; justify-content: center; align-items: center; color: var(--text-color); }
        .container { background: rgba(26, 26, 26, 0.95); padding: 25px; border-radius: 20px; box-shadow: 0 0 25px var(--primary-color); width: 100%; max-width: 500px; border: 2px solid var(--primary-color); text-align: center; }
        h1 { color: var(--primary-color); margin-bottom: 25px; font-size: 1.5rem; text-transform: uppercase; }
        .input-group { margin-bottom: 20px; text-align: left; }
        label { display: block; margin-bottom: 8px; color: var(--primary-color); font-weight: 600; }
        input { width: 100%; padding: 12px; border: 2px solid var(--input-border); border-radius: 10px; background: #111; color: #fff; }
        button { width: 100%; padding: 15px; background: linear-gradient(135deg, var(--primary-color), #D4AF37); color: #1A1A1A; border: none; border-radius: 10px; font-weight: 600; cursor: pointer; margin-top: 20px; }
        #result { margin-top: 15px; font-size: 2.5rem; font-weight: bold; color: #D4AF37; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lot Size Calculator</h1>
        <div class="input-group"><label>Account Size ($)</label><input type="number" id="accountSize" placeholder="Enter balance"></div>
        <div class="input-group"><label>Risk Percentage (%)</label><input type="number" id="riskPercent" placeholder="Enter risk %"></div>
        <div class="input-group"><label>Stop Loss (Pips)</label><input type="number" id="stopLoss" placeholder="Enter stop loss"></div>
        <button onclick="calculateLotSize()">Calculate</button>
        <div id="result"></div>
    </div>
    <script>
        function calculateLotSize() {
            const acc = parseFloat(document.getElementById('accountSize').value);
            const risk = parseFloat(document.getElementById('riskPercent').value);
            const sl = parseFloat(document.getElementById('stopLoss').value);
            if (!acc || !risk || !sl) return;
            const res = ((acc * risk / 100) / (sl * 10)).toFixed(2);
            const r = document.getElementById('result');
            r.textContent = `${res} Lot`; r.style.display = 'block';
        }
    </script>
</body>
</html>
"""

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_role' not in st.session_state: st.session_state['user_role'] = None
if 'username' not in st.session_state: st.session_state['username'] = None
if 'current_page' not in st.session_state: st.session_state['current_page'] = 'home'
if 'users_db' not in st.session_state:
    data = {"Username": ["admin", "user"], "Password": ["Rollic@786", "123"], "Role": ["Admin", "User"], "Status": ["Active", "Active"]}
    st.session_state['users_db'] = pd.DataFrame(data)

# REPORT DATABASE (HTML Reports)
if 'html_reports' not in st.session_state:
    st.session_state['html_reports'] = {
        datetime.now().strftime("%Y-%m-%d"): DEFAULT_REPORT_HTML
    }

# --- 5. COMPONENT FUNCTIONS ---

def render_navbar():
    st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""<div class="navbar"><span style="color: #d4af37; font-weight: bold; font-size: 18px; margin-right: 20px;">🪙 ROLLIC TRADES</span></div>""", unsafe_allow_html=True)
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
        with col1:
            if st.button("🏠 Home", use_container_width=True): st.session_state['current_page'] = 'home'; st.rerun()
        with col2:
            if st.button("📊 Macro", use_container_width=True): st.session_state['current_page'] = 'macro'; st.rerun()
        with col3:
            if st.button("📄 Reports", use_container_width=True): st.session_state['current_page'] = 'reports'; st.rerun()
        with col4:
            if st.button("🧮 Calculator", use_container_width=True): st.session_state['current_page'] = 'calculator'; st.rerun()
        with col5:
            if st.session_state['user_role'] == 'Admin':
                if st.button("⚙️ Admin", use_container_width=True): st.session_state['current_page'] = 'admin'; st.rerun()
        with col6:
            if st.button("Log Out", use_container_width=True): st.session_state['logged_in'] = False; st.rerun()
    st.markdown("---")

def render_footer():
    st.markdown(f"""
        <div class="footer">
            <div class="footer-logo-row">
                <img src="{LOGO_URL}" width="40" style="border-radius: 50%; border: 2px solid #444; margin-right: 15px;">
                <span style="color: #d4af37; font-weight: bold; font-size: 16px; letter-spacing: 1px;">ROLLIC TRADES</span>
            </div>
            <p style="max-width: 800px; line-height: 1.5;">
                <strong>Risk Disclaimer:</strong> Trading foreign exchange, gold, and indices carries a high level of risk. 
                Analysis provided is for educational purposes only. Trade responsibly.
            </p>
            <p style="margin-top: 15px; color: #444;">© 2026 Rollic Trades. All Rights Reserved.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE: LOGIN
# ==========================================
def login_page():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""<div style="text-align: center; margin-top: 50px;"><img src="{LOGO_URL}" width="150" style="border-radius: 50%; border: 3px solid #d4af37;"><h2 style="color: white; margin-top: 15px;">ROLLIC TRADES</h2></div>""", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login Access", use_container_width=True):
            db = st.session_state['users_db']
            match = db[(db['Username'] == username) & (db['Password'] == password)]
            if not match.empty:
                st.session_state['logged_in'] = True; st.session_state['user_role'] = match.iloc[0]['Role']; st.session_state['username'] = username; st.rerun()
            else: st.error("Access Denied")

# ==========================================
# PAGE: HOME
# ==========================================
def home_page():
    st.markdown(f"""<div style="text-align: center; padding-top: 20px; padding-bottom: 10px;"><img src="{LOGO_URL}" width="180" style="border-radius: 50%; border: 4px solid #d4af37; box-shadow: 0 0 30px rgba(212, 175, 55, 0.3);"></div>""", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:white;'>Welcome, {st.session_state['username']}</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class="smart-card"><div style="font-size:30px;">📊</div><p class="card-title">Macro Terminal</p><p class="card-desc">Live Data & Yields</p></div>""", unsafe_allow_html=True)
        if st.button("Open Terminal", use_container_width=True): st.session_state['current_page'] = 'macro'; st.rerun()
    with c2:
        st.markdown("""<div class="smart-card"><div style="font-size:30px;">📄</div><p class="card-title">Daily Reports</p><p class="card-desc">Market Analysis</p></div>""", unsafe_allow_html=True)
        if st.button("View Reports", use_container_width=True): st.session_state['current_page'] = 'reports'; st.rerun()
    with c3:
        st.markdown("""<div class="smart-card"><div style="font-size:30px;">🧮</div><p class="card-title">Risk Calculator</p><p class="card-desc">Lot Size Manager</p></div>""", unsafe_allow_html=True)
        if st.button("Open Calculator", use_container_width=True): st.session_state['current_page'] = 'calculator'; st.rerun()
    with c4: st.markdown("""<div class="smart-card" style="opacity: 0.5;"><div style="font-size:30px;">🎓</div><p class="card-title">Academy</p><p class="card-desc">Coming Soon</p></div>""", unsafe_allow_html=True)

# ==========================================
# PAGE: CALCULATOR
# ==========================================
def calculator_page():
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>RISK MANAGEMENT TOOL</h2>", unsafe_allow_html=True)
    components.html(CALCULATOR_HTML, height=750, scrolling=True)

# ==========================================
# PAGE: ADMIN PANEL
# ==========================================
def admin_panel():
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>ADMIN CONSOLE</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📄 Upload Reports", "👥 User DB"])
    
    with tab1:
        st.markdown("### Upload HTML Report")
        st.info("Upload your analysis HTML file here. It will be rendered exactly as coded.")
        
        uploaded_file = st.file_uploader("Select HTML File", type=['html'])
        report_date = st.date_input("Report Date", datetime.now())
        
        if st.button("Publish HTML Report"):
            if uploaded_file:
                # Read HTML file as string
                html_string = uploaded_file.getvalue().decode("utf-8")
                date_key = report_date.strftime("%Y-%m-%d")
                
                # Save to session state
                st.session_state['html_reports'][date_key] = html_string
                st.success(f"✅ Report for {date_key} published successfully!")
            else:
                st.error("Please select an HTML file.")

    with tab2:
        st.dataframe(st.session_state['users_db'], use_container_width=True)

# ==========================================
# PAGE: REPORTS PAGE (HTML RENDERER)
# ==========================================
def reports_page():
    # --- HEADER ---
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{LOGO_URL}" width="100" style="border-radius: 50%; border: 3px solid #d4af37; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);">
                <h2 style="color: white; margin-top: 10px; margin-bottom: 0;">EXPERT ANALYSIS</h2>
                <p style="color: #888; font-size: 14px; letter-spacing: 2px;">DAILY MARKET REPORT</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_r:
        dates = list(st.session_state['html_reports'].keys())
        dates.sort(reverse=True)
        if dates:
            sel_date = st.selectbox("📅 Archive", dates, label_visibility="visible")
        else:
            sel_date = None
            st.markdown("<br><p style='text-align:right; color:#666;'>No Reports</p>", unsafe_allow_html=True)
            
    st.markdown("---")
    
    # --- REPORT DISPLAY ---
    if sel_date:
        html_content = st.session_state['html_reports'][sel_date]
        # Render HTML inside an iframe to keep styles isolated and correct
        components.html(html_content, height=1500, scrolling=True)
    else:
        st.info("No report selected. Please upload from Admin Panel.")

# ==========================================
# PAGE: MACRO DASHBOARD
# ==========================================
def macro_dashboard():
    st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;"><h1 style="margin: 0; font-family: 'Arial Black', sans-serif;">ROLLIC TRADES MACRO TERMINAL</h1><p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Grade Analysis</p></div>""", unsafe_allow_html=True)
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
            st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:12px; border-radius:12px; text-align:center; margin:-30px auto 35px auto; max-width: 290px;"><p style="margin:0; font-size:12px; font-weight:500; color:#333;">{msg}</p><div style="margin-top:8px;"><span style="background:#1e3c72; color:white; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{dxy_b}</span> <span style="background:#d4af37; color:black; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{gold_b}</span></div><p style="margin-top:10px; color:#000; font-size:11px; font-weight:bold;">📅 Next: {info_next}</p></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    # Demo data as placeholder
    draw_meter(c1, "CPI Inflation", 3.2, 3.1, "Feb 13", "Inflation Rising", "BULLISH", "BEARISH", "#d32f2f", "#fff5f5")
    draw_meter(c2, "Fed Rates", 5.5, 5.5, "Mar 18", "Rates Steady", "STABLE", "NEUTRAL", "#1976d2", "#e3f2fd")

    # Section 4: COT Ring
    st.markdown("<hr><h2 style='text-align: center; color: #d4af37;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -30px; color: #ffffff; font-size: 16px;'>Bullish Sentiment Index</p>", unsafe_allow_html=True)
        fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=75, gauge={'bar': {'color': "#d4af37"}, 'axis': {'range': [0, 100]}}))
        fig_cot = go.Figure(data=[go.Pie(values=[75, 25], hole=.75, direction='clockwise', sort=False, marker=dict(colors=['#d4af37', '#f0f0f0']), textinfo='none', hoverinfo='none')])
        fig_cot.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=300, annotations=[dict(text="75%", x=0.5, y=0.55, font_size=40, showarrow=False, font_family="Arial Black", font_color="#d4af37"), dict(text="BULLISH POWER", x=0.5, y=0.42, font_size=12, showarrow=False, font_color="#555", font_weight="bold")])
        st.plotly_chart(fig_cot, use_container_width=True)
    with col_r:
        st.markdown(f"""<div style="background:white; border:2px solid #d4af37; padding:25px; border-radius:15px; margin-top:20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><h3 style="color:#d4af37; margin-top:0;">Expert Analysis (XAUUSD)</h3><p style="font-size:14px; color:#333; line-height:1.6;">Smart Money is accumulating longs. We see strong rejection at 2000 level.</p><hr><div style="display:flex; justify-content:space-around; text-align:center;"><div><p style="margin:0; font-size:11px; color:#777;">Longs</p><b style="color:#388e3c; font-size:16px;">250k</b></div><div><p style="margin:0; font-size:11px; color:#777;">Shorts</p><b style="color:#d32f2f; font-size:16px;">50k</b></div><div><p style="margin:0; font-size:11px; color:#777;">Net</p><b style="color:#1e3c72; font-size:16px;">200k</b></div></div></div>""", unsafe_allow_html=True)

# ==========================================
# MAIN CONTROLLER
# ==========================================
if not st.session_state['logged_in']:
    login_page()
    render_footer()
else:
    render_navbar()
    if st.session_state['current_page'] == 'home': home_page()
    elif st.session_state['current_page'] == 'macro': macro_dashboard()
    elif st.session_state['current_page'] == 'reports': reports_page()
    elif st.session_state['current_page'] == 'calculator': calculator_page()
    elif st.session_state['current_page'] == 'admin': admin_panel()
    render_footer()

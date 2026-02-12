import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import json
import math

# ============================================
# 1. PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Rollic Trades Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🪙"
)

# ============================================
# 2. ALL CSS STYLES
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    .stApp {
        background: #000000;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    .stDeployButton {display: none;}

    ::-webkit-scrollbar {width: 5px;}
    ::-webkit-scrollbar-track {background: #000;}
    ::-webkit-scrollbar-thumb {background: #222; border-radius: 10px;}
    ::-webkit-scrollbar-thumb:hover {background: #d4af37;}

    /* BUTTONS */
    div.stButton > button {
        background: rgba(255,255,255,0.03) !important;
        color: rgba(255,255,255,0.7) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: rgba(212,175,55,0.1) !important;
        color: #d4af37 !important;
        border-color: rgba(212,175,55,0.25) !important;
        transform: translateY(-1px) !important;
    }
    .gold-btn > div > button {
        background: linear-gradient(135deg, #d4af37, #b8860b) !important;
        color: #000 !important;
        border: none !important;
        font-weight: 700 !important;
    }
    .gold-btn > div > button:hover {
        box-shadow: 0 8px 30px rgba(212,175,55,0.25) !important;
        color: #000 !important;
    }

    /* NAV BUTTONS - SPECIAL STYLE */
    .nav-btn > div > button {
        background: transparent !important;
        color: rgba(255,255,255,0.6) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
    }
    .nav-btn > div > button:hover {
        background: rgba(212,175,55,0.08) !important;
        color: #d4af37 !important;
        border-color: rgba(212,175,55,0.2) !important;
    }
    .nav-btn-active > div > button {
        background: rgba(212,175,55,0.12) !important;
        color: #d4af37 !important;
        border-color: rgba(212,175,55,0.25) !important;
    }

    /* INPUTS */
    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        padding: 14px 16px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 3px rgba(212,175,55,0.08) !important;
    }
    div[data-testid="stTextInput"] label {
        color: rgba(255,255,255,0.4) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
    }

    /* SELECTBOX */
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
    }
    div[data-testid="stSelectbox"] label {
        color: rgba(255,255,255,0.4) !important;
    }

    /* TABS */
    div[data-testid="stTabs"] button {
        color: rgba(255,255,255,0.4) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        background: transparent !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #d4af37 !important;
        border-bottom-color: #d4af37 !important;
    }

    /* FILE UPLOADER */
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.015) !important;
        border: 2px dashed rgba(212,175,55,0.15) !important;
        border-radius: 16px !important;
    }

    /* DATE INPUT */
    div[data-testid="stDateInput"] input {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* METRIC */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 18px;
    }
    div[data-testid="stMetric"] label {
        color: rgba(255,255,255,0.3) !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #d4af37 !important;
        font-weight: 700 !important;
    }

    /* GLASS CARD */
    .glass-card {
        background: rgba(255,255,255,0.025);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 28px;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent);
    }
    .glass-card:hover {
        border-color: rgba(212,175,55,0.15);
        transform: translateY(-3px);
        box-shadow: 0 16px 48px rgba(212,175,55,0.06);
    }

    /* GRADIENT TEXT */
    .gradient-text {
        background: linear-gradient(135deg, #d4af37 0%, #f5d769 30%, #d4af37 60%, #b8860b 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3.5s ease-in-out infinite;
    }
    @keyframes shimmer {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 200% center; }
    }

    /* GLOW RING */
    .glow-ring {
        border-radius: 50%;
        border: 2.5px solid #d4af37;
        box-shadow: 0 0 12px rgba(212,175,55,0.25),
                    0 0 30px rgba(212,175,55,0.1);
    }

    /* PULSE DOT */
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(48,209,88,0.4); }
        50% { box-shadow: 0 0 0 8px rgba(48,209,88,0); }
    }
    .pulse-dot {
        width: 7px; height: 7px;
        background: #30d158;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-glow 2s infinite;
    }

    /* FLOAT */
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    .float-anim { animation: float 5s ease-in-out infinite; }

    /* HR */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent) !important;
        margin: 35px 0 !important;
    }

    /* TICKER */
    .ticker-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 16px 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .ticker-card:hover {
        border-color: rgba(212,175,55,0.15);
    }

    /* SECTION HEADERS */
    .section-eyebrow {
        font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
        color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 6px;
        text-align: center;
    }
    .section-title {
        font-size: 30px; font-weight: 800; color: #fff;
        text-align: center; margin-bottom: 6px;
    }
    .section-subtitle {
        font-size: 14px; color: rgba(255,255,255,0.25);
        text-align: center; margin-bottom: 35px;
    }

    /* HIDE ANCHORS */
    h1 a, h2 a, h3 a { display: none !important; }

    /* ANIMATED TRADING BANNER */
    @keyframes ticker-scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .trading-ticker-wrapper {
        overflow: hidden;
        background: rgba(212,175,55,0.04);
        border: 1px solid rgba(212,175,55,0.08);
        border-radius: 12px;
        padding: 10px 0;
        margin-bottom: 30px;
    }
    .trading-ticker-content {
        display: flex;
        white-space: nowrap;
        animation: ticker-scroll 30s linear infinite;
    }
    .ticker-item {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 25px;
        font-size: 12px;
        font-weight: 600;
        color: rgba(255,255,255,0.5);
    }
    .ticker-item .price {
        color: #d4af37;
        font-family: 'JetBrains Mono', monospace;
    }
    .ticker-item .up { color: #30d158; }
    .ticker-item .down { color: #ff453a; }

    /* ADMIN STAT CARD */
    .admin-stat {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    .admin-stat-value {
        font-size: 36px; font-weight: 800;
        color: #d4af37;
        font-family: 'JetBrains Mono', monospace;
    }
    .admin-stat-label {
        font-size: 10px; letter-spacing: 1.5px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.3);
        font-weight: 600; margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 3. GLOBAL VARIABLES
# ============================================
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60"

# ============================================
# 4. DEFAULT REPORT HTML
# ============================================
DEFAULT_REPORT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    body{font-family:'Inter',sans-serif;background:#000;color:#fff;overflow-x:hidden;}
    .mc{max-width:1000px;margin:0 auto;padding:30px 20px;}
    .hero{text-align:center;padding:60px 20px;position:relative;}
    .hero::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;background:radial-gradient(circle,rgba(212,175,55,0.08)0%,transparent 70%);pointer-events:none;}
    .ey{font-size:12px;letter-spacing:4px;text-transform:uppercase;color:#d4af37;font-weight:600;margin-bottom:15px;}
    .ht{font-size:48px;font-weight:800;background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px;}
    .hs{font-size:16px;color:rgba(255,255,255,0.4);}
    .sec{margin-bottom:30px;padding:30px;background:rgba(255,255,255,0.03);border-radius:24px;border:1px solid rgba(255,255,255,0.06);position:relative;overflow:hidden;}
    .sec::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.2),transparent);}
    .sh{font-size:13px;font-weight:700;color:#d4af37;letter-spacing:2px;text-transform:uppercase;margin-bottom:25px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.04);}
    .sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:15px;}
    .sc{background:rgba(255,255,255,0.02);padding:20px 15px;border-radius:16px;border:1px solid rgba(255,255,255,0.04);text-align:center;}
    .sl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}
    .sv{font-size:28px;font-weight:800;color:#d4af37;font-family:'JetBrains Mono',monospace;}
    .lb{background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);padding:20px;border-radius:16px;margin-top:20px;font-size:14px;line-height:1.7;color:rgba(255,255,255,0.7);}
    .lb strong{color:#fff;}
    .scc{background:rgba(255,255,255,0.02);padding:25px;border-radius:20px;border:1px solid rgba(255,255,255,0.04);margin-bottom:15px;border-left:3px solid #d4af37;}
    .st{font-size:16px;font-weight:700;margin-bottom:8px;color:#fff;}
    .scc p{color:rgba(255,255,255,0.5);font-size:14px;line-height:1.6;}
    .bl{text-align:center;padding:40px;background:rgba(212,175,55,0.03);border-radius:24px;border:1px solid rgba(212,175,55,0.15);}
    .bl h3{font-size:28px;font-weight:800;margin-bottom:10px;background:linear-gradient(135deg,#d4af37,#f5d769);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .bl p{color:rgba(255,255,255,0.5);font-size:15px;}
    .bl strong{color:#fff;}
</style>
</head>
<body>
<div class="mc">
    <section class="hero"><p class="ey">Institutional Intelligence</p><h1 class="ht">Gold Analysis</h1><p class="hs">Smart Money Positioning — APR 26 Contract</p></section>
    <section class="sec"><div class="sh">Futures Data</div><div class="sg"><div class="sc"><div class="sl">Price</div><div class="sv" style="color:#FF453A">5,086</div></div><div class="sc"><div class="sl">Volume</div><div class="sv">129,968</div></div><div class="sc"><div class="sl">OI Change</div><div class="sv" style="color:#FF453A">+1,199</div></div><div class="sc"><div class="sl">Blocks</div><div class="sv">475</div></div></div><div class="lb"><strong>Logic:</strong> Price DOWN + OI UP = SHORT BUILDUP</div></section>
    <section class="sec"><div class="sh">Trade Scenarios</div><div class="scc"><div class="st">Scenario A: Sell Rally (70%)</div><p>Test <strong>5269-5311</strong> zone SHORT. Target: 5020</p></div><div class="scc" style="border-left-color:#FF453A;"><div class="st">Scenario B: Continuation</div><p>Below <strong>5036</strong> fall to 4979</p></div></section>
    <section class="bl"><h3>VERDICT: BEARISH</h3><p>Short rallies into 5280 targeting 5020</p></section>
</div>
</body>
</html>
"""

# ============================================
# 5. CALCULATOR HTML
# ============================================
CALCULATOR_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:transparent;display:flex;justify-content:center;padding:30px;font-family:'Inter',sans-serif;}
    .c{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:28px;padding:40px;width:100%;max-width:480px;position:relative;overflow:hidden;}
    .c::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.3),transparent);}
    .ce{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.6);font-weight:600;text-align:center;margin-bottom:8px;}
    .ct{font-size:28px;font-weight:800;text-align:center;background:linear-gradient(135deg,#d4af37,#f5d769);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:35px;}
    .ig{margin-bottom:22px;}
    .ig label{display:block;margin-bottom:8px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.35);}
    .ig input{width:100%;padding:16px 20px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;color:#fff;font-size:16px;font-family:'Inter',sans-serif;outline:none;transition:all 0.3s ease;}
    .ig input:focus{border-color:rgba(212,175,55,0.5);box-shadow:0 0 0 4px rgba(212,175,55,0.08);}
    .ig input::placeholder{color:rgba(255,255,255,0.15);}
    .cb{width:100%;padding:18px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#000;border:none;border-radius:16px;font-size:15px;font-weight:700;cursor:pointer;margin-top:15px;transition:all 0.3s ease;text-transform:uppercase;}
    .cb:hover{box-shadow:0 8px 40px rgba(212,175,55,0.3);transform:translateY(-2px);}
    #result{margin-top:30px;text-align:center;display:none;padding:30px;border-radius:20px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);}
    .rl{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}
    .rv{font-size:48px;font-weight:800;background:linear-gradient(135deg,#d4af37,#f5d769);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .rr{font-size:13px;color:rgba(255,255,255,0.3);margin-top:8px;}
</style>
</head>
<body>
<div class="c">
    <p class="ce">Risk Management</p>
    <h1 class="ct">Position Sizer</h1>
    <div class="ig"><label>Account Balance</label><input type="number" id="a" placeholder="$10,000"></div>
    <div class="ig"><label>Risk Per Trade (%)</label><input type="number" id="r" placeholder="2.0"></div>
    <div class="ig"><label>Stop Loss (Pips)</label><input type="number" id="s" placeholder="50"></div>
    <button class="cb" onclick="calc()">Calculate Position</button>
    <div id="result"><p class="rl">Recommended Lot Size</p><p class="rv" id="lv"></p><p class="rr" id="ra"></p></div>
</div>
<script>
function calc(){
    const a=parseFloat(document.getElementById('a').value);
    const r=parseFloat(document.getElementById('r').value);
    const s=parseFloat(document.getElementById('s').value);
    if(!a||!r||!s)return;
    const ra=(a*r/100);
    const l=(ra/(s*10)).toFixed(2);
    document.getElementById('lv').textContent=l+' Lot';
    document.getElementById('ra').textContent='Risk: $'+ra.toFixed(2);
    document.getElementById('result').style.display='block';
}
</script>
</body>
</html>
"""

# ============================================
# 6. SESSION STATE
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = pd.DataFrame({
        "Username": ["admin", "user"],
        "Password": ["Rollic@786", "123"],
        "Role": ["Admin", "User"],
        "Status": ["Active", "Active"],
        "Created": [datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")]
    })
if 'html_reports' not in st.session_state:
    st.session_state['html_reports'] = {
        datetime.now().strftime("%Y-%m-%d"): DEFAULT_REPORT_HTML
    }
if 'pages_db' not in st.session_state:
    st.session_state['pages_db'] = {}


# ============================================
# 7. MINI CHART FUNCTION
# ============================================
def render_mini_chart(prices, color="#d4af37"):
    r_val = int(color.lstrip("#")[0:2], 16)
    g_val = int(color.lstrip("#")[2:4], 16)
    b_val = int(color.lstrip("#")[4:6], 16)
    fill_color = f"rgba({r_val},{g_val},{b_val},0.06)"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=prices, mode='lines',
        line=dict(color=color, width=2.5, shape='spline'),
        fill='tozeroy', fillcolor=fill_color, hoverinfo='y'
    ))
    fig.update_layout(
        height=140, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
        showlegend=False
    )
    return fig


# ============================================
# 8. FIXED HEADER WITH MENU ON ALL PAGES
# ============================================
def render_header():
    # Spacer for fixed header
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    user_initial = "U"
    if st.session_state['username']:
        user_initial = st.session_state['username'][0].upper()

    # HTML HEADER BAR with logo
    st.markdown(f"""
    <div style="
        background: rgba(0,0,0,0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 12px 24px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="{LOGO_URL}" width="34" height="34"
                 style="border-radius: 50%; object-fit: cover;
                        border: 2px solid rgba(212,175,55,0.4);">
            <span style="font-size: 14px; font-weight: 700; letter-spacing: 2px;
                        color: #d4af37;">ROLLIC TRADES</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 11px; color: rgba(255,255,255,0.35);
                        font-weight: 500;">{st.session_state['username']}</span>
            <div style="width: 28px; height: 28px; border-radius: 50%;
                        background: linear-gradient(135deg, #d4af37, #8b6914);
                        display: flex; align-items: center; justify-content: center;
                        font-size: 11px; font-weight: 800; color: #000;">
                {user_initial}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # NAVIGATION BUTTONS - ALWAYS SHOWN
    current = st.session_state['current_page']
    is_admin = st.session_state['user_role'] == 'Admin'

    if is_admin:
        nav_cols = st.columns([1, 1, 1, 1, 1, 1])
    else:
        nav_cols = st.columns([1, 1, 1, 1, 1])

    pages = [
        ("home", "🏠 Home"),
        ("macro", "📊 Macro"),
        ("reports", "📄 Reports"),
        ("calculator", "🧮 Calculator"),
    ]

    for i, (page_id, label) in enumerate(pages):
        with nav_cols[i]:
            css_class = "nav-btn-active" if current == page_id else "nav-btn"
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(label, use_container_width=True, key=f"nav_{page_id}"):
                st.session_state['current_page'] = page_id
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    if is_admin:
        with nav_cols[4]:
            css_class = "nav-btn-active" if current == "admin" else "nav-btn"
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button("⚙️ Admin", use_container_width=True, key="nav_admin"):
                st.session_state['current_page'] = 'admin'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with nav_cols[5]:
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("↗ Sign Out", use_container_width=True, key="nav_logout"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        with nav_cols[4]:
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("↗ Sign Out", use_container_width=True, key="nav_logout"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)


# ============================================
# 9. ELEGANT FOOTER WITH PAGE LINKS
# ============================================
def render_footer():
    st.markdown(f"""
    <div style="margin-top: 100px; padding: 50px 20px 40px;
                border-top: 1px solid rgba(255,255,255,0.04);
                text-align: center; position: relative;">

        <div style="position: absolute; top: -80px; left: 50%;
                    transform: translateX(-50%);
                    width: 500px; height: 160px;
                    background: radial-gradient(ellipse, rgba(212,175,55,0.03) 0%, transparent 70%);
                    pointer-events: none;"></div>

        <div style="margin-bottom: 15px;">
            <img src="{LOGO_URL}" width="42" height="42"
                 style="border-radius: 50%; object-fit: cover;
                        border: 2px solid rgba(212,175,55,0.3);
                        box-shadow: 0 0 20px rgba(212,175,55,0.08);">
        </div>

        <p style="font-size: 13px; font-weight: 700; letter-spacing: 3px;
                  color: rgba(212,175,55,0.4); margin-bottom: 4px;">
            ROLLIC TRADES
        </p>
        <p style="font-size: 11px; color: rgba(255,255,255,0.12);">
            Smart Money Intelligence Platform
        </p>

        <div style="display: flex; justify-content: center; gap: 28px;
                    margin: 25px 0; flex-wrap: wrap;">
            <span style="color: rgba(255,255,255,0.25); font-size: 12px;
                        font-weight: 500; cursor: pointer;
                        transition: color 0.3s ease;"
                  onmouseover="this.style.color='#d4af37'"
                  onmouseout="this.style.color='rgba(255,255,255,0.25)'">Home</span>
            <span style="color: rgba(255,255,255,0.25); font-size: 12px;
                        font-weight: 500; cursor: pointer;
                        transition: color 0.3s ease;"
                  onmouseover="this.style.color='#d4af37'"
                  onmouseout="this.style.color='rgba(255,255,255,0.25)'">Macro Terminal</span>
            <span style="color: rgba(255,255,255,0.25); font-size: 12px;
                        font-weight: 500; cursor: pointer;
                        transition: color 0.3s ease;"
                  onmouseover="this.style.color='#d4af37'"
                  onmouseout="this.style.color='rgba(255,255,255,0.25)'">Daily Reports</span>
            <span style="color: rgba(255,255,255,0.25); font-size: 12px;
                        font-weight: 500; cursor: pointer;
                        transition: color 0.3s ease;"
                  onmouseover="this.style.color='#d4af37'"
                  onmouseout="this.style.color='rgba(255,255,255,0.25)'">Risk Calculator</span>
            <span style="color: rgba(255,255,255,0.25); font-size: 12px;
                        font-weight: 500; cursor: pointer;
                        transition: color 0.3s ease;"
                  onmouseover="this.style.color='#d4af37'"
                  onmouseout="this.style.color='rgba(255,255,255,0.25)'">Academy</span>
        </div>

        <div style="width: 60px; height: 1px; margin: 25px auto;
                    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);"></div>

        <p style="max-width: 650px; margin: 0 auto; font-size: 10.5px;
                  line-height: 1.9; color: rgba(255,255,255,0.13);">
            <strong style="color: rgba(255,255,255,0.2);">Risk Disclaimer</strong><br>
            Trading foreign exchange, gold, and indices on margin carries a high level of risk
            and may not be suitable for all investors. Analysis is for educational purposes only.
            Past performance is not indicative of future results. Trade responsibly.
        </p>

        <div style="width: 60px; height: 1px; margin: 25px auto;
                    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);"></div>

        <div style="display: flex; justify-content: center; gap: 20px;
                    margin-bottom: 20px; flex-wrap: wrap;">
            <span style="font-size: 10px; color: rgba(255,255,255,0.1);
                        letter-spacing: 0.5px;">Privacy Policy</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.05);">|</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.1);
                        letter-spacing: 0.5px;">Terms of Service</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.05);">|</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.1);
                        letter-spacing: 0.5px;">Contact</span>
        </div>

        <p style="font-size: 10px; color: rgba(255,255,255,0.06); letter-spacing: 2px;">
            &copy; 2026 ROLLIC TRADES &middot; ALL RIGHTS RESERVED
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# PAGE: LOGIN
# ============================================
def login_page():
    st.markdown("""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                pointer-events: none; z-index: 0;">
        <div style="position: absolute; top: 25%; left: 50%;
                    transform: translate(-50%, -50%);
                    width: 700px; height: 700px; border-radius: 50%;
                    background: radial-gradient(circle,
                        rgba(212,175,55,0.05) 0%, transparent 65%);
                    filter: blur(50px);"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;" class="float-anim">
            <img src="{LOGO_URL}" width="110" height="110"
                 style="border-radius: 50%; object-fit: cover;" class="glow-ring">
        </div>
        <div style="text-align: center; margin-bottom: 6px;">
            <p style="font-size: 9px; letter-spacing: 5px; text-transform: uppercase;
                      color: rgba(212,175,55,0.4); font-weight: 600; margin-bottom: 6px;">
                INSTITUTIONAL TRADING
            </p>
            <h1 class="gradient-text" style="font-size: 30px; font-weight: 800; margin: 0;">
                ROLLIC TRADES
            </h1>
            <p style="color: rgba(255,255,255,0.2); font-size: 12px; margin-top: 4px;">
                Smart Money Intelligence Platform
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        username = st.text_input("USERNAME", placeholder="Enter username", key="login_user")
        password = st.text_input("PASSWORD", placeholder="Enter password",
                                 type="password", key="login_pass")

        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
        login_clicked = st.button("SIGN IN →", use_container_width=True, key="login_btn")
        st.markdown('</div>', unsafe_allow_html=True)

        if login_clicked:
            db = st.session_state['users_db']
            match = db[(db['Username'] == username) & (db['Password'] == password)]
            if not match.empty:
                if match.iloc[0]['Status'] == 'Active':
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = match.iloc[0]['Role']
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Account suspended. Contact admin.")
            else:
                st.error("Invalid credentials")

        st.markdown("""
        <div style="text-align: center; margin-top: 22px;">
            <span class="pulse-dot"></span>
            <span style="color: rgba(255,255,255,0.15); font-size: 10px;
                        margin-left: 6px;">Encrypted Connection</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# PAGE: HOME - ULTRA PREMIUM
# ============================================
def home_page():
    # === ANIMATED TRADING TICKER BANNER ===
    st.markdown("""
    <div class="trading-ticker-wrapper">
        <div class="trading-ticker-content">
            <span class="ticker-item">🪙 XAUUSD <span class="price">3,312.45</span> <span class="up">+0.54%</span></span>
            <span class="ticker-item">💶 EURUSD <span class="price">1.1382</span> <span class="up">+0.18%</span></span>
            <span class="ticker-item">📈 SP500 <span class="price">5,525.21</span> <span class="down">-0.32%</span></span>
            <span class="ticker-item">₿ BTCUSD <span class="price">94,250</span> <span class="up">+1.24%</span></span>
            <span class="ticker-item">💴 USDJPY <span class="price">143.82</span> <span class="down">-0.15%</span></span>
            <span class="ticker-item">🛢 CRUDE <span class="price">62.45</span> <span class="up">+0.87%</span></span>
            <span class="ticker-item">📊 DXY <span class="price">99.58</span> <span class="down">-0.32%</span></span>
            <span class="ticker-item">🪙 XAUUSD <span class="price">3,312.45</span> <span class="up">+0.54%</span></span>
            <span class="ticker-item">💶 EURUSD <span class="price">1.1382</span> <span class="up">+0.18%</span></span>
            <span class="ticker-item">📈 SP500 <span class="price">5,525.21</span> <span class="down">-0.32%</span></span>
            <span class="ticker-item">₿ BTCUSD <span class="price">94,250</span> <span class="up">+1.24%</span></span>
            <span class="ticker-item">💴 USDJPY <span class="price">143.82</span> <span class="down">-0.15%</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === HERO SECTION ===
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0 25px; position: relative;">
        <div style="position: absolute; top: -50px; left: 50%;
                    transform: translateX(-50%);
                    width: 600px; height: 600px;
                    background: radial-gradient(circle,
                        rgba(212,175,55,0.06) 0%,
                        rgba(212,175,55,0.02) 30%,
                        transparent 70%);
                    pointer-events: none;"></div>

        <div style="margin-bottom: 16px;" class="float-anim">
            <img src="{LOGO_URL}" width="85" height="85"
                 style="border-radius: 50%; object-fit: cover;" class="glow-ring">
        </div>

        <p style="font-size: 9px; letter-spacing: 5px; text-transform: uppercase;
                  color: rgba(212,175,55,0.4); font-weight: 600; margin-bottom: 6px;">
            WELCOME BACK
        </p>

        <h1 style="font-size: 40px; font-weight: 800; color: #fff;
                   margin: 0; line-height: 1.15;">
            {st.session_state['username'].title()},
            <span class="gradient-text">let's trade.</span>
        </h1>

        <p style="color: rgba(255,255,255,0.2); font-size: 13px;
                  margin-top: 8px;">
            {st.session_state['user_role']} &middot;
            {datetime.now().strftime("%A, %B %d, %Y")}
        </p>

        <div style="margin-top: 14px; display: flex;
                    justify-content: center; align-items: center; gap: 8px;">
            <span class="pulse-dot"></span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.2);
                        font-weight: 500;">Markets Open</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # === LIVE PRICE CHART WIDGETS ===
    st.markdown("""
    <p class="section-eyebrow">LIVE MARKETS</p>
    <p class="section-title">Market <span class="gradient-text">Overview</span></p>
    <p class="section-subtitle">Real-time institutional price feed</p>
    """, unsafe_allow_html=True)

    markets = [
        {"name": "XAUUSD", "label": "Gold", "price": "3,312.45",
         "change": "+0.54%", "up": True, "color": "#d4af37",
         "data": [3280, 3290, 3285, 3300, 3295, 3310, 3305, 3312, 3308, 3315, 3312]},
        {"name": "EURUSD", "label": "EUR/USD", "price": "1.1382",
         "change": "+0.18%", "up": True, "color": "#007AFF",
         "data": [1.130, 1.132, 1.131, 1.134, 1.133, 1.136, 1.135, 1.137, 1.136, 1.138, 1.138]},
        {"name": "SP500", "label": "S&P 500", "price": "5,525.21",
         "change": "-0.32%", "up": False, "color": "#30D158",
         "data": [5550, 5545, 5548, 5540, 5535, 5530, 5528, 5532, 5525, 5520, 5525]},
        {"name": "BTCUSD", "label": "Bitcoin", "price": "94,250",
         "change": "+1.24%", "up": True, "color": "#FF9F0A",
         "data": [92000, 92500, 93000, 92800, 93200, 93500, 93800, 94000, 93900, 94100, 94250]},
    ]

    mc1, mc2, mc3, mc4 = st.columns(4)
    for col, m in zip([mc1, mc2, mc3, mc4], markets):
        with col:
            change_color = '#30d158' if m['up'] else '#ff453a'
            arrow = '▲' if m['up'] else '▼'
            st.markdown(f"""
            <div class="ticker-card">
                <div style="display: flex; align-items: center;
                            justify-content: space-between; margin-bottom: 4px;">
                    <p style="font-size: 11px; font-weight: 700;
                              letter-spacing: 1.5px; text-transform: uppercase;
                              color: rgba(255,255,255,0.4); margin: 0;">
                        {m['name']}
                    </p>
                    <div style="display: flex; align-items: center; gap: 4px;">
                        <span style="width: 5px; height: 5px;
                                    background: {change_color};
                                    border-radius: 50%;"></span>
                        <span style="font-size: 9px;
                                    color: rgba(255,255,255,0.2);">LIVE</span>
                    </div>
                </div>
                <p style="font-size: 22px; font-weight: 800; color: #fff;
                          font-family: 'JetBrains Mono', monospace; margin: 4px 0;">
                    {m['price']}
                </p>
                <p style="font-size: 12px; font-weight: 600;
                          color: {change_color}; margin: 0;">
                    {arrow} {m['change']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            fig = render_mini_chart(m['data'], m['color'])
            st.plotly_chart(fig, use_container_width=True, key=f"mini_{m['name']}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # === FEATURE CARDS ===
    st.markdown("""
    <p class="section-eyebrow">TRADING SUITE</p>
    <p class="section-title">Your <span class="gradient-text">Toolkit</span></p>
    <p class="section-subtitle">Everything for institutional-grade trading</p>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 240px;">
            <div style="width: 52px; height: 52px; border-radius: 14px;
                        background: rgba(212,175,55,0.08);
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto 14px; font-size: 24px;">📄</div>
            <p style="color: #fff; font-size: 17px; font-weight: 700;
                      margin-bottom: 8px;">Daily Reports</p>
            <p style="color: rgba(255,255,255,0.25); font-size: 12px;
                      line-height: 1.7; margin-bottom: 16px;">
                Expert analysis with trade scenarios and Smart Money decode.</p>
            <span style="font-size: 9px; padding: 4px 10px; border-radius: 20px;
                        background: rgba(48,209,88,0.08); color: #30d158;
                        font-weight: 600;">UPDATED DAILY</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Reports →", use_container_width=True, key="hm_rep"):
            st.session_state['current_page'] = 'reports'
            st.rerun()

    with f2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 240px;">
            <div style="width: 52px; height: 52px; border-radius: 14px;
                        background: rgba(0,122,255,0.08);
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto 14px; font-size: 24px;">📊</div>
            <p style="color: #fff; font-size: 17px; font-weight: 700;
                      margin-bottom: 8px;">Macro Terminal</p>
            <p style="color: rgba(255,255,255,0.25); font-size: 12px;
                      line-height: 1.7; margin-bottom: 16px;">
                Economic indicators, COT analysis, and Fed tracking.</p>
            <span style="font-size: 9px; padding: 4px 10px; border-radius: 20px;
                        background: rgba(0,122,255,0.08); color: #007AFF;
                        font-weight: 600;">LIVE DATA</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Terminal →", use_container_width=True, key="hm_mac"):
            st.session_state['current_page'] = 'macro'
            st.rerun()

    with f3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 240px;">
            <div style="width: 52px; height: 52px; border-radius: 14px;
                        background: rgba(191,90,242,0.08);
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto 14px; font-size: 24px;">🧮</div>
            <p style="color: #fff; font-size: 17px; font-weight: 700;
                      margin-bottom: 8px;">Risk Calculator</p>
            <p style="color: rgba(255,255,255,0.25); font-size: 12px;
                      line-height: 1.7; margin-bottom: 16px;">
                Precision position sizing for every trade setup.</p>
            <span style="font-size: 9px; padding: 4px 10px; border-radius: 20px;
                        background: rgba(191,90,242,0.08); color: #BF5AF2;
                        font-weight: 600;">TOOL</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate →", use_container_width=True, key="hm_cal"):
            st.session_state['current_page'] = 'calculator'
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # === QUICK STATS ===
    st.markdown("""
    <p class="section-eyebrow">PLATFORM</p>
    <p class="section-title">Quick <span class="gradient-text">Stats</span></p>
    """, unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Total Reports", len(st.session_state['html_reports']))
    with s2:
        st.metric("Active Users", len(st.session_state['users_db']))
    with s3:
        st.metric("Platform", "v3.0")
    with s4:
        st.metric("Uptime", "99.9%")


# ============================================
# PAGE: CALCULATOR
# ============================================
def calculator_page():
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 5px;">
        <p class="section-eyebrow">RISK MANAGEMENT</p>
        <p class="section-title">Position <span class="gradient-text">Calculator</span></p>
        <p class="section-subtitle">Calculate optimal lot sizes for risk-adjusted entries</p>
    </div>
    """, unsafe_allow_html=True)
    components.html(CALCULATOR_HTML, height=680, scrolling=False)


# ============================================
# PAGE: ADMIN - EXPERT LEVEL
# ============================================
def admin_panel():
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 5px;">
        <p class="section-eyebrow">SYSTEM CONTROL</p>
        <p class="section-title">Admin <span class="gradient-text">Console</span></p>
        <p class="section-subtitle">Manage reports, users, pages, and system settings</p>
    </div>
    """, unsafe_allow_html=True)

    # Admin Stats Bar
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    as1, as2, as3, as4 = st.columns(4)
    with as1:
        st.markdown(f"""
        <div class="admin-stat">
            <div class="admin-stat-value">{len(st.session_state['users_db'])}</div>
            <div class="admin-stat-label">Total Users</div>
        </div>
        """, unsafe_allow_html=True)
    with as2:
        active = len(st.session_state['users_db'][st.session_state['users_db']['Status'] == 'Active'])
        st.markdown(f"""
        <div class="admin-stat">
            <div class="admin-stat-value" style="color: #30d158;">{active}</div>
            <div class="admin-stat-label">Active Users</div>
        </div>
        """, unsafe_allow_html=True)
    with as3:
        st.markdown(f"""
        <div class="admin-stat">
            <div class="admin-stat-value">{len(st.session_state['html_reports'])}</div>
            <div class="admin-stat-label">Reports</div>
        </div>
        """, unsafe_allow_html=True)
    with as4:
        st.markdown(f"""
        <div class="admin-stat">
            <div class="admin-stat-value">{len(st.session_state['pages_db'])}</div>
            <div class="admin-stat-label">Custom Pages</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📄 Report Manager",
        "👥 User Management",
        "📑 Page Manager"
    ])

    # ---- TAB 1: REPORT MANAGER ----
    with tab1:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 30px;">
            <span style="font-size: 32px;">📄</span>
            <h3 style="color: #fff; margin-top: 10px; margin-bottom: 4px;
                       font-size: 17px;">Upload Analysis Report</h3>
            <p style="color: rgba(255,255,255,0.25); font-size: 12px;">
                HTML files rendered exactly as designed</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        uc1, uc2 = st.columns([2, 1])
        with uc1:
            uploaded_file = st.file_uploader(
                "Select HTML File", type=['html'],
                label_visibility="collapsed", key="report_upload"
            )
        with uc2:
            report_date = st.date_input("Report Date", datetime.now(), key="report_date")

        st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
        if st.button("PUBLISH REPORT →", use_container_width=True, key="pub_report"):
            if uploaded_file:
                html_string = uploaded_file.getvalue().decode("utf-8")
                date_key = report_date.strftime("%Y-%m-%d")
                st.session_state['html_reports'][date_key] = html_string
                st.success(f"Report for {date_key} published!")
            else:
                st.error("Select an HTML file first.")
        st.markdown('</div>', unsafe_allow_html=True)

        # List reports
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📅 Published Reports")

        for dk in sorted(st.session_state['html_reports'].keys(), reverse=True):
            rc1, rc2 = st.columns([5, 1])
            with rc1:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02);
                            border: 1px solid rgba(255,255,255,0.05);
                            border-radius: 12px; padding: 12px 18px;
                            margin-bottom: 6px;
                            display: flex; align-items: center; gap: 10px;">
                    <span style="color: #d4af37;">📄</span>
                    <div>
                        <p style="color: #fff; font-size: 13px;
                                  font-weight: 600; margin: 0;">{dk}</p>
                        <p style="color: rgba(255,255,255,0.2);
                                  font-size: 10px; margin: 0;">HTML Report</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with rc2:
                if st.button("🗑️", key=f"del_r_{dk}"):
                    del st.session_state['html_reports'][dk]
                    st.rerun()

    # ---- TAB 2: USER MANAGEMENT ----
    with tab2:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown("#### 👥 All Users")
        st.dataframe(
            st.session_state['users_db'],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        # ADD USER
        st.markdown("#### ➕ Add New User")
        ac1, ac2 = st.columns(2)
        with ac1:
            new_user = st.text_input("Username", key="new_u",
                                     placeholder="Enter username")
        with ac2:
            new_pass = st.text_input("Password", key="new_p",
                                     placeholder="Enter password", type="password")

        ac3, ac4 = st.columns(2)
        with ac3:
            new_role = st.selectbox("Role", ["User", "Admin"], key="new_r")
        with ac4:
            new_status = st.selectbox("Status", ["Active", "Suspended"], key="new_s")

        st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
        if st.button("CREATE USER →", use_container_width=True, key="create_user"):
            if new_user and new_pass:
                existing = st.session_state['users_db']
                if new_user in existing['Username'].values:
                    st.error(f"Username '{new_user}' already exists!")
                else:
                    new_row = pd.DataFrame({
                        "Username": [new_user],
                        "Password": [new_pass],
                        "Role": [new_role],
                        "Status": [new_status],
                        "Created": [datetime.now().strftime("%Y-%m-%d")]
                    })
                    st.session_state['users_db'] = pd.concat(
                        [st.session_state['users_db'], new_row],
                        ignore_index=True
                    )
                    st.success(f"User '{new_user}' created!")
                    st.rerun()
            else:
                st.error("Fill all fields.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # MODIFY USER
        st.markdown("#### ✏️ Modify User")
        all_users = st.session_state['users_db']['Username'].tolist()

        mc1, mc2 = st.columns(2)
        with mc1:
            sel_user = st.selectbox("Select User", all_users, key="mod_user")
        with mc2:
            action = st.selectbox("Action", [
                "Activate", "Suspend", "Change to Admin",
                "Change to User", "Reset Password", "Delete"
            ], key="mod_action")

        new_pw = ""
        if action == "Reset Password":
            new_pw = st.text_input("New Password", type="password",
                                   key="reset_pw", placeholder="Enter new password")

        if st.button("APPLY ACTION →", use_container_width=True, key="apply_mod"):
            db = st.session_state['users_db']
            idx = db[db['Username'] == sel_user].index

            if len(idx) > 0:
                i = idx[0]
                if sel_user == "admin" and action == "Delete":
                    st.error("Cannot delete admin account!")
                elif action == "Activate":
                    db.at[i, 'Status'] = 'Active'
                    st.success(f"'{sel_user}' activated.")
                    st.rerun()
                elif action == "Suspend":
                    if sel_user == "admin":
                        st.error("Cannot suspend admin!")
                    else:
                        db.at[i, 'Status'] = 'Suspended'
                        st.success(f"'{sel_user}' suspended.")
                        st.rerun()
                elif action == "Change to Admin":
                    db.at[i, 'Role'] = 'Admin'
                    st.success(f"'{sel_user}' is now Admin.")
                    st.rerun()
                elif action == "Change to User":
                    if sel_user == "admin":
                        st.error("Cannot change admin role!")
                    else:
                        db.at[i, 'Role'] = 'User'
                        st.success(f"'{sel_user}' is now User.")
                        st.rerun()
                elif action == "Reset Password":
                    if new_pw:
                        db.at[i, 'Password'] = new_pw
                        st.success(f"Password reset for '{sel_user}'.")
                        st.rerun()
                    else:
                        st.error("Enter new password.")
                elif action == "Delete":
                    st.session_state['users_db'] = db.drop(i).reset_index(drop=True)
                    st.success(f"'{sel_user}' deleted.")
                    st.rerun()

    # ---- TAB 3: PAGE MANAGER ----
    with tab3:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 30px;">
            <span style="font-size: 32px;">📑</span>
            <h3 style="color: #fff; margin-top: 10px; margin-bottom: 4px;
                       font-size: 17px;">Custom Page Builder</h3>
            <p style="color: rgba(255,255,255,0.25); font-size: 12px;">
                Add custom HTML pages to your platform</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        pc1, pc2 = st.columns(2)
        with pc1:
            page_name = st.text_input("Page Name", key="page_name",
                                      placeholder="e.g., Weekly Outlook")
        with pc2:
            page_icon = st.text_input("Page Icon (emoji)", key="page_icon",
                                      placeholder="e.g., 📈", value="📄")

        page_file = st.file_uploader(
            "Upload Page HTML", type=['html'],
            label_visibility="visible", key="page_upload"
        )

        st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
        if st.button("ADD PAGE →", use_container_width=True, key="add_page"):
            if page_name and page_file:
                html_content = page_file.getvalue().decode("utf-8")
                page_id = page_name.lower().replace(" ", "_")
                st.session_state['pages_db'][page_id] = {
                    'name': page_name,
                    'icon': page_icon,
                    'html': html_content,
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.success(f"Page '{page_name}' added!")
                st.rerun()
            else:
                st.error("Fill name and upload HTML.")
        st.markdown('</div>', unsafe_allow_html=True)

        # List pages
        if st.session_state['pages_db']:
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            st.markdown("#### 📑 Custom Pages")

            for pid, pdata in st.session_state['pages_db'].items():
                pc1, pc2, pc3 = st.columns([4, 1, 1])
                with pc1:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.02);
                                border: 1px solid rgba(255,255,255,0.05);
                                border-radius: 12px; padding: 12px 18px;
                                margin-bottom: 6px;
                                display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 18px;">{pdata['icon']}</span>
                        <div>
                            <p style="color: #fff; font-size: 13px;
                                      font-weight: 600; margin: 0;">{pdata['name']}</p>
                            <p style="color: rgba(255,255,255,0.2);
                                      font-size: 10px; margin: 0;">
                                Created: {pdata['created']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with pc2:
                    if st.button("👁️", key=f"view_{pid}"):
                        st.session_state['current_page'] = f'custom_{pid}'
                        st.rerun()
                with pc3:
                    if st.button("🗑️", key=f"delp_{pid}"):
                        del st.session_state['pages_db'][pid]
                        st.rerun()


# ============================================
# PAGE: REPORTS
# ============================================
def reports_page():
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0 5px;">
        <div style="margin-bottom: 12px;">
            <img src="{LOGO_URL}" width="55" height="55"
                 style="border-radius: 50%; object-fit: cover;" class="glow-ring">
        </div>
        <p class="section-eyebrow">EXPERT ANALYSIS</p>
        <p class="section-title">Daily <span class="gradient-text">Market Report</span></p>
    </div>
    """, unsafe_allow_html=True)

    dates = sorted(st.session_state['html_reports'].keys(), reverse=True)

    if dates:
        _, cc, _ = st.columns([2, 1, 2])
        with cc:
            sel_date = st.selectbox("Select Date", dates,
                                    label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)

        if sel_date:
            components.html(
                st.session_state['html_reports'][sel_date],
                height=1500, scrolling=True
            )
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <span style="font-size: 50px; opacity: 0.2;">📄</span>
            <h3 style="color: rgba(255,255,255,0.2); margin-top: 12px;">
                No Reports</h3>
            <p style="color: rgba(255,255,255,0.1); font-size: 13px;">
                Upload from Admin Console.</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# PAGE: CUSTOM PAGE VIEWER
# ============================================
def custom_page_viewer(page_id):
    pid = page_id.replace("custom_", "")
    if pid in st.session_state['pages_db']:
        pdata = st.session_state['pages_db'][pid]
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0 5px;">
            <p class="section-eyebrow">CUSTOM PAGE</p>
            <p class="section-title">{pdata['icon']}
                <span class="gradient-text">{pdata['name']}</span></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        components.html(pdata['html'], height=1500, scrolling=True)
    else:
        st.error("Page not found!")


# ============================================
# PAGE: MACRO DASHBOARD
# ============================================
def macro_dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 5px;">
        <p class="section-eyebrow">INSTITUTIONAL GRADE</p>
        <p class="section-title">Macro <span class="gradient-text">Terminal</span></p>
        <p class="section-subtitle">Economic intelligence and Smart Money positioning</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        API_KEY = st.secrets["FRED_API_KEY"]
        fred = Fred(api_key=API_KEY)

        @st.cache_data(ttl=3600)
        def fetch_fred():
            smap = {
                "CPI": "CPIAUCSL",
                "Fed Rate": "FEDFUNDS",
                "US 10Y": "DGS10",
                "Unemployment": "UNRATE",
                "GDP Growth": "A191RL1Q225SBEA",
                "PCE": "PCEPI"
            }
            results = {}
            for name, sid in smap.items():
                try:
                    d = fred.get_series(sid)
                    if len(d) >= 2:
                        results[name] = {
                            'latest': round(float(d.iloc[-1]), 2),
                            'previous': round(float(d.iloc[-2]), 2),
                            'change': round(float(d.iloc[-1]) - float(d.iloc[-2]), 3)
                        }
                except Exception:
                    results[name] = {'latest': 0, 'previous': 0, 'change': 0}
            return results

        fred_data = fetch_fred()
    except Exception:
        fred_data = {
            "CPI": {'latest': 3.2, 'previous': 3.1, 'change': 0.1},
            "Fed Rate": {'latest': 5.50, 'previous': 5.50, 'change': 0.0},
            "US 10Y": {'latest': 4.26, 'previous': 4.22, 'change': 0.04},
            "Unemployment": {'latest': 4.1, 'previous': 4.0, 'change': 0.1},
            "GDP Growth": {'latest': 2.8, 'previous': 3.0, 'change': -0.2},
            "PCE": {'latest': 2.7, 'previous': 2.6, 'change': 0.1}
        }
        st.info("📡 Demo mode — add FRED_API_KEY to secrets for live data.")

    def build_gauge(value, prev_val, color):
        low = min(value, prev_val) * 0.85
        high = max(value, prev_val) * 1.15
        if low == high:
            low = value * 0.9
            high = value * 1.1

        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=value,
            number={'font': {'size': 30, 'color': '#fff', 'family': 'Inter'}},
            gauge={
                'axis': {'range': [low, high],
                         'tickcolor': '#222',
                         'tickfont': {'color': '#444', 'size': 9}},
                'bar': {'color': color, 'thickness': 0.3},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 0,
                'steps': [
                    {'range': [low, prev_val],
                     'color': 'rgba(255,255,255,0.015)'}
                ],
                'threshold': {
                    'line': {'color': '#fff', 'width': 1.5},
                    'thickness': 0.75, 'value': prev_val
                }
            }
        ))
        fig.update_layout(
            height=190,
            margin=dict(l=20, r=20, t=25, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    items = [
        ("CPI Inflation", "CPI", "#FF453A", "📈", "BULLISH", "BEARISH", "Feb 12"),
        ("Fed Funds Rate", "Fed Rate", "#007AFF", "🏛️", "BULLISH", "BEARISH", "Mar 19"),
        ("US 10Y Yield", "US 10Y", "#d4af37", "📊", "BULLISH", "BEARISH", "Daily"),
        ("Unemployment", "Unemployment", "#FF9F0A", "👥", "BEARISH", "BULLISH", "Feb 7"),
        ("GDP Growth", "GDP Growth", "#30D158", "📈", "BULLISH", "BEARISH", "Feb 27"),
        ("PCE Index", "PCE", "#BF5AF2", "💰", "BULLISH", "BEARISH", "Feb 28"),
    ]

    for row in range(0, len(items), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = row + i
            if idx < len(items):
                title, key, color, icon, dxy, gold, nxt = items[idx]
                d = fred_data.get(key, {'latest': 0, 'previous': 0, 'change': 0})

                with col:
                    chg_color = '#30D158' if d['change'] >= 0 else '#FF453A'
                    chg_arrow = '↑' if d['change'] >= 0 else '↓'
                    chg_bg = 'rgba(48,209,88,0.08)' if d['change'] >= 0 else 'rgba(255,69,58,0.08)'

                    st.markdown(f"""
                    <div class="glass-card" style="padding: 16px;">
                        <div style="display: flex; align-items: center;
                                    justify-content: space-between; margin-bottom: 2px;">
                            <span style="font-size: 10px; letter-spacing: 1.5px;
                                        text-transform: uppercase;
                                        color: rgba(255,255,255,0.35);
                                        font-weight: 600;">
                                {icon} {title}
                            </span>
                            <span style="font-size: 9px; padding: 3px 8px;
                                        border-radius: 12px; background: {chg_bg};
                                        color: {chg_color}; font-weight: 600;">
                                {chg_arrow} {abs(d['change'])}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.plotly_chart(
                        build_gauge(d['latest'], d['previous'], color),
                        use_container_width=True, key=f"g_{key}_{idx}"
                    )

                    st.markdown(f"""
                    <div style="display: flex; justify-content: center;
                                gap: 6px; margin-top: -10px; margin-bottom: 10px;">
                        <span style="font-size: 9px; padding: 3px 10px;
                                    border-radius: 14px;
                                    background: rgba(0,122,255,0.08);
                                    color: #007AFF; font-weight: 600;">
                            DXY: {dxy}</span>
                        <span style="font-size: 9px; padding: 3px 10px;
                                    border-radius: 14px;
                                    background: rgba(212,175,55,0.08);
                                    color: #d4af37; font-weight: 600;">
                            GOLD: {gold}</span>
                    </div>
                    <p style="text-align: center; font-size: 9px;
                              color: rgba(255,255,255,0.12);">
                        📅 Next: {nxt}</p>
                    """, unsafe_allow_html=True)

    # COT SECTION
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p class="section-eyebrow">SMART MONEY</p>
    <p class="section-title">COT <span class="gradient-text">Analysis</span></p>
    """, unsafe_allow_html=True)

    cl, cr = st.columns([1, 1.5])

    with cl:
        fig_cot = go.Figure(data=[go.Pie(
            values=[75, 25], hole=.78,
            direction='clockwise', sort=False,
            marker=dict(
                colors=['#d4af37', 'rgba(255,255,255,0.02)'],
                line=dict(color='#000', width=2)
            ),
            textinfo='none', hoverinfo='none'
        )])
        fig_cot.update_layout(
            showlegend=False,
            margin=dict(t=15, b=15, l=15, r=15),
            height=280,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text="75%", x=0.5, y=0.55, font_size=42,
                     showarrow=False, font_color="#d4af37",
                     font_family="Inter"),
                dict(text="BULLISH", x=0.5, y=0.42, font_size=10,
                     showarrow=False,
                     font_color="rgba(255,255,255,0.25)")
            ]
        )
        st.plotly_chart(fig_cot, use_container_width=True, key="cot_donut")

    with cr:
        st.markdown("""
        <div class="glass-card" style="margin-top: 5px;">
            <p style="font-size: 10px; letter-spacing: 2px;
                      text-transform: uppercase;
                      color: rgba(212,175,55,0.5); font-weight: 700;
                      margin-bottom: 14px;">
                XAUUSD POSITIONING
            </p>
            <p style="color: rgba(255,255,255,0.4); font-size: 13px;
                      line-height: 1.8; margin-bottom: 18px;">
                Commercial traders showing
                <strong style="color: #fff;">net long positioning</strong>.
                Smart Money accumulating at institutional zones.
            </p>
            <div style="display: flex; justify-content: space-around;
                        text-align: center; padding: 16px 0;
                        border-top: 1px solid rgba(255,255,255,0.03);
                        border-bottom: 1px solid rgba(255,255,255,0.03);">
                <div>
                    <p style="font-size: 9px; letter-spacing: 1px;
                              color: rgba(255,255,255,0.25);
                              text-transform: uppercase;
                              margin-bottom: 4px;">Longs</p>
                    <p style="font-size: 20px; font-weight: 800;
                              color: #30D158;">250K</p>
                </div>
                <div>
                    <p style="font-size: 9px; letter-spacing: 1px;
                              color: rgba(255,255,255,0.25);
                              text-transform: uppercase;
                              margin-bottom: 4px;">Shorts</p>
                    <p style="font-size: 20px; font-weight: 800;
                              color: #FF453A;">50K</p>
                </div>
                <div>
                    <p style="font-size: 9px; letter-spacing: 1px;
                              color: rgba(255,255,255,0.25);
                              text-transform: uppercase;
                              margin-bottom: 4px;">Net</p>
                    <p style="font-size: 20px; font-weight: 800;
                              color: #d4af37;">+200K</p>
                </div>
            </div>
            <div style="margin-top: 12px; text-align: center;">
                <span style="font-size: 9px; padding: 4px 14px;
                            border-radius: 20px;
                            background: rgba(48,209,88,0.08);
                            color: #30d158; font-weight: 700;
                            letter-spacing: 1px;">
                    ● BIAS: BULLISH
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# MAIN CONTROLLER
# ============================================
if not st.session_state['logged_in']:
    login_page()
    render_footer()
else:
    render_header()

    page = st.session_state['current_page']

    if page == 'home':
        home_page()
    elif page == 'macro':
        macro_dashboard()
    elif page == 'reports':
        reports_page()
    elif page == 'calculator':
        calculator_page()
    elif page == 'admin':
        admin_panel()
    elif page.startswith('custom_'):
        custom_page_viewer(page)
    else:
        home_page()

    render_footer()

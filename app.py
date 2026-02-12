import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components
import requests

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
# 2. GLOBAL
# ============================================
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60"

# ============================================
# 3. CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    .stApp {background:#000;font-family:'Inter',sans-serif;}
    #MainMenu,footer,header{visibility:hidden;}
    div[data-testid="stToolbar"],div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],.stDeployButton{display:none;}
    ::-webkit-scrollbar{width:5px;}
    ::-webkit-scrollbar-track{background:#000;}
    ::-webkit-scrollbar-thumb{background:#222;border-radius:10px;}

    div.stButton > button {
        background:rgba(255,255,255,0.03)!important;
        color:rgba(255,255,255,0.7)!important;
        border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important;
        padding:10px 20px!important;
        font-family:'Inter',sans-serif!important;
        font-weight:600!important;font-size:13px!important;
        transition:all 0.3s ease!important;
    }
    div.stButton > button:hover {
        background:rgba(212,175,55,0.1)!important;
        color:#d4af37!important;
        border-color:rgba(212,175,55,0.25)!important;
    }

    div[data-testid="stTextInput"] input {
        background:rgba(255,255,255,0.03)!important;
        border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important;color:#fff!important;
        font-size:14px!important;padding:14px 16px!important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color:#d4af37!important;
        box-shadow:0 0 0 3px rgba(212,175,55,0.08)!important;
    }
    div[data-testid="stTextInput"] label {
        color:rgba(255,255,255,0.4)!important;font-weight:500!important;font-size:12px!important;
    }
    div[data-testid="stTextArea"] textarea {
        background:rgba(255,255,255,0.03)!important;
        border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important;color:#fff!important;
    }
    div[data-testid="stTextArea"] label {
        color:rgba(255,255,255,0.4)!important;
    }
    div[data-testid="stSelectbox"] > div > div {
        background:rgba(255,255,255,0.03)!important;
        border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important;
    }
    div[data-testid="stSelectbox"] label{color:rgba(255,255,255,0.4)!important;}
    div[data-testid="stTabs"] button {
        color:rgba(255,255,255,0.4)!important;font-weight:600!important;
        font-size:13px!important;background:transparent!important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color:#d4af37!important;border-bottom-color:#d4af37!important;
    }
    div[data-testid="stFileUploader"] {
        background:rgba(255,255,255,0.015)!important;
        border:2px dashed rgba(212,175,55,0.15)!important;
        border-radius:16px!important;
    }
    div[data-testid="stDateInput"] input {
        background:rgba(255,255,255,0.03)!important;
        border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important;color:white!important;
    }
    div[data-testid="stMetric"] {
        background:rgba(255,255,255,0.02);
        border:1px solid rgba(255,255,255,0.05);
        border-radius:16px;padding:18px;
    }
    div[data-testid="stMetric"] label {
        color:rgba(255,255,255,0.3)!important;font-size:11px!important;
        letter-spacing:1px!important;text-transform:uppercase!important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color:#d4af37!important;font-weight:700!important;
    }
    hr {
        border:none!important;height:1px!important;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.05),transparent)!important;
        margin:35px 0!important;
    }
    h1 a,h2 a,h3 a{display:none!important;}
    @keyframes shimmer {
        0%,100%{background-position:0% center;}
        50%{background-position:200% center;}
    }
    @keyframes pulse-glow {
        0%,100%{box-shadow:0 0 0 0 rgba(48,209,88,0.4);}
        50%{box-shadow:0 0 0 8px rgba(48,209,88,0);}
    }
    @keyframes float {
        0%,100%{transform:translateY(0);}
        50%{transform:translateY(-8px);}
    }
    @keyframes ticker-scroll {
        0%{transform:translateX(0);}
        100%{transform:translateX(-50%);}
    }
    @keyframes fadeInUp {
        0%{opacity:0;transform:translateY(20px);}
        100%{opacity:1;transform:translateY(0);}
    }
    @keyframes glow-pulse {
        0%,100%{box-shadow:0 0 20px rgba(212,175,55,0.1);}
        50%{box-shadow:0 0 40px rgba(212,175,55,0.2);}
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. DEFAULT REPORT HTML
# ============================================
DEFAULT_REPORT_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Inter',sans-serif;background:#000;color:#fff;}
.mc{max-width:1000px;margin:0 auto;padding:30px 20px;}
.hero{text-align:center;padding:60px 20px;}
.ht{font-size:48px;font-weight:800;color:#d4af37;margin-bottom:10px;}
.hs{font-size:16px;color:rgba(255,255,255,0.4);}
.sec{margin-bottom:30px;padding:30px;background:rgba(255,255,255,0.03);border-radius:24px;border:1px solid rgba(255,255,255,0.06);}
.sh{font-size:13px;font-weight:700;color:#d4af37;letter-spacing:2px;text-transform:uppercase;margin-bottom:25px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.04);}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:15px;}
.sc{background:rgba(255,255,255,0.02);padding:20px;border-radius:16px;border:1px solid rgba(255,255,255,0.04);text-align:center;}
.sl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}
.sv{font-size:28px;font-weight:800;color:#d4af37;}
.lb{background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);padding:20px;border-radius:16px;margin-top:20px;font-size:14px;line-height:1.7;color:rgba(255,255,255,0.7);}
.scc{background:rgba(255,255,255,0.02);padding:25px;border-radius:20px;border:1px solid rgba(255,255,255,0.04);margin-bottom:15px;border-left:3px solid #d4af37;}
.st2{font-size:16px;font-weight:700;margin-bottom:8px;color:#fff;}
.scc p{color:rgba(255,255,255,0.5);font-size:14px;line-height:1.6;}
.bl{text-align:center;padding:40px;background:rgba(212,175,55,0.03);border-radius:24px;border:1px solid rgba(212,175,55,0.15);}
.bl h3{font-size:28px;font-weight:800;color:#d4af37;margin-bottom:10px;}
.bl p{color:rgba(255,255,255,0.5);}
</style></head><body>
<div class="mc">
<section class="hero"><h1 class="ht">Gold Analysis</h1><p class="hs">Smart Money Positioning - APR 26 Contract</p></section>
<section class="sec"><div class="sh">Futures Data</div><div class="sg"><div class="sc"><div class="sl">Price</div><div class="sv" style="color:#FF453A">5,086</div></div><div class="sc"><div class="sl">Volume</div><div class="sv">129,968</div></div><div class="sc"><div class="sl">OI Change</div><div class="sv" style="color:#FF453A">+1,199</div></div><div class="sc"><div class="sl">Blocks</div><div class="sv">475</div></div></div><div class="lb"><strong>Logic:</strong> Price DOWN + OI UP = SHORT BUILDUP</div></section>
<section class="sec"><div class="sh">Trade Scenarios</div><div class="scc"><div class="st2">Scenario A: Sell Rally (70%)</div><p>Test 5269-5311 zone SHORT. Target: 5020</p></div><div class="scc" style="border-left-color:#FF453A;"><div class="st2">Scenario B: Continuation</div><p>Below 5036 fall to 4979</p></div></section>
<section class="bl"><h3>VERDICT: BEARISH</h3><p>Short rallies into 5280 targeting 5020</p></section>
</div></body></html>"""

# ============================================
# 5. CALCULATOR HTML
# ============================================
CALCULATOR_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;display:flex;justify-content:center;padding:30px;font-family:'Inter',sans-serif;}
.c{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:28px;padding:40px;width:100%;max-width:480px;}
.ce{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.6);font-weight:600;text-align:center;margin-bottom:8px;}
.ct{font-size:28px;font-weight:800;text-align:center;color:#d4af37;margin-bottom:35px;}
.ig{margin-bottom:22px;}
.ig label{display:block;margin-bottom:8px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.35);}
.ig input{width:100%;padding:16px 20px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;color:#fff;font-size:16px;outline:none;}
.ig input:focus{border-color:rgba(212,175,55,0.5);}
.cb{width:100%;padding:18px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#000;border:none;border-radius:16px;font-size:15px;font-weight:700;cursor:pointer;margin-top:15px;}
#result{margin-top:30px;text-align:center;display:none;padding:30px;border-radius:20px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);}
.rv{font-size:48px;font-weight:800;color:#d4af37;}
.rr{font-size:13px;color:rgba(255,255,255,0.3);margin-top:8px;}
</style></head><body>
<div class="c">
<p class="ce">Risk Management</p><h1 class="ct">Position Sizer</h1>
<div class="ig"><label>Account Balance</label><input type="number" id="a" placeholder="10000"></div>
<div class="ig"><label>Risk Per Trade (%)</label><input type="number" id="r" placeholder="2.0"></div>
<div class="ig"><label>Stop Loss (Pips)</label><input type="number" id="s" placeholder="50"></div>
<button class="cb" onclick="calc()">Calculate Position</button>
<div id="result"><p style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Recommended Lot Size</p><p class="rv" id="lv"></p><p class="rr" id="ra"></p></div>
</div>
<script>function calc(){var a=parseFloat(document.getElementById('a').value);var r=parseFloat(document.getElementById('r').value);var s=parseFloat(document.getElementById('s').value);if(!a||!r||!s)return;var ra=(a*r/100);var l=(ra/(s*10)).toFixed(2);document.getElementById('lv').textContent=l+' Lot';document.getElementById('ra').textContent='Risk: $'+ra.toFixed(2);document.getElementById('result').style.display='block';}</script>
</body></html>"""

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
        "Created": [datetime.now().strftime("%Y-%m-%d")] * 2
    })
if 'html_reports' not in st.session_state:
    st.session_state['html_reports'] = {
        datetime.now().strftime("%Y-%m-%d"): DEFAULT_REPORT_HTML
    }
if 'pages_db' not in st.session_state:
    st.session_state['pages_db'] = {}
if 'hero_quote' not in st.session_state:
    st.session_state['hero_quote'] = "The trend is your friend until it bends at the end."
if 'hero_subtitle' not in st.session_state:
    st.session_state['hero_subtitle'] = "Smart Money Intelligence Platform"
if 'news_articles' not in st.session_state:
    st.session_state['news_articles'] = [
        {
            "title": "Gold Surges Past $3,300 on Safe Haven Demand",
            "desc": "Institutional buyers accumulate as geopolitical tensions rise. COT data shows record net longs.",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tag": "GOLD"
        },
        {
            "title": "Fed Holds Rates Steady - What It Means for Markets",
            "desc": "The Federal Reserve kept rates unchanged. Dollar weakness expected in coming sessions.",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tag": "MACRO"
        },
        {
            "title": "Bitcoin Breaks $94K - New ATH in Sight?",
            "desc": "Crypto markets rally as institutional adoption accelerates. Key resistance at $95,500.",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tag": "CRYPTO"
        }
    ]


# ============================================
# 7. FETCH LIVE PRICES
# ============================================
@st.cache_data(ttl=300)
def fetch_live_prices():
    prices = {
        "XAUUSD": {"price": "3,312.45", "change": "+0.54", "up": True},
        "EURUSD": {"price": "1.1382", "change": "+0.18", "up": True},
        "SPX500": {"price": "5,525.21", "change": "-0.32", "up": False},
        "BTCUSD": {"price": "94,250", "change": "+1.24", "up": True},
    }
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            btc_price = data['bitcoin']['usd']
            btc_change = round(data['bitcoin']['usd_24h_change'], 2)
            btc_up = btc_change >= 0
            prices["BTCUSD"] = {
                "price": "{:,.0f}".format(btc_price),
                "change": ("+" if btc_up else "") + str(btc_change),
                "up": btc_up
            }
    except Exception:
        pass

    try:
        url2 = "https://api.frankfurter.app/latest?from=USD&to=EUR"
        resp2 = requests.get(url2, timeout=5)
        if resp2.status_code == 200:
            data2 = resp2.json()
            eur_rate = round(1.0 / data2['rates']['EUR'], 4)
            prices["EURUSD"] = {
                "price": str(eur_rate),
                "change": "+0.12",
                "up": True
            }
    except Exception:
        pass

    try:
        gold_url = "https://api.metalpriceapi.com/v1/latest?api_key=demo&base=XAU&currencies=USD"
        resp3 = requests.get(gold_url, timeout=5)
        if resp3.status_code == 200:
            data3 = resp3.json()
            if 'rates' in data3 and 'USD' in data3['rates']:
                gold_price = round(data3['rates']['USD'], 2)
                prices["XAUUSD"] = {
                    "price": "{:,.2f}".format(gold_price),
                    "change": "+0.54",
                    "up": True
                }
    except Exception:
        pass

    return prices


# ============================================
# 8. HEADER WITH MENU
# ============================================
def render_header():
    uname = st.session_state['username'] if st.session_state['username'] else "User"
    u_init = uname[0].upper()

    header_html = (
        '<div style="'
        'background:rgba(10,10,10,0.95);'
        'backdrop-filter:blur(20px);'
        'border:1px solid rgba(255,255,255,0.06);'
        'border-radius:16px;'
        'padding:14px 24px;'
        'margin-bottom:6px;'
        'display:flex;align-items:center;justify-content:space-between;">'
        '<div style="display:flex;align-items:center;gap:10px;">'
        '<img src="' + LOGO_URL + '" width="34" height="34" '
        'style="border-radius:50%;object-fit:cover;'
        'border:2px solid rgba(212,175,55,0.4);">'
        '<span style="font-size:14px;font-weight:700;letter-spacing:2px;'
        'color:#d4af37;">ROLLIC TRADES</span>'
        '</div>'
        '<div style="display:flex;align-items:center;gap:8px;">'
        '<span style="font-size:11px;color:rgba(255,255,255,0.35);'
        'font-weight:500;">' + uname + '</span>'
        '<div style="width:28px;height:28px;border-radius:50%;'
        'background:linear-gradient(135deg,#d4af37,#8b6914);'
        'display:flex;align-items:center;justify-content:center;'
        'font-size:11px;font-weight:800;color:#000;">' + u_init + '</div>'
        '</div></div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    current = st.session_state['current_page']
    is_admin = (st.session_state['user_role'] == 'Admin')

    if is_admin:
        cols = st.columns([1, 1, 1, 1, 1, 1])
    else:
        cols = st.columns([1, 1, 1, 1, 1])

    pages_list = [
        ("home", "Home"),
        ("macro", "Macro"),
        ("reports", "Reports"),
        ("calculator", "Calculator"),
    ]

    for i, (pid, plabel) in enumerate(pages_list):
        with cols[i]:
            if st.button(plabel, use_container_width=True, key="nav_" + pid):
                st.session_state['current_page'] = pid
                st.rerun()

    if is_admin:
        with cols[4]:
            if st.button("Admin", use_container_width=True, key="nav_admin"):
                st.session_state['current_page'] = 'admin'
                st.rerun()
        with cols[5]:
            if st.button("Sign Out", use_container_width=True, key="nav_out"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()
    else:
        with cols[4]:
            if st.button("Sign Out", use_container_width=True, key="nav_out"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)


# ============================================
# 9. FOOTER
# ============================================
def render_footer():
    footer_html = (
        '<div style="margin-top:80px;padding:50px 20px 40px;'
        'border-top:1px solid rgba(255,255,255,0.06);text-align:center;">'
        '<div style="margin-bottom:15px;">'
        '<img src="' + LOGO_URL + '" width="42" height="42" '
        'style="border-radius:50%;object-fit:cover;'
        'border:2px solid rgba(212,175,55,0.3);">'
        '</div>'
        '<p style="font-size:13px;font-weight:700;letter-spacing:3px;'
        'color:rgba(212,175,55,0.6);margin-bottom:4px;">ROLLIC TRADES</p>'
        '<p style="font-size:11px;color:rgba(255,255,255,0.3);">'
        'Smart Money Intelligence Platform</p>'
        '<div style="display:flex;justify-content:center;gap:28px;'
        'margin:25px 0;flex-wrap:wrap;">'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Home</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Macro Terminal</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Daily Reports</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Risk Calculator</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Academy</span>'
        '</div>'
        '<div style="width:60px;height:1px;margin:25px auto;'
        'background:linear-gradient(90deg,transparent,rgba(212,175,55,0.4),transparent);"></div>'
        '<p style="max-width:650px;margin:0 auto;font-size:11px;'
        'line-height:1.9;color:rgba(255,255,255,0.3);">'
        '<strong style="color:rgba(255,255,255,0.45);">Risk Disclaimer</strong><br>'
        'Trading foreign exchange, gold, and indices on margin carries a high level of risk '
        'and may not be suitable for all investors. Analysis is for educational purposes only. '
        'Past performance is not indicative of future results. Trade responsibly.</p>'
        '<div style="width:60px;height:1px;margin:25px auto;'
        'background:linear-gradient(90deg,transparent,rgba(212,175,55,0.4),transparent);"></div>'
        '<div style="display:flex;justify-content:center;gap:20px;'
        'margin-bottom:20px;flex-wrap:wrap;">'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);">Privacy Policy</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.15);">|</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);">Terms of Service</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.15);">|</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);">Contact</span>'
        '</div>'
        '<p style="font-size:10px;color:rgba(255,255,255,0.15);letter-spacing:2px;">'
        '2026 ROLLIC TRADES - ALL RIGHTS RESERVED</p>'
        '</div>'
    )
    st.markdown(footer_html, unsafe_allow_html=True)


# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
        logo_html = (
            '<div style="text-align:center;margin-bottom:20px;">'
            '<img src="' + LOGO_URL + '" width="110" height="110" '
            'style="border-radius:50%;object-fit:cover;'
            'border:2.5px solid #d4af37;'
            'box-shadow:0 0 12px rgba(212,175,55,0.25),0 0 30px rgba(212,175,55,0.1);">'
            '</div>'
            '<div style="text-align:center;margin-bottom:6px;">'
            '<p style="font-size:9px;letter-spacing:5px;text-transform:uppercase;'
            'color:rgba(212,175,55,0.4);font-weight:600;margin-bottom:6px;">'
            'INSTITUTIONAL TRADING</p>'
            '<h1 style="font-size:30px;font-weight:800;margin:0;'
            'background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
            'background-size:200% auto;-webkit-background-clip:text;'
            '-webkit-text-fill-color:transparent;'
            'animation:shimmer 3.5s ease-in-out infinite;">ROLLIC TRADES</h1>'
            '<p style="color:rgba(255,255,255,0.2);font-size:12px;margin-top:4px;">'
            'Smart Money Intelligence Platform</p></div>'
        )
        st.markdown(logo_html, unsafe_allow_html=True)
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

        username = st.text_input("USERNAME", placeholder="Enter username", key="login_user")
        password = st.text_input("PASSWORD", placeholder="Enter password", type="password", key="login_pass")
        st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

        if st.button("SIGN IN", use_container_width=True, key="login_btn"):
            db = st.session_state['users_db']
            match = db[(db['Username'] == username) & (db['Password'] == password)]
            if not match.empty:
                if match.iloc[0]['Status'] == 'Active':
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = match.iloc[0]['Role']
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Account suspended.")
            else:
                st.error("Invalid credentials")

        st.markdown(
            '<div style="text-align:center;margin-top:22px;">'
            '<span style="width:7px;height:7px;background:#30d158;border-radius:50%;'
            'display:inline-block;animation:pulse-glow 2s infinite;"></span>'
            '<span style="color:rgba(255,255,255,0.15);font-size:10px;'
            'margin-left:6px;">Encrypted Connection</span></div>',
            unsafe_allow_html=True
        )


# ============================================
# HOME PAGE
# ============================================
def home_page():
    live_prices = fetch_live_prices()
    hero_quote = st.session_state['hero_quote']
    hero_sub = st.session_state['hero_subtitle']

    # === ANIMATED HERO BANNER ===
    hero_html = (
        '<div style="'
        'background:linear-gradient(135deg,rgba(212,175,55,0.06) 0%,rgba(0,0,0,0.9) 40%,rgba(212,175,55,0.04) 100%);'
        'border:1px solid rgba(212,175,55,0.1);'
        'border-radius:24px;padding:50px 30px;text-align:center;'
        'margin-bottom:30px;position:relative;overflow:hidden;'
        'animation:fadeInUp 0.8s ease-out;">'
        '<div style="position:absolute;top:-100px;left:50%;transform:translateX(-50%);'
        'width:500px;height:500px;background:radial-gradient(circle,'
        'rgba(212,175,55,0.08) 0%,transparent 70%);pointer-events:none;'
        'animation:glow-pulse 4s ease-in-out infinite;"></div>'
        '<p style="font-size:9px;letter-spacing:6px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:15px;'
        'position:relative;">ROLLIC TRADES</p>'
        '<h1 style="font-size:32px;font-weight:800;color:#fff;margin:0 auto;'
        'max-width:700px;line-height:1.3;position:relative;">'
        '"<span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;'
        '-webkit-text-fill-color:transparent;animation:shimmer 3.5s ease-in-out infinite;">'
        + hero_quote + '</span>"</h1>'
        '<p style="color:rgba(255,255,255,0.3);font-size:13px;margin-top:15px;'
        'position:relative;">' + hero_sub + '</p>'
        '<div style="margin-top:20px;display:flex;justify-content:center;'
        'align-items:center;gap:8px;position:relative;">'
        '<span style="width:7px;height:7px;background:#30d158;border-radius:50%;'
        'display:inline-block;animation:pulse-glow 2s infinite;"></span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);font-weight:500;">'
        'Markets Open</span></div>'
        '</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # === LIVE TICKER BAR ===
    xau = live_prices.get("XAUUSD", {"price": "3,312", "change": "+0.54", "up": True})
    eur = live_prices.get("EURUSD", {"price": "1.1382", "change": "+0.18", "up": True})
    spx = live_prices.get("SPX500", {"price": "5,525", "change": "-0.32", "up": False})
    btc = live_prices.get("BTCUSD", {"price": "94,250", "change": "+1.24", "up": True})

    def tc(data):
        return "#30d158" if data["up"] else "#ff453a"

    ticker_html = (
        '<div style="overflow:hidden;background:rgba(212,175,55,0.03);'
        'border:1px solid rgba(212,175,55,0.06);border-radius:12px;'
        'padding:10px 0;margin-bottom:30px;">'
        '<div style="display:flex;white-space:nowrap;'
        'animation:ticker-scroll 25s linear infinite;">'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'XAUUSD <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + xau["price"] + '</span> <span style="color:' + tc(xau) + ';">'
        + xau["change"] + '%</span></span>'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'EURUSD <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + eur["price"] + '</span> <span style="color:' + tc(eur) + ';">'
        + eur["change"] + '%</span></span>'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'SP500 <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + spx["price"] + '</span> <span style="color:' + tc(spx) + ';">'
        + spx["change"] + '%</span></span>'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'BTCUSD <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + btc["price"] + '</span> <span style="color:' + tc(btc) + ';">'
        + btc["change"] + '%</span></span>'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'XAUUSD <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + xau["price"] + '</span> <span style="color:' + tc(xau) + ';">'
        + xau["change"] + '%</span></span>'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'EURUSD <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + eur["price"] + '</span> <span style="color:' + tc(eur) + ';">'
        + eur["change"] + '%</span></span>'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'SP500 <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + spx["price"] + '</span> <span style="color:' + tc(spx) + ';">'
        + spx["change"] + '%</span></span>'

        '<span style="display:inline-flex;align-items:center;gap:6px;'
        'padding:0 25px;font-size:12px;font-weight:600;color:rgba(255,255,255,0.5);">'
        'BTCUSD <span style="color:#d4af37;font-family:JetBrains Mono,monospace;">'
        + btc["price"] + '</span> <span style="color:' + tc(btc) + ';">'
        + btc["change"] + '%</span></span>'

        '</div></div>'
    )
    st.markdown(ticker_html, unsafe_allow_html=True)

    # === MARKET OVERVIEW - TRADINGVIEW WIDGETS ===
    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">'
        'LIVE MARKETS</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:6px;">'
        'Market <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Overview</span></p>'
        '<p style="font-size:14px;color:rgba(255,255,255,0.25);text-align:center;margin-bottom:30px;">'
        'Real-time TradingView charts</p>',
        unsafe_allow_html=True
    )

    tv_widgets = [
        ("XAUUSD", "OANDA:XAUUSD"),
        ("EURUSD", "FX:EURUSD"),
        ("SP500", "FOREXCOM:SPXUSD"),
        ("BTCUSD", "COINBASE:BTCUSD"),
    ]

    w1, w2 = st.columns(2)
    for i, (label, symbol) in enumerate(tv_widgets):
        col_target = w1 if i % 2 == 0 else w2
        with col_target:
            widget_html = (
                '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                'border-radius:18px;overflow:hidden;margin-bottom:15px;">'
                '<div style="padding:12px 16px 0;display:flex;align-items:center;'
                'justify-content:space-between;">'
                '<span style="font-size:11px;font-weight:700;letter-spacing:1.5px;'
                'text-transform:uppercase;color:rgba(255,255,255,0.4);">' + label + '</span>'
                '<div style="display:flex;align-items:center;gap:4px;">'
                '<span style="width:5px;height:5px;background:#30d158;border-radius:50%;'
                'display:inline-block;animation:pulse-glow 2s infinite;"></span>'
                '<span style="font-size:9px;color:rgba(255,255,255,0.2);">LIVE</span>'
                '</div></div></div>'
            )
            st.markdown(widget_html, unsafe_allow_html=True)

            tv_embed = (
                '<!-- TradingView Widget -->'
                '<div class="tradingview-widget-container">'
                '<div class="tradingview-widget-container__widget"></div>'
                '<script type="text/javascript" '
                'src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" '
                'async>'
                '{"symbol":"' + symbol + '",'
                '"width":"100%","height":"220",'
                '"locale":"en","dateRange":"1M",'
                '"colorTheme":"dark",'
                '"isTransparent":true,'
                '"autosize":true,'
                '"largeChartUrl":"",'
                '"chartOnly":false,'
                '"noTimeScale":false}'
                '</script></div>'
            )
            components.html(tv_embed, height=240)

    st.markdown("<hr>", unsafe_allow_html=True)

    # === TRADER TOOLKIT ===
    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">'
        'TRADING SUITE</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:6px;">'
        'Trader <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Toolkit</span></p>'
        '<p style="font-size:14px;color:rgba(255,255,255,0.25);text-align:center;margin-bottom:35px;">'
        'Click any card to open</p>',
        unsafe_allow_html=True
    )

    t1, t2, t3 = st.columns(3)

    # Card 1 - Reports
    with t1:
        card_html = (
            '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
            'border-radius:20px;padding:30px;text-align:center;min-height:220px;cursor:pointer;'
            'transition:all 0.4s ease;" '
            'onmouseover="this.style.background=\'rgba(212,175,55,0.06)\';'
            'this.style.borderColor=\'rgba(212,175,55,0.2)\';'
            'this.style.transform=\'translateY(-4px)\';'
            'this.style.boxShadow=\'0 16px 48px rgba(212,175,55,0.08)\'" '
            'onmouseout="this.style.background=\'rgba(255,255,255,0.02)\';'
            'this.style.borderColor=\'rgba(255,255,255,0.05)\';'
            'this.style.transform=\'translateY(0)\';'
            'this.style.boxShadow=\'none\'">'
            '<div style="width:52px;height:52px;border-radius:14px;background:rgba(212,175,55,0.08);'
            'display:flex;align-items:center;justify-content:center;margin:0 auto 14px;font-size:24px;">'
            '📄</div>'
            '<p style="color:#fff;font-size:17px;font-weight:700;margin-bottom:8px;">Daily Reports</p>'
            '<p style="color:rgba(255,255,255,0.3);font-size:12px;line-height:1.7;margin-bottom:14px;">'
            'Expert analysis with Smart Money decode</p>'
            '<span style="font-size:9px;padding:4px 10px;border-radius:20px;'
            'background:rgba(48,209,88,0.08);color:#30d158;font-weight:600;">UPDATED DAILY</span>'
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
        if st.button("Open Reports", use_container_width=True, key="tk_rep"):
            st.session_state['current_page'] = 'reports'
            st.rerun()

    # Card 2 - Macro
    with t2:
        card_html2 = (
            '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
            'border-radius:20px;padding:30px;text-align:center;min-height:220px;cursor:pointer;'
            'transition:all 0.4s ease;" '
            'onmouseover="this.style.background=\'rgba(0,122,255,0.04)\';'
            'this.style.borderColor=\'rgba(0,122,255,0.15)\';'
            'this.style.transform=\'translateY(-4px)\';'
            'this.style.boxShadow=\'0 16px 48px rgba(0,122,255,0.06)\'" '
            'onmouseout="this.style.background=\'rgba(255,255,255,0.02)\';'
            'this.style.borderColor=\'rgba(255,255,255,0.05)\';'
            'this.style.transform=\'translateY(0)\';'
            'this.style.boxShadow=\'none\'">'
            '<div style="width:52px;height:52px;border-radius:14px;background:rgba(0,122,255,0.08);'
            'display:flex;align-items:center;justify-content:center;margin:0 auto 14px;font-size:24px;">'
            '📊</div>'
            '<p style="color:#fff;font-size:17px;font-weight:700;margin-bottom:8px;">Macro Terminal</p>'
            '<p style="color:rgba(255,255,255,0.3);font-size:12px;line-height:1.7;margin-bottom:14px;">'
            'Economic indicators and Fed tracking</p>'
            '<span style="font-size:9px;padding:4px 10px;border-radius:20px;'
            'background:rgba(0,122,255,0.08);color:#007AFF;font-weight:600;">LIVE DATA</span>'
            '</div>'
        )
        st.markdown(card_html2, unsafe_allow_html=True)
        if st.button("Open Terminal", use_container_width=True, key="tk_mac"):
            st.session_state['current_page'] = 'macro'
            st.rerun()

    # Card 3 - Calculator
    with t3:
        card_html3 = (
            '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
            'border-radius:20px;padding:30px;text-align:center;min-height:220px;cursor:pointer;'
            'transition:all 0.4s ease;" '
            'onmouseover="this.style.background=\'rgba(191,90,242,0.04)\';'
            'this.style.borderColor=\'rgba(191,90,242,0.15)\';'
            'this.style.transform=\'translateY(-4px)\';'
            'this.style.boxShadow=\'0 16px 48px rgba(191,90,242,0.06)\'" '
            'onmouseout="this.style.background=\'rgba(255,255,255,0.02)\';'
            'this.style.borderColor=\'rgba(255,255,255,0.05)\';'
            'this.style.transform=\'translateY(0)\';'
            'this.style.boxShadow=\'none\'">'
            '<div style="width:52px;height:52px;border-radius:14px;background:rgba(191,90,242,0.08);'
            'display:flex;align-items:center;justify-content:center;margin:0 auto 14px;font-size:24px;">'
            '🧮</div>'
            '<p style="color:#fff;font-size:17px;font-weight:700;margin-bottom:8px;">Risk Calculator</p>'
            '<p style="color:rgba(255,255,255,0.3);font-size:12px;line-height:1.7;margin-bottom:14px;">'
            'Precision position sizing tool</p>'
            '<span style="font-size:9px;padding:4px 10px;border-radius:20px;'
            'background:rgba(191,90,242,0.08);color:#BF5AF2;font-weight:600;">TOOL</span>'
            '</div>'
        )
        st.markdown(card_html3, unsafe_allow_html=True)
        if st.button("Open Calculator", use_container_width=True, key="tk_cal"):
            st.session_state['current_page'] = 'calculator'
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # === NEWS / ARTICLES SECTION ===
    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">'
        'LATEST INTELLIGENCE</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:6px;">'
        'Market <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">News</span></p>'
        '<p style="font-size:14px;color:rgba(255,255,255,0.25);text-align:center;margin-bottom:35px;">'
        'Curated market insights and analysis</p>',
        unsafe_allow_html=True
    )

    articles = st.session_state['news_articles']
    for idx, article in enumerate(articles):
        tag_colors = {
            "GOLD": ("#d4af37", "rgba(212,175,55,0.08)"),
            "MACRO": ("#007AFF", "rgba(0,122,255,0.08)"),
            "CRYPTO": ("#FF9F0A", "rgba(255,159,10,0.08)"),
            "FOREX": ("#30D158", "rgba(48,209,88,0.08)"),
        }
        tag = article.get("tag", "GOLD")
        tag_color, tag_bg = tag_colors.get(tag, ("#d4af37", "rgba(212,175,55,0.08)"))

        article_html = (
            '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
            'border-radius:20px;padding:25px;margin-bottom:15px;'
            'transition:all 0.3s ease;cursor:pointer;" '
            'onmouseover="this.style.borderColor=\'rgba(212,175,55,0.15)\';'
            'this.style.background=\'rgba(255,255,255,0.03)\'" '
            'onmouseout="this.style.borderColor=\'rgba(255,255,255,0.05)\';'
            'this.style.background=\'rgba(255,255,255,0.02)\'">'
            '<div style="display:flex;align-items:center;justify-content:space-between;'
            'margin-bottom:12px;">'
            '<span style="font-size:9px;padding:4px 12px;border-radius:20px;'
            'background:' + tag_bg + ';color:' + tag_color + ';'
            'font-weight:700;letter-spacing:1px;">' + tag + '</span>'
            '<span style="font-size:11px;color:rgba(255,255,255,0.2);">'
            + article["date"] + '</span>'
            '</div>'
            '<h3 style="color:#fff;font-size:17px;font-weight:700;margin-bottom:8px;'
            'line-height:1.4;">' + article["title"] + '</h3>'
            '<p style="color:rgba(255,255,255,0.35);font-size:13px;line-height:1.7;">'
            + article["desc"] + '</p>'
            '</div>'
        )
        st.markdown(article_html, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # === QUICK STATS ===
    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">'
        'PLATFORM</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:30px;">'
        'Quick <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Stats</span></p>',
        unsafe_allow_html=True
    )
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Reports", len(st.session_state['html_reports']))
    with s2:
        st.metric("Users", len(st.session_state['users_db']))
    with s3:
        st.metric("Platform", "v3.0")
    with s4:
        st.metric("Uptime", "99.9%")


# ============================================
# CALCULATOR PAGE
# ============================================
def calculator_page():
    st.markdown(
        '<div style="text-align:center;padding:20px 0 5px;">'
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:6px;">RISK MANAGEMENT</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;margin-bottom:6px;">'
        'Position <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Calculator</span></p></div>',
        unsafe_allow_html=True
    )
    components.html(CALCULATOR_HTML, height=680, scrolling=False)


# ============================================
# ADMIN PANEL
# ============================================
def admin_panel():
    st.markdown(
        '<div style="text-align:center;padding:20px 0 5px;">'
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:6px;">SYSTEM CONTROL</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;margin-bottom:25px;">'
        'Admin <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Console</span></p></div>',
        unsafe_allow_html=True
    )

    # Stats
    total_u = str(len(st.session_state['users_db']))
    active_u = str(len(st.session_state['users_db'][st.session_state['users_db']['Status'] == 'Active']))
    total_r = str(len(st.session_state['html_reports']))
    total_n = str(len(st.session_state['news_articles']))

    a1, a2, a3, a4 = st.columns(4)
    for col_obj, val, label in [(a1, total_u, "Users"), (a2, active_u, "Active"),
                                 (a3, total_r, "Reports"), (a4, total_n, "Articles")]:
        with col_obj:
            st.markdown(
                '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                'border-radius:16px;padding:24px;text-align:center;">'
                '<div style="font-size:36px;font-weight:800;color:#d4af37;">' + val + '</div>'
                '<div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;'
                'color:rgba(255,255,255,0.3);font-weight:600;margin-top:6px;">' + label + '</div>'
                '</div>', unsafe_allow_html=True
            )

    st.markdown('<div style="height:15px;"></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Reports", "👥 Users", "📑 Pages",
        "✏️ Hero Banner", "📰 News Manager"
    ])

    # TAB 1: REPORTS
    with tab1:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        uc1, uc2 = st.columns([2, 1])
        with uc1:
            uploaded_file = st.file_uploader("HTML File", type=['html'],
                                              label_visibility="collapsed", key="rpt_up")
        with uc2:
            report_date = st.date_input("Date", datetime.now(), key="rpt_dt")

        if st.button("PUBLISH REPORT", use_container_width=True, key="pub_rpt"):
            if uploaded_file:
                html_str = uploaded_file.getvalue().decode("utf-8")
                dk = report_date.strftime("%Y-%m-%d")
                st.session_state['html_reports'][dk] = html_str
                st.success("Published for " + dk)
            else:
                st.error("Select file first.")

        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        for dk in sorted(st.session_state['html_reports'].keys(), reverse=True):
            rc1, rc2 = st.columns([5, 1])
            with rc1:
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.02);'
                    'border:1px solid rgba(255,255,255,0.05);border-radius:12px;'
                    'padding:12px 18px;margin-bottom:6px;">'
                    '<span style="color:#d4af37;">📄</span> '
                    '<span style="color:#fff;font-size:13px;font-weight:600;">'
                    + dk + '</span></div>', unsafe_allow_html=True
                )
            with rc2:
                if st.button("Del", key="dr_" + dk):
                    del st.session_state['html_reports'][dk]
                    st.rerun()

    # TAB 2: USERS
    with tab2:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.dataframe(st.session_state['users_db'], use_container_width=True, hide_index=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Add User")
        ac1, ac2 = st.columns(2)
        with ac1:
            new_user = st.text_input("Username", key="nu", placeholder="username")
        with ac2:
            new_pass = st.text_input("Password", key="np", placeholder="password", type="password")
        ac3, ac4 = st.columns(2)
        with ac3:
            new_role = st.selectbox("Role", ["User", "Admin"], key="nr")
        with ac4:
            new_status = st.selectbox("Status", ["Active", "Suspended"], key="ns")

        if st.button("CREATE USER", use_container_width=True, key="cr_u"):
            if new_user and new_pass:
                if new_user in st.session_state['users_db']['Username'].values:
                    st.error("Username exists!")
                else:
                    new_row = pd.DataFrame({
                        "Username": [new_user], "Password": [new_pass],
                        "Role": [new_role], "Status": [new_status],
                        "Created": [datetime.now().strftime("%Y-%m-%d")]
                    })
                    st.session_state['users_db'] = pd.concat(
                        [st.session_state['users_db'], new_row], ignore_index=True)
                    st.success("Created: " + new_user)
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Modify User")
        all_users = st.session_state['users_db']['Username'].tolist()
        m1, m2 = st.columns(2)
        with m1:
            sel_user = st.selectbox("User", all_users, key="mu")
        with m2:
            action = st.selectbox("Action", [
                "Activate", "Suspend", "Make Admin", "Make User",
                "Reset Password", "Delete"
            ], key="ma")

        new_pw = ""
        if action == "Reset Password":
            new_pw = st.text_input("New Password", type="password", key="rpw")

        if st.button("APPLY", use_container_width=True, key="apl"):
            db = st.session_state['users_db']
            idx = db[db['Username'] == sel_user].index
            if len(idx) > 0:
                i = idx[0]
                if action == "Activate":
                    db.at[i, 'Status'] = 'Active'
                    st.success(sel_user + " activated")
                    st.rerun()
                elif action == "Suspend":
                    if sel_user == "admin":
                        st.error("Cannot suspend admin!")
                    else:
                        db.at[i, 'Status'] = 'Suspended'
                        st.success(sel_user + " suspended")
                        st.rerun()
                elif action == "Make Admin":
                    db.at[i, 'Role'] = 'Admin'
                    st.success(sel_user + " is Admin")
                    st.rerun()
                elif action == "Make User":
                    if sel_user == "admin":
                        st.error("Cannot change admin!")
                    else:
                        db.at[i, 'Role'] = 'User'
                        st.rerun()
                elif action == "Reset Password":
                    if new_pw:
                        db.at[i, 'Password'] = new_pw
                        st.success("Password reset")
                        st.rerun()
                    else:
                        st.error("Enter password")
                elif action == "Delete":
                    if sel_user == "admin":
                        st.error("Cannot delete admin!")
                    else:
                        st.session_state['users_db'] = db.drop(i).reset_index(drop=True)
                        st.success(sel_user + " deleted")
                        st.rerun()

    # TAB 3: PAGES
    with tab3:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        pc1, pc2 = st.columns(2)
        with pc1:
            page_name = st.text_input("Page Name", key="pn", placeholder="e.g. Weekly Outlook")
        with pc2:
            page_icon = st.text_input("Icon", key="pi", value="📄")
        page_file = st.file_uploader("Page HTML", type=['html'], key="pf")

        if st.button("ADD PAGE", use_container_width=True, key="ap"):
            if page_name and page_file:
                html_c = page_file.getvalue().decode("utf-8")
                pid = page_name.lower().replace(" ", "_")
                st.session_state['pages_db'][pid] = {
                    'name': page_name, 'icon': page_icon, 'html': html_c,
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.success("Added: " + page_name)
                st.rerun()

        if st.session_state['pages_db']:
            st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
            for pid, pdata in st.session_state['pages_db'].items():
                p1, p2, p3 = st.columns([4, 1, 1])
                with p1:
                    st.markdown(
                        '<span style="font-size:16px;">' + pdata['icon'] + '</span> '
                        '<span style="color:#fff;font-weight:600;">' + pdata['name'] + '</span>',
                        unsafe_allow_html=True
                    )
                with p2:
                    if st.button("View", key="vp_" + pid):
                        st.session_state['current_page'] = 'custom_' + pid
                        st.rerun()
                with p3:
                    if st.button("Del", key="xp_" + pid):
                        del st.session_state['pages_db'][pid]
                        st.rerun()

    # TAB 4: HERO BANNER
    with tab4:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Edit Hero Banner")
        st.info("This text appears in the animated hero section on the Home page.")

        new_quote = st.text_area(
            "Hero Quote / Text",
            value=st.session_state['hero_quote'],
            height=100, key="hq_input"
        )
        new_sub = st.text_input(
            "Subtitle",
            value=st.session_state['hero_subtitle'],
            key="hs_input"
        )

        if st.button("UPDATE HERO BANNER", use_container_width=True, key="upd_hero"):
            st.session_state['hero_quote'] = new_quote
            st.session_state['hero_subtitle'] = new_sub
            st.success("Hero banner updated!")
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Preview")
        st.markdown(
            '<div style="background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.1);'
            'border-radius:16px;padding:30px;text-align:center;">'
            '<p style="font-size:20px;font-weight:700;color:#d4af37;line-height:1.4;">"'
            + st.session_state['hero_quote'] + '"</p>'
            '<p style="color:rgba(255,255,255,0.3);font-size:12px;margin-top:10px;">'
            + st.session_state['hero_subtitle'] + '</p></div>',
            unsafe_allow_html=True
        )

    # TAB 5: NEWS MANAGER
    with tab5:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Add News Article")

        n1, n2 = st.columns(2)
        with n1:
            news_title = st.text_input("Title", key="nt", placeholder="Article title")
        with n2:
            news_tag = st.selectbox("Category", ["GOLD", "MACRO", "CRYPTO", "FOREX"], key="ntg")

        news_desc = st.text_area("Description", key="nd", placeholder="Article summary...", height=100)

        if st.button("ADD ARTICLE", use_container_width=True, key="add_news"):
            if news_title and news_desc:
                st.session_state['news_articles'].insert(0, {
                    "title": news_title,
                    "desc": news_desc,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "tag": news_tag
                })
                st.success("Article added!")
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Current Articles")

        for i, art in enumerate(st.session_state['news_articles']):
            ac1, ac2 = st.columns([5, 1])
            with ac1:
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.02);'
                    'border:1px solid rgba(255,255,255,0.05);border-radius:12px;'
                    'padding:12px 18px;margin-bottom:6px;">'
                    '<span style="font-size:9px;padding:3px 8px;border-radius:10px;'
                    'background:rgba(212,175,55,0.08);color:#d4af37;font-weight:700;">'
                    + art["tag"] + '</span> '
                    '<span style="color:#fff;font-size:13px;font-weight:600;margin-left:8px;">'
                    + art["title"] + '</span></div>',
                    unsafe_allow_html=True
                )
            with ac2:
                if st.button("Del", key="dn_" + str(i)):
                    st.session_state['news_articles'].pop(i)
                    st.rerun()


# ============================================
# REPORTS PAGE
# ============================================
def reports_page():
    st.markdown(
        '<div style="text-align:center;padding:20px 0 5px;">'
        '<div style="margin-bottom:12px;">'
        '<img src="' + LOGO_URL + '" width="55" height="55" '
        'style="border-radius:50%;object-fit:cover;'
        'border:2.5px solid #d4af37;box-shadow:0 0 12px rgba(212,175,55,0.25);">'
        '</div>'
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:6px;">EXPERT ANALYSIS</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;margin-bottom:6px;">'
        'Daily <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Market Report</span></p></div>',
        unsafe_allow_html=True
    )
    dates = sorted(st.session_state['html_reports'].keys(), reverse=True)
    if dates:
        x1, cc, x2 = st.columns([2, 1, 2])
        with cc:
            sel_date = st.selectbox("Date", dates, label_visibility="collapsed")
        st.markdown("<hr>", unsafe_allow_html=True)
        if sel_date:
            components.html(st.session_state['html_reports'][sel_date], height=1500, scrolling=True)
    else:
        st.info("No reports. Upload from Admin.")


# ============================================
# CUSTOM PAGE VIEWER
# ============================================
def custom_page_viewer(page_id):
    pid = page_id.replace("custom_", "")
    if pid in st.session_state['pages_db']:
        pdata = st.session_state['pages_db'][pid]
        st.markdown(
            '<div style="text-align:center;padding:20px 0 5px;">'
            '<p style="font-size:30px;font-weight:800;color:#fff;">'
            + pdata['icon'] + ' '
            '<span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
            'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            'animation:shimmer 3.5s ease-in-out infinite;">' + pdata['name'] + '</span></p></div>',
            unsafe_allow_html=True
        )
        st.markdown("<hr>", unsafe_allow_html=True)
        components.html(pdata['html'], height=1500, scrolling=True)
    else:
        st.error("Page not found!")


# ============================================
# MACRO DASHBOARD
# ============================================
def macro_dashboard():
    st.markdown(
        '<div style="text-align:center;padding:20px 0 5px;">'
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:6px;">INSTITUTIONAL GRADE</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;margin-bottom:6px;">'
        'Macro <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Terminal</span></p>'
        '<p style="font-size:14px;color:rgba(255,255,255,0.25);margin-bottom:35px;">'
        'Economic intelligence and Smart Money positioning</p></div>',
        unsafe_allow_html=True
    )

    try:
        API_KEY = st.secrets["FRED_API_KEY"]
        fred = Fred(api_key=API_KEY)

        @st.cache_data(ttl=3600)
        def fetch_fred():
            smap = {"CPI": "CPIAUCSL", "Fed Rate": "FEDFUNDS", "US 10Y": "DGS10",
                    "Unemployment": "UNRATE", "GDP Growth": "A191RL1Q225SBEA", "PCE": "PCEPI"}
            results = {}
            for name, sid in smap.items():
                try:
                    d = fred.get_series(sid)
                    if len(d) >= 2:
                        results[name] = {'latest': round(float(d.iloc[-1]), 2),
                                         'previous': round(float(d.iloc[-2]), 2),
                                         'change': round(float(d.iloc[-1]) - float(d.iloc[-2]), 3)}
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
        st.info("Demo mode - add FRED_API_KEY for live data.")

    def build_gauge(value, prev_val, color):
        low = min(value, prev_val) * 0.85
        high = max(value, prev_val) * 1.15
        if low == high:
            low = value * 0.9
            high = value * 1.1
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=value,
            number={'font': {'size': 30, 'color': '#fff', 'family': 'Inter'}},
            gauge={'axis': {'range': [low, high], 'tickcolor': '#222',
                            'tickfont': {'color': '#444', 'size': 9}},
                   'bar': {'color': color, 'thickness': 0.3},
                   'bgcolor': 'rgba(0,0,0,0)', 'borderwidth': 0,
                   'threshold': {'line': {'color': '#fff', 'width': 1.5},
                                 'thickness': 0.75, 'value': prev_val}}
        ))
        fig.update_layout(height=190, margin=dict(l=20, r=20, t=25, b=0),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    items = [
        ("CPI Inflation", "CPI", "#FF453A", "BULLISH", "BEARISH", "Feb 12"),
        ("Fed Funds Rate", "Fed Rate", "#007AFF", "BULLISH", "BEARISH", "Mar 19"),
        ("US 10Y Yield", "US 10Y", "#d4af37", "BULLISH", "BEARISH", "Daily"),
        ("Unemployment", "Unemployment", "#FF9F0A", "BEARISH", "BULLISH", "Feb 7"),
        ("GDP Growth", "GDP Growth", "#30D158", "BULLISH", "BEARISH", "Feb 27"),
        ("PCE Index", "PCE", "#BF5AF2", "BULLISH", "BEARISH", "Feb 28"),
    ]

    for row in range(0, len(items), 3):
        cols = st.columns(3)
        for i, col_obj in enumerate(cols):
            idx_val = row + i
            if idx_val < len(items):
                title, key, color, dxy, gold, nxt = items[idx_val]
                d = fred_data.get(key, {'latest': 0, 'previous': 0, 'change': 0})
                with col_obj:
                    if d['change'] >= 0:
                        chg_c = "#30D158"
                        chg_bg = "rgba(48,209,88,0.08)"
                        chg_prefix = "+"
                    else:
                        chg_c = "#FF453A"
                        chg_bg = "rgba(255,69,58,0.08)"
                        chg_prefix = ""

                    st.markdown(
                        '<div style="background:rgba(255,255,255,0.025);'
                        'border:1px solid rgba(255,255,255,0.05);border-radius:20px;padding:16px;">'
                        '<div style="display:flex;align-items:center;justify-content:space-between;">'
                        '<span style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;'
                        'color:rgba(255,255,255,0.35);font-weight:600;">' + title + '</span>'
                        '<span style="font-size:9px;padding:3px 8px;border-radius:12px;'
                        'background:' + chg_bg + ';color:' + chg_c + ';font-weight:600;">'
                        + chg_prefix + str(abs(d['change'])) + '</span>'
                        '</div></div>',
                        unsafe_allow_html=True
                    )
                    st.plotly_chart(build_gauge(d['latest'], d['previous'], color),
                                   use_container_width=True, key="g_" + key + str(idx_val))
                    st.markdown(
                        '<div style="display:flex;justify-content:center;gap:6px;'
                        'margin-top:-10px;margin-bottom:10px;">'
                        '<span style="font-size:9px;padding:3px 10px;border-radius:14px;'
                        'background:rgba(0,122,255,0.08);color:#007AFF;font-weight:600;">'
                        'DXY: ' + dxy + '</span>'
                        '<span style="font-size:9px;padding:3px 10px;border-radius:14px;'
                        'background:rgba(212,175,55,0.08);color:#d4af37;font-weight:600;">'
                        'GOLD: ' + gold + '</span></div>'
                        '<p style="text-align:center;font-size:9px;color:rgba(255,255,255,0.15);">'
                        'Next: ' + nxt + '</p>',
                        unsafe_allow_html=True
                    )

    # COT
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">'
        'SMART MONEY</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:30px;">'
        'COT <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Analysis</span></p>',
        unsafe_allow_html=True
    )

    cl, cr = st.columns([1, 1.5])
    with cl:
        fig_cot = go.Figure(data=[go.Pie(
            values=[75, 25], hole=.78, direction='clockwise', sort=False,
            marker=dict(colors=['#d4af37', 'rgba(255,255,255,0.02)'],
                        line=dict(color='#000', width=2)),
            textinfo='none', hoverinfo='none'
        )])
        fig_cot.update_layout(
            showlegend=False, margin=dict(t=15, b=15, l=15, r=15), height=280,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text="75%", x=0.5, y=0.55, font_size=42, showarrow=False,
                     font_color="#d4af37", font_family="Inter"),
                dict(text="BULLISH", x=0.5, y=0.42, font_size=10, showarrow=False,
                     font_color="rgba(255,255,255,0.25)")
            ]
        )
        st.plotly_chart(fig_cot, use_container_width=True, key="cot_d")

    with cr:
        st.markdown(
            '<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.05);'
            'border-radius:20px;padding:28px;margin-top:5px;">'
            '<p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;'
            'color:rgba(212,175,55,0.5);font-weight:700;margin-bottom:14px;">XAUUSD POSITIONING</p>'
            '<p style="color:rgba(255,255,255,0.4);font-size:13px;line-height:1.8;margin-bottom:18px;">'
            'Commercial traders showing <strong style="color:#fff;">net long positioning</strong>. '
            'Smart Money accumulating at institutional zones.</p>'
            '<div style="display:flex;justify-content:space-around;text-align:center;'
            'padding:16px 0;border-top:1px solid rgba(255,255,255,0.03);'
            'border-bottom:1px solid rgba(255,255,255,0.03);">'
            '<div><p style="font-size:9px;color:rgba(255,255,255,0.25);text-transform:uppercase;'
            'margin-bottom:4px;">Longs</p>'
            '<p style="font-size:20px;font-weight:800;color:#30D158;">250K</p></div>'
            '<div><p style="font-size:9px;color:rgba(255,255,255,0.25);text-transform:uppercase;'
            'margin-bottom:4px;">Shorts</p>'
            '<p style="font-size:20px;font-weight:800;color:#FF453A;">50K</p></div>'
            '<div><p style="font-size:9px;color:rgba(255,255,255,0.25);text-transform:uppercase;'
            'margin-bottom:4px;">Net</p>'
            '<p style="font-size:20px;font-weight:800;color:#d4af37;">+200K</p></div>'
            '</div>'
            '<div style="margin-top:12px;text-align:center;">'
            '<span style="font-size:9px;padding:4px 14px;border-radius:20px;'
            'background:rgba(48,209,88,0.08);color:#30d158;font-weight:700;">'
            'BIAS: BULLISH</span></div></div>',
            unsafe_allow_html=True
        )


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

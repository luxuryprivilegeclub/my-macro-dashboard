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
        border-radius:12px!important;padding:10px 20px!important;
        font-family:'Inter',sans-serif!important;
        font-weight:600!important;font-size:13px!important;
        transition:all 0.3s ease!important;
    }
    div.stButton > button:hover {
        background:rgba(212,175,55,0.1)!important;
        color:#d4af37!important;border-color:rgba(212,175,55,0.25)!important;
    }
    div[data-testid="stTextInput"] input {
        background:rgba(255,255,255,0.03)!important;
        border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important;color:#fff!important;
        font-size:14px!important;padding:14px 16px!important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color:#d4af37!important;box-shadow:0 0 0 3px rgba(212,175,55,0.08)!important;
    }
    div[data-testid="stTextInput"] label{color:rgba(255,255,255,0.4)!important;font-weight:500!important;font-size:12px!important;}
    div[data-testid="stTextArea"] textarea{background:rgba(255,255,255,0.03)!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:12px!important;color:#fff!important;}
    div[data-testid="stTextArea"] label{color:rgba(255,255,255,0.4)!important;}
    div[data-testid="stSelectbox"] > div > div{background:rgba(255,255,255,0.03)!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:12px!important;}
    div[data-testid="stSelectbox"] label{color:rgba(255,255,255,0.4)!important;}
    div[data-testid="stTabs"] button{color:rgba(255,255,255,0.4)!important;font-weight:600!important;font-size:13px!important;background:transparent!important;}
    div[data-testid="stTabs"] button[aria-selected="true"]{color:#d4af37!important;border-bottom-color:#d4af37!important;}
    div[data-testid="stFileUploader"]{background:rgba(255,255,255,0.015)!important;border:2px dashed rgba(212,175,55,0.15)!important;border-radius:16px!important;}
    div[data-testid="stDateInput"] input{background:rgba(255,255,255,0.03)!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:12px!important;color:white!important;}
    div[data-testid="stMetric"]{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:16px;padding:18px;}
    div[data-testid="stMetric"] label{color:rgba(255,255,255,0.3)!important;font-size:11px!important;letter-spacing:1px!important;text-transform:uppercase!important;}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"]{color:#d4af37!important;font-weight:700!important;}
    hr{border:none!important;height:1px!important;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.05),transparent)!important;margin:35px 0!important;}
    h1 a,h2 a,h3 a{display:none!important;}

    @keyframes shimmer{0%,100%{background-position:0% center;}50%{background-position:200% center;}}
    @keyframes pulse-glow{0%,100%{box-shadow:0 0 0 0 rgba(48,209,88,0.4);}50%{box-shadow:0 0 0 8px rgba(48,209,88,0);}}
    @keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
    @keyframes fadeInUp{0%{opacity:0;transform:translateY(20px);}100%{opacity:1;transform:translateY(0);}}
    @keyframes glow-pulse{0%,100%{box-shadow:0 0 20px rgba(212,175,55,0.1);}50%{box-shadow:0 0 40px rgba(212,175,55,0.2);}}
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. DEFAULT HTMLS
# ============================================
DEFAULT_REPORT_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:'Inter',sans-serif;background:#000;color:#fff;}.mc{max-width:1000px;margin:0 auto;padding:30px 20px;}.hero{text-align:center;padding:60px 20px;}.ht{font-size:48px;font-weight:800;color:#d4af37;margin-bottom:10px;}.sec{margin-bottom:30px;padding:30px;background:rgba(255,255,255,0.03);border-radius:24px;border:1px solid rgba(255,255,255,0.06);}.sh{font-size:13px;font-weight:700;color:#d4af37;letter-spacing:2px;text-transform:uppercase;margin-bottom:25px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.04);}.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:15px;}.sc{background:rgba(255,255,255,0.02);padding:20px;border-radius:16px;border:1px solid rgba(255,255,255,0.04);text-align:center;}.sl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}.sv{font-size:28px;font-weight:800;color:#d4af37;}.lb{background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);padding:20px;border-radius:16px;margin-top:20px;font-size:14px;line-height:1.7;color:rgba(255,255,255,0.7);}.bl{text-align:center;padding:40px;background:rgba(212,175,55,0.03);border-radius:24px;border:1px solid rgba(212,175,55,0.15);}.bl h3{font-size:28px;font-weight:800;color:#d4af37;margin-bottom:10px;}.bl p{color:rgba(255,255,255,0.5);}</style></head><body><div class="mc"><section class="hero"><h1 class="ht">Gold Analysis</h1><p style="color:rgba(255,255,255,0.4);">Smart Money Positioning - APR 26 Contract</p></section><section class="sec"><div class="sh">Futures Data</div><div class="sg"><div class="sc"><div class="sl">Price</div><div class="sv" style="color:#FF453A">5,086</div></div><div class="sc"><div class="sl">Volume</div><div class="sv">129,968</div></div><div class="sc"><div class="sl">OI</div><div class="sv" style="color:#FF453A">+1,199</div></div><div class="sc"><div class="sl">Blocks</div><div class="sv">475</div></div></div><div class="lb"><strong>Logic:</strong> Price DOWN + OI UP = SHORT BUILDUP</div></section><section class="bl"><h3>VERDICT: BEARISH</h3><p>Short rallies into 5280 targeting 5020</p></section></div></body></html>"""

CALCULATOR_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{margin:0;padding:0;box-sizing:border-box;}body{background:transparent;display:flex;justify-content:center;padding:30px;font-family:'Inter',sans-serif;}.c{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:28px;padding:40px;width:100%;max-width:480px;}.ce{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.6);font-weight:600;text-align:center;margin-bottom:8px;}.ct{font-size:28px;font-weight:800;text-align:center;color:#d4af37;margin-bottom:35px;}.ig{margin-bottom:22px;}.ig label{display:block;margin-bottom:8px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.35);}.ig input{width:100%;padding:16px 20px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;color:#fff;font-size:16px;outline:none;}.ig input:focus{border-color:rgba(212,175,55,0.5);}.cb{width:100%;padding:18px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#000;border:none;border-radius:16px;font-size:15px;font-weight:700;cursor:pointer;margin-top:15px;}#result{margin-top:30px;text-align:center;display:none;padding:30px;border-radius:20px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);}.rv{font-size:48px;font-weight:800;color:#d4af37;}.rr{font-size:13px;color:rgba(255,255,255,0.3);margin-top:8px;}</style></head><body><div class="c"><p class="ce">Risk Management</p><h1 class="ct">Position Sizer</h1><div class="ig"><label>Account Balance</label><input type="number" id="a" placeholder="10000"></div><div class="ig"><label>Risk (%)</label><input type="number" id="r" placeholder="2.0"></div><div class="ig"><label>Stop Loss (Pips)</label><input type="number" id="s" placeholder="50"></div><button class="cb" onclick="calc()">Calculate</button><div id="result"><p style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Lot Size</p><p class="rv" id="lv"></p><p class="rr" id="ra"></p></div></div><script>function calc(){var a=parseFloat(document.getElementById('a').value);var r=parseFloat(document.getElementById('r').value);var s=parseFloat(document.getElementById('s').value);if(!a||!r||!s)return;var ra=(a*r/100);var l=(ra/(s*10)).toFixed(2);document.getElementById('lv').textContent=l+' Lot';document.getElementById('ra').textContent='Risk: $'+ra.toFixed(2);document.getElementById('result').style.display='block';}</script></body></html>"""

# ============================================
# 5. SESSION STATE
# ============================================
defaults = {
    'logged_in': False, 'user_role': None, 'username': None,
    'current_page': 'home',
    'hero_quote': "The trend is your friend until it bends at the end.",
    'hero_subtitle': "Smart Money Intelligence Platform",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if 'users_db' not in st.session_state:
    st.session_state['users_db'] = pd.DataFrame({
        "Username": ["admin", "user"], "Password": ["Rollic@786", "123"],
        "Role": ["Admin", "User"], "Status": ["Active", "Active"],
        "Created": [datetime.now().strftime("%Y-%m-%d")] * 2
    })

tool_keys = [
    "macro_terminal", "money_flow", "oi_analyzer", "gold_report", "forex_report",
    "btc_report", "sp500_report", "market_news", "calculator", "learning",
]

tool_meta = {
    "macro_terminal": {"name": "Macro Terminal", "icon": "📊", "color": "#007AFF", "tag": "LIVE DATA", "desc": "Economic indicators, COT analysis and Fed tracking"},
    "money_flow": {"name": "Money Flow Track", "icon": "💰", "color": "#30D158", "tag": "FLOW", "desc": "Track institutional money flow and liquidity zones"},
    "oi_analyzer": {"name": "OI Analyzer", "icon": "📈", "color": "#FF9F0A", "tag": "ANALYSIS", "desc": "Open Interest analysis with smart money positioning"},
    "gold_report": {"name": "Gold Intelligence", "icon": "🪙", "color": "#d4af37", "tag": "XAUUSD", "desc": "Institutional gold analysis with trade scenarios"},
    "forex_report": {"name": "Forex Intelligence", "icon": "💶", "color": "#BF5AF2", "tag": "FOREX", "desc": "Major pairs analysis with liquidity maps"},
    "btc_report": {"name": "BTC Intelligence", "icon": "₿", "color": "#FF9F0A", "tag": "CRYPTO", "desc": "Bitcoin institutional analysis and key levels"},
    "sp500_report": {"name": "S&P500 Intelligence", "icon": "📉", "color": "#FF453A", "tag": "INDEX", "desc": "S&P 500 smart money decode and scenarios"},
    "market_news": {"name": "Market News", "icon": "📰", "color": "#007AFF", "tag": "NEWS", "desc": "Curated market insights and breaking news"},
    "calculator": {"name": "Risk Calculator", "icon": "🧮", "color": "#BF5AF2", "tag": "TOOL", "desc": "Precision position sizing for every setup"},
    "learning": {"name": "Learning Academy", "icon": "🎓", "color": "#30D158", "tag": "LEARN", "desc": "Trading education and strategy courses"},
}

for tk in tool_keys:
    store_key = "content_" + tk
    if store_key not in st.session_state:
        if tk == "gold_report":
            st.session_state[store_key] = DEFAULT_REPORT_HTML
        else:
            st.session_state[store_key] = ""

if 'html_reports' not in st.session_state:
    st.session_state['html_reports'] = {datetime.now().strftime("%Y-%m-%d"): DEFAULT_REPORT_HTML}
if 'news_articles' not in st.session_state:
    st.session_state['news_articles'] = [
        {"title": "Gold Surges Past $3,300 on Safe Haven Demand", "desc": "Institutional buyers accumulate as geopolitical tensions rise.", "date": datetime.now().strftime("%Y-%m-%d"), "tag": "GOLD"},
        {"title": "Fed Holds Rates Steady", "desc": "Dollar weakness expected in coming sessions.", "date": datetime.now().strftime("%Y-%m-%d"), "tag": "MACRO"},
        {"title": "Bitcoin Breaks $94K", "desc": "Crypto markets rally as institutional adoption accelerates.", "date": datetime.now().strftime("%Y-%m-%d"), "tag": "CRYPTO"},
    ]


# ============================================
# 6. HEADER
# ============================================
def render_header():
    uname = st.session_state['username'] if st.session_state['username'] else "User"
    u_init = uname[0].upper()

    header_html = (
        '<div style="background:rgba(10,10,10,0.95);backdrop-filter:blur(20px);'
        'border:1px solid rgba(255,255,255,0.06);border-radius:16px;'
        'padding:14px 24px;margin-bottom:6px;display:flex;align-items:center;'
        'justify-content:space-between;">'
        '<div style="display:flex;align-items:center;gap:10px;">'
        '<img src="' + LOGO_URL + '" width="34" height="34" '
        'style="border-radius:50%;object-fit:cover;border:2px solid rgba(212,175,55,0.4);">'
        '<span style="font-size:14px;font-weight:700;letter-spacing:2px;color:#d4af37;">ROLLIC TRADES</span>'
        '</div>'
        '<div style="display:flex;align-items:center;gap:8px;">'
        '<span style="font-size:11px;color:rgba(255,255,255,0.35);font-weight:500;">' + uname + '</span>'
        '<div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#d4af37,#8b6914);'
        'display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#000;">'
        + u_init + '</div></div></div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    is_admin = (st.session_state['user_role'] == 'Admin')
    if is_admin:
        cols = st.columns([1, 1, 1])
    else:
        cols = st.columns([1, 1])

    with cols[0]:
        if st.button("Home", use_container_width=True, key="nav_home"):
            st.session_state['current_page'] = 'home'
            st.rerun()
    if is_admin:
        with cols[1]:
            if st.button("Admin", use_container_width=True, key="nav_admin"):
                st.session_state['current_page'] = 'admin'
                st.rerun()
        with cols[2]:
            if st.button("Sign Out", use_container_width=True, key="nav_out"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()
    else:
        with cols[1]:
            if st.button("Sign Out", use_container_width=True, key="nav_out"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()


# ============================================
# 7. TRADINGVIEW TICKER TAPE
# ============================================
def render_ticker_tape():
    tv_ticker = """
    <div style="border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.05);margin-bottom:25px;">
    <div class="tradingview-widget-container">
    <div class="tradingview-widget-container__widget"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
    {
    "symbols": [
        {"proName": "OANDA:XAUUSD","title": "Gold"},
        {"proName": "FX:EURUSD","title": "EUR/USD"},
        {"proName": "FOREXCOM:SPXUSD","title": "S&P 500"},
        {"proName": "COINBASE:BTCUSD","title": "Bitcoin"},
        {"proName": "FX:USDJPY","title": "USD/JPY"},
        {"proName": "FX:GBPUSD","title": "GBP/USD"},
        {"proName": "TVC:DXY","title": "DXY"},
        {"proName": "NYMEX:CL1!","title": "Crude Oil"}
    ],
    "showSymbolLogo": true,
    "isTransparent": true,
    "displayMode": "regular",
    "colorTheme": "dark",
    "locale": "en"
    }
    </script>
    </div>
    </div>
    """
    components.html(tv_ticker, height=78)


# ============================================
# 8. FOOTER
# ============================================
def render_footer():
    footer_html = (
        '<div style="margin-top:80px;padding:50px 20px 40px;'
        'border-top:1px solid rgba(255,255,255,0.06);text-align:center;">'
        '<div style="margin-bottom:15px;">'
        '<img src="' + LOGO_URL + '" width="42" height="42" '
        'style="border-radius:50%;object-fit:cover;border:2px solid rgba(212,175,55,0.3);">'
        '</div>'
        '<p style="font-size:13px;font-weight:700;letter-spacing:3px;color:rgba(212,175,55,0.6);margin-bottom:4px;">ROLLIC TRADES</p>'
        '<p style="font-size:11px;color:rgba(255,255,255,0.3);">Smart Money Intelligence Platform</p>'
        '<div style="display:flex;justify-content:center;gap:28px;margin:25px 0;flex-wrap:wrap;">'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Home</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Macro Terminal</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Reports</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Calculator</span>'
        '<span style="color:rgba(255,255,255,0.4);font-size:12px;font-weight:500;">Academy</span>'
        '</div>'
        '<div style="width:60px;height:1px;margin:25px auto;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.4),transparent);"></div>'
        '<p style="max-width:650px;margin:0 auto;font-size:11px;line-height:1.9;color:rgba(255,255,255,0.3);">'
        '<strong style="color:rgba(255,255,255,0.45);">Risk Disclaimer</strong><br>'
        'Trading carries high risk. Analysis is for educational purposes only. Trade responsibly.</p>'
        '<div style="width:60px;height:1px;margin:25px auto;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.4),transparent);"></div>'
        '<div style="display:flex;justify-content:center;gap:20px;margin-bottom:20px;">'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);">Privacy</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.15);">|</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);">Terms</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.15);">|</span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);">Contact</span>'
        '</div>'
        '<p style="font-size:10px;color:rgba(255,255,255,0.15);letter-spacing:2px;">2026 ROLLIC TRADES</p>'
        '</div>'
    )
    st.markdown(footer_html, unsafe_allow_html=True)


# ============================================
# LOGIN
# ============================================
def login_page():
    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;margin-bottom:20px;">'
            '<img src="' + LOGO_URL + '" width="110" height="110" '
            'style="border-radius:50%;object-fit:cover;border:2.5px solid #d4af37;'
            'box-shadow:0 0 12px rgba(212,175,55,0.25),0 0 30px rgba(212,175,55,0.1);">'
            '</div>'
            '<div style="text-align:center;margin-bottom:6px;">'
            '<p style="font-size:9px;letter-spacing:5px;text-transform:uppercase;'
            'color:rgba(212,175,55,0.4);font-weight:600;margin-bottom:6px;">INSTITUTIONAL TRADING</p>'
            '<h1 style="font-size:30px;font-weight:800;margin:0;'
            'background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;'
            '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            'animation:shimmer 3.5s ease-in-out infinite;">ROLLIC TRADES</h1>'
            '<p style="color:rgba(255,255,255,0.2);font-size:12px;margin-top:4px;">Smart Money Intelligence Platform</p>'
            '</div>', unsafe_allow_html=True
        )
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        username = st.text_input("USERNAME", placeholder="Enter username", key="lu")
        password = st.text_input("PASSWORD", placeholder="Enter password", type="password", key="lp")
        st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
        if st.button("SIGN IN", use_container_width=True, key="lb"):
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


# ============================================
# HOME PAGE
# ============================================
def home_page():
    hero_quote = st.session_state['hero_quote']
    hero_sub = st.session_state['hero_subtitle']

    render_ticker_tape()

    hero_html = (
        '<div style="background:linear-gradient(135deg,rgba(212,175,55,0.06) 0%,rgba(0,0,0,0.9) 40%,rgba(212,175,55,0.04) 100%);'
        'border:1px solid rgba(212,175,55,0.1);border-radius:24px;padding:50px 30px;text-align:center;'
        'margin-bottom:30px;position:relative;overflow:hidden;animation:fadeInUp 0.8s ease-out;">'
        '<div style="position:absolute;top:-100px;left:50%;transform:translateX(-50%);'
        'width:500px;height:500px;background:radial-gradient(circle,rgba(212,175,55,0.08) 0%,transparent 70%);'
        'pointer-events:none;animation:glow-pulse 4s ease-in-out infinite;"></div>'
        '<p style="font-size:9px;letter-spacing:6px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:15px;position:relative;">ROLLIC TRADES</p>'
        '<h1 style="font-size:32px;font-weight:800;color:#fff;margin:0 auto;max-width:700px;line-height:1.3;position:relative;">"'
        '<span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3.5s ease-in-out infinite;">'
        + hero_quote + '</span>"</h1>'
        '<p style="color:rgba(255,255,255,0.3);font-size:13px;margin-top:15px;position:relative;">' + hero_sub + '</p>'
        '<div style="margin-top:20px;display:flex;justify-content:center;align-items:center;gap:8px;position:relative;">'
        '<span style="width:7px;height:7px;background:#30d158;border-radius:50%;display:inline-block;'
        'animation:pulse-glow 2s infinite;"></span>'
        '<span style="font-size:10px;color:rgba(255,255,255,0.25);font-weight:500;">Markets Open</span>'
        '</div></div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">LIVE MARKETS</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:6px;">'
        'Market <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3.5s ease-in-out infinite;">'
        'Overview</span></p>'
        '<p style="font-size:14px;color:rgba(255,255,255,0.25);text-align:center;margin-bottom:30px;">'
        'Real-time TradingView charts</p>',
        unsafe_allow_html=True
    )

    tv_widgets_data = [("XAUUSD", "OANDA:XAUUSD"), ("EURUSD", "FX:EURUSD"), ("SP500", "FOREXCOM:SPXUSD"), ("BTCUSD", "COINBASE:BTCUSD")]

    w1, w2 = st.columns(2)
    for i, (label, symbol) in enumerate(tv_widgets_data):
        target_col = w1 if i % 2 == 0 else w2
        with target_col:
            st.markdown(
                '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                'border-radius:18px;overflow:hidden;margin-bottom:15px;">'
                '<div style="padding:12px 16px 0;display:flex;align-items:center;justify-content:space-between;">'
                '<span style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;'
                'color:rgba(255,255,255,0.4);">' + label + '</span>'
                '<div style="display:flex;align-items:center;gap:4px;">'
                '<span style="width:5px;height:5px;background:#30d158;border-radius:50%;display:inline-block;'
                'animation:pulse-glow 2s infinite;"></span>'
                '<span style="font-size:9px;color:rgba(255,255,255,0.2);">LIVE</span>'
                '</div></div></div>',
                unsafe_allow_html=True
            )
            tv_embed = (
                '<div class="tradingview-widget-container">'
                '<div class="tradingview-widget-container__widget"></div>'
                '<script type="text/javascript" '
                'src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>'
                '{"symbol":"' + symbol + '","width":"100%","height":"220",'
                '"locale":"en","dateRange":"1M","colorTheme":"dark",'
                '"isTransparent":true,"autosize":true,"largeChartUrl":""}</script></div>'
            )
            components.html(tv_embed, height=240)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">TRADING SUITE</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:6px;">'
        'Trader <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3.5s ease-in-out infinite;">'
        'Toolkit</span></p>'
        '<p style="font-size:14px;color:rgba(255,255,255,0.25);text-align:center;margin-bottom:35px;">'
        'Hover and click to explore</p>',
        unsafe_allow_html=True
    )

    for row_start in range(0, len(tool_keys), 5):
        row_keys = tool_keys[row_start:row_start + 5]
        cols = st.columns(len(row_keys))
        for col_obj, tk in zip(cols, row_keys):
            meta = tool_meta[tk]
            with col_obj:
                has_content = bool(st.session_state.get("content_" + tk, ""))
                if tk in ["calculator", "macro_terminal"]: has_content = True

                if has_content:
                    status_dot = '<span style="width:6px;height:6px;background:#30d158;border-radius:50%;display:inline-block;"></span>'
                    status_text = "ACTIVE"
                else:
                    status_dot = '<span style="width:6px;height:6px;background:rgba(255,255,255,0.15);border-radius:50%;display:inline-block;"></span>'
                    status_text = "COMING"

                card_html = (
                    '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                    'border-radius:20px;padding:24px 16px;text-align:center;min-height:200px;cursor:pointer;'
                    'transition:all 0.4s ease;" '
                    'onmouseover="this.style.background=\'rgba(' + str(int(meta["color"].lstrip("#")[0:2], 16)) + ','
                    + str(int(meta["color"].lstrip("#")[2:4], 16)) + ',' + str(int(meta["color"].lstrip("#")[4:6], 16))
                    + ',0.05)\';this.style.borderColor=\'rgba(' + str(int(meta["color"].lstrip("#")[0:2], 16)) + ','
                    + str(int(meta["color"].lstrip("#")[2:4], 16)) + ',' + str(int(meta["color"].lstrip("#")[4:6], 16))
                    + ',0.2)\';this.style.transform=\'translateY(-4px)\';'
                    'this.style.boxShadow=\'0 16px 48px rgba(' + str(int(meta["color"].lstrip("#")[0:2], 16)) + ','
                    + str(int(meta["color"].lstrip("#")[2:4], 16)) + ',' + str(int(meta["color"].lstrip("#")[4:6], 16))
                    + ',0.08)\'" '
                    'onmouseout="this.style.background=\'rgba(255,255,255,0.02)\';'
                    'this.style.borderColor=\'rgba(255,255,255,0.05)\';'
                    'this.style.transform=\'translateY(0)\';this.style.boxShadow=\'none\'">'
                    '<div style="font-size:28px;margin-bottom:10px;">' + meta["icon"] + '</div>'
                    '<p style="color:#fff;font-size:13px;font-weight:700;margin-bottom:6px;line-height:1.3;">'
                    + meta["name"] + '</p>'
                    '<p style="color:rgba(255,255,255,0.25);font-size:10px;line-height:1.5;margin-bottom:12px;">'
                    + meta["desc"] + '</p>'
                    '<div style="display:flex;align-items:center;justify-content:center;gap:5px;">'
                    + status_dot +
                    '<span style="font-size:8px;letter-spacing:1px;color:rgba(255,255,255,0.3);font-weight:600;">'
                    + status_text + '</span></div></div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                if st.button("Open", use_container_width=True, key="open_" + tk):
                    if tk == "macro_terminal": st.session_state['current_page'] = 'macro'
                    elif tk == "calculator": st.session_state['current_page'] = 'calculator'
                    else: st.session_state['current_page'] = 'tool_' + tk
                    st.rerun()


# ============================================
# TOOL PAGE VIEWER
# ============================================
def tool_page(tool_id):
    tk = tool_id.replace("tool_", "")
    meta = tool_meta.get(tk, {"name": "Unknown", "icon": "📄", "color": "#d4af37"})
    content = st.session_state.get("content_" + tk, "")

    st.markdown(
        '<div style="text-align:center;padding:20px 0 5px;">'
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:6px;">' + meta.get("tag", "ANALYSIS") + '</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;margin-bottom:6px;">'
        + meta["icon"] + ' <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">' + meta["name"] + '</span></p></div>',
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    if tk == "market_news":
        articles = st.session_state['news_articles']
        if articles:
            for art in articles:
                tag_colors = {"GOLD": "#d4af37", "MACRO": "#007AFF", "CRYPTO": "#FF9F0A", "FOREX": "#30D158"}
                tc = tag_colors.get(art.get("tag", "GOLD"), "#d4af37")
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                    'border-radius:20px;padding:25px;margin-bottom:15px;transition:all 0.3s ease;" '
                    'onmouseover="this.style.borderColor=\'rgba(212,175,55,0.15)\'" '
                    'onmouseout="this.style.borderColor=\'rgba(255,255,255,0.05)\'">'
                    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">'
                    '<span style="font-size:9px;padding:4px 12px;border-radius:20px;'
                    'background:rgba(212,175,55,0.08);color:' + tc + ';font-weight:700;letter-spacing:1px;">'
                    + art.get("tag", "NEWS") + '</span>'
                    '<span style="font-size:11px;color:rgba(255,255,255,0.2);">' + art["date"] + '</span></div>'
                    '<h3 style="color:#fff;font-size:17px;font-weight:700;margin-bottom:8px;line-height:1.4;">'
                    + art["title"] + '</h3>'
                    '<p style="color:rgba(255,255,255,0.35);font-size:13px;line-height:1.7;">'
                    + art["desc"] + '</p></div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No news articles yet. Admin can add from Admin Panel.")
        return

    if content:
        components.html(content, height=1500, scrolling=True)
    else:
        st.markdown(
            '<div style="text-align:center;padding:80px 20px;">'
            '<span style="font-size:60px;opacity:0.15;">' + meta["icon"] + '</span>'
            '<h3 style="color:rgba(255,255,255,0.25);margin-top:15px;">Content Coming Soon</h3>'
            '<p style="color:rgba(255,255,255,0.15);font-size:13px;margin-top:8px;">'
            'Admin will upload content for this section.</p></div>',
            unsafe_allow_html=True
        )


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
            smap = {"CPI": "CPIAUCSL", "Fed Rate": "FEDFUNDS", "US 10Y": "DGS10", "T10YIE": "T10YIE",
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
            "T10YIE": {'latest': 2.30, 'previous': 2.28, 'change': 0.02},
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
            gauge={'axis': {'range': [low, high], 'tickcolor': '#222', 'tickfont': {'color': '#444', 'size': 9}},
                   'bar': {'color': color, 'thickness': 0.3}, 'bgcolor': 'rgba(0,0,0,0)', 'borderwidth': 0,
                   'threshold': {'line': {'color': '#fff', 'width': 1.5}, 'thickness': 0.75, 'value': prev_val}}
        ))
        fig.update_layout(height=190, margin=dict(l=20, r=20, t=25, b=0),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    # ====================================================
    # NEW: TOP 3 CORE MACRO METERS (Fixed & Beautified)
    # ====================================================
    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;text-align:center;margin-bottom:6px;">CORE DRIVERS</p>'
        '<p style="font-size:24px;font-weight:800;color:#fff;text-align:center;margin-bottom:20px;">'
        'Live Market <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);'
        'background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'animation:shimmer 3.5s ease-in-out infinite;">Correlations</span></p>',
        unsafe_allow_html=True
    )

    def get_live_asset(symbol):
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                d = res.json()
                price = d['chart']['result'][0]['meta']['regularMarketPrice']
                prev = d['chart']['result'][0]['meta']['chartPreviousClose']
                return float(price), float(prev)
            return 0.0, 0.0
        except:
            return 0.0, 0.0

    dxy_price, dxy_prev = get_live_asset("DX-Y.NYB")
    xau_price, xau_prev = get_live_asset("XAUUSD=X")

    # Mock Data as fallback
    if dxy_price == 0.0: dxy_price, dxy_prev = 104.50, 104.20
    if xau_price == 0.0: xau_price, xau_prev = 2350.50, 2340.00

    us10_latest = fred_data.get('US 10Y', {}).get('latest', 4.26)
    us10_prev = fred_data.get('US 10Y', {}).get('previous', 4.22)
    t10_latest = fred_data.get('T10YIE', {}).get('latest', 2.30)
    t10_prev = fred_data.get('T10YIE', {}).get('previous', 2.28)

    ry_latest = round(us10_latest - t10_latest, 2)
    ry_prev = round(us10_prev - t10_prev, 2)

    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        st.markdown('<div style="text-align:center;"><span style="color:rgba(255,255,255,0.4);font-size:11px;font-weight:700;letter-spacing:1px;">DOLLAR INDEX (DXY)</span></div>', unsafe_allow_html=True)
        st.plotly_chart(build_gauge(dxy_price, dxy_prev, "#007AFF"), use_container_width=True, key="top_dxy")

    with tc2:
        st.markdown('<div style="text-align:center;"><span style="color:rgba(255,255,255,0.4);font-size:11px;font-weight:700;letter-spacing:1px;">REAL YIELD (US10Y - T10YIE)</span></div>', unsafe_allow_html=True)
        st.plotly_chart(build_gauge(ry_latest, ry_prev, "#BF5AF2"), use_container_width=True, key="top_ry")

    with tc3:
        st.markdown('<div style="text-align:center;"><span style="color:rgba(255,255,255,0.4);font-size:11px;font-weight:700;letter-spacing:1px;">GOLD (XAUUSD)</span></div>', unsafe_allow_html=True)
        st.plotly_chart(build_gauge(xau_price, xau_prev, "#d4af37"), use_container_width=True, key="top_xau")

    ry_dir = "Rising" if ry_latest > ry_prev else ("Falling" if ry_latest < ry_prev else "Flat")
    dxy_dir = "Rising" if dxy_price > dxy_prev else ("Falling" if dxy_price < dxy_prev else "Flat")

    # Detailed Expert Logic Processing
    if ry_dir == "Rising" and dxy_dir == "Rising":
        b_text = "BEARISH 🔴"
        b_col = "#FF453A"
        b_bg = "rgba(255,69,58,0.15)"
        b_glow = "rgba(255,69,58,0.4)"
        logic_desc = "DXY aur Real Yields dono breakout kar rahay hain. Institutional logic ke mutabiq, jab safe-haven bonds acha return dein (High Yield) aur Dollar strong ho, toh non-yielding asset (Gold) hold karne ki 'Opportunity Cost' barh jati hai. Is environment mein smart money Gold se paisa nikal kar bonds/dollar mein park karti hai.<br><br><span style='color:#FF453A; font-weight:700;'>Result: Heavy Selling Pressure expected on XAUUSD.</span>"
    elif ry_dir == "Falling" and dxy_dir == "Falling":
        b_text = "BULLISH 🟢"
        b_col = "#30D158"
        b_bg = "rgba(48,209,88,0.15)"
        b_glow = "rgba(48,209,88,0.4)"
        logic_desc = "DXY aur Real Yields dono crash ho rahay hain. Institutional logic ke mutabiq, jab bonds ka return gir raha ho aur Dollar weak ho jaye, toh inflation aur market risk se bachne ke liye smart money direct Gold (Safe Haven) mein pump hoti hai.<br><br><span style='color:#30D158; font-weight:700;'>Result: Strong Buying Pressure expected on XAUUSD.</span>"
    else:
        b_text = "MIXED / NEUTRAL 🟡"
        b_col = "#FF9F0A"
        b_bg = "rgba(255,159,10,0.15)"
        b_glow = "rgba(255,159,10,0.4)"
        logic_desc = f"DXY ({dxy_dir}) aur Real Yield ({ry_dir}) ka correlation is waqt mixed hai (divergence). Market direction decide nahi kar paa rahi. Aise macro environment mein Gold normally range-bound rehta hai ya pure technical levels ko respect karta hai.<br><br><span style='color:#FF9F0A; font-weight:700;'>Result: Wait for clear Macro trend or trade strictly level-to-level.</span>"

    # Ultra-Modern Expert Logic Decoder Card - FIXED HTML PARSING
    card_html = f"""
    <div style="background: linear-gradient(145deg, rgba(20,20,20,0.9), rgba(10,10,10,0.95)); border: 1px solid rgba(212,175,55,0.25); border-radius: 24px; padding: 25px 30px; margin-top: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05); position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: radial-gradient(circle, {b_glow} 0%, transparent 70%); filter: blur(30px); opacity: 0.5;"></div>
        <div style="display:flex; align-items:center; justify-content:space-between; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 15px; margin-bottom: 20px;">
            <div style="display:flex; align-items:center; gap:15px;">
                <div style="background: rgba(212,175,55,0.1); width:40px; height:40px; border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size:20px; border:1px solid rgba(212,175,55,0.2);">🧠</div>
                <div>
                    <h3 style="margin:0; color:#d4af37; font-size:16px; font-weight:800; letter-spacing:1px; text-transform:uppercase;">Macro Logic Decoder</h3>
                    <p style="margin:0; color:rgba(255,255,255,0.4); font-size:11px; letter-spacing:0.5px;">Institutional Correlation Analysis</p>
                </div>
            </div>
            <div>
                <span style="background:{b_bg}; color:{b_col}; padding:8px 18px; border-radius:20px; font-weight:800; font-size:12px; box-shadow: 0 0 15px {b_glow}; border: 1px solid {b_col}; letter-spacing:1px;">{b_text}</span>
            </div>
        </div>
        <div style="background: rgba(0,0,0,0.3); border-radius: 16px; padding: 20px; border-left: 4px solid {b_col};">
            <h4 style="margin:0 0 8px 0; color:#fff; font-size:13px; text-transform:uppercase; letter-spacing:1px;">Current Market Context</h4>
            <p style="margin:0; color:rgba(255,255,255,0.75); font-size:14px; line-height:1.7;">{logic_desc}</p>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    # ====================================================

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
            iv = row + i
            if iv < len(items):
                title, key, color, dxy, gold, nxt = items[iv]
                d = fred_data.get(key, {'latest': 0, 'previous': 0, 'change': 0})
                with col_obj:
                    chg_c = "#30D158" if d['change'] >= 0 else "#FF453A"
                    chg_bg = "rgba(48,209,88,0.08)" if d['change'] >= 0 else "rgba(255,69,58,0.08)"
                    chg_p = "+" if d['change'] >= 0 else ""
                    st.markdown(
                        '<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.05);'
                        'border-radius:20px;padding:16px;"><div style="display:flex;align-items:center;'
                        'justify-content:space-between;"><span style="font-size:10px;letter-spacing:1.5px;'
                        'text-transform:uppercase;color:rgba(255,255,255,0.35);font-weight:600;">' + title + '</span>'
                        '<span style="font-size:9px;padding:3px 8px;border-radius:12px;background:' + chg_bg
                        + ';color:' + chg_c + ';font-weight:600;">' + chg_p + str(abs(d['change'])) + '</span>'
                        '</div></div>', unsafe_allow_html=True
                    )
                    st.plotly_chart(build_gauge(d['latest'], d['previous'], color),
                                   use_container_width=True, key="g_" + key + str(iv))
                    st.markdown(
                        '<div style="display:flex;justify-content:center;gap:6px;margin-top:-10px;margin-bottom:10px;">'
                        '<span style="font-size:9px;padding:3px 10px;border-radius:14px;background:rgba(0,122,255,0.08);'
                        'color:#007AFF;font-weight:600;">DXY: ' + dxy + '</span>'
                        '<span style="font-size:9px;padding:3px 10px;border-radius:14px;background:rgba(212,175,55,0.08);'
                        'color:#d4af37;font-weight:600;">GOLD: ' + gold + '</span></div>'
                        '<p style="text-align:center;font-size:9px;color:rgba(255,255,255,0.15);">Next: ' + nxt + '</p>',
                        unsafe_allow_html=True
                    )

    # COT
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;color:rgba(212,175,55,0.5);'
        'font-weight:600;text-align:center;margin-bottom:6px;">SMART MONEY</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;text-align:center;margin-bottom:30px;">'
        'COT <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3.5s ease-in-out infinite;">'
        'Analysis</span></p>', unsafe_allow_html=True
    )
    cl, cr = st.columns([1, 1.5])
    with cl:
        fig_cot = go.Figure(data=[go.Pie(values=[75, 25], hole=.78, direction='clockwise', sort=False,
            marker=dict(colors=['#d4af37', 'rgba(255,255,255,0.02)'], line=dict(color='#000', width=2)),
            textinfo='none', hoverinfo='none')])
        fig_cot.update_layout(showlegend=False, margin=dict(t=15, b=15, l=15, r=15), height=280,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(text="75%", x=0.5, y=0.55, font_size=42, showarrow=False, font_color="#d4af37"),
                         dict(text="BULLISH", x=0.5, y=0.42, font_size=10, showarrow=False, font_color="rgba(255,255,255,0.25)")])
        st.plotly_chart(fig_cot, use_container_width=True, key="cot_d")
    with cr:
        st.markdown(
            '<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.05);'
            'border-radius:20px;padding:28px;margin-top:5px;">'
            '<p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);'
            'font-weight:700;margin-bottom:14px;">XAUUSD POSITIONING</p>'
            '<p style="color:rgba(255,255,255,0.4);font-size:13px;line-height:1.8;margin-bottom:18px;">'
            'Smart Money <strong style="color:#fff;">net long</strong>. Accumulating at institutional zones.</p>'
            '<div style="display:flex;justify-content:space-around;text-align:center;padding:16px 0;'
            'border-top:1px solid rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.03);">'
            '<div><p style="font-size:9px;color:rgba(255,255,255,0.25);text-transform:uppercase;margin-bottom:4px;">Longs</p>'
            '<p style="font-size:20px;font-weight:800;color:#30D158;">250K</p></div>'
            '<div><p style="font-size:9px;color:rgba(255,255,255,0.25);text-transform:uppercase;margin-bottom:4px;">Shorts</p>'
            '<p style="font-size:20px;font-weight:800;color:#FF453A;">50K</p></div>'
            '<div><p style="font-size:9px;color:rgba(255,255,255,0.25);text-transform:uppercase;margin-bottom:4px;">Net</p>'
            '<p style="font-size:20px;font-weight:800;color:#d4af37;">+200K</p></div></div>'
            '<div style="margin-top:12px;text-align:center;"><span style="font-size:9px;padding:4px 14px;border-radius:20px;'
            'background:rgba(48,209,88,0.08);color:#30d158;font-weight:700;">BIAS: BULLISH</span></div></div>',
            unsafe_allow_html=True
        )


# ============================================
# ADMIN PANEL
# ============================================
def admin_panel():
    st.markdown(
        '<div style="text-align:center;padding:20px 0 5px;">'
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:6px;">SYSTEM CONTROL</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;margin-bottom:25px;">'
        'Admin <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3.5s ease-in-out infinite;">'
        'Console</span></p></div>',
        unsafe_allow_html=True
    )

    uploadable_tools = ["money_flow", "oi_analyzer", "gold_report", "forex_report",
                        "btc_report", "sp500_report", "learning"]

    tab_list = ["📄 Content Manager", "👥 Users", "✏️ Hero Banner", "📰 News Manager"]
    tabs = st.tabs(tab_list)

    # TAB 1: CONTENT MANAGER
    with tabs[0]:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Upload Content for Toolkit Sections")
        st.info("Select a section and upload its HTML file. It will appear when users click that box on the home page.")

        selected_tool = st.selectbox(
            "Select Section",
            uploadable_tools,
            format_func=lambda x: tool_meta[x]["icon"] + " " + tool_meta[x]["name"],
            key="sel_tool"
        )

        uploaded = st.file_uploader("Upload HTML", type=['html'], key="tool_upload")

        if st.button("PUBLISH CONTENT", use_container_width=True, key="pub_tool"):
            if uploaded:
                html_str = uploaded.getvalue().decode("utf-8")
                st.session_state["content_" + selected_tool] = html_str
                st.success("Published: " + tool_meta[selected_tool]["name"])
            else:
                st.error("Select an HTML file.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Current Content Status")

        for tk in uploadable_tools:
            meta = tool_meta[tk]
            has = bool(st.session_state.get("content_" + tk, ""))
            status = "ACTIVE" if has else "EMPTY"
            s_color = "#30d158" if has else "rgba(255,255,255,0.2)"

            c1, c2, c3 = st.columns([4, 1, 1])
            with c1:
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                    'border-radius:12px;padding:12px 18px;margin-bottom:6px;">'
                    '<span style="font-size:16px;">' + meta["icon"] + '</span> '
                    '<span style="color:#fff;font-size:13px;font-weight:600;">' + meta["name"] + '</span> '
                    '<span style="font-size:9px;padding:2px 8px;border-radius:10px;margin-left:8px;'
                    'color:' + s_color + ';font-weight:600;">' + status + '</span></div>',
                    unsafe_allow_html=True
                )
            with c2:
                if has:
                    if st.button("View", key="vt_" + tk):
                        st.session_state['current_page'] = 'tool_' + tk
                        st.rerun()
            with c3:
                if has:
                    if st.button("Clear", key="ct_" + tk):
                        st.session_state["content_" + tk] = ""
                        st.success("Cleared: " + meta["name"])
                        st.rerun()

    # TAB 2: USERS
    with tabs[1]:
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
                    st.error("Exists!")
                else:
                    nr = pd.DataFrame({"Username": [new_user], "Password": [new_pass],
                                       "Role": [new_role], "Status": [new_status],
                                       "Created": [datetime.now().strftime("%Y-%m-%d")]})
                    st.session_state['users_db'] = pd.concat([st.session_state['users_db'], nr], ignore_index=True)
                    st.success("Created: " + new_user)
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Modify User")
        all_u = st.session_state['users_db']['Username'].tolist()
        m1, m2 = st.columns(2)
        with m1:
            sel_u = st.selectbox("User", all_u, key="mu")
        with m2:
            act = st.selectbox("Action", ["Activate", "Suspend", "Make Admin", "Make User", "Reset Password", "Delete"], key="ma")
        new_pw = ""
        if act == "Reset Password":
            new_pw = st.text_input("New Password", type="password", key="rpw")
        if st.button("APPLY", use_container_width=True, key="apl"):
            db = st.session_state['users_db']
            idx = db[db['Username'] == sel_u].index
            if len(idx) > 0:
                i = idx[0]
                if act == "Activate":
                    db.at[i, 'Status'] = 'Active'; st.rerun()
                elif act == "Suspend":
                    if sel_u != "admin": db.at[i, 'Status'] = 'Suspended'; st.rerun()
                    else: st.error("Cannot suspend admin!")
                elif act == "Make Admin":
                    db.at[i, 'Role'] = 'Admin'; st.rerun()
                elif act == "Make User":
                    if sel_u != "admin": db.at[i, 'Role'] = 'User'; st.rerun()
                    else: st.error("Cannot change admin!")
                elif act == "Reset Password":
                    if new_pw: db.at[i, 'Password'] = new_pw; st.rerun()
                    else: st.error("Enter password")
                elif act == "Delete":
                    if sel_u != "admin":
                        st.session_state['users_db'] = db.drop(i).reset_index(drop=True); st.rerun()
                    else: st.error("Cannot delete admin!")

    # TAB 3: HERO BANNER
    with tabs[2]:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        new_q = st.text_area("Hero Quote", value=st.session_state['hero_quote'], height=100, key="hqi")
        new_s = st.text_input("Subtitle", value=st.session_state['hero_subtitle'], key="hsi")
        if st.button("UPDATE BANNER", use_container_width=True, key="ub"):
            st.session_state['hero_quote'] = new_q
            st.session_state['hero_subtitle'] = new_s
            st.success("Updated!")
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

    # TAB 4: NEWS
    with tabs[3]:
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Add Article")
        n1, n2 = st.columns(2)
        with n1:
            nt = st.text_input("Title", key="nt", placeholder="Article title")
        with n2:
            ntg = st.selectbox("Category", ["GOLD", "MACRO", "CRYPTO", "FOREX"], key="ntg")
        nd = st.text_area("Description", key="nd", placeholder="Summary...", height=100)
        if st.button("ADD ARTICLE", use_container_width=True, key="an"):
            if nt and nd:
                st.session_state['news_articles'].insert(0, {
                    "title": nt, "desc": nd,
                    "date": datetime.now().strftime("%Y-%m-%d"), "tag": ntg
                })
                st.success("Added!")
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Current Articles")
        for i, art in enumerate(st.session_state['news_articles']):
            ac1, ac2 = st.columns([5, 1])
            with ac1:
                st.markdown(
                    '<span style="font-size:9px;padding:3px 8px;border-radius:10px;'
                    'background:rgba(212,175,55,0.08);color:#d4af37;font-weight:700;">'
                    + art["tag"] + '</span> '
                    '<span style="color:#fff;font-size:13px;font-weight:600;margin-left:8px;">'
                    + art["title"] + '</span>',
                    unsafe_allow_html=True
                )
            with ac2:
                if st.button("Del", key="dn_" + str(i)):
                    st.session_state['news_articles'].pop(i)
                    st.rerun()


# ============================================
# REPORTS PAGE (legacy - redirects to gold_report)
# ============================================
def reports_page():
    st.markdown(
        '<div style="text-align:center;padding:20px 0 5px;">'
        '<div style="margin-bottom:12px;">'
        '<img src="' + LOGO_URL + '" width="55" height="55" '
        'style="border-radius:50%;object-fit:cover;border:2.5px solid #d4af37;">'
        '</div>'
        '<p style="font-size:10px;letter-spacing:4px;text-transform:uppercase;'
        'color:rgba(212,175,55,0.5);font-weight:600;margin-bottom:6px;">EXPERT ANALYSIS</p>'
        '<p style="font-size:30px;font-weight:800;color:#fff;margin-bottom:6px;">'
        'Daily <span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3.5s ease-in-out infinite;">'
        'Market Report</span></p></div>',
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
        st.info("No reports yet.")


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
    elif page.startswith('tool_'):
        tool_page(page)
    else:
        home_page()
    render_footer()

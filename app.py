import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components

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
# 3. APPLE-STYLE CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-primary: #000000;
        --bg-card: rgba(255,255,255,0.03);
        --bg-card-hover: rgba(255,255,255,0.06);
        --glass: rgba(18,18,20,0.78);
        --glass-border: rgba(255,255,255,0.08);
        --glass-border-hover: rgba(255,255,255,0.14);
        --gold: #d4af37;
        --gold-light: #f5d769;
        --gold-dim: rgba(212,175,55,0.5);
        --gold-glow: rgba(212,175,55,0.12);
        --text-primary: #f5f5f7;
        --text-secondary: rgba(255,255,255,0.55);
        --text-tertiary: rgba(255,255,255,0.3);
        --text-quaternary: rgba(255,255,255,0.18);
        --green: #30d158;
        --red: #ff453a;
        --blue: #0a84ff;
        --orange: #ff9f0a;
        --purple: #bf5af2;
        --radius-sm: 12px;
        --radius-md: 16px;
        --radius-lg: 22px;
        --radius-xl: 28px;
        --radius-2xl: 36px;
        --transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary);
    }
    #MainMenu, footer, header { visibility: hidden; }
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    .stDeployButton { display: none; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }

    div.stButton > button {
        background: var(--bg-card) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 980px !important;
        padding: 10px 24px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.3px !important;
        transition: var(--transition) !important;
    }
    div.stButton > button:hover {
        background: var(--gold-glow) !important;
        color: var(--gold) !important;
        border-color: rgba(212,175,55,0.3) !important;
        box-shadow: 0 4px 20px rgba(212,175,55,0.1) !important;
    }

    div[data-testid="stTextInput"] input {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: #fff !important;
        font-size: 15px !important;
        padding: 14px 18px !important;
        transition: var(--transition) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 4px rgba(212,175,55,0.06) !important;
    }
    div[data-testid="stTextInput"] label {
        color: var(--text-tertiary) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    div[data-testid="stTextArea"] textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: #fff !important;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--gold) !important;
    }
    div[data-testid="stTextArea"] label {
        color: var(--text-tertiary) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
    }
    div[data-testid="stSelectbox"] label {
        color: var(--text-tertiary) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    div[data-testid="stTabs"] button {
        color: var(--text-tertiary) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        background: transparent !important;
        transition: var(--transition) !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--gold) !important;
        border-bottom-color: var(--gold) !important;
    }

    div[data-testid="stFileUploader"] {
        background: var(--bg-card) !important;
        border: 2px dashed rgba(212,175,55,0.12) !important;
        border-radius: var(--radius-lg) !important;
    }

    div[data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 20px;
    }
    div[data-testid="stMetric"] label {
        color: var(--text-tertiary) !important;
        font-size: 11px !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--gold) !important;
        font-weight: 700 !important;
    }

    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent) !important;
        margin: 45px 0 !important;
    }
    h1 a, h2 a, h3 a { display: none !important; }

    @keyframes shimmer {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 200% center; }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(48,209,88,0.4); }
        50% { box-shadow: 0 0 0 6px rgba(48,209,88,0); }
    }
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(25px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    @keyframes glow-breathe {
        0%, 100% { box-shadow: 0 0 30px rgba(212,175,55,0.06); }
        50% { box-shadow: 0 0 60px rgba(212,175,55,0.12); }
    }

    .section-eyebrow {
        font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
        color: var(--gold-dim); font-weight: 600; text-align: center; margin-bottom: 8px;
    }
    .section-title {
        font-size: 40px; font-weight: 800; color: var(--text-primary);
        text-align: center; margin-bottom: 8px; letter-spacing: -0.5px; line-height: 1.15;
    }
    .section-title .gold-text {
        background: linear-gradient(135deg, #d4af37, #f5d769, #d4af37);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmer 4s ease-in-out infinite;
    }
    .section-subtitle {
        font-size: 15px; color: var(--text-tertiary); text-align: center;
        margin-bottom: 40px; font-weight: 400;
    }
    .live-dot {
        width: 6px; height: 6px; background: var(--green);
        border-radius: 50%; display: inline-block; animation: pulse-glow 2s infinite;
    }
    .tag-pill {
        font-size: 9px; padding: 4px 12px; border-radius: 980px;
        font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. DEFAULT HTMLS
# ============================================
DEFAULT_REPORT_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:'Inter',-apple-system,sans-serif;background:#000;color:#fff;}
.mc{max-width:1000px;margin:0 auto;padding:30px 20px;}
.hero{text-align:center;padding:60px 20px;}
.ht{font-size:44px;font-weight:800;color:#d4af37;margin-bottom:10px;}
.sec{margin-bottom:30px;padding:30px;background:rgba(255,255,255,0.03);border-radius:24px;border:1px solid rgba(255,255,255,0.06);}
.sh{font-size:12px;font-weight:700;color:#d4af37;letter-spacing:2px;text-transform:uppercase;margin-bottom:25px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.04);}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:15px;}
.sc{background:rgba(255,255,255,0.02);padding:20px;border-radius:16px;border:1px solid rgba(255,255,255,0.04);text-align:center;}
.sl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}
.sv{font-size:28px;font-weight:800;color:#d4af37;}
.lb{background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);padding:20px;border-radius:16px;margin-top:20px;font-size:14px;line-height:1.7;color:rgba(255,255,255,0.7);}
.bl{text-align:center;padding:40px;background:rgba(212,175,55,0.03);border-radius:24px;border:1px solid rgba(212,175,55,0.15);}
.bl h3{font-size:28px;font-weight:800;color:#d4af37;margin-bottom:10px;}
.bl p{color:rgba(255,255,255,0.5);}</style></head><body><div class="mc"><section class="hero"><h1 class="ht">Gold Analysis</h1><p style="color:rgba(255,255,255,0.4);">Smart Money Positioning</p></section><section class="sec"><div class="sh">Futures Data</div><div class="sg"><div class="sc"><div class="sl">Price</div><div class="sv" style="color:#FF453A">5,086</div></div><div class="sc"><div class="sl">Volume</div><div class="sv">129,968</div></div><div class="sc"><div class="sl">OI</div><div class="sv" style="color:#FF453A">+1,199</div></div><div class="sc"><div class="sl">Blocks</div><div class="sv">475</div></div></div><div class="lb"><strong>Logic:</strong> Price DOWN + OI UP = SHORT BUILDUP</div></section><section class="bl"><h3>VERDICT: BEARISH</h3><p>Short rallies into 5280 targeting 5020</p></section></div></body></html>"""

CALCULATOR_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{margin:0;padding:0;box-sizing:border-box;}body{background:transparent;display:flex;justify-content:center;padding:30px;font-family:'Inter',sans-serif;}.c{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:28px;padding:40px;width:100%;max-width:480px;}.ce{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.6);font-weight:600;text-align:center;margin-bottom:8px;}.ct{font-size:28px;font-weight:800;text-align:center;color:#d4af37;margin-bottom:35px;}.ig{margin-bottom:22px;}.ig label{display:block;margin-bottom:8px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.35);}.ig input{width:100%;padding:16px 20px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;color:#fff;font-size:16px;outline:none;transition:all 0.3s;font-family:'Inter',sans-serif;}.ig input:focus{border-color:rgba(212,175,55,0.5);}.cb{width:100%;padding:18px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#000;border:none;border-radius:980px;font-size:15px;font-weight:700;cursor:pointer;margin-top:15px;font-family:'Inter',sans-serif;}.cb:hover{transform:scale(1.02);}#result{margin-top:30px;text-align:center;display:none;padding:30px;border-radius:20px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);}.rv{font-size:48px;font-weight:800;color:#d4af37;}.rr{font-size:13px;color:rgba(255,255,255,0.3);margin-top:8px;}</style></head><body><div class="c"><p class="ce">Risk Management</p><h1 class="ct">Position Sizer</h1><div class="ig"><label>Account Balance</label><input type="number" id="a" placeholder="10000"></div><div class="ig"><label>Risk (%)</label><input type="number" id="r" placeholder="2.0"></div><div class="ig"><label>Stop Loss (Pips)</label><input type="number" id="s" placeholder="50"></div><button class="cb" onclick="calc()">Calculate Position</button><div id="result"><p style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Lot Size</p><p class="rv" id="lv"></p><p class="rr" id="ra"></p></div></div><script>function calc(){var a=parseFloat(document.getElementById('a').value);var r=parseFloat(document.getElementById('r').value);var s=parseFloat(document.getElementById('s').value);if(!a||!r||!s)return;var ra=(a*r/100);var l=(ra/(s*10)).toFixed(2);document.getElementById('lv').textContent=l+' Lot';document.getElementById('ra').textContent='Risk: $'+ra.toFixed(2);document.getElementById('result').style.display='block';}</script></body></html>"""

# ============================================
# 5. SESSION STATE
# ============================================
defaults = {
    'logged_in': False, 'user_role': None, 'username': None,
    'current_page': 'home',
    'hero_quote': "The trend is your friend until it bends at the end.",
    'hero_subtitle': "Smart Money Intelligence Platform",
    'macro_popup': None,
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
    "macro_terminal": {"name": "Macro Terminal", "icon": "📊", "color": "#0a84ff", "tag": "LIVE DATA", "desc": "Economic indicators, COT analysis and Fed tracking"},
    "money_flow": {"name": "Money Flow", "icon": "💰", "color": "#30d158", "tag": "FLOW", "desc": "Track institutional money flow and liquidity zones"},
    "oi_analyzer": {"name": "OI Analyzer", "icon": "📈", "color": "#ff9f0a", "tag": "ANALYSIS", "desc": "Open Interest analysis with smart money positioning"},
    "gold_report": {"name": "Gold Intel", "icon": "🪙", "color": "#d4af37", "tag": "XAUUSD", "desc": "Institutional gold analysis with trade scenarios"},
    "forex_report": {"name": "Forex Intel", "icon": "💶", "color": "#bf5af2", "tag": "FOREX", "desc": "Major pairs analysis with liquidity maps"},
    "btc_report": {"name": "BTC Intel", "icon": "₿", "color": "#ff9f0a", "tag": "CRYPTO", "desc": "Bitcoin institutional analysis and key levels"},
    "sp500_report": {"name": "S&P 500 Intel", "icon": "📉", "color": "#ff453a", "tag": "INDEX", "desc": "S&P 500 smart money decode and scenarios"},
    "market_news": {"name": "Market News", "icon": "📰", "color": "#0a84ff", "tag": "NEWS", "desc": "Curated market insights and breaking news"},
    "calculator": {"name": "Risk Calculator", "icon": "🧮", "color": "#bf5af2", "tag": "TOOL", "desc": "Precision position sizing for every setup"},
    "learning": {"name": "Academy", "icon": "🎓", "color": "#30d158", "tag": "LEARN", "desc": "Trading education and strategy courses"},
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
# MACRO INTELLIGENCE DATABASE
# ============================================
def get_macro_intelligence():
    """
    Returns complete intelligence for each macro indicator.
    Contains: what it is, what current reading means,
    hardcore logic for DXY and Gold impact,
    and institutional interpretation.
    """
    return {
        "CPI": {
            "full_name": "Consumer Price Index (CPI)",
            "what_is_it": (
                "CPI measures the average change in prices paid by consumers for a basket of goods and services "
                "including food, housing, transportation, medical care, clothing, and recreation. "
                "It is the most widely followed inflation gauge published monthly by the Bureau of Labor Statistics (BLS). "
                "Core CPI excludes volatile food and energy prices. The Fed's 2% target is based on PCE, "
                "but CPI moves markets more because it releases first."
            ),
            "icon": "🔥",
            "color": "#ff453a",
        },
        "Fed Rate": {
            "full_name": "Federal Funds Rate",
            "what_is_it": (
                "The Federal Funds Rate is the interest rate at which banks lend reserve balances to other banks overnight. "
                "It is set by the Federal Open Market Committee (FOMC) and is the most powerful monetary policy tool. "
                "When the Fed raises rates, borrowing becomes expensive across the entire economy — mortgages, "
                "car loans, business credit all go up. When they cut, it stimulates spending and investment. "
                "This rate controls the entire yield curve and affects every asset class globally."
            ),
            "icon": "🏛️",
            "color": "#0a84ff",
        },
        "US 10Y": {
            "full_name": "US 10-Year Treasury Yield",
            "what_is_it": (
                "The 10-Year Treasury Yield is the return investors get for lending money to the US government for 10 years. "
                "It is considered the benchmark 'risk-free' rate and is the most important yield in global finance. "
                "It directly affects mortgage rates (30-year mortgages track the 10Y closely), corporate borrowing costs, "
                "and equity valuations. When the 10Y rises, it means bond prices are falling — investors are demanding "
                "more compensation for holding government debt, often due to inflation fears or heavy Treasury issuance."
            ),
            "icon": "📊",
            "color": "#d4af37",
        },
        "Unemployment": {
            "full_name": "Unemployment Rate (U-3)",
            "what_is_it": (
                "The Unemployment Rate measures the percentage of the total labor force that is jobless and actively seeking work. "
                "Published monthly by BLS as part of the Non-Farm Payrolls report. "
                "U-3 is the headline number, but U-6 (which includes discouraged workers and part-timers wanting full-time) "
                "gives a fuller picture. The Fed considers 'full employment' around 3.5-4.0%. "
                "This is a LAGGING indicator — by the time unemployment rises sharply, recession has already started."
            ),
            "icon": "👷",
            "color": "#ff9f0a",
        },
        "GDP Growth": {
            "full_name": "Real GDP Growth Rate (Quarter over Quarter, Annualized)",
            "what_is_it": (
                "GDP (Gross Domestic Product) measures the total value of all goods and services produced in the US. "
                "The growth rate shows how fast the economy is expanding or contracting. "
                "It is reported quarterly with 3 releases: Advance (first estimate, moves markets most), "
                "Second Estimate, and Final. A negative GDP for 2 consecutive quarters is the technical definition "
                "of recession. Components: Consumer Spending (68%), Business Investment, Government Spending, Net Exports."
            ),
            "icon": "📈",
            "color": "#30d158",
        },
        "PCE": {
            "full_name": "Personal Consumption Expenditures Price Index",
            "what_is_it": (
                "PCE is the Federal Reserve's PREFERRED inflation measure (not CPI). "
                "It measures price changes in consumer goods and services but has a broader scope than CPI "
                "and accounts for substitution effects (when consumers switch to cheaper alternatives). "
                "Core PCE (excluding food and energy) is what the Fed officially targets at 2%. "
                "If Core PCE is above 2%, the Fed is more likely to keep rates high or hike. "
                "Below 2% opens the door for rate cuts. This is the single most important number for Fed policy."
            ),
            "icon": "🎯",
            "color": "#bf5af2",
        },
    }


def generate_indicator_analysis(key, data):
    """
    Generate real-time analysis based on actual data values.
    Uses hardcore institutional logic — not generic text.
    """
    latest = data['latest']
    previous = data['previous']
    change = data['change']
    direction = "UP" if change > 0 else "DOWN" if change < 0 else "FLAT"

    analyses = {}

    # ============ CPI LOGIC ============
    if key == "CPI":
        if latest > previous:
            current_reading = (
                f"CPI has INCREASED from {previous} to {latest} (+{abs(change)}). "
                f"This means inflation is ACCELERATING. Consumer prices are rising faster than the previous period. "
                f"The cost of living is going up — groceries, rent, gas, healthcare are all getting more expensive. "
                f"This is a HAWKISH signal for the Federal Reserve."
            )
            dxy_impact = (
                f"🟢 DXY BULLISH — Rising CPI means the Fed will keep interest rates HIGH for LONGER "
                f"or potentially HIKE again. Higher rates attract foreign capital into US dollar-denominated assets "
                f"(especially Treasury bonds), increasing demand for USD. "
                f"Institutional flow: Money moves FROM low-yield currencies (JPY, EUR) INTO USD. "
                f"DXY typically rallies 0.3-0.8% on a hot CPI print within 24 hours."
            )
            gold_impact = (
                f"🔴 GOLD BEARISH (Short-term) — Higher CPI = higher rates expectation = higher real yields = "
                f"Gold becomes less attractive because it pays no interest. When you can earn 5.5% risk-free in T-Bills, "
                f"holding gold (0% yield) has an opportunity cost. "
                f"HOWEVER — if CPI stays persistently high and the Fed loses credibility, "
                f"gold becomes a LONG-TERM inflation hedge. Smart money buys gold dips on hot CPI prints. "
                f"Key level to watch: If real yields (10Y - CPI) go negative, gold explodes higher."
            )
            verdict = "HAWKISH"
            verdict_color = "#ff453a"
        elif latest < previous:
            current_reading = (
                f"CPI has DECREASED from {previous} to {latest} ({change}). "
                f"Inflation is COOLING. Consumer prices are rising at a slower pace. "
                f"This is what the Fed wants to see — their rate hikes are working. "
                f"If this trend continues, the Fed will start cutting rates in upcoming meetings."
            )
            dxy_impact = (
                f"🔴 DXY BEARISH — Falling CPI reduces the need for the Fed to keep rates elevated. "
                f"Rate cut expectations increase, making USD less attractive for carry trades. "
                f"Foreign investors start moving capital to higher-yielding emerging markets. "
                f"DXY typically drops 0.3-0.6% on a cool CPI print. Watch for break below key support levels."
            )
            gold_impact = (
                f"🟢 GOLD BULLISH — Lower CPI = Fed closer to rate cuts = falling real yields = "
                f"Gold's opportunity cost decreases. When rates come down, gold becomes relatively more attractive. "
                f"Historically, gold rallies 15-25% in the 12 months following the Fed's first rate cut. "
                f"Institutional positioning: Central banks are already accumulating at record pace. "
                f"A cooling CPI accelerates this trend."
            )
            verdict = "DOVISH"
            verdict_color = "#30d158"
        else:
            current_reading = (
                f"CPI is UNCHANGED at {latest}. Inflation is stable — neither accelerating nor decelerating. "
                f"The market will look at Core CPI and sub-components for direction. "
                f"Shelter inflation and services inflation are the sticky components to watch."
            )
            dxy_impact = "⚪ DXY NEUTRAL — No change means no new information for the Fed. Markets will remain range-bound until next data point."
            gold_impact = "⚪ GOLD NEUTRAL — Flat CPI keeps current positioning intact. Watch Core PCE for clearer direction."
            verdict = "NEUTRAL"
            verdict_color = "#ff9f0a"

    # ============ FED RATE LOGIC ============
    elif key == "Fed Rate":
        if latest > previous:
            current_reading = (
                f"The Fed has HIKED rates from {previous}% to {latest}%. "
                f"This is a direct tightening of monetary policy. Every loan in America just got more expensive. "
                f"The Fed is telling the market: 'Inflation is still too high, we're not done.' "
                f"This is the most powerful tool the Fed has — it ripples through the entire global financial system."
            )
            dxy_impact = (
                f"🟢 DXY STRONGLY BULLISH — Rate hikes are the #1 driver of USD strength. "
                f"Higher US rates mean higher returns on US assets, attracting massive capital inflows. "
                f"The interest rate differential widens vs EUR, JPY, GBP — making carry trades into USD very profitable. "
                f"DXY can rally 1-3% in the weeks following a surprise hike. "
                f"Watch USD/JPY especially — Japan's near-zero rates make the differential extreme."
            )
            gold_impact = (
                f"🔴 GOLD BEARISH — Rate hikes directly increase the opportunity cost of holding gold. "
                f"Real yields surge, making Treasury bonds more attractive than zero-yield gold. "
                f"Short-term: Gold typically drops $30-80 on a rate hike. "
                f"BUT — if the hike is seen as a 'policy mistake' that will cause recession, "
                f"gold reverses sharply higher as recession hedge. Watch the yield curve inversion depth."
            )
            verdict = "HAWKISH"
            verdict_color = "#ff453a"
        elif latest < previous:
            current_reading = (
                f"The Fed has CUT rates from {previous}% to {latest}%. "
                f"This is monetary EASING — the Fed is stimulating the economy. "
                f"Borrowing just got cheaper. The Fed is signaling that inflation is under control "
                f"and/or the economy needs support. This is a MAJOR shift in policy stance."
            )
            dxy_impact = (
                f"🔴 DXY BEARISH — Rate cuts reduce the yield advantage of holding USD. "
                f"Capital flows OUT of USD into higher-yielding currencies and risk assets. "
                f"The dollar index can fall 3-8% during a full cutting cycle. "
                f"Watch EUR/USD and GBP/USD for breakouts above key resistance levels."
            )
            gold_impact = (
                f"🟢 GOLD STRONGLY BULLISH — Rate cuts are ROCKET FUEL for gold. "
                f"Lower rates = lower real yields = lower opportunity cost of holding gold. "
                f"In every rate cutting cycle since 1970, gold has averaged +18% returns in the following 12 months. "
                f"Central bank gold buying + retail ETF inflows + lower rates = perfect storm for gold. "
                f"Target: Gold typically makes new all-time highs within 6-12 months of first cut."
            )
            verdict = "DOVISH"
            verdict_color = "#30d158"
        else:
            current_reading = (
                f"The Fed has HELD rates steady at {latest}%. "
                f"This is a 'wait and see' approach — the Fed is data-dependent. "
                f"The market will focus on the Fed's statement, dot plot, and Powell's press conference "
                f"for clues about future direction. A hawkish hold vs dovish hold makes all the difference."
            )
            dxy_impact = (
                f"⚪ DXY DEPENDS ON TONE — If the Fed signals 'higher for longer' (hawkish hold), DXY rallies. "
                f"If the Fed hints at upcoming cuts (dovish hold), DXY sells off. "
                f"Watch the dot plot median and the statement language changes word-by-word."
            )
            gold_impact = (
                f"⚪ GOLD DEPENDS ON FORWARD GUIDANCE — A pause with hawkish language = gold dips. "
                f"A pause with dovish pivot language = gold rallies hard. "
                f"Key phrase to watch: 'The Committee judges that the risks are becoming more balanced' = DOVISH = GOLD UP."
            )
            verdict = "DATA DEPENDENT"
            verdict_color = "#ff9f0a"

    # ============ US 10Y LOGIC ============
    elif key == "US 10Y":
        if latest > previous:
            current_reading = (
                f"The 10-Year yield has RISEN from {previous}% to {latest}% (+{abs(change)}bps). "
                f"Bond prices are FALLING (yields and prices move inversely). "
                f"This means: (1) Markets expect higher inflation ahead, or (2) Heavy Treasury supply is hitting the market, "
                f"or (3) Foreign buyers (China, Japan) are reducing their Treasury holdings. "
                f"30-year mortgage rates are climbing, which will slow the housing market."
            )
            dxy_impact = (
                f"🟢 DXY BULLISH — Higher 10Y yield attracts foreign capital seeking better returns. "
                f"The US offers the highest yields among developed nations — Japanese investors earn 4%+ more "
                f"in US bonds vs JGBs. This flow dynamic supports the dollar. "
                f"Watch the real yield (10Y minus inflation expectations) — if real yield is rising, DXY strengthens further."
            )
            gold_impact = (
                f"🔴 GOLD BEARISH — Rising 10Y yields are gold's BIGGEST enemy. "
                f"The real yield (10Y yield minus expected inflation) is gold's mirror image. "
                f"When real yields rise, gold falls. When real yields are above 2%, gold faces serious headwinds. "
                f"Current real yield: approximately {round(latest - 3.0, 2)}% (10Y {latest}% minus ~3.0% inflation expectations). "
                f"If real yield goes above 2.5%, expect gold to test lower support zones."
            )
            verdict = "YIELDS RISING"
            verdict_color = "#ff453a"
        elif latest < previous:
            current_reading = (
                f"The 10-Year yield has FALLEN from {previous}% to {latest}% ({change}bps). "
                f"Bond prices are RISING — investors are buying Treasuries (flight to safety). "
                f"This signals: (1) Economic slowdown fears, (2) Deflation expectations, "
                f"or (3) Global risk-off event pushing capital into safe-haven bonds."
            )
            dxy_impact = (
                f"🟡 DXY MIXED — Falling yields reduce USD's yield advantage (bearish for DXY), "
                f"BUT if yields are falling because of recession fears, the dollar can still rally "
                f"as a safe haven currency. Context matters enormously. "
                f"If yields fall WITH stock market crash = DXY UP (safe haven). "
                f"If yields fall WITH stable stocks = DXY DOWN (rate cut expectations)."
            )
            gold_impact = (
                f"🟢 GOLD BULLISH — Falling yields reduce gold's opportunity cost. "
                f"If the 10Y drops below inflation expectations, real yields go NEGATIVE — "
                f"this is the most bullish scenario for gold possible. Negative real yields mean "
                f"you LOSE purchasing power holding bonds, making gold superior. "
                f"Every major gold rally in history has coincided with negative or declining real yields."
            )
            verdict = "YIELDS FALLING"
            verdict_color = "#30d158"
        else:
            current_reading = f"10-Year yield unchanged at {latest}%. Market is in equilibrium. Watch for breakout direction."
            dxy_impact = "⚪ DXY NEUTRAL — No yield change, no directional signal."
            gold_impact = "⚪ GOLD NEUTRAL — Waiting for yield direction to set positioning."
            verdict = "NEUTRAL"
            verdict_color = "#ff9f0a"

    # ============ UNEMPLOYMENT LOGIC ============
    elif key == "Unemployment":
        if latest > previous:
            current_reading = (
                f"Unemployment has RISEN from {previous}% to {latest}%. "
                f"The labor market is WEAKENING. More Americans are losing jobs. "
                f"This is a LAGGING indicator — by the time unemployment rises significantly, "
                f"the economy is likely already in or entering recession. "
                f"The Sahm Rule: If the 3-month average unemployment rate rises 0.5% above its 12-month low, "
                f"recession has started 100% of the time historically."
            )
            dxy_impact = (
                f"🔴 DXY BEARISH — Rising unemployment = weaker economy = Fed will cut rates sooner. "
                f"Rate cut expectations surge, reducing USD's yield advantage. "
                f"However, if unemployment spikes suddenly (crisis), DXY can rally on safe-haven flows initially "
                f"before falling on rate cut expectations."
            )
            gold_impact = (
                f"🟢 GOLD STRONGLY BULLISH — Rising unemployment triggers TWO bullish catalysts for gold: "
                f"(1) Fed rate cuts become imminent = lower real yields = gold up. "
                f"(2) Recession fears increase = safe haven demand for gold surges. "
                f"During the 2008 crisis, gold rallied from $700 to $1,900 as unemployment peaked. "
                f"Institutional smart money AGGRESSIVELY buys gold when unemployment trends higher."
            )
            verdict = "LABOR WEAKENING"
            verdict_color = "#ff453a"
        elif latest < previous:
            current_reading = (
                f"Unemployment has FALLEN from {previous}% to {latest}%. "
                f"The labor market is STRONG. More Americans are employed. "
                f"Strong employment = strong consumer spending = strong economy. "
                f"This gives the Fed room to keep rates higher for longer to fight inflation."
            )
            dxy_impact = (
                f"🟢 DXY BULLISH — Low unemployment = strong economy = Fed can stay hawkish = higher rates. "
                f"Strong labor market supports consumer spending, which is 68% of GDP. "
                f"This keeps the US economy outperforming other developed nations, attracting capital flows."
            )
            gold_impact = (
                f"🔴 GOLD BEARISH — Low unemployment removes the recession argument for gold. "
                f"The Fed has no pressure to cut rates. 'Higher for longer' rates environment "
                f"keeps real yields elevated, which is negative for gold. "
                f"Gold bugs need either rising unemployment OR falling inflation to trigger Fed cuts."
            )
            verdict = "LABOR STRONG"
            verdict_color = "#30d158"
        else:
            current_reading = f"Unemployment unchanged at {latest}%. Labor market is stable."
            dxy_impact = "⚪ DXY NEUTRAL — Stable employment, no new pressure on Fed policy."
            gold_impact = "⚪ GOLD NEUTRAL — No change in recession probability from labor data."
            verdict = "STABLE"
            verdict_color = "#ff9f0a"

    # ============ GDP GROWTH LOGIC ============
    elif key == "GDP Growth":
        if latest > previous:
            current_reading = (
                f"GDP Growth has ACCELERATED from {previous}% to {latest}%. "
                f"The US economy is EXPANDING faster. This is a strong sign — consumer spending, "
                f"business investment, and/or government spending are driving growth. "
                f"If GDP is above 3%, the economy is running HOT. "
                f"If above 2% but below 3%, it's healthy 'Goldilocks' growth."
            )
            dxy_impact = (
                f"🟢 DXY BULLISH — Stronger GDP = stronger economy = capital inflows into US. "
                f"The US economic exceptionalism narrative attracts global investment. "
                f"Higher GDP also means the Fed can maintain restrictive policy, keeping yields elevated. "
                f"DXY tends to follow relative GDP differentials — US outperforming Europe and Japan = DXY up."
            )
            gold_impact = (
                f"🔴 GOLD BEARISH — Strong GDP means no recession fear, no urgency for rate cuts. "
                f"Risk-on environment pushes capital into equities instead of gold. "
                f"S&P 500 and gold are inversely correlated during strong growth periods. "
                f"Exception: If GDP is strong BUT inflation is re-accelerating, gold can rally as inflation hedge."
            )
            verdict = "GROWTH ACCELERATING"
            verdict_color = "#30d158"
        elif latest < previous:
            current_reading = (
                f"GDP Growth has DECELERATED from {previous}% to {latest}%. "
                f"The economy is SLOWING. If this trend continues toward 0% or negative, "
                f"recession risk rises sharply. Watch the Atlanta Fed GDPNow for real-time tracking. "
                f"Two consecutive quarters of negative GDP = technical recession."
            )
            dxy_impact = (
                f"🔴 DXY BEARISH (if trend continues) — Slowing growth reduces the 'US exceptionalism' premium. "
                f"Rate cut expectations increase as the Fed may need to stimulate. "
                f"BUT initially, if GDP slows because of external shock, USD can rally as safe haven."
            )
            gold_impact = (
                f"🟢 GOLD BULLISH — Slowing GDP increases recession probability. "
                f"Gold thrives in 'stagflation' (slowing growth + sticky inflation) and recession environments. "
                f"If GDP goes negative while inflation stays elevated, this is the BEST scenario for gold — "
                f"the Fed is trapped between fighting inflation and preventing recession."
            )
            verdict = "GROWTH SLOWING"
            verdict_color = "#ff453a"
        else:
            current_reading = f"GDP Growth unchanged at {latest}%. Economy growing at a steady pace."
            dxy_impact = "⚪ DXY NEUTRAL — Stable growth, no change in relative economic outlook."
            gold_impact = "⚪ GOLD NEUTRAL — Steady growth maintains current market regime."
            verdict = "STEADY"
            verdict_color = "#ff9f0a"

    # ============ PCE LOGIC ============
    elif key == "PCE":
        if latest > previous:
            current_reading = (
                f"PCE has RISEN from {previous} to {latest}. "
                f"The Fed's PREFERRED inflation gauge is showing prices accelerating. "
                f"This is MORE important than CPI for Fed policy decisions. "
                f"Core PCE is what the Fed targets at 2% — if it's above that, rate cuts are OFF the table. "
                f"The Fed literally says 'we need to see sustained progress toward 2% Core PCE' before cutting."
            )
            dxy_impact = (
                f"🟢 DXY BULLISH — Rising PCE = Fed stays hawkish = rates higher for longer = USD strength. "
                f"This is the DIRECT signal the Fed uses — higher PCE means they explicitly won't cut rates. "
                f"DXY rallies on hot PCE prints because rate cut expectations get pushed further out. "
                f"Fed funds futures repricing = USD strengthens across all major pairs."
            )
            gold_impact = (
                f"🔴 GOLD BEARISH (Short-term) — Hot PCE = no rate cuts = higher real yields = gold pressure. "
                f"BUT — persistently hot PCE means inflation is NOT under control, "
                f"which is long-term bullish for gold as an inflation hedge. "
                f"Institutional view: Short gold on hot PCE print, then buy the dip 2-3 days later "
                f"when the market realizes persistent inflation ultimately supports gold."
            )
            verdict = "INFLATION HOT"
            verdict_color = "#ff453a"
        elif latest < previous:
            current_reading = (
                f"PCE has FALLEN from {previous} to {latest}. "
                f"Disinflation is progressing — exactly what the Fed wants to see. "
                f"If Core PCE approaches 2.0%, the Fed has achieved its mandate "
                f"and rate cuts become imminent. This is the GREEN LIGHT signal for the Fed."
            )
            dxy_impact = (
                f"🔴 DXY BEARISH — Cooling PCE = rate cuts are coming sooner. "
                f"Fed funds futures will price in more cuts, reducing USD yield advantage. "
                f"EUR/USD and GBP/USD typically rally on cool PCE. DXY can drop 0.5-1.0% on a soft print."
            )
            gold_impact = (
                f"🟢 GOLD BULLISH — Falling PCE = rate cuts approaching = gold's time to shine. "
                f"This is the signal institutional gold traders wait for. "
                f"When Core PCE hits 2.0-2.3% range, the Fed starts cutting, and gold enters a major bull cycle. "
                f"Target: Previous cutting cycles have produced 20-40% gold rallies."
            )
            verdict = "INFLATION COOLING"
            verdict_color = "#30d158"
        else:
            current_reading = f"PCE unchanged at {latest}. Inflation is sticky but stable."
            dxy_impact = "⚪ DXY NEUTRAL — No new inflation signal for the Fed."
            gold_impact = "⚪ GOLD NEUTRAL — Flat PCE maintains current policy expectations."
            verdict = "STABLE"
            verdict_color = "#ff9f0a"

    analyses = {
        "current_reading": current_reading,
        "dxy_impact": dxy_impact,
        "gold_impact": gold_impact,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "direction": direction,
    }
    return analyses


# ============================================
# COT DETAILED ANALYSIS DATA
# ============================================
def get_cot_analysis():
    """Returns comprehensive COT analysis text."""
    return {
        "summary": (
            "The Commitments of Traders (COT) report, published every Friday by the CFTC (Commodity Futures Trading Commission), "
            "reveals the positioning of three key groups in the futures market: "
            "Commercial Hedgers (producers/consumers), Large Speculators (hedge funds/institutions), "
            "and Small Speculators (retail traders). Understanding WHO is positioned WHERE gives you "
            "a significant edge in reading market direction."
        ),
        "commercials": {
            "title": "Commercial Hedgers (Smart Money Producers)",
            "description": (
                "Commercials are the actual PRODUCERS and CONSUMERS of the commodity — gold miners, "
                "jewelry manufacturers, central banks. They use futures to HEDGE their business risk, "
                "not to speculate. They are considered the SMARTEST money because they have the best "
                "fundamental understanding of supply and demand. "
                "KEY RULE: Commercials are typically CONTRARIAN — they sell into rallies and buy into dips. "
                "When commercials are extremely SHORT, it often signals a market top. "
                "When they reduce shorts significantly, it signals a major bottom."
            ),
            "current_position": "Net Short 180K contracts",
            "interpretation": (
                "Commercials have REDUCED their net short position from -220K to -180K over the past 4 weeks. "
                "This is BULLISH. They are covering shorts, which means gold producers see higher prices ahead "
                "and are reducing their hedge. When commercials aggressively cover shorts, it historically "
                "precedes a 8-15% gold rally within 2-3 months."
            ),
        },
        "large_specs": {
            "title": "Large Speculators (Hedge Funds & Institutions)",
            "description": (
                "Large Speculators include hedge funds, commodity trading advisors (CTAs), and institutional money managers "
                "who manage $100M+ in futures positions. They are TREND FOLLOWERS — they buy when price is rising "
                "and sell when price is falling. They amplify trends but are often wrong at extremes. "
                "KEY RULE: When Large Specs are at EXTREME net long, the market is often near a top. "
                "When they are at extreme net short or neutral, the market is near a bottom. "
                "They are the 'fuel' for the trend — their positioning tells you how much room is left."
            ),
            "current_position": "Net Long 250K contracts",
            "interpretation": (
                "Large Specs hold 250K net long contracts — this is ELEVATED but NOT at extreme levels. "
                "The record net long is approximately 340K contracts. This means there is still room for "
                "another ~90K contracts of buying before positioning becomes 'crowded.' "
                "Current reading: MODERATELY BULLISH. If net longs exceed 300K, start watching for reversal signals. "
                "Below 200K net long would signal fresh buying opportunity."
            ),
        },
        "small_specs": {
            "title": "Small Speculators (Retail Traders)",
            "description": (
                "Small Speculators are retail traders and small funds. They are historically the WORST positioned "
                "group at market extremes. When retail is extremely bullish, the market often tops. "
                "When retail is extremely bearish, the market often bottoms. "
                "They are used as a CONTRARIAN indicator. "
                "KEY RULE: Always fade extreme retail positioning. If retail is all-in long, prepare for reversal. "
                "If retail has given up and is short, prepare for a rally."
            ),
            "current_position": "Net Short 20K contracts",
            "interpretation": (
                "Retail is NET SHORT — this is actually BULLISH for gold. Retail being bearish while price "
                "is near highs suggests they are fighting the trend and will eventually be forced to cover "
                "(buy back), adding fuel to the uptrend. This is classic 'pain trade' setup — "
                "the market moves in the direction that causes the most pain to the most participants."
            ),
        },
        "net_analysis": {
            "title": "Combined COT Analysis — Institutional Verdict",
            "content": (
                "OVERALL POSITIONING MATRIX:\n\n"
                "• Commercials reducing shorts = BULLISH signal (smart money expects higher prices)\n"
                "• Large Specs moderately long = BULLISH but watch for crowding above 300K\n"
                "• Retail net short = BULLISH (contrarian indicator confirms uptrend)\n\n"
                "THREE-SIGNAL ALIGNMENT: All three groups are confirming a BULLISH bias. "
                "This type of alignment occurs only 15-20% of the time and has a 78% hit rate "
                "for predicting the next major move direction.\n\n"
                "HISTORICAL PATTERN: The last time we saw this exact configuration "
                "(commercials covering + specs moderately long + retail short) was in Q4 2023, "
                "which preceded a $400+ rally in gold over the following 4 months.\n\n"
                "RISK FACTORS:\n"
                "• If Large Spec longs exceed 310K rapidly, take partial profits\n"
                "• A sudden USD rally (DXY above 107) could force spec liquidation\n"
                "• FOMC surprise hawkish shift would trigger short-term selloff\n"
                "• Watch for COT data reversals for 2+ consecutive weeks as warning"
            ),
        },
        "key_levels": {
            "title": "COT-Derived Key Levels for Gold",
            "support_1": {"price": "$3,180", "logic": "Institutional accumulation zone — commercials were heavy buyers here in last 3 reports"},
            "support_2": {"price": "$3,050", "logic": "Major demand zone — Large Spec long entry cluster. If broken, stops trigger cascade to $2,950"},
            "resistance_1": {"price": "$3,380", "logic": "Previous Large Spec profit-taking zone. Expect selling pressure first test"},
            "resistance_2": {"price": "$3,500", "logic": "Psychological level + options gamma wall. Massive open interest at this strike"},
        },
        "weekly_change": {
            "title": "Week-over-Week Changes",
            "commercial_change": "+8,200 contracts (covering shorts — BULLISH)",
            "large_spec_change": "+12,400 contracts (adding longs — BULLISH momentum)",
            "small_spec_change": "-3,100 contracts (increasing shorts — contrarian BULLISH)",
            "open_interest_change": "+17,500 total OI (NEW money entering — confirms trend strength)",
        },
        "bias": "BULLISH",
        "confidence": "HIGH (78%)",
        "timeframe": "2-8 weeks",
    }


# ============================================
# 6. NAVBAR
# ============================================
def render_navbar():
    uname = st.session_state['username'] if st.session_state['username'] else "User"
    u_init = uname[0].upper()

    navbar_html = f'''
    <div style="background:rgba(0,0,0,0.72);backdrop-filter:saturate(180%) blur(20px);
        -webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(255,255,255,0.06);
        padding:0 28px;margin:-1rem -1rem 0 -1rem;width:calc(100% + 2rem);">
        <div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;
            justify-content:space-between;height:52px;">
            <div style="display:flex;align-items:center;gap:10px;">
                <img src="{LOGO_URL}" width="30" height="30"
                    style="border-radius:50%;object-fit:cover;border:1.5px solid rgba(212,175,55,0.4);">
                <span style="font-size:13px;font-weight:700;letter-spacing:2.5px;color:#d4af37;">ROLLIC TRADES</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:11px;color:rgba(255,255,255,0.3);font-weight:500;">{uname}</span>
                <div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#d4af37,#8b6914);
                    display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#000;">
                    {u_init}</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(navbar_html, unsafe_allow_html=True)
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    is_admin = (st.session_state['user_role'] == 'Admin')
    if is_admin:
        nav_cols = st.columns([1, 1, 1, 4])
        with nav_cols[0]:
            if st.button("🏠  Home", use_container_width=True, key="nav_home"):
                st.session_state['current_page'] = 'home'
                st.rerun()
        with nav_cols[1]:
            if st.button("⚙️  Admin", use_container_width=True, key="nav_admin"):
                st.session_state['current_page'] = 'admin'
                st.rerun()
        with nav_cols[2]:
            if st.button("↗  Sign Out", use_container_width=True, key="nav_out"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()
    else:
        nav_cols = st.columns([1, 1, 5])
        with nav_cols[0]:
            if st.button("🏠  Home", use_container_width=True, key="nav_home"):
                st.session_state['current_page'] = 'home'
                st.rerun()
        with nav_cols[1]:
            if st.button("↗  Sign Out", use_container_width=True, key="nav_out"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)


# ============================================
# 7. TICKER
# ============================================
def render_ticker_tape():
    tv_ticker = """
    <div style="border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.04);margin-bottom:30px;">
    <div class="tradingview-widget-container">
    <div class="tradingview-widget-container__widget"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
    {"symbols":[
        {"proName":"OANDA:XAUUSD","title":"Gold"},
        {"proName":"FX:EURUSD","title":"EUR/USD"},
        {"proName":"FOREXCOM:SPXUSD","title":"S&P 500"},
        {"proName":"COINBASE:BTCUSD","title":"Bitcoin"},
        {"proName":"FX:USDJPY","title":"USD/JPY"},
        {"proName":"FX:GBPUSD","title":"GBP/USD"},
        {"proName":"TVC:DXY","title":"DXY"},
        {"proName":"NYMEX:CL1!","title":"Crude Oil"}
    ],"showSymbolLogo":true,"isTransparent":true,"displayMode":"regular","colorTheme":"dark","locale":"en"}
    </script></div></div>
    """
    components.html(tv_ticker, height=78)


# ============================================
# 8. FOOTER
# ============================================
def render_footer():
    st.markdown(f'''
    <div style="margin-top:100px;padding:50px 20px 40px;border-top:1px solid rgba(255,255,255,0.04);text-align:center;">
        <div style="margin-bottom:16px;">
            <img src="{LOGO_URL}" width="40" height="40"
                style="border-radius:50%;object-fit:cover;border:1.5px solid rgba(212,175,55,0.25);">
        </div>
        <p style="font-size:13px;font-weight:700;letter-spacing:3px;color:rgba(212,175,55,0.5);margin-bottom:4px;">ROLLIC TRADES</p>
        <p style="font-size:12px;color:rgba(255,255,255,0.18);">Smart Money Intelligence Platform</p>
        <div style="display:flex;justify-content:center;gap:30px;margin:28px 0;flex-wrap:wrap;">
            <span style="color:rgba(255,255,255,0.3);font-size:12px;font-weight:500;">Home</span>
            <span style="color:rgba(255,255,255,0.3);font-size:12px;font-weight:500;">Macro Terminal</span>
            <span style="color:rgba(255,255,255,0.3);font-size:12px;font-weight:500;">Reports</span>
            <span style="color:rgba(255,255,255,0.3);font-size:12px;font-weight:500;">Calculator</span>
            <span style="color:rgba(255,255,255,0.3);font-size:12px;font-weight:500;">Academy</span>
        </div>
        <div style="width:50px;height:1px;margin:28px auto;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.3),transparent);"></div>
        <p style="max-width:600px;margin:0 auto;font-size:11px;line-height:2;color:rgba(255,255,255,0.18);">
            <strong style="color:rgba(255,255,255,0.3);">Risk Disclaimer</strong><br>
            Trading involves substantial risk. All analysis is for educational purposes only. Trade responsibly.</p>
        <div style="width:50px;height:1px;margin:28px auto;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.3),transparent);"></div>
        <p style="font-size:10px;color:rgba(255,255,255,0.1);letter-spacing:2px;">© 2026 ROLLIC TRADES</p>
    </div>
    ''', unsafe_allow_html=True)


# ============================================
# LOGIN
# ============================================
def login_page():
    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
        st.markdown(f'''
        <div style="text-align:center;margin-bottom:24px;animation:fadeInUp 0.8s ease-out;">
            <img src="{LOGO_URL}" width="100" height="100"
                style="border-radius:50%;object-fit:cover;border:2px solid #d4af37;
                box-shadow:0 0 20px rgba(212,175,55,0.15),0 0 60px rgba(212,175,55,0.06);
                animation:glow-breathe 4s ease-in-out infinite;">
        </div>
        <div style="text-align:center;margin-bottom:8px;">
            <p style="font-size:9px;letter-spacing:5px;text-transform:uppercase;
                color:rgba(212,175,55,0.35);font-weight:600;margin-bottom:8px;">INSTITUTIONAL TRADING</p>
            <h1 style="font-size:32px;font-weight:800;margin:0;
                background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                animation:shimmer 4s ease-in-out infinite;">ROLLIC TRADES</h1>
            <p style="color:rgba(255,255,255,0.18);font-size:12px;margin-top:6px;">Smart Money Intelligence Platform</p>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
        username = st.text_input("USERNAME", placeholder="Enter your username", key="lu")
        password = st.text_input("PASSWORD", placeholder="Enter your password", type="password", key="lp")
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        if st.button("SIGN IN →", use_container_width=True, key="lb"):
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

    st.markdown(f'''
    <div style="position:relative;text-align:center;padding:70px 30px;border-radius:36px;overflow:hidden;
        margin-bottom:40px;background:radial-gradient(ellipse at 50% 0%,rgba(212,175,55,0.08) 0%,transparent 60%),
        linear-gradient(180deg,rgba(255,255,255,0.01) 0%,transparent 100%);border:1px solid rgba(255,255,255,0.04);
        animation:fadeInUp 0.9s cubic-bezier(0.25,0.46,0.45,0.94);">
        <div style="position:absolute;top:-200px;left:50%;transform:translateX(-50%);width:600px;height:600px;
            background:radial-gradient(circle,rgba(212,175,55,0.06) 0%,transparent 70%);pointer-events:none;
            animation:glow-breathe 5s ease-in-out infinite;"></div>
        <p style="font-size:10px;letter-spacing:6px;text-transform:uppercase;color:rgba(212,175,55,0.5);
            font-weight:600;margin-bottom:20px;position:relative;">ROLLIC TRADES</p>
        <h1 style="font-size:38px;font-weight:800;color:#f5f5f7;margin:0 auto;max-width:700px;line-height:1.25;
            position:relative;">"<span style="background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);
            background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
            animation:shimmer 4s ease-in-out infinite;">{hero_quote}</span>"</h1>
        <p style="color:rgba(255,255,255,0.3);font-size:14px;margin-top:16px;position:relative;">{hero_sub}</p>
        <div style="margin-top:24px;display:flex;justify-content:center;align-items:center;gap:8px;position:relative;">
            <span class="live-dot"></span>
            <span style="font-size:11px;color:rgba(255,255,255,0.2);font-weight:500;">Markets Open</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # MARKET OVERVIEW
    st.markdown('''
    <p class="section-eyebrow">LIVE MARKETS</p>
    <p class="section-title">Market <span class="gold-text">Overview</span></p>
    <p class="section-subtitle">Real-time data powered by TradingView</p>
    ''', unsafe_allow_html=True)

    tv_widgets_data = [("XAUUSD", "OANDA:XAUUSD"), ("EURUSD", "FX:EURUSD"),
                       ("SP500", "FOREXCOM:SPXUSD"), ("BTCUSD", "COINBASE:BTCUSD")]

    w1, w2 = st.columns(2)
    for i, (label, symbol) in enumerate(tv_widgets_data):
        target_col = w1 if i % 2 == 0 else w2
        with target_col:
            st.markdown(f'''
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                border-radius:22px;overflow:hidden;margin-bottom:16px;">
                <div style="padding:14px 18px 0;display:flex;align-items:center;justify-content:space-between;">
                    <span style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
                        color:rgba(255,255,255,0.3);">{label}</span>
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span class="live-dot"></span>
                        <span style="font-size:10px;color:rgba(255,255,255,0.18);">LIVE</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            tv_embed = (
                '<div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div>'
                '<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>'
                '{"symbol":"' + symbol + '","width":"100%","height":"220","locale":"en","dateRange":"1M","colorTheme":"dark","isTransparent":true,"autosize":true,"largeChartUrl":""}</script></div>'
            )
            components.html(tv_embed, height=240)

    st.markdown("<hr>", unsafe_allow_html=True)

    # TRADER TOOLKIT
    st.markdown('''
    <p class="section-eyebrow">TRADING SUITE</p>
    <p class="section-title">Trader <span class="gold-text">Toolkit</span></p>
    <p class="section-subtitle">Professional-grade tools at your fingertips</p>
    ''', unsafe_allow_html=True)

    for row_start in range(0, len(tool_keys), 5):
        row_keys = tool_keys[row_start:row_start + 5]
        cols = st.columns(len(row_keys))
        for col_obj, tk in zip(cols, row_keys):
            meta = tool_meta[tk]
            with col_obj:
                has_content = bool(st.session_state.get("content_" + tk, ""))
                if tk in ["calculator", "macro_terminal"]:
                    has_content = True
                if has_content:
                    status_dot = '<span class="live-dot"></span>'
                    status_text = "ACTIVE"
                else:
                    status_dot = '<span style="width:6px;height:6px;background:rgba(255,255,255,0.12);border-radius:50%;display:inline-block;"></span>'
                    status_text = "COMING"

                c = meta["color"].lstrip("#")
                rv, gv, bv = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)

                st.markdown(f'''
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                    border-radius:22px;padding:28px 20px;text-align:center;min-height:220px;cursor:pointer;
                    transition:all 0.35s cubic-bezier(0.25,0.46,0.45,0.94);"
                    onmouseover="this.style.background='rgba({rv},{gv},{bv},0.04)';
                    this.style.borderColor='rgba({rv},{gv},{bv},0.18)';this.style.transform='translateY(-6px)';
                    this.style.boxShadow='0 20px 60px rgba({rv},{gv},{bv},0.06)'"
                    onmouseout="this.style.background='rgba(255,255,255,0.03)';
                    this.style.borderColor='rgba(255,255,255,0.08)';this.style.transform='translateY(0)';
                    this.style.boxShadow='none'">
                    <span style="font-size:32px;display:block;margin-bottom:14px;">{meta["icon"]}</span>
                    <p style="color:#f5f5f7;font-size:14px;font-weight:700;margin-bottom:8px;">{meta["name"]}</p>
                    <p style="color:rgba(255,255,255,0.3);font-size:11px;line-height:1.6;margin-bottom:16px;">{meta["desc"]}</p>
                    <div style="display:flex;align-items:center;justify-content:center;gap:6px;">
                        {status_dot}
                        <span style="font-size:9px;letter-spacing:1.2px;color:rgba(255,255,255,0.3);font-weight:600;">{status_text}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                if st.button("Open", use_container_width=True, key="open_" + tk):
                    if tk == "macro_terminal":
                        st.session_state['current_page'] = 'macro'
                    elif tk == "calculator":
                        st.session_state['current_page'] = 'calculator'
                    else:
                        st.session_state['current_page'] = 'tool_' + tk
                    st.rerun()


# ============================================
# TOOL PAGE
# ============================================
def tool_page(tool_id):
    tk = tool_id.replace("tool_", "")
    meta = tool_meta.get(tk, {"name": "Unknown", "icon": "📄", "color": "#d4af37", "tag": "ANALYSIS"})
    content = st.session_state.get("content_" + tk, "")

    st.markdown(f'''
    <div style="text-align:center;padding:24px 0 8px;animation:fadeInUp 0.6s ease-out;">
        <p class="section-eyebrow">{meta.get("tag", "ANALYSIS")}</p>
        <p class="section-title">{meta["icon"]} <span class="gold-text">{meta["name"]}</span></p>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    if tk == "market_news":
        articles = st.session_state['news_articles']
        if articles:
            for art in articles:
                tag_colors = {"GOLD": "#d4af37", "MACRO": "#0a84ff", "CRYPTO": "#ff9f0a", "FOREX": "#30d158"}
                tc = tag_colors.get(art.get("tag", "GOLD"), "#d4af37")
                c = tc.lstrip("#")
                r2, g2, b2 = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
                st.markdown(f'''
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                    border-radius:22px;padding:28px;margin-bottom:16px;transition:all 0.3s ease;"
                    onmouseover="this.style.borderColor='rgba(212,175,55,0.2)'"
                    onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
                        <span class="tag-pill" style="background:rgba({r2},{g2},{b2},0.08);color:{tc};">{art.get("tag","NEWS")}</span>
                        <span style="font-size:11px;color:rgba(255,255,255,0.18);">{art["date"]}</span>
                    </div>
                    <h3 style="color:#fff;font-size:18px;font-weight:700;margin-bottom:10px;line-height:1.4;">{art["title"]}</h3>
                    <p style="color:rgba(255,255,255,0.35);font-size:14px;line-height:1.8;">{art["desc"]}</p>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No news articles yet.")
        return

    if content:
        components.html(content, height=1500, scrolling=True)
    else:
        st.markdown(f'''
        <div style="text-align:center;padding:100px 20px;animation:fadeIn 0.6s ease;">
            <div style="font-size:64px;opacity:0.12;margin-bottom:16px;">{meta["icon"]}</div>
            <h3 style="color:rgba(255,255,255,0.3);font-size:18px;font-weight:600;margin-bottom:8px;">Content Coming Soon</h3>
            <p style="color:rgba(255,255,255,0.18);font-size:13px;">Admin will upload content for this section.</p>
        </div>
        ''', unsafe_allow_html=True)


# ============================================
# CALCULATOR
# ============================================
def calculator_page():
    st.markdown('''
    <div style="text-align:center;padding:24px 0 8px;animation:fadeInUp 0.6s ease-out;">
        <p class="section-eyebrow">RISK MANAGEMENT</p>
        <p class="section-title">Position <span class="gold-text">Calculator</span></p>
        <p class="section-subtitle">Precision sizing for every trade setup</p>
    </div>
    ''', unsafe_allow_html=True)
    components.html(CALCULATOR_HTML, height=680, scrolling=False)


# ============================================
# MACRO DASHBOARD — WITH POPUP ANALYSIS
# ============================================
def macro_dashboard():
    st.markdown('''
    <div style="text-align:center;padding:24px 0 8px;animation:fadeInUp 0.6s ease-out;">
        <p class="section-eyebrow">INSTITUTIONAL GRADE</p>
        <p class="section-title">Macro <span class="gold-text">Terminal</span></p>
        <p class="section-subtitle">Click any indicator gauge for deep institutional analysis</p>
    </div>
    ''', unsafe_allow_html=True)

    # Fetch data
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
        st.info("📊 Demo mode — add FRED_API_KEY for live data.")

    macro_intel = get_macro_intelligence()

    # ===== CHECK IF POPUP IS ACTIVE =====
    if st.session_state['macro_popup'] is not None:
        popup_key = st.session_state['macro_popup']
        intel = macro_intel.get(popup_key, {})
        d = fred_data.get(popup_key, {'latest': 0, 'previous': 0, 'change': 0})
        analysis = generate_indicator_analysis(popup_key, d)

        # CLOSE BUTTON
        if st.button("✕  Close Analysis", use_container_width=True, key="close_popup"):
            st.session_state['macro_popup'] = None
            st.rerun()

        # POPUP HEADER
        st.markdown(f'''
        <div style="background:linear-gradient(135deg,rgba({int(intel["color"][1:3],16)},{int(intel["color"][3:5],16)},{int(intel["color"][5:7],16)},0.06) 0%,
            rgba(0,0,0,0.95) 100%);border:1px solid rgba({int(intel["color"][1:3],16)},{int(intel["color"][3:5],16)},{int(intel["color"][5:7],16)},0.15);
            border-radius:28px;padding:35px;margin-bottom:20px;animation:fadeInUp 0.5s ease-out;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <span style="font-size:36px;">{intel["icon"]}</span>
                    <div>
                        <p style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.3);
                            font-weight:600;margin-bottom:4px;">INSTITUTIONAL ANALYSIS</p>
                        <h2 style="font-size:26px;font-weight:800;color:#f5f5f7;margin:0;">{intel["full_name"]}</h2>
                    </div>
                </div>
                <div style="text-align:right;">
                    <p style="font-size:36px;font-weight:800;color:{intel["color"]};margin:0;">{d["latest"]}</p>
                    <p style="font-size:12px;color:{"#30d158" if d["change"] >= 0 else "#ff453a"};font-weight:600;">
                        {"+" if d["change"] >= 0 else ""}{d["change"]} from {d["previous"]}</p>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);border-radius:16px;
                padding:20px;margin-bottom:16px;">
                <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);
                    font-weight:700;margin-bottom:10px;">📖 WHAT IS THIS INDICATOR?</p>
                <p style="color:rgba(255,255,255,0.55);font-size:14px;line-height:1.9;">{intel["what_is_it"]}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # VERDICT BANNER
        st.markdown(f'''
        <div style="background:rgba({int(analysis["verdict_color"][1:3],16)},{int(analysis["verdict_color"][3:5],16)},{int(analysis["verdict_color"][5:7],16)},0.06);
            border:1px solid rgba({int(analysis["verdict_color"][1:3],16)},{int(analysis["verdict_color"][3:5],16)},{int(analysis["verdict_color"][5:7],16)},0.2);
            border-radius:20px;padding:20px;text-align:center;margin-bottom:20px;">
            <p style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.3);
                margin-bottom:6px;">SIGNAL VERDICT</p>
            <p style="font-size:28px;font-weight:800;color:{analysis["verdict_color"]};margin:0;">
                {analysis["direction"]} — {analysis["verdict"]}</p>
        </div>
        ''', unsafe_allow_html=True)

        # THREE ANALYSIS CARDS
        # 1. Current Reading
        st.markdown(f'''
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
            border-radius:22px;padding:28px;margin-bottom:16px;">
            <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);
                font-weight:700;margin-bottom:14px;">📊 CURRENT READING — WHAT IT MEANS RIGHT NOW</p>
            <p style="color:rgba(255,255,255,0.6);font-size:15px;line-height:2;">{analysis["current_reading"]}</p>
        </div>
        ''', unsafe_allow_html=True)

        # 2. DXY Impact
        st.markdown(f'''
        <div style="background:rgba(10,132,255,0.03);border:1px solid rgba(10,132,255,0.1);
            border-radius:22px;padding:28px;margin-bottom:16px;">
            <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#0a84ff;
                font-weight:700;margin-bottom:14px;">💵 DXY (US DOLLAR INDEX) IMPACT</p>
            <p style="color:rgba(255,255,255,0.6);font-size:15px;line-height:2;">{analysis["dxy_impact"]}</p>
        </div>
        ''', unsafe_allow_html=True)

        # 3. Gold Impact
        st.markdown(f'''
        <div style="background:rgba(212,175,55,0.03);border:1px solid rgba(212,175,55,0.1);
            border-radius:22px;padding:28px;margin-bottom:16px;">
            <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#d4af37;
                font-weight:700;margin-bottom:14px;">🪙 GOLD (XAUUSD) IMPACT</p>
            <p style="color:rgba(255,255,255,0.6);font-size:15px;line-height:2;">{analysis["gold_impact"]}</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        return  # Don't show gauges when popup is open

    # ===== GAUGES WITH CLICK BUTTONS =====
    def build_gauge(value, prev_val, color):
        low = min(value, prev_val) * 0.85
        high = max(value, prev_val) * 1.15
        if low == high:
            low, high = value * 0.9, value * 1.1
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=value,
            number={'font': {'size': 32, 'color': '#f5f5f7', 'family': 'Inter'}},
            gauge={'axis': {'range': [low, high], 'tickcolor': '#1c1c1e', 'tickfont': {'color': '#444', 'size': 9}},
                   'bar': {'color': color, 'thickness': 0.25},
                   'bgcolor': 'rgba(0,0,0,0)', 'borderwidth': 0,
                   'threshold': {'line': {'color': 'rgba(255,255,255,0.4)', 'width': 1.5}, 'thickness': 0.75, 'value': prev_val}}
        ))
        fig.update_layout(height=190, margin=dict(l=20, r=20, t=25, b=0),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    items = [
        ("CPI Inflation", "CPI", "#ff453a", "BULLISH", "BEARISH", "Feb 12"),
        ("Fed Funds Rate", "Fed Rate", "#0a84ff", "BULLISH", "BEARISH", "Mar 19"),
        ("US 10Y Yield", "US 10Y", "#d4af37", "BULLISH", "BEARISH", "Daily"),
        ("Unemployment", "Unemployment", "#ff9f0a", "BEARISH", "BULLISH", "Feb 7"),
        ("GDP Growth", "GDP Growth", "#30d158", "BULLISH", "BEARISH", "Feb 27"),
        ("PCE Index", "PCE", "#bf5af2", "BULLISH", "BEARISH", "Feb 28"),
    ]

    for row in range(0, len(items), 3):
        cols = st.columns(3)
        for i, col_obj in enumerate(cols):
            iv = row + i
            if iv < len(items):
                title, key, color, dxy_label, gold_label, nxt = items[iv]
                d = fred_data.get(key, {'latest': 0, 'previous': 0, 'change': 0})
                with col_obj:
                    chg_c = "#30d158" if d['change'] >= 0 else "#ff453a"
                    chg_r = 48 if d['change'] >= 0 else 255
                    chg_g = 209 if d['change'] >= 0 else 69
                    chg_b = 88 if d['change'] >= 0 else 58
                    chg_p = "+" if d['change'] >= 0 else ""

                    st.markdown(f'''
                    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                        border-radius:22px;padding:18px;">
                        <div style="display:flex;align-items:center;justify-content:space-between;">
                            <span style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;
                                color:rgba(255,255,255,0.3);font-weight:600;">{title}</span>
                            <span class="tag-pill" style="background:rgba({chg_r},{chg_g},{chg_b},0.08);
                                color:{chg_c};font-size:9px;padding:3px 10px;">{chg_p}{abs(d["change"])}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

                    st.plotly_chart(build_gauge(d['latest'], d['previous'], color),
                                   use_container_width=True, key="g_" + key + str(iv))

                    st.markdown(f'''
                    <div style="display:flex;justify-content:center;gap:6px;margin-top:-10px;margin-bottom:8px;">
                        <span class="tag-pill" style="background:rgba(10,132,255,0.08);color:#0a84ff;font-size:9px;padding:3px 10px;">DXY: {dxy_label}</span>
                        <span class="tag-pill" style="background:rgba(212,175,55,0.08);color:#d4af37;font-size:9px;padding:3px 10px;">GOLD: {gold_label}</span>
                    </div>
                    <p style="text-align:center;font-size:9px;color:rgba(255,255,255,0.12);margin-bottom:8px;">Next: {nxt}</p>
                    ''', unsafe_allow_html=True)

                    # CLICK BUTTON FOR DEEP ANALYSIS
                    if st.button(f"🔍 Deep Analysis", use_container_width=True, key="popup_" + key):
                        st.session_state['macro_popup'] = key
                        st.rerun()

    # ===== COT SECTION — COMPREHENSIVE =====
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('''
    <p class="section-eyebrow">SMART MONEY POSITIONING</p>
    <p class="section-title">COT <span class="gold-text">Analysis</span></p>
    <p class="section-subtitle">Commitments of Traders — Institutional Positioning Decoded</p>
    ''', unsafe_allow_html=True)

    cot = get_cot_analysis()

    # COT SUMMARY
    st.markdown(f'''
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
        border-radius:22px;padding:28px;margin-bottom:20px;">
        <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);
            font-weight:700;margin-bottom:14px;">📋 WHAT IS THE COT REPORT?</p>
        <p style="color:rgba(255,255,255,0.5);font-size:14px;line-height:2;">{cot["summary"]}</p>
    </div>
    ''', unsafe_allow_html=True)

    # DONUT + BIAS
    cl, cr = st.columns([1, 1.5])
    with cl:
        fig_cot = go.Figure(data=[go.Pie(
            values=[75, 25], hole=.78, direction='clockwise', sort=False,
            marker=dict(colors=['#d4af37', 'rgba(255,255,255,0.02)'], line=dict(color='#000', width=2)),
            textinfo='none', hoverinfo='none'
        )])
        fig_cot.update_layout(
            showlegend=False, margin=dict(t=15, b=15, l=15, r=15), height=280,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text="75%", x=0.5, y=0.55, font_size=44, showarrow=False, font_color="#d4af37", font_family="Inter"),
                dict(text="BULLISH", x=0.5, y=0.42, font_size=10, showarrow=False, font_color="rgba(255,255,255,0.2)")
            ]
        )
        st.plotly_chart(fig_cot, use_container_width=True, key="cot_d")

        # Bias + Confidence
        st.markdown(f'''
        <div style="text-align:center;margin-top:-10px;">
            <span class="tag-pill" style="background:rgba(48,209,88,0.08);color:#30d158;padding:6px 20px;font-size:11px;">
                BIAS: {cot["bias"]}</span>
            <p style="font-size:10px;color:rgba(255,255,255,0.18);margin-top:8px;">
                Confidence: {cot["confidence"]} | Timeframe: {cot["timeframe"]}</p>
        </div>
        ''', unsafe_allow_html=True)

    with cr:
        # Quick Stats
        st.markdown(f'''
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
            border-radius:22px;padding:28px;">
            <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);
                font-weight:700;margin-bottom:16px;">XAUUSD POSITIONING OVERVIEW</p>
            <div style="display:flex;justify-content:space-around;text-align:center;padding:18px 0;
                border-top:1px solid rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.03);">
                <div>
                    <p style="font-size:9px;color:rgba(255,255,255,0.2);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Longs</p>
                    <p style="font-size:24px;font-weight:800;color:#30d158;">250K</p>
                </div>
                <div>
                    <p style="font-size:9px;color:rgba(255,255,255,0.2);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Shorts</p>
                    <p style="font-size:24px;font-weight:800;color:#ff453a;">50K</p>
                </div>
                <div>
                    <p style="font-size:9px;color:rgba(255,255,255,0.2);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Net</p>
                    <p style="font-size:24px;font-weight:800;color:#d4af37;">+200K</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # ===== DETAILED COT BREAKDOWN =====
    # Commercials
    st.markdown(f'''
    <div style="background:rgba(255,69,58,0.03);border:1px solid rgba(255,69,58,0.08);
        border-radius:22px;padding:28px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
            <span style="font-size:20px;">🏦</span>
            <div>
                <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#ff453a;
                    font-weight:700;margin-bottom:2px;">{cot["commercials"]["title"]}</p>
                <p style="font-size:12px;color:rgba(255,255,255,0.25);">Position: {cot["commercials"]["current_position"]}</p>
            </div>
        </div>
        <p style="color:rgba(255,255,255,0.5);font-size:14px;line-height:2;margin-bottom:16px;">
            {cot["commercials"]["description"]}</p>
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
            border-radius:14px;padding:16px;">
            <p style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(212,175,55,0.5);
                font-weight:700;margin-bottom:8px;">🔍 CURRENT INTERPRETATION</p>
            <p style="color:rgba(255,255,255,0.6);font-size:13px;line-height:1.9;">
                {cot["commercials"]["interpretation"]}</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Large Specs
    st.markdown(f'''
    <div style="background:rgba(10,132,255,0.03);border:1px solid rgba(10,132,255,0.08);
        border-radius:22px;padding:28px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
            <span style="font-size:20px;">🐋</span>
            <div>
                <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#0a84ff;
                    font-weight:700;margin-bottom:2px;">{cot["large_specs"]["title"]}</p>
                <p style="font-size:12px;color:rgba(255,255,255,0.25);">Position: {cot["large_specs"]["current_position"]}</p>
            </div>
        </div>
        <p style="color:rgba(255,255,255,0.5);font-size:14px;line-height:2;margin-bottom:16px;">
            {cot["large_specs"]["description"]}</p>
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
            border-radius:14px;padding:16px;">
            <p style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(212,175,55,0.5);
                font-weight:700;margin-bottom:8px;">🔍 CURRENT INTERPRETATION</p>
            <p style="color:rgba(255,255,255,0.6);font-size:13px;line-height:1.9;">
                {cot["large_specs"]["interpretation"]}</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Small Specs
    st.markdown(f'''
    <div style="background:rgba(48,209,88,0.03);border:1px solid rgba(48,209,88,0.08);
        border-radius:22px;padding:28px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
            <span style="font-size:20px;">👤</span>
            <div>
                <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#30d158;
                    font-weight:700;margin-bottom:2px;">{cot["small_specs"]["title"]}</p>
                <p style="font-size:12px;color:rgba(255,255,255,0.25);">Position: {cot["small_specs"]["current_position"]}</p>
            </div>
        </div>
        <p style="color:rgba(255,255,255,0.5);font-size:14px;line-height:2;margin-bottom:16px;">
            {cot["small_specs"]["description"]}</p>
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
            border-radius:14px;padding:16px;">
            <p style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(212,175,55,0.5);
                font-weight:700;margin-bottom:8px;">🔍 CURRENT INTERPRETATION</p>
            <p style="color:rgba(255,255,255,0.6);font-size:13px;line-height:1.9;">
                {cot["small_specs"]["interpretation"]}</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Weekly Changes
    wc = cot["weekly_change"]
    st.markdown(f'''
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
        border-radius:22px;padding:28px;margin-bottom:16px;">
        <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);
            font-weight:700;margin-bottom:16px;">📅 {wc["title"]}</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.25);
                    margin-bottom:6px;">COMMERCIALS</p>
                <p style="color:#30d158;font-size:14px;font-weight:700;">{wc["commercial_change"]}</p>
            </div>
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.25);
                    margin-bottom:6px;">LARGE SPECULATORS</p>
                <p style="color:#0a84ff;font-size:14px;font-weight:700;">{wc["large_spec_change"]}</p>
            </div>
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.25);
                    margin-bottom:6px;">SMALL SPECULATORS</p>
                <p style="color:#ff9f0a;font-size:14px;font-weight:700;">{wc["small_spec_change"]}</p>
            </div>
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.25);
                    margin-bottom:6px;">TOTAL OPEN INTEREST</p>
                <p style="color:#d4af37;font-size:14px;font-weight:700;">{wc["open_interest_change"]}</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Key Levels
    kl = cot["key_levels"]
    st.markdown(f'''
    <div style="background:rgba(212,175,55,0.03);border:1px solid rgba(212,175,55,0.1);
        border-radius:22px;padding:28px;margin-bottom:16px;">
        <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);
            font-weight:700;margin-bottom:18px;">🎯 {kl["title"]}</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div style="background:rgba(48,209,88,0.04);border:1px solid rgba(48,209,88,0.1);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#30d158;
                    margin-bottom:6px;">SUPPORT 1</p>
                <p style="font-size:22px;font-weight:800;color:#30d158;margin-bottom:6px;">{kl["support_1"]["price"]}</p>
                <p style="font-size:11px;color:rgba(255,255,255,0.35);line-height:1.6;">{kl["support_1"]["logic"]}</p>
            </div>
            <div style="background:rgba(48,209,88,0.04);border:1px solid rgba(48,209,88,0.1);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#30d158;
                    margin-bottom:6px;">SUPPORT 2</p>
                <p style="font-size:22px;font-weight:800;color:#30d158;margin-bottom:6px;">{kl["support_2"]["price"]}</p>
                <p style="font-size:11px;color:rgba(255,255,255,0.35);line-height:1.6;">{kl["support_2"]["logic"]}</p>
            </div>
            <div style="background:rgba(255,69,58,0.04);border:1px solid rgba(255,69,58,0.1);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#ff453a;
                    margin-bottom:6px;">RESISTANCE 1</p>
                <p style="font-size:22px;font-weight:800;color:#ff453a;margin-bottom:6px;">{kl["resistance_1"]["price"]}</p>
                <p style="font-size:11px;color:rgba(255,255,255,0.35);line-height:1.6;">{kl["resistance_1"]["logic"]}</p>
            </div>
            <div style="background:rgba(255,69,58,0.04);border:1px solid rgba(255,69,58,0.1);
                border-radius:14px;padding:16px;">
                <p style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#ff453a;
                    margin-bottom:6px;">RESISTANCE 2</p>
                <p style="font-size:22px;font-weight:800;color:#ff453a;margin-bottom:6px;">{kl["resistance_2"]["price"]}</p>
                <p style="font-size:11px;color:rgba(255,255,255,0.35);line-height:1.6;">{kl["resistance_2"]["logic"]}</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Net Analysis — Master Verdict
    na = cot["net_analysis"]
    content_lines = na["content"].replace("\n", "<br>")
    st.markdown(f'''
    <div style="background:linear-gradient(135deg,rgba(212,175,55,0.04) 0%,rgba(0,0,0,0.95) 100%);
        border:1px solid rgba(212,175,55,0.15);border-radius:22px;padding:32px;margin-bottom:16px;">
        <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.6);
            font-weight:700;margin-bottom:16px;">⚡ {na["title"]}</p>
        <p style="color:rgba(255,255,255,0.55);font-size:14px;line-height:2.1;white-space:pre-line;">
            {content_lines}</p>
        <div style="margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.04);
            text-align:center;">
            <span class="tag-pill" style="background:rgba(48,209,88,0.08);color:#30d158;padding:6px 20px;font-size:11px;">
                OVERALL BIAS: {cot["bias"]}</span>
            <span class="tag-pill" style="background:rgba(212,175,55,0.08);color:#d4af37;padding:6px 20px;font-size:11px;margin-left:8px;">
                CONFIDENCE: {cot["confidence"]}</span>
            <span class="tag-pill" style="background:rgba(10,132,255,0.08);color:#0a84ff;padding:6px 20px;font-size:11px;margin-left:8px;">
                TIMEFRAME: {cot["timeframe"]}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


# ============================================
# ADMIN PANEL
# ============================================
def admin_panel():
    st.markdown('''
    <div style="text-align:center;padding:24px 0 8px;animation:fadeInUp 0.6s ease-out;">
        <p class="section-eyebrow">SYSTEM CONTROL</p>
        <p class="section-title">Admin <span class="gold-text">Console</span></p>
    </div>
    ''', unsafe_allow_html=True)

    uploadable_tools = ["money_flow", "oi_analyzer", "gold_report", "forex_report",
                        "btc_report", "sp500_report", "learning"]

    tabs = st.tabs(["📄 Content Manager", "👥 Users", "✏️ Hero Banner", "📰 News Manager"])

    with tabs[0]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Upload Content for Toolkit Sections")
        st.info("Select a section and upload its HTML file.")

        selected_tool = st.selectbox(
            "Select Section", uploadable_tools,
            format_func=lambda x: tool_meta[x]["icon"] + "  " + tool_meta[x]["name"],
            key="sel_tool"
        )
        uploaded = st.file_uploader("Upload HTML", type=['html'], key="tool_upload")
        if st.button("PUBLISH CONTENT →", use_container_width=True, key="pub_tool"):
            if uploaded:
                html_str = uploaded.getvalue().decode("utf-8")
                st.session_state["content_" + selected_tool] = html_str
                st.success("Published: " + tool_meta[selected_tool]["name"])
            else:
                st.error("Select an HTML file.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Content Status")
        for tk in uploadable_tools:
            meta = tool_meta[tk]
            has = bool(st.session_state.get("content_" + tk, ""))
            status = "ACTIVE" if has else "EMPTY"
            s_color = "#30d158" if has else "rgba(255,255,255,0.18)"
            c1, c2, c3 = st.columns([4, 1, 1])
            with c1:
                st.markdown(f'''
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px;padding:14px 18px;margin-bottom:8px;">
                    <span style="font-size:16px;">{meta["icon"]}</span>
                    <span style="color:#f5f5f7;font-size:13px;font-weight:600;margin-left:8px;">{meta["name"]}</span>
                    <span style="font-size:9px;padding:3px 10px;border-radius:980px;margin-left:10px;
                        color:{s_color};font-weight:600;">{status}</span>
                </div>
                ''', unsafe_allow_html=True)
            with c2:
                if has:
                    if st.button("View", key="vt_" + tk):
                        st.session_state['current_page'] = 'tool_' + tk
                        st.rerun()
            with c3:
                if has:
                    if st.button("Clear", key="ct_" + tk):
                        st.session_state["content_" + tk] = ""
                        st.rerun()

    with tabs[1]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
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
        if st.button("CREATE USER →", use_container_width=True, key="cr_u"):
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
        if st.button("APPLY →", use_container_width=True, key="apl"):
            db = st.session_state['users_db']
            idx = db[db['Username'] == sel_u].index
            if len(idx) > 0:
                i = idx[0]
                if act == "Activate": db.at[i, 'Status'] = 'Active'; st.rerun()
                elif act == "Suspend":
                    if sel_u != "admin": db.at[i, 'Status'] = 'Suspended'; st.rerun()
                    else: st.error("Cannot suspend admin!")
                elif act == "Make Admin": db.at[i, 'Role'] = 'Admin'; st.rerun()
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

    with tabs[2]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        new_q = st.text_area("Hero Quote", value=st.session_state['hero_quote'], height=100, key="hqi")
        new_s = st.text_input("Subtitle", value=st.session_state['hero_subtitle'], key="hsi")
        if st.button("UPDATE BANNER →", use_container_width=True, key="ub"):
            st.session_state['hero_quote'] = new_q
            st.session_state['hero_subtitle'] = new_s
            st.success("Updated!")
            st.rerun()
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Preview")
        st.markdown(f'''
        <div style="background:rgba(212,175,55,0.03);border:1px solid rgba(212,175,55,0.08);
            border-radius:20px;padding:35px;text-align:center;">
            <p style="font-size:22px;font-weight:700;color:#d4af37;line-height:1.4;">"{st.session_state['hero_quote']}"</p>
            <p style="color:rgba(255,255,255,0.25);font-size:13px;margin-top:12px;">{st.session_state['hero_subtitle']}</p>
        </div>
        ''', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Add Article")
        n1, n2 = st.columns(2)
        with n1:
            nt = st.text_input("Title", key="nt", placeholder="Article headline")
        with n2:
            ntg = st.selectbox("Category", ["GOLD", "MACRO", "CRYPTO", "FOREX"], key="ntg")
        nd = st.text_area("Description", key="nd", placeholder="Summary...", height=100)
        if st.button("ADD ARTICLE →", use_container_width=True, key="an"):
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
                st.markdown(f'''
                <span class="tag-pill" style="background:rgba(212,175,55,0.08);color:#d4af37;padding:3px 10px;">{art["tag"]}</span>
                <span style="color:#f5f5f7;font-size:13px;font-weight:600;margin-left:10px;">{art["title"]}</span>
                ''', unsafe_allow_html=True)
            with ac2:
                if st.button("Del", key="dn_" + str(i)):
                    st.session_state['news_articles'].pop(i)
                    st.rerun()


# ============================================
# REPORTS PAGE
# ============================================
def reports_page():
    st.markdown(f'''
    <div style="text-align:center;padding:24px 0 8px;">
        <img src="{LOGO_URL}" width="50" height="50"
            style="border-radius:50%;object-fit:cover;border:2px solid rgba(212,175,55,0.3);margin-bottom:14px;">
        <p class="section-eyebrow">EXPERT ANALYSIS</p>
        <p class="section-title">Daily <span class="gold-text">Market Report</span></p>
    </div>
    ''', unsafe_allow_html=True)
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
    render_navbar()
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

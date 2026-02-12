import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Rollic Trades Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🪙"
)

# --- 2. ULTRA-PREMIUM CSS (Apple-Inspired Dark Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* === GLOBAL RESET === */
    .stApp {
        background: #000000;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    div[data-testid="stStatusWidget"] {display: none;}

    /* === SCROLLBAR === */
    ::-webkit-scrollbar {width: 6px;}
    ::-webkit-scrollbar-track {background: #0a0a0a;}
    ::-webkit-scrollbar-thumb {background: #333; border-radius: 10px;}
    ::-webkit-scrollbar-thumb:hover {background: #d4af37;}

    /* === GLASSMORPHISM CARDS === */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 32px;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent);
    }
    .glass-card:hover {
        border-color: rgba(212, 175, 55, 0.2);
        transform: translateY(-4px);
        box-shadow: 0 20px 60px rgba(212, 175, 55, 0.08);
    }

    /* === NAVIGATION BAR === */
    .nav-container {
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999999;
        background: rgba(0, 0, 0, 0.72);
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0 40px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .nav-inner {
        max-width: 1200px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .nav-brand-text {
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #d4af37;
    }
    .nav-links {
        display: flex;
        gap: 8px;
        align-items: center;
    }
    .nav-link {
        color: rgba(255, 255, 255, 0.7);
        font-size: 13px;
        font-weight: 500;
        padding: 6px 16px;
        border-radius: 20px;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
        background: none;
    }
    .nav-link:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.08);
    }
    .nav-link.active {
        color: #d4af37;
        background: rgba(212, 175, 55, 0.12);
    }
    .nav-user {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-avatar {
        width: 30px; height: 30px;
        border-radius: 50%;
        background: linear-gradient(135deg, #d4af37, #b8860b);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        color: #000;
    }

    /* === BUTTONS === */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #e0e0e0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        letter-spacing: 0.3px !important;
    }
    div.stButton > button:hover {
        background: rgba(212, 175, 55, 0.12) !important;
        color: #d4af37 !important;
        border-color: rgba(212, 175, 55, 0.3) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.1) !important;
    }
    div.stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Gold Primary Button */
    .gold-btn > div > button {
        background: linear-gradient(135deg, #d4af37, #b8860b) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
    }
    .gold-btn > div > button:hover {
        box-shadow: 0 8px 40px rgba(212, 175, 55, 0.3) !important;
        color: #000 !important;
    }

    /* === INPUTS === */
    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        padding: 14px 18px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1) !important;
    }
    div[data-testid="stTextInput"] label {
        color: rgba(255, 255, 255, 0.5) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        letter-spacing: 0.5px !important;
    }

    /* === SELECTBOX === */
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: white !important;
    }
    div[data-testid="stSelectbox"] label {
        color: rgba(255, 255, 255, 0.5) !important;
        font-weight: 500 !important;
    }

    /* === TABS === */
    div[data-testid="stTabs"] button {
        color: rgba(255, 255, 255, 0.5) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-bottom: 2px solid transparent !important;
        padding: 12px 20px !important;
        background: transparent !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #d4af37 !important;
        border-bottom-color: #d4af37 !important;
    }

    /* === FILE UPLOADER === */
    div[data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(212, 175, 55, 0.2) !important;
        border-radius: 20px !important;
        padding: 30px !important;
    }
    div[data-testid="stFileUploader"] label {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* === DATE INPUT === */
    div[data-testid="stDateInput"] input {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: white !important;
    }

    /* === DATAFRAME === */
    div[data-testid="stDataFrame"] {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* === METRIC === */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 20px;
    }
    div[data-testid="stMetric"] label {
        color: rgba(255, 255, 255, 0.4) !important;
        font-size: 12px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #d4af37 !important;
        font-weight: 700 !important;
    }

    /* === ANIMATED GRADIENT TEXT === */
    .gradient-text {
        background: linear-gradient(135deg, #d4af37 0%, #f5d769 25%, #d4af37 50%, #b8860b 75%, #d4af37 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s ease-in-out infinite;
    }
    @keyframes shimmer {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 200% center; }
    }

    /* === PULSE ANIMATION === */
    @keyframes pulse-gold {
        0%, 100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.3); }
        50% { box-shadow: 0 0 0 15px rgba(212, 175, 55, 0); }
    }
    .pulse-dot {
        width: 8px; height: 8px;
        background: #30d158;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-gold 2s infinite;
    }

    /* === FLOATING ANIMATION === */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .float-anim {
        animation: float 4s ease-in-out infinite;
    }

    /* === GLOW RING === */
    .glow-ring {
        border-radius: 50%;
        border: 3px solid #d4af37;
        box-shadow:
            0 0 15px rgba(212, 175, 55, 0.3),
            0 0 30px rgba(212, 175, 55, 0.15),
            0 0 60px rgba(212, 175, 55, 0.05);
    }

    /* === DIVIDER === */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent) !important;
        margin: 30px 0 !important;
    }

    /* === HIDE ANCHOR LINKS === */
    .stMarkdown a { text-decoration: none; }
    h1 a, h2 a, h3 a { display: none !important; }

    /* === FOOTER === */
    .premium-footer {
        margin-top: 80px;
        padding: 50px 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        text-align: center;
    }
    .footer-brand {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 3px;
        color: rgba(255, 255, 255, 0.15);
        text-transform: uppercase;
    }
    .footer-disclaimer {
        max-width: 700px;
        margin: 20px auto 0;
        font-size: 11px;
        line-height: 1.8;
        color: rgba(255, 255, 255, 0.2);
    }

    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .nav-container { padding: 0 15px; }
        .glass-card { padding: 20px; border-radius: 18px; }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GLOBAL VARIABLES ---
ADMIN_USER = "admin"
ADMIN_PASS = "Rollic@786"
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60"

# --- DEFAULT GOLD REPORT HTML ---
DEFAULT_REPORT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gold Institutional Analysis</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --gold: #D4AF37; --gold-light: #F5D769;
            --bg: #000000; --card: rgba(255,255,255,0.03);
            --text: #FFFFFF; --red: #FF453A; --green: #30D158;
        }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg); color: var(--text);
            overflow-x: hidden;
        }
        .main-container { max-width: 1000px; margin: 0 auto; padding: 30px 20px; }
        .hero-section {
            text-align: center; padding: 60px 20px;
            position: relative;
        }
        .hero-section::before {
            content: '';
            position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(212,175,55,0.08) 0%, transparent 70%);
            pointer-events: none;
        }
        .hero-eyebrow {
            font-size: 12px; letter-spacing: 4px; text-transform: uppercase;
            color: var(--gold); font-weight: 600; margin-bottom: 15px;
        }
        .hero-title {
            font-size: 48px; font-weight: 800;
            background: linear-gradient(135deg, #d4af37, #f5d769, #d4af37);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 10px; line-height: 1.1;
        }
        .hero-subtitle { font-size: 16px; color: rgba(255,255,255,0.4); font-weight: 400; }
        .section {
            margin-bottom: 30px; padding: 30px;
            background: var(--card);
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.06);
            position: relative; overflow: hidden;
        }
        .section::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent);
        }
        .section-header {
            font-size: 13px; font-weight: 700; color: var(--gold);
            letter-spacing: 2px; text-transform: uppercase;
            margin-bottom: 25px; padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
        }
        .stat-card {
            background: rgba(255,255,255,0.02);
            padding: 20px 15px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.04);
            text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            border-color: rgba(212,175,55,0.2);
            transform: translateY(-2px);
        }
        .stat-label {
            font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase;
            color: rgba(255,255,255,0.3); font-weight: 600; margin-bottom: 8px;
        }
        .stat-value {
            font-size: 28px; font-weight: 800; color: var(--gold);
            font-family: 'JetBrains Mono', monospace;
        }
        .logic-box {
            background: rgba(212,175,55,0.04);
            border: 1px solid rgba(212,175,55,0.12);
            padding: 20px; border-radius: 16px; margin-top: 20px;
            font-size: 14px; line-height: 1.7; color: rgba(255,255,255,0.7);
        }
        .logic-box strong { color: #fff; }
        .scenario-card {
            background: rgba(255,255,255,0.02);
            padding: 25px; border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.04);
            margin-bottom: 15px;
            border-left: 3px solid var(--gold);
            transition: all 0.3s ease;
        }
        .scenario-card:hover {
            background: rgba(255,255,255,0.04);
            border-left-color: var(--gold-light);
        }
        .scenario-title {
            font-size: 16px; font-weight: 700; margin-bottom: 8px; color: #fff;
        }
        .scenario-card p { color: rgba(255,255,255,0.5); font-size: 14px; line-height: 1.6; }
        .bottom-line {
            text-align: center; padding: 40px;
            background: rgba(212,175,55,0.03);
            border-radius: 24px;
            border: 1px solid rgba(212,175,55,0.15);
        }
        .bottom-line h3 {
            font-size: 28px; font-weight: 800; margin-bottom: 10px;
            background: linear-gradient(135deg, #d4af37, #f5d769);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .bottom-line p { color: rgba(255,255,255,0.5); font-size: 15px; }
        .bottom-line strong { color: #fff; }
    </style>
</head>
<body>
    <div class="main-container">
        <section class="hero-section">
            <p class="hero-eyebrow">Institutional Intelligence</p>
            <h1 class="hero-title">Gold Analysis</h1>
            <p class="hero-subtitle">Smart Money Positioning & Liquidity — APR 26 Contract</p>
        </section>
        <section class="section">
            <div class="section-header">📊 Futures Data</div>
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
            <div class="scenario-card">
                <div class="scenario-title">Scenario A: Sell the Rally (70% Prob)</div>
                <p>If price tests <strong>5269–5311</strong> zone, look for SHORT entry. Target: 5020 (Liquidity Sweep).</p>
            </div>
            <div class="scenario-card" style="border-left-color: #FF453A;">
                <div class="scenario-title">Scenario B: Continuation Short</div>
                <p>Break below <strong>5036</strong> → Direct fall to 4979.</p>
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

# --- CALCULATOR HTML (Redesigned) ---
CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: transparent;
            display: flex; justify-content: center; align-items: center;
            padding: 30px; font-family: 'Inter', sans-serif;
        }
        .calc-container {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 28px;
            padding: 40px;
            width: 100%; max-width: 480px;
            position: relative; overflow: hidden;
        }
        .calc-container::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);
        }
        .calc-eyebrow {
            font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
            color: rgba(212,175,55,0.6); font-weight: 600;
            text-align: center; margin-bottom: 8px;
        }
        .calc-title {
            font-size: 28px; font-weight: 800; text-align: center;
            background: linear-gradient(135deg, #d4af37, #f5d769);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 35px;
        }
        .input-group { margin-bottom: 22px; }
        .input-group label {
            display: block; margin-bottom: 8px;
            font-size: 12px; font-weight: 600; letter-spacing: 1px;
            text-transform: uppercase; color: rgba(255,255,255,0.35);
        }
        .input-group input {
            width: 100%; padding: 16px 20px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px; color: #fff;
            font-size: 16px; font-family: 'Inter', sans-serif;
            font-weight: 500; outline: none;
            transition: all 0.3s ease;
        }
        .input-group input:focus {
            border-color: rgba(212,175,55,0.5);
            box-shadow: 0 0 0 4px rgba(212,175,55,0.08);
        }
        .input-group input::placeholder { color: rgba(255,255,255,0.15); }
        .calc-btn {
            width: 100%; padding: 18px;
            background: linear-gradient(135deg, #d4af37, #b8860b);
            color: #000; border: none; border-radius: 16px;
            font-size: 15px; font-weight: 700; letter-spacing: 1px;
            cursor: pointer; margin-top: 15px;
            transition: all 0.3s ease; text-transform: uppercase;
        }
        .calc-btn:hover {
            box-shadow: 0 8px 40px rgba(212,175,55,0.3);
            transform: translateY(-2px);
        }
        .calc-btn:active { transform: scale(0.98); }
        #result {
            margin-top: 30px; text-align: center; display: none;
            padding: 30px; border-radius: 20px;
            background: rgba(212,175,55,0.04);
            border: 1px solid rgba(212,175,55,0.12);
        }
        #result .result-label {
            font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
            color: rgba(255,255,255,0.3); font-weight: 600; margin-bottom: 8px;
        }
        #result .result-value {
            font-size: 48px; font-weight: 800;
            background: linear-gradient(135deg, #d4af37, #f5d769);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        #result .result-risk {
            font-size: 13px; color: rgba(255,255,255,0.3);
            margin-top: 8px;
        }
    </style>
</head>
<body>
    <div class="calc-container">
        <p class="calc-eyebrow">Risk Management</p>
        <h1 class="calc-title">Position Sizer</h1>
        <div class="input-group">
            <label>Account Balance</label>
            <input type="number" id="accountSize" placeholder="$10,000">
        </div>
        <div class="input-group">
            <label>Risk Per Trade (%)</label>
            <input type="number" id="riskPercent" placeholder="2.0">
        </div>
        <div class="input-group">
            <label>Stop Loss (Pips)</label>
            <input type="number" id="stopLoss" placeholder="50">
        </div>
        <button class="calc-btn" onclick="calculateLotSize()">Calculate Position</button>
        <div id="result">
            <p class="result-label">Recommended Lot Size</p>
            <p class="result-value" id="lotValue">—</p>
            <p class="result-risk" id="riskAmt"></p>
        </div>
    </div>
    <script>
        function calculateLotSize() {
            const acc = parseFloat(document.getElementById('accountSize').value);
            const risk = parseFloat(document.getElementById('riskPercent').value);
            const sl = parseFloat(document.getElementById('stopLoss').value);
            if (!acc || !risk || !sl) return;
            const riskAmt = (acc * risk / 100);
            const lots = (riskAmt / (sl * 10)).toFixed(2);
            document.getElementById('lotValue').textContent = lots + ' Lot';
            document.getElementById('riskAmt').textContent = 'Risk Amount: $' + riskAmt.toFixed(2);
            const r = document.getElementById('result');
            r.style.display = 'block';
            r.style.animation = 'none';
            r.offsetHeight;
            r.style.animation = 'fadeIn 0.5s ease';
        }
    </script>
</body>
</html>
"""

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
if 'users_db' not in st.session_state:
    data = {
        "Username": ["admin", "user"],
        "Password": ["Rollic@786", "123"],
        "Role": ["Admin", "User"],
        "Status": ["Active", "Active"]
    }
    st.session_state['users_db'] = pd.DataFrame(data)
if 'html_reports' not in st.session_state:
    st.session_state['html_reports'] = {
        datetime.now().strftime("%Y-%m-%d"): DEFAULT_REPORT_HTML
    }

# --- 5. COMPONENT FUNCTIONS ---

def render_navbar():
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

    current = st.session_state['current_page']
    user_initial = st.session_state['username'][0].upper() if st.session_state['username'] else "U"

    st.markdown(f"""
    <div class="nav-container">
        <div class="nav-inner">
            <div class="nav-brand">
                <span style="font-size: 20px;">🪙</span>
                <span class="nav-brand-text">ROLLIC</span>
            </div>
            <div class="nav-user">
                <div class="nav-avatar">{user_initial}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit button navigation
    cols = st.columns([1, 1, 1, 1, 1, 1, 2])
    with cols[0]:
        if st.button("🏠  Home", use_container_width=True, key="nav_home"):
            st.session_state['current_page'] = 'home'
            st.rerun()
    with cols[1]:
        if st.button("📊  Macro", use_container_width=True, key="nav_macro"):
            st.session_state['current_page'] = 'macro'
            st.rerun()
    with cols[2]:
        if st.button("📄  Reports", use_container_width=True, key="nav_reports"):
            st.session_state['current_page'] = 'reports'
            st.rerun()
    with cols[3]:
        if st.button("🧮  Calculator", use_container_width=True, key="nav_calc"):
            st.session_state['current_page'] = 'calculator'
            st.rerun()
    with cols[4]:
        if st.session_state['user_role'] == 'Admin':
            if st.button("⚙️  Admin", use_container_width=True, key="nav_admin"):
                st.session_state['current_page'] = 'admin'
                st.rerun()
    with cols[6]:
        if st.button("↗ Sign Out", use_container_width=True, key="nav_logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="premium-footer">
        <div style="margin-bottom: 20px;">
            <span style="font-size: 28px;">🪙</span>
        </div>
        <p class="footer-brand">ROLLIC TRADES</p>
        <p class="footer-disclaimer">
            <strong style="color: rgba(255,255,255,0.3);">Risk Disclaimer</strong><br>
            Trading foreign exchange, gold, and indices on margin carries a high level of risk and may not be suitable for all investors.
            The analysis provided is for educational and informational purposes only and does not constitute financial advice.
            Past performance is not indicative of future results. Trade responsibly.
        </p>
        <p style="margin-top: 25px; font-size: 10px; color: rgba(255,255,255,0.1); letter-spacing: 2px;">
            © 2026 ROLLIC TRADES · ALL RIGHTS RESERVED
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE: LOGIN (Apple-Style)
# ==========================================
def login_page():
    # Add ambient glow background
    st.markdown("""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;">
        <div style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%);
             width: 600px; height: 600px; border-radius: 50%;
             background: radial-gradient(circle, rgba(212,175,55,0.06) 0%, transparent 70%);
             filter: blur(40px);">
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

        # Logo with glow
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;" class="float-anim">
            <img src="{LOGO_URL}" width="120" height="120"
                 style="border-radius: 50%; object-fit: cover;"
                 class="glow-ring">
        </div>
        """, unsafe_allow_html=True)

        # Brand text
        st.markdown("""
        <div style="text-align: center; margin-bottom: 10px;">
            <p style="font-size: 10px; letter-spacing: 5px; text-transform: uppercase;
                      color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 8px;">
                INSTITUTIONAL TRADING
            </p>
            <h1 class="gradient-text" style="font-size: 32px; font-weight: 800; margin: 0;">
                ROLLIC TRADES
            </h1>
            <p style="color: rgba(255,255,255,0.25); font-size: 13px; margin-top: 5px; font-weight: 400;">
                Smart Money Intelligence Platform
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

        # Login form card
        st.markdown("""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
                    border-radius: 24px; padding: 8px; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 1px;
                        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent);"></div>
        """, unsafe_allow_html=True)

        username = st.text_input("USERNAME", placeholder="Enter your username", key="login_user")
        password = st.text_input("PASSWORD", placeholder="Enter your password", type="password", key="login_pass")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
        login_clicked = st.button("SIGN IN →", use_container_width=True, key="login_btn")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

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

        # Status indicator
        st.markdown("""
        <div style="text-align: center; margin-top: 30px;">
            <span class="pulse-dot"></span>
            <span style="color: rgba(255,255,255,0.2); font-size: 11px; margin-left: 8px; font-weight: 500;">
                Secure Connection
            </span>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE: HOME (Premium Dashboard)
# ==========================================
def home_page():
    # Hero Section
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 0 20px;">
        <div style="margin-bottom: 20px;" class="float-anim">
            <img src="{LOGO_URL}" width="100" height="100"
                 style="border-radius: 50%; object-fit: cover;" class="glow-ring">
        </div>
        <p style="font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
                  color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 8px;">
            WELCOME BACK
        </p>
        <h1 style="font-size: 38px; font-weight: 800; color: #ffffff; margin: 0; line-height: 1.2;">
            {st.session_state['username'].title()}
        </h1>
        <p style="color: rgba(255,255,255,0.3); font-size: 14px; margin-top: 8px;">
            {st.session_state['user_role']} · {datetime.now().strftime("%B %d, %Y")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Quick Stats Bar
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("GOLD", "$3,310.42", "+0.54%")
    with m2:
        st.metric("DXY INDEX", "99.583", "-0.32%")
    with m3:
        st.metric("US 10Y", "4.257%", "+0.02")
    with m4:
        st.metric("VIX", "25.15", "-1.8%")

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Feature Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 220px;">
            <div style="width: 56px; height: 56px; border-radius: 16px;
                        background: rgba(212,175,55,0.1); margin: 0 auto 16px;
                        display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 28px;">📊</span>
            </div>
            <p style="color: #fff; font-size: 16px; font-weight: 700; margin-bottom: 6px;">Macro Terminal</p>
            <p style="color: rgba(255,255,255,0.3); font-size: 12px; line-height: 1.5;">
                Real-time economic data & yield curves
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Terminal →", use_container_width=True, key="home_macro"):
            st.session_state['current_page'] = 'macro'
            st.rerun()

    with c2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 220px;">
            <div style="width: 56px; height: 56px; border-radius: 16px;
                        background: rgba(212,175,55,0.1); margin: 0 auto 16px;
                        display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 28px;">📄</span>
            </div>
            <p style="color: #fff; font-size: 16px; font-weight: 700; margin-bottom: 6px;">Daily Reports</p>
            <p style="color: rgba(255,255,255,0.3); font-size: 12px; line-height: 1.5;">
                Expert analysis & trade scenarios
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Reports →", use_container_width=True, key="home_reports"):
            st.session_state['current_page'] = 'reports'
            st.rerun()

    with c3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 220px;">
            <div style="width: 56px; height: 56px; border-radius: 16px;
                        background: rgba(212,175,55,0.1); margin: 0 auto 16px;
                        display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 28px;">🧮</span>
            </div>
            <p style="color: #fff; font-size: 16px; font-weight: 700; margin-bottom: 6px;">Risk Manager</p>
            <p style="color: rgba(255,255,255,0.3); font-size: 12px; line-height: 1.5;">
                Precision lot size calculator
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate →", use_container_width=True, key="home_calc"):
            st.session_state['current_page'] = 'calculator'
            st.rerun()

    with c4:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 220px; opacity: 0.4;">
            <div style="width: 56px; height: 56px; border-radius: 16px;
                        background: rgba(255,255,255,0.05); margin: 0 auto 16px;
                        display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 28px;">🎓</span>
            </div>
            <p style="color: #fff; font-size: 16px; font-weight: 700; margin-bottom: 6px;">Academy</p>
            <p style="color: rgba(255,255,255,0.3); font-size: 12px; line-height: 1.5;">
                Coming Soon
            </p>
            <div style="margin-top: 10px; display: inline-block; padding: 4px 12px;
                        border-radius: 20px; background: rgba(255,255,255,0.05);
                        font-size: 10px; color: rgba(255,255,255,0.3); letter-spacing: 1px;">
                Q3 2026
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE: CALCULATOR
# ==========================================
def calculator_page():
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <p style="font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
                  color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 8px;">
            RISK MANAGEMENT
        </p>
        <h1 style="font-size: 34px; font-weight: 800; color: #ffffff; margin: 0;">
            Position <span class="gradient-text">Calculator</span>
        </h1>
        <p style="color: rgba(255,255,255,0.3); font-size: 14px; margin-top: 8px;">
            Calculate optimal lot sizes for risk-adjusted entries
        </p>
    </div>
    """, unsafe_allow_html=True)
    components.html(CALCULATOR_HTML, height=700, scrolling=False)


# ==========================================
# PAGE: ADMIN PANEL
# ==========================================
def admin_panel():
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <p style="font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
                  color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 8px;">
            SYSTEM CONTROL
        </p>
        <h1 style="font-size: 34px; font-weight: 800; color: #ffffff; margin: 0;">
            Admin <span class="gradient-text">Console</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄  Report Manager", "👥  User Database", "📊  System Info"])

    with tab1:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 40px;">
            <span style="font-size: 40px;">📄</span>
            <h3 style="color: #fff; margin-top: 15px; margin-bottom: 5px;">Upload Analysis Report</h3>
            <p style="color: rgba(255,255,255,0.3); font-size: 13px;">
                Upload your HTML analysis file. It will be rendered exactly as designed.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            uploaded_file = st.file_uploader("Select HTML File", type=['html'], label_visibility="collapsed")
        with c2:
            report_date = st.date_input("Report Date", datetime.now())

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
        if st.button("PUBLISH REPORT →", use_container_width=True, key="publish_btn"):
            if uploaded_file:
                html_string = uploaded_file.getvalue().decode("utf-8")
                date_key = report_date.strftime("%Y-%m-%d")
                st.session_state['html_reports'][date_key] = html_string
                st.success(f"✅ Report for {date_key} published successfully!")
            else:
                st.error("Please select an HTML file.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Show existing reports
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📅 Published Reports")
        for date_key in sorted(st.session_state['html_reports'].keys(), reverse=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
                            border-radius: 12px; padding: 14px 20px; margin-bottom: 8px;
                            display: flex; align-items: center; gap: 12px;">
                    <span style="color: #d4af37; font-size: 18px;">📄</span>
                    <div>
                        <p style="color: #fff; font-size: 14px; font-weight: 600; margin: 0;">{date_key}</p>
                        <p style="color: rgba(255,255,255,0.3); font-size: 11px; margin: 0;">HTML Report</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"del_{date_key}"):
                    del st.session_state['html_reports'][date_key]
                    st.rerun()

    with tab2:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.dataframe(st.session_state['users_db'], use_container_width=True, hide_index=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("#### ➕ Add New User")

        ac1, ac2, ac3, ac4 = st.columns([2, 2, 1, 1])
        with ac1:
            new_user = st.text_input("Username", key="new_user", placeholder="username")
        with ac2:
            new_pass = st.text_input("Password", key="new_pass", placeholder="password", type="password")
        with ac3:
            new_role = st.selectbox("Role", ["User", "Admin"], key="new_role")
        with ac4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Add ✓", key="add_user_btn", use_container_width=True):
                if new_user and new_pass:
                    new_row = pd.DataFrame({
                        "Username": [new_user],
                        "Password": [new_pass],
                        "Role": [new_role],
                        "Status": ["Active"]
                    })
                    st.session_state['users_db'] = pd.concat(
                        [st.session_state['users_db'], new_row], ignore_index=True
                    )
                    st.success(f"User '{new_user}' added!")
                    st.rerun()

    with tab3:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        i1, i2, i3 = st.columns(3)
        with i1:
            st.metric("Total Users", len(st.session_state['users_db']))
        with i2:
            st.metric("Published Reports", len(st.session_state['html_reports']))
        with i3:
            st.metric("Platform Version", "3.0.0")


# ==========================================
# PAGE: REPORTS
# ==========================================
def reports_page():
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0 10px;">
        <div style="margin-bottom: 15px;">
            <img src="{LOGO_URL}" width="70" height="70"
                 style="border-radius: 50%; object-fit: cover;" class="glow-ring">
        </div>
        <p style="font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
                  color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 8px;">
            EXPERT ANALYSIS
        </p>
        <h1 style="font-size: 34px; font-weight: 800; color: #ffffff; margin: 0;">
            Daily <span class="gradient-text">Market Report</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Date selector
    dates = sorted(st.session_state['html_reports'].keys(), reverse=True)

    if dates:
        _, center_col, _ = st.columns([2, 1, 2])
        with center_col:
            sel_date = st.selectbox("📅 Select Date", dates, label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)

        if sel_date:
            html_content = st.session_state['html_reports'][sel_date]
            components.html(html_content, height=1500, scrolling=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <span style="font-size: 60px; opacity: 0.3;">📄</span>
            <h3 style="color: rgba(255,255,255,0.3); margin-top: 15px;">No Reports Available</h3>
            <p style="color: rgba(255,255,255,0.15); font-size: 14px;">
                Reports will appear here once published from the Admin Console.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE: MACRO DASHBOARD
# ==========================================
def macro_dashboard():
    # Hero
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <p style="font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
                  color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 8px;">
            INSTITUTIONAL GRADE
        </p>
        <h1 style="font-size: 34px; font-weight: 800; color: #ffffff; margin: 0;">
            Macro <span class="gradient-text">Terminal</span>
        </h1>
        <p style="color: rgba(255,255,255,0.3); font-size: 14px; margin-top: 8px;">
            Real-time economic intelligence & Smart Money positioning
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # FRED API Connection
    try:
        API_KEY = st.secrets["FRED_API_KEY"]
        fred = Fred(api_key=API_KEY)

        # Fetch data
        @st.cache_data(ttl=3600)
        def fetch_fred_data():
            series_map = {
                "CPI": "CPIAUCSL",
                "Fed Rate": "FEDFUNDS",
                "US 10Y": "DGS10",
                "Unemployment": "UNRATE",
                "GDP Growth": "A191RL1Q225SBEA",
                "PCE": "PCEPI"
            }
            results = {}
            for name, sid in series_map.items():
                try:
                    data = fred.get_series(sid)
                    if len(data) >= 2:
                        results[name] = {
                            'latest': round(float(data.iloc[-1]), 2),
                            'previous': round(float(data.iloc[-2]), 2),
                            'change': round(float(data.iloc[-1]) - float(data.iloc[-2]), 3)
                        }
                except Exception:
                    results[name] = {'latest': 0, 'previous': 0, 'change': 0}
            return results

        fred_data = fetch_fred_data()

    except Exception:
        # Demo mode
        fred_data = {
            "CPI": {'latest': 3.2, 'previous': 3.1, 'change': 0.1},
            "Fed Rate": {'latest': 5.50, 'previous': 5.50, 'change': 0.0},
            "US 10Y": {'latest': 4.26, 'previous': 4.22, 'change': 0.04},
            "Unemployment": {'latest': 4.1, 'previous': 4.0, 'change': 0.1},
            "GDP Growth": {'latest': 2.8, 'previous': 3.0, 'change': -0.2},
            "PCE": {'latest': 2.7, 'previous': 2.6, 'change': 0.1}
        }
        st.info("📡 Running in demo mode. Add FRED_API_KEY to secrets for live data.")

    # Gauge builder
    def build_gauge(name, value, prev_val, color, icon, impact_dxy, impact_gold, next_date):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={'font': {'size': 36, 'color': '#ffffff', 'family': 'Inter'}},
            gauge={
                'axis': {
                    'range': [min(value, prev_val) * 0.85, max(value, prev_val) * 1.15],
                    'tickcolor': '#333',
                    'tickfont': {'color': '#555', 'size': 10}
                },
                'bar': {'color': color, 'thickness': 0.3},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 0,
                'steps': [
                    {'range': [min(value, prev_val) * 0.85, prev_val], 'color': 'rgba(255,255,255,0.02)'},
                    {'range': [prev_val, max(value, prev_val) * 1.15], 'color': 'rgba(255,255,255,0.01)'}
                ],
                'threshold': {
                    'line': {'color': '#ffffff', 'width': 2},
                    'thickness': 0.8,
                    'value': prev_val
                }
            }
        ))
        fig.update_layout(
            height=220,
            margin=dict(l=25, r=25, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Inter'}
        )
        return fig

    # Layout: 3 columns x 2 rows
    macro_items = [
        ("CPI Inflation", "CPI", "#FF453A", "📈", "BULLISH", "BEARISH", "Feb 12, 2025"),
        ("Federal Funds Rate", "Fed Rate", "#007AFF", "🏛️", "BULLISH", "BEARISH", "Mar 19, 2025"),
        ("US 10Y Treasury", "US 10Y", "#d4af37", "📊", "BULLISH", "BEARISH", "Daily"),
        ("Unemployment Rate", "Unemployment", "#FF9F0A", "👥", "BEARISH", "BULLISH", "Feb 7, 2025"),
        ("GDP Growth Rate", "GDP Growth", "#30D158", "📈", "BULLISH", "BEARISH", "Feb 27, 2025"),
        ("PCE Price Index", "PCE", "#BF5AF2", "💰", "BULLISH", "BEARISH", "Feb 28, 2025"),
    ]

    for row_start in range(0, len(macro_items), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = row_start + i
            if idx < len(macro_items):
                title, key, color, icon, dxy_imp, gold_imp, next_dt = macro_items[idx]
                d = fred_data.get(key, {'latest': 0, 'previous': 0, 'change': 0})

                with col:
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 20px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;
                                        color: rgba(255,255,255,0.4); font-weight: 600;">
                                {icon} {title}
                            </span>
                            <span style="font-size: 10px; padding: 3px 10px; border-radius: 20px;
                                        background: {'rgba(48,209,88,0.1)' if d['change'] >= 0 else 'rgba(255,69,58,0.1)'};
                                        color: {'#30D158' if d['change'] >= 0 else '#FF453A'}; font-weight: 600;">
                                {'↑' if d['change'] >= 0 else '↓'} {abs(d['change'])}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    fig = build_gauge(title, d['latest'], d['previous'], color,
                                      icon, dxy_imp, gold_imp, next_dt)
                    st.plotly_chart(fig, use_container_width=True, key=f"gauge_{key}_{idx}")

                    # Impact badges
                    st.markdown(f"""
                    <div style="display: flex; justify-content: center; gap: 8px; margin-top: -15px; margin-bottom: 15px;">
                        <span style="font-size: 10px; padding: 4px 12px; border-radius: 20px;
                                    background: rgba(0,122,255,0.1); color: #007AFF; font-weight: 600;
                                    letter-spacing: 0.5px;">
                            DXY: {dxy_imp}
                        </span>
                        <span style="font-size: 10px; padding: 4px 12px; border-radius: 20px;
                                    background: rgba(212,175,55,0.1); color: #d4af37; font-weight: 600;
                                    letter-spacing: 0.5px;">
                            GOLD: {gold_imp}
                        </span>
                    </div>
                    <p style="text-align: center; font-size: 10px; color: rgba(255,255,255,0.2);
                              letter-spacing: 0.5px;">
                        📅 Next Release: {next_dt}
                    </p>
                    """, unsafe_allow_html=True)

    # === COT ANALYSIS SECTION ===
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: 30px 0 20px;">
        <p style="font-size: 10px; letter-spacing: 4px; text-transform: uppercase;
                  color: rgba(212,175,55,0.5); font-weight: 600; margin-bottom: 8px;">
            SMART MONEY
        </p>
        <h2 style="font-size: 28px; font-weight: 800; color: #ffffff; margin: 0;">
            COT <span class="gradient-text">Analysis</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    cot_left, cot_right = st.columns([1, 1.5])

    with cot_left:
        # Donut chart
        fig_cot = go.Figure(data=[go.Pie(
            values=[75, 25],
            hole=.78,
            direction='clockwise',
            sort=False,
            marker=dict(colors=['#d4af37', 'rgba(255,255,255,0.03)'],
                        line=dict(color='#000000', width=2)),
            textinfo='none',
            hoverinfo='none'
        )])
        fig_cot.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text="75%", x=0.5, y=0.55, font_size=48,
                     showarrow=False, font_family="Inter",
                     font_color="#d4af37", font_weight=800),
                dict(text="BULLISH", x=0.5, y=0.42, font_size=11,
                     showarrow=False, font_color="rgba(255,255,255,0.3)",
                     font_weight=700, font_family="Inter")
            ]
        )
        st.plotly_chart(fig_cot, use_container_width=True, key="cot_ring")

    with cot_right:
        st.markdown("""
        <div class="glass-card" style="margin-top: 10px;">
            <p style="font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
                      color: rgba(212,175,55,0.6); font-weight: 700; margin-bottom: 20px;">
                XAUUSD POSITIONING
            </p>
            <p style="color: rgba(255,255,255,0.5); font-size: 14px; line-height: 1.8; margin-bottom: 25px;">
                Commercial traders showing <strong style="color: #fff;">net long positioning</strong>.
                Smart Money is accumulating at key institutional zones.
                Strong rejection observed at 2000 psychological level.
            </p>
            <div style="display: flex; justify-content: space-around; text-align: center;
                        padding: 20px 0; border-top: 1px solid rgba(255,255,255,0.04);
                        border-bottom: 1px solid rgba(255,255,255,0.04);">
                <div>
                    <p style="font-size: 10px; letter-spacing: 1px; color: rgba(255,255,255,0.3);
                              text-transform: uppercase; margin-bottom: 5px;">Longs</p>
                    <p style="font-size: 22px; font-weight: 800; color: #30D158;">250K</p>
                </div>
                <div>
                    <p style="font-size: 10px; letter-spacing: 1px; color: rgba(255,255,255,0.3);
                              text-transform: uppercase; margin-bottom: 5px;">Shorts</p>
                    <p style="font-size: 22px; font-weight: 800; color: #FF453A;">50K</p>
                </div>
                <div>
                    <p style="font-size: 10px; letter-spacing: 1px; color: rgba(255,255,255,0.3);
                              text-transform: uppercase; margin-bottom: 5px;">Net</p>
                    <p style="font-size: 22px; font-weight: 800; color: #d4af37;">+200K</p>
                </div>
            </div>
            <div style="margin-top: 15px; text-align: center;">
                <span style="font-size: 10px; padding: 5px 15px; border-radius: 20px;
                            background: rgba(48,209,88,0.1); color: #30D158; font-weight: 700;
                            letter-spacing: 1px;">
                    ● INSTITUTIONAL BIAS: BULLISH
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# MAIN CONTROLLER
# ==========================================
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
    render_footer()

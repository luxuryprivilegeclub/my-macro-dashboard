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

# --- 2. MEGA PREMIUM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* === GLOBAL === */
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

    /* === HEADER BAR === */
    .header-bar {
        position: fixed; top: 0; left: 0; right: 0; z-index: 999999;
        height: 56px;
        background: rgba(0, 0, 0, 0.82);
        backdrop-filter: saturate(200%) blur(24px);
        -webkit-backdrop-filter: saturate(200%) blur(24px);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        display: flex; align-items: center; justify-content: center;
        padding: 0 30px;
    }
    .header-inner {
        max-width: 1400px; width: 100%;
        display: flex; align-items: center; justify-content: space-between;
    }
    .header-brand {
        display: flex; align-items: center; gap: 10px;
    }
    .header-brand img {
        width: 32px; height: 32px; border-radius: 50%;
        border: 1.5px solid rgba(212,175,55,0.5);
        object-fit: cover;
    }
    .header-brand-text {
        font-size: 14px; font-weight: 700; letter-spacing: 2px;
        color: #d4af37;
    }
    .header-nav {
        display: flex; align-items: center; gap: 4px;
    }
    .header-nav-link {
        color: rgba(255,255,255,0.55); font-size: 12.5px; font-weight: 500;
        padding: 7px 16px; border-radius: 8px;
        text-decoration: none; transition: all 0.25s ease; cursor: pointer;
        letter-spacing: 0.3px;
    }
    .header-nav-link:hover {
        color: #ffffff; background: rgba(255,255,255,0.06);
    }
    .header-nav-link.active {
        color: #d4af37; background: rgba(212,175,55,0.1);
    }
    .header-user {
        display: flex; align-items: center; gap: 10px;
    }
    .header-avatar {
        width: 28px; height: 28px; border-radius: 50%;
        background: linear-gradient(135deg, #d4af37, #8b6914);
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 800; color: #000;
    }
    .header-username {
        font-size: 12px; color: rgba(255,255,255,0.5); font-weight: 500;
    }

    /* === BUTTONS === */
    div.stButton > button {
        background: rgba(255,255,255,0.03) !important;
        color: rgba(255,255,255,0.7) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important; font-size: 13px !important;
        transition: all 0.3s cubic-bezier(0.25,0.46,0.45,0.94) !important;
        letter-spacing: 0.3px !important;
    }
    div.stButton > button:hover {
        background: rgba(212,175,55,0.1) !important;
        color: #d4af37 !important;
        border-color: rgba(212,175,55,0.25) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(212,175,55,0.08) !important;
    }
    div.stButton > button:active {
        transform: scale(0.98) !important;
    }
    .gold-btn > div > button {
        background: linear-gradient(135deg, #d4af37, #b8860b) !important;
        color: #000000 !important; border: none !important;
        font-weight: 700 !important; letter-spacing: 0.8px !important;
    }
    .gold-btn > div > button:hover {
        box-shadow: 0 8px 30px rgba(212,175,55,0.25) !important;
        color: #000 !important;
    }

    /* === INPUTS === */
    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important; color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important; padding: 14px 16px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 3px rgba(212,175,55,0.08) !important;
    }
    div[data-testid="stTextInput"] label {
        color: rgba(255,255,255,0.4) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important; font-size: 12px !important;
        letter-spacing: 0.5px !important;
    }

    /* === SELECTBOX === */
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important; color: white !important;
    }
    div[data-testid="stSelectbox"] label {
        color: rgba(255,255,255,0.4) !important; font-weight: 500 !important;
    }

    /* === TABS === */
    div[data-testid="stTabs"] button {
        color: rgba(255,255,255,0.4) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important; font-size: 13px !important;
        border-bottom: 2px solid transparent !important;
        padding: 12px 18px !important; background: transparent !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #d4af37 !important;
        border-bottom-color: #d4af37 !important;
    }

    /* === FILE UPLOADER === */
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.015) !important;
        border: 2px dashed rgba(212,175,55,0.15) !important;
        border-radius: 16px !important; padding: 25px !important;
    }
    div[data-testid="stFileUploader"] label {
        color: rgba(255,255,255,0.5) !important;
    }

    /* === DATE INPUT === */
    div[data-testid="stDateInput"] input {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important; color: white !important;
    }

    /* === METRIC === */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px; padding: 18px;
    }
    div[data-testid="stMetric"] label {
        color: rgba(255,255,255,0.3) !important;
        font-size: 11px !important; letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #d4af37 !important; font-weight: 700 !important;
    }

    /* === GLASS CARD === */
    .glass-card {
        background: rgba(255,255,255,0.025);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px; padding: 28px;
        transition: all 0.4s cubic-bezier(0.25,0.46,0.45,0.94);
        position: relative; overflow: hidden;
    }
    .glass-card::before {
        content: ''; position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent);
    }
    .glass-card:hover {
        border-color: rgba(212,175,55,0.15);
        transform: translateY(-3px);
        box-shadow: 0 16px 48px rgba(212,175,55,0.06);
    }

    /* === GRADIENT TEXT === */
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

    /* === GLOW RING === */
    .glow-ring {
        border-radius: 50%;
        border: 2.5px solid #d4af37;
        box-shadow: 0 0 12px rgba(212,175,55,0.25),
                    0 0 30px rgba(212,175,55,0.1),
                    0 0 50px rgba(212,175,55,0.04);
    }

    /* === PULSE DOT === */
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(48,209,88,0.4); }
        50% { box-shadow: 0 0 0 8px rgba(48,209,88,0); }
    }
    .pulse-dot {
        width: 7px; height: 7px; background: #30d158;
        border-radius: 50%; display: inline-block;
        animation: pulse-glow 2s infinite;
    }

    /* === FLOAT === */
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    .float-anim { animation: float 5s ease-in-out infinite; }

    /* === HR === */
    hr {
        border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent) !important;
        margin: 35px 0 !important;
    }

    /* === PREMIUM FOOTER === */
    .premium-footer {
        margin-top: 100px;
        padding: 60px 20px 40px;
        border-top: 1px solid rgba(255,255,255,0.04);
        text-align: center;
        position: relative;
    }
    .premium-footer::before {
        content: '';
        position: absolute; top: -80px; left: 50%;
        transform: translateX(-50%);
        width: 500px; height: 160px;
        background: radial-gradient(ellipse, rgba(212,175,55,0.03) 0%, transparent 70%);
        pointer-events: none;
    }
    .footer-links {
        display: flex; justify-content: center; gap: 30px;
        margin: 20px 0 30px; flex-wrap: wrap;
    }
    .footer-link {
        color: rgba(255,255,255,0.3); font-size: 12px;
        font-weight: 500; text-decoration: none;
        transition: color 0.3s ease; cursor: pointer;
        letter-spacing: 0.5px;
    }
    .footer-link:hover { color: #d4af37; }
    .footer-divider {
        width: 60px; height: 1px; margin: 25px auto;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);
    }
    .footer-disclaimer {
        max-width: 650px; margin: 0 auto;
        font-size: 10.5px; line-height: 1.9;
        color: rgba(255,255,255,0.15);
    }
    .footer-copy {
        margin-top: 30px; font-size: 10px;
        color: rgba(255,255,255,0.08); letter-spacing: 2px;
    }

    /* === HERO PARTICLES === */
    .hero-bg {
        position: relative; overflow: hidden;
    }
    .hero-bg::before {
        content: '';
        position: absolute; top: -20%; left: 50%;
        transform: translateX(-50%);
        width: 800px; height: 800px;
        background: radial-gradient(circle,
            rgba(212,175,55,0.06) 0%,
            rgba(212,175,55,0.02) 30%,
            transparent 70%);
        pointer-events: none;
    }
    .hero-bg::after {
        content: '';
        position: absolute; bottom: -40%; right: -10%;
        width: 500px; height: 500px;
        background: radial-gradient(circle,
            rgba(212,175,55,0.03) 0%,
            transparent 70%);
        pointer-events: none;
    }

    /* === FEATURE ICON BOX === */
    .feature-icon {
        width: 52px; height: 52px; border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 14px; font-size: 24px;
    }

    /* === LIVE TICKER BAR === */
    .ticker-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px; padding: 16px 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .ticker-card:hover {
        border-color: rgba(212,175,55,0.15);
        background: rgba(255,255,255,0.03);
    }
    .ticker-symbol {
        font-size: 11px; font-weight: 700;
        letter-spacing: 1.5px; text-transform: uppercase;
        color: rgba(255,255,255,0.4); margin-bottom: 4px;
    }
    .ticker-price {
        font-size: 22px; font-weight: 800; color: #fff;
        font-family: 'JetBrains Mono', monospace;
    }
    .ticker-change-up {
        font-size: 12px; font-weight: 600; color: #30d158;
        margin-top: 4px;
    }
    .ticker-change-down {
        font-size: 12px; font-weight: 600; color: #ff453a;
        margin-top: 4px;
    }

    /* === SECTION HEADER === */
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
        text-align: center; font-weight: 400; margin-bottom: 35px;
    }

    /* Hidden anchor links */
    h1 a, h2 a, h3 a { display: none !important; }

    /* Responsive */
    @media (max-width: 768px) {
        .header-bar { padding: 0 12px; }
        .glass-card { padding: 18px; border-radius: 16px; }
        .footer-links { gap: 15px; }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GLOBAL VARIABLES ---
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60"

# --- DEFAULT REPORT HTML ---
DEFAULT_REPORT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    :root{--gold:#D4AF37;--bg:#000;--card:rgba(255,255,255,0.03);--text:#FFF;--red:#FF453A;--green:#30D158;}
    body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;}
    .main-container{max-width:1000px;margin:0 auto;padding:30px 20px;}
    .hero-section{text-align:center;padding:60px 20px;position:relative;}
    .hero-section::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;background:radial-gradient(circle,rgba(212,175,55,0.08)0%,transparent 70%);pointer-events:none;}
    .hero-eyebrow{font-size:12px;letter-spacing:4px;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:15px;}
    .hero-title{font-size:48px;font-weight:800;background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px;line-height:1.1;}
    .hero-subtitle{font-size:16px;color:rgba(255,255,255,0.4);font-weight:400;}
    .section{margin-bottom:30px;padding:30px;background:var(--card);border-radius:24px;border:1px solid rgba(255,255,255,0.06);position:relative;overflow:hidden;}
    .section::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.2),transparent);}
    .section-header{font-size:13px;font-weight:700;color:var(--gold);letter-spacing:2px;text-transform:uppercase;margin-bottom:25px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.04);}
    .stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:15px;}
    .stat-card{background:rgba(255,255,255,0.02);padding:20px 15px;border-radius:16px;border:1px solid rgba(255,255,255,0.04);text-align:center;transition:all 0.3s ease;}
    .stat-card:hover{border-color:rgba(212,175,55,0.2);transform:translateY(-2px);}
    .stat-label{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}
    .stat-value{font-size:28px;font-weight:800;color:var(--gold);font-family:'JetBrains Mono',monospace;}
    .logic-box{background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);padding:20px;border-radius:16px;margin-top:20px;font-size:14px;line-height:1.7;color:rgba(255,255,255,0.7);}
    .logic-box strong{color:#fff;}
    .scenario-card{background:rgba(255,255,255,0.02);padding:25px;border-radius:20px;border:1px solid rgba(255,255,255,0.04);margin-bottom:15px;border-left:3px solid var(--gold);transition:all 0.3s ease;}
    .scenario-card:hover{background:rgba(255,255,255,0.04);}
    .scenario-title{font-size:16px;font-weight:700;margin-bottom:8px;color:#fff;}
    .scenario-card p{color:rgba(255,255,255,0.5);font-size:14px;line-height:1.6;}
    .bottom-line{text-align:center;padding:40px;background:rgba(212,175,55,0.03);border-radius:24px;border:1px solid rgba(212,175,55,0.15);}
    .bottom-line h3{font-size:28px;font-weight:800;margin-bottom:10px;background:linear-gradient(135deg,#d4af37,#f5d769);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .bottom-line p{color:rgba(255,255,255,0.5);font-size:15px;}
    .bottom-line strong{color:#fff;}
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
        <div class="logic-box"><strong>Logic:</strong> Price DOWN + OI UP = 🔴 <strong>SHORT BUILDUP</strong>. Smart Money is adding fresh shorts.</div>
    </section>
    <section class="section">
        <div class="section-header">🎯 Trade Scenarios</div>
        <div class="scenario-card"><div class="scenario-title">Scenario A: Sell the Rally (70% Prob)</div><p>If price tests <strong>5269–5311</strong> zone, SHORT entry. Target: 5020.</p></div>
        <div class="scenario-card" style="border-left-color:#FF453A;"><div class="scenario-title">Scenario B: Continuation Short</div><p>Break below <strong>5036</strong> → Direct fall to 4979.</p></div>
    </section>
    <section class="bottom-line">
        <h3>🎯 VERDICT: BEARISH</h3>
        <p>Smart Money is actively building shorts. <strong>Best Trade:</strong> Short rallies into 5280 zone targeting 5020.</p>
    </section>
</div>
</body>
</html>
"""

# --- CALCULATOR HTML ---
CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:transparent;display:flex;justify-content:center;align-items:center;padding:30px;font-family:'Inter',sans-serif;}
    .calc-container{background:rgba(255,255,255,0.03);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.06);border-radius:28px;padding:40px;width:100%;max-width:480px;position:relative;overflow:hidden;}
    .calc-container::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.3),transparent);}
    .calc-eyebrow{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.6);font-weight:600;text-align:center;margin-bottom:8px;}
    .calc-title{font-size:28px;font-weight:800;text-align:center;background:linear-gradient(135deg,#d4af37,#f5d769);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:35px;}
    .input-group{margin-bottom:22px;}
    .input-group label{display:block;margin-bottom:8px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.35);}
    .input-group input{width:100%;padding:16px 20px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;color:#fff;font-size:16px;font-family:'Inter',sans-serif;font-weight:500;outline:none;transition:all 0.3s ease;}
    .input-group input:focus{border-color:rgba(212,175,55,0.5);box-shadow:0 0 0 4px rgba(212,175,55,0.08);}
    .input-group input::placeholder{color:rgba(255,255,255,0.15);}
    .calc-btn{width:100%;padding:18px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#000;border:none;border-radius:16px;font-size:15px;font-weight:700;letter-spacing:1px;cursor:pointer;margin-top:15px;transition:all 0.3s ease;text-transform:uppercase;}
    .calc-btn:hover{box-shadow:0 8px 40px rgba(212,175,55,0.3);transform:translateY(-2px);}
    .calc-btn:active{transform:scale(0.98);}
    #result{margin-top:30px;text-align:center;display:none;padding:30px;border-radius:20px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);}
    #result .result-label{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}
    #result .result-value{font-size:48px;font-weight:800;background:linear-gradient(135deg,#d4af37,#f5d769);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    #result .result-risk{font-size:13px;color:rgba(255,255,255,0.3);margin-top:8px;}
</style>
</head>
<body>
<div class="calc-container">
    <p class="calc-eyebrow">Risk Management</p>
    <h1 class="calc-title">Position Sizer</h1>
    <div class="input-group"><label>Account Balance</label><input type="number" id="accountSize" placeholder="$10,000"></div>
    <div class="input-group"><label>Risk Per Trade (%)</label><input type="number" id="riskPercent" placeholder="2.0"></div>
    <div class="input-group"><label>Stop Loss (Pips)</label><input type="number" id="stopLoss" placeholder="50"></div>
    <button class="calc-btn" onclick="calculateLotSize()">Calculate Position</button>
    <div id="result">
        <p class="result-label">Recommended Lot Size</p>
        <p class="result-value" id="lotValue">—</p>
        <p class="result-risk" id="riskAmt"></p>
    </div>
</div>
<script>
function calculateLotSize(){
    const acc=parseFloat(document.getElementById('accountSize').value);
    const risk=parseFloat(document.getElementById('riskPercent').value);
    const sl=parseFloat(document.getElementById('stopLoss').value);
    if(!acc||!risk||!sl)return;
    const riskAmt=(acc*risk/100);
    const lots=(riskAmt/(sl*10)).toFixed(2);
    document.getElementById('lotValue').textContent=lots+' Lot';
    document.getElementById('riskAmt').textContent='Risk Amount: $'+riskAmt.toFixed(2);
    const r=document.getElementById('result');r.style.display='block';
}
</script>
</body>
</html>
"""

# --- LIVE CHART WIDGET HTML ---
def get_tradingview_widget(symbol, name):
    return f"""
    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
                border-radius: 18px; overflow: hidden; height: 320px; position: relative;">
        <div style="padding: 14px 18px 0; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p style="font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
                          color: rgba(255,255,255,0.3); text-transform: uppercase; margin: 0;">{name}</p>
            </div>
            <div style="display: flex; align-items: center; gap: 5px;">
                <span style="width: 6px; height: 6px; background: #30d158; border-radius: 50%;
                             display: inline-block; animation: pulse-glow 2s infinite;"></span>
                <span style="font-size: 9px; color: rgba(255,255,255,0.25); font-weight: 500;">LIVE</span>
            </div>
        </div>
        <!-- TradingView Widget -->
        <div class="tradingview-widget-container" style="height: 270px; margin-top: 5px;">
            <div id="tv-widget-{symbol}"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.MediumWidget({{
                "symbols": [["{symbol}|1M"]],
                "chartOnly": true,
                "width": "100%",
                "height": "100%",
                "locale": "en",
                "colorTheme": "dark",
                "autosize": true,
                "showVolume": false,
                "hideDateRanges": true,
                "hideMarketStatus": true,
                "hideSymbolLogo": true,
                "scalePosition": "no",
                "scaleMode": "Normal",
                "fontFamily": "Inter, sans-serif",
                "fontSize": "10",
                "noTimeScale": false,
                "chartType": "area",
                "gridLineColor": "rgba(255,255,255,0.02)",
                "fontColor": "rgba(255,255,255,0.3)",
                "lineColor": "#d4af37",
                "topColor": "rgba(212,175,55,0.15)",
                "bottomColor": "rgba(212,175,55,0.0)",
                "lineWidth": 2,
                "container_id": "tv-widget-{symbol}"
            }});
            </script>
        </div>
    </div>
    """

# Simple mini chart fallback using plotly
def render_mini_chart(name, symbol_label, prices, color="#d4af37"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=prices, mode='lines',
        line=dict(color=color, width=2.5, shape='spline'),
        fill='tozeroy',
        fillcolor=f'rgba({",".join([str(int(color.lstrip("#")[i:i+2], 16)) for i in (0,2,4)])},0.06)',
        hoverinfo='y'
    ))
    fig.update_layout(
        height=180, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
        showlegend=False
    )
    return fig


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
    st.session_state['users_db'] = pd.DataFrame({
        "Username": ["admin", "user"],
        "Password": ["Rollic@786", "123"],
        "Role": ["Admin", "User"],
        "Status": ["Active", "Active"]
    })
if 'html_reports' not in st.session_state:
    st.session_state['html_reports'] = {
        datetime.now().strftime("%Y-%m-%d"): DEFAULT_REPORT_HTML
    }


# ==========================================
# HEADER WITH EMBEDDED MENU
# ==========================================
def render_header():
    st.markdown('<div style="height: 65px;"></div>', unsafe_allow_html=True)
    user_initial = st.session_state['username'][0].upper() if st.session_state['username'] else "U"
    current = st.session_state['current_page']

    st.markdown(f"""
    <div class="header-bar">
        <div class="header-inner">
            <div class="header-brand">
                <img src="{LOGO_URL}" alt="Logo">
                <span class="header-brand-text">ROLLIC TRADES</span>
            </div>
            <div class="header-user">
                <span class="header-username">{st.session_state['username']}</span>
                <div class="header-avatar">{user_initial}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Menu buttons inside header area
    menu_items = ["home", "macro", "reports", "calculator"]
    menu_labels = {
        "home": "🏠 Home",
        "macro": "📊 Macro",
        "reports": "📄 Reports",
        "calculator": "🧮 Calculator",
        "admin": "⚙️ Admin"
    }

    if st.session_state['user_role'] == 'Admin':
        menu_items.append("admin")

    total_cols = len(menu_items) + 1  # +1 for logout
    cols = st.columns(total_cols)

    for i, item in enumerate(menu_items):
        with cols[i]:
            label = menu_labels[item]
            if st.button(label, use_container_width=True, key=f"hdr_{item}"):
                st.session_state['current_page'] = item
                st.rerun()

    with cols[-1]:
        if st.button("↗ Sign Out", use_container_width=True, key="hdr_logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# ELEGANT FOOTER WITH PAGE LINKS
# ==========================================
def render_footer():
    st.markdown(f"""
    <div class="premium-footer">
        <div style="margin-bottom: 15px;">
            <img src="{LOGO_URL}" width="44" height="44"
                 style="border-radius: 50%; object-fit: cover;
                        border: 2px solid rgba(212,175,55,0.3);
                        box-shadow: 0 0 20px rgba(212,175,55,0.1);">
        </div>
        <p style="font-size: 13px; font-weight: 700; letter-spacing: 3px;
                  color: rgba(212,175,55,0.4); margin-bottom: 5px;">
            ROLLIC TRADES
        </p>
        <p style="font-size: 11px; color: rgba(255,255,255,0.15); font-weight: 400;">
            Smart Money Intelligence Platform
        </p>

        <div class="footer-links">
            <span class="footer-link">Home</span>
            <span class="footer-link">Macro Terminal</span>
            <span class="footer-link">Daily Reports</span>
            <span class="footer-link">Risk Calculator</span>
            <span class="footer-link">Academy</span>
        </div>

        <div class="footer-divider"></div>

        <p class="footer-disclaimer">
            <strong style="color: rgba(255,255,255,0.25);">Risk Disclaimer</strong><br>
            Trading foreign exchange, gold, and indices on margin carries a high level of risk
            and may not be suitable for all investors. The analysis provided is for educational
            and informational purposes only and does not constitute financial advice.
            Past performance is not indicative of future results. Trade responsibly.
        </p>

        <div class="footer-divider"></div>

        <div style="display: flex; justify-content: center; gap: 25px; margin-bottom: 20px;">
            <span style="font-size: 10px; color: rgba(255,255,255,0.12); letter-spacing: 1px;">Privacy Policy</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.06);">|</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.12); letter-spacing: 1px;">Terms of Service</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.06);">|</span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.12); letter-spacing: 1px;">Contact</span>
        </div>

        <p class="footer-copy">© 2026 ROLLIC TRADES · ALL RIGHTS RESERVED</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE: LOGIN
# ==========================================
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
        <div style="position: absolute; bottom: 10%; right: 10%;
                    width: 400px; height: 400px; border-radius: 50%;
                    background: radial-gradient(circle,
                        rgba(212,175,55,0.03) 0%, transparent 65%);
                    filter: blur(40px);"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;" class="float-anim">
            <img src="{LOGO_URL}" width="110" height="110"
                 style="border-radius: 50%; object-fit: cover;" class="glow-ring">
        </div>
        <div style="text-align: center; margin-bottom: 8px;">
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

        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

        username = st.text_input("USERNAME", placeholder="Enter username", key="login_user")
        password = st.text_input("PASSWORD", placeholder="Enter password", type="password", key="login_pass")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

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
                    st.error("Account suspended.")
            else:
                st.error("Invalid credentials")

        st.markdown("""
        <div style="text-align: center; margin-top: 25px;">
            <span class="pulse-dot"></span>
            <span style="color: rgba(255,255,255,0.15); font-size: 10px;
                        margin-left: 6px; font-weight: 500;">
                Encrypted Connection
            </span>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE: HOME — ULTRA PREMIUM
# ==========================================
def home_page():
    import random

    # === HERO SECTION ===
    st.markdown(f"""
    <div class="hero-bg" style="text-align: center; padding: 50px 0 30px; position: relative;">
        <div style="margin-bottom: 18px;" class="float-anim">
            <img src="{LOGO_URL}" width="90" height="90"
                 style="border-radius: 50%; object-fit: cover;" class="glow-ring">
        </div>
        <p style="font-size: 9px; letter-spacing: 5px; text-transform: uppercase;
                  color: rgba(212,175,55,0.4); font-weight: 600; margin-bottom: 6px;">
            WELCOME BACK
        </p>
        <h1 style="font-size: 42px; font-weight: 800; color: #fff; margin: 0; line-height: 1.15;">
            {st.session_state['username'].title()},
            <span class="gradient-text">let's trade.</span>
        </h1>
        <p style="color: rgba(255,255,255,0.2); font-size: 13px; margin-top: 8px; font-weight: 400;">
            {st.session_state['user_role']} · {datetime.now().strftime("%A, %B %d, %Y")}
        </p>
        <div style="margin-top: 18px; display: flex; justify-content: center; align-items: center; gap: 8px;">
            <span class="pulse-dot"></span>
            <span style="font-size: 10px; color: rgba(255,255,255,0.2); font-weight: 500;
                        letter-spacing: 0.5px;">Markets Open</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # === LIVE PRICE TICKER CARDS ===
    st.markdown("""
    <p class="section-eyebrow">LIVE MARKETS</p>
    <p class="section-title">Market <span class="gradient-text">Overview</span></p>
    <p class="section-subtitle">Real-time institutional price feed</p>
    """, unsafe_allow_html=True)

    # Market data with mini charts
    markets = [
        {"name": "XAUUSD", "label": "Gold", "price": "3,312.45", "change": "+0.54%", "up": True,
         "color": "#d4af37", "data": [3280, 3290, 3285, 3300, 3295, 3310, 3305, 3312, 3308, 3315, 3312]},
        {"name": "EURUSD", "label": "EUR/USD", "price": "1.1382", "change": "+0.18%", "up": True,
         "color": "#007AFF", "data": [1.130, 1.132, 1.131, 1.134, 1.133, 1.136, 1.135, 1.137, 1.136, 1.138, 1.138]},
        {"name": "SP500", "label": "S&P 500", "price": "5,525.21", "change": "-0.32%", "up": False,
         "color": "#30D158", "data": [5550, 5545, 5548, 5540, 5535, 5530, 5528, 5532, 5525, 5520, 5525]},
        {"name": "BTCUSD", "label": "Bitcoin", "price": "94,250", "change": "+1.24%", "up": True,
         "color": "#FF9F0A", "data": [92000, 92500, 93000, 92800, 93200, 93500, 93800, 94000, 93900, 94100, 94250]}
    ]

    mc1, mc2, mc3, mc4 = st.columns(4)
    for col, m in zip([mc1, mc2, mc3, mc4], markets):
        with col:
            st.markdown(f"""
            <div class="ticker-card">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <p class="ticker-symbol">{m['name']}</p>
                    <div style="display: flex; align-items: center; gap: 4px;">
                        <span style="width: 5px; height: 5px; background: {'#30d158' if m['up'] else '#ff453a'};
                                    border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 9px; color: rgba(255,255,255,0.2);">LIVE</span>
                    </div>
                </div>
                <p class="ticker-price">{m['price']}</p>
                <p class="{'ticker-change-up' if m['up'] else 'ticker-change-down'}">
                    {'▲' if m['up'] else '▼'} {m['change']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            fig = render_mini_chart(m['name'], m['label'], m['data'], m['color'])
            st.plotly_chart(fig, use_container_width=True, key=f"mini_{m['name']}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # === FEATURE CARDS SECTION ===
    st.markdown("""
    <p class="section-eyebrow">TRADING SUITE</p>
    <p class="section-title">Your <span class="gradient-text">Toolkit</span></p>
    <p class="section-subtitle">Everything you need for institutional-grade trading</p>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 260px;">
            <div class="feature-icon" style="background: rgba(212,175,55,0.08);">📄</div>
            <p style="color: #fff; font-size: 17px; font-weight: 700; margin-bottom: 8px;">
                Daily Reports
            </p>
            <p style="color: rgba(255,255,255,0.25); font-size: 12.5px; line-height: 1.7; margin-bottom: 18px;">
                Expert institutional analysis with trade scenarios, liquidity maps, and Smart Money decode.
            </p>
            <div style="display: flex; justify-content: center; gap: 8px;">
                <span style="font-size: 9px; padding: 4px 10px; border-radius: 20px;
                            background: rgba(48,209,88,0.08); color: #30d158;
                            font-weight: 600; letter-spacing: 0.5px;">UPDATED DAILY</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Reports →", use_container_width=True, key="hm_reports"):
            st.session_state['current_page'] = 'reports'
            st.rerun()

    with f2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 260px;">
            <div class="feature-icon" style="background: rgba(0,122,255,0.08);">📊</div>
            <p style="color: #fff; font-size: 17px; font-weight: 700; margin-bottom: 8px;">
                Macro Terminal
            </p>
            <p style="color: rgba(255,255,255,0.25); font-size: 12.5px; line-height: 1.7; margin-bottom: 18px;">
                Real-time economic indicators, yield curves, COT analysis, and Fed policy tracking.
            </p>
            <div style="display: flex; justify-content: center; gap: 8px;">
                <span style="font-size: 9px; padding: 4px 10px; border-radius: 20px;
                            background: rgba(0,122,255,0.08); color: #007AFF;
                            font-weight: 600; letter-spacing: 0.5px;">LIVE DATA</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Terminal →", use_container_width=True, key="hm_macro"):
            st.session_state['current_page'] = 'macro'
            st.rerun()

    with f3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 260px;">
            <div class="feature-icon" style="background: rgba(191,90,242,0.08);">🧮</div>
            <p style="color: #fff; font-size: 17px; font-weight: 700; margin-bottom: 8px;">
                Risk Calculator
            </p>
            <p style="color: rgba(255,255,255,0.25); font-size: 12.5px; line-height: 1.7; margin-bottom: 18px;">
                Precision position sizing with risk-adjusted lot calculations for every trade setup.
            </p>
            <div style="display: flex; justify-content: center; gap: 8px;">
                <span style="font-size: 9px; padding: 4px 10px; border-radius: 20px;
                            background: rgba(191,90,242,0.08); color: #BF5AF2;
                            font-weight: 600; letter-spacing: 0.5px;">TOOL</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate →", use_container_width=True, key="hm_calc"):
            st.session_state['current_page'] = 'calculator'
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # === LATEST REPORT PREVIEW ===
    st.markdown("""
    <p class="section-eyebrow">LATEST INTELLIGENCE</p>
    <p class="section-title">Today's <span class="gradient-text">Report</span></p>
    <p class="section-subtitle">Most recent institutional analysis available</p>
    """, unsafe_allow_html=True)

    dates = sorted(st.session_state['html_reports'].keys(), reverse=True)
    if dates:
        latest = dates[0]
        st.markdown(f"""
        <div class="glass-card" style="padding: 30px;">
            <div style="display: flex; align-items: center; justify-content: space-between;
                        margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 12px;
                                background: rgba(212,175,55,0.08);
                                display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 20px;">📄</span>
                    </div>
                    <div>
                        <p style="color: #fff; font-size: 15px; font-weight: 700; margin: 0;">
                            Gold Institutional Analysis
                        </p>
                        <p style="color: rgba(255,255,255,0.25); font-size: 11px; margin: 0;">
                            Published: {latest}
                        </p>
                    </div>
                </div>
                <span style="font-size: 9px; padding: 5px 12px; border-radius: 20px;
                            background: rgba(48,209,88,0.08); color: #30d158;
                            font-weight: 700; letter-spacing: 1px;">NEW</span>
            </div>
            <p style="color: rgba(255,255,255,0.3); font-size: 13px; line-height: 1.7;">
                Smart Money positioning decoded with futures data, COT analysis, and key
                trade scenarios for the current session. Click below to read the full report.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Read Full Report →", use_container_width=True, key="hm_read"):
            st.session_state['current_page'] = 'reports'
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
        st.metric("Platform Version", "3.0")
    with s4:
        st.metric("Uptime", "99.9%")


# ==========================================
# PAGE: CALCULATOR
# ==========================================
def calculator_page():
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <p class="section-eyebrow">RISK MANAGEMENT</p>
        <p class="section-title">Position <span class="gradient-text">Calculator</span></p>
        <p class="section-subtitle">Calculate optimal lot sizes for risk-adjusted entries</p>
    </div>
    """, unsafe_allow_html=True)
    components.html(CALCULATOR_HTML, height=700, scrolling=False)


# ==========================================
# PAGE: ADMIN PANEL
# ==========================================
def admin_panel():
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <p class="section-eyebrow">SYSTEM CONTROL</p>
        <p class="section-title">Admin <span class="gradient-text">Console</span></p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄  Report Manager", "👥  Users", "📊  System"])

    with tab1:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 35px;">
            <span style="font-size: 36px;">📄</span>
            <h3 style="color: #fff; margin-top: 12px; margin-bottom: 4px; font-size: 18px;">Upload Report</h3>
            <p style="color: rgba(255,255,255,0.25); font-size: 12px;">
                Upload HTML analysis — rendered exactly as designed.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            uploaded_file = st.file_uploader("HTML File", type=['html'], label_visibility="collapsed")
        with c2:
            report_date = st.date_input("Report Date", datetime.now())

        st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
        if st.button("PUBLISH REPORT →", use_container_width=True, key="pub_btn"):
            if uploaded_file:
                html_string = uploaded_file.getvalue().decode("utf-8")
                date_key = report_date.strftime("%Y-%m-%d")
                st.session_state['html_reports'][date_key] = html_string
                st.success(f"✅ Published for {date_key}")
            else:
                st.error("Select an HTML file.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("#### Published Reports")
        for dk in sorted(st.session_state['html_reports'].keys(), reverse=True):
            rc1, rc2 = st.columns([5, 1])
            with rc1:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
                            border-radius: 12px; padding: 12px 18px; margin-bottom: 6px;
                            display: flex; align-items: center; gap: 10px;">
                    <span style="color: #d4af37;">📄</span>
                    <div>
                        <p style="color: #fff; font-size: 13px; font-weight: 600; margin: 0;">{dk}</p>
                        <p style="color: rgba(255,255,255,0.2); font-size: 10px; margin: 0;">HTML Report</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with rc2:
                if st.button("🗑️", key=f"del_{dk}"):
                    del st.session_state['html_reports'][dk]
                    st.rerun()

    with tab2:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.dataframe(st.session_state['users_db'], use_container_width=True, hide_index=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("#### ➕ Add User")
        ac1, ac2, ac3, ac4 = st.columns([2, 2, 1, 1])
        with ac1:
            new_user = st.text_input("Username", key="nu", placeholder="username")
        with ac2:
            new_pass = st.text_input("Password", key="np", placeholder="password", type="password")
        with ac3:
            new_role = st.selectbox("Role", ["User", "Admin"], key="nr")
        with ac4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Add ✓", key="add_u", use_container_width=True):
                if new_user and new_pass:
                    new_row = pd.DataFrame({"Username": [new_user], "Password": [new_pass],
                                            "Role": [new_role], "Status": ["Active"]})
                    st.session_state['users_db'] = pd.concat(
                        [st.session_state['users_db'], new_row], ignore_index=True)
                    st.success(f"Added '{new_user}'")
                    st.rerun()

    with tab3:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        i1, i2, i3 = st.columns(3)
        with i1:
            st.metric("Users", len(st.session_state['users_db']))
        with i2:
            st.metric("Reports", len(st.session_state['html_reports']))
        with i3:
            st.metric("Version", "3.0.0")


# ==========================================
# PAGE: REPORTS
# ==========================================
def reports_page():
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0 10px;">
        <div style="margin-bottom: 12px;">
            <img src="{LOGO_URL}" width="60" height="60"
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
            sel_date = st.selectbox("📅 Select", dates, label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)

        if sel_date:
            components.html(st.session_state['html_reports'][sel_date], height=1500, scrolling=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <span style="font-size: 50px; opacity: 0.2;">📄</span>
            <h3 style="color: rgba(255,255,255,0.2); margin-top: 12px;">No Reports</h3>
            <p style="color: rgba(255,255,255,0.1); font-size: 13px;">
                Upload from Admin Console.</p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE: MACRO DASHBOARD
# ==========================================
def macro_dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <p class="section-eyebrow">INSTITUTIONAL GRADE</p>
        <p class="section-title">Macro <span class="gradient-text">Terminal</span></p>
        <p class="section-subtitle">Economic intelligence & Smart Money positioning</p>
    </div>
    """, unsafe_allow_html=True)

    # FRED
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
                except:
                    results[name] = {'latest': 0, 'previous': 0, 'change': 0}
            return results
        fred_data = fetch_fred()
    except:
        fred_data = {
            "CPI": {'latest': 3.2, 'previous': 3.1, 'change': 0.1},
            "Fed Rate": {'latest': 5.50, 'previous': 5.50, 'change': 0.0},
            "US 10Y": {'latest': 4.26, 'previous': 4.22, 'change': 0.04},
            "Unemployment": {'latest': 4.1, 'previous': 4.0, 'change': 0.1},
            "GDP Growth": {'latest': 2.8, 'previous': 3.0, 'change': -0.2},
            "PCE": {'latest': 2.7, 'previous': 2.6, 'change': 0.1}
        }
        st.info("📡 Demo mode — add FRED_API_KEY for live data.")

    def build_gauge(value, prev_val, color):
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=value,
            number={'font': {'size': 32, 'color': '#fff', 'family': 'Inter'}},
            gauge={'axis': {'range': [min(value, prev_val)*0.85, max(value, prev_val)*1.15],
                            'tickcolor': '#222', 'tickfont': {'color': '#444', 'size': 9}},
                   'bar': {'color': color, 'thickness': 0.3},
                   'bgcolor': 'rgba(0,0,0,0)', 'borderwidth': 0,
                   'steps': [{'range': [min(value, prev_val)*0.85, prev_val],
                              'color': 'rgba(255,255,255,0.015)'}],
                   'threshold': {'line': {'color': '#fff', 'width': 1.5},
                                 'thickness': 0.75, 'value': prev_val}}
        ))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=25, b=0),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    items = [
        ("CPI Inflation", "CPI", "#FF453A", "📈", "BULLISH", "BEARISH", "Feb 12"),
        ("Federal Funds Rate", "Fed Rate", "#007AFF", "🏛️", "BULLISH", "BEARISH", "Mar 19"),
        ("US 10Y Treasury", "US 10Y", "#d4af37", "📊", "BULLISH", "BEARISH", "Daily"),
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
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 18px;">
                        <div style="display: flex; align-items: center; justify-content: space-between;
                                    margin-bottom: 3px;">
                            <span style="font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase;
                                        color: rgba(255,255,255,0.35); font-weight: 600;">
                                {icon} {title}
                            </span>
                            <span style="font-size: 9px; padding: 3px 8px; border-radius: 12px;
                                        background: {'rgba(48,209,88,0.08)' if d['change']>=0 else 'rgba(255,69,58,0.08)'};
                                        color: {'#30D158' if d['change']>=0 else '#FF453A'}; font-weight: 600;">
                                {'↑' if d['change']>=0 else '↓'} {abs(d['change'])}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.plotly_chart(build_gauge(d['latest'], d['previous'], color),
                                   use_container_width=True, key=f"g_{key}_{idx}")

                    st.markdown(f"""
                    <div style="display: flex; justify-content: center; gap: 6px;
                                margin-top: -12px; margin-bottom: 12px;">
                        <span style="font-size: 9px; padding: 3px 10px; border-radius: 14px;
                                    background: rgba(0,122,255,0.08); color: #007AFF;
                                    font-weight: 600;">DXY: {dxy}</span>
                        <span style="font-size: 9px; padding: 3px 10px; border-radius: 14px;
                                    background: rgba(212,175,55,0.08); color: #d4af37;
                                    font-weight: 600;">GOLD: {gold}</span>
                    </div>
                    <p style="text-align: center; font-size: 9px;
                              color: rgba(255,255,255,0.15);">📅 Next: {nxt}</p>
                    """, unsafe_allow_html=True)

    # === COT ===
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p class="section-eyebrow">SMART MONEY</p>
    <p class="section-title">COT <span class="gradient-text">Analysis</span></p>
    """, unsafe_allow_html=True)

    cl, cr = st.columns([1, 1.5])
    with cl:
        fig_cot = go.Figure(data=[go.Pie(
            values=[75, 25], hole=.78, direction='clockwise', sort=False,
            marker=dict(colors=['#d4af37', 'rgba(255,255,255,0.02)'],
                        line=dict(color='#000', width=2)),
            textinfo='none', hoverinfo='none'
        )])
        fig_cot.update_layout(
            showlegend=False, margin=dict(t=15, b=15, l=15, r=15), height=300,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text="75%", x=0.5, y=0.55, font_size=44, showarrow=False,
                     font_family="Inter", font_color="#d4af37"),
                dict(text="BULLISH", x=0.5, y=0.42, font_size=10, showarrow=False,
                     font_color="rgba(255,255,255,0.25)")]
        )
        st.plotly_chart(fig_cot, use_container_width=True, key="cot_r")

    with cr:
        st.markdown("""
        <div class="glass-card" style="margin-top: 8px;">
            <p style="font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
                      color: rgba(212,175,55,0.5); font-weight: 700; margin-bottom: 16px;">
                XAUUSD POSITIONING
            </p>
            <p style="color: rgba(255,255,255,0.4); font-size: 13px; line-height: 1.8; margin-bottom: 20px;">
                Commercial traders showing <strong style="color: #fff;">net long positioning</strong>.
                Smart Money accumulating at institutional zones. Strong rejection at 2000 level.
            </p>
            <div style="display: flex; justify-content: space-around; text-align: center;
                        padding: 18px 0; border-top: 1px solid rgba(255,255,255,0.03);
                        border-bottom: 1px solid rgba(255,255,255,0.03);">
                <div>
                    <p style="font-size: 9px; letter-spacing: 1px; color: rgba(255,255,255,0.25);
                              text-transform: uppercase; margin-bottom: 4px;">Longs</p>
                    <p style="font-size: 20px; font-weight: 800; color: #30D158;">250K</p>
                </div>
                <div>
                    <p style="font-size: 9px; letter-spacing: 1px; color: rgba(255,255,255,0.25);
                              text-transform: uppercase; margin-bottom: 4px;">Shorts</p>
                    <p style="font-size: 20px; font-weight: 800; color: #FF453A;">50K</p>
                </div>
                <div>
                    <p style="font-size: 9px; letter-spacing: 1px; color: rgba(255,255,255,0.25);
                              text-transform: uppercase; margin-bottom: 4px;">Net</p>
                    <p style="font-size: 20px; font-weight: 800; color: #d4af37;">+200K</p>
                </div>
            </div>
            <div style="margin-top: 12px; text-align: center;">
                <span style="font-size: 9px; padding: 4px 14px; border-radius: 20px;
                            background: rgba(48,209,88,0.08); color: #30d158;
                            font-weight: 700; letter-spacing: 1px;">
                    ● BIAS: BULLISH
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
    render_footer()

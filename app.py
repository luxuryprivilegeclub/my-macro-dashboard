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
# 3. APPLE-STYLE CSS — COMPLETE OVERHAUL
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0a;
        --bg-elevated: rgba(28,28,30,0.72);
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
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
        --shadow-md: 0 8px 32px rgba(0,0,0,0.4);
        --shadow-lg: 0 20px 60px rgba(0,0,0,0.5);
        --shadow-gold: 0 0 40px rgba(212,175,55,0.08);
        --transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    /* ===== BASE ===== */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
        color: var(--text-primary);
    }
    #MainMenu, footer, header { visibility: hidden; }
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    .stDeployButton { display: none; }

    /* ===== SCROLLBAR — Apple thin ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }

    /* ===== BUTTONS — Apple Pill Style ===== */
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
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
    }
    div.stButton > button:hover {
        background: var(--gold-glow) !important;
        color: var(--gold) !important;
        border-color: rgba(212,175,55,0.3) !important;
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(212,175,55,0.1) !important;
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* ===== TEXT INPUTS — Apple Frosted ===== */
    div[data-testid="stTextInput"] input {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: #fff !important;
        font-size: 15px !important;
        padding: 14px 18px !important;
        font-family: 'Inter', sans-serif !important;
        transition: var(--transition) !important;
        backdrop-filter: blur(10px) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 4px rgba(212,175,55,0.06), var(--shadow-gold) !important;
        background: rgba(255,255,255,0.05) !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: var(--text-quaternary) !important;
    }
    div[data-testid="stTextInput"] label {
        color: var(--text-tertiary) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    /* ===== TEXT AREA ===== */
    div[data-testid="stTextArea"] textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        backdrop-filter: blur(10px) !important;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 4px rgba(212,175,55,0.06) !important;
    }
    div[data-testid="stTextArea"] label {
        color: var(--text-tertiary) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    /* ===== SELECTBOX ===== */
    div[data-testid="stSelectbox"] > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        backdrop-filter: blur(10px) !important;
    }
    div[data-testid="stSelectbox"] label {
        color: var(--text-tertiary) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    /* ===== TABS — Apple Segmented ===== */
    div[data-testid="stTabs"] button {
        color: var(--text-tertiary) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        background: transparent !important;
        border-bottom: 2px solid transparent !important;
        transition: var(--transition) !important;
        letter-spacing: 0.3px !important;
    }
    div[data-testid="stTabs"] button:hover {
        color: var(--text-secondary) !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--gold) !important;
        border-bottom-color: var(--gold) !important;
    }

    /* ===== FILE UPLOADER ===== */
    div[data-testid="stFileUploader"] {
        background: var(--bg-card) !important;
        border: 2px dashed rgba(212,175,55,0.12) !important;
        border-radius: var(--radius-lg) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* ===== DATE INPUT ===== */
    div[data-testid="stDateInput"] input {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: white !important;
    }

    /* ===== METRICS ===== */
    div[data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 20px;
        backdrop-filter: blur(20px);
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

    /* ===== HR ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent) !important;
        margin: 45px 0 !important;
    }

    /* ===== HIDE ANCHORS ===== */
    h1 a, h2 a, h3 a { display: none !important; }

    /* ===== DATAFRAME ===== */
    div[data-testid="stDataFrame"] {
        border-radius: var(--radius-md) !important;
        overflow: hidden;
    }

    /* ===== ANIMATIONS ===== */
    @keyframes shimmer {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 200% center; }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(48,209,88,0.4); }
        50% { box-shadow: 0 0 0 6px rgba(48,209,88,0); }
    }
    @keyframes float-gentle {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
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
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(212,175,55,0.1); }
        50% { border-color: rgba(212,175,55,0.25); }
    }
    @keyframes spin-slow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* ===== NAVBAR — Apple Frosted Glass (via HTML) ===== */
    .apple-navbar {
        position: sticky;
        top: 0;
        z-index: 9999;
        background: rgba(0,0,0,0.72);
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 0 28px;
        margin: -1rem -1rem 0 -1rem;
        width: calc(100% + 2rem);
    }
    .apple-navbar-inner {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 52px;
    }
    .apple-navbar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .apple-navbar-brand img {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        object-fit: cover;
        border: 1.5px solid rgba(212,175,55,0.4);
    }
    .apple-navbar-brand span {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2.5px;
        color: var(--gold);
    }
    .apple-navbar-links {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .apple-navbar-user {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .apple-navbar-user span {
        font-size: 11px;
        color: var(--text-tertiary);
        font-weight: 500;
    }
    .apple-navbar-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--gold), #8b6914);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        color: #000;
    }

    /* ===== APPLE CARD SYSTEM ===== */
    .apple-card {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 28px;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    .apple-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    }
    .apple-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--glass-border-hover);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    /* ===== SECTION HEADERS ===== */
    .section-eyebrow {
        font-size: 10px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: var(--gold-dim);
        font-weight: 600;
        text-align: center;
        margin-bottom: 8px;
    }
    .section-title {
        font-size: 40px;
        font-weight: 800;
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        line-height: 1.15;
    }
    .section-title .gold-text {
        background: linear-gradient(135deg, #d4af37, #f5d769, #d4af37);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s ease-in-out infinite;
    }
    .section-subtitle {
        font-size: 15px;
        color: var(--text-tertiary);
        text-align: center;
        margin-bottom: 40px;
        font-weight: 400;
    }

    /* ===== LIVE BADGE ===== */
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 10px;
        color: var(--text-quaternary);
        font-weight: 500;
    }
    .live-dot {
        width: 6px;
        height: 6px;
        background: var(--green);
        border-radius: 50%;
        display: inline-block;
        animation: pulse-glow 2s infinite;
    }

    /* ===== TAG PILL ===== */
    .tag-pill {
        font-size: 9px;
        padding: 4px 12px;
        border-radius: 980px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        display: inline-block;
    }

    /* ===== TOOL CARD ===== */
    .tool-card {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 28px 20px;
        text-align: center;
        min-height: 220px;
        cursor: pointer;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    .tool-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
    }
    .tool-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    .tool-card .tool-icon {
        font-size: 32px;
        margin-bottom: 14px;
        display: block;
    }
    .tool-card .tool-name {
        color: var(--text-primary);
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
        line-height: 1.3;
    }
    .tool-card .tool-desc {
        color: var(--text-tertiary);
        font-size: 11px;
        line-height: 1.6;
        margin-bottom: 16px;
    }
    .tool-card .tool-status {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }
    .tool-card .tool-status span.status-label {
        font-size: 9px;
        letter-spacing: 1.2px;
        color: var(--text-tertiary);
        font-weight: 600;
    }

    /* ===== NEWS CARD ===== */
    .news-card {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 28px;
        margin-bottom: 16px;
        transition: var(--transition);
    }
    .news-card:hover {
        border-color: rgba(212,175,55,0.2);
        background: var(--bg-card-hover);
        transform: translateY(-1px);
    }

    /* ===== APPLE HERO ===== */
    .apple-hero {
        position: relative;
        text-align: center;
        padding: 70px 30px;
        border-radius: var(--radius-2xl);
        overflow: hidden;
        margin-bottom: 40px;
        background: radial-gradient(ellipse at 50% 0%, rgba(212,175,55,0.08) 0%, transparent 60%),
                    linear-gradient(180deg, rgba(255,255,255,0.01) 0%, transparent 100%);
        border: 1px solid rgba(255,255,255,0.04);
        animation: fadeInUp 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    .apple-hero::before {
        content: '';
        position: absolute;
        top: -200px;
        left: 50%;
        transform: translateX(-50%);
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(212,175,55,0.06) 0%, transparent 70%);
        pointer-events: none;
        animation: glow-breathe 5s ease-in-out infinite;
    }
    .apple-hero .hero-eyebrow {
        font-size: 10px;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: var(--gold-dim);
        font-weight: 600;
        margin-bottom: 20px;
        position: relative;
    }
    .apple-hero .hero-title {
        font-size: 38px;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 auto;
        max-width: 700px;
        line-height: 1.25;
        position: relative;
        letter-spacing: -0.3px;
    }
    .apple-hero .hero-title .gold-text {
        background: linear-gradient(135deg, #d4af37, #f5d769, #d4af37);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s ease-in-out infinite;
    }
    .apple-hero .hero-sub {
        color: var(--text-tertiary);
        font-size: 14px;
        margin-top: 16px;
        position: relative;
        font-weight: 400;
    }
    .apple-hero .hero-live {
        margin-top: 24px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        position: relative;
    }

    /* ===== MARKET CHART CARD ===== */
    .chart-card {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        overflow: hidden;
        margin-bottom: 16px;
        transition: var(--transition);
    }
    .chart-card:hover {
        border-color: var(--glass-border-hover);
    }
    .chart-card-header {
        padding: 14px 18px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .chart-card-header .chart-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-tertiary);
    }

    /* ===== FOOTER ===== */
    .apple-footer {
        margin-top: 100px;
        padding: 50px 20px 40px;
        border-top: 1px solid rgba(255,255,255,0.04);
        text-align: center;
    }
    .apple-footer .footer-brand {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 3px;
        color: rgba(212,175,55,0.5);
        margin-bottom: 4px;
    }
    .apple-footer .footer-desc {
        font-size: 12px;
        color: var(--text-quaternary);
    }
    .apple-footer .footer-links {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 28px 0;
        flex-wrap: wrap;
    }
    .apple-footer .footer-links span {
        color: var(--text-tertiary);
        font-size: 12px;
        font-weight: 500;
        cursor: pointer;
        transition: var(--transition);
    }
    .apple-footer .footer-links span:hover {
        color: var(--gold);
    }
    .apple-footer .footer-divider {
        width: 50px;
        height: 1px;
        margin: 28px auto;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);
    }
    .apple-footer .footer-disclaimer {
        max-width: 600px;
        margin: 0 auto;
        font-size: 11px;
        line-height: 2;
        color: var(--text-quaternary);
    }
    .apple-footer .footer-legal {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
    }
    .apple-footer .footer-legal span {
        font-size: 10px;
        color: var(--text-quaternary);
    }
    .apple-footer .footer-copy {
        font-size: 10px;
        color: rgba(255,255,255,0.1);
        letter-spacing: 2px;
    }

    /* ===== LOGIN CARD ===== */
    .login-container {
        animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    .login-logo {
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid var(--gold);
        box-shadow: 0 0 20px rgba(212,175,55,0.15), 0 0 60px rgba(212,175,55,0.06);
        animation: glow-breathe 4s ease-in-out infinite;
    }

    /* ===== MACRO GAUGE CARD ===== */
    .gauge-card {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 18px;
        transition: var(--transition);
    }
    .gauge-card:hover {
        border-color: var(--glass-border-hover);
        background: var(--bg-card-hover);
    }

    /* ===== COT CARD ===== */
    .cot-card {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 30px;
    }

    /* ===== ADMIN STATUS ROW ===== */
    .admin-status-row {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-sm);
        padding: 14px 18px;
        margin-bottom: 8px;
        transition: var(--transition);
    }
    .admin-status-row:hover {
        border-color: var(--glass-border-hover);
    }

    /* ===== CONTENT EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 100px 20px;
        animation: fadeIn 0.6s ease;
    }
    .empty-state .empty-icon {
        font-size: 64px;
        opacity: 0.12;
        margin-bottom: 16px;
    }
    .empty-state h3 {
        color: var(--text-tertiary);
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .empty-state p {
        color: var(--text-quaternary);
        font-size: 13px;
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
.ht{font-size:44px;font-weight:800;color:#d4af37;margin-bottom:10px;letter-spacing:-0.5px;}
.sec{margin-bottom:30px;padding:30px;background:rgba(255,255,255,0.03);border-radius:24px;border:1px solid rgba(255,255,255,0.06);}
.sh{font-size:12px;font-weight:700;color:#d4af37;letter-spacing:2px;text-transform:uppercase;margin-bottom:25px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.04);}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:15px;}
.sc{background:rgba(255,255,255,0.02);padding:20px;border-radius:16px;border:1px solid rgba(255,255,255,0.04);text-align:center;}
.sl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);font-weight:600;margin-bottom:8px;}
.sv{font-size:28px;font-weight:800;color:#d4af37;}
.lb{background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);padding:20px;border-radius:16px;margin-top:20px;font-size:14px;line-height:1.7;color:rgba(255,255,255,0.7);}
.bl{text-align:center;padding:40px;background:rgba(212,175,55,0.03);border-radius:24px;border:1px solid rgba(212,175,55,0.15);}
.bl h3{font-size:28px;font-weight:800;color:#d4af37;margin-bottom:10px;}
.bl p{color:rgba(255,255,255,0.5);}</style></head><body><div class="mc"><section class="hero"><h1 class="ht">Gold Analysis</h1><p style="color:rgba(255,255,255,0.4);">Smart Money Positioning — APR 26 Contract</p></section><section class="sec"><div class="sh">Futures Data</div><div class="sg"><div class="sc"><div class="sl">Price</div><div class="sv" style="color:#FF453A">5,086</div></div><div class="sc"><div class="sl">Volume</div><div class="sv">129,968</div></div><div class="sc"><div class="sl">OI</div><div class="sv" style="color:#FF453A">+1,199</div></div><div class="sc"><div class="sl">Blocks</div><div class="sv">475</div></div></div><div class="lb"><strong>Logic:</strong> Price DOWN + OI UP = SHORT BUILDUP</div></section><section class="bl"><h3>VERDICT: BEARISH</h3><p>Short rallies into 5280 targeting 5020</p></section></div></body></html>"""

CALCULATOR_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{margin:0;padding:0;box-sizing:border-box;}body{background:transparent;display:flex;justify-content:center;padding:30px;font-family:'Inter',-apple-system,sans-serif;}.c{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:28px;padding:40px;width:100%;max-width:480px;}.ce{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.6);font-weight:600;text-align:center;margin-bottom:8px;}.ct{font-size:28px;font-weight:800;text-align:center;color:#d4af37;margin-bottom:35px;letter-spacing:-0.3px;}.ig{margin-bottom:22px;}.ig label{display:block;margin-bottom:8px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.35);}.ig input{width:100%;padding:16px 20px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;color:#fff;font-size:16px;outline:none;transition:all 0.3s;font-family:'Inter',sans-serif;}.ig input:focus{border-color:rgba(212,175,55,0.5);box-shadow:0 0 0 4px rgba(212,175,55,0.06);}.cb{width:100%;padding:18px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#000;border:none;border-radius:980px;font-size:15px;font-weight:700;cursor:pointer;margin-top:15px;transition:all 0.3s;font-family:'Inter',sans-serif;}.cb:hover{transform:scale(1.02);box-shadow:0 8px 30px rgba(212,175,55,0.2);}#result{margin-top:30px;text-align:center;display:none;padding:30px;border-radius:20px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.12);}.rv{font-size:48px;font-weight:800;color:#d4af37;letter-spacing:-1px;}.rr{font-size:13px;color:rgba(255,255,255,0.3);margin-top:8px;}</style></head><body><div class="c"><p class="ce">Risk Management</p><h1 class="ct">Position Sizer</h1><div class="ig"><label>Account Balance</label><input type="number" id="a" placeholder="10000"></div><div class="ig"><label>Risk (%)</label><input type="number" id="r" placeholder="2.0"></div><div class="ig"><label>Stop Loss (Pips)</label><input type="number" id="s" placeholder="50"></div><button class="cb" onclick="calc()">Calculate Position</button><div id="result"><p style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Recommended Lot Size</p><p class="rv" id="lv"></p><p class="rr" id="ra"></p></div></div><script>function calc(){var a=parseFloat(document.getElementById('a').value);var r=parseFloat(document.getElementById('r').value);var s=parseFloat(document.getElementById('s').value);if(!a||!r||!s)return;var ra=(a*r/100);var l=(ra/(s*10)).toFixed(2);document.getElementById('lv').textContent=l+' Lot';document.getElementById('ra').textContent='Risk Amount: $'+ra.toFixed(2);document.getElementById('result').style.display='block';}</script></body></html>"""

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
        {"title": "Gold Surges Past $3,300 on Safe Haven Demand", "desc": "Institutional buyers accumulate as geopolitical tensions rise. Smart money continues to build long positions at key support zones.", "date": datetime.now().strftime("%Y-%m-%d"), "tag": "GOLD"},
        {"title": "Fed Holds Rates Steady — Dollar Weakness Ahead", "desc": "The Federal Reserve maintained its current stance. Markets price in potential cuts for Q3.", "date": datetime.now().strftime("%Y-%m-%d"), "tag": "MACRO"},
        {"title": "Bitcoin Breaks $94K — Institutional Adoption Accelerates", "desc": "Crypto markets rally as major funds increase BTC allocation. ETF inflows hit record levels.", "date": datetime.now().strftime("%Y-%m-%d"), "tag": "CRYPTO"},
    ]


# ============================================
# 6. APPLE NAVBAR (Frosted Glass)
# ============================================
def render_navbar():
    uname = st.session_state['username'] if st.session_state['username'] else "User"
    u_init = uname[0].upper()
    is_admin = (st.session_state['user_role'] == 'Admin')

    # Current page for active state
    current = st.session_state['current_page']

    navbar_html = f'''
    <div class="apple-navbar">
        <div class="apple-navbar-inner">
            <div class="apple-navbar-brand">
                <img src="{LOGO_URL}" alt="Logo">
                <span>ROLLIC TRADES</span>
            </div>
            <div class="apple-navbar-user">
                <span>{uname}</span>
                <div class="apple-navbar-avatar">{u_init}</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(navbar_html, unsafe_allow_html=True)
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # Navigation buttons as pills
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
# 7. TRADINGVIEW TICKER
# ============================================
def render_ticker_tape():
    tv_ticker = """
    <div style="border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.04);margin-bottom:30px;">
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
    </script></div></div>
    """
    components.html(tv_ticker, height=78)


# ============================================
# 8. FOOTER
# ============================================
def render_footer():
    st.markdown(f'''
    <div class="apple-footer">
        <div style="margin-bottom:16px;">
            <img src="{LOGO_URL}" width="40" height="40"
                style="border-radius:50%;object-fit:cover;border:1.5px solid rgba(212,175,55,0.25);">
        </div>
        <p class="footer-brand">ROLLIC TRADES</p>
        <p class="footer-desc">Smart Money Intelligence Platform</p>
        <div class="footer-links">
            <span>Home</span>
            <span>Macro Terminal</span>
            <span>Reports</span>
            <span>Calculator</span>
            <span>Academy</span>
        </div>
        <div class="footer-divider"></div>
        <p class="footer-disclaimer">
            <strong style="color:rgba(255,255,255,0.35);">Risk Disclaimer</strong><br>
            Trading involves substantial risk. All analysis is for educational purposes only.
            Past performance is not indicative of future results. Trade responsibly.
        </p>
        <div class="footer-divider"></div>
        <div class="footer-legal">
            <span>Privacy Policy</span>
            <span style="color:rgba(255,255,255,0.08);">|</span>
            <span>Terms of Service</span>
            <span style="color:rgba(255,255,255,0.08);">|</span>
            <span>Contact Us</span>
        </div>
        <p class="footer-copy">© 2026 ROLLIC TRADES — ALL RIGHTS RESERVED</p>
    </div>
    ''', unsafe_allow_html=True)


# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="text-align:center;margin-bottom:24px;">
            <img src="{LOGO_URL}" width="100" height="100" class="login-logo">
        </div>
        <div style="text-align:center;margin-bottom:8px;">
            <p style="font-size:9px;letter-spacing:5px;text-transform:uppercase;
                color:rgba(212,175,55,0.35);font-weight:600;margin-bottom:8px;">INSTITUTIONAL TRADING</p>
            <h1 style="font-size:32px;font-weight:800;margin:0;letter-spacing:-0.5px;
                background:linear-gradient(135deg,#d4af37,#f5d769,#d4af37);background-size:200% auto;
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                animation:shimmer 4s ease-in-out infinite;">ROLLIC TRADES</h1>
            <p style="color:rgba(255,255,255,0.18);font-size:12px;margin-top:6px;font-weight:400;">
                Smart Money Intelligence Platform</p>
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
                    st.error("Account suspended. Contact admin.")
            else:
                st.error("Invalid credentials")

        st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# HOME PAGE
# ============================================
def home_page():
    hero_quote = st.session_state['hero_quote']
    hero_sub = st.session_state['hero_subtitle']

    render_ticker_tape()

    # APPLE HERO
    st.markdown(f'''
    <div class="apple-hero">
        <p class="hero-eyebrow">ROLLIC TRADES</p>
        <h1 class="hero-title">"<span class="gold-text">{hero_quote}</span>"</h1>
        <p class="hero-sub">{hero_sub}</p>
        <div class="hero-live">
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

    tv_widgets_data = [
        ("XAUUSD", "OANDA:XAUUSD"),
        ("EURUSD", "FX:EURUSD"),
        ("SP500", "FOREXCOM:SPXUSD"),
        ("BTCUSD", "COINBASE:BTCUSD"),
    ]

    w1, w2 = st.columns(2)
    for i, (label, symbol) in enumerate(tv_widgets_data):
        target_col = w1 if i % 2 == 0 else w2
        with target_col:
            st.markdown(f'''
            <div class="chart-card">
                <div class="chart-card-header">
                    <span class="chart-label">{label}</span>
                    <div class="live-badge">
                        <span class="live-dot"></span>
                        <span>LIVE</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
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
                    status_dot = f'<span class="live-dot"></span>'
                    status_text = "ACTIVE"
                else:
                    status_dot = '<span style="width:6px;height:6px;background:rgba(255,255,255,0.12);border-radius:50%;display:inline-block;"></span>'
                    status_text = "COMING"

                # Parse color for hover
                c = meta["color"].lstrip("#")
                r_val, g_val, b_val = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)

                card_html = f'''
                <div class="tool-card"
                    onmouseover="this.style.background='rgba({r_val},{g_val},{b_val},0.04)';
                    this.style.borderColor='rgba({r_val},{g_val},{b_val},0.18)';
                    this.style.boxShadow='0 20px 60px rgba({r_val},{g_val},{b_val},0.06)'"
                    onmouseout="this.style.background='rgba(255,255,255,0.03)';
                    this.style.borderColor='rgba(255,255,255,0.08)';
                    this.style.boxShadow='none'">
                    <span class="tool-icon">{meta["icon"]}</span>
                    <p class="tool-name">{meta["name"]}</p>
                    <p class="tool-desc">{meta["desc"]}</p>
                    <div class="tool-status">
                        {status_dot}
                        <span class="status-label">{status_text}</span>
                    </div>
                </div>
                '''
                st.markdown(card_html, unsafe_allow_html=True)

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
                st.markdown(f'''
                <div class="news-card">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
                        <span class="tag-pill" style="background:rgba({int(tc[1:3],16)},{int(tc[3:5],16)},{int(tc[5:7],16)},0.08);color:{tc};">
                            {art.get("tag", "NEWS")}</span>
                        <span style="font-size:11px;color:rgba(255,255,255,0.18);">{art["date"]}</span>
                    </div>
                    <h3 style="color:#fff;font-size:18px;font-weight:700;margin-bottom:10px;line-height:1.4;letter-spacing:-0.2px;">
                        {art["title"]}</h3>
                    <p style="color:rgba(255,255,255,0.35);font-size:14px;line-height:1.8;">
                        {art["desc"]}</p>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No news articles yet. Admin can add from Admin Panel.")
        return

    if content:
        components.html(content, height=1500, scrolling=True)
    else:
        st.markdown(f'''
        <div class="empty-state">
            <div class="empty-icon">{meta["icon"]}</div>
            <h3>Content Coming Soon</h3>
            <p>Admin will upload content for this section.</p>
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
# MACRO DASHBOARD
# ============================================
def macro_dashboard():
    st.markdown('''
    <div style="text-align:center;padding:24px 0 8px;animation:fadeInUp 0.6s ease-out;">
        <p class="section-eyebrow">INSTITUTIONAL GRADE</p>
        <p class="section-title">Macro <span class="gold-text">Terminal</span></p>
        <p class="section-subtitle">Economic intelligence and Smart Money positioning</p>
    </div>
    ''', unsafe_allow_html=True)

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
        st.info("📊 Demo mode — add FRED_API_KEY in secrets for live data.")

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
                title, key, color, dxy, gold, nxt = items[iv]
                d = fred_data.get(key, {'latest': 0, 'previous': 0, 'change': 0})
                with col_obj:
                    chg_c = "#30d158" if d['change'] >= 0 else "#ff453a"
                    chg_bg = f"rgba({48 if d['change'] >= 0 else 255},{209 if d['change'] >= 0 else 69},{88 if d['change'] >= 0 else 58},0.08)"
                    chg_p = "+" if d['change'] >= 0 else ""

                    st.markdown(f'''
                    <div class="gauge-card">
                        <div style="display:flex;align-items:center;justify-content:space-between;">
                            <span style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;
                                color:rgba(255,255,255,0.3);font-weight:600;">{title}</span>
                            <span class="tag-pill" style="background:{chg_bg};color:{chg_c};font-size:9px;padding:3px 10px;">
                                {chg_p}{abs(d['change'])}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

                    st.plotly_chart(build_gauge(d['latest'], d['previous'], color),
                                   use_container_width=True, key="g_" + key + str(iv))

                    st.markdown(f'''
                    <div style="display:flex;justify-content:center;gap:6px;margin-top:-10px;margin-bottom:10px;">
                        <span class="tag-pill" style="background:rgba(10,132,255,0.08);color:#0a84ff;font-size:9px;padding:3px 10px;">
                            DXY: {dxy}</span>
                        <span class="tag-pill" style="background:rgba(212,175,55,0.08);color:#d4af37;font-size:9px;padding:3px 10px;">
                            GOLD: {gold}</span>
                    </div>
                    <p style="text-align:center;font-size:9px;color:rgba(255,255,255,0.12);">Next Release: {nxt}</p>
                    ''', unsafe_allow_html=True)

    # COT SECTION
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('''
    <p class="section-eyebrow">SMART MONEY</p>
    <p class="section-title">COT <span class="gold-text">Analysis</span></p>
    ''', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

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
                dict(text="75%", x=0.5, y=0.55, font_size=44, showarrow=False, font_color="#d4af37",
                     font_family="Inter"),
                dict(text="BULLISH", x=0.5, y=0.42, font_size=10, showarrow=False,
                     font_color="rgba(255,255,255,0.2)")
            ]
        )
        st.plotly_chart(fig_cot, use_container_width=True, key="cot_d")

    with cr:
        st.markdown('''
        <div class="cot-card">
            <p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.5);
                font-weight:700;margin-bottom:16px;">XAUUSD POSITIONING</p>
            <p style="color:rgba(255,255,255,0.4);font-size:14px;line-height:1.8;margin-bottom:20px;">
                Smart Money <strong style="color:#f5f5f7;">net long</strong>. Accumulating at institutional demand zones.
                Commercial hedgers reducing shorts.</p>
            <div style="display:flex;justify-content:space-around;text-align:center;padding:18px 0;
                border-top:1px solid rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.03);">
                <div>
                    <p style="font-size:9px;color:rgba(255,255,255,0.2);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Longs</p>
                    <p style="font-size:22px;font-weight:800;color:#30d158;letter-spacing:-0.5px;">250K</p>
                </div>
                <div>
                    <p style="font-size:9px;color:rgba(255,255,255,0.2);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Shorts</p>
                    <p style="font-size:22px;font-weight:800;color:#ff453a;letter-spacing:-0.5px;">50K</p>
                </div>
                <div>
                    <p style="font-size:9px;color:rgba(255,255,255,0.2);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Net</p>
                    <p style="font-size:22px;font-weight:800;color:#d4af37;letter-spacing:-0.5px;">+200K</p>
                </div>
            </div>
            <div style="margin-top:14px;text-align:center;">
                <span class="tag-pill" style="background:rgba(48,209,88,0.08);color:#30d158;padding:5px 16px;font-size:10px;">
                    BIAS: BULLISH</span>
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
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    uploadable_tools = ["money_flow", "oi_analyzer", "gold_report", "forex_report",
                        "btc_report", "sp500_report", "learning"]

    tabs = st.tabs(["📄 Content Manager", "👥 Users", "✏️ Hero Banner", "📰 News Manager"])

    # TAB 1
    with tabs[0]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Upload Content for Toolkit Sections")
        st.info("Select a section and upload its HTML file. Content appears when users open that tool.")

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
                st.success("✅ Published: " + tool_meta[selected_tool]["name"])
            else:
                st.error("Select an HTML file first.")

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
                <div class="admin-status-row">
                    <span style="font-size:16px;">{meta["icon"]}</span>
                    <span style="color:#f5f5f7;font-size:13px;font-weight:600;margin-left:8px;">{meta["name"]}</span>
                    <span style="font-size:9px;padding:3px 10px;border-radius:980px;margin-left:10px;
                        color:{s_color};font-weight:600;letter-spacing:0.5px;">{status}</span>
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
                        st.success("Cleared: " + meta["name"])
                        st.rerun()

    # TAB 2
    with tabs[1]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.dataframe(st.session_state['users_db'], use_container_width=True, hide_index=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Add New User")
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
                    st.error("Username already exists!")
                else:
                    nr = pd.DataFrame({"Username": [new_user], "Password": [new_pass],
                                       "Role": [new_role], "Status": [new_status],
                                       "Created": [datetime.now().strftime("%Y-%m-%d")]})
                    st.session_state['users_db'] = pd.concat([st.session_state['users_db'], nr], ignore_index=True)
                    st.success("✅ Created: " + new_user)
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Modify User")
        all_u = st.session_state['users_db']['Username'].tolist()
        m1, m2 = st.columns(2)
        with m1:
            sel_u = st.selectbox("Select User", all_u, key="mu")
        with m2:
            act = st.selectbox("Action", ["Activate", "Suspend", "Make Admin", "Make User", "Reset Password", "Delete"], key="ma")
        new_pw = ""
        if act == "Reset Password":
            new_pw = st.text_input("New Password", type="password", key="rpw")

        if st.button("APPLY ACTION →", use_container_width=True, key="apl"):
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
                    else: st.error("Cannot change admin role!")
                elif act == "Reset Password":
                    if new_pw: db.at[i, 'Password'] = new_pw; st.rerun()
                    else: st.error("Enter a new password")
                elif act == "Delete":
                    if sel_u != "admin":
                        st.session_state['users_db'] = db.drop(i).reset_index(drop=True); st.rerun()
                    else: st.error("Cannot delete admin!")

    # TAB 3
    with tabs[2]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        new_q = st.text_area("Hero Quote", value=st.session_state['hero_quote'], height=100, key="hqi")
        new_s = st.text_input("Subtitle", value=st.session_state['hero_subtitle'], key="hsi")
        if st.button("UPDATE BANNER →", use_container_width=True, key="ub"):
            st.session_state['hero_quote'] = new_q
            st.session_state['hero_subtitle'] = new_s
            st.success("✅ Banner updated!")
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Preview")
        st.markdown(f'''
        <div style="background:rgba(212,175,55,0.03);border:1px solid rgba(212,175,55,0.08);
            border-radius:20px;padding:35px;text-align:center;">
            <p style="font-size:22px;font-weight:700;color:#d4af37;line-height:1.4;letter-spacing:-0.3px;">
                "{st.session_state['hero_quote']}"</p>
            <p style="color:rgba(255,255,255,0.25);font-size:13px;margin-top:12px;">
                {st.session_state['hero_subtitle']}</p>
        </div>
        ''', unsafe_allow_html=True)

    # TAB 4
    with tabs[3]:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Add Article")
        n1, n2 = st.columns(2)
        with n1:
            nt = st.text_input("Title", key="nt", placeholder="Article headline")
        with n2:
            ntg = st.selectbox("Category", ["GOLD", "MACRO", "CRYPTO", "FOREX"], key="ntg")
        nd = st.text_area("Description", key="nd", placeholder="Article summary...", height=100)

        if st.button("ADD ARTICLE →", use_container_width=True, key="an"):
            if nt and nd:
                st.session_state['news_articles'].insert(0, {
                    "title": nt, "desc": nd,
                    "date": datetime.now().strftime("%Y-%m-%d"), "tag": ntg
                })
                st.success("✅ Article added!")
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Current Articles")
        for i, art in enumerate(st.session_state['news_articles']):
            ac1, ac2 = st.columns([5, 1])
            with ac1:
                st.markdown(f'''
                <span class="tag-pill" style="background:rgba(212,175,55,0.08);color:#d4af37;padding:3px 10px;">
                    {art["tag"]}</span>
                <span style="color:#f5f5f7;font-size:13px;font-weight:600;margin-left:10px;">
                    {art["title"]}</span>
                ''', unsafe_allow_html=True)
            with ac2:
                if st.button("Delete", key="dn_" + str(i)):
                    st.session_state['news_articles'].pop(i)
                    st.rerun()


# ============================================
# REPORTS PAGE (Legacy)
# ============================================
def reports_page():
    st.markdown(f'''
    <div style="text-align:center;padding:24px 0 8px;">
        <div style="margin-bottom:14px;">
            <img src="{LOGO_URL}" width="50" height="50"
                style="border-radius:50%;object-fit:cover;border:2px solid rgba(212,175,55,0.3);">
        </div>
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
        st.info("No reports available yet.")


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

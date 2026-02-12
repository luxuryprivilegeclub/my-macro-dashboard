import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Rollic Trades Terminal", layout="wide", initial_sidebar_state="collapsed")

# --- ADMIN CREDENTIALS (MASTER USER) ---
# Ye Master Admin hai jo users ko manage karega
ADMIN_USER = "admin"
ADMIN_PASS = "Rollic@786"  # Aapka Master Password (Change kar lena)
ADMIN_EMAIL = "ahmedraomuhmmad@gmail.com"

# --- LOGO & QUOTE ---
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
TRADING_QUOTE = "“The goal of a successful trader is to make the best trades. Money is secondary.” – Alexander Elder"

# --- SESSION STATE SETUP ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# --- DUMMY DATABASE (Replace with Google Sheets for Permanent Storage) ---
# Demo ke liye ye list use ho rahi hai. Real SaaS ke liye Google Sheets connect karni hogi.
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = pd.DataFrame([
        {"Username": "admin", "Password": "123", "Role": "Admin", "Status": "Active", "Email": ADMIN_EMAIL},
        {"Username": "demo_user", "Password": "123", "Role": "User", "Status": "Active", "Email": "demo@test.com"}
    ])

# ==========================================
# 1. AUTHENTICATION & REGISTRATION SYSTEM
# ==========================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo & Quote
        st.markdown(f"""
            <div style="text-align: center; margin-top: 50px;">
                <img src="{LOGO_URL}" width="200" style="border-radius: 50%; border: 4px solid #d4af37; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.5);">
                <h1 style="color: #d4af37; font-family: 'Arial Black'; margin-top: 20px;">ROLLIC TRADES</h1>
                <p style="font-style: italic; color: #888; font-size: 14px;">{TRADING_QUOTE}</p>
                <hr style="border: 1px solid #d4af37; width: 50%; margin: 20px auto;">
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔒 LOGIN", "📝 REGISTER"])

        # --- LOGIN TAB ---
        with tab1:
            st.markdown("### Access Dashboard")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("LOGIN", type="primary", use_container_width=True):
                # Check Admin Hardcoded
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Admin"
                    st.session_state['username'] = "Master Admin"
                    st.rerun()
                
                # Check User DB
                db = st.session_state['users_db']
                user_match = db[(db['Username'] == username) & (db['Password'] == password)]
                
                if not user_match.empty:
                    status = user_match.iloc[0]['Status']
                    if status == "Active":
                        st.session_state['logged_in'] = True
                        st.session_state['user_role'] = user_match.iloc[0]['Role']
                        st.session_state['username'] = username
                        st.success("Login Successful!")
                        time.sleep(1)
                        st.rerun()
                    elif status == "Blocked":
                        st.error("🚫 Your account has been BLOCKED by Admin.")
                    else:
                        st.warning("⏳ Your account is Pending Approval.")
                else:
                    st.error("Invalid Username or Password")

        # --- REGISTRATION TAB ---
        with tab2:
            st.markdown("### New User Registration")
            new_user = st.text_input("Choose Username")
            new_email = st.text_input("Your Email")
            new_pass = st.text_input("Choose Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            
            if st.button("Submit Registration", use_container_width=True):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                elif new_user and new_email and new_pass:
                    # Email Logic (FormSubmit)
                    contact_form = f"""
                    <form action="https://formsubmit.co/{ADMIN_EMAIL}" method="POST" id="reg_form">
                        <input type="hidden" name="Subject" value="New Rollic Trades Registration">
                        <input type="hidden" name="Username" value="{new_user}">
                        <input type="hidden" name="Email" value="{new_email}">
                        <input type="hidden" name="Password" value="{new_pass}">
                        <input type="hidden" name="Message" value="Please approve this user in Admin Panel.">
                    </form>
                    <script>document.getElementById("reg_form").submit();</script>
                    """
                    st.components.v1.html(contact_form, height=0, width=0)
                    
                    st.success("✅ Registration Request Sent to Admin!")
                    st.info(f"Details sent to {ADMIN_EMAIL}. Wait for approval.")
                    
                    # Add to temp DB as Pending
                    new_data = pd.DataFrame([{"Username": new_user, "Password": new_pass, "Role": "User", "Status": "Pending", "Email": new_email}])
                    st.session_state['users_db'] = pd.concat([st.session_state['users_db'], new_data], ignore_index=True)
                else:
                    st.warning("Please fill all fields.")

# ==========================================
# 2. ADMIN PANEL (MANAGEMENT SYSTEM)
# ==========================================
def admin_panel():
    st.markdown("## 🛠 Admin Management Panel")
    st.info("Yahan aap users ko Block/Unblock kar sakte hain. (Changes temporary hain jab tak Google Sheets connect na ho).")
    
    # Edit Data
    edited_df = st.data_editor(
        st.session_state['users_db'],
        num_rows="dynamic",
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Active", "Blocked", "Pending"],
                required=True,
            ),
            "Role": st.column_config.SelectboxColumn(
                "Role",
                options=["User", "Admin"],
                required=True,
            )
        },
        use_container_width=True
    )
    
    if st.button("Save Changes"):
        st.session_state['users_db'] = edited_df
        st.success("User Database Updated!")

# ==========================================
# 3. MAIN DASHBOARD (YOUR EXISTING CODE)
# ==========================================
def main_dashboard():
    # Sidebar Logout
    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state['username']}**")
        if st.session_state['user_role'] == 'Admin':
            if st.button("Go to Admin Panel"):
                st.session_state['page'] = 'admin'
                st.rerun()
            if st.button("Go to Dashboard"):
                st.session_state['page'] = 'dashboard'
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", type="primary"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- YOUR ORIGINAL DASHBOARD CODE STARTS HERE ---
    
    # 2. Centered Logo
    st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{LOGO_URL}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

    # 3. Professional Header
    st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
        <h1 style="margin: 0; font-family: 'Arial Black', sans-serif;">ROLLIC TRADES MACRO & COT TERMINAL</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Grade Analysis | 2026 Trader Edition</p>
    </div>""", unsafe_allow_html=True)

    # 4. API Setup
    try:
        API_KEY = st.secrets["FRED_API_KEY"]
        fred = Fred(api_key=API_KEY)
    except:
        st.error("API Key missing! Check Streamlit Secrets.")
        st.stop()

    # --- Helper Function (White Headings) ---
    def draw_meter(col, name, latest, prev, info_next, msg, dxy_b, gold_b, color, bg, height=280):
        with col:
            st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -40px; color: #ffffff; font-size: 16px; position: relative; z-index: 10;'>{name}</p>", unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", 
                value=latest, 
                gauge={
                    'bar': {'color': color},
                    'axis': {'range': [min(latest, prev)*0.9, max(latest, prev)*1.1]}
                }
            ))
            fig.update_layout(height=height, margin=dict(l=30, r=30, t=60, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div style="background:{bg}; border:1px solid {color}44; padding:12px; border-radius:12px; text-align:center; margin:-30px auto 35px auto; max-width: 290px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <p style="margin:0; font-size:12px; font-weight:500; color:#333;">{msg}</p>
                <div style="margin-top:8px;">
                    <span style="background:#1e3c72; color:white; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{dxy_b}</span>
                    <span style="background:#d4af37; color:black; padding:3px 10px; border-radius:6px; font-size:10px; font-weight:bold; display:inline-block;">{gold_b}</span>
                </div>
                <p style="margin-top:10px; color:#000; font-size:11px; font-weight:bold;">📅 Next: {info_next}</p>
            </div>""", unsafe_allow_html=True)

    # --- SECTIONS ---
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📌 Primary Gold & DXY Drivers</h2>", unsafe_allow_html=True)
    cols1 = st.columns(2)
    main_ind = {
        'CPI Inflation': {'id': 'CPIAUCSL', 'next': 'Feb 13, 2026'},
        'NFP (Jobs Data)': {'id': 'PAYEMS', 'next': 'Mar 06, 2026'},
        'Unemployment Rate': {'id': 'UNRATE', 'next': 'Mar 06, 2026'},
        'Fed Interest Rate': {'id': 'FEDFUNDS', 'next': 'Mar 18, 2026'}
    }

    for i, (name, info) in enumerate(main_ind.items()):
        try:
            data = fred.get_series(info['id'])
            latest, prev = data.iloc[-1], data.iloc[-2]
            if 'CPI' in name:
                color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
                msg = "Inflation barh rahi hai." if latest > prev else "Inflation cooling hai."
                d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
            elif 'NFP' in name:
                color, bg = ("#388e3c", "#f1f8e9") if latest > prev else ("#d32f2f", "#fff5f5")
                msg = "Jobs data strong hai." if latest > prev else "Jobs weak hai."
                d_b, g_b = ("DXY: BULLISH", "GOLD: BEARISH") if latest > prev else ("DXY: BEARISH", "GOLD: BULLISH")
            elif 'Unemployment' in name:
                color, bg = ("#d32f2f", "#fff5f5") if latest > prev else ("#388e3c", "#f1f8e9")
                msg = "Berozgari barh rahi hai." if latest > prev else "Berozgari kam hui hai."
                d_b, g_b = ("DXY: BEARISH", "GOLD: BULLISH") if latest > prev else ("DXY: BULLISH", "GOLD: BEARISH")
            else: 
                color, bg = ("#1976d2", "#e3f2fd")
                msg = f"Current Rate: {latest}%"
                d_b, g_b = ("DXY: STABLE", "GOLD: PRESSURE")
            draw_meter(cols1[i%2], name, latest, prev, info['next'], msg, d_b, g_b, color, bg, 280)
        except: st.error(f"Error loading {name}")

    st.markdown("<hr><h2 style='text-align: center; color: #2c3e50;'>🌊 Liquidity & Recession Risk</h2>", unsafe_allow_html=True)
    cols2 = st.columns(4)
    liq_ind = {
        'M2 Money Supply': {'id': 'WM2NS', 'next': 'Weekly'},
        'Yield Curve (10Y-2Y)': {'id': 'T10Y2Y', 'next': 'Daily'},
        'PCE Inflation': {'id': 'PCEPI', 'next': 'Feb 27, 2026'},
        'Consumer Sentiment': {'id': 'UMCSENT', 'next': 'Feb 20, 2026'}
    }

    for i, (name, info) in enumerate(liq_ind.items()):
        try:
            data = fred.get_series(info['id'])
            latest, prev = data.iloc[-1], data.iloc[-2]
            color = "#1976d2"
            d_b, g_b = "DXY: TREND", "GOLD: TREND"
            if 'Curve' in name:
                color = "#d32f2f" if latest < 0 else "#388e3c"
                d_b, g_b = ("DXY: RISK", "GOLD: BUY") if latest < 0 else ("DXY: OK", "GOLD: HOLD")
            draw_meter(cols2[i], name, latest, prev, info['next'], "Macro trend.", d_b, g_b, color, "#fafafa", 200)
        except: st.write(f"Error {name}")

    st.markdown("<hr><h2 style='text-align: center; color: #2c3e50;'>📊 Yields & Fed Target</h2>", unsafe_allow_html=True)
    cols3 = st.columns(4)
    yield_ind = {
        'US 10Y Yield': {'id': 'DGS10', 'next': 'Daily'},
        '10Y Breakeven': {'id': 'T10YIE', 'next': 'Daily'},
        'Real Yield (10Y)': {'id': 'DFII10', 'next': 'Daily'}
    }
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

    st.markdown("<hr><h2 style='text-align: center; color: #d4af37;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)
    cot_reports = [
        {"date": "Feb 06, 2026", "longs": 285000, "shorts": 45000, "analysis": "Smart Money ne mazeed longs add kiye hain. Gold par bullish pressure barh raha hai kyunke shorts cover ho rahay hain. ICT order block par buy setups talash karein."},
        {"date": "Jan 30, 2026", "longs": 270000, "shorts": 52000, "analysis": "Institutions ne positions hold ki hui hain. Price consolidation mein hai lekin bias abhi bhi bullish hai."}
    ]
    sel_date = st.selectbox("Select COT Date", [d['date'] for d in cot_reports])
    rep = next(d for d in cot_reports if d['date'] == sel_date)
    sentiment = (rep['longs'] / (rep['longs'] + rep['shorts'])) * 100

    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -30px; color: #ffffff; font-size: 16px;'>Bullish Sentiment Index</p>", unsafe_allow_html=True)
        fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=sentiment, gauge={'bar': {'color': "#d4af37"}, 'axis': {'range': [0, 100]}}))
        fig_cot.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=0))
        st.plotly_chart(fig_cot, use_container_width=True)

    with col_r:
        st.markdown(f"""<div style="background:white; border:2px solid #d4af37; padding:25px; border-radius:15px; margin-top:20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="color:#d4af37; margin-top:0;">Expert Analysis (XAUUSD)</h3>
            <p style="font-size:14px; color:#333; line-height:1.6;">{rep['analysis']}</p>
            <hr><div style="display:flex; justify-content:space-around; text-align:center;">
                <div><p style="margin:0; font-size:11px; color:#777;">Longs</p><b style="color:#388e3c; font-size:16px;">{rep['longs']:,}</b></div>
                <div><p style="margin:0; font-size:11px; color:#777;">Shorts</p><b style="color:#d32f2f; font-size:16px;">{rep['shorts']:,}</b></div>
                <div><p style="margin:0; font-size:11px; color:#777;">Net</p><b style="color:#1e3c72; font-size:16px;">{rep['longs']-rep['shorts']:,}</b></div>
            </div></div>""", unsafe_allow_html=True)
    
    st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:60px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# ==========================================
# 4. APP FLOW LOGIC
# ==========================================
if not st.session_state['logged_in']:
    login_page()
else:
    if 'page' not in st.session_state:
        st.session_state['page'] = 'dashboard'
    
    if st.session_state['page'] == 'admin':
        admin_panel()
        if st.button("🔙 Back to Dashboard"):
            st.session_state['page'] = 'dashboard'
            st.rerun()
    else:
        main_dashboard()

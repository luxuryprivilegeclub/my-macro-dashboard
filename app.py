import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Rollic Trades SaaS", layout="wide", initial_sidebar_state="collapsed")

# --- GLOBAL VARIABLES ---
ADMIN_USER = "admin"
ADMIN_PASS = "Rollic@786"
ADMIN_EMAIL = "ahmedraomuhmmad@gmail.com"
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"
TRADING_QUOTE = "“The goal of a successful trader is to make the best trades. Money is secondary.” – Alexander Elder"

# --- SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_role' not in st.session_state: st.session_state['user_role'] = None
if 'username' not in st.session_state: st.session_state['username'] = None
if 'admin_alerts' not in st.session_state: st.session_state['admin_alerts'] = ["Welcome to Rollic Trades!"]

# --- DATABASE SIMULATION ---
if 'users_db' not in st.session_state:
    data = {
        "Username": ["admin", "shoby_trader", "new_user"],
        "Password": ["Rollic@786", "123", "123"],
        "Role": ["Admin", "User", "User"],
        "Status": ["Active", "Active", "Pending"],
        "Plan": ["Platinum", "Pro", "Basic"],
        "Email": [ADMIN_EMAIL, "shoby@gmail.com", "user@test.com"],
        "Join Date": ["2025-01-01", "2026-02-10", "2026-02-12"],
        "Last Login": [datetime.now().strftime("%Y-%m-%d %H:%M"), "2026-02-11 14:30", "Never"],
        "IP Address": ["192.168.1.1", "203.101.12.45", "Unknown"]
    }
    st.session_state['users_db'] = pd.DataFrame(data)

def get_user_ip():
    return f"{random.randint(100, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# ==========================================
# 1. LOGIN PAGE
# ==========================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 50px;">
                <img src="{LOGO_URL}" width="180" style="border-radius: 50%; border: 4px solid #d4af37; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.5);">
                <h1 style="color: #d4af37; font-family: 'Arial Black'; margin-top: 15px;">ROLLIC TRADES</h1>
                <p style="font-style: italic; color: #888;">{TRADING_QUOTE}</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔒 LOGIN", "📝 REGISTER"])

        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("LOGIN", type="primary", use_container_width=True):
                db = st.session_state['users_db']
                user_match = db[(db['Username'] == username) & (db['Password'] == password)]
                
                if not user_match.empty:
                    status = user_match.iloc[0]['Status']
                    if status == "Active":
                        idx = user_match.index[0]
                        st.session_state['users_db'].at[idx, 'Last Login'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.session_state['users_db'].at[idx, 'IP Address'] = get_user_ip()
                        
                        st.session_state['logged_in'] = True
                        st.session_state['user_role'] = user_match.iloc[0]['Role']
                        st.session_state['username'] = username
                        st.success("Login Successful!")
                        time.sleep(0.5)
                        st.rerun()
                    elif status == "Blocked":
                        st.error("🚫 Account Blocked.")
                    else:
                        st.warning("⏳ Approval Pending.")
                else:
                    st.error("Invalid Credentials")

        with tab2:
            new_user = st.text_input("Choose Username")
            new_email = st.text_input("Email")
            new_pass = st.text_input("Password", type="password")
            plan = st.selectbox("Select Plan", ["Basic", "Pro", "Platinum"])
            
            if st.button("Register Request", use_container_width=True):
                if new_user and new_email and new_pass:
                    contact_form = f"""
                    <form action="https://formsubmit.co/{ADMIN_EMAIL}" method="POST" id="reg_form">
                        <input type="hidden" name="Subject" value="New Rollic Registration: {plan}">
                        <input type="hidden" name="Username" value="{new_user}">
                    </form>
                    <script>document.getElementById("reg_form").submit();</script>
                    """
                    st.components.v1.html(contact_form, height=0, width=0)
                    new_entry = {
                        "Username": new_user, "Password": new_pass, "Role": "User", "Status": "Pending",
                        "Plan": plan, "Email": new_email, "Join Date": datetime.now().strftime("%Y-%m-%d"),
                        "Last Login": "Never", "IP Address": get_user_ip()
                    }
                    st.session_state['users_db'] = pd.concat([st.session_state['users_db'], pd.DataFrame([new_entry])], ignore_index=True)
                    st.success("Request Sent!")

# ==========================================
# 2. ADMIN PANEL (FIXED)
# ==========================================
def admin_panel():
    col_l, col_r = st.columns([1, 6])
    with col_l:
        st.image(LOGO_URL, width=80)
    with col_r:
        st.markdown("<h2 style='text-align: center; color: #d4af37; margin-top: 10px;'>ADMIN MANAGEMENT CONSOLE</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    db = st.session_state['users_db']
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("👥 Total Users", len(db))
    kpi2.metric("✅ Active", len(db[db['Status'] == "Active"]))
    kpi3.metric("⏳ Pending", len(db[db['Status'] == "Pending"]))
    
    st.markdown("### 📢 Alerts")
    with st.form("alert_form"):
        new_msg = st.text_input("Broadcast Message")
        if st.form_submit_button("Send"):
            st.session_state['admin_alerts'].insert(0, f"{datetime.now().strftime('%H:%M')} - {new_msg}")
            st.success("Sent!")

    st.markdown("### 📋 User Database")
    
    # FIXED: Removed type="password" to fix crash
    edited_df = st.data_editor(
        db,
        column_config={
            "Status": st.column_config.SelectboxColumn("Status", options=["Active", "Blocked", "Pending"], required=True),
            "Plan": st.column_config.SelectboxColumn("Plan", options=["Basic", "Pro", "Platinum"], required=True),
            "Role": st.column_config.SelectboxColumn("Role", options=["User", "Admin"], required=True),
            "IP Address": st.column_config.TextColumn("IP Logs", disabled=True),
            "Last Login": st.column_config.TextColumn("Last Seen", disabled=True),
            "Password": st.column_config.TextColumn("Password") 
        },
        use_container_width=True,
        num_rows="dynamic"
    )
    
    if st.button("💾 Save Changes"):
        st.session_state['users_db'] = edited_df
        st.success("Saved!")

# ==========================================
# 3. MAIN DASHBOARD (EXACT SAME CODE AS BEFORE)
# ==========================================
def main_dashboard():
    # Sidebar
    with st.sidebar:
        st.image(LOGO_URL, width=100)
        st.write(f"User: **{st.session_state['username']}**")
        st.markdown("---")
        st.markdown("### 🔔 Admin Alerts")
        if st.session_state['admin_alerts']:
            for msg in st.session_state['admin_alerts'][:3]:
                st.info(msg, icon="📢")
        else:
            st.write("No alerts.")
        st.markdown("---")
        if st.session_state['user_role'] == 'Admin':
            if st.button("⚙️ Admin Panel"):
                st.session_state['page'] = 'admin'
                st.rerun()
        if st.button("Logout", type="primary"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- RESTORED LOGO ---
    st.markdown(f"""<div style="display: flex; justify-content: center; margin: 10px;"><img src="{LOGO_URL}" width="160" style="border-radius: 12px;"></div>""", unsafe_allow_html=True)

    # --- ORIGINAL DASHBOARD CODE ---
    st.markdown("""<div style="background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
        <h1 style="margin: 0; font-family: 'Arial Black', sans-serif;">ROLLIC TRADES MACRO & COT TERMINAL</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Institutional Grade Analysis | 2026 Trader Edition</p>
    </div>""", unsafe_allow_html=True)

    try:
        API_KEY = st.secrets["FRED_API_KEY"]
        fred = Fred(api_key=API_KEY)
    except:
        st.error("API Key missing!")
        st.stop()

    def draw_meter(col, name, latest, prev, info_next, msg, dxy_b, gold_b, color, bg, height=280):
        with col:
            st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -40px; color: #ffffff; font-size: 16px; position: relative; z-index: 10;'>{name}</p>", unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(mode="gauge+number", value=latest, gauge={'bar': {'color': color}, 'axis': {'range': [min(latest, prev)*0.9, max(latest, prev)*1.1]}}))
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

    # Section 4 (Ring)
    st.markdown("<hr><h2 style='text-align: center; color: #d4af37;'>🏆 Smart Money COT Analysis (Gold)</h2>", unsafe_allow_html=True)
    cot_reports = [{"date": "Feb 06, 2026", "longs": 285000, "shorts": 45000, "analysis": "Smart Money ne mazeed longs add kiye hain. Gold par bullish pressure barh raha hai kyunke shorts cover ho rahay hain. ICT order block par buy setups talash karein."}]
    report = cot_reports[0]
    sentiment = (report['longs'] / (report['longs'] + report['shorts'])) * 100
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown(f"<p style='text-align: center; font-weight: bold; margin-bottom: -30px; color: #ffffff; font-size: 16px;'>Bullish Sentiment Index</p>", unsafe_allow_html=True)
        fig_cot = go.Figure(go.Indicator(mode="gauge+number", value=sentiment, gauge={'bar': {'color': "#d4af37"}, 'axis': {'range': [0, 100]}}))
        # RING LOGIC PRESERVED
        fig_cot = go.Figure(data=[go.Pie(values=[sentiment, 100-sentiment], hole=.75, direction='clockwise', sort=False, marker=dict(colors=['#d4af37', '#f0f0f0']), textinfo='none', hoverinfo='none')])
        fig_cot.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=300, annotations=[dict(text=f"{int(sentiment)}%", x=0.5, y=0.55, font_size=40, showarrow=False, font_family="Arial Black", font_color="#d4af37"), dict(text="BULLISH POWER", x=0.5, y=0.42, font_size=12, showarrow=False, font_color="#555", font_weight="bold")])
        st.plotly_chart(fig_cot, use_container_width=True)

    with col_r:
        st.markdown(f"""<div style="background:white; border:2px solid #d4af37; padding:25px; border-radius:15px; margin-top:20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><h3 style="color:#d4af37; margin-top:0;">Expert Analysis (XAUUSD)</h3><p style="font-size:14px; color:#333; line-height:1.6;">{report['analysis']}</p><hr><div style="display:flex; justify-content:space-around; text-align:center;"><div><p style="margin:0; font-size:11px; color:#777;">Longs</p><b style="color:#388e3c; font-size:16px;">{report['longs']:,}</b></div><div><p style="margin:0; font-size:11px; color:#777;">Shorts</p><b style="color:#d32f2f; font-size:16px;">{report['shorts']:,}</b></div><div><p style="margin:0; font-size:11px; color:#777;">Net</p><b style="color:#1e3c72; font-size:16px;">{report['longs']-report['shorts']:,}</b></div></div></div>""", unsafe_allow_html=True)
    
    st.markdown(f"<p style='text-align:center; color:gray; font-size:12px; margin-top:60px;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# ==========================================
# 4. FLOW LOGIC
# ==========================================
if not st.session_state['logged_in']:
    login_page()
else:
    if 'page' not in st.session_state: st.session_state['page'] = 'dashboard'
    if st.session_state['page'] == 'admin':
        admin_panel()
        if st.button("🔙 Back to Dashboard"):
            st.session_state['page'] = 'dashboard'
            st.rerun()
    else:
        main_dashboard()

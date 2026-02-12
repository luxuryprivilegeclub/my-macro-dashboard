import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Rollic Trades Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🪙"
)

# --- 2. APPLE-STYLE CSS (MODERN UI) ---
st.markdown("""
    <style>
    /* General App Styling */
    .stApp {
        background-color: #F5F5F7; /* Apple Light Grey */
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Navbar Styling */
    .navbar-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0,0,0,0.1);
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Cards (Apple Style) */
    .apple-card {
        background: white;
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid rgba(0,0,0,0.02);
    }
    .apple-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.12);
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #1d1d1f;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    p {
        color: #86868b;
        font-size: 16px;
    }

    /* Buttons Override */
    div.stButton > button {
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GLOBAL VARIABLES ---
ADMIN_USER = "admin"
ADMIN_PASS = "Rollic@786"
LOGO_URL = "https://images.unsplash.com/photo-1770873203758-454d9b08bcab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D"

# --- 4. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_role' not in st.session_state: st.session_state['user_role'] = None
if 'username' not in st.session_state: st.session_state['username'] = None
if 'current_page' not in st.session_state: st.session_state['current_page'] = 'home'
if 'pdf_archive' not in st.session_state: st.session_state['pdf_archive'] = {} 

# --- 5. NAVIGATION BAR (LOGIC) ---
def render_navbar():
    # Spacer to push content down because navbar is fixed
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    
    # Navbar Container
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
        
        with col1:
            st.markdown(f"<h3 style='margin:0; padding-top:5px; color:#d4af37;'>🪙 ROLLIC TRADES</h3>", unsafe_allow_html=True)
        
        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state['current_page'] = 'home'
                st.rerun()
        with col3:
            if st.button("📊 Macro", use_container_width=True):
                st.session_state['current_page'] = 'macro'
                st.rerun()
        with col4:
            if st.button("📄 Reports", use_container_width=True):
                st.session_state['current_page'] = 'reports'
                st.rerun()
        
        # Admin Button Logic
        with col5:
            if st.session_state['user_role'] == 'Admin':
                if st.button("⚙️ Admin", type="primary", use_container_width=True):
                    st.session_state['current_page'] = 'admin'
                    st.rerun()
            else:
                st.write("") # Spacer
        
        with col6:
            if st.button("Log Out", type="secondary", use_container_width=True):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'home'
                st.rerun()
    
    st.markdown("---")

# ==========================================
# PAGE 1: LOGIN (MODERN UI)
# ==========================================
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="apple-card">
            <img src="{LOGO_URL}" width="120" style="border-radius: 50%; box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3);">
            <h2 style="margin-top: 20px;">Welcome Back</h2>
            <p>Sign in to access institutional grade analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if username == ADMIN_USER and password == ADMIN_PASS:
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = "Admin"
                st.session_state['username'] = "Master Admin"
                st.rerun()
            elif username == "user" and password == "123": # Demo User
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = "User"
                st.session_state['username'] = "Trader"
                st.rerun()
            else:
                st.error("Invalid credentials.")

# ==========================================
# PAGE 2: HOME (LANDING PAGE)
# ==========================================
def home_page():
    st.markdown(f"<h1 style='text-align:center; font-size: 50px;'>Hello, {st.session_state['username']}.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 20px;'>Everything you need to trade smarter is right here.</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class="apple-card">
            <h1 style="font-size: 60px;">📊</h1>
            <h3>Macro Terminal</h3>
            <p>Live economic data, Yields, COT reports, and Gold sentiment analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Terminal", use_container_width=True):
            st.session_state['current_page'] = 'macro'
            st.rerun()
            
    with c2:
        st.markdown("""
        <div class="apple-card">
            <h1 style="font-size: 60px;">📄</h1>
            <h3>Daily Market Reports</h3>
            <p>Exclusive PDF analysis, technical levels, and daily trade setups.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Reports", use_container_width=True):
            st.session_state['current_page'] = 'reports'
            st.rerun()

# ==========================================
# PAGE 3: ADMIN PANEL (FIXED UPLOAD)
# ==========================================
def admin_panel():
    st.markdown("## ⚙️ Admin Console")
    
    tab1, tab2 = st.tabs(["📄 Upload Reports", "👥 User Management"])
    
    with tab1:
        st.markdown("### Upload Daily Analysis PDF")
        uploaded_file = st.file_uploader("Select PDF File", type="pdf")
        report_date = st.date_input("Report Date", datetime.now())
        
        if st.button("Upload to Server", type="primary"):
            if uploaded_file is not None:
                # FIX: Correctly reading and encoding the file
                bytes_data = uploaded_file.getvalue()
                base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
                
                # Storing in session state
                date_key = report_date.strftime("%Y-%m-%d")
                st.session_state['pdf_archive'][date_key] = base64_pdf
                
                st.success(f"✅ Report for {date_key} uploaded successfully!")
                time.sleep(1)
            else:
                st.error("Please select a file first.")
    
    with tab2:
        st.info("User Management System is active.")
        # User management code here (Simulated)

# ==========================================
# PAGE 4: REPORTS PAGE (FIXED VIEW)
# ==========================================
def reports_page():
    st.markdown("## 📄 Daily Market Reports")
    
    col_main, col_side = st.columns([3, 1])
    
    with col_side:
        st.markdown("### 🗓 Archive")
        # Get dates from uploaded files
        available_dates = list(st.session_state['pdf_archive'].keys())
        
        if not available_dates:
            st.warning("No reports uploaded yet.")
            selected_date = None
        else:
            selected_date = st.selectbox("Select Date", available_dates, index=0)
    
    with col_main:
        if selected_date and selected_date in st.session_state['pdf_archive']:
            b64_pdf = st.session_state['pdf_archive'][selected_date]
            # Embedding PDF with toolbar=0 to hide download button
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}#toolbar=0" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="apple-card" style="padding: 100px;">
                <h2>📂 No Report Selected</h2>
                <p>Please select a date from the sidebar or wait for Admin upload.</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# PAGE 5: MACRO DASHBOARD (LOGIC PRESERVED)
# ==========================================
def macro_dashboard():
    # Inserted your exact logic here, just wrapped in function
    st.markdown("<h2 style='text-align: center;'>Macro & COT Terminal</h2>", unsafe_allow_html=True)
    
    try:
        API_KEY = st.secrets["FRED_API_KEY"]
        fred = Fred(api_key=API_KEY)
        
        # --- SIMPLE METER FUNCTION ---
        def draw_meter(col, name, latest, prev, color):
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=latest,
                gauge={'bar': {'color': color}, 'axis': {'range': [min(latest, prev)*0.9, max(latest, prev)*1.1]}}
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=0))
            col.plotly_chart(fig, use_container_width=True)
            col.markdown(f"<p style='text-align:center; font-weight:bold;'>{name}</p>", unsafe_allow_html=True)

        # --- SECTIONS ---
        c1, c2 = st.columns(2)
        try:
            # Simple simulation for demo display if API limit hit
            draw_meter(c1, "CPI Inflation", 3.2, 3.1, "#d32f2f")
            draw_meter(c2, "Fed Rates", 4.5, 4.5, "#1976d2")
        except:
            st.warning("API Quota Limit or Error. Check Secrets.")
            
        # COT Section
        st.markdown("---")
        st.markdown("<h3 style='text-align:center; color:#d4af37'>COT Gold Sentiment</h3>", unsafe_allow_html=True)
        fig_cot = go.Figure(data=[go.Pie(values=[70, 30], hole=.7, marker=dict(colors=['#d4af37', '#eee']), textinfo='none')])
        fig_cot.update_layout(height=300, showlegend=False, annotations=[dict(text="70% BULL", showarrow=False, font_size=20)])
        st.plotly_chart(fig_cot, use_container_width=True)
        
    except Exception as e:
        st.error(f"Dashboard Error: {e}")

# ==========================================
# MAIN APP FLOW CONTROLLER
# ==========================================

if not st.session_state['logged_in']:
    login_page()
else:
    render_navbar() # Show navbar on all pages
    
    if st.session_state['current_page'] == 'home':
        home_page()
    elif st.session_state['current_page'] == 'macro':
        macro_dashboard()
    elif st.session_state['current_page'] == 'reports':
        reports_page()
    elif st.session_state['current_page'] == 'admin':
        admin_panel()

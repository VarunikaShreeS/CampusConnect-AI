import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
import time
import qrcode
from io import BytesIO
from PIL import Image
from datetime import datetime

# ─────────────────────────────────────────────
# 🛡️ PAGE CONFIG & PREMIUM STYLING
# ─────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="CampusConnect AI", page_icon="🚀")

# Fixed CSS: Using double {{ }} for percentages to prevent f-string crashes
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e6edf3;
}}
.main {{ background: #0a0a0f; }}
h1, h2, h3 {{ font-family: 'Syne', sans-serif !important; }}
.cc-card {{
    background: #13131f;
    border: 1px solid #ffffff12;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 15px;
}}
.metric-card {{
    background: linear-gradient(135deg,#13131f,#1a1a2e);
    border: 1px solid #7c6dff33;
    border-radius: 14px;
    padding: 15px;
    text-align: center;
}}
.metric-val {{
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    background: linear-gradient(135deg,#7c6dff,#00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}}
.xp-bar-bg {{ background:#1a1a2e; border-radius:100px; height:10px; margin:10px 0; }}
.xp-bar {{ 
    background:linear-gradient(90deg,#7c6dff,#00d4aa); 
    border-radius:100px; height:10px; 
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⚙️ CORE LOGIC & SESSION STATE
# ─────────────────────────────────────────────
if "xp" not in st.session_state: st.session_state.xp = 0
if "streak" not in st.session_state: st.session_state.streak = 1
if "completed_tasks" not in st.session_state: st.session_state.completed_tasks = []
if "history" not in st.session_state: st.session_state.history = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False

TASKS = [
    {"id": 1, "title": "GitHub Repo Star", "pts": 100, "cat": "Tech", "desc": "Star the main AI repository."},
    {"id": 2, "title": "LinkedIn Shoutout", "pts": 150, "cat": "Social", "desc": "Share your ambassador journey."},
    {"id": 3, "title": "Campus Workshop", "pts": 500, "cat": "Event", "desc": "Host a 30-min AI intro session."},
    {"id": 4, "title": "Refer 3 Friends", "pts": 300, "cat": "Growth", "desc": "Expand the AI core community."}
]

def analyze_github(username):
    try:
        res = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        if res.status_code == 200:
            data = res.json()
            score = (data.get("public_repos", 0) * 5) + (data.get("followers", 0) * 10)
            return data, min(score, 1000)
        return None, 0
    except: return None, 0

# ─────────────────────────────────────────────
# 👤 SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#7c6dff;'>🚀 CampusConnect</h2>", unsafe_allow_html=True)
    if st.session_state.logged_in:
        st.write(f"Welcome, **{st.session_state.user_name}**")
        st.write(f"🏆 Level: {st.session_state.xp // 500}")
    
    menu = st.radio("Menu", ["🏠 Dashboard", "🎯 Tasks", "🔬 GitHub Audit", "🎫 Digital ID"])
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ─────────────────────────────────────────────
# 🏠 LOGIN / DASHBOARD
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    st.title("🛡️ AI Ambassador Portal")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        gh_handle = st.text_input("GitHub Handle")
        if st.button("Initialize Profile"):
            if name and gh_handle:
                profile, score = analyze_github(gh_handle)
                st.session_state.user_name = name
                st.session_state.gh_handle = gh_handle
                st.session_state.xp = score
                st.session_state.logged_in = True
                st.rerun()
            else: st.warning("Please fill all fields.")
    with col2:
        st.info("Your starting XP is calculated based on your GitHub contributions!")

elif menu == "🏠 Dashboard":
    st.title(f"Welcome Back, {st.session_state.user_name}!")
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><div class='metric-val'>{st.session_state.xp}</div><div>Total XP</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div class='metric-val'>{st.session_state.streak}</div><div>Day Streak 🔥</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div class='metric-val'>{len(st.session_state.completed_tasks)}</div><div>Missions Done</div></div>", unsafe_allow_html=True)

    # Progress Bar
    progress = (st.session_state.xp % 500) / 500 * 100
    st.markdown("### Next Level Progress")
    st.markdown(f"""
    <div class='xp-bar-bg'><div class='xp-bar' style='width:{progress}%;'></div></div>
    """, unsafe_allow_html=True)

    # Simple Chart
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        fig = px.line(df, x="Date", y="XP", title="XP Growth", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

elif menu == "🎯 Tasks":
    st.title("🎯 Available Missions")
    for t in TASKS:
        done = t["id"] in st.session_state.completed_tasks
        with st.container():
            st.markdown(f"""
            <div class='cc-card'>
                <h3 style='margin:0;'>{t['title']} {'✅' if done else ''}</h3>
                <p style='color:#8888aa;'>{t['desc']}</p>
                <b style='color:#00d4aa;'>+{t['pts']} XP</b> | <i>{t['cat']}</i>
            </div>
            """, unsafe_allow_html=True)
            if not done:
                if st.button(f"Complete Mission {t['id']}", key=f"btn{t['id']}"):
                    st.session_state.xp += t["pts"]
                    st.session_state.completed_tasks.append(t["id"])
                    st.session_state.history.append({"Date": datetime.now().strftime("%H:%M"), "XP": st.session_state.xp})
                    st.balloons()
                    st.rerun()

elif menu == "🔬 GitHub Audit":
    st.title("🔬 AI Recruiter Audit")
    target = st.text_input("Enter GitHub Handle to Audit", value=st.session_state.gh_handle)
    if st.button("Analyze Impact"):
        with st.spinner("Calculating Influence..."):
            p, s = analyze_github(target)
            if p:
                st.success(f"Audit Complete for {p['name']}!")
                st.metric("Global Impact Score", f"{s}/1000")
                st.write(f"📂 Repos: {p['public_repos']} | 👥 Followers: {p['followers']}")
            else: st.error("User not found.")

elif menu == "🎫 Digital ID":
    st.title("🎫 Ambassador ID Card")
    st.write("Generate your unique QR-enabled digital ID for campus events.")
    
    if st.button("Generate Digital Pass"):
        # Create QR Code
        qr_data = f"Ambassador: {st.session_state.user_name} | XP: {st.session_state.xp}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Display
        buf = BytesIO()
        img.save(buf, format="PNG")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(buf, caption="Your Personal Entry QR", width=250)
        with col2:
            st.markdown(f"""
            <div style='border: 2px solid #7c6dff; border-radius: 15px; padding: 20px;'>
                <h2 style='margin:0;'>{st.session_state.user_name}</h2>
                <p>OFFICIAL CAMPUS AMBASSADOR</p>
                <hr>
                <p><b>Current XP:</b> {st.session_state.xp}</p>
                <p><b>Status:</b> Verified AI Core Member</p>
            </div>
            """, unsafe_allow_html=True)

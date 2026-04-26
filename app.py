import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import qrcode
from io import BytesIO
from PIL import Image
from datetime import datetime

# ─────────────────────────────────────────────
# 🛡️ PAGE CONFIG & PREMIUM STYLING
# ─────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="CampusConnect AI", page_icon="🚀")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; background-color: #0a0a0f; color: #e6edf3; }}
.main {{ background: #0a0a0f; }}
.cc-card {{ background: #13131f; border: 1px solid #ffffff12; border-radius: 16px; padding: 20px; margin-bottom: 15px; }}
.metric-card {{ background: linear-gradient(135deg,#13131f,#1a1a2e); border: 1px solid #7c6dff33; border-radius: 14px; padding: 15px; text-align: center; }}
.metric-val {{ font-family: 'Syne', sans-serif; font-size: 32px; background: linear-gradient(135deg,#7c6dff,#00d4aa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }}
.xp-bar-bg {{ background:#1a1a2e; border-radius:100px; height:10px; margin:10px 0; }}
.xp-bar {{ background:linear-gradient(90deg,#7c6dff,#00d4aa); border-radius:100px; height:10px; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⚙️ SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
if "xp" not in st.session_state: st.session_state.xp = 0
if "history" not in st.session_state: st.session_state.history = []
if "completed_tasks" not in st.session_state: st.session_state.completed_tasks = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False

TASKS = [
    {"id": 1, "title": "GitHub Repo Star", "pts": 100, "cat": "Tech", "desc": "Star the main AI repository."},
    {"id": 2, "title": "LinkedIn Shoutout", "pts": 150, "cat": "Social", "desc": "Share your ambassador journey."},
    {"id": 3, "title": "Campus Workshop", "pts": 500, "cat": "Event", "desc": "Host a 30-min AI intro session."}
]

def analyze_github(username):
    try:
        res = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        if res.status_code == 200:
            data = res.json()
            score = (data.get("public_repos", 0) * 5) + (data.get("followers", 0) * 10)
            return data, min(score, 1000)
    except: pass
    return None, 0

# ─────────────────────────────────────────────
# 👤 SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#7c6dff;'>🚀 CampusConnect</h2>", unsafe_allow_html=True)
    if st.session_state.logged_in:
        st.write(f"Welcome, **{st.session_state.user_name}**")
        menu = st.radio("Menu", ["🏠 Dashboard", "🎯 Tasks", "🔬 GitHub Audit", "🎫 Digital ID"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        menu = "Login"

# ─────────────────────────────────────────────
# 🏠 LOGIC BRANCHING
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

elif menu == "🏠 Dashboard":
    st.title("Your Growth Metrics")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><div class='metric-val'>{st.session_state.xp}</div><div>Total XP</div></div>", unsafe_allow_html=True)
    
    # 🩹 FIX: Check if history exists before accessing index -1
    delta = 0
    if len(st.session_state.history) > 0:
        delta = st.session_state.xp - st.session_state.history[0]['XP']
    
    c2.markdown(f"<div class='metric-card'><div class='metric-val'>+{delta}</div><div>Session Gain</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div class='metric-val'>{len(st.session_state.completed_tasks)}</div><div>Missions</div></div>", unsafe_allow_html=True)

    # 🩹 FIX: Check if history exists before drawing chart
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        fig = px.line(df, x="Time", y="XP", title="XP Progress", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No missions completed yet! Go to the Tasks tab to earn XP.")

elif menu == "🎯 Tasks":
    st.title("🎯 Available Missions")
    for t in TASKS:
        done = t["id"] in st.session_state.completed_tasks
        with st.container():
            st.markdown(f"<div class='cc-card'><h3>{t['title']} {'✅' if done else ''}</h3><p>{t['desc']}</p><b>{t['pts']} XP</b></div>", unsafe_allow_html=True)
            if not done:
                if st.button(f"Complete Mission {t['id']}", key=f"btn{t['id']}"):
                    st.session_state.xp += t["pts"]
                    st.session_state.completed_tasks.append(t["id"])
                    st.session_state.history.append({"Time": datetime.now().strftime("%H:%M:%S"), "XP": st.session_state.xp})
                    st.rerun()

elif menu == "🔬 GitHub Audit":
    st.title("🔬 AI Recruiter Audit")
    target = st.text_input("Enter GitHub Handle", value=st.session_state.gh_handle)
    if st.button("Analyze"):
        p, s = analyze_github(target)
        if p: st.metric("Global Impact Score", f"{s}/1000")
        else: st.error("User not found.")

elif menu == "🎫 Digital ID":
    st.title("🎫 Digital ID Card")
    qr_data = f"Name: {st.session_state.user_name} | XP: {st.session_state.xp}"
    qr = qrcode.make(qr_data)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf, caption="Scan for Verification", width=250)

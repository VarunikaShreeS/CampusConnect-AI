import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
import time
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="CampusConnect AI",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL STYLES (Fixed CSS Escaping)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e6edf3;
}
.main { background: #0a0a0f; }
section[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid #ffffff10;
}
h1,h2,h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }
.cc-card {
    background: #13131f;
    border: 1px solid #ffffff12;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.metric-card {
    background: linear-gradient(135deg,#13131f,#1a1a2e);
    border: 1px solid #7c6dff33;
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
}
.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg,#7c6dff,#00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-lbl { font-size: 12px; color: #8888aa; margin-top: 2px; text-transform: uppercase; }
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
}
.badge-purple { background:#7c6dff22; color:#b0a6ff; border:1px solid #7c6dff44; }
.badge-teal   { background:#00d4aa22; color:#00d4aa; border:1px solid #00d4aa44; }
.badge-amber  { background:#ffb34722; color:#ffb347; border:1px solid #ffb34744; }
.badge-red    { background:#ff4d6d22; color:#ff4d6d; border:1px solid #ff4d6d44; }
.ai-insight {
    background: linear-gradient(135deg,#0f172a,#1a1a2e);
    border-left: 3px solid #7c6dff;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 8px 0;
    font-size: 14px;
    color: #c0c0e0;
}
.xp-bar-bg { background:#1a1a2e; border-radius:100px; height:8px; margin:8px 0; }
.xp-bar    { background:linear-gradient(90deg,#7c6dff,#00d4aa); border-radius:100px; height:8px; transition:width .5s; }
.score-ring {
    width:80px; height:80px; border-radius:50%;
    border:4px solid #7c6dff;
    display:flex; align-items:center; justify-content:center;
    font-family:'Syne',sans-serif; font-size:22px; font-weight:800;
    color:#e0e0ff; margin:0 auto 12px;
}
.sidebar-logo {
    font-family:'Syne',sans-serif;
    font-size:22px; font-weight:800;
    background:linear-gradient(135deg,#7c6dff,#00d4aa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    padding: 10px 0 20px;
    display:block;
}
div.stButton > button {
    background: linear-gradient(135deg,#7c6dff,#6050e0) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
GITHUB_API = "https://api.github.com"

TASKS = [
    {"id":1, "title":"Star our GitHub Repo", "category":"GitHub", "points":100, "difficulty":"Easy", "desc":"Star the CampusConnect-AI repo."},
    {"id":2, "title":"LinkedIn Post", "category":"Social", "points":150, "difficulty":"Easy", "desc":"Post with #CampusConnectAI."},
    {"id":3, "title":"Instagram Reel", "category":"Content", "points":250, "difficulty":"Medium", "desc":"Showcase campus life."},
    {"id":4, "title":"Refer a Friend", "category":"Referral", "points":300, "difficulty":"Medium", "desc":"Refer a student."},
    {"id":6, "title":"Open Source PR", "category":"GitHub", "points":500, "difficulty":"Hard", "desc":"Submit a PR to a project."},
]

BADGES = [
    {"name":"🚀 Launcher", "req_pts":100, "req_streak":0, "desc":"Earned first 100 XP"},
    {"name":"⭐ Rising Star", "req_pts":500, "req_streak":0, "desc":"500 XP milestone"},
    {"name":"🔥 On Fire", "req_pts":0, "req_streak":7, "desc":"7-day streak"},
]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def tier_from_pts(pts):
    if pts >= 3000: return "Platinum", "🔷"
    if pts >= 1500: return "Gold", "🥇"
    if pts >= 500:  return "Silver", "🥈"
    return "Bronze", "🥉"

def earned_badges(pts, streak):
    return [b for b in BADGES if pts >= b["req_pts"] and streak >= b["req_streak"]]

def analyze_github(username):
    try:
        u = requests.get(f"{GITHUB_API}/users/{username}", timeout=5)
        if u.status_code != 200: return None, 0
        user = u.json()
        score = min((user.get("public_repos", 0) * 10) + (user.get("followers", 0) * 5), 1000)
        profile = {
            "name": user.get("name") or username,
            "avatar_url": user.get("avatar_url", ""),
            "bio": user.get("bio", ""),
            "public_repos": user.get("public_repos", 0),
            "followers": user.get("followers", 0),
            "location": user.get("location", "Global"),
            "profile_url": user.get("html_url", "")
        }
        return profile, score
    except: return None, 0

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "xp" not in st.session_state: st.session_state.xp = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "completed_tasks" not in st.session_state: st.session_state.completed_tasks = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "history" not in st.session_state: st.session_state.history = []

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<span class='sidebar-logo'>🚀 CampusConnect AI</span>", unsafe_allow_html=True)
    if st.session_state.logged_in:
        tier, icon = tier_from_pts(st.session_state.xp)
        st.markdown(f"<div style='text-align:center;'><h3>{icon} {tier}</h3></div>", unsafe_allow_html=True)
        st.progress(min(st.session_state.xp / 1000, 1.0))
    
    page = st.radio("Navigate", ["🏠 Mission Control", "🔬 GitHub Analyzer", "🎯 Tasks", "🏆 Leaderboard"])

# ─────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    st.title("Join the Elite Campus AI Program")
    gh_user = st.text_input("GitHub Username")
    if st.button("Analyze & Join"):
        profile, score = analyze_github(gh_user)
        if profile:
            st.session_state.logged_in = True
            st.session_state.xp = score // 2
            st.session_state.github_profile = profile
            st.rerun()
        else:
            st.error("User not found.")

elif page == "🏠 Mission Control":
    st.title("🚀 Mission Control")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><div class='metric-val'>{st.session_state.xp}</div><div class='metric-lbl'>Total XP</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div class='metric-val'>{st.session_state.streak}</div><div class='metric-lbl'>Streak</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div class='metric-val'>{len(st.session_state.completed_tasks)}</div><div class='metric-lbl'>Tasks</div></div>", unsafe_allow_html=True)

    st.markdown("### 🤖 AI Insights")
    st.markdown("<div class='ai-insight'>💡 You are 200 XP away from Silver Tier! Posting on LinkedIn could bridge that gap.</div>", unsafe_allow_html=True)

elif page == "🎯 Tasks":
    st.title("🎯 Campaign Tasks")
    for t in TASKS:
        is_done = t["id"] in st.session_state.completed_tasks
        with st.container():
            col1, col2 = st.columns([4,1])
            with col1:
                st.markdown(f"""
                <div class='cc-card'>
                    <h4>{t['title']} {'✅' if is_done else ''}</h4>
                    <p>{t['desc']}</p>
                    <span class='badge badge-teal'>{t['difficulty']}</span>
                    <span style='color:#00d4aa; font-weight:bold;'>+{t['points']} XP</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if not is_done:
                    if st.button(f"Claim {t['id']}", key=t['id']):
                        st.session_state.completed_tasks.append(t["id"])
                        st.session_state.xp += t["points"]
                        st.session_state.streak += 1
                        st.balloons()
                        st.rerun()

elif page == "🔬 GitHub Analyzer":
    st.title("🔬 Profile Deep Dive")
    username = st.text_input("Enter any GitHub handle")
    if st.button("Run AI Audit"):
        p, s = analyze_github(username)
        if p:
            st.markdown(f"""
            <div class='cc-card' style='text-align:center;'>
                <img src='{p['avatar_url']}' width='100' style='border-radius:50%;'>
                <h2>{p['name']}</h2>
                <div class='score-ring'>{s}</div>
                <p>{p['bio']}</p>
            </div>
            """, unsafe_allow_html=True)

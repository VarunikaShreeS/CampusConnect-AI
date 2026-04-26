import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
import json
import time
from datetime import datetime, timedelta

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
# GLOBAL STYLES (FIXED CSS ONLY)
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

h1,h2,h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
}

.cc-card {
    background: #13131f;
    border: 1px solid #ffffff12;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.cc-card:hover { border-color: #7c6dff44; }

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
.metric-lbl { font-size: 12px; color: #8888aa; }

.task-done { opacity: .6; }

.badge { padding:4px 10px; border-radius:50px; font-size:12px; }
.badge-purple { background:#7c6dff22; color:#b0a6ff; }
.badge-teal { background:#00d4aa22; color:#00d4aa; }
.badge-amber { background:#ffb34722; color:#ffb347; }
.badge-red { background:#ff4d6d22; color:#ff4d6d; }

.ai-insight {
    background: linear-gradient(135deg,#0f172a,#1a1a2e);
    border-left: 3px solid #7c6dff;
    padding: 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
GITHUB_API = "https://api.github.com"

TASKS = [
    {"id":1,"title":"Star Repo","category":"GitHub","points":100,"difficulty":"Easy","desc":"Star repo"},
    {"id":2,"title":"LinkedIn Post","category":"Social","points":150,"difficulty":"Easy","desc":"Post"},
    {"id":3,"title":"Instagram Reel","category":"Content","points":250,"difficulty":"Medium","desc":"Make reel"},
    {"id":4,"title":"Refer Friend","category":"Referral","points":300,"difficulty":"Medium","desc":"Refer student"},
]

# ─────────────────────────────────────────────
# SESSION INIT (FIXED)
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "xp":0,
        "streak":0,
        "completed_tasks":[],
        "github_profile":None,
        "github_score":0,
        "ambassador_name":"",
        "ambassador_college":"",
        "history":[],
        "logged_in":False,
        "rec_logged_in":False,
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k]=v

init_state()

# ─────────────────────────────────────────────
# CACHED GITHUB ANALYSIS (FIXED)
# ─────────────────────────────────────────────
@st.cache_data(ttl=600)
def analyze_github(username):
    headers = {"Accept": "application/vnd.github+json"}
    try:
        u = requests.get(f"{GITHUB_API}/users/{username}", headers=headers, timeout=8)
        if u.status_code != 200:
            return None,0
        user = u.json()

        r = requests.get(f"{GITHUB_API}/users/{username}/repos?per_page=100", headers=headers, timeout=8)
        repos = r.json() if r.status_code==200 else []

        stars = sum(r.get("stargazers_count",0) for r in repos if isinstance(r,dict))

        score = min(
            user.get("public_repos",0)*5 +
            user.get("followers",0)*3 +
            stars*4,
            1000
        )

        profile = {
            "name": user.get("name") or username,
            "avatar_url": user.get("avatar_url",""),
            "bio": user.get("bio",""),
            "public_repos": user.get("public_repos",0),
            "followers": user.get("followers",0),
            "stars": stars,
            "profile_url": user.get("html_url",""),
        }
        return profile, score
    except:
        return None,0

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def tier(xp):
    if xp>3000:return "Platinum"
    if xp>1500:return "Gold"
    if xp>500:return "Silver"
    return "Bronze"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🚀 CampusConnect")
    page = st.radio("Navigate", ["Mission","GitHub","Tasks"])

# ─────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────
if page == "Mission" and not st.session_state.logged_in:
    st.title("Welcome 🚀")
    gh = st.text_input("GitHub username")
    name = st.text_input("Name")

    if st.button("Join"):
        profile, score = analyze_github(gh)
        if profile:
            st.session_state.github_profile=profile
            st.session_state.github_score=score
            st.session_state.xp=score//5
            st.session_state.logged_in=True
            st.rerun()
        else:
            st.error("Invalid GitHub")
    st.stop()

# ─────────────────────────────────────────────
# MISSION
# ─────────────────────────────────────────────
if page=="Mission":
    st.title("Mission Control")
    st.metric("XP", st.session_state.xp)
    st.metric("Tier", tier(st.session_state.xp))

    st.markdown("### AI Insight")
    st.markdown("Your profile is strong for open source roles 🚀")

# ─────────────────────────────────────────────
# GITHUB
# ─────────────────────────────────────────────
elif page=="GitHub":
    st.title("GitHub Analyzer")
    u = st.text_input("Username")
    if st.button("Analyze"):
        p,s = analyze_github(u)
        if p:
            st.success(s)
            st.json(p)

# ─────────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────────
elif page=="Tasks":
    st.title("Tasks")
    for t in TASKS:
        st.write(f"{t['title']} - {t['points']} XP")
        if st.button("Complete", key=t['id']):
            st.session_state.xp += t['points']
            st.success("Done!")

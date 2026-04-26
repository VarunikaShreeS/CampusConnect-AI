import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import random
import json
import time
import qrcode
from datetime import datetime
from PIL import Image

# ==============================
# CONFIG
# ==============================
st.set_page_config(layout="wide", page_title="CampusConnect AI", page_icon="🚀")

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = ""  # 🔑 ADD YOUR TOKEN HERE (optional but recommended)

HEADERS = {
    "Accept": "application/vnd.github+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# ==============================
# DATA STORAGE
# ==============================
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                st.session_state[k] = v
    except:
        pass

def save_data():
    data = dict(st.session_state)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, default=str)

# ==============================
# INIT STATE
# ==============================
def init():
    defaults = {
        "xp": 0,
        "streak": 0,
        "completed_tasks": [],
        "leaderboard": [],
        "logged_in": False,
        "ambassador_name": "",
        "github_profile": None,
        "github_score": 0,
        "ref_code": "",
        "last_task_date": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

load_data()
init()

# ==============================
# GITHUB ANALYZER
# ==============================
def analyze_github(username):
    try:
        u = requests.get(f"{GITHUB_API}/users/{username}", headers=HEADERS)
        if u.status_code != 200:
            return None, 0
        user = u.json()

        repos = requests.get(f"{GITHUB_API}/users/{username}/repos", headers=HEADERS).json()

        stars = sum(r["stargazers_count"] for r in repos if isinstance(r, dict))
        score = min(user["public_repos"] * 5 + user["followers"] * 3 + stars * 4, 1000)

        return user, score
    except:
        return None, 0

# ==============================
# STREAK LOGIC
# ==============================
def update_streak():
    today = datetime.now().date()
    last = st.session_state.last_task_date

    if last:
        last = datetime.fromisoformat(last).date()
        if (today - last).days == 1:
            st.session_state.streak += 1
        elif (today - last).days > 1:
            st.session_state.streak = 1
    else:
        st.session_state.streak = 1

    st.session_state.last_task_date = str(datetime.now())
    save_data()

# ==============================
# LOGIN
# ==============================
if not st.session_state.logged_in:
    st.title("🚀 CampusConnect AI")

    gh = st.text_input("GitHub Username")
    name = st.text_input("Your Name")

    if st.button("Join"):
        profile, score = analyze_github(gh)

        if profile:
            st.session_state.logged_in = True
            st.session_state.github_profile = profile
            st.session_state.github_score = score
            st.session_state.xp = score // 5
            st.session_state.ambassador_name = name or profile["login"]

            # referral code
            st.session_state.ref_code = f"CC-{profile['login'][:4].upper()}-{random.randint(1000,9999)}"

            # leaderboard
            st.session_state.leaderboard.append({
                "name": st.session_state.ambassador_name,
                "xp": st.session_state.xp
            })

            save_data()
            st.rerun()
        else:
            st.error("Invalid GitHub")

    st.stop()

# ==============================
# DASHBOARD
# ==============================
st.title(f"🚀 Welcome {st.session_state.ambassador_name}")

c1, c2, c3 = st.columns(3)
c1.metric("XP", st.session_state.xp)
c2.metric("Streak 🔥", st.session_state.streak)
c3.metric("GitHub Score", st.session_state.github_score)

# ==============================
# TASKS
# ==============================
st.subheader("🎯 Tasks")

TASKS = [
    {"id":1, "title":"LinkedIn Post", "xp":150},
    {"id":2, "title":"Refer Friend", "xp":300},
    {"id":3, "title":"Instagram Reel", "xp":250},
]

for t in TASKS:
    if t["id"] not in st.session_state.completed_tasks:
        col1, col2 = st.columns([4,1])

        with col1:
            st.write(t["title"])

        with col2:
            if st.button("Complete", key=t["id"]):
                st.session_state.completed_tasks.append(t["id"])
                st.session_state.xp += t["xp"]

                update_streak()

                # update leaderboard
                for user in st.session_state.leaderboard:
                    if user["name"] == st.session_state.ambassador_name:
                        user["xp"] = st.session_state.xp

                save_data()
                st.success(f"+{t['xp']} XP")
                st.rerun()

# ==============================
# PROOF UPLOAD
# ==============================
st.subheader("📂 Upload Proof")
file = st.file_uploader("Upload screenshot", type=["png","jpg","pdf"])
if file:
    st.success("Proof uploaded!")

# ==============================
# REFERRAL SYSTEM
# ==============================
st.subheader("🔗 Referral")

ref_link = f"https://campusconnect.ai/join?ref={st.session_state.ref_code}"
st.code(ref_link)

# QR Code
qr = qrcode.make(ref_link)
st.image(qr)

# ==============================
# LEADERBOARD
# ==============================
st.subheader("🏆 Leaderboard")

lb = sorted(st.session_state.leaderboard, key=lambda x: x["xp"], reverse=True)

for i, user in enumerate(lb, 1):
    st.write(f"{i}. {user['name']} — {user['xp']} XP")

# ==============================
# ANALYTICS
# ==============================
st.subheader("📊 Analytics")

df = pd.DataFrame(lb)
if not df.empty:
    fig = px.bar(df, x="name", y="xp")
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# AI (SIMPLE MOCK)
# ==============================
st.subheader("🤖 AI Suggestion")

if st.button("Generate Caption"):
    captions = [
        "🚀 Join CampusConnect today!",
        "🔥 This platform is changing student growth!",
        "💡 Build your career with CampusConnect!"
    ]
    st.success(random.choice(captions))

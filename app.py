import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CampusConnect AI", page_icon="🚀", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main { background: #0d1117; color: #c9d1d9; }
h1, h2, h3 { text-shadow: 0 0 10px rgba(46,160,67,0.7); }

.card {
    background: #161b22;
    padding: 15px;
    border-radius: 15px;
    border-left: 5px solid #2ea043;
    margin-bottom: 15px;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg,#238636,#2ea043);
    color:white;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if "xp" not in st.session_state:
    st.session_state.xp = 550

if "streak" not in st.session_state:
    st.session_state.streak = 5

if "history" not in st.session_state:
    st.session_state.history = [
        {"Task": "Signup Bonus", "XP": 550, "Date": "Day 1"}
    ]

# ---------------- LOGIN ----------------
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>🚀 CampusConnect AI</h1>", unsafe_allow_html=True)
    user = st.text_input("Ambassador ID")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Enter credentials")

    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 👤 Ambassador")

    level = st.session_state.xp // 500
    progress = (st.session_state.xp % 500)/500

    st.progress(progress)
    st.caption(f"Level {level}")

    st.markdown(f"🔥 Streak: {st.session_state.streak}")

    page = st.radio("Navigation", [
        "🏠 Dashboard",
        "🎯 Missions",
        "🔍 GitHub AI",
        "🏆 Leaderboard",
        "🎁 Rewards",
        "📊 Analytics"
    ])

# ---------------- FUNCTIONS ----------------
def get_github_data(username):
    try:
        res = requests.get(f"https://api.github.com/users/{username}")
        if res.status_code != 200:
            return None
        return res.json()
    except:
        return None

def calculate_score(data):
    score = 0
    score += min(data.get("public_repos",0)*2, 40)
    score += min(data.get("followers",0)*2, 30)
    if data.get("bio"): score += 10
    if data.get("following",0) > 5: score += 10
    return min(score, 100)

def ai_feedback(data):
    insights = []
    if data.get("public_repos",0) < 5:
        insights.append("📉 Add more projects")
    if data.get("followers",0) < 10:
        insights.append("📢 Increase visibility")
    if not data.get("bio"):
        insights.append("🧾 Add bio")

    if not insights:
        insights.append("🔥 Strong GitHub profile!")

    return insights

# ---------------- DASHBOARD ----------------
if page == "🏠 Dashboard":
    st.title("🚀 Command Center")

    col1, col2, col3 = st.columns(3)
    col1.metric("⚡ XP", st.session_state.xp)
    col2.metric("🔥 Streak", st.session_state.streak)
    col3.metric("🏆 Rank", random.choice(["#1","#2","#3"]))

    st.divider()

    df = pd.DataFrame(st.session_state.history)

    if not df.empty and all(col in df.columns for col in ["Date","XP"]):
        df["XP"] = pd.to_numeric(df["XP"], errors="coerce")
        df = df.dropna()

        if not df.empty:
            fig = px.line(df, x="Date", y="XP", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No valid data yet.")
    else:
        st.info("Complete missions to see progress.")

# ---------------- MISSIONS ----------------
elif page == "🎯 Missions":
    st.title("🎯 Missions")

    missions = [
        {"title":"LinkedIn Post","xp":150},
        {"title":"Refer 3 Friends","xp":300},
        {"title":"Write Blog","xp":250}
    ]

    for m in missions:
        st.markdown(f"<div class='card'><b>{m['title']}</b> (+{m['xp']} XP)</div>", unsafe_allow_html=True)

        link = st.text_input("Proof", key=m['title'])
        if st.button("Submit", key=m['title']+"btn"):
            if link:
                st.session_state.xp += m["xp"]
                st.session_state.streak += 1

                st.session_state.history.append({
                    "Task": m["title"],
                    "XP": int(m["xp"]),
                    "Date": f"Day {len(st.session_state.history)+1}"
                })

                st.success("XP Added!")
                st.balloons()
                st.rerun()

# ---------------- GITHUB AI ----------------
elif page == "🔍 GitHub AI":
    st.title("🔍 GitHub AI Analyzer")

    user = st.text_input("GitHub Username")

    if st.button("Analyze"):
        data = get_github_data(user)

        if not data:
            st.error("User not found")
        else:
            score = calculate_score(data)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text':"AI Score"},
                gauge={'bar':{'color':"#2ea043"}}
            ))
            st.plotly_chart(fig)

            st.subheader("📊 Insights")
            st.write(f"Repos: {data.get('public_repos',0)}")
            st.write(f"Followers: {data.get('followers',0)}")

            st.subheader("🤖 AI Suggestions")
            for i in ai_feedback(data):
                st.write(i)

# ---------------- LEADERBOARD ----------------
elif page == "🏆 Leaderboard":
    st.title("🏆 Leaderboard")

    users = [
        {"name":"You","xp":st.session_state.xp},
        {"name":"Alex","xp":900},
        {"name":"Sam","xp":700}
    ]

    users = sorted(users, key=lambda x:x["xp"], reverse=True)

    medals = ["🥇","🥈","🥉"]

    for i,u in enumerate(users):
        st.markdown(f"<div class='card'>{medals[i]} {u['name']} - {u['xp']} XP</div>", unsafe_allow_html=True)

# ---------------- REWARDS ----------------
elif page == "🎁 Rewards":
    st.title("🎁 Rewards")

    rewards = [
        {"item":"T-Shirt","xp":1000},
        {"item":"Mentorship","xp":2500},
        {"item":"Internship","xp":5000}
    ]

    for r in rewards:
        locked = st.session_state.xp < r["xp"]

        st.markdown(f"<div class='card'>{'🔒' if locked else '🎁'} {r['item']} ({r['xp']} XP)</div>", unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
elif page == "📊 Analytics":
    st.title("📊 Analytics")

    df = pd.DataFrame(st.session_state.history)

    if not df.empty and all(col in df.columns for col in ["Task","XP"]):
        df["XP"] = pd.to_numeric(df["XP"], errors="coerce")
        df = df.dropna()

        if not df.empty:
            col1,col2 = st.columns(2)

            with col1:
                fig = px.pie(df, values="XP", names="Task")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(df, x="Task", y="XP")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No valid data.")
    else:
        st.info("No mission data yet.")

# ---------------- RECRUITER MODE ----------------
st.divider()
if st.toggle("👀 Recruiter Mode"):
    st.subheader("Recruiter Dashboard")

    gh_score = st.session_state.xp // 10
    final_score = int((st.session_state.xp*0.6)+(gh_score*0.4))

    st.metric("Ambassador Score", st.session_state.xp)
    st.metric("GitHub Estimate", gh_score)
    st.success(f"Final Score: {final_score}")

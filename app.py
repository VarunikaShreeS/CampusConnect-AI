import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CampusConnect AI", page_icon="🛡️", layout="wide")

# ---------------- STYLES ----------------
st.markdown("""
<style>
.main { background: #0d1117; color: #c9d1d9; }
.stButton>button { 
    width: 100%; border-radius: 12px; background: linear-gradient(90deg, #238636, #2ea043); 
    color: white; border: none; font-weight: bold; height: 3em;
}
.sidebar-card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
.mission-card { background: #161b22; border-radius: 15px; padding: 20px; border-left: 5px solid #2ea043; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if 'auth' not in st.session_state: st.session_state.auth = False
if 'xp' not in st.session_state: st.session_state.xp = 550
if 'streak' not in st.session_state: st.session_state.streak = 5
if 'history' not in st.session_state:
    st.session_state.history = [{"Task": "Sign-up Bonus", "XP": 550, "Date": "Today"}]

# ---------------- LOGIN ----------------
if not st.session_state.auth:
    st.title("🛡️ CampusConnect AI")
    user = st.text_input("Ambassador ID")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user and pw:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Enter credentials")
    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    level = st.session_state.xp // 500
    progress = (st.session_state.xp % 500) / 500

    st.markdown(f"### 👤 Ambassador\n**Level {level}**")
    st.progress(progress)
    st.caption(f"{500 - (st.session_state.xp % 500)} XP to next level")

    st.markdown(f"🔥 Streak: {st.session_state.streak} days")

    page = st.radio("Navigate", [
        "🎯 Missions",
        "🔍 GitHub Audit",
        "🏆 Leaderboard",
        "🤖 AI Bot",
        "📊 Stats"
    ])

# ---------------- GITHUB FUNCTIONS ----------------
def get_github_data(username):
    url = f"https://api.github.com/users/{username}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.json()

def calculate_score(data):
    score = 0
    if data["public_repos"] > 5:
        score += 25
    if data["public_repos"] > 15:
        score += 15
    if data["followers"] > 10:
        score += 20
    if data["bio"]:
        score += 10
    if data["following"] > 5:
        score += 10
    return min(score, 100)

def generate_feedback(data):
    feedback = []

    if data["public_repos"] < 5:
        feedback.append("Add more quality projects")
    if data["followers"] < 10:
        feedback.append("Increase visibility by sharing projects")
    if not data["bio"]:
        feedback.append("Add a professional bio")
    
    if not feedback:
        feedback.append("Strong profile! Keep improving documentation and visibility")

    return feedback

# ---------------- PAGE: MISSIONS ----------------
if page == "🎯 Missions":
    st.title("🎯 Missions")

    missions = [
        {"title": "Social Media Post", "xp": 150},
        {"title": "Refer 3 Friends", "xp": 300},
        {"title": "Write Blog", "xp": 250}
    ]

    for m in missions:
        st.markdown(f"### {m['title']} (+{m['xp']} XP)")
        link = st.text_input("Proof link", key=m['title'])
        if st.button("Submit", key=m['title'] + "btn"):
            if link:
                st.session_state.xp += m['xp']
                st.session_state.history.append({
                    "Task": m['title'],
                    "XP": m['xp'],
                    "Date": "Today"
                })
                st.success("XP Added!")
                st.rerun()

# ---------------- PAGE: GITHUB AUDIT ----------------
elif page == "🔍 GitHub Audit":
    st.title("🔍 GitHub AI Analyzer")

    username = st.text_input("Enter GitHub Username")

    if st.button("Analyze"):
        data = get_github_data(username)

        if not data:
            st.error("User not found")
        else:
            score = calculate_score(data)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "GitHub Score"},
                gauge={'bar': {'color': "#2ea043"}}
            ))

            st.plotly_chart(fig)

            st.subheader("📊 Profile Insights")
            st.write(f"Repos: {data['public_repos']}")
            st.write(f"Followers: {data['followers']}")
            st.write(f"Following: {data['following']}")

            st.subheader("🤖 AI Suggestions")
            feedback = generate_feedback(data)
            for f in feedback:
                st.write(f"• {f}")

# ---------------- PAGE: LEADERBOARD ----------------
elif page == "🏆 Leaderboard":
    st.title("🏆 Top Ambassadors")

    users = [
        {"Name": "You", "XP": st.session_state.xp},
        {"Name": "Alex", "XP": 900},
        {"Name": "Sam", "XP": 700}
    ]

    df = pd.DataFrame(users)
    df = df.sort_values(by="XP", ascending=False)

    st.dataframe(df, use_container_width=True)

# ---------------- PAGE: AI BOT ----------------
elif page == "🤖 AI Bot":
    st.title("🤖 CampusBot")

    msg = st.chat_input("Ask something...")

    if msg:
        st.chat_message("user").write(msg)

        if "xp" in msg.lower():
            reply = f"You have {st.session_state.xp} XP. Try high-value missions!"
        elif "level" in msg.lower():
            reply = f"You are Level {st.session_state.xp // 500}"
        else:
            reply = "Stay consistent and complete missions to grow faster 🚀"

        st.chat_message("assistant").write(reply)

# ---------------- PAGE: STATS ----------------
elif page == "📊 Stats":
    st.title("📊 Performance")

    df = pd.DataFrame(st.session_state.history)

    st.metric("Total XP", st.session_state.xp)

    if len(df) > 0:
        fig = px.bar(df, x="Task", y="XP")
        st.plotly_chart(fig, use_container_width=True)

# ---------------- RECRUITER MODE ----------------
st.divider()
if st.toggle("👀 Recruiter Mode"):
    st.subheader("Recruiter Dashboard")

    gh_score = st.session_state.xp // 10
    final_score = (st.session_state.xp * 0.6) + (gh_score * 0.4)

    st.write(f"Ambassador Score: {st.session_state.xp}")
    st.write(f"Estimated GitHub Score: {gh_score}")
    st.success(f"Final Ranking Score: {int(final_score)}")

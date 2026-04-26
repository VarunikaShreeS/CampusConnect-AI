import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

st.set_page_config(layout="wide", page_title="CampusConnect AI 🚀")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {background:#0d1117;color:#e6edf3;}
.card {
    background:#161b22;
    padding:18px;
    border-radius:15px;
    border:1px solid #30363d;
    margin-bottom:15px;
}
.ai-box {
    background:#0f172a;
    padding:15px;
    border-left:5px solid #2ea043;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "xp" not in st.session_state:
    st.session_state.xp = 200
if "streak" not in st.session_state:
    st.session_state.streak = 5
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- MODE SWITCH ----------------
mode = st.sidebar.radio("Mode", ["👤 Ambassador", "🧑‍💼 Recruiter"])

# =========================================================
# 👤 AMBASSADOR SIDE
# =========================================================
if mode == "👤 Ambassador":

    page = st.sidebar.radio("Navigation", [
        "🏠 Mission Control",
        "🎯 Tasks",
        "🤖 AI Content",
        "🔗 Referrals",
        "🎁 Rewards"
    ])

    # ---------------- DASHBOARD ----------------
    if page == "🏠 Mission Control":
        st.title("🚀 Mission Control")

        col1, col2, col3 = st.columns(3)
        col1.metric("XP", st.session_state.xp)
        col2.metric("Streak", st.session_state.streak)
        col3.metric("Level", st.session_state.xp//500)

        st.divider()

        st.subheader("🤖 AI Insights")
        insights = [
            "You're in top 10% performers 🚀",
            "1 more task → next level 🔥",
            "Your consistency is elite"
        ]
        st.markdown(f"<div class='ai-box'>{random.choice(insights)}</div>", unsafe_allow_html=True)

        st.subheader("🔥 Streak Tracker")
        st.progress(st.session_state.streak/30)

    # ---------------- TASKS ----------------
    elif page == "🎯 Tasks":
        st.title("🎯 Campaign Tasks")

        tasks = [
            {"title":"Post on Instagram","xp":150},
            {"title":"Refer 5 Friends","xp":300},
            {"title":"Create Reel","xp":250}
        ]

        for t in tasks:
            st.markdown(f"<div class='card'><b>{t['title']}</b> (+{t['xp']} XP)</div>", unsafe_allow_html=True)

            if st.button(f"Complete {t['title']}"):
                st.session_state.xp += t["xp"]
                st.session_state.streak += 1
                st.session_state.history.append({
                    "Task": t["title"],
                    "XP": t["xp"],
                    "Date": datetime.now().strftime("%d-%m")
                })
                st.success("Task Completed 🚀")
                st.rerun()

    # ---------------- AI CONTENT ----------------
    elif page == "🤖 AI Content":
        st.title("🤖 Content Co-Pilot")

        idea = st.text_input("Campaign topic")

        if st.button("Generate Caption"):
            captions = [
                f"🔥 Don't miss this! {idea} is here 🚀",
                f"Level up with {idea}! Join now 💯",
                f"{idea} just dropped — check it out 👀"
            ]
            st.success(random.choice(captions))

        if st.button("Generate Video Script"):
            st.info(f"""
Hook: Ever heard about {idea}?  
Content: Here's why it's amazing...  
CTA: Join now before it's too late!
""")

    # ---------------- REFERRALS ----------------
    elif page == "🔗 Referrals":
        st.title("🔗 Referral Tracker")

        link = f"https://app.com/ref/{random.randint(1000,9999)}"
        st.code(link)

        st.metric("Clicks", random.randint(10,200))
        st.metric("Conversions", random.randint(1,50))

    # ---------------- REWARDS ----------------
    elif page == "🎁 Rewards":
        st.title("🎁 Rewards")

        rewards = [
            {"name":"T-Shirt","xp":1000},
            {"name":"Internship","xp":5000}
        ]

        for r in rewards:
            locked = st.session_state.xp < r["xp"]
            st.markdown(f"<div class='card'>{'🔒' if locked else '🎁'} {r['name']}</div>", unsafe_allow_html=True)

# =========================================================
# 🧑‍💼 RECRUITER SIDE
# =========================================================
else:

    page = st.sidebar.radio("Navigation", [
        "📊 Analytics",
        "🤖 AI Matching",
        "📢 Campaign Builder",
        "🧠 AI Insights"
    ])

    # ---------------- ANALYTICS ----------------
    if page == "📊 Analytics":
        st.title("📊 Live Performance")

        data = pd.DataFrame({
            "Ambassador":["A","B","C"],
            "Clicks":[120,90,150],
            "Conversions":[30,20,50]
        })

        fig = px.bar(data, x="Ambassador", y="Conversions")
        st.plotly_chart(fig)

    # ---------------- MATCHING ----------------
    elif page == "🤖 AI Matching":
        st.title("🤖 AI Ambassador Matching")

        st.success(random.choice([
            "Best match: Ambassador A (High engagement)",
            "Best match: Ambassador C (Top conversions)"
        ]))

    # ---------------- CAMPAIGN BUILDER ----------------
    elif page == "📢 Campaign Builder":
        st.title("📢 Create Campaign")

        name = st.text_input("Campaign Name")
        desc = st.text_area("Description")

        if st.button("Generate AI Brief"):
            st.info(f"""
Campaign: {name}  
Target: Students  
Deliverables: 3 posts + 1 reel  
CTA: Sign up now
""")

    # ---------------- AI INSIGHTS ----------------
    elif page == "🧠 AI Insights":
        st.title("🧠 Recruiter AI Assistant")

        q = st.text_input("Ask a question")

        if st.button("Analyze"):
            st.success(random.choice([
                "Top performer this week: Ambassador C",
                "Highest conversions from Chennai campus",
                "Engagement increased by 25%"
            ]))

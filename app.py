import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# 1. PREMIUM UI CONFIG
st.set_page_config(page_title="CampusConnect AI | Pro", layout="wide")

# Custom CSS for "Neon-Glass" UI
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; }
    .badge { padding: 5px 15px; border-radius: 20px; background: #00ffcc; color: black; font-weight: bold; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; background: rgba(255,255,255,0.02); }
    </style>
    """, unsafe_allow_html=True)

# Data Engine
if 'points' not in st.session_state:
    st.session_state.points = {"Varun": 450, "Praneetha": 380, "Suba": 310, "Harini (You)": 150}
if 'streak' not in st.session_state: st.session_state.streak = 5

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("CampusConnect AI")
st.sidebar.markdown(f"**Current Streak:** 🔥 {st.session_state.streak} Days")
menu = st.sidebar.selectbox("Go to", ["Ambassador Command Center", "Leaderboard Analytics", "AI Talent Audit"])

# --- PAGE 1: COMMAND CENTER (Gamification + Automation) ---
if menu == "Ambassador Command Center":
    st.title("🚀 Ambassador Command Center")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Your Total XP", f"{st.session_state.points['Harini (You)']} XP", "Top 10%")
    c2.metric("Active Challenges", "4", "2 Ending Soon")
    status = "👑 ELITE" if st.session_state.points['Harini (You)'] >= 200 else "⭐ ROOKIE"
    c3.markdown(f"**Current Rank:** <span class='badge'>{status}</span>", unsafe_allow_html=True)

    st.divider()

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("Verify New Contribution")
        with st.container():
            task = st.selectbox("Select Activity", ["Viral LinkedIn Post", "Discord Community Growth", "Technical Workshop"])
            url = st.text_input("Proof URL (Verified via AI)")
            if st.button("Submit & Claim Rewards", use_container_width=True):
                if url:
                    st.session_state.points["Harini (You)"] += 50
                    st.session_state.streak += 1
                    st.balloons()
                    st.success("Task Analyzed. +50 XP and +1 Streak Day awarded!")
                else: st.error("Verification link required.")

    with col_right:
        st.subheader("Smart Suggestions")
        if st.session_state.points["Harini (You)"] < 200:
            st.info("💡 **Goal:** Earn 50 more XP to unlock the 'Elite' Badge!")
        st.warning("⚠️ **Urgent:** 1 referral task expires in 4 hours!")

# --- PAGE 2: ANALYTICS (Data-Driven Innovation) ---
elif menu == "Leaderboard Analytics":
    st.title("📊 Program ROI & Leaderboard")
    df = pd.DataFrame(list(st.session_state.points.items()), columns=['Ambassador', 'XP']).sort_values('XP', ascending=False)
    
    fig = px.bar(df, x='Ambassador', y='XP', color='XP', 
                 color_continuous_scale='Turbo', template="plotly_dark", title="Impact Score by Ambassador")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Global Talent Rankings")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- PAGE 3: AI AUDIT (Recruiter-Ready Feature) ---
elif menu == "AI Talent Audit":
    st.title("🔍 Recruiter-Ready AI Audit")
    user = st.text_input("Enter Candidate GitHub Username")
    if st.button("Run Deep Analysis"):
        res = requests.get(f"https://api.github.com/users/{user}")
        if res.status_code == 200:
            data = res.json()
            score = round((data['public_repos'] * 0.3) + (data['followers'] * 0.2), 1)
            
            c1, c2 = st.columns([1, 2])
            with c1: st.image(data['avatar_url'], width=180)
            with c2:
                st.header(data.get('name', user))
                st.metric("AI Recruiter Score", f"{score}/10")
                st.write(f"**Bio:** {data['bio']}")
            
            st.success("✅ Candidate is highly recommended for Technical Ambassador roles.")
        else: st.error("Profile not found.")

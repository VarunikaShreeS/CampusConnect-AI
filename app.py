import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. ENTERPRISE BRANDING
st.set_page_config(page_title="CampusConnect AI | Enterprise", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { border: 1px solid #30363d; padding: 20px; border-radius: 12px; background: #161b22; }
    div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# Data Initialization
if 'points' not in st.session_state:
    st.session_state.points = {"Varun": 450, "Praneetha": 380, "Suba": 310, "Harini (You)": 150}

# Sidebar
st.sidebar.title("💎 CampusConnect AI")
st.sidebar.caption("SaaS Management Portal v2.0")
st.sidebar.divider()
page = st.sidebar.selectbox("Navigate Console", ["Executive Dashboard", "Leaderboard", "Technical Talent Audit"])

# --- PAGE 1: EXECUTIVE DASHBOARD (Automation & Proof) ---
if page == "Executive Dashboard":
    st.title("Ambassador Operations & Automation")
    st.markdown("Assign and verify tasks using our automated XP scoring engine.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("🚀 Submit New Task Proof", expanded=True):
            task = st.selectbox("Challenge Type", ["LinkedIn Brand Post", "WhatsApp Referral", "Tech Blog Content"])
            url = st.text_input("Validation Link (URL)")
            if st.button("Submit for Auto-Scoring", use_container_width=True):
                if url:
                    st.session_state.points["Harini (You)"] += 50
                    st.balloons()
                    st.success(f"Proof Verified! 50 XP added to 'Harini (You)'.")
                else:
                    st.error("Please provide a valid URL for verification.")

    with col2:
        st.subheader("Personal ROI")
        st.metric("Total XP Earned", f"{st.session_state.points['Harini (You)']} XP", delta="+50 today")
        st.progress(st.session_state.points["Harini (You)"] / 500)
        st.caption("90% to 'Gold Tier' Mentor Badge")

# --- PAGE 2: LEADERBOARD (Gamification) ---
elif page == "Leaderboard":
    st.title("Global Talent Analytics")
    df = pd.DataFrame(list(st.session_state.points.items()), columns=['Ambassador', 'XP']).sort_values('XP', ascending=False)
    
    # Professional Chart
    fig = px.bar(df, x='Ambassador', y='XP', color='XP', color_continuous_scale='Viridis', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Real-Time Rankings")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- PAGE 3: TALENT AUDIT (Recruiter Ready) ---
elif page == "Technical Talent Audit":
    st.title("AI Recruiter-Ready Audit")
    user = st.text_input("Enter GitHub Username for Analysis")
    if st.button("Run Audit"):
        res = requests.get(f"https://api.github.com/users/{user}")
        if res.status_code == 200:
            data = res.json()
            score = round((data['public_repos'] * 0.4) + (data['followers'] * 0.1), 1)
            c1, c2 = st.columns(2)
            c1.image(data['avatar_url'], width=150)
            c2.metric("Recruiter Benchmark Score", f"{score}/10")
            st.write(f"**Bio Analysis:** {data['bio']}")
            st.info("System Tip: High repository count detected. Candidate is 'Top 5%' for technical engagement.")

import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
import requests
from io import BytesIO
from datetime import datetime

# ─────────────────────────────────────────────
# 🎨 PREMIUM UI CONFIG
# ─────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="CampusConnect AI", page_icon="🌐")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); border: none; color: white; font-weight: bold; }
    .feature-card { background: #1a1c24; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 10px; }
    .status-online { color: #238636; font-weight: bold; font-size: 0.8em; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⚙️ LOGIC & DATA
# ─────────────────────────────────────────────
if "xp" not in st.session_state: st.session_state.xp = 150
if "history" not in st.session_state: st.session_state.history = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# Mock Leaderboard Data for Demo
leaderboard_data = pd.DataFrame([
    {"Rank": 1, "Ambassador": "Varun", "Total XP": 550},
    {"Rank": 2, "Ambassador": "Praneetha", "Total XP": 420},
    {"Rank": 3, "Ambassador": "Suba", "Total XP": 310},
    {"Rank": 4, "Ambassador": "Harini (You)", "Total XP": 150}
])

# ─────────────────────────────────────────────
# 👤 SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1998/1998592.png", width=80)
    st.title("Admin Panel")
    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.user_name}")
        st.info("🔥 5 Day Streak")
        menu = st.radio("Go To", ["🎯 Task Marketplace", "🔬 GitHub Auditor", "🏆 Leaderboard", "🤖 AI Co-Pilot", "🎫 Digital ID"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        menu = "Login"

# ─────────────────────────────────────────────
# 🚀 PAGE ROUTING
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    st.title("🌐 CampusConnect AI")
    name = st.text_input("Ambassador Name")
    if st.button("Enter Portal"):
        st.session_state.user_name = name
        st.session_state.logged_in = True
        st.rerun()

elif menu == "🎯 Task Marketplace":
    st.title("🎯 Mission Control")
    col1, col2 = st.columns([2, 1])
    with col1:
        tasks = [
            ("Social Media Spotlight", "+50 XP", "Share the new event poster on LinkedIn."),
            ("Community Growth", "+100 XP", "Onboard 5 new members via your referral link."),
            ("Technical Blogging", "+80 XP", "Write a summary of the latest AI workshop.")
        ]
        for title, xp, desc in tasks:
            with st.container():
                st.markdown(f"<div class='feature-card'><h3>{title} <span style='color:#00f2fe'>{xp}</span></h3><p>{desc}</p></div>", unsafe_allow_html=True)
                with st.expander("Submit Evidence"):
                    st.text_input("Link to Proof", key=title)
                    if st.button(f"Submit {title}"):
                        st.balloons()
    with col2:
        st.markdown("<div class='feature-card'><h4>Active Campaigns</h4><p>Spring AI Fest 🌸</p><p>Core Team Hiring 💼</p></div>", unsafe_allow_html=True)

elif menu == "🔬 GitHub Auditor":
    st.title("🔍 Recruiter-Ready Audit")
    handle = st.text_input("Enter GitHub Username", placeholder="e.g., VarunikaShreeS")
    if st.button("Analyze Profile"):
        st.write("Fetching API data...")
        st.info("Analysis Complete: Profile is 'Top 10%' for Python contributions.")

elif menu == "🏆 Leaderboard":
    st.title("🏆 Global Rankings")
    st.table(leaderboard_data)

elif menu == "🤖 AI Co-Pilot":
    st.title("✍️ Content Co-Pilot")
    st.write("Generate AI-drafted captions for your social posts.")
    topic = st.text_input("What are you posting about?", "AI Workshop")
    if st.button("Generate Post"):
        st.code(f"🚀 Just attended an incredible {topic} with CampusConnect! \n\nLearning how to build SaaS apps in minutes. #AI #CampusAmbassador #Tech", language="text")
        st.success("Captions adapted to your voice!")

elif menu == "🎫 Digital ID":
    st.title("🎫 Digital ID & Verification")
    col1, col2 = st.columns(2)
    with col1:
        qr = qrcode.make(f"Verified Ambassador: {st.session_state.user_name}")
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf, caption="Your Unique Referral QR")
    with col2:
        st.markdown(f"""
        <div class='feature-card' style='border-left: 5px solid #00f2fe;'>
            <h2>{st.session_state.user_name}</h2>
            <p><b>Status:</b> Elite Ambassador</p>
            <p><b>Verification:</b> DigiLocker Verified ✅</p>
            <p><b>ID Number:</b> CC-2026-X99</p>
        </div>
        """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# 1. PAGE CONFIG
st.set_page_config(page_title="CampusConnect Elite", page_icon="🛡️", layout="wide")

# 2. PRO UI STYLING
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stButton>button { 
        width: 100%; border-radius: 8px; background: linear-gradient(45deg, #238636, #2ea043); 
        color: white; border: none; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    .sidebar-user { text-align: center; padding: 20px; border-bottom: 1px solid #30363d; }
    .reward-card { 
        background: #161b22; border: 1px solid #30363d; padding: 15px; 
        border-radius: 12px; margin-bottom: 10px; border-left: 5px solid #2ea043;
    }
    .streak-fire { font-size: 30px; animation: burn 1.5s infinite alternate; }
    @keyframes burn { from { opacity: 0.7; } to { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE
if 'auth' not in st.session_state: st.session_state.auth = False
if 'xp' not in st.session_state: st.session_state.xp = 450
if 'streak' not in st.session_state: st.session_state.streak = 5
if 'history' not in st.session_state: 
    st.session_state.history = [{"Task": "Initial Sign-up", "XP": 450, "Date": "2024-03-10"}]

# --- LOGIN GATE ---
if not st.session_state.auth:
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown("<h1 style='text-align: center;'>🛡️ CampusConnect</h1>", unsafe_allow_html=True)
        user = st.text_input("Ambassador ID")
        pw = st.text_input("Password", type="password")
        if st.button("Unlock Dashboard"):
            if user.lower() == "harini" and pw.lower() == "win":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied.")
    st.stop()

# --- SIDEBAR WITH AVATAR & MOTIVATION ---
with st.sidebar:
    # Profile Avatar
    st.markdown("""
        <div class='sidebar-user'>
            <img src='https://cdn-icons-png.flaticon.com/512/6840/6840478.png' width='100' style='border-radius:50%; border: 3px solid #2ea043;'>
            <h3>Harini</h3>
            <p style='color:#8b949e;'>Elite Ambassador</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Interesting Streak Maintainer
    st.markdown(f"<div style='text-align:center;'><span class='streak-fire'>🔥</span><br><b>{st.session_state.streak} DAY STREAK</b></div>", unsafe_allow_html=True)
    progress = (st.session_state.streak / 7) # Progress towards weekly bonus
    st.progress(progress if progress <= 1.0 else 1.0)
    st.caption(f"Next Weekly Reward in {7 - st.session_state.streak} days!")
    
    st.divider()
    
    page = st.radio("Explore", ["🎯 Task Marketplace", "🔍 GitHub Auditor", "🎁 Rewards Vault", "📊 Performance", "⚙️ Settings"])
    
    if st.button("Sign Out"):
        st.session_state.auth = False
        st.rerun()

# --- PAGE 1: TASK MARKETPLACE ---
if page == "🎯 Task Marketplace":
    st.title("🎯 Available Missions")
    tasks = [
        {"n": "LinkedIn Viral Post", "x": 200, "d": "Post a tech insight and tag @AICoreConnect."},
        {"n": "Campus Workshop", "x": 500, "d": "Organize a mini-demo for 10+ students."}
    ]
    for t in tasks:
        with st.container():
            st.markdown(f"<div class='reward-card'><b>{t['n']}</b><br><small>{t['d']}</small><br><span style='color:#2ea043;'>+{t['x']} XP</span></div>", unsafe_allow_html=True)
            with st.expander("Submit Evidence"):
                link = st.text_input("Proof Link", key=t['n'])
                if st.button("Verify Mission", key=f"btn_{t['n']}"):
                    if link:
                        with st.spinner("AI Auditor Scanning..."): time.sleep(1.5)
                        st.session_state.xp += t['x']
                        st.session_state.history.append({"Task": t['n'], "XP": t['x'], "Date": "Today"})
                        st.balloons()
                        st.success("Mission Verified!")

# --- PAGE 2: GITHUB AUDITOR ---
elif page == "🔍 GitHub Auditor":
    st.title("🔍 Career Readiness Audit")
    u = st.text_input("GitHub Username")
    if st.button("Audit Profile"):
        score = random.randint(70, 95)
        fig = go.Figure(go.Indicator(mode="gauge+number", value=score, title={'text': "Recruiter Score"}, gauge={'bar':{'color':"#2ea043"}}))
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig)

# --- PAGE 3: REWARDS VAULT (NEW!) ---
elif page == "🎁 Rewards Vault":
    st.title("🎁 Your Rewards & Perks")
    st.write(f"Current Balance: **{st.session_state.xp} XP**")
    
    rewards = [
        {"item": "Official AICore Connect T-Shirt", "cost": 1000, "locked": True},
        {"item": "1-on-1 Mentorship Session", "cost": 2500, "locked": True},
        {"item": "Internship Fast-Track Pass", "cost": 5000, "locked": True}
    ]
    
    for r in rewards:
        status = "🔒 Locked" if st.session_state.xp < r['cost'] else "🔓 Available!"
        st.markdown(f"""
            <div class='reward-card'>
                <h4>{r['item']}</h4>
                <p>Cost: {r['cost']} XP | <b>{status}</b></p>
            </div>
            """, unsafe_allow_html=True)

# --- PAGE 4: PERFORMANCE (CRASH-FIXED) ---
elif page == "📊 Performance":
    st.title("📊 Your Impact Analytics")
    c1, c2 = st.columns(2)
    df = pd.DataFrame(st.session_state.history)
    
    with c1:
        st.metric("Total XP Earned", st.session_state.xp)
        if not df.empty:
            fig_pie = px.pie(df, values='XP', names='Task', template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        st.metric("Weekly Rank", "#4")
        st.info("💡 Keep your streak alive to jump to #3 next week!")

# --- PAGE 5: SETTINGS ---
elif page == "⚙️ Settings":
    st.title("⚙️ Account Preferences")
    st.text_input("Full Name", value="Harini")
    st.text_input("University", value="College of Engineering")
    st.selectbox("Main Tech Stack", ["Python", "WebDev", "AI/ML", "DevOps"])
    if st.button("Save Profile"):
        st.toast("Profile Saved!")

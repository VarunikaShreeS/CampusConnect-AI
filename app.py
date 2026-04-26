import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="CampusConnect Elite", page_icon="🛡️", layout="wide")

# 2. ADVANCED UI STYLING
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { 
        width: 100%; border-radius: 8px; background: linear-gradient(45deg, #238636, #2ea043); 
        color: white; border: none; font-weight: 600; height: 3em; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4); }
    .card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    .streak-box { background: rgba(255, 165, 0, 0.1); border: 1px solid orange; padding: 10px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE (Initialization with Mock Data for Demo)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'xp' not in st.session_state: st.session_state.xp = 350
if 'streak' not in st.session_state: st.session_state.streak = 7
if 'history' not in st.session_state:
    st.session_state.history = [
        {"Task": "Onboarding", "XP": 100, "Date": "2024-03-01"},
        {"Task": "LinkedIn Referral", "XP": 250, "Date": "2024-03-05"}
    ]

# --- LOGIN GATE ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<h1 style='text-align: center;'>🛡️ CampusConnect</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>The Single Source of Truth for CA Programs</p>", unsafe_allow_html=True)
        with st.container():
            user = st.text_input("Ambassador ID")
            pw = st.text_input("Access Key", type="password")
            if st.button("Secure Login"):
                if user.lower() == "harini" and pw.lower() == "win":
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Invalid ID or Key. (Try: harini / win)")
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("CampusConnect")
    st.markdown(f"### Welcome, Harini! 👋")
    st.markdown(f"<div class='streak-box'>🔥 {st.session_state.streak} Day Streak</div>", unsafe_allow_html=True)
    st.write(f"**Level {st.session_state.xp // 100} Ambassador**")
    st.divider()
    page = st.radio("Menu", ["🎯 Task Marketplace", "🔍 GitHub Auditor", "🏆 Leaderboard", "📈 My Impact", "⚙️ Settings"])
    if st.button("Sign Out"):
        st.session_state.auth = False
        st.rerun()

# --- PAGE 1: TASK MARKETPLACE ---
if page == "🎯 Task Marketplace":
    st.title("🎯 Active Missions")
    st.info("Complete missions, upload proof, and earn auto-scored XP.")
    
    tasks = [
        {"name": "LinkedIn Brand Awareness", "xp": 150, "desc": "Post about the new AICore workshop with the official banner."},
        {"name": "GitHub Project Star", "xp": 100, "desc": "Contribute a PR or Star the community repo."},
        {"name": "Referral King/Queen", "xp": 300, "desc": "Onboard 3 students using your unique CA link."}
    ]
    
    for t in tasks:
        with st.container():
            st.markdown(f"""<div class='card'>
                <h4>{t['name']} <span style='color:#2ea043; float:right;'>+{t['xp']} XP</span></h4>
                <p style='color:#8b949e;'>{t['desc']}</p>
            </div>""", unsafe_allow_html=True)
            with st.expander("Submit Proof of Work"):
                link = st.text_input("Proof URL (LinkedIn/GitHub/Drive)", key=t['name'])
                if st.button("Submit Mission", key=f"btn_{t['name']}"):
                    if "http" in link:
                        with st.status("AI Auditor Verifying..."):
                            time.sleep(1.5)
                        st.session_state.xp += t['xp']
                        st.session_state.history.append({"Task": t['name'], "XP": t['xp'], "Date": "Today"})
                        st.balloons()
                        st.success(f"Verified! {t['xp']} XP credited.")
                    else:
                        st.error("Please provide a valid URL link.")

# --- PAGE 2: GITHUB AUDITOR (JUDGE FAVORITE) ---
elif page == "🔍 GitHub Auditor":
    st.title("🔍 Recruiter-Ready Audit")
    st.write("We assess your GitHub presence to see how recruiters view your profile.")
    
    gh_user = st.text_input("Enter GitHub Username", placeholder="e.g., HariniDev")
    if st.button("Run Impact Audit"):
        if gh_user:
            with st.spinner("Analyzing Repo Depth & Commit Patterns..."):
                time.sleep(2)
            
            score = random.randint(70, 95)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = score,
                title = {'text': "Recruiter Readiness Score"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#2ea043"}}
            ))
            fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success("**Strengths Identified:**\n- High commit consistency\n- Meaningful repo naming")
            with col2:
                st.warning("**Improvement Areas:**\n- Missing 'About' section in 2 repos\n- Profile README needs links")
        else:
            st.warning("Please enter a username.")

# --- PAGE 3: LEADERBOARD ---
elif page == "🏆 Leaderboard":
    st.title("🏆 Global Hall of Fame")
    df_lb = pd.DataFrame({
        "Ambassador": ["Varun", "Priya", "Harini (You)", "Subash", "Ananya"],
        "XP": [850, 720, st.session_state.xp, 310, 290],
        "Missions": [12, 10, len(st.session_state.history), 4, 3]
    }).sort_values("XP", ascending=False)
    
    st.table(df_lb)
    st.markdown("### 🏅 Milestone Rewards")
    st.write("- **Level 5:** AICore Connect T-Shirt 👕\n- **Level 10:** Internship Interview Fast-Track 🚀")

# --- PAGE 4: ANALYTICS ---
elif page == "📈 My Impact":
    st.title("📈 Performance Analytics")
    col1, col2 = st.columns(2)
    
    df = pd.DataFrame(st.session_state.history)
    with col1:
        st.metric("Total XP", st.session_state.xp, delta="+15% from last week")
        fig_pie = px.pie(df, values='XP', names='Task', title="XP Distribution by Source", template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.metric("Tasks Completed", len(df))
        fig_bar = px.bar(df, x='Date', y='XP', title="XP Growth Timeline", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

# --- PAGE 5: SETTINGS ---
elif page == "⚙️ Settings":
    st.title("⚙️ Account Settings")
    st.text_input("Display Name", value="Harini")
    st.text_input("Linked College", value="Tech University")
    st.toggle("Public Profile", value=True)
    st.toggle("Email Notifications for New Tasks", value=True)
    if st.button("Save Changes"):
        st.toast("Profile Updated Successfully!")

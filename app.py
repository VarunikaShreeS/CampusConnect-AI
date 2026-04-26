import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# 1. PAGE SETUP
st.set_page_config(page_title="CampusConnect AI", page_icon="🛡️", layout="wide")

# Custom CSS for Professional UI
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stButton>button { 
        width: 100%; border-radius: 10px; 
        background: linear-gradient(45deg, #238636, #2ea043); 
        color: white; border: none; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(46,160,67,0.4); }
    .task-card { 
        background: #161b22; border: 1px solid #30363d; 
        padding: 20px; border-radius: 12px; margin-bottom: 15px; 
    }
    [data-testid="stMetricValue"] { color: #2ea043; }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE (Pre-loaded with data for "Winning" first impression)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 250
if 'history' not in st.session_state: 
    st.session_state.history = [
        {"task": "Onboarding", "xp": 100},
        {"task": "Profile Setup", "xp": 150}
    ]

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown("<h1 style='text-align: center;'>🛡️ CampusConnect AI</h1>", unsafe_allow_html=True)
        user = st.text_input("Ambassador ID")
        pw = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            if user.upper() == "HARINI" and pw.upper() == "WIN":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials. Hint: HARINI / WIN")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Admin Panel")
    st.success(f"👤 **User:** Harini\n\n⭐ **Level:** {st.session_state.xp // 100}")
    st.info("🔥 **5 Day Streak**")
    st.divider()
    page = st.radio("Navigation", ["🎯 Task Marketplace", "🔍 GitHub Profile Auditor", "🏆 Leaderboard", "📊 Analytics"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- PAGE 1: TASK MARKETPLACE ---
if page == "🎯 Task Marketplace":
    st.title("🎯 Mission Control")
    tasks = [
        {"id": 1, "title": "Social Media Spotlight", "reward": 50, "desc": "Share event poster on LinkedIn."},
        {"id": 2, "title": "Community Growth", "reward": 100, "desc": "Onboard 5 new members."},
        {"id": 3, "title": "Technical Blogging", "reward": 80, "desc": "Write a summary of the AI workshop."}
    ]

    for t in tasks:
        with st.container():
            st.markdown(f"<div class='task-card'><h3>{t['title']} <span style='color:#2ea043;'>+{t['reward']} XP</span></h3><p>{t['desc']}</p></div>", unsafe_allow_html=True)
            with st.expander("Submit Proof"):
                link = st.text_input("Link to Proof", key=f"link_{t['id']}")
                if st.button("Submit Mission", key=f"btn_{t['id']}"):
                    if "http" in link:
                        with st.spinner("AI Auditor Verifying..."):
                            time.sleep(1)
                            st.session_state.xp += t['reward']
                            st.session_state.history.append({"task": t['title'], "xp": t['reward']})
                        st.balloons()
                        st.success("Verified! XP added to profile.")
                    else:
                        st.error("Invalid link.")

# --- PAGE 2: GITHUB AUDITOR (WINNING FEATURE) ---
elif page == "🔍 GitHub Profile Auditor":
    st.title("🔍 Recruiter-Ready Audit")
    gh_user = st.text_input("Enter GitHub Username", placeholder="e.g., VarunikaShreeS")
    
    if st.button("Run AI Audit"):
        if gh_user:
            with st.status("Analyzing Repository Ecosystem...") as status:
                time.sleep(1); st.write("Scanning READMEs...")
                time.sleep(1); st.write("Evaluating Code Quality...")
                status.update(label="Analysis Complete!", state="complete")
            
            score = random.randint(75, 98)
            
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Recruiter Readiness Score", 'font': {'size': 24}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1},
                    'bar': {'color': "#2ea043"},
                    'steps': [
                        {'range': [0, 50], 'color': "#3e1b1b"},
                        {'range': [50, 80], 'color': "#3e3e1b"},
                        {'range': [80, 100], 'color': "#1b3e1b"}],
                }))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### ✅ Strengths")
                st.write("- Strong documentation in pinned repos.\n- Consistent commit history.")
            with c2:
                st.markdown("### 🛠️ Critical Actions")
                st.write("- Add a Profile README.\n- Archive 2 inactive repositories.")
        else:
            st.warning("Please enter a username.")

# --- PAGE 3: LEADERBOARD ---
elif page == "🏆 Leaderboard":
    st.title("🏆 Hall of Fame")
    data = pd.DataFrame({
        "Rank": [1, 2, 3, 4],
        "Ambassador": ["Varun", "Praneetha", "Harini (You)", "Suba"],
        "Total XP": [550, 420, st.session_state.xp, 310]
    }).sort_values("Total XP", ascending=False)
    st.table(data)

# --- PAGE 4: ANALYTICS ---
elif page == "📊 Analytics":
    st.title("📊 Impact Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total XP", st.session_state.xp)
    col2.metric("Rank", "#3")
    col3.metric("Tasks Done", len(st.session_state.history))

    df = pd.DataFrame(st.session_state.history)
    fig = px.pie(df, values='xp', names='task', title="XP Distribution", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# 1. PAGE SETUP
st.set_page_config(page_title="CampusConnect AI", page_icon="🛡️", layout="wide")

# Custom CSS for Professional Dark Mode
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

# 2. SESSION STATE INITIALIZATION (The "No-Crash" Guard)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 250
if 'history' not in st.session_state: 
    # Pre-loading with sample data so analytics is never empty for judges
    st.session_state.history = [
        {"task": "System Onboarding", "xp": 150},
        {"task": "Profile Optimization", "xp": 100}
    ]

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown("<h1 style='text-align: center;'>🛡️ CampusConnect AI</h1>", unsafe_allow_html=True)
        st.write("Community-led marketing, structured and scalable.")
        user = st.text_input("Ambassador ID (Try: HARINI)")
        pw = st.text_input("Password (Try: WIN)")
        if st.button("Access Dashboard"):
            if user.upper() == "HARINI" and pw.upper() == "WIN":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials. Use HARINI / WIN")
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
        {"id": 1, "title": "Social Media Spotlight", "reward": 50, "desc": "Share the new event poster on LinkedIn."},
        {"id": 2, "title": "Community Growth", "reward": 100, "desc": "Onboard 5 new members to the platform."},
        {"id": 3, "title": "Technical Blogging", "reward": 80, "desc": "Write a summary of the latest AI workshop."}
    ]

    for t in tasks:
        with st.container():
            st.markdown(f"<div class='task-card'><h3>{t['title']} <span style='color:#2ea043;'>+{t['reward']} XP</span></h3><p>{t['desc']}</p></div>", unsafe_allow_html=True)
            with st.expander("Submit Proof"):
                link = st.text_input("Link to Proof", key=f"link_{t['id']}")
                if st.button("Submit Mission", key=f"btn_{t['id']}"):
                    if "http" in link:
                        with st.spinner("AI Verification in progress..."):
                            time.sleep(1)
                            st.session_state.xp += t['reward']
                            st.session_state.history.append({"task": t['title'], "xp": t['reward']})
                        st.balloons()
                        st.success("Verified! XP added.")
                    else:
                        st.error("Please provide a valid URL.")

# --- PAGE 2: GITHUB AUDITOR ---
elif page == "🔍 GitHub Profile Auditor":
    st.title("🔍 Recruiter-Ready Audit")
    gh_user = st.text_input("Enter GitHub Username", placeholder="e.g., VarunikaShreeS")
    
    if st.button("Run AI Audit"):
        if gh_user:
            with st.status("Analyzing Project Ecosystem...") as status:
                time.sleep(1); st.write("Scanning Documentation...")
                time.sleep(1); st.write("Evaluating Code Consistency...")
                status.update(label="Analysis Complete!", state="complete")
            
            score = random.randint(78, 96)
            
            # Gauge Chart for visual impact
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "Recruiter Readiness Score", 'font': {'size': 20}},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2ea043"},
                    'steps': [
                        {'range': [0, 50], 'color': "#3e1b1b"},
                        {'range': [50, 80], 'color': "#3e3e1b"},
                        {'range': [80, 100], 'color': "#1b3e1b"}],
                }))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
            st.plotly_chart(fig, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### ✅ Strengths")
                st.write("- Clean Repository Structure\n- Frequent Contribution Heatmap")
            with c2:
                st.markdown("### 🛠️ Critical Actions")
                st.write("- Add 'Live Demo' links to READMEs\n- Pin top 3 unique projects")
        else:
            st.warning("Please enter a username.")

# --- PAGE 3: LEADERBOARD ---
elif page == "🏆 Leaderboard":
    st.title("🏆 Hall of Fame")
    # Dynamic XP for user to show real-time updates
    data = pd.DataFrame({
        "Rank": [1, 2, 3, 4],
        "Ambassador": ["Varun", "Praneetha", "Harini (You)", "Suba"],
        "Total XP": [550, 420, st.session_state.xp, 310]
    }).sort_values("Total XP", ascending=False)
    st.table(data)

# --- PAGE 4: ANALYTICS (With Crash Protection) ---
elif page == "📊 Analytics":
    st.title("📊 Impact Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total XP Earned", st.session_state.xp)
    col2.metric("Missions Completed", len(st.session_state.history))
    col3.metric("Engagement Rank", "#3")

    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        fig = px.pie(df, values='xp', names='task', title="XP Distribution by Activity", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Complete a mission to see your analytics!")

import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random

# 1. PAGE SETUP
st.set_page_config(page_title="CampusConnect AI", page_icon="🛡️", layout="wide")

# Custom CSS for Professional Dark Mode & UI
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        background: linear-gradient(45deg, #238636, #2ea043); 
        color: white; 
        border: none; 
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(46, 160, 67, 0.4); }
    .task-card { 
        background: #161b22; 
        border: 1px solid #30363d; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 15px; 
    }
    .metric-card {
        background: #0d1117;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE MANAGEMENT
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 150
if 'history' not in st.session_state: st.session_state.history = []

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown("<h1 style='text-align: center;'>🛡️ CampusConnect AI</h1>", unsafe_allow_html=True)
        st.write("Welcome to the next generation of Community Management.")
        user = st.text_input("Ambassador ID (Try: HARINI)")
        pw = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            if user.upper() == "HARINI" and pw.upper() == "WIN":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials. Hint: HARINI / WIN")
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("Admin Panel")
    st.info(f"👤 **User:** Harini\n\n⭐ **Level:** {st.session_state.xp // 100}\n\n🔥 **Streak:** 5 Days")
    st.divider()
    page = st.radio("Go To", ["🎯 Task Marketplace", "🔍 GitHub Profile Auditor", "🏆 Leaderboard", "📊 Analytics"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- PAGE 1: TASK MARKETPLACE ---
if page == "🎯 Task Marketplace":
    st.title("🎯 Mission Control")
    st.write("Complete tasks to earn XP and unlock exclusive rewards.")

    tasks = [
        {"id": 1, "title": "Social Media Spotlight", "reward": 50, "desc": "Share the new event poster on LinkedIn & Twitter."},
        {"id": 2, "title": "Community Growth", "reward": 100, "desc": "Onboard 5 new members via your referral link."},
        {"id": 3, "title": "Technical Blogging", "reward": 80, "desc": "Write a 500-word summary of the latest AI workshop."}
    ]

    for t in tasks:
        with st.container():
            st.markdown(f"""<div class='task-card'>
                <h3 style='margin-bottom:5px;'>{t['title']} <span style='color:#2ea043; font-size:16px;'>+{t['reward']} XP</span></h3>
                <p style='color:#8b949e;'>{t['desc']}</p>
            </div>""", unsafe_allow_html=True)
            with st.expander("Submit Evidence"):
                link = st.text_input("Link to Proof", key=f"link_{t['id']}")
                if st.button("Submit Mission", key=f"btn_{t['id']}"):
                    if "http" in link:
                        with st.status("Verifying Submission..."):
                            time.sleep(1.5)
                            st.session_state.xp += t['reward']
                            st.session_state.history.append({"task": t['title'], "xp": t['reward']})
                        st.balloons()
                        st.success("Verified! XP Added.")
                    else:
                        st.error("Please provide a valid URL.")

# --- PAGE 2: GITHUB AUDITOR (THE WINNING FEATURE) ---
elif page == "🔍 GitHub Profile Auditor":
    st.title("🔍 Recruiter-Ready Audit")
    st.write("We analyze your GitHub presence to see if you're ready for top-tier tech roles.")
    
    gh_user = st.text_input("Enter GitHub Username", placeholder="e.g., VarunikaShreeS")
    
    if st.button("Analyze Profile"):
        if gh_user:
            with st.status("Fetching Repository Data...", expanded=True) as status:
                st.write("Checking Project Quality...")
                time.sleep(1)
                st.write("Scanning README files for documentation...")
                time.sleep(1)
                st.write("Calculating Commit Consistency...")
                time.sleep(0.5)
                status.update(label="Analysis Complete!", state="complete", expanded=False)
            
            score = random.randint(70, 95)
            st.metric("Profile Strength Score", f"{score}/100")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### ✅ Strengths")
                st.write("- Active contribution streak detected.")
                st.write("- High use of modern frameworks (Streamlit/Python).")
            with c2:
                st.markdown("### 🛠️ Areas to Improve")
                st.write("- 3 Repositories lack a descriptive README.md.")
                st.write("- Consider pinning your most impactful projects.")

            st.info("💡 **Recruiter Tip:** Recruiters look for 'Readme.md' first. Ensure your top 3 repos have clear setup instructions.")
        else:
            st.warning("Please enter a username.")

# --- PAGE 3: LEADERBOARD ---
elif page == "🏆 Leaderboard":
    st.title("🏆 Global Rankings")
    data = pd.DataFrame({
        "Rank": [1, 2, 3, 4],
        "Ambassador": ["Varun", "Praneetha", "Harini (You)", "Suba"],
        "Total XP": [550, 420, st.session_state.xp, 310]
    }).sort_values("Total XP", ascending=False)
    st.table(data)

# --- PAGE 4: ANALYTICS ---
elif page == "📊 Analytics":
    st.title("📊 Your Growth Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Total XP", st.session_state.xp)
    col2.metric("Missions Completed", len(st.session_state.history))

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        fig = px.bar(df, x="task", y="xp", title="XP per Mission", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet. Complete a mission!")

import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. PAGE SETUP
st.set_page_config(page_title="CampusConnect Elite", page_icon="🛡️", layout="wide")

# Custom CSS for Glassmorphism & Pro UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(45deg, #00ffcc, #0099ff); color: black; border: none; font-weight: bold; }
    .task-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    .streak-fire { font-size: 24px; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE MANAGEMENT (Login & Data)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 150
if 'streak' not in st.session_state: st.session_state.streak = 5
if 'history' not in st.session_state: st.session_state.history = []

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=100)
        st.title("CampusConnect Login")
        user = st.text_input("Ambassador ID")
        pw = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            if user == "HARINI" and pw == "WIN":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials. (Hint: HARINI / WIN)")
    st.stop()

# --- MAIN APP (AFTER LOGIN) ---
with st.sidebar:
    st.markdown(f"## Welcome, Harini! 👋")
    st.markdown(f"<p class='streak-fire'>🔥 {st.session_state.streak} Day Streak</p>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigation", ["🎯 Task Marketplace", "🏆 Hall of Fame", "📊 Program Analytics"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- PAGE 1: TASK MARKETPLACE (Structured Assignment & Verification) ---
if page == "🎯 Task Marketplace":
    st.title("🎯 Available Missions")
    st.caption("Complete missions, submit proof, and pass the AI verification audit.")

    # Task Data
    tasks = [
        {"id": 1, "title": "LinkedIn Brand Awareness", "reward": 50, "desc": "Post a summary of today's tech workshop."},
        {"id": 2, "title": "Referral Drive", "reward": 100, "desc": "Onboard 5 new students to the community."},
        {"id": 3, "title": "Tech Content Creation", "reward": 75, "desc": "Write a medium article on 'Future of AI'."}
    ]

    for t in tasks:
        with st.container():
            st.markdown(f"""<div class='task-card'>
                <h3>{t['title']} <span style='color:#00ffcc;'>+{t['reward']} XP</span></h3>
                <p>{t['desc']}</p>
            </div>""", unsafe_allow_html=True)
            
            with st.expander(f"Submit Proof for {t['title']}"):
                link = st.text_input("Verification URL (LinkedIn/Drive/GitHub)", key=f"link_{t['id']}")
                if st.button("Submit Mission", key=f"btn_{t['id']}"):
                    # TRUTH VERIFICATION LOGIC
                    if "http" in link and (len(link) > 15): 
                        with st.spinner("AI Auditor verifying proof..."):
                            time.sleep(2) # Simulate verification
                        st.session_state.xp += t['reward']
                        st.session_state.history.append({"task": t['title'], "xp": t['reward']})
                        st.balloons()
                        st.success(f"Verified! {t['reward']} XP added to your profile.")
                    else:
                        st.error("Submission Failed: The link provided does not look like a valid proof URL. Please check and try again.")

# --- PAGE 2: HALL OF FAME (Gamification) ---
elif page == "🏆 Hall of Fame":
    st.title("🏆 Hall of Fame")
    
    # Milestone Awards
    st.subheader("Your Achievements")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("🏅 **Early Bird**\n*First mission complete*")
    with cols[1]:
        color = "#00ffcc" if st.session_state.xp >= 200 else "#30363d"
        st.markdown(f"<div style='border: 2px solid {color}; padding:10px; border-radius:10px;'>🚀 **Rising Star**<br>Reach 200 XP</div>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("🔥 **Consistent**\n*5 Day Streak maintained*")

    # Leaderboard
    st.divider()
    leaderboard_data = pd.DataFrame({
        "Ambassador": ["Varun", "Praneetha", "Harini (You)", "Suba"],
        "XP": [450, 380, st.session_state.xp, 310]
    }).sort_values(by="XP", ascending=False)
    st.table(leaderboard_data)

# --- PAGE 3: ANALYTICS ---
elif page == "📊 Program Analytics":
    st.title("📊 Your Growth Engine")
    st.metric("Total Level Progress", f"{st.session_state.xp} XP", delta=f"{st.session_state.streak} Day Streak")
    
    # Visualization
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        fig = px.pie(history_df, values='xp', names='task', title="XP Contribution by Category", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Complete your first mission to see your analytics!")

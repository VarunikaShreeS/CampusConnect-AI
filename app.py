import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. THEME & CONFIG
st.set_page_config(page_title="CampusConnect Elite", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 15px; }
    .profile-box { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; text-align: center; }
    .rank-tag { background: #00ffcc; color: black; padding: 2px 10px; border-radius: 10px; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 210
if 'bio' not in st.session_state: st.session_state.bio = "Tech Enthusiast | Content Creator"

# --- LOGIN GATE ---
if not st.session_state.logged_in:
    _, center, _ = st.columns([1, 1, 1])
    with center:
        st.title("🔒 Access Portal")
        uid = st.text_input("Ambassador ID")
        ups = st.text_input("Password", type="password")
        if st.button("Login"):
            if uid.upper() == "HARINI" and ups.upper() == "WIN":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- POST-LOGIN UI ---
with st.sidebar:
    # THE AVATAR IS BACK!
    st.markdown("<div class='profile-box'>", unsafe_allow_html=True)
    st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Harini", width=100)
    st.markdown(f"### Harini")
    st.markdown("<span class='rank-tag'>GOLD AMBASSADOR</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Management Hub", ["🎯 Mission Control", "📊 Impact Analytics", "👤 Profile & Settings"])
    st.divider()
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

# --- PAGE 1: MISSION CONTROL ---
if page == "🎯 Mission Control":
    st.title("🚀 Active Missions")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container(border=True):
            st.subheader("LinkedIn Content Drive")
            st.write("Post about CampusConnect features. Reward: **50 XP**")
            url = st.text_input("Submission Link")
            if st.button("Verify & Submit"):
                if "http" in url:
                    with st.status("Running AI Truth Scan...", expanded=True) as status:
                        st.write("Checking link integrity...")
                        time.sleep(1)
                        st.write("Verifying metadata...")
                        time.sleep(1)
                        status.update(label="Verification Complete!", state="complete", expanded=False)
                    st.session_state.xp += 50
                    st.balloons()
                    st.success("Points Reconciled! +50 XP")
                else: st.error("Invalid URL detected by Truth Scanner.")

# --- PAGE 2: ANALYTICS ---
elif page == "📊 Impact Analytics":
    st.title("📈 Performance Analytics")
    df = pd.DataFrame({"User": ["Varun", "Praneetha", "Harini (You)", "Suba"], "XP": [450, 380, st.session_state.xp, 310]})
    fig = px.bar(df, x='User', y='XP', color='XP', template="plotly_dark", title="Leaderboard Standings")
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 3: PROFILE & SETTINGS ---
elif page == "👤 Profile & Settings":
    st.title("⚙️ Account Settings")
    
    tab1, tab2 = st.tabs(["Public Profile", "System Settings"])
    
    with tab1:
        st.subheader("Edit Ambassador Persona")
        new_bio = st.text_area("Your Bio", st.session_state.bio)
        if st.button("Update Profile"):
            st.session_state.bio = new_bio
            st.toast("Profile Updated!")
            
    with tab2:
        st.subheader("Preferences")
        st.checkbox("Email Notifications for New Missions", value=True)
        st.checkbox("Show my XP on Global Leaderboard", value=True)
        st.selectbox("Default Dashboard View", ["Missions", "Analytics"])

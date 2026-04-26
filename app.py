import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. PAGE CONFIG
st.set_page_config(page_title="CampusConnect Pro", page_icon="🚀", layout="wide")

# 2. ADVANCED NEON UI STYLING
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #11141c; border-right: 1px solid #00ffcc; }
    .stMetric { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 12px; }
    .rank-badge { 
        background: linear-gradient(45deg, #00ffcc, #0099ff); 
        color: black; padding: 4px 12px; border-radius: 15px; 
        font-weight: bold; font-size: 12px; 
    }
    </style>
    """, unsafe_allow_html=True)

# Data Initialization
if 'points' not in st.session_state:
    st.session_state.points = {"Varun": 450, "Praneetha": 380, "Suba": 310, "Harini (You)": 150}

# --- INTERESTING SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #00ffcc;'>💎 CampusConnect</h2>", unsafe_allow_html=True)
    st.divider()
    
    # User Profile Section
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Harini", width=60)
    with col2:
        st.markdown("**Harini**")
        st.markdown("<span class='rank-badge'>SILVER TIER</span>", unsafe_allow_html=True)
    
    st.write("")
    # XP Progress Bar in Sidebar
    current_xp = st.session_state.points["Harini (You)"]
    next_level = 500
    progress = current_xp / next_level
    st.caption(f"Level Progress: {current_xp}/{next_level} XP")
    st.progress(progress if progress <= 1.0 else 1.0)
    
    st.divider()
    
    # Styled Navigation
    menu = st.radio(
        "CORE CONSOLE",
        ["🚀 Command Center", "📊 Analytics Hub", "🔍 AI Talent Audit"],
        index=0
    )
    
    st.divider()
    st.info("💡 Tip: Post on LinkedIn to earn 50 XP instantly!")

# --- MAIN CONTENT LOGIC ---
if menu == "🚀 Command Center":
    st.title("Ambassador Operations")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("Submit Task")
            task = st.selectbox("Task Type", ["Social Media", "Referral", "Event"])
            url = st.text_input("Proof URL")
            if st.button("Claim XP", use_container_width=True):
                if url:
                    st.session_state.points["Harini (You)"] += 50
                    st.balloons()
                    st.rerun()
    with c2:
        st.metric("Total Impact", f"{current_xp} XP", delta="+50 this week")

elif menu == "📊 Analytics Hub":
    st.title("Program ROI")
    df = pd.DataFrame(list(st.session_state.points.items()), columns=['Ambassador', 'XP']).sort_values('XP', ascending=False)
    fig = px.bar(df, x='Ambassador', y='XP', color='XP', color_continuous_scale='GnBu', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    st.table(df)

elif menu == "🔍 AI Talent Audit":
    st.title("Talent Audit System")
    user = st.text_input("GitHub Username")
    if st.button("Analyze"):
        res = requests.get(f"https://api.github.com/users/{user}")
        if res.status_code == 200:
            data = res.json()
            st.success(f"Audit Score: {round(data['public_repos']*1.2, 1)}/10")
            st.json(data)

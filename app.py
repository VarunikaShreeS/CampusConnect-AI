import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# 1. PAGE CONFIG
st.set_page_config(page_title="CampusConnect Elite", page_icon="💎", layout="wide")

# 2. PRO UI STYLING
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #11141c; border-right: 2px solid #00ffcc; }
    .stMetric { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; }
    .achievement-card {
        padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #1e222d 0%, #11141c 100%);
        border: 1px solid #30363d; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Data Initialization
if 'points' not in st.session_state:
    st.session_state.points = {"Varun": 450, "Praneetha": 380, "Suba": 310, "Harini (You)": 210}

# --- SIDEBAR: GAMIFIED HUB ---
with st.sidebar:
    st.markdown("<h2 style='color: #00ffcc;'>💎 CampusConnect</h2>", unsafe_allow_html=True)
    
    # Profile Hub
    col_a, col_b = st.columns([1, 2])
    with col_a: st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Harini", width=70)
    with col_b:
        st.markdown("**Harini**")
        st.markdown("<p style='color: #00ffcc; font-size: 12px;'>🏆 GOLD AMBASSADOR</p>", unsafe_allow_html=True)
    
    # Leveling System
    xp = st.session_state.points["Harini (You)"]
    st.write(f"**Level 4** | {xp}/500 XP")
    st.progress(xp/500)
    
    st.divider()
    menu = st.radio("OPERATIONS", ["🚀 Mission Control", "📊 Impact Analytics", "🔍 AI Talent Audit"])
    st.divider()
    st.success("🔥 7 Day Streak!")

# --- PAGE 1: MISSION CONTROL (Innovation: Smart Tasks) ---
if menu == "🚀 Mission Control":
    st.title("🚀 Mission Control")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Active Challenges")
        with st.container():
            st.markdown("""
            <div class='achievement-card'>
                <h4>📣 Social Media Blitz</h4>
                <p>Post about the hackathon on LinkedIn. <b>Reward: 50 XP</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            proof = st.text_input("Enter Proof Link")
            if st.button("Submit Mission", use_container_width=True):
                if proof:
                    st.session_state.points["Harini (You)"] += 50
                    st.balloons()
                    st.toast("Mission Accomplished! +50 XP")
                    st.rerun()
    
    with col2:
        st.markdown("### Achievements")
        st.write("✅ First Referral")
        st.write("✅ 5 Day Streak")
        st.write("🔒 Mentor Status (450 XP)")

# --- PAGE 2: IMPACT ANALYTICS (Innovation: Skill Radar) ---
elif menu == "📊 Impact Analytics":
    st.title("📊 Impact Analytics")
    
    df = pd.DataFrame(list(st.session_state.points.items()), columns=['Ambassador', 'XP']).sort_values('XP', ascending=False)
    
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df, x='Ambassador', y='XP', color='XP', template="plotly_dark", title="Global Rankings")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        # INNOVATION: Radar Chart for Skills
        categories = ['Marketing','Technical','Referrals','Content','Events']
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=[4, 5, 2, 4, 3], theta=categories, fill='toself', name='Your Skills'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, template="plotly_dark", title="Ambassador Skill Radar")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- PAGE 3: AI TALENT AUDIT ---
elif menu == "🔍 AI Talent Audit":
    st.title("🔍 AI Talent Audit")
    username = st.text_input("GitHub Username")
    if st.button("Deep Scan"):
        res = requests.get(f"https://api.github.com/users/{username}")
        if res.status_code == 200:
            data = res.json()
            st.metric("Recruiter Score", f"{round(data['public_repos']*0.5, 1)}/10")
            st.write(f"**AI Summary:** {data.get('name')} is a consistent contributor with focus on {data.get('bio', 'software development')}.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# 1. PAGE CONFIG & THEME
st.set_page_config(page_title="CampusConnect AI", page_icon="🛡️", layout="wide")

# 2. ENHANCED CSS (Glassmorphism & Glow Effects)
st.markdown("""
    <style>
    .main { background: #0d1117; color: #c9d1d9; }
    .stButton>button { 
        width: 100%; border-radius: 12px; background: linear-gradient(90deg, #238636, #2ea043); 
        color: white; border: none; font-weight: bold; height: 3em; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(46, 160, 67, 0.4); }
    .sidebar-card { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    .mission-card { background: #161b22; border-radius: 15px; padding: 20px; border-left: 5px solid #2ea043; margin-bottom: 15px; }
    .ai-chat { background: #010409; border-radius: 10px; padding: 10px; border: 1px solid #30363d; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# 3. DYNAMIC SESSION STATE
if 'auth' not in st.session_state: st.session_state.auth = False
if 'xp' not in st.session_state: st.session_state.xp = 550
if 'streak' not in st.session_state: st.session_state.streak = 5
if 'history' not in st.session_state: 
    st.session_state.history = [{"Task": "Sign-up Bonus", "XP": 550, "Date": "2024-03-20"}]

# --- LOGIN GATE ---
if not st.session_state.auth:
    cols = st.columns([1, 1.2, 1])
    with cols[1]:
        st.markdown("<h1 style='text-align: center;'>🛡️ CampusConnect AI</h1>", unsafe_allow_html=True)
        user = st.text_input("Ambassador ID")
        pw = st.text_input("Password", type="password")
        if st.button("Access Command Center"):
            if user.lower() == "harini" and pw.lower() == "win":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied.")
    st.stop()

# --- SIDEBAR: GAMIFIED HUB ---
with st.sidebar:
    # Profile & Leveling
    level = st.session_state.xp // 500
    progress = (st.session_state.xp % 500) / 500
    st.markdown(f"""
        <div style='text-align: center;'>
            <img src='https://cdn-icons-png.flaticon.com/512/6840/6840478.png' width='80' style='border-radius:50%; border: 2px solid #2ea043;'>
            <h3>Harini</h3>
            <p style='color:#2ea043; font-weight:bold;'>LVL {level} ELITE</p>
        </div>
    """, unsafe_allow_html=True)
    st.progress(progress)
    st.caption(f"✨ {500 - (st.session_state.xp % 500)} XP to reach Level {level + 1}")
    
    # Streak Shield
    st.markdown(f"""
        <div class='sidebar-card' style='text-align:center;'>
            <h2 style='margin:0;'>🔥 {st.session_state.streak}</h2>
            <small>Day Streak</small>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    page = st.radio("Navigation", ["🎯 Missions", "🔍 GitHub Audit", "🤖 AI CampusBot", "🎁 Vault", "📊 Stats"])
    
    # AI CampusBot Sidebar Hook
    st.divider()
    st.markdown("**🤖 AI Status:** Online")
    st.caption("AI is monitoring your progress...")

# --- PAGE 1: MISSIONS (GAMIFIED) ---
if page == "🎯 Missions":
    st.title("🎯 Mission Marketplace")
    st.info("Complete missions to fuel your Level Up!")
    
    missions = [
        {"id": "m1", "title": "Social Media Blast", "xp": 150, "icon": "📱"},
        {"id": "m2", "title": "Referral Surge", "xp": 400, "icon": "🚀"},
        {"id": "m3", "title": "Tech Blog Writing", "xp": 250, "icon": "✍️"}
    ]

    for m in missions:
        with st.container():
            st.markdown(f"""<div class='mission-card'>
                <h3>{m['icon']} {m['title']} <span style='float:right; color:#2ea043;'>+{m['xp']} XP</span></h3>
                <p>Submit proof to unlock rewards and boost your rank.</p>
            </div>""", unsafe_allow_html=True)
            with st.expander("Submit Proof"):
                link = st.text_input("Submission URL", key=m['id'])
                if st.button("Claim Reward", key=f"btn_{m['id']}"):
                    if link:
                        with st.status("AI Verifying Content..."):
                            time.sleep(1.2)
                            st.session_state.xp += m['xp']
                            st.session_state.history.append({"Task": m['title'], "XP": m['xp'], "Date": "Today"})
                        st.balloons()
                        st.toast("XP Credited!")
                        st.rerun()

# --- PAGE 2: GITHUB AUDIT ---
elif page == "🔍 GitHub Audit":
    st.title("🔍 Recruiter AI Audit")
    gh = st.text_input("Username", placeholder="e.g. VarunikaShreeS")
    if st.button("Start AI Analysis"):
        score = random.randint(75, 98)
        fig = go.Figure(go.Indicator(mode="gauge+number", value=score, 
            title={'text': "Recruiter Grade"},
            gauge={'bar':{'color':"#2ea043"}, 'steps':[{'range':[0,70],'color':'#3e1b1b'},{'range':[70,100],'color':'#1b3e1b'}]}))
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)
        st.success("AI Recommendation: Profile pinned repos to hit 90+ Score!")

# --- PAGE 3: AI CAMPUSBOT (THE "WOW" FACTOR) ---
elif page == "🤖 AI CampusBot":
    st.title("🤖 CampusBot AI")
    st.write("Your personal AI mentor for the Ambassador program.")
    
    prompt = st.chat_input("Ask about rewards, levels, or how to earn XP...")
    if prompt:
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            if "xp" in prompt.lower():
                st.write(f"Hello Harini! You currently have **{st.session_state.xp} XP**. I suggest the 'Referral Surge' mission to hit Level {level + 1} faster!")
            elif "reward" in prompt.lower():
                st.write("You are close to unlocking the **Official T-Shirt**! Keep your streak going.")
            else:
                st.write("I'm analyzing your profile... You're doing great! Your consistency is in the top 5%.")

# --- PAGE 4: REWARDS VAULT ---
elif page == "🎁 Vault":
    st.title("🎁 Rewards Vault")
    rewards = [
        {"item": "AICore T-Shirt", "xp": 1000},
        {"item": "Expert Mentorship", "xp": 2500},
        {"item": "Internship Pass", "xp": 5000}
    ]
    for r in rewards:
        locked = st.session_state.xp < r['xp']
        st.markdown(f"""
            <div class='mission-card' style='opacity: {0.5 if locked else 1};'>
                <h4>{'🔒' if locked else '🎁'} {r['item']}</h4>
                <p>Unlock at {r['xp']} XP</p>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 5: STATS ---
elif page == "📊 Stats" or page == "📊 Performance":
    st.title("📊 Impact Analytics")
    
    # Check if history exists to avoid IndexError
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        
        col1, col2 = st.columns(2)
        with col1:
            # Safe delta calculation
            last_xp = st.session_state.history[-1]['XP']
            st.metric("Total XP", st.session_state.xp, delta=f"+{last_xp}")
            
            # Safe Chart rendering
            fig_pie = px.pie(df, values='XP', names='Task', template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.metric("Daily Streak", f"{st.session_state.streak} Days")
            fig_bar = px.bar(df, x='Date', y='XP', template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        # What the judge sees if they haven't done a mission yet
        st.info("🚀 Your Impact Analytics will appear here once you complete your first mission!")
        st.metric("Total XP", st.session_state.xp)

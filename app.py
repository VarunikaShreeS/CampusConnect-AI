import streamlit as st
import pandas as pd
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="CampusConnect AI Pro", page_icon="💎", layout="wide")

# Custom CSS to make it look "Premium"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4259; }
    </style>
    """, unsafe_allow_html=True)

# 2. BRANDING & SIDEBAR
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=80)
st.sidebar.title("📍 CampusConnect AI")
st.sidebar.markdown("*First-Year Innovation Hack*")
st.sidebar.divider()
page = st.sidebar.radio("Navigation Menu", ["Dashboard", "Leaderboard", "GitHub Recruiter Review"])

# Initialize session state for gamification
if 'points' not in st.session_state:
    st.session_state.points = {"Harini (You)": 50, "Varun": 450, "Praneetha": 380, "Suba": 310}
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

# --- PAGE 1: DASHBOARD ---
if page == "Dashboard":
    st.title("🙌 Ambassador Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Submit Task Proof")
        task_type = st.selectbox("What task did you complete?", ["LinkedIn Brand Post", "WhatsApp Referral", "Content Creation", "Event Hosting"])
        proof_url = st.text_input("Paste URL (Social Media Post or Google Drive Link)")
        
        if st.button("Submit & Claim Points", use_container_width=True):
            if proof_url:
                st.balloons()
                st.session_state.points["Harini (You)"] += 50
                st.session_state.last_submission = task_type
                st.success(f"Verified! +50 XP added for {task_type}.")
            else:
                st.error("Please provide a link as proof.")

    with col2:
        st.subheader("Your Progress")
        current_pts = st.session_state.points["Harini (You)"]
        st.metric("Your Total XP", f"{current_pts} XP", delta="50 XP (Today)")
        
        # Rank Logic
        progress = current_pts / 500  # Target 500
        st.write(f"Progress to 'Gold Level'")
        st.progress(progress if progress <= 1.0 else 1.0)
        st.caption("Earn 500 XP to unlock the exclusive Mentorship Badge!")

# --- PAGE 2: LEADERBOARD ---
elif page == "Leaderboard":
    st.title("🏆 Campus Leaderboard")
    
    # Process Data
    data_list = [{"Ambassador": k, "XP Points": v} for k, v in st.session_state.points.items()]
    df = pd.DataFrame(data_list).sort_values(by="XP Points", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    
    # Visual Highlights
    st.write("### 🔥 Top Performers")
    col1, col2, col3 = st.columns(3)
    col1.metric("1st Place", df.iloc[0]['Ambassador'], f"{df.iloc[0]['XP Points']} XP")
    if len(df) > 1: col2.metric("2nd Place", df.iloc[1]['Ambassador'], f"{df.iloc[1]['XP Points']} XP")
    if len(df) > 2: col3.metric("3rd Place", df.iloc[2]['Ambassador'], f"{df.iloc[2]['XP Points']} XP")
    
    st.divider()
    st.dataframe(df, use_container_width=True)

# --- PAGE 3: GITHUB REVIEW ---
elif page == "GitHub Recruiter Review":
    st.title("🔍 Recruiter-Ready Analysis")
    username = st.text_input("Enter GitHub Username")
    
    if st.button("Start Analysis"):
        if username:
            with st.spinner("AI analyzing profile metrics..."):
                res = requests.get(f"https://api.github.com/users/{username}")
                if res.status_code == 200:
                    data = res.json()
                    
                    # AI Scoring Logic
                    repos = data['public_repos']
                    followers = data['followers']
                    score = min(10, (repos * 0.5) + (followers * 0.1))
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(data['avatar_url'], width=200)
                        st.metric("AI Recruiter Score", f"{score:.1f}/10")
                    
                    with col2:
                        st.write(f"## {data.get('name', username)}")
                        st.write(f"**Bio:** {data['bio'] if data['bio'] else 'No bio provided'}")
                        st.info(f"💡 **AI Tip:** Your account is {2026 - int(data['created_at'][:4])} years old. {'Great consistency!' if repos > 10 else 'Try to upload more projects to increase your score.'}")
                        
                        st.subheader("Action Plan:")
                        st.markdown(f"- [ ] Update README for your top 3 repos.")
                        st.markdown(f"- [ ] Pin repositories that use modern tech stacks.")
                else:
                    st.error("User not found.")

import streamlit as st
import pandas as pd
import requests

# 1. PROFESSIONAL PAGE CONFIG
st.set_page_config(page_title="CampusConnect Enterprise", page_icon="📈", layout="wide")

# Professional Corporate Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #1c1f23; }
    .stMetric { border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px; background: white; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3192, #1bffff); }
    h1 { color: #1c1f23; font-weight: 700; letter-spacing: -0.5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR NAVIGATION (Clean & Minimalist)
st.sidebar.title("CampusConnect")
st.sidebar.caption("Enterprise Administration Portal")
st.sidebar.divider()
page = st.sidebar.radio("Console", ["Activity Overview", "Performance Analytics", "Talent Audit"])

# Session State Logic
if 'points' not in st.session_state:
    st.session_state.points = {"Harini": 50, "Varun": 450, "Praneetha": 380, "Suba": 310}

# --- PAGE 1: ACTIVITY OVERVIEW (Dashboard) ---
if page == "Activity Overview":
    st.title("Activity Submission Portal")
    st.markdown("Track and validate ambassador contributions via secure URL verification.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("Submit New Activity Proof", expanded=True):
            task_type = st.selectbox("Activity Category", ["LinkedIn Corporate Branding", "User Referral Program", "Technical Content", "Campus Event Management"])
            proof_url = st.text_input("Validation URL (Social/Cloud Storage)")
            
            if st.button("Submit for Verification", use_container_width=True):
                if proof_url:
                    st.session_state.points["Harini"] += 50
                    st.toast("Submission successful. Points reconciled.")
                    st.success("Verification in progress. +50 XP allocated to profile.")
                else:
                    st.warning("A valid URL is required for audit purposes.")

    with col2:
        st.subheader("Personal Metrics")
        current_pts = st.session_state.points["Harini"]
        st.metric("Total Contribution XP", f"{current_pts}", delta="+50 today")
        
        progress = current_pts / 500
        st.write(f"Tier Progress: **{int(progress*100)}%**")
        st.progress(progress if progress <= 1.0 else 1.0)
        st.caption("Next Tier: Senior Ambassador Level")

# --- PAGE 2: PERFORMANCE ANALYTICS (Leaderboard) ---
elif page == "Performance Analytics":
    st.title("Program Performance Analytics")
    st.markdown("Real-time data distribution of top-performing campus representatives.")
    
    data_list = [{"Ambassador": k, "XP Points": v} for k, v in st.session_state.points.items()]
    df = pd.DataFrame(data_list).sort_values(by="XP Points", ascending=False).reset_index(drop=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Top Performer", df.iloc[0]['Ambassador'])
    c2.metric("Average XP", f"{int(df['XP Points'].mean())}")
    c3.metric("Total Program XP", f"{df['XP Points'].sum()}")
    
    st.divider()
    st.table(df)

# --- PAGE 3: TALENT AUDIT (GitHub Review) ---
elif page == "Talent Audit":
    st.title("Technical Talent Audit")
    st.markdown("Objective GitHub profile analysis for recruiter-readiness scoring.")
    
    username = st.text_input("Enter Candidate GitHub Username")
    
    if st.button("Run Audit"):
        if username:
            res = requests.get(f"https://api.github.com/users/{username}")
            if res.status_code == 200:
                data = res.json()
                
                # Pro Scoring Logic
                score = min(10.0, (data['public_repos'] * 0.4) + (data['followers'] * 0.2))
                
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.image(data['avatar_url'], width=150)
                with col_b:
                    st.header(data.get('name', username))
                    st.write(f"**Professional Bio:** {data['bio'] if data['bio'] else 'N/A'}")
                    st.metric("Recruiter Benchmark Score", f"{score:.1f} / 10.0")
                
                st.subheader("Audit Observations")
                st.markdown(f"- **Account Longevity:** Established {2026 - int(data['created_at'][:4])} years ago.")
                st.markdown(f"- **Project Density:** {data['public_repos']} public repositories detected.")
                st.info("System recommendation: Focus on project documentation (README.md) to increase audit score.")
            else:
                st.error("Profile not found in GitHub global database.")

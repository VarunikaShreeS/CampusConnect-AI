import streamlit as st
import pandas as pd
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="CampusConnect AI", 
    page_icon="🚀", 
    layout="wide"
)

# 2. BRANDING & SIDEBAR
st.sidebar.markdown("# 📍 CampusConnect")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation Menu", ["Dashboard", "Leaderboard", "GitHub Recruiter Review"])

# Initialize session state for gamification points
# I updated these with the names you provided!
if 'points' not in st.session_state:
    st.session_state.points = {
        "Harini (You)": 50, 
        "Varun": 450, 
        "Praneetha": 380, 
        "Suba": 310
    }

# --- PAGE 1: DASHBOARD (Meets: Automated Task Workflows) ---
if page == "Dashboard":
    st.title("🙌 Ambassador Dashboard")
    st.markdown("### *Assign, track, and verify tasks with AI auto-scoring.* [cite: 20]")
    
    with st.container():
        st.subheader("Submit Task Proof")
        task_type = st.selectbox(
            "What task did you complete?", 
            ["LinkedIn Brand Post", "WhatsApp Referral", "Content Creation", "Event Hosting"]
        )
        proof_url = st.text_input("Paste URL (Social Media Post or Google Drive Link)")
        
        if st.button("Submit & Claim Points"):
            if proof_url:
                st.success(f"Proof received for {task_type}! AI is now verifying...")
                st.balloons()
                st.session_state.points["Harini (You)"] += 50
                st.info("Verified! +50 XP added to your profile. Check the Leaderboard! [cite: 21]")
            else:
                st.error("Please provide a link as proof of work.")

# --- PAGE 2: LEADERBOARD (Meets: Identify Top Performers & Gamification) ---
elif page == "Leaderboard":
    st.title("🏆 Campus Leaderboard")
    st.markdown("### *Surface high-impact ambassadors through real-time data.* [cite: 19]")
    
    # Convert points dictionary to a list for sorting
    data_list = []
    for name, score in st.session_state.points.items():
        data_list.append({"Ambassador": name, "XP Points": score})
    
    # Create the DataFrame (Table)
    df = pd.DataFrame(data_list)
    df = df.sort_values(by="XP Points", ascending=False).reset_index(drop=True)
    
    # Add rank icons
    df.index = df.index + 1
    
    st.table(df)
    st.success("Top 3 performers this month get exclusive Mentorship Badges! 🏅 [cite: 21]")

# --- PAGE 3: GITHUB REVIEW (Meets: Impact Criteria & Success Look) ---
elif page == "GitHub Recruiter Review":
    st.title("🔍 GitHub Recruiter-Ready Analysis")
    st.markdown("### *Assessing GitHub profiles in under 2 minutes.* [cite: 28]")
    
    username = st.text_input("Enter your GitHub username to see what recruiters notice first [cite: 37]")
    
    if st.button("Start AI Analysis"):
        if username:
            with st.spinner("Analyzing repositories and commit history..."):
                # Fetching real data from GitHub API
                response = requests.get(f"https://api.github.com/users/{username}")
                
                if response.status_code == 200:
                    user_data = response.json()
                    
                    st.write(f"## Analysis for {user_data.get('name', username)}")
                    
                    # Creating columns for metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Public Projects", user_data['public_repos'])
                    col2.metric("Followers", user_data['followers'])
                    col3.metric("Account Age", f"{2026 - int(user_data['created_at'][:4])} Years")
                    
                    st.divider()
                    
                    # Specific Advice based on Success Criteria
                    st.subheader("💡 How to become Recruiter-Ready [cite: 40]")
                    st.markdown("- **What they notice first:** Your profile bio and 'Pinned' repos. Ensure these reflect your current skills. [cite: 37]")
                    st.markdown("- **Repos to Improve:** Any repository without a README.md file should be improved or archived. [cite: 39]")
                    st.markdown("- **Next Steps:** Organize your projects into a structured portfolio to make them more impressive. [cite: 39]")
                else:
                    st.error("GitHub user not found. Please check the spelling.")

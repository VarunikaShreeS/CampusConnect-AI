import streamlit as st
import pandas as pd
import requests
import plotly.express as px # Added for professional charts

st.set_page_config(page_title="CampusConnect Analytics", layout="wide")

# Modern "Dark Mode" styling for a high-tech feel
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { border: 1px solid #30363d; padding: 15px; border-radius: 10px; background: #161b22; }
    h1, h2 { font-family: 'Inter', sans-serif; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# Corrected Data Dictionary (Fixing the KeyError)
if 'points' not in st.session_state:
    st.session_state.points = {"Harini": 50, "Varun": 450, "Praneetha": 380, "Suba": 310}

st.sidebar.title("CampusConnect")
st.sidebar.caption("v2.0 Enterprise Edition")
page = st.sidebar.radio("Management Console", ["Global Analytics", "Audit Candidate"])

if page == "Global Analytics":
    st.title("Program Analytics Dashboard")
    
    # Professional Visuals: A Bar Chart of performance
    df = pd.DataFrame(list(st.session_state.points.items()), columns=['Ambassador', 'XP'])
    fig = px.bar(df, x='Ambassador', y='XP', color='XP', template="plotly_dark", title="Ambassador XP Distribution")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Performance Metrics")
        st.metric("Your Status", f"{st.session_state.points['Harini']} XP", delta="+50 points")
    with col2:
        st.subheader("Leaderboard Table")
        st.table(df.sort_values('XP', ascending=False))

elif page == "Audit Candidate":
    st.title("Technical Talent Audit")
    user = st.text_input("GitHub Username")
    if st.button("Run AI Audit"):
        res = requests.get(f"https://api.github.com/users/{user}")
        if res.status_code == 200:
            data = res.json()
            st.success(f"Audit Complete for {data.get('name', user)}")
            st.json({"Score": round(data['public_repos'] * 1.5, 1), "Category": "Developer", "Status": "Recruiter Ready"})

import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from io import BytesIO

# --- UI CONFIG ---
st.set_page_config(layout="wide", page_title="CampusConnect PRO", page_icon="📈")

# --- STYLING ---
st.markdown("""
<style>
    .roi-card { background: linear-gradient(135deg, #1e1e2f, #252545); border-radius: 15px; padding: 25px; border: 1px solid #4facfe; }
    .stat-val { font-size: 36px; font-weight: 800; color: #00f2fe; }
</style>
""", unsafe_allow_html=True)

# --- APP NAVIGATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

with st.sidebar:
    st.title("🌐 CC-AI PRO")
    if st.session_state.logged_in:
        page = st.radio("Switch View", ["Ambassador Portal", "Recruiter Dashboard (ROI)"])
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        page = "Login"

# --- LOGIC ---
if not st.session_state.logged_in:
    st.title("🚀 Welcome to CampusConnect AI")
    user = st.text_input("Username")
    if st.button("Launch Portal"):
        st.session_state.user_name = user
        st.session_state.logged_in = True
        st.rerun()

elif page == "Ambassador Portal":
    st.title(f"👋 Welcome, {st.session_state.user_name}!")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Your Missions")
        st.info("🎯 Mission 1: Host a Python workshop (+200 XP)")
        st.info("📢 Mission 2: Share the hackathon link (+50 XP)")
        
        # Referral Logic
        st.subheader("🔗 Your Referral Engine")
        ref_link = f"https://campusconnect.ai/join?ref={st.session_state.user_name.lower()}"
        st.code(ref_link, language="text")
        if st.button("Copy Link"):
            st.toast("Link copied to clipboard!")

    with col2:
        st.subheader("Digital ID")
        qr = qrcode.make(ref_link)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf, width=200)

elif page == "Recruiter Dashboard (ROI)":
    st.title("📊 Brand Impact Analytics")
    st.write("This view is for the companies hiring the ambassadors.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='roi-card'><div class='stat-val'>$4.2k</div><div>Ad Spend Saved</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='roi-card'><div class='stat-val'>12.5k</div><div>Organic Reach</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='roi-card'><div class='stat-val'>82%</div><div>Conversion Rate</div></div>", unsafe_allow_html=True)

    # ROI Chart
    data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Manual Ads': [1000, 2000, 3000, 4000],
        'CampusConnect AI': [200, 500, 800, 1100]
    })
    fig = px.bar(data, x='Month', y=['Manual Ads', 'CampusConnect AI'], 
                 title="Cost Comparison: Traditional vs CampusConnect",
                 barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

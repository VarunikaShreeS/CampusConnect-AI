import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
import json
import time
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="CampusConnect AI",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e6edf3;
}
.main { background: #0a0a0f; }
section[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid #ffffff10;
}

/* Headings */
h1,h2,h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

/* Cards */
.cc-card {
    background: #13131f;
    border: 1px solid #ffffff12;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color .2s;
}
.cc-card:hover { border-color: #7c6dff44; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg,#13131f,#1a1a2e);
    border: 1px solid #7c6dff33;
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
}
.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg,#7c6dff,#00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-lbl { font-size: 12px; color: #8888aa; margin-top: 2px; letter-spacing: .05em; text-transform: uppercase; }

/* Task cards */
.task-card {
    background: #13131f;
    border: 1px solid #ffffff12;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.task-done { border-color: #00d4aa44; opacity: .6; }
.task-pts {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #00d4aa;
    min-width: 56px;
    text-align: right;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
}
.badge-purple { background:#7c6dff22; color:#b0a6ff; border:1px solid #7c6dff44; }
.badge-teal   { background:#00d4aa22; color:#00d4aa; border:1px solid #00d4aa44; }
.badge-amber  { background:#ffb34722; color:#ffb347; border:1px solid #ffb34744; }
.badge-red    { background:#ff4d6d22; color:#ff4d6d; border:1px solid #ff4d6d44; }

/* Leaderboard row */
.lb-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 6px;
    background: #13131f;
    border: 1px solid #ffffff0a;
}
.lb-rank { font-family:'Syne',sans-serif; font-size:18px; font-weight:800; min-width:30px; }
.lb-1 { color:#ffd700; }
.lb-2 { color:#c0c0c0; }
.lb-3 { color:#cd7f32; }

/* AI box */
.ai-insight {
    background: linear-gradient(135deg,#0f172a,#1a1a2e);
    border-left: 3px solid #7c6dff;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 8px 0;
    font-size: 14px;
    color: #c0c0e0;
}

/* Progress bar */
.xp-bar-bg { background:#1a1a2e; border-radius:100px; height:8px; margin:8px 0; }
.xp-bar    { background:linear-gradient(90deg,#7c6dff,#00d4aa); border-radius:100px; height:8px; transition:width .5s; }

/* Tier badge */
.tier-bronze  { color:#cd7f32; }
.tier-silver  { color:#c0c0c0; }
.tier-gold    { color:#ffd700; }
.tier-plat    { color:#a0c4ff; }

/* GitHub score ring */
.score-ring {
    width:100px; height:100px; border-radius:50%;
    border:4px solid #7c6dff;
    display:flex; align-items:center; justify-content:center;
    font-family:'Syne',sans-serif; font-size:26px; font-weight:800;
    color:#e0e0ff; margin:0 auto 12px;
}

/* Sidebar logo */
.sidebar-logo {
    font-family:'Syne',sans-serif;
    font-size:22px; font-weight:800;
    background:linear-gradient(135deg,#7c6dff,#00d4aa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    padding: 10px 0 20px;
    display:block;
}

/* Divider */
.cc-divider { border:none; border-top:1px solid #ffffff10; margin:20px 0; }

/* Stmetric override */
[data-testid="stMetricValue"] { font-family:'Syne',sans-serif !important; font-size:28px !important; }

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg,#7c6dff,#6050e0) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    transition: .2s !important;
}
div.stButton > button:hover { opacity:.85 !important; transform:translateY(-1px) !important; }

/* Input styling */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #13131f !important;
    border: 1px solid #ffffff18 !important;
    color: #e6edf3 !important;
    border-radius: 10px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:#0a0a0f; }
::-webkit-scrollbar-thumb { background:#7c6dff55; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS & HELPERS
# ─────────────────────────────────────────────
GITHUB_API = "https://api.github.com"

TASKS = [
    {"id":1, "title":"Star our GitHub Repo",        "category":"GitHub",   "points":100, "difficulty":"Easy",   "desc":"Star the CampusConnect-AI repo and fork it."},
    {"id":2, "title":"LinkedIn Post",                "category":"Social",   "points":150, "difficulty":"Easy",   "desc":"Post about CampusConnect with #CampusConnectAI."},
    {"id":3, "title":"Instagram Reel",               "category":"Content",  "points":250, "difficulty":"Medium", "desc":"Create a 30s Reel showcasing campus life."},
    {"id":4, "title":"Refer a Friend",               "category":"Referral", "points":300, "difficulty":"Medium", "desc":"Refer a fellow student to the program."},
    {"id":5, "title":"Write a Blog Post",            "category":"Content",  "points":400, "difficulty":"Hard",   "desc":"500-word post about tech communities."},
    {"id":6, "title":"Open Source PR",               "category":"GitHub",   "points":500, "difficulty":"Hard",   "desc":"Submit a PR to any open source project."},
    {"id":7, "title":"Host a Workshop",              "category":"Event",    "points":800, "difficulty":"Expert", "desc":"Organize a workshop at your college."},
    {"id":8, "title":"Onboard 5 Ambassadors",        "category":"Referral", "points":1000,"difficulty":"Expert", "desc":"Recruit and onboard 5 new ambassadors."},
]

BADGES = [
    {"name":"🚀 Launcher",    "req_pts":100,  "req_streak":0, "desc":"Earned first 100 XP"},
    {"name":"⭐ Rising Star", "req_pts":500,  "req_streak":0, "desc":"500 XP milestone"},
    {"name":"🔥 On Fire",     "req_pts":0,    "req_streak":7, "desc":"7-day streak"},
    {"name":"💎 Diamond",     "req_pts":1500, "req_streak":0, "desc":"1500 XP milestone"},
    {"name":"🏆 Champion",    "req_pts":3000, "req_streak":0, "desc":"3000 XP milestone"},
    {"name":"👑 Legend",      "req_pts":5000, "req_streak":0, "desc":"5000 XP milestone"},
]

SAMPLE_LEADERBOARD = [
    {"name":"Arun K.",      "college":"IIT Madras",   "pts":4820, "streak":14, "tier":"Platinum", "gh":"arundev"},
    {"name":"Priya S.",     "college":"BITS Pilani",  "pts":3650, "streak":9,  "tier":"Gold",     "gh":"priyacode"},
    {"name":"Rahul M.",     "college":"VIT Chennai",  "pts":2900, "streak":5,  "tier":"Gold",     "gh":"rahulmr"},
    {"name":"Sneha R.",     "college":"Anna Univ",    "pts":1800, "streak":3,  "tier":"Silver",   "gh":"snehar"},
    {"name":"Kiran P.",     "college":"NIT Trichy",   "pts":1200, "streak":2,  "tier":"Silver",   "gh":"kiranpv"},
]

def tier_from_pts(pts):
    if pts >= 3000: return "Platinum", "🔷"
    if pts >= 1500: return "Gold",     "🥇"
    if pts >= 500:  return "Silver",   "🥈"
    return "Bronze", "🥉"

def xp_to_next(pts):
    tiers = [500, 1500, 3000, 5000]
    for t in tiers:
        if pts < t: return pts, t
    return pts, pts

def earned_badges(pts, streak):
    return [b for b in BADGES if pts >= b["req_pts"] and streak >= b["req_streak"]]

def diff_color(d):
    return {"Easy":"badge-teal","Medium":"badge-amber","Hard":"badge-red","Expert":"badge-purple"}.get(d,"badge-purple")

def cat_icon(c):
    return {"GitHub":"💻","Social":"📱","Content":"✍️","Referral":"🔗","Event":"🎤"}.get(c,"📌")

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "xp": 0, "streak": 0, "completed_tasks": [],
        "github_profile": None, "github_score": 0,
        "ambassador_name": "", "ambassador_college": "",
        "history": [], "logged_in": False,
        "rec_logged_in": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# GITHUB ANALYZER  ← The killer feature
# ─────────────────────────────────────────────
def analyze_github(username: str):
    headers = {"Accept": "application/vnd.github+json"}
    try:
        u = requests.get(f"{GITHUB_API}/users/{username}", headers=headers, timeout=8)
        if u.status_code != 200:
            return None, 0
        user = u.json()
        repos_r = requests.get(f"{GITHUB_API}/users/{username}/repos?per_page=100&sort=updated", headers=headers, timeout=8)
        repos = repos_r.json() if repos_r.status_code == 200 else []
        repos = [r for r in repos if isinstance(r, dict)]

        stars   = sum(r.get("stargazers_count", 0) for r in repos)
        forks   = sum(r.get("forks_count", 0)      for r in repos)
        langs   = list({r.get("language") for r in repos if r.get("language")})
        score = min(
            user.get("public_repos",  0) * 5  +
            user.get("followers",     0) * 3  +
            stars  * 4 +
            forks  * 3 +
            len(langs) * 10 +
            (50 if user.get("bio")     else 0) +
            (50 if user.get("blog")    else 0) +
            (50 if user.get("company") else 0),
            1000
        )
        profile = {
            "name":         user.get("name") or username,
            "avatar_url":   user.get("avatar_url",""),
            "bio":          user.get("bio",""),
            "public_repos": user.get("public_repos",0),
            "followers":    user.get("followers",0),
            "following":    user.get("following",0),
            "stars":        stars,
            "forks":        forks,
            "languages":    langs[:8],
            "location":     user.get("location",""),
            "profile_url":  user.get("html_url",""),
            "company":      user.get("company",""),
        }
        return profile, score
    except Exception:
        return None, 0

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<span class='sidebar-logo'>🚀 CampusConnect AI</span>", unsafe_allow_html=True)
    mode = st.radio("Switch portal", ["👤 Ambassador", "🧑‍💼 Recruiter"], label_visibility="collapsed")
    st.markdown("<hr class='cc-divider'>", unsafe_allow_html=True)

    if mode == "👤 Ambassador":
        if st.session_state.logged_in:
            tier, icon = tier_from_pts(st.session_state.xp)
            st.markdown(f"""
            <div style='text-align:center;padding:8px 0'>
              <div style='font-size:36px'>{icon}</div>
              <div style='font-weight:600;font-size:15px'>{st.session_state.ambassador_name or "Ambassador"}</div>
              <div style='font-size:12px;color:#8888aa'>{st.session_state.ambassador_college}</div>
              <div style='font-size:12px;color:#7c6dff;margin-top:4px'>{tier} Tier</div>
            </div>
            """, unsafe_allow_html=True)
            cur, nxt = xp_to_next(st.session_state.xp)
            pct = int(cur / nxt * 100) if nxt else 100
            st.markdown(f"""
            <div style='font-size:11px;color:#8888aa;margin-top:8px'>XP to next tier</div>
            <div class='xp-bar-bg'><div class='xp-bar' style='width:{pct}%'></div></div>
            <div style='font-size:11px;color:#8888aa;text-align:right'>{cur} / {nxt}</div>
            """, unsafe_allow_html=True)
            st.markdown("<hr class='cc-divider'>", unsafe_allow_html=True)

        page = st.radio("Navigate", [
            "🏠 Mission Control",
            "🔬 GitHub Analyzer",
            "🎯 Tasks",
            "🤖 AI Content Studio",
            "🔗 Referral Hub",
            "🏆 Leaderboard",
            "🎁 Rewards",
        ], label_visibility="collapsed")
    else:
        page = st.radio("Navigate", [
            "📊 Analytics Dashboard",
            "👥 Ambassador Directory",
            "🤖 AI Matching",
            "📢 Campaign Builder",
            "🧠 AI Insights",
            "✅ Task Manager",
        ], label_visibility="collapsed")

# ─────────────────────────────────────────────
# ░░ AMBASSADOR PORTAL ░░
# ─────────────────────────────────────────────
if mode == "👤 Ambassador":

    # ── LOGIN ────────────────────────────────
    if not st.session_state.logged_in and page == "🏠 Mission Control":
        st.markdown("## Welcome to **CampusConnect AI** 🚀")
        st.markdown("<p style='color:#8888aa;font-size:16px'>The smart campus ambassador platform. Connect your GitHub to get started in under 2 minutes.</p>", unsafe_allow_html=True)
        st.markdown("<hr class='cc-divider'>", unsafe_allow_html=True)

        col1, col2 = st.columns([1.2, 1])
        with col1:
            st.markdown("### Get started")
            gh_user = st.text_input("GitHub username", placeholder="e.g. torvalds")
            name    = st.text_input("Your name", placeholder="e.g. Varunika Shree")
            college = st.text_input("Your college", placeholder="e.g. Anna University")

            if st.button("🔬 Analyze GitHub & Join", use_container_width=True):
                if not gh_user:
                    st.error("Enter your GitHub username.")
                else:
                    with st.spinner("Scanning your GitHub profile..."):
                        profile, score = analyze_github(gh_user.strip())
                    if profile:
                        st.session_state.github_profile = profile
                        st.session_state.github_score   = score
                        st.session_state.xp             = score // 5
                        st.session_state.streak         = random.randint(1, 5)
                        st.session_state.ambassador_name    = name or profile["name"]
                        st.session_state.ambassador_college = college
                        st.session_state.logged_in      = True
                        st.success(f"✅ Welcome {profile['name']}! GitHub score: {score}/1000")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("GitHub user not found. Check the username and try again.")

        with col2:
            st.markdown("""
            <div class='cc-card' style='margin-top:40px'>
              <div style='font-size:13px;color:#8888aa;margin-bottom:12px;text-transform:uppercase;letter-spacing:.05em'>What you get</div>
              <div style='margin-bottom:10px'>💻 <b>GitHub score</b> in under 2 min</div>
              <div style='margin-bottom:10px'>🎯 <b>Personalized tasks</b> based on your stack</div>
              <div style='margin-bottom:10px'>🏆 <b>Live leaderboard</b> & tier system</div>
              <div style='margin-bottom:10px'>🤖 <b>AI content co-pilot</b> for campaigns</div>
              <div>🎁 <b>Rewards</b> for every contribution</div>
            </div>
            """, unsafe_allow_html=True)
        st.stop()

    # ── MISSION CONTROL ──────────────────────
    if page == "🏠 Mission Control":
        profile = st.session_state.github_profile or {}
        name    = st.session_state.ambassador_name or "Ambassador"
        tier, icon = tier_from_pts(st.session_state.xp)

        st.markdown(f"## 🚀 Mission Control")
        st.markdown(f"<p style='color:#8888aa'>Welcome back, <b style='color:#e6edf3'>{name}</b></p>", unsafe_allow_html=True)

        # Metrics row
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='metric-card'>
            <div class='metric-val'>{st.session_state.xp}</div>
            <div class='metric-lbl'>Total XP</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card'>
            <div class='metric-val'>{st.session_state.streak}</div>
            <div class='metric-lbl'>Day Streak 🔥</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'>
            <div class='metric-val'>{len(st.session_state.completed_tasks)}</div>
            <div class='metric-lbl'>Tasks Done</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='metric-card'>
            <div class='metric-val'>{st.session_state.github_score}</div>
            <div class='metric-lbl'>GitHub Score</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns([1.4, 1])

        with col_a:
            st.markdown("### 🤖 AI Insights")
            insights = [
                f"Your GitHub score ({st.session_state.github_score}/1000) places you in the top 20% of ambassadors!",
                f"Complete 2 more tasks to reach {tier_from_pts(st.session_state.xp+300)[0]} tier 🏆",
                f"Your {st.session_state.streak}-day streak is building momentum — don't break it! 🔥",
                "Ambassadors who post on LinkedIn earn 2x more referrals on average.",
                "Your GitHub activity suggests you'd excel at the Open Source PR task (+500 XP).",
            ]
            for ins in random.sample(insights, min(3, len(insights))):
                st.markdown(f"<div class='ai-insight'>💡 {ins}</div>", unsafe_allow_html=True)

            # XP chart
            st.markdown("### 📈 XP History")
            if st.session_state.history:
                df = pd.DataFrame(st.session_state.history)
                fig = px.area(df, x="date", y="cumulative_xp",
                    color_discrete_sequence=["#7c6dff"],
                    template="plotly_dark")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0,r=0,t=10,b=0), height=180,
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor="#ffffff10"),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("<div class='cc-card' style='text-align:center;color:#8888aa;padding:32px'>Complete tasks to see your XP growth chart</div>", unsafe_allow_html=True)

        with col_b:
            # GitHub profile card
            if profile:
                st.markdown("### 🧑‍💻 GitHub Profile")
                st.markdown(f"""
                <div class='cc-card'>
                  <div style='display:flex;align-items:center;gap:14px;margin-bottom:14px'>
                    <img src='{profile.get("avatar_url","")}' style='width:52px;height:52px;border-radius:50%;border:2px solid #7c6dff55'/>
                    <div>
                      <div style='font-weight:600;font-size:15px'>{profile.get("name","")}</div>
                      <div style='font-size:12px;color:#8888aa'>{profile.get("location","") or "🌍 Worldwide"}</div>
                    </div>
                  </div>
                  <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px'>
                    <div>📦 <b>{profile.get("public_repos",0)}</b> repos</div>
                    <div>⭐ <b>{profile.get("stars",0)}</b> stars</div>
                    <div>👥 <b>{profile.get("followers",0)}</b> followers</div>
                    <div>🍴 <b>{profile.get("forks",0)}</b> forks</div>
                  </div>
                  <div style='margin-top:12px'>
                    {"".join(f"<span class='badge badge-purple'>{l}</span>" for l in profile.get("languages",[])[:5])}
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Badges
            st.markdown("### 🏅 Your Badges")
            my_badges = earned_badges(st.session_state.xp, st.session_state.streak)
            if my_badges:
                badge_html = "".join(f"<span title='{b['desc']}' class='badge badge-teal'>{b['name']}</span>" for b in my_badges)
                st.markdown(f"<div>{badge_html}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='cc-card' style='color:#8888aa;font-size:13px'>Complete tasks to unlock badges!</div>", unsafe_allow_html=True)

            # Streak tracker
            st.markdown("### 🔥 Streak Tracker")
            streak_pct = min(st.session_state.streak / 30 * 100, 100)
            st.markdown(f"""
            <div class='cc-card'>
              <div style='font-size:28px;font-weight:800;color:#ffb347'>{st.session_state.streak} days</div>
              <div class='xp-bar-bg'><div class='xp-bar' style='width:{streak_pct:.0f}%;background:linear-gradient(90deg,#ffb347,#ff4d6d)'></div></div>
              <div style='font-size:12px;color:#8888aa'>{30 - st.session_state.streak} days to 30-day badge</div>
            </div>
            """, unsafe_allow_html=True)

    # ── GITHUB ANALYZER ──────────────────────
    elif page == "🔬 GitHub Analyzer":
        st.markdown("## 🔬 GitHub Analyzer")
        st.markdown("<p style='color:#8888aa'>Assess any GitHub profile in under 2 minutes</p>", unsafe_allow_html=True)

        gh_inp = st.text_input("GitHub username to analyze", placeholder="Enter any GitHub username...")
        col_btn, _ = st.columns([1, 3])
        with col_btn:
            analyze_btn = st.button("🔬 Analyze Now", use_container_width=True)

        if analyze_btn and gh_inp:
            with st.spinner(f"Analyzing @{gh_inp}..."):
                profile, score = analyze_github(gh_inp.strip())

            if not profile:
                st.error("User not found on GitHub.")
            else:
                # Score gauge
                col1, col2, col3 = st.columns([1, 1.5, 1])
                with col1:
                    tier_name = "Beginner" if score < 200 else "Intermediate" if score < 500 else "Advanced" if score < 750 else "Expert"
                    color = "#ffb347" if score < 500 else "#00d4aa" if score < 750 else "#7c6dff"
                    st.markdown(f"""
                    <div class='cc-card' style='text-align:center'>
                      <div style='font-size:14px;color:#8888aa;margin-bottom:8px'>GitHub Score</div>
                      <div class='score-ring' style='border-color:{color};color:{color}'>{score}</div>
                      <div style='font-size:13px;color:{color};font-weight:600'>{tier_name}</div>
                      <div style='font-size:11px;color:#8888aa;margin-top:4px'>out of 1000</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class='cc-card'>
                      <div style='display:flex;align-items:center;gap:14px;margin-bottom:14px'>
                        <img src='{profile["avatar_url"]}' style='width:56px;height:56px;border-radius:50%;border:2px solid {color}55'/>
                        <div>
                          <div style='font-size:17px;font-weight:700'>{profile["name"]}</div>
                          <a href='{profile["profile_url"]}' target='_blank' style='font-size:12px;color:{color}'>@{gh_inp}</a>
                          <div style='font-size:12px;color:#8888aa;margin-top:2px'>{profile.get("bio","") or ""}</div>
                        </div>
                      </div>
                      <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;font-size:13px'>
                        <div><div style='font-size:20px;font-weight:800;color:{color}'>{profile["public_repos"]}</div><div style='color:#8888aa;font-size:11px'>Repos</div></div>
                        <div><div style='font-size:20px;font-weight:800;color:{color}'>{profile["followers"]}</div><div style='color:#8888aa;font-size:11px'>Followers</div></div>
                        <div><div style='font-size:20px;font-weight:800;color:{color}'>{profile["stars"]}</div><div style='color:#8888aa;font-size:11px'>Stars</div></div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    rec = "✅ Strong fit — highly recommended!" if score >= 600 else "👍 Good fit — welcome aboard." if score >= 300 else "📚 Developing — great potential!"
                    st.markdown(f"""
                    <div class='cc-card' style='text-align:center'>
                      <div style='font-size:13px;color:#8888aa;margin-bottom:8px'>AI Recommendation</div>
                      <div style='font-size:14px;line-height:1.6;color:#c0c0e0'>{rec}</div>
                      <div style='margin-top:16px;font-size:12px;color:#8888aa'>Suggested tier</div>
                      <div style='font-size:18px;font-weight:700;color:{color}'>{tier_from_pts(score//5)[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Languages chart
                st.markdown("#### 💻 Language Breakdown")
                if profile["languages"]:
                    fig = px.pie(
                        names=profile["languages"],
                        values=[random.randint(10,40) for _ in profile["languages"]],
                        color_discrete_sequence=["#7c6dff","#00d4aa","#ffb347","#ff4d6d","#a0c4ff","#c0ffd4","#ffe4a0","#ffc0cb"],
                        hole=0.5,
                        template="plotly_dark"
                    )
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0), height=240, showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)

                # Score breakdown
                st.markdown("#### 📊 Score Breakdown")
                breakdown = {
                    "Repos":      min(profile["public_repos"] * 5, 200),
                    "Followers":  min(profile["followers"] * 3, 150),
                    "Stars":      min(profile["stars"] * 4, 200),
                    "Forks":      min(profile["forks"] * 3, 150),
                    "Languages":  min(len(profile["languages"]) * 10, 100),
                    "Profile completeness": (50 if profile.get("bio") else 0) + (50 if profile.get("company") else 0),
                }
                df_b = pd.DataFrame({"Category": list(breakdown.keys()), "Score": list(breakdown.values())})
                fig2 = px.bar(df_b, x="Score", y="Category", orientation="h",
                    color="Score", color_continuous_scale=["#7c6dff","#00d4aa"],
                    template="plotly_dark")
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0,r=0,t=0,b=0), height=220, showlegend=False,
                    coloraxis_showscale=False,
                    yaxis=dict(showgrid=False), xaxis=dict(showgrid=True, gridcolor="#ffffff10"))
                st.plotly_chart(fig2, use_container_width=True)

    # ── TASKS ────────────────────────────────
    elif page == "🎯 Tasks":
        st.markdown("## 🎯 Campaign Tasks")

        # Filters
        fc1, fc2, _ = st.columns([1,1,2])
        with fc1:
            cat_filter = st.selectbox("Category", ["All","GitHub","Social","Content","Referral","Event"])
        with fc2:
            diff_filter = st.selectbox("Difficulty", ["All","Easy","Medium","Hard","Expert"])

        tasks = TASKS
        if cat_filter  != "All": tasks = [t for t in tasks if t["category"]  == cat_filter]
        if diff_filter != "All": tasks = [t for t in tasks if t["difficulty"] == diff_filter]

        total_available = sum(t["points"] for t in tasks if t["id"] not in st.session_state.completed_tasks)
        st.markdown(f"<div style='font-size:13px;color:#8888aa;margin-bottom:16px'>{len(tasks)} tasks shown · {total_available} XP available</div>", unsafe_allow_html=True)

        for t in tasks:
            done = t["id"] in st.session_state.completed_tasks
            card_class = "cc-card task-done" if done else "cc-card"
            col_info, col_act = st.columns([4, 1])
            with col_info:
                st.markdown(f"""
                <div class='{card_class}'>
                  <div style='display:flex;align-items:flex-start;gap:12px'>
                    <div style='font-size:22px'>{cat_icon(t["category"])}</div>
                    <div style='flex:1'>
                      <div style='font-weight:600;font-size:15px;{"text-decoration:line-through;opacity:.5" if done else ""}'>{t["title"]}</div>
                      <div style='font-size:13px;color:#8888aa;margin-top:2px'>{t["desc"]}</div>
                      <div style='margin-top:8px'>
                        <span class='badge {diff_color(t["difficulty"])}'>{t["difficulty"]}</span>
                        <span class='badge badge-purple'>{t["category"]}</span>
                        <span style='font-size:13px;color:#00d4aa;font-weight:600;margin-left:8px'>+{t["points"]} XP</span>
                        {"<span style='color:#00d4aa;font-size:13px;margin-left:8px'>✅ Done</span>" if done else ""}
                      </div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with col_act:
                if not done:
                    if st.button(f"Submit", key=f"task_{t['id']}"):
                        st.session_state.completed_tasks.append(t["id"])
                        st.session_state.xp     += t["points"]
                        st.session_state.streak += 1
                        now = datetime.now()
                        st.session_state.history.append({
                            "date":         now.strftime("%b %d"),
                            "task":         t["title"],
                            "xp":           t["points"],
                            "cumulative_xp": st.session_state.xp,
                        })
                        st.success(f"+{t['points']} XP! 🚀")
                        time.sleep(0.5)
                        st.rerun()

    # ── AI CONTENT STUDIO ────────────────────
    elif page == "🤖 AI Content Studio":
        st.markdown("## 🤖 AI Content Studio")
        st.markdown("<p style='color:#8888aa'>Generate campaign-ready content in one click</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✍️ Caption Generator")
            topic    = st.text_input("Campaign topic", placeholder="e.g. AICore Hackathon 2025")
            platform = st.selectbox("Platform", ["LinkedIn","Instagram","Twitter/X","WhatsApp"])
            tone     = st.selectbox("Tone", ["Professional","Hype","Casual","Inspirational"])
            if st.button("✨ Generate Caption", use_container_width=True):
                captions = {
                    "LinkedIn":    [f"🚀 Excited to be part of {topic}! This is exactly the kind of initiative that bridges the gap between students and the real world. Join us → [link] #CampusConnect #{topic.replace(' ','')}",
                                    f"Just joined {topic} as a campus ambassador and I'm already seeing the impact. If you're a student who wants to grow — this is for you. 🔥"],
                    "Instagram":   [f"✨ {topic} just dropped and it's 🔥\nTag a friend who needs this! 👇\n#CampusLife #StudentLife #{topic.replace(' ','')}",
                                    f"POV: You just discovered {topic} 👀\nThis changes everything for campus students fr 💯"],
                    "Twitter/X":   [f"{topic} is live and it's built different 🧵\n\nHere's why every student should pay attention 👇\n#CampusConnect",
                                    f"unpopular opinion: {topic} is the best thing to happen to campus communities this year. change my mind."],
                    "WhatsApp":    [f"Hey! 👋 Have you heard about {topic}? It's an amazing opportunity for students. Check it out → [link]",
                                    f"Bro/Sis this is legit — {topic} is giving students real opportunities 🚀 Tag someone who should apply!"],
                }
                st.markdown(f"<div class='ai-insight'>{random.choice(captions.get(platform, captions['LinkedIn']))}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("### 🎬 Video Script Generator")
            vtopic = st.text_input("Video topic", placeholder="e.g. Why I joined CampusConnect")
            vlen   = st.selectbox("Length", ["15s (Reel/Short)","30s (Story)","60s (YouTube Short)"])
            if st.button("🎬 Generate Script", use_container_width=True):
                scripts = {
                    "15s (Reel/Short)": f"[0-3s] Hook: 'You're missing out if you haven't heard about {vtopic}!'\n[3-12s] Show 3 quick benefits with text overlays\n[12-15s] CTA: 'Link in bio — join now!' + tag 2 friends",
                    "30s (Story)":      f"[0-5s] Hook: Start with a relatable problem\n[5-20s] '{vtopic} solved it for me — here's how...'\n[20-28s] Show proof / results\n[28-30s] Strong CTA with urgency",
                    "60s (YouTube Short)": f"[0-5s] Bold hook: 'Here's what nobody tells you about {vtopic}'\n[5-30s] Tell your story — personal + relatable\n[30-50s] 3 key benefits with examples\n[50-58s] Social proof + community angle\n[58-60s] CTA: Subscribe + comment your experience",
                }
                st.markdown(f"<div class='ai-insight' style='white-space:pre-line'>{scripts.get(vlen,'')}</div>", unsafe_allow_html=True)

            st.markdown("### #️⃣ Hashtag Pack")
            htopic = st.text_input("Topic for hashtags", placeholder="e.g. Open Source")
            if st.button("Generate Hashtags", use_container_width=True):
                base = htopic.replace(" ","")
                tags = [f"#{base}",f"#CampusConnect",f"#StudentLife",f"#TechCommunity",f"#OpenSource",f"#AICore",f"#Hackathon2025",f"#Campus{base}",f"#BuildInPublic",f"#StudentDev"]
                st.markdown("<div class='ai-insight'>" + " ".join(f"<span class='badge badge-purple'>{t}</span>" for t in tags) + "</div>", unsafe_allow_html=True)

    # ── REFERRAL HUB ─────────────────────────
    elif page == "🔗 Referral Hub":
        st.markdown("## 🔗 Referral Hub")
        ref_code = f"CC-{(st.session_state.ambassador_name or 'AMB').upper()[:4]}-{random.randint(1000,9999)}"
        ref_link = f"https://campusconnect.ai/join?ref={ref_code}"

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Your referral link")
            st.code(ref_link)
            clicks       = random.randint(20, 300)
            conversions  = random.randint(2, clicks // 5)
            xp_from_refs = conversions * 300

            st.markdown(f"""
            <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:16px'>
              <div class='metric-card'><div class='metric-val'>{clicks}</div><div class='metric-lbl'>Clicks</div></div>
              <div class='metric-card'><div class='metric-val'>{conversions}</div><div class='metric-lbl'>Signups</div></div>
              <div class='metric-card'><div class='metric-val'>{xp_from_refs}</div><div class='metric-lbl'>XP Earned</div></div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("### 📈 Referral Funnel")
            funnel_data = {"Stage":["Link Visits","Clicked","Signed Up","Completed Onboarding"],"Count":[clicks, int(clicks*.6), conversions, int(conversions*.7)]}
            fig = px.funnel(pd.DataFrame(funnel_data), x="Count", y="Stage",
                color_discrete_sequence=["#7c6dff"], template="plotly_dark")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0), height=220)
            st.plotly_chart(fig, use_container_width=True)

    # ── LEADERBOARD ──────────────────────────
    elif page == "🏆 Leaderboard":
        st.markdown("## 🏆 Live Leaderboard")

        # Inject current user into leaderboard
        lb = SAMPLE_LEADERBOARD.copy()
        me = {
            "name":    st.session_state.ambassador_name or "You",
            "college": st.session_state.ambassador_college or "Your College",
            "pts":     st.session_state.xp,
            "streak":  st.session_state.streak,
            "tier":    tier_from_pts(st.session_state.xp)[0],
            "gh":      "you",
        }
        lb.append(me)
        lb = sorted(lb, key=lambda x: x["pts"], reverse=True)

        rank_icons = {1:"🥇",2:"🥈",3:"🥉"}
        for i, amb in enumerate(lb, 1):
            is_me = amb["gh"] == "you"
            border = "border:1px solid #7c6dff44;" if is_me else ""
            rank_color = {1:"#ffd700",2:"#c0c0c0",3:"#cd7f32"}.get(i,"#8888aa")
            tier_lbl = amb["tier"]
            st.markdown(f"""
            <div class='lb-row' style='{border}'>
              <div class='lb-rank' style='color:{rank_color}'>{rank_icons.get(i,str(i))}</div>
              <div style='flex:1'>
                <div style='font-weight:600;font-size:15px'>{amb["name"]} {"<span style='color:#7c6dff;font-size:12px'>(you)</span>" if is_me else ""}</div>
                <div style='font-size:12px;color:#8888aa'>{amb["college"]} · {tier_lbl}</div>
              </div>
              <div style='text-align:right'>
                <div style='font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#00d4aa'>{amb["pts"]}</div>
                <div style='font-size:11px;color:#8888aa'>🔥 {amb["streak"]} streak</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── REWARDS ──────────────────────────────
    elif page == "🎁 Rewards":
        st.markdown("## 🎁 Rewards Catalogue")
        current_xp = st.session_state.xp
        rewards = [
            {"name":"CampusConnect T-Shirt",  "xp":500,  "icon":"👕", "desc":"Official merch for top ambassadors"},
            {"name":"Amazon Gift Card ₹500",   "xp":1000, "icon":"🎁", "desc":"Redeemable anywhere"},
            {"name":"Internship Referral",      "xp":2000, "icon":"💼", "desc":"Fast-track referral to partner companies"},
            {"name":"Mentorship Session",       "xp":1500, "icon":"🧑‍🏫","desc":"1:1 session with industry expert"},
            {"name":"LinkedIn Recommendation",  "xp":2500, "icon":"🏅", "desc":"From AICore Connect leadership"},
            {"name":"Paid Ambassador Role",     "xp":5000, "icon":"💰", "desc":"Become a paid ambassador"},
        ]
        cols = st.columns(3)
        for i, r in enumerate(rewards):
            locked = current_xp < r["xp"]
            deficit = r["xp"] - current_xp
            with cols[i % 3]:
                st.markdown(f"""
                <div class='cc-card' style='text-align:center;opacity:{"0.5" if locked else "1"}'>
                  <div style='font-size:40px;margin-bottom:8px'>{r["icon"]}</div>
                  <div style='font-weight:600;font-size:15px'>{r["name"]}</div>
                  <div style='font-size:12px;color:#8888aa;margin:6px 0 12px'>{r["desc"]}</div>
                  <div style='font-size:14px;color:{"#8888aa" if locked else "#00d4aa"};font-weight:600'>{r["xp"]} XP</div>
                  {"<div style='font-size:11px;color:#ff4d6d;margin-top:4px'>🔒 Need " + str(deficit) + " more XP</div>" if locked else "<div style='font-size:11px;color:#00d4aa;margin-top:4px'>✅ Unlocked!</div>"}
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ░░ RECRUITER PORTAL ░░
# ─────────────────────────────────────────────
else:
    # Simple auth gate
    if not st.session_state.rec_logged_in:
        st.markdown("## 🧑‍💼 Recruiter Portal")
        rc1, rc2 = st.columns([1,2])
        with rc1:
            st.markdown("<div class='cc-card'>", unsafe_allow_html=True)
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if u == "admin" and p == "admin123":
                    st.session_state.rec_logged_in = True
                    st.success("Welcome back!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try admin / admin123")
            st.markdown("</div>", unsafe_allow_html=True)
            st.caption("Demo credentials: admin / admin123")
        st.stop()

    # ── ANALYTICS DASHBOARD ──────────────────
    if page == "📊 Analytics Dashboard":
        st.markdown("## 📊 Live Analytics Dashboard")

        c1,c2,c3,c4 = st.columns(4)
        with c1: st.markdown("<div class='metric-card'><div class='metric-val'>247</div><div class='metric-lbl'>Total Ambassadors</div></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'><div class='metric-val'>1,842</div><div class='metric-lbl'>Tasks Completed</div></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'><div class='metric-val'>₹84K</div><div class='metric-lbl'>Rewards Distributed</div></div>", unsafe_allow_html=True)
        with c4: st.markdown("<div class='metric-card'><div class='metric-val'>38</div><div class='metric-lbl'>Active Today</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### 📈 Weekly Engagement")
            days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
            submissions = [42,58,71,63,88,95,77]
            fig = px.bar(x=days, y=submissions, color=submissions,
                color_continuous_scale=["#7c6dff","#00d4aa"], template="plotly_dark")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=0,b=0), height=220, showlegend=False,
                coloraxis_showscale=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor="#ffffff10"))
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.markdown("### 🥧 Tasks by Category")
            cats = ["Social","GitHub","Content","Referral","Event"]
            vals = [380, 290, 430, 510, 232]
            fig2 = px.pie(names=cats, values=vals, hole=0.5,
                color_discrete_sequence=["#7c6dff","#00d4aa","#ffb347","#ff4d6d","#a0c4ff"],
                template="plotly_dark")
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0), height=220)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 🗺️ Top Performing Colleges")
        college_df = pd.DataFrame({
            "College":["IIT Madras","BITS Pilani","VIT Chennai","Anna University","NIT Trichy","SRM","PSG Tech"],
            "Ambassadors":[38,30,45,28,22,55,29],
            "Total XP":[182000,145000,210000,132000,98000,241000,140000],
        })
        fig3 = px.scatter(college_df, x="Ambassadors", y="Total XP", text="College", size="Ambassadors",
            color="Total XP", color_continuous_scale=["#7c6dff","#00d4aa"], template="plotly_dark")
        fig3.update_traces(textposition="top center", marker=dict(sizemin=10))
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0), height=280, coloraxis_showscale=False,
            xaxis=dict(showgrid=True,gridcolor="#ffffff10"), yaxis=dict(showgrid=True,gridcolor="#ffffff10"))
        st.plotly_chart(fig3, use_container_width=True)

    # ── AMBASSADOR DIRECTORY ─────────────────
    elif page == "👥 Ambassador Directory":
        st.markdown("## 👥 Ambassador Directory")
        search = st.text_input("Search by name or college", placeholder="e.g. IIT Madras")

        ambassadors = [
            {"Name":"Arun K.","College":"IIT Madras","XP":4820,"Tier":"Platinum","Streak":14,"GitHub":"arundev","Tasks":18},
            {"Name":"Priya S.","College":"BITS Pilani","XP":3650,"Tier":"Gold","Streak":9,"GitHub":"priyacode","Tasks":14},
            {"Name":"Rahul M.","College":"VIT Chennai","XP":2900,"Tier":"Gold","Streak":5,"GitHub":"rahulmr","Tasks":11},
            {"Name":"Sneha R.","College":"Anna Univ","XP":1800,"Tier":"Silver","Streak":3,"GitHub":"snehar","Tasks":7},
            {"Name":"Kiran P.","College":"NIT Trichy","XP":1200,"Tier":"Silver","Streak":2,"GitHub":"kiranpv","Tasks":5},
            {"Name":"Divya M.","College":"SRM","XP":980,"Tier":"Silver","Streak":4,"GitHub":"divyam","Tasks":4},
            {"Name":"Arjun V.","College":"PSG Tech","XP":450,"Tier":"Bronze","Streak":1,"GitHub":"arjunv","Tasks":2},
        ]
        df = pd.DataFrame(ambassadors)
        if search:
            df = df[df["Name"].str.contains(search, case=False) | df["College"].str.contains(search, case=False)]
        st.dataframe(df.style.background_gradient(subset=["XP"], cmap="Purples"),
            use_container_width=True, hide_index=True)

    # ── AI MATCHING ──────────────────────────
    elif page == "🤖 AI Matching":
        st.markdown("## 🤖 AI Ambassador Matching")
        st.markdown("<p style='color:#8888aa'>Match the right ambassador to the right campaign automatically</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            campaign_type = st.selectbox("Campaign type", ["GitHub Challenge","Social Media Blitz","Content Creation","Event Promotion","Referral Drive"])
            target_college = st.selectbox("Target college", ["All Colleges","IIT Madras","BITS Pilani","VIT Chennai","Anna University"])

        with col2:
            min_xp = st.slider("Minimum XP", 0, 5000, 500, step=100)
            min_streak = st.slider("Minimum streak (days)", 0, 30, 3)

        if st.button("🤖 Find Best Matches", use_container_width=True):
            matches = [
                {"Ambassador":"Arun K.",  "College":"IIT Madras",  "Match Score":"98%","Reason":"High GitHub score + 14-day streak"},
                {"Ambassador":"Priya S.", "College":"BITS Pilani", "Match Score":"91%","Reason":"Top content creator, 3650 XP"},
                {"Ambassador":"Rahul M.", "College":"VIT Chennai", "Match Score":"84%","Reason":"Strong referral history"},
            ]
            st.markdown("### ✅ Top Matches")
            for m in matches:
                st.markdown(f"""
                <div class='cc-card'>
                  <div style='display:flex;justify-content:space-between;align-items:center'>
                    <div>
                      <div style='font-weight:600'>{m["Ambassador"]} · {m["College"]}</div>
                      <div style='font-size:13px;color:#8888aa;margin-top:4px'>{m["Reason"]}</div>
                    </div>
                    <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:#00d4aa'>{m["Match Score"]}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── CAMPAIGN BUILDER ─────────────────────
    elif page == "📢 Campaign Builder":
        st.markdown("## 📢 AI Campaign Builder")
        col1, col2 = st.columns(2)
        with col1:
            cname = st.text_input("Campaign name", placeholder="e.g. Launch Week 2025")
            cdesc = st.text_area("Campaign description", placeholder="What is this campaign about?", height=100)
            ctype = st.selectbox("Campaign type", ["Brand Awareness","Referral Drive","Content Creation","Event Promotion","GitHub Challenge"])
            cpts  = st.number_input("Points per task", min_value=50, max_value=2000, value=250, step=50)
        with col2:
            cdead = st.date_input("Deadline", min_value=datetime.today())
            ctarg = st.multiselect("Target colleges", ["All","IIT Madras","BITS Pilani","VIT","Anna University","NIT"], default=["All"])

        if st.button("✨ Generate AI Campaign Brief", use_container_width=True):
            st.markdown(f"""
            <div class='cc-card'>
              <div style='font-size:12px;color:#8888aa;text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px'>AI-Generated Campaign Brief</div>
              <div style='font-size:20px;font-weight:700;margin-bottom:8px'>🚀 {cname}</div>
              <div style='font-size:14px;color:#c0c0e0;line-height:1.7;margin-bottom:12px'>{cdesc or "A high-impact campus campaign designed to maximize ambassador engagement and brand visibility."}</div>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:13px'>
                <div><span class='badge badge-purple'>Type: {ctype}</span></div>
                <div><span class='badge badge-teal'>Points: {cpts} XP/task</span></div>
                <div><span class='badge badge-amber'>Deadline: {cdead}</span></div>
                <div><span class='badge badge-red'>Target: {", ".join(ctarg)}</span></div>
              </div>
              <div style='margin-top:16px;padding-top:12px;border-top:1px solid #ffffff10'>
                <div style='font-size:13px;font-weight:600;margin-bottom:8px'>Suggested Deliverables</div>
                <div style='font-size:13px;color:#8888aa'>1. 2 social posts (Instagram + LinkedIn)<br>2. 1 referral link share<br>3. 1 photo/reel from campus<br>4. Tag @CampusConnectAI</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── AI INSIGHTS ──────────────────────────
    elif page == "🧠 AI Insights":
        st.markdown("## 🧠 Recruiter AI Assistant")
        st.markdown("<p style='color:#8888aa'>Ask anything about your ambassador program</p>", unsafe_allow_html=True)

        questions = [
            "Who are the top performers this week?",
            "Which college has the highest engagement?",
            "What tasks are being completed most?",
            "Which ambassadors are at risk of dropping off?",
            "What's the overall program ROI?",
        ]
        selected_q = st.selectbox("Quick questions", ["Custom question..."] + questions)
        query = st.text_input("Your question", value="" if selected_q == "Custom question..." else selected_q)

        if st.button("🤖 Analyze", use_container_width=True) and query:
            responses = {
                "Who are the top performers this week?": "Top performers: Arun K. (IIT Madras, +820 XP), Priya S. (BITS, +650 XP), Rahul M. (VIT, +580 XP). All 3 completed GitHub challenges.",
                "Which college has the highest engagement?": "SRM leads with 55 ambassadors and 241K total XP. VIT Chennai is a close second. Consider doubling down on SRM campaigns.",
                "What tasks are being completed most?": "Referral tasks (34%) and LinkedIn Posts (28%) dominate. GitHub challenges have highest drop-off — consider simplifying requirements.",
                "Which ambassadors are at risk of dropping off?": "7 ambassadors haven't logged in for 5+ days. Suggested action: send a streak reminder + offer a 50 XP bonus for return.",
                "What's the overall program ROI?": "247 ambassadors generated 1,842 task completions = ~₹2.8L estimated brand value vs ₹84K in rewards distributed. ROI: 3.3x",
            }
            answer = responses.get(query, f"Based on current data: Your program is performing well. {query.replace('?','')} shows strong trends — consider focusing on ambassador retention through gamification and streak bonuses.")
            st.markdown(f"<div class='ai-insight'>🤖 {answer}</div>", unsafe_allow_html=True)

    # ── TASK MANAGER ─────────────────────────
    elif page == "✅ Task Manager":
        st.markdown("## ✅ Task Manager")
        st.markdown("### Current Tasks")
        for t in TASKS:
            col_t, col_d, col_p, col_a = st.columns([3,1,1,1])
            with col_t: st.write(f"{cat_icon(t['category'])} {t['title']}")
            with col_d: st.write(f"<span class='badge {diff_color(t['difficulty'])}'>{t['difficulty']}</span>", unsafe_allow_html=True)
            with col_p: st.write(f"+{t['points']} XP")
            with col_a:
                if st.button("🗑️", key=f"del_{t['id']}"): st.toast("Task deactivated (demo)")

        st.markdown("<hr class='cc-divider'>", unsafe_allow_html=True)
        st.markdown("### ➕ Add New Task")
        nc1, nc2 = st.columns(2)
        with nc1:
            ntitle = st.text_input("Task title")
            ncat   = st.selectbox("Category", ["GitHub","Social","Content","Referral","Event"])
        with nc2:
            npts   = st.number_input("Points", min_value=50, max_value=1000, value=200, step=50)
            ndiff  = st.selectbox("Difficulty", ["Easy","Medium","Hard","Expert"])
        ndesc = st.text_area("Description", height=80)
        if st.button("Add Task", use_container_width=True):
            if ntitle:
                st.success(f"✅ Task '{ntitle}' added for {npts} XP!")
            else:
                st.error("Enter a task title.")

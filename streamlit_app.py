import streamlit as st
import time
from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline
from utils.job_matcher import compute_similarity
from utils.skill_analyzer import skill_gap_analysis


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Apex Careers — AI Job Hunt",
    page_icon="◈",
    layout="wide"
)

# --------------------------------------------------
# Session State Init
# --------------------------------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "confetti_fired" not in st.session_state:
    st.session_state.confetti_fired = False

is_dark = st.session_state.theme == "dark"

# --------------------------------------------------
# THEME VARIABLES
# --------------------------------------------------

if is_dark:
    BG        = "#070709"
    BG2       = "#0F0F12"
    BG3       = "#161619"
    BG4       = "#1E1E23"
    TEXT      = "#F0E6CC"
    SILVER    = "#8A929E"
    BORDER    = "rgba(212,168,67,0.15)"
    CARD_BG   = "#0F0F12"
    SIDEBAR   = "#0F0F12"
    TOGGLE_BG = "#1E1E23"
    TOGGLE_ICON = "☀️"
    TOGGLE_LABEL = "Light Mode"
else:
    BG        = "#F5F0E8"
    BG2       = "#FFFFFF"
    BG3       = "#F0EBE0"
    BG4       = "#E8E0D0"
    TEXT      = "#1A1206"
    SILVER    = "#5A5040"
    BORDER    = "rgba(160,100,20,0.2)"
    CARD_BG   = "#FFFFFF"
    SIDEBAR   = "#FAF6EE"
    TOGGLE_BG = "#E8E0D0"
    TOGGLE_ICON = "🌙"
    TOGGLE_LABEL = "Dark Mode"

GOLD       = "#D4A843"
GOLD_BRIGHT= "#F5C842"
GOLD_DIM   = "#7A5E18"
GREEN      = "#3EC98A"
RED        = "#E05252"

# --------------------------------------------------
# MASTER CSS
# --------------------------------------------------

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=Epilogue:wght@200;300;400;500;600;700&display=swap');

:root {{
  --gold:         {GOLD};
  --gold-bright:  {GOLD_BRIGHT};
  --gold-dim:     {GOLD_DIM};
  --cream:        {TEXT};
  --bg:           {BG};
  --bg2:          {BG2};
  --bg3:          {BG3};
  --bg4:          {BG4};
  --silver:       {SILVER};
  --green:        {GREEN};
  --red:          {RED};
  --border:       {BORDER};
  --card:         {CARD_BG};
  --sidebar:      {SIDEBAR};
}}

/* ── KEYFRAMES ── */

@keyframes fadeUp {{
  from {{ opacity:0; transform:translateY(22px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes fadeIn {{
  from {{ opacity:0; }}
  to   {{ opacity:1; }}
}}
@keyframes shimmer {{
  0%   {{ background-position:-400px 0; }}
  100% {{ background-position:400px 0; }}
}}
@keyframes goldPulse {{
  0%,100% {{ box-shadow:0 0 0 0 rgba(212,168,67,0); }}
  50%      {{ box-shadow:0 0 22px 6px rgba(212,168,67,0.2); }}
}}
@keyframes scanline {{
  0%   {{ top:-2%; }}
  100% {{ top:104%; }}
}}
@keyframes rotateStar {{
  from {{ transform:rotate(0deg); }}
  to   {{ transform:rotate(360deg); }}
}}
@keyframes floatDot {{
  0%,100% {{ transform:translateY(0) scale(1);   opacity:0.5; }}
  50%     {{ transform:translateY(-12px) scale(1.3); opacity:1; }}
}}
@keyframes blink {{
  0%,100% {{ opacity:1; }}
  50%     {{ opacity:0.15; }}
}}
@keyframes slideInLeft {{
  from {{ opacity:0; transform:translateX(-28px); }}
  to   {{ opacity:1; transform:translateX(0); }}
}}
@keyframes goldTraceSweep {{
  0%   {{ left:-100%; opacity:0; }}
  15%  {{ opacity:1; }}
  85%  {{ opacity:1; }}
  100% {{ left:120%; opacity:0; }}
}}
@keyframes cardReveal {{
  from {{ opacity:0; transform:translateX(-14px); }}
  to   {{ opacity:1; transform:translateX(0); }}
}}
@keyframes metricPop {{
  from {{ opacity:0; transform:scale(0.75); }}
  to   {{ opacity:1; transform:scale(1); }}
}}
@keyframes progressFill {{
  from {{ width:0%; }}
  to   {{ width:100%; }}
}}
@keyframes confettiFall {{
  0%   {{ transform:translateY(-20px) rotate(0deg); opacity:1; }}
  100% {{ transform:translateY(100vh) rotate(720deg); opacity:0; }}
}}
@keyframes arcDraw {{
  from {{ stroke-dashoffset:283; }}
  to   {{ stroke-dashoffset:var(--dash-offset); }}
}}
@keyframes typewriter {{
  from {{ clip-path:inset(0 100% 0 0); }}
  to   {{ clip-path:inset(0 0% 0 0); }}
}}
@keyframes cursorBlink {{
  0%,100% {{ opacity:1; }}
  50%     {{ opacity:0; }}
}}
@keyframes themeSwitch {{
  0%   {{ opacity:0; transform:scale(0.95); }}
  100% {{ opacity:1; transform:scale(1); }}
}}

/* ── BASE ── */
*, *::before, *::after {{ box-sizing:border-box; }}

html, body, .stApp {{
  font-family:'Epilogue',sans-serif;
  background:var(--bg) !important;
  color:var(--cream);
  min-height:100vh;
  transition:background 0.4s, color 0.4s;
  animation:themeSwitch 0.35s ease both;
}}

/* Scanline — dark only */
{"" if not is_dark else """
.stApp::before {
  content:'';
  position:fixed;
  left:0; top:0;
  width:100%; height:5px;
  background:linear-gradient(90deg,
    transparent 0%,
    rgba(212,168,67,0.03) 40%,
    rgba(212,168,67,0.12) 50%,
    rgba(212,168,67,0.03) 60%,
    transparent 100%);
  animation:scanline 9s linear infinite;
  pointer-events:none;
  z-index:9998;
}
"""}

/* Grain */
.stApp::after {{
  content:'';
  position:fixed; inset:0;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events:none;
  z-index:9997;
  opacity:{0.5 if is_dark else 0.15};
}}

::-webkit-scrollbar {{ width:4px; }}
::-webkit-scrollbar-track {{ background:var(--bg); }}
::-webkit-scrollbar-thumb {{ background:{GOLD_DIM}; border-radius:2px; }}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
  background:var(--sidebar) !important;
  border-right:1px solid var(--border) !important;
  animation:fadeIn 0.7s ease both;
}}
section[data-testid="stSidebar"] h1 {{
  font-family:'Playfair Display',serif !important;
  font-size:17px !important; font-weight:900 !important;
  color:var(--gold) !important; letter-spacing:0.04em !important;
}}
section[data-testid="stSidebar"] .stMarkdown h3 {{
  font-family:'Epilogue',sans-serif !important;
  font-size:9px !important; font-weight:600 !important;
  letter-spacing:0.28em !important; text-transform:uppercase !important;
  color:var(--gold-dim) !important; margin:22px 0 10px !important;
}}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {{
  font-size:12.5px !important; color:var(--silver) !important; line-height:2 !important;
}}

/* ── THEME TOGGLE BUTTON ── */
.theme-toggle {{
  display:inline-flex;
  align-items:center;
  gap:9px;
  background:{TOGGLE_BG};
  border:1px solid var(--border);
  border-radius:100px;
  padding:8px 18px 8px 12px;
  cursor:pointer;
  font-family:'Epilogue',sans-serif;
  font-size:11px;
  font-weight:600;
  letter-spacing:0.12em;
  text-transform:uppercase;
  color:var(--gold);
  transition:box-shadow 0.2s, border-color 0.2s, transform 0.15s;
  user-select:none;
}}
.theme-toggle:hover {{
  border-color:var(--gold);
  box-shadow:0 0 14px rgba(212,168,67,0.2);
  transform:scale(1.03);
}}
.theme-toggle-dot {{
  width:18px; height:18px;
  border-radius:50%;
  background:var(--gold);
  display:flex; align-items:center; justify-content:center;
  font-size:11px;
  animation:goldPulse 3s ease-in-out infinite;
}}

/* ── HERO ── */
.hero {{
  position:relative;
  padding:80px 64px 68px;
  margin-bottom:52px;
  overflow:hidden;
  border-bottom:1px solid var(--border);
  animation:fadeUp 0.7s ease both;
}}
.hero-beam {{
  position:absolute;
  top:-120px; right:-60px;
  width:420px; height:700px;
  background:linear-gradient(160deg,
    rgba(212,168,67,{0.07 if is_dark else 0.04}) 0%,
    transparent 70%);
  transform:rotate(-18deg);
  pointer-events:none;
}}
.hero-dot {{
  position:absolute; width:3px; height:3px;
  border-radius:50%; background:var(--gold);
}}
.hero-dot:nth-child(1) {{ top:22%; right:26%; animation:floatDot 3.2s 0.0s ease-in-out infinite; }}
.hero-dot:nth-child(2) {{ top:56%; right:19%; animation:floatDot 4.1s 0.7s ease-in-out infinite; }}
.hero-dot:nth-child(3) {{ top:36%; right:39%; animation:floatDot 2.8s 1.4s ease-in-out infinite; }}
.hero-dot:nth-child(4) {{ top:72%; right:31%; animation:floatDot 3.7s 0.3s ease-in-out infinite; opacity:0.4; }}

.hero-watermark {{
  position:absolute; bottom:-30px; right:-20px;
  font-family:'Playfair Display',serif;
  font-size:220px; font-weight:900; font-style:italic;
  color:rgba(212,168,67,{0.035 if is_dark else 0.06});
  line-height:1; user-select:none; pointer-events:none;
  letter-spacing:-0.05em;
  animation:fadeIn 1.5s 0.8s ease both;
}}
.hero-eyebrow {{
  display:inline-flex; align-items:center; gap:10px;
  font-size:9px; font-weight:600; letter-spacing:0.35em;
  text-transform:uppercase; color:var(--gold); margin-bottom:26px;
  animation:slideInLeft 0.6s 0.2s ease both;
}}
.hero-eyebrow-line {{
  display:inline-block; width:32px; height:1px; background:var(--gold);
}}
.hero-star {{
  display:inline-block; font-size:13px; color:var(--gold);
  animation:rotateStar 8s linear infinite; margin-right:6px;
}}

/* ── TYPEWRITER HEADLINE ── */
.hero-title-wrap {{
  position:relative;
  display:inline-block;
  overflow:visible;
  margin-bottom:4px;
}}
.hero-title {{
  font-family:'Playfair Display',serif;
  font-size:72px; font-weight:900; line-height:1.0;
  letter-spacing:-0.025em; color:var(--cream);
  display:block;
  animation:fadeUp 0.7s 0.3s ease both;
}}
.hero-title em {{
  font-style:italic; color:var(--gold); position:relative;
}}
.hero-title em::after {{
  content:'';
  position:absolute; left:0; bottom:-4px;
  height:2px; width:100%;
  background:linear-gradient(90deg,var(--gold),transparent);
  animation:fadeIn 0.8s 1.4s ease both;
  opacity:0; animation-fill-mode:forwards;
}}

/* Typewriter line 2 */
.hero-title-typed {{
  font-family:'Playfair Display',serif;
  font-size:72px; font-weight:900; line-height:1.0;
  letter-spacing:-0.025em; color:var(--gold); font-style:italic;
  display:inline-block;
  overflow:hidden; white-space:nowrap;
  animation:typewriter 1.4s 0.9s steps(12) both;
  clip-path:inset(0 100% 0 0);
  animation:typewriter 1.4s 0.9s steps(12,end) forwards;
}}
.hero-cursor {{
  display:inline-block;
  width:3px; height:68px;
  background:var(--gold);
  vertical-align:bottom;
  margin-left:4px;
  animation:cursorBlink 0.9s 0.9s step-end infinite;
  border-radius:1px;
}}

.hero-sub {{
  font-size:15px; font-weight:300; color:var(--silver);
  max-width:520px; line-height:1.9; margin-top:22px;
  animation:fadeUp 0.7s 0.5s ease both;
}}
.hero-rule {{
  display:flex; align-items:center; gap:14px;
  margin-top:36px;
  animation:fadeIn 0.8s 1s ease both; opacity:0;
  animation-fill-mode:forwards;
}}
.hero-rule-line {{ width:50px; height:1px; background:var(--gold); }}
.hero-rule-text {{
  font-size:9px; font-weight:600; letter-spacing:0.3em;
  text-transform:uppercase; color:var(--gold-dim);
}}
.hero-rule-dots {{ display:flex; gap:5px; }}
.hero-rule-dot {{
  width:4px; height:4px; border-radius:50%; background:var(--gold);
}}
.hero-rule-dot:nth-child(1) {{ animation:blink 1.6s 0.0s infinite; }}
.hero-rule-dot:nth-child(2) {{ animation:blink 1.6s 0.3s infinite; }}
.hero-rule-dot:nth-child(3) {{ animation:blink 1.6s 0.6s infinite; }}

/* ── PROGRESS BAR ── */
.apex-progress-wrap {{
  margin:18px 0 8px;
  animation:fadeIn 0.5s ease both;
}}
.apex-progress-label {{
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:8px;
  font-size:9px; font-weight:600; letter-spacing:0.25em;
  text-transform:uppercase; color:var(--gold-dim);
}}
.apex-progress-track {{
  width:100%; height:3px;
  background:var(--bg4);
  border-radius:2px; overflow:hidden;
  position:relative;
}}
.apex-progress-fill {{
  height:100%; border-radius:2px;
  background:linear-gradient(90deg, var(--gold-dim), var(--gold), var(--gold-bright));
  animation:progressFill var(--dur) cubic-bezier(0.4,0,0.2,1) both;
  box-shadow:0 0 8px rgba(212,168,67,0.5);
  position:relative;
}}
/* shimmer on bar */
.apex-progress-fill::after {{
  content:'';
  position:absolute; top:0; left:0;
  width:60%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.35),transparent);
  animation:goldTraceSweep 1.8s ease-in-out infinite;
}}

/* ── PROFILE CARD ── */
.profile-card {{
  position:relative;
  background:var(--bg2);
  border:1px solid var(--border);
  border-top:2px solid var(--gold);
  padding:44px 40px 36px;
  margin-bottom:32px; overflow:hidden;
  animation:fadeUp 0.7s 0.15s ease both;
}}
.profile-card::before {{
  content:'';
  position:absolute; top:0; left:-100%;
  width:60%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(212,168,67,{0.04 if is_dark else 0.03}),transparent);
  animation:goldTraceSweep 5s 1s ease-in-out infinite;
  pointer-events:none;
}}
.profile-header {{
  display:flex; align-items:center; gap:14px;
  margin-bottom:32px; padding-bottom:20px;
  border-bottom:1px solid var(--border);
}}
.profile-icon-ring {{
  width:44px; height:44px; border-radius:50%;
  border:1px solid var(--gold);
  display:flex; align-items:center; justify-content:center;
  animation:goldPulse 3s ease-in-out infinite; flex-shrink:0;
}}
.profile-icon {{ font-size:19px; animation:rotateStar 12s linear infinite; }}
.profile-label {{
  font-family:'Epilogue',sans-serif; font-size:9px; font-weight:600;
  letter-spacing:0.35em; text-transform:uppercase; color:var(--gold-dim); margin-bottom:3px;
}}
.profile-title {{
  font-family:'Playfair Display',serif; font-size:20px;
  font-weight:700; color:var(--cream); letter-spacing:-0.01em;
}}
.profile-status {{
  margin-left:auto; display:flex; align-items:center; gap:7px;
  font-size:9px; font-weight:600; letter-spacing:0.2em;
  text-transform:uppercase; color:var(--green);
}}
.profile-status-dot {{
  width:6px; height:6px; border-radius:50%; background:var(--green);
  animation:blink 2s ease-in-out infinite;
}}

/* ── INPUT FIELDS ── */
.stTextInput label, .stTextArea label {{
  font-family:'Epilogue',sans-serif !important;
  font-size:9px !important; font-weight:600 !important;
  letter-spacing:0.28em !important; text-transform:uppercase !important;
  color:var(--gold-dim) !important; transition:color 0.2s !important;
}}
.stTextInput:focus-within label, .stTextArea:focus-within label {{
  color:var(--gold) !important;
}}
.stTextInput input, .stTextArea textarea {{
  background:var(--bg3) !important;
  border:1px solid {BORDER} !important;
  border-radius:3px !important;
  color:var(--cream) !important;
  font-family:'Epilogue',sans-serif !important;
  font-size:14px !important; font-weight:300 !important;
  caret-color:var(--gold) !important;
  transition:border-color 0.25s, box-shadow 0.25s, background 0.25s !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
  border-color:var(--gold) !important;
  background:var(--bg3) !important;
  box-shadow:0 0 0 2px rgba(212,168,67,0.1), 0 0 28px rgba(212,168,67,0.06) !important;
}}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {{
  color:rgba(138,146,158,0.3) !important;
}}

/* ── BUTTON ── */
div.stButton > button {{
  font-family:'Epilogue',sans-serif !important;
  font-size:10px !important; font-weight:700 !important;
  letter-spacing:0.32em !important; text-transform:uppercase !important;
  color:{BG} !important;
  background:var(--gold) !important;
  border:none !important; border-radius:2px !important;
  padding:17px 40px !important; width:100% !important;
  cursor:pointer !important;
  position:relative !important; overflow:hidden !important;
  transition:background 0.2s, transform 0.15s, box-shadow 0.25s !important;
  box-shadow:0 2px 20px rgba(212,168,67,0.22) !important;
}}
div.stButton > button::after {{
  content:'';
  position:absolute; top:0; left:-100%;
  width:60%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.22),transparent);
  animation:goldTraceSweep 3s 2s ease-in-out infinite;
}}
div.stButton > button:hover {{
  background:var(--gold-bright) !important;
  transform:translateY(-2px) !important;
  box-shadow:0 8px 32px rgba(212,168,67,0.45) !important;
}}
div.stButton > button:active {{ transform:translateY(1px) !important; }}

/* ── SECTION RULE ── */
.section-rule {{
  display:flex; align-items:center; gap:16px;
  margin:52px 0 28px;
  animation:fadeIn 0.8s ease both;
}}
.section-rule-text {{
  font-family:'Epilogue',sans-serif; font-size:8.5px; font-weight:700;
  letter-spacing:0.38em; text-transform:uppercase; color:var(--gold); white-space:nowrap;
}}
.section-rule-line {{ flex:1; height:1px; background:linear-gradient(90deg,{GOLD_DIM},transparent); }}
.section-rule-num {{
  font-family:'Playfair Display',serif; font-size:11px;
  font-weight:700; color:var(--gold-dim); letter-spacing:0.1em;
}}

/* ── HEADERS ── */
[data-testid="stMarkdownContainer"] h2, .stApp h2 {{
  font-family:'Playfair Display',serif !important;
  font-size:34px !important; font-weight:700 !important;
  color:var(--cream) !important; letter-spacing:-0.015em !important;
  margin-bottom:6px !important; animation:fadeUp 0.6s ease both;
}}
[data-testid="stMarkdownContainer"] h3 {{
  font-family:'Epilogue',sans-serif !important;
  font-size:8.5px !important; font-weight:700 !important;
  letter-spacing:0.32em !important; text-transform:uppercase !important;
  color:var(--gold-dim) !important; margin:24px 0 10px !important;
}}

/* ── JOB CARD ── */
.job-card {{
  position:relative;
  padding:34px 38px 30px; margin-bottom:6px;
  background:var(--card);
  border:1px solid var(--border);
  border-left:3px solid var(--gold);
  overflow:hidden;
  animation:cardReveal 0.5s ease both;
  transition:background 0.25s, box-shadow 0.3s, border-color 0.25s, transform 0.2s;
}}
.job-card::before {{
  content:''; position:absolute; inset:0;
  background:linear-gradient(120deg,transparent 0%,rgba(212,168,67,0.025) 50%,transparent 100%);
  opacity:0; transition:opacity 0.3s;
}}
.job-card:hover {{
  background:var(--bg3);
  border-color:rgba(212,168,67,0.42);
  box-shadow:6px 0 40px rgba(212,168,67,0.09);
  transform:translateX(2px);
}}
.job-card:hover::before {{ opacity:1; }}
.job-num {{
  position:absolute; top:16px; right:24px;
  font-family:'Playfair Display',serif;
  font-size:64px; font-weight:900;
  color:rgba(212,168,67,{0.055 if is_dark else 0.1});
  line-height:1; user-select:none; transition:color 0.3s;
}}
.job-card:hover .job-num {{ color:rgba(212,168,67,{0.12 if is_dark else 0.2}); }}
.job-card h3 {{
  font-family:'Playfair Display',serif !important;
  font-size:23px !important; font-weight:700 !important;
  color:var(--cream) !important; letter-spacing:-0.01em !important;
  margin-bottom:7px !important; text-transform:none !important;
}}
.job-agency {{
  font-size:10px; font-weight:600; letter-spacing:0.22em;
  text-transform:uppercase; color:var(--gold-dim);
}}

/* ── CIRCULAR SCORE METER ── */
.score-ring-wrap {{
  display:flex; flex-direction:column; align-items:center;
  gap:8px; padding:20px;
  background:var(--bg3);
  border:1px solid var(--border);
  border-top:2px solid var(--gold-dim);
  border-radius:2px;
  animation:metricPop 0.5s ease both;
  transition:border-color 0.25s, box-shadow 0.25s, transform 0.2s;
}}
.score-ring-wrap:hover {{
  border-color:rgba(212,168,67,0.4);
  box-shadow:0 4px 24px rgba(212,168,67,0.12);
  transform:translateY(-2px);
}}
.score-ring-label {{
  font-family:'Epilogue',sans-serif;
  font-size:8.5px; font-weight:700; letter-spacing:0.25em;
  text-transform:uppercase; color:var(--silver);
}}
.score-ring-svg {{ overflow:visible; }}
.score-ring-bg {{
  fill:none; stroke:rgba(212,168,67,0.1); stroke-width:6;
}}
.score-ring-arc {{
  fill:none;
  stroke:url(#goldGrad);
  stroke-width:6;
  stroke-linecap:round;
  stroke-dasharray:283;
  stroke-dashoffset:var(--dash-offset);
  transform:rotate(-90deg);
  transform-origin:50px 50px;
  animation:arcDraw 1.4s 0.3s cubic-bezier(0.4,0,0.2,1) both;
  filter:drop-shadow(0 0 6px rgba(212,168,67,0.5));
}}
.score-ring-value {{
  font-family:'Playfair Display',serif;
  font-size:22px; font-weight:700; fill:var(--gold);
  dominant-baseline:middle; text-anchor:middle;
}}
.score-ring-pct {{
  font-family:'Epilogue',sans-serif;
  font-size:9px; font-weight:600; fill:var(--gold-dim);
  dominant-baseline:middle; text-anchor:middle;
}}

/* Skill / count metric boxes */
.metric-box {{
  display:flex; flex-direction:column; align-items:center;
  justify-content:center; gap:6px; padding:20px 12px;
  background:var(--bg3);
  border:1px solid var(--border);
  border-top:2px solid var(--gold-dim);
  border-radius:2px;
  animation:metricPop 0.5s ease both;
  transition:border-color 0.25s, box-shadow 0.25s, transform 0.2s;
}}
.metric-box:hover {{
  border-color:rgba(212,168,67,0.4);
  box-shadow:0 4px 24px rgba(212,168,67,0.1);
  transform:translateY(-2px);
}}
.metric-box-label {{
  font-family:'Epilogue',sans-serif;
  font-size:8.5px; font-weight:700; letter-spacing:0.25em;
  text-transform:uppercase; color:var(--silver); text-align:center;
}}
.metric-box-value {{
  font-family:'Playfair Display',serif;
  font-size:38px; font-weight:700; color:var(--gold);
  letter-spacing:-0.02em; line-height:1;
}}

/* ── SKILL TAGS ── */
.skill-box {{
  display:inline-flex; align-items:center;
  padding:4px 14px; margin:3px;
  font-family:'Epilogue',sans-serif; font-size:10.5px;
  font-weight:500; letter-spacing:0.06em; border-radius:2px;
  transition:transform 0.15s, box-shadow 0.15s;
}}
.skill-box:hover {{ transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,0.25); }}
.matching {{
  background:rgba(62,201,138,0.07);
  border:1px solid rgba(62,201,138,0.25);
  color:var(--green);
}}
.missing {{
  background:rgba(224,82,82,0.07);
  border:1px solid rgba(224,82,82,0.22);
  color:var(--red);
}}

/* ── EXPANDER ── */
[data-testid="stExpander"] {{
  background:var(--bg3) !important; border:1px solid var(--border) !important;
  border-radius:2px !important; transition:border-color 0.2s !important;
}}
[data-testid="stExpander"]:hover {{ border-color:rgba(212,168,67,0.35) !important; }}
[data-testid="stExpander"] summary {{
  font-family:'Epilogue',sans-serif !important; font-size:9px !important;
  font-weight:700 !important; letter-spacing:0.25em !important;
  text-transform:uppercase !important; color:var(--gold-dim) !important;
  padding:16px 20px !important; transition:color 0.2s !important;
}}
[data-testid="stExpander"] summary:hover {{ color:var(--gold) !important; }}

/* ── DIVIDER ── */
hr {{
  border:none !important; height:1px !important;
  background:linear-gradient(90deg,transparent,{BORDER} 30%,{BORDER} 70%,transparent) !important;
  margin:40px 0 !important;
}}

/* ── CHECKBOX ── */
.stCheckbox label {{
  font-family:'Epilogue',sans-serif !important; font-size:10px !important;
  font-weight:600 !important; letter-spacing:0.18em !important;
  text-transform:uppercase !important; color:var(--silver) !important;
  transition:color 0.2s !important;
}}
.stCheckbox:hover label {{ color:var(--gold) !important; }}

/* ── ALERTS / SPINNER ── */
.stAlert {{
  border-radius:2px !important; border:1px solid var(--border) !important;
  background:var(--bg3) !important; font-family:'Epilogue',sans-serif !important;
}}
.stSpinner > div {{ border-top-color:var(--gold) !important; }}

[data-testid="stMarkdownContainer"] p {{
  font-family:'Epilogue',sans-serif; font-size:14px;
  font-weight:300; color:var(--silver); line-height:1.8;
}}

/* ── CONFETTI ── */
.confetti-piece {{
  position:fixed;
  top:-20px;
  width:8px; height:14px;
  border-radius:2px;
  opacity:0;
  z-index:99999;
  pointer-events:none;
  animation:confettiFall var(--fall-dur) var(--fall-delay) cubic-bezier(0.25,0.46,0.45,0.94) forwards;
}}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Confetti JS (fires once on trigger)
# --------------------------------------------------

CONFETTI_JS = """
<div id="confetti-container"></div>
<script>
(function() {
  var colors = ['#D4A843','#F5C842','#3EC98A','#E05252','#F0E6CC','#FFD700','#FFA500'];
  var container = document.getElementById('confetti-container');
  var count = 120;
  for (var i = 0; i < count; i++) {
    var el = document.createElement('div');
    el.classList.add('confetti-piece');
    var left  = Math.random() * 100;
    var color = colors[Math.floor(Math.random() * colors.length)];
    var dur   = (2.2 + Math.random() * 2.5).toFixed(2) + 's';
    var delay = (Math.random() * 1.2).toFixed(2) + 's';
    var rot   = Math.random() > 0.5 ? 'skewX(15deg)' : 'skewX(-15deg)';
    el.style.cssText = [
      'left:' + left + 'vw',
      'background:' + color,
      '--fall-dur:' + dur,
      '--fall-delay:' + delay,
      'transform:' + rot,
      'width:' + (6 + Math.random()*6) + 'px',
      'height:' + (10 + Math.random()*10) + 'px',
    ].join(';');
    container.appendChild(el);
  }
  // clean up after 5s
  setTimeout(function() {
    if (container && container.parentNode) container.parentNode.removeChild(container);
  }, 5500);
})();
</script>
"""

# --------------------------------------------------
# Helper: Circular Score Ring
# --------------------------------------------------

def score_ring(score_pct: float, label: str) -> str:
    """Return an SVG circular arc score meter as HTML."""
    radius = 45
    circumference = 2 * 3.14159 * radius  # ~282.7
    offset = circumference * (1 - score_pct / 100)
    return f"""
    <div class="score-ring-wrap">
      <div class="score-ring-label">{label}</div>
      <svg class="score-ring-svg" width="100" height="100" viewBox="0 0 100 100">
        <defs>
          <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%"   stop-color="#7A5E18"/>
            <stop offset="50%"  stop-color="#D4A843"/>
            <stop offset="100%" stop-color="#F5C842"/>
          </linearGradient>
        </defs>
        <circle class="score-ring-bg" cx="50" cy="50" r="{radius}"/>
        <circle class="score-ring-arc"
          cx="50" cy="50" r="{radius}"
          style="--dash-offset:{offset:.1f}"
        />
        <text class="score-ring-value" x="50" y="46">{score_pct:.0f}</text>
        <text class="score-ring-pct"   x="50" y="62">%</text>
      </svg>
    </div>
    """

# --------------------------------------------------
# Helper: Animated Progress Bar
# --------------------------------------------------

def progress_bar(label: str, pct: int, duration: str = "1.6s") -> str:
    return f"""
    <div class="apex-progress-wrap">
      <div class="apex-progress-label">
        <span>{label}</span><span>{pct}%</span>
      </div>
      <div class="apex-progress-track">
        <div class="apex-progress-fill" style="width:{pct}%; --dur:{duration};"></div>
      </div>
    </div>
    """

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=88)
    st.title("Apex Careers")

    # Theme toggle
    if st.button(f"{TOGGLE_ICON}  {TOGGLE_LABEL}"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

    st.markdown("""
### Features

✔ Job Recommendation System  
✔ Resume–Job Similarity Scoring  
✔ Skill Gap Analysis  
✔ AI Resume Summary Generator  
✔ AI Cover Letter Generator  
✔ AI Outreach Message Generator  

---
Built with:

• CrewAI  
• SentenceTransformers  
• Streamlit  
""")


# --------------------------------------------------
# Hero — Typewriter Headline
# --------------------------------------------------

st.markdown(f"""
<div class="hero">
  <div class="hero-beam"></div>
  <div class="hero-dot"></div>
  <div class="hero-dot"></div>
  <div class="hero-dot"></div>
  <div class="hero-dot"></div>
  <div class="hero-watermark">Apex</div>

  <div class="hero-eyebrow">
    <span class="hero-eyebrow-line"></span>
    AI-Powered Career Intelligence
  </div>

  <div class="hero-title-wrap">
    <span class="hero-title">Land the Role</span><br>
    <span class="hero-title-typed">You Deserve.</span><span class="hero-cursor"></span>
  </div>

  <p class="hero-sub">
    Precision job matching, instant skill gap diagnostics,
    and AI-authored applications — built for the modern professional.
  </p>

  <div class="hero-rule">
    <div class="hero-rule-line"></div>
    <span class="hero-rule-text">Powered by CrewAI</span>
    <div class="hero-rule-dots">
      <div class="hero-rule-dot"></div>
      <div class="hero-rule-dot"></div>
      <div class="hero-rule-dot"></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Profile Card
# --------------------------------------------------

st.markdown("""
<div class="profile-card">
  <div class="profile-header">
    <div class="profile-icon-ring">
      <span class="profile-icon">◈</span>
    </div>
    <div class="profile-title-block">
      <div class="profile-label">Section 01</div>
      <div class="profile-title">Your Profile</div>
    </div>
    <div class="profile-status">
      <div class="profile-status-dot"></div>
      Ready
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Inputs
# --------------------------------------------------

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    candidate_name = st.text_input("Your Name",    placeholder="Enter your full name")
    keyword        = st.text_input("Job Keyword",  value="data scientist")
    location       = st.text_input("Location",     value="remote")

with col2:
    bio         = st.text_input("Short Bio", value="I'm a data professional passionate about public service.")
    resume_text = st.text_area("Paste Your Resume", height=215)


# --------------------------------------------------
# Fetch Jobs — with animated progress bar
# --------------------------------------------------

if st.button("◈  Run Job Hunt Assistant"):

    # Step-by-step animated progress
    prog_slot = st.empty()

    steps = [
        ("Connecting to USAJobs API", 18, "0.4s"),
        ("Fetching job listings",     42, "0.7s"),
        ("Running similarity model",  68, "0.9s"),
        ("Scoring & ranking results", 88, "0.7s"),
        ("Complete",                 100, "0.5s"),
    ]

    for label, pct, dur in steps:
        prog_slot.markdown(progress_bar(label, pct, dur), unsafe_allow_html=True)
        time.sleep(0.55)

    prog_slot.empty()

    jobs = fetch_usajobs(keyword, location)

    if not jobs:
        st.error("No jobs found.")
    else:
        jobs = jobs[:5]

        job_descriptions = [
            job["MatchedObjectDescriptor"]["UserArea"]["Details"]["JobSummary"]
            for job in jobs
        ]

        scores = compute_similarity(resume_text, job_descriptions)

        st.session_state.jobs   = jobs
        st.session_state.scores = scores
        st.session_state.confetti_fired = False


# --------------------------------------------------
# Recommended Jobs
# --------------------------------------------------

if "jobs" in st.session_state:

    st.markdown("""
    <div class="section-rule">
      <span class="section-rule-text">Matched Positions</span>
      <span class="section-rule-line"></span>
      <span class="section-rule-num">02</span>
    </div>
    """, unsafe_allow_html=True)

    st.header("Recommended Jobs")

    selected_jobs = []

    for i, job in enumerate(st.session_state.jobs):

        descriptor = job["MatchedObjectDescriptor"]
        title      = descriptor["PositionTitle"]
        agency     = descriptor["OrganizationName"]
        summary    = descriptor["UserArea"]["Details"]["JobSummary"]
        score      = st.session_state.scores[i]
        score_pct  = score * 100

        st.markdown(f"""
        <div class="job-card">
          <span class="job-num">0{i+1}</span>
          <h3>{title}</h3>
          <p class="job-agency">{agency}</p>
        </div>
        """, unsafe_allow_html=True)

        # Skill gap
        matching, missing = skill_gap_analysis(resume_text, summary)

        # ── Circular score + count metrics ──
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(score_ring(score_pct, "Match Score"), unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-box-label">✦ Matching Skills</div>
              <div class="metric-box-value">{len(matching)}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-box-label">⚠ Skills to Gain</div>
              <div class="metric-box-value">{len(missing)}</div>
            </div>
            """, unsafe_allow_html=True)

        # Job Description
        with st.expander("View Full Job Description"):
            st.write(summary)

        # Matching
        st.markdown("### ✦ Matching Skills")
        if matching:
            for skill in matching:
                st.markdown(f'<span class="skill-box matching">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("No strong matching skills detected.")

        # Missing
        st.markdown("### ✦ Skills to Develop")
        if missing:
            for skill in missing:
                st.markdown(f'<span class="skill-box missing">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("No missing skills detected.")

        if st.checkbox("Select this position", key=i):
            selected_jobs.append(job)

        st.markdown("---")

    # ── Apply Button + Confetti ──
    if st.button("◈  Apply to Selected Jobs"):

        if selected_jobs:
            # Fire confetti
            st.markdown(CONFETTI_JS, unsafe_allow_html=True)
            st.session_state.confetti_fired = True

        for job in selected_jobs:

            descriptor = job["MatchedObjectDescriptor"]
            title      = descriptor["PositionTitle"]
            agency     = descriptor["OrganizationName"]
            summary    = descriptor["UserArea"]["Details"]["JobSummary"]

            st.header(title)

            with st.spinner("Running AI agents..."):
                result = run_pipeline(job, resume_text, bio, candidate_name)

            st.subheader("✨ AI Generated Output")
            st.write(result)
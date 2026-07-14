"""
Authentication helpers.
Uses native st.form for login (bypasses streamlit-authenticator rendering issues)
and bcrypt for password verification against credentials.yaml.
"""
import base64
from pathlib import Path

import bcrypt
import yaml
import streamlit as st
import streamlit_authenticator as stauth

_CREDS_FILE = Path(__file__).parent.parent / "credentials.yaml"
_LOGO_FILE  = Path(__file__).parent.parent / "static" / "logo-dark.svg"


def _logo_b64() -> str:
    return base64.b64encode(_LOGO_FILE.read_bytes()).decode()


def _load_creds() -> dict:
    with open(_CREDS_FILE) as f:
        return yaml.safe_load(f)


def _verify(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


# ── Branding panel HTML (no HTML comments — they break st.markdown) ─────────
def _branding_panel(logo: str) -> str:
    cards = "".join(
        f'<div class="sc"><div class="scv">{v}</div>'
        f'<div class="scl">{l}</div><div class="sct">{t}</div></div>'
        for v, l, t in [
            ("2,847", "Tests Automated",  "&#8593; +12% this week"),
            ("73.4%", "Coverage",          "&#8593; On Track"),
            ("8",     "Active Projects",   "&#8593; 2 ahead of plan"),
            ("98.2%", "Pass Rate",         "&#8593; Stable"),
        ]
    )
    return f"""
<div class="lp">
  <div class="orb orb1"></div><div class="orb orb2"></div>
  <div class="lp-logo">
    <img src="data:image/svg+xml;base64,{logo}" alt="Polaris"/>
  </div>
  <div class="lp-mid">
    <svg viewBox="0 0 320 220" fill="none" xmlns="http://www.w3.org/2000/svg"
         style="width:100%;max-width:300px;display:block;margin:0 auto 1.4rem;">
      <rect x="30" y="180" width="260" height="7" rx="3.5" fill="rgba(255,255,255,.12)"/>
      <rect x="50" y="40" width="220" height="140" rx="12"
            fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.22)" stroke-width="1.5"/>
      <rect x="50" y="40" width="220" height="22" rx="12" fill="rgba(255,255,255,.16)"/>
      <circle cx="66" cy="51" r="3.5" fill="rgba(255,255,255,.55)"/>
      <circle cx="79" cy="51" r="3.5" fill="rgba(255,255,255,.35)"/>
      <circle cx="92" cy="51" r="3.5" fill="rgba(255,255,255,.2)"/>
      <rect x="65" y="76" width="75" height="6" rx="3" fill="rgba(255,255,255,.1)"/>
      <rect x="65" y="76" width="58" height="6" rx="3" fill="#21D4C4"/>
      <rect x="65" y="90" width="75" height="6" rx="3" fill="rgba(255,255,255,.1)"/>
      <rect x="65" y="90" width="44" height="6" rx="3" fill="#4f8ef7"/>
      <rect x="65" y="104" width="75" height="6" rx="3" fill="rgba(255,255,255,.1)"/>
      <rect x="65" y="104" width="65" height="6" rx="3" fill="#21D4C4" opacity=".7"/>
      <rect x="65" y="118" width="75" height="6" rx="3" fill="rgba(255,255,255,.1)"/>
      <rect x="65" y="118" width="28" height="6" rx="3" fill="#ff6b6b" opacity=".75"/>
      <circle cx="210" cy="120" r="26" stroke="rgba(255,255,255,.1)" stroke-width="11"/>
      <circle cx="210" cy="120" r="26" stroke="#21D4C4" stroke-width="11"
              stroke-dasharray="82 82" stroke-dashoffset="20" transform="rotate(-90 210 120)"/>
      <circle cx="210" cy="120" r="26" stroke="#4f8ef7" stroke-width="11"
              stroke-dasharray="41 123" stroke-dashoffset="-62" transform="rotate(-90 210 120)" opacity=".8"/>
      <text x="210" y="124" text-anchor="middle" fill="#fff"
            font-size="10" font-weight="700" font-family="Inter,sans-serif">73%</text>
      <line x1="50" y1="180" x2="32" y2="180" stroke="rgba(33,212,196,.5)"
            stroke-width="1.5" stroke-dasharray="4 3"/>
      <line x1="270" y1="180" x2="288" y2="180" stroke="rgba(33,212,196,.5)"
            stroke-width="1.5" stroke-dasharray="4 3"/>
      <rect x="14" y="171" width="18" height="13" rx="3"
            fill="rgba(255,255,255,.13)" stroke="rgba(33,212,196,.5)" stroke-width="1"/>
      <rect x="288" y="171" width="18" height="13" rx="3"
            fill="rgba(255,255,255,.13)" stroke="rgba(33,212,196,.5)" stroke-width="1"/>
      <circle cx="23" cy="177" r="2.5" fill="#21D4C4"/>
      <circle cx="297" cy="177" r="2.5" fill="#21D4C4"/>
      <polyline points="65,155 84,150 103,153 122,146 141,149"
                stroke="#21D4C4" stroke-width="1.8" fill="none"
                stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="141" cy="149" r="2.5" fill="#21D4C4"/>
    </svg>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;padding:0 0.3rem;">
      {cards}
    </div>
  </div>
  <div class="lp-foot">Delivering Intelligent Test Automation</div>
</div>"""


def _inject_css(logo: str) -> None:
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

[data-testid="stSidebarNav"],[data-testid="stSidebarHeader"],
section[data-testid="stSidebar"],[data-testid="stHeader"],
[data-testid="stToolbar"],footer {{ display:none !important; }}

.stApp {{
    background: linear-gradient(135deg,#F7FAFF 0%,#EEF5FF 100%) !important;
    font-family: 'Inter',sans-serif !important;
}}
.main .block-container {{
    margin-left: 45% !important;
    width: 55% !important;
    max-width: none !important;
    padding: 0 2.5rem !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    box-sizing: border-box !important;
}}

/* ── Login card ── */
.login-card {{
    width: 100%;
    max-width: 430px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 8px 40px rgba(24,70,163,0.13);
    border: 1px solid #e2eaf8;
    overflow: hidden;
    animation: fadeUp 0.45s ease both;
}}
.login-card-head {{
    padding: 2.4rem 2.4rem 1.4rem;
    text-align: center;
    border-bottom: 1px solid #f0f4ff;
}}
.login-card-head h2 {{
    font-size: 1.6rem; font-weight: 700;
    color: #0b2668; margin: 0 0 0.35rem;
    letter-spacing: -0.4px;
}}
.login-card-head p {{
    font-size: 0.83rem; color: #64748b; margin: 0; line-height: 1.6;
}}
.login-card-body {{
    padding: 1.6rem 2.4rem 2rem;
}}
.login-card-foot {{
    padding: 0.9rem 2.4rem 1.2rem;
    text-align: center;
    border-top: 1px solid #f0f4ff;
    font-size: 0.72rem; color: #94a3b8;
}}

/* ── Streamlit inputs inside the card ── */
.login-card-body label {{
    font-size: 0.84rem !important; font-weight: 500 !important;
    color: #374151 !important;
}}
.login-card-body input {{
    height: 52px !important;
    border-radius: 10px !important;
    border: 1.5px solid #d1daf0 !important;
    background: #f7f9ff !important;
    font-size: 0.92rem !important;
    font-family: 'Inter',sans-serif !important;
    transition: border 0.18s, box-shadow 0.18s !important;
}}
.login-card-body input:focus {{
    border-color: #1846A3 !important;
    background: #fff !important;
    box-shadow: 0 0 0 4px rgba(24,70,163,0.1) !important;
}}
.login-card-body button[kind="primaryFormSubmit"],
.login-card-body button {{
    width: 100% !important; height: 52px !important;
    background: linear-gradient(90deg,#1846A3,#1e5bbf) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important;
    font-size: 0.97rem !important; font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 18px rgba(24,70,163,0.28) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    font-family: 'Inter',sans-serif !important;
}}
.login-card-body button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(24,70,163,0.36) !important;
}}
/* strip the stForm border */
.login-card-body [data-testid="stForm"] {{
    border: none !important; padding: 0 !important;
    background: transparent !important; box-shadow: none !important;
}}

@keyframes fadeUp {{
    from {{ opacity:0; transform:translateY(16px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}

/* ── Left branding panel ── */
.lp {{
    position:fixed; top:0; left:0; width:45%; height:100vh;
    background:linear-gradient(150deg,#0b2668 0%,#1846A3 50%,#1760c4 80%,#21D4C4 140%);
    display:flex; flex-direction:column; align-items:center;
    justify-content:space-between; padding:2.6rem 2rem 1.8rem;
    z-index:100; overflow:hidden;
}}
.lp::before {{
    content:''; position:absolute; inset:0;
    background-image:
      linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
      linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);
    background-size:36px 36px;
}}
.lp-logo {{ position:relative; z-index:2; align-self:flex-start; }}
.lp-logo img {{ height:30px; filter:brightness(0) invert(1); }}
.lp-mid  {{ position:relative; z-index:2; width:100%; }}
.lp-foot {{
    position:relative; z-index:2; font-size:0.72rem;
    letter-spacing:1px; text-transform:uppercase; color:rgba(255,255,255,.55);
}}
.orb {{ position:absolute; border-radius:50%; filter:blur(64px); opacity:.22; pointer-events:none; }}
.orb1 {{ width:240px;height:240px;background:#21D4C4;top:-80px;right:-60px; }}
.orb2 {{ width:200px;height:200px;background:#4f8ef7;bottom:40px;left:-70px; }}
.sc {{
    background:rgba(255,255,255,.12); backdrop-filter:blur(10px);
    border:1px solid rgba(255,255,255,.18); border-radius:12px;
    padding:0.85rem 1rem; color:#fff;
}}
.scv {{ font-size:1.4rem; font-weight:700; line-height:1; }}
.scl {{ font-size:0.7rem; opacity:.72; margin-top:3px; }}
.sct {{ font-size:0.68rem; color:#21D4C4; margin-top:5px; }}
</style>
{_branding_panel(logo)}
""", unsafe_allow_html=True)


def require_login() -> str:
    """
    Show branded login page if not authenticated.
    Uses native Streamlit form + bcrypt — no dependency on auth.login() rendering.
    """
    if st.session_state.get("authentication_status"):
        # Already authenticated — show logout in sidebar
        with st.sidebar:
            if st.button("Logout", use_container_width=True, key="logout_btn"):
                for k in ["authentication_status","username","name",
                          "_role","_username","_name"]:
                    st.session_state.pop(k, None)
                st.rerun()
        return st.session_state.get("_role", "user")

    # ── Render login page ──────────────────────────────────────────────────────
    logo = _logo_b64()
    _inject_css(logo)

    # Card wrapper — rendered in the block-container (right 55%)
    st.markdown(
        '<div class="login-card">'
        '<div class="login-card-head">'
        '<h2>Welcome to Polaris</h2>'
        '<p>Sign in to access the Automation Dashboard</p>'
        '</div>'
        '<div class="login-card-body">',
        unsafe_allow_html=True,
    )

    with st.form("polaris_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

    st.markdown(
        '</div>'
        '<div class="login-card-foot">Internal Use Only &nbsp;·&nbsp; Version 2.0</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if submitted:
        cfg   = _load_creds()
        users = cfg["credentials"]["usernames"]
        if username in users and _verify(password, users[username]["password"]):
            role = users[username].get("role", "user")
            st.session_state["authentication_status"] = True
            st.session_state["username"]  = username
            st.session_state["name"]      = users[username].get("name", username)
            st.session_state["_role"]     = role
            st.session_state["_username"] = username
            st.session_state["_name"]     = users[username].get("name", username)
            st.rerun()
        else:
            st.error("Incorrect username or password.")

    st.stop()


def is_admin() -> bool:
    return st.session_state.get("_role") == "admin"


def current_user() -> str:
    return st.session_state.get("_name", "")

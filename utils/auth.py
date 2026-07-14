"""
Authentication helpers using streamlit-authenticator.
"""
import base64
from pathlib import Path
import yaml
import streamlit as st
import streamlit_authenticator as stauth

_CREDS_FILE  = Path(__file__).parent.parent / "credentials.yaml"
_LOGO_FILE   = Path(__file__).parent.parent / "static" / "logo-dark.svg"


def _logo_b64() -> str:
    return base64.b64encode(_LOGO_FILE.read_bytes()).decode()


def _inject_login_css() -> None:
    """Inject split-screen enterprise login UI — CSS + left branding panel only."""
    logo = _logo_b64()

    # Build stat cards HTML without any comments (Streamlit markdown chokes on <!-- -->)
    stat_cards = (
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;padding:0 0.3rem;">'
        + ''.join(
            f'<div class="sc">'
            f'<div class="scv">{v}</div>'
            f'<div class="scl">{l}</div>'
            f'<div class="sct">{t}</div>'
            f'</div>'
            for v, l, t in [
                ("2,847", "Tests Automated",  "↑ +12% this week"),
                ("73.4%", "Coverage",          "↑ On Track"),
                ("8",     "Active Projects",   "↑ 2 ahead of plan"),
                ("98.2%", "Pass Rate",         "↑ Stable"),
            ]
        )
        + '</div>'
    )

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    [data-testid="stSidebarNav"],
    [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    footer {{ display:none !important; }}

    .stApp {{
        background:linear-gradient(135deg,#F7FAFF 0%,#EEF5FF 100%) !important;
        font-family:'Inter',sans-serif !important;
    }}

    /* Hide all Streamlit main content chrome — we position everything ourselves */
    .main .block-container {{
        padding: 0 !important;
        max-width: none !important;
    }}

    @keyframes fadeUp {{
        from {{ opacity:0; transform:translateY(20px); }}
        to   {{ opacity:1; transform:translateY(0); }}
    }}

    /* Right-panel background */
    .main {{
        background: linear-gradient(135deg,#F7FAFF 0%,#EEF5FF 100%) !important;
    }}

    /* Fix the form card in the centre of the right panel */
    div[data-testid="stForm"] {{
        position: fixed !important;
        top: 50% !important;
        left: 72.5% !important;
        transform: translate(-50%, -50%) !important;
        width: 430px !important;
        background: #ffffff !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 48px rgba(24,70,163,0.14) !important;
        padding: 2.6rem 2.4rem 2.2rem !important;
        border: 1px solid #e2eaf8 !important;
        z-index: 200 !important;
        animation: fadeUp 0.5s ease both !important;
    }}
    div[data-testid="stForm"] h1,
    div[data-testid="stForm"] h2,
    div[data-testid="stForm"] h3 {{ display:none !important; }}

    div[data-testid="stForm"] label {{
        font-size:0.84rem !important; font-weight:500 !important;
        color:#374151 !important; letter-spacing:0.15px !important;
    }}
    div[data-testid="stForm"] input {{
        height:52px !important;
        border-radius:10px !important;
        border:1.5px solid #d1daf0 !important;
        background:#f7f9ff !important;
        font-size:0.92rem !important;
        transition:border 0.18s, box-shadow 0.18s !important;
        font-family:'Inter',sans-serif !important;
    }}
    div[data-testid="stForm"] input:focus {{
        border-color:#1846A3 !important;
        background:#fff !important;
        box-shadow:0 0 0 4px rgba(24,70,163,0.1) !important;
    }}
    div[data-testid="stForm"] button {{
        width:100% !important; height:52px !important;
        background:linear-gradient(90deg,#1846A3 0%,#1e5bbf 100%) !important;
        color:#fff !important; border:none !important;
        border-radius:10px !important;
        font-size:0.97rem !important; font-weight:600 !important;
        letter-spacing:0.3px !important;
        box-shadow:0 4px 18px rgba(24,70,163,0.28) !important;
        transition:transform 0.15s, box-shadow 0.15s !important;
        margin-top:0.5rem !important;
        font-family:'Inter',sans-serif !important;
    }}
    div[data-testid="stForm"] button:hover {{
        transform:translateY(-2px) !important;
        box-shadow:0 8px 28px rgba(24,70,163,0.36) !important;
    }}

    /* Welcome heading — fixed above the form card */
    .rp-heading {{
        position: fixed !important;
        top: calc(50% - 220px) !important;
        left: 72.5% !important;
        transform: translateX(-50%) !important;
        width: 430px !important;
        text-align: center !important;
        z-index: 201 !important;
        animation: fadeUp 0.5s ease both !important;
    }}

    /* Footer — fixed bottom centre of right panel */
    .rp-footer {{
        position: fixed !important;
        bottom: 1.4rem !important;
        left: 72.5% !important;
        transform: translateX(-50%) !important;
        font-size: 0.72rem !important;
        color: #94a3b8 !important;
        font-family: Inter,sans-serif !important;
        z-index: 201 !important;
        white-space: nowrap !important;
    }}

    .lp {{
        position:fixed; top:0; left:0;
        width:45%; height:100vh;
        background:linear-gradient(150deg,#0b2668 0%,#1846A3 50%,#1760c4 80%,#21D4C4 140%);
        display:flex; flex-direction:column;
        align-items:center; justify-content:space-between;
        padding:2.6rem 2rem 1.8rem;
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
    .lp-mid {{ position:relative; z-index:2; width:100%; }}
    .lp-foot {{
        position:relative; z-index:2;
        font-size:0.72rem; letter-spacing:1px; text-transform:uppercase;
        color:rgba(255,255,255,.55);
    }}
    .orb {{ position:absolute; border-radius:50%; filter:blur(64px); opacity:.22; pointer-events:none; }}
    .orb1 {{ width:240px;height:240px;background:#21D4C4;top:-80px;right:-60px; }}
    .orb2 {{ width:200px;height:200px;background:#4f8ef7;bottom:40px;left:-70px; }}
    .sc {{
        background:rgba(255,255,255,.12);
        backdrop-filter:blur(10px);
        border:1px solid rgba(255,255,255,.18);
        border-radius:12px;
        padding:0.85rem 1rem;
        color:#fff;
    }}
    .scv {{ font-size:1.4rem; font-weight:700; line-height:1; }}
    .scl {{ font-size:0.7rem; opacity:.72; margin-top:3px; }}
    .sct {{ font-size:0.68rem; color:#21D4C4; margin-top:5px; }}
    </style>

    <div class="lp">
      <div class="orb orb1"></div>
      <div class="orb orb2"></div>
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
          <line x1="50" y1="180" x2="32" y2="180" stroke="rgba(33,212,196,.5)" stroke-width="1.5" stroke-dasharray="4 3"/>
          <line x1="270" y1="180" x2="288" y2="180" stroke="rgba(33,212,196,.5)" stroke-width="1.5" stroke-dasharray="4 3"/>
          <rect x="14" y="171" width="18" height="13" rx="3" fill="rgba(255,255,255,.13)" stroke="rgba(33,212,196,.5)" stroke-width="1"/>
          <rect x="288" y="171" width="18" height="13" rx="3" fill="rgba(255,255,255,.13)" stroke="rgba(33,212,196,.5)" stroke-width="1"/>
          <circle cx="23" cy="177" r="2.5" fill="#21D4C4"/>
          <circle cx="297" cy="177" r="2.5" fill="#21D4C4"/>
          <polyline points="65,155 84,150 103,153 122,146 141,149"
                    stroke="#21D4C4" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="141" cy="149" r="2.5" fill="#21D4C4"/>
        </svg>
        {stat_cards}
      </div>
      <div class="lp-foot">Delivering Intelligent Test Automation</div>
    </div>
    """, unsafe_allow_html=True)

    # Welcome heading + footer — fixed over the right panel
    st.markdown(
        '<div class="rp-heading">'
        '<div style="font-size:1.7rem;font-weight:700;color:#0b2668;'
        'letter-spacing:-0.5px;font-family:Inter,sans-serif;">Welcome to Polaris</div>'
        '<div style="font-size:0.84rem;color:#64748b;margin-top:0.45rem;'
        'font-family:Inter,sans-serif;line-height:1.6;">'
        'Sign in to access the Automation Dashboard</div>'
        '</div>'
        '<div class="rp-footer">Internal Use Only &nbsp;·&nbsp; Version 2.0</div>',
        unsafe_allow_html=True,
    )


def load_authenticator() -> stauth.Authenticate:
    with open(_CREDS_FILE) as f:
        cfg = yaml.safe_load(f)
    return stauth.Authenticate(
        cfg["credentials"],
        cfg["cookie"]["name"],
        cfg["cookie"]["key"],
        cfg["cookie"]["expiry_days"],
    )


def require_login() -> str:
    """
    Render branded login page if not authenticated.
    Returns the current user's role ('admin' or 'user') once logged in.
    Stops page execution if not authenticated.
    """
    auth = load_authenticator()

    auth_status = st.session_state.get("authentication_status")

    if not auth_status:
        _inject_login_css()
        auth.login(location="main")

        auth_status = st.session_state.get("authentication_status")
        if auth_status is False:
            st.error("Incorrect username or password. Please try again.")
        if not auth_status:
            st.stop()

    # Authenticated — render logout button in sidebar
    auth.logout("Logout", location="sidebar",
                key=f"logout_{st.session_state.get('username', '')}")

    username = st.session_state.get("username", "")
    name     = st.session_state.get("name", "")

    with open(_CREDS_FILE) as f:
        cfg = yaml.safe_load(f)
    role = cfg["credentials"]["usernames"].get(username, {}).get("role", "user")

    st.session_state["_role"]     = role
    st.session_state["_username"] = username
    st.session_state["_name"]     = name
    return role


def is_admin() -> bool:
    return st.session_state.get("_role") == "admin"


def current_user() -> str:
    return st.session_state.get("_name", "")

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
    """Inject split-screen enterprise login UI."""
    logo = _logo_b64()
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Reset & hide Streamlit chrome ── */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"] {{ display:none !important; }}
    [data-testid="stHeader"]         {{ display:none !important; }}
    [data-testid="stToolbar"]        {{ display:none !important; }}
    footer                           {{ display:none !important; }}
    .stApp {{ background:#F4F8FF !important; font-family:'Inter',sans-serif !important; }}

    /* ── Streamlit main block sits in right 55% ── */
    .main .block-container {{
        position: fixed !important;
        top: 0; right: 0;
        width: 55% !important;
        height: 100vh !important;
        max-width: none !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: linear-gradient(135deg,#F7FAFF,#EEF5FF) !important;
        overflow-y: auto !important;
    }}

    /* ── Form card ── */
    div[data-testid="stForm"] {{
        background: #ffffff !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 48px rgba(24,70,163,0.13) !important;
        padding: 2.8rem 2.6rem 2.4rem !important;
        width: 420px !important;
        border: 1px solid #e2eaf8 !important;
        animation: fadeUp 0.5s ease both !important;
    }}
    @keyframes fadeUp {{
        from {{ opacity:0; transform:translateY(18px); }}
        to   {{ opacity:1; transform:translateY(0); }}
    }}

    /* Hide the auto "Login" h-tag from stauth */
    div[data-testid="stForm"] h1,
    div[data-testid="stForm"] h2,
    div[data-testid="stForm"] h3 {{ display:none !important; }}

    /* Labels */
    div[data-testid="stForm"] label {{
        font-size:0.83rem !important;
        font-weight:500 !important;
        color:#374151 !important;
        letter-spacing:0.2px !important;
    }}
    /* Inputs */
    div[data-testid="stForm"] input {{
        height:52px !important;
        border-radius:10px !important;
        border:1.5px solid #d1daf0 !important;
        background:#f7f9ff !important;
        font-size:0.92rem !important;
        padding:0 1rem !important;
        transition:border 0.18s, box-shadow 0.18s !important;
        font-family:'Inter',sans-serif !important;
    }}
    div[data-testid="stForm"] input:focus {{
        border-color:#1846A3 !important;
        background:#fff !important;
        box-shadow:0 0 0 4px rgba(24,70,163,0.1) !important;
        outline:none !important;
    }}
    /* Submit / Login button */
    div[data-testid="stForm"] button {{
        width:100% !important;
        height:52px !important;
        background:linear-gradient(90deg,#1846A3,#1e5bbf) !important;
        color:#fff !important;
        border:none !important;
        border-radius:10px !important;
        font-size:0.97rem !important;
        font-weight:600 !important;
        letter-spacing:0.3px !important;
        cursor:pointer !important;
        box-shadow:0 4px 18px rgba(24,70,163,0.28) !important;
        transition:transform 0.15s, box-shadow 0.15s !important;
        margin-top:0.5rem !important;
    }}
    div[data-testid="stForm"] button:hover {{
        transform:translateY(-1px) !important;
        box-shadow:0 6px 24px rgba(24,70,163,0.38) !important;
    }}
    div[data-testid="stForm"] button:active {{
        transform:translateY(0) !important;
    }}

    /* ── Left branding panel — fixed ── */
    .lp {{
        position:fixed; top:0; left:0;
        width:45%; height:100vh;
        background:linear-gradient(145deg,#0d2d7a 0%,#1846A3 45%,#1a6abf 80%,#21D4C4 130%);
        display:flex; flex-direction:column;
        align-items:center; justify-content:space-between;
        padding:2.8rem 2.4rem 2rem;
        z-index:1000; overflow:hidden;
    }}
    /* subtle grid overlay */
    .lp::before {{
        content:'';
        position:absolute; inset:0;
        background-image:
          linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),
          linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);
        background-size:40px 40px;
    }}
    .lp-logo {{ position:relative; z-index:2; }}
    .lp-logo img {{ height:34px; filter:brightness(0) invert(1); }}
    .lp-center {{ position:relative; z-index:2; width:100%; }}
    .lp-tagline {{
        position:relative; z-index:2;
        text-align:center; color:rgba(255,255,255,0.65);
        font-size:0.78rem; letter-spacing:0.8px; text-transform:uppercase;
    }}

    /* Floating stat cards */
    .stat-card {{
        background:rgba(255,255,255,0.13);
        backdrop-filter:blur(12px);
        border:1px solid rgba(255,255,255,0.2);
        border-radius:14px;
        padding:0.9rem 1.2rem;
        color:#fff;
        box-shadow:0 4px 24px rgba(0,0,0,0.12);
    }}
    .stat-card .sc-val {{font-size:1.5rem;font-weight:700;line-height:1;}}
    .stat-card .sc-lbl {{font-size:0.72rem;opacity:0.75;margin-top:3px;}}
    .stat-card .sc-trend {{font-size:0.7rem;color:#21D4C4;margin-top:4px;}}

    /* Glowing orbs */
    .orb {{
        position:absolute; border-radius:50%;
        filter:blur(60px); opacity:0.25; pointer-events:none;
    }}
    .orb1 {{ width:220px;height:220px;background:#21D4C4;top:-60px;right:-40px; }}
    .orb2 {{ width:180px;height:180px;background:#4f8ef7;bottom:60px;left:-50px; }}
    </style>

    <!-- ════ LEFT BRANDING PANEL ════ -->
    <div class="lp">
      <div class="orb orb1"></div>
      <div class="orb orb2"></div>

      <!-- Logo -->
      <div class="lp-logo">
        <img src="data:image/svg+xml;base64,{logo}" alt="Polaris"/>
      </div>

      <!-- Centre illustration + cards -->
      <div class="lp-center">
        <!-- SVG illustration -->
        <svg viewBox="0 0 340 260" fill="none" xmlns="http://www.w3.org/2000/svg"
             style="width:100%;max-width:320px;display:block;margin:0 auto 1.6rem;">
          <!-- Base platform -->
          <rect x="30" y="190" width="280" height="8" rx="4" fill="rgba(255,255,255,.15)"/>
          <!-- Screen / dashboard frame -->
          <rect x="60" y="60" width="220" height="130" rx="12" fill="rgba(255,255,255,.1)" stroke="rgba(255,255,255,.25)" stroke-width="1.5"/>
          <!-- Screen header bar -->
          <rect x="60" y="60" width="220" height="22" rx="12" fill="rgba(255,255,255,.18)"/>
          <circle cx="77" cy="71" r="4" fill="rgba(255,255,255,.5)"/>
          <circle cx="91" cy="71" r="4" fill="rgba(255,255,255,.35)"/>
          <circle cx="105" cy="71" r="4" fill="rgba(255,255,255,.2)"/>
          <!-- Progress bars inside screen -->
          <rect x="75" y="96" width="80" height="7" rx="3.5" fill="rgba(255,255,255,.12)"/>
          <rect x="75" y="96" width="62" height="7" rx="3.5" fill="#21D4C4"/>
          <rect x="75" y="112" width="80" height="7" rx="3.5" fill="rgba(255,255,255,.12)"/>
          <rect x="75" y="112" width="48" height="7" rx="3.5" fill="#4f8ef7"/>
          <rect x="75" y="128" width="80" height="7" rx="3.5" fill="rgba(255,255,255,.12)"/>
          <rect x="75" y="128" width="70" height="7" rx="3.5" fill="#21D4C4" opacity=".7"/>
          <rect x="75" y="144" width="80" height="7" rx="3.5" fill="rgba(255,255,255,.12)"/>
          <rect x="75" y="144" width="30" height="7" rx="3.5" fill="#ff6b6b" opacity=".8"/>
          <!-- Mini donut chart -->
          <circle cx="225" cy="140" r="28" stroke="rgba(255,255,255,.12)" stroke-width="12"/>
          <circle cx="225" cy="140" r="28" stroke="#21D4C4" stroke-width="12"
                  stroke-dasharray="88 88" stroke-dashoffset="22" transform="rotate(-90 225 140)"/>
          <circle cx="225" cy="140" r="28" stroke="#4f8ef7" stroke-width="12"
                  stroke-dasharray="44 132" stroke-dashoffset="-66" transform="rotate(-90 225 140)" opacity=".8"/>
          <text x="225" y="144" text-anchor="middle" fill="#fff" font-size="11" font-weight="700" font-family="Inter,sans-serif">73%</text>
          <!-- Connector lines to devices -->
          <line x1="60" y1="190" x2="40" y2="190" stroke="rgba(33,212,196,.4)" stroke-width="1.5" stroke-dasharray="4 3"/>
          <line x1="280" y1="190" x2="300" y2="190" stroke="rgba(33,212,196,.4)" stroke-width="1.5" stroke-dasharray="4 3"/>
          <!-- Device boxes -->
          <rect x="18" y="180" width="22" height="16" rx="3" fill="rgba(255,255,255,.15)" stroke="rgba(33,212,196,.5)" stroke-width="1"/>
          <rect x="300" y="180" width="22" height="16" rx="3" fill="rgba(255,255,255,.15)" stroke="rgba(33,212,196,.5)" stroke-width="1"/>
          <!-- Pulse dots -->
          <circle cx="29" cy="188" r="3" fill="#21D4C4" opacity=".9"/>
          <circle cx="311" cy="188" r="3" fill="#21D4C4" opacity=".9"/>
          <!-- Small line chart -->
          <polyline points="75,170 95,165 115,168 135,160 155,163"
                    stroke="#21D4C4" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="155" cy="163" r="3" fill="#21D4C4"/>
        </svg>

        <!-- Stat cards grid -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;padding:0 0.5rem;">
          <div class="stat-card">
            <div class="sc-val">2,847</div>
            <div class="sc-lbl">Tests Automated</div>
            <div class="sc-trend">↑ +12% this week</div>
          </div>
          <div class="stat-card">
            <div class="sc-val">73.4%</div>
            <div class="sc-lbl">Coverage</div>
            <div class="sc-trend">↑ On Track</div>
          </div>
          <div class="stat-card">
            <div class="sc-val">8</div>
            <div class="sc-lbl">Active Projects</div>
            <div class="sc-trend">↑ 2 ahead of plan</div>
          </div>
          <div class="stat-card">
            <div class="sc-val">98.2%</div>
            <div class="sc-lbl">Pass Rate</div>
            <div class="sc-trend">↑ Stable</div>
          </div>
        </div>
      </div>

      <!-- Tagline -->
      <div class="lp-tagline">Delivering Intelligent Test Automation</div>
    </div>

    <!-- ════ RIGHT — card header injected before the Streamlit form ════ -->
    <div style="width:420px;animation:fadeUp 0.5s ease both;">
      <div style="text-align:center;margin-bottom:1.8rem;">
        <div style="font-size:1.65rem;font-weight:700;color:#0d2d7a;letter-spacing:-0.5px;font-family:Inter,sans-serif;">
          Welcome to Polaris
        </div>
        <div style="font-size:0.85rem;color:#64748b;margin-top:0.4rem;font-family:Inter,sans-serif;">
          Sign in to access the Automation Dashboard
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


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
            st.markdown(
                '<div style="text-align:center;font-size:0.72rem;color:#94a3b8;'
                'margin-top:1rem;font-family:Inter,sans-serif;">'
                'Internal Use Only &nbsp;·&nbsp; Version 2.0</div>',
                unsafe_allow_html=True,
            )
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

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
    """Inject full-page CSS for the login screen."""
    logo = _logo_b64()
    st.markdown(f"""
    <style>
    /* ── Hide sidebar on login ── */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"] {{ display: none !important; }}

    /* ── Full-page gradient background ── */
    .stApp {{
        background: linear-gradient(160deg, #dce8fb 0%, #eef3ff 50%, #d8e8f7 100%) !important;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
        box-shadow: none !important;
    }}

    /* ── Main block: wide card layout ── */
    .main .block-container {{
        max-width: 860px !important;
        margin: 0 auto !important;
        padding: 8vh 2rem 2rem !important;
    }}

    /* ── Card top: logo + title + description ── */
    .login-card-top {{
        background: #ffffff;
        border: 1px solid #dde6f5;
        border-bottom: none;
        border-radius: 16px 16px 0 0;
        padding: 3rem 3rem 2rem;
        box-shadow: 0 4px 32px rgba(10,54,144,0.09);
    }}
    .login-logo {{
        display: block;
        margin: 0 auto 1.3rem;
        height: 38px;
    }}
    .login-title {{
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #0A3690;
        margin: 0 0 0.4rem;
        letter-spacing: -0.3px;
    }}
    .login-sub {{
        text-align: center;
        font-size: 0.82rem;
        color: #64748b;
        margin: 0;
        line-height: 1.7;
    }}

    /* ── Form: bottom half of same card ── */
    div[data-testid="stForm"] {{
        background: #ffffff !important;
        border: 1px solid #dde6f5 !important;
        border-top: none !important;
        border-radius: 0 0 16px 16px !important;
        box-shadow: 0 4px 32px rgba(10,54,144,0.09) !important;
        padding: 2rem 3rem 2.5rem !important;
        margin-top: 0 !important;
    }}
    /* Hide auto-generated "Login" heading */
    div[data-testid="stForm"] h1,
    div[data-testid="stForm"] h2,
    div[data-testid="stForm"] h3 {{ display: none !important; }}

    /* Labels */
    div[data-testid="stForm"] label {{
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }}
    /* Inputs */
    div[data-testid="stForm"] input[type="text"],
    div[data-testid="stForm"] input[type="password"] {{
        border-radius: 8px !important;
        border: 1.5px solid #d1daf0 !important;
        background: #f5f8ff !important;
        font-size: 0.9rem !important;
        padding: 0.55rem 0.8rem !important;
        transition: border 0.15s !important;
    }}
    div[data-testid="stForm"] input:focus {{
        border-color: #0A3690 !important;
        background: #fff !important;
        box-shadow: 0 0 0 3px rgba(10,54,144,0.08) !important;
    }}
    /* Login button — small, left-aligned, Polaris blue */
    div[data-testid="stForm"] button {{
        background: #0A3690 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.48rem 1.6rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        width: auto !important;
        cursor: pointer !important;
        transition: background 0.15s !important;
    }}
    div[data-testid="stForm"] button:hover {{
        background: #0c44b0 !important;
    }}

    /* ── Footer below card ── */
    .login-footer {{
        text-align: center;
        font-size: 0.73rem;
        color: #94a3b8;
        margin-top: 1.4rem;
        letter-spacing: 0.2px;
    }}
    </style>

    <div class="login-card-top">
      <img class="login-logo"
           src="data:image/svg+xml;base64,{logo}"
           alt="Polaris Grids" />
      <div class="login-title">Automation Dashboard</div>
      <div class="login-sub">
        Real-time test automation tracker for Meter Firmware, HES, VEE, WFM and allied Polaris projects.
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
            st.markdown('<div class="login-footer">Polaris Grids · Internal Use Only</div>',
                        unsafe_allow_html=True)
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

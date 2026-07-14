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
    .stApp {{ background: linear-gradient(135deg,#dce8fb 0%,#eef4ff 55%,#ddf0f8 100%) !important; }}
    [data-testid="stHeader"] {{ background: transparent !important; box-shadow: none !important; }}

    /* ── Centre & constrain main block ── */
    .main .block-container {{
        max-width: 460px !important;
        margin: 0 auto !important;
        padding-top: 6vh !important;
        padding-bottom: 2rem !important;
    }}

    /* ── Card: wraps the HTML header + the Streamlit form ── */
    .login-card-top {{
        background: #fff;
        border: 1px solid #dbe4f5;
        border-bottom: none;
        border-radius: 20px 20px 0 0;
        padding: 2.6rem 2.4rem 1.8rem;
        box-shadow: 0 8px 40px rgba(10,54,144,0.11);
    }}
    .login-logo {{
        display:block; margin:0 auto 1.2rem; height:40px;
    }}
    .login-title {{
        text-align:center; font-size:1.45rem; font-weight:700;
        color:#0A3690; margin:0 0 0.3rem; letter-spacing:-0.3px;
    }}
    .login-sub {{
        text-align:center; font-size:0.8rem; color:#64748b;
        margin:0 0 1.5rem; line-height:1.65;
    }}
    .login-divider {{
        border:none; border-top:1px solid #e4ecfa; margin:0;
    }}

    /* ── Form bottom half of card ── */
    div[data-testid="stForm"] {{
        background: #fff !important;
        border: 1px solid #dbe4f5 !important;
        border-top: none !important;
        border-radius: 0 0 20px 20px !important;
        box-shadow: 0 8px 40px rgba(10,54,144,0.11) !important;
        padding: 1.6rem 2.4rem 2rem !important;
    }}
    /* Hide the default "Login" heading inside the form */
    div[data-testid="stForm"] h1,
    div[data-testid="stForm"] h2,
    div[data-testid="stForm"] h3 {{ display: none !important; }}

    /* Input fields */
    div[data-testid="stForm"] input {{
        border-radius: 8px !important;
        border: 1.5px solid #dbe4f5 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 0.75rem !important;
    }}
    div[data-testid="stForm"] input:focus {{
        border-color: #0A3690 !important;
        box-shadow: 0 0 0 3px rgba(10,54,144,0.1) !important;
    }}
    /* Submit button — full width Polaris blue */
    div[data-testid="stForm"] button {{
        background: #0A3690 !important;
        color: #fff !important;
        border-radius: 8px !important;
        width: 100% !important;
        padding: 0.55rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        margin-top: 0.4rem !important;
        transition: background 0.15s !important;
    }}
    div[data-testid="stForm"] button:hover {{
        background: #0c44b0 !important;
    }}

    /* Footer note */
    .login-footer {{
        text-align:center; font-size:0.72rem; color:#94a3b8; margin-top:1.2rem;
    }}
    </style>

    <div class="login-card-top">
      <img class="login-logo"
           src="data:image/svg+xml;base64,{logo}"
           alt="Polaris Grids"/>
      <div class="login-title">Automation Dashboard</div>
      <div class="login-sub">
        Real-time test automation tracker for Meter Firmware,<br>
        HES, VEE, WFM and allied Polaris projects.
      </div>
      <hr class="login-divider"/>
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

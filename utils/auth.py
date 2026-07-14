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


def _inject_login_ui() -> None:
    """Inject CSS + branded header above the login form."""
    logo = _logo_b64()
    st.markdown(f"""
    <style>
    /* Hide sidebar nav links on login screen */
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    [data-testid="stSidebarHeader"] {{ display: none !important; }}
    section[data-testid="stSidebar"] {{ display: none !important; }}

    /* Full-page centred layout */
    .login-wrap {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 1rem 1rem;
    }}
    .login-card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        box-shadow: 0 4px 32px rgba(10,54,144,0.08);
        padding: 2.5rem 2.5rem 2rem;
        max-width: 420px;
        width: 100%;
    }}
    .login-logo {{
        display: block;
        margin: 0 auto 1.2rem;
        height: 36px;
    }}
    .login-title {{
        text-align: center;
        font-size: 1.45rem;
        font-weight: 700;
        color: #0A3690;
        margin: 0 0 0.3rem;
        letter-spacing: -0.3px;
    }}
    .login-sub {{
        text-align: center;
        font-size: 0.82rem;
        color: #64748b;
        margin: 0 0 1.6rem;
        line-height: 1.5;
    }}
    .login-divider {{
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 1.4rem 0 1.2rem;
    }}
    .login-footer {{
        text-align: center;
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 1.5rem;
    }}

    /* Style the stAuth form to sit inside card area */
    div[data-testid="stForm"] {{
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }}
    div[data-testid="stForm"] > div {{
        padding: 0 !important;
    }}
    </style>

    <div class="login-wrap">
      <div class="login-card">
        <img class="login-logo"
             src="data:image/svg+xml;base64,{logo}"
             alt="Polaris Grids" />
        <div class="login-title">Automation Dashboard</div>
        <div class="login-sub">
          Real-time test automation portfolio tracker for<br>
          Meter Firmware, HES, VEE and allied projects.<br>
          <strong style="color:#0A3690;">Sign in to continue.</strong>
        </div>
        <hr class="login-divider"/>
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
        # Inject branding above the login form
        _inject_login_ui()

        # Render the auth form in a narrow centred column
        _, col, _ = st.columns([1, 1.6, 1])
        with col:
            auth.login(location="main")

        auth_status = st.session_state.get("authentication_status")
        if auth_status is False:
            _, col, _ = st.columns([1, 1.6, 1])
            with col:
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

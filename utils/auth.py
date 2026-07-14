"""
Authentication helpers using streamlit-authenticator.
"""
from pathlib import Path
import yaml
import streamlit as st
import streamlit_authenticator as stauth

_CREDS_FILE = Path(__file__).parent.parent / "credentials.yaml"


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
    Render login form if not authenticated.
    Returns the current user's role ('admin' or 'user') once logged in.
    Stops page execution if not authenticated.
    """
    auth = load_authenticator()

    # v0.4+: login() returns None; results land in st.session_state
    auth.login(location="main")

    auth_status = st.session_state.get("authentication_status")
    username    = st.session_state.get("username", "")
    name        = st.session_state.get("name", "")

    if auth_status is False:
        st.error("Incorrect username or password.")
        st.stop()
    if not auth_status:
        st.stop()

    # Logout button in sidebar
    auth.logout("Logout", location="sidebar")

    # Read role from credentials file
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

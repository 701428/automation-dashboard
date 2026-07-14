"""
Authentication helpers.
Native st.form + bcrypt — no dependency on streamlit-authenticator rendering.
"""
import base64
from pathlib import Path

import bcrypt
import yaml
import streamlit as st

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


# ── SVG icons (data-URI) for input backgrounds ───────────────────────────────
_ICON_USER = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' "
    "viewBox='0 0 24 24' fill='none' stroke='%2394A3B8' stroke-width='1.8' "
    "stroke-linecap='round' stroke-linejoin='round'%3E"
    "%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E"
    "%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E"
)
_ICON_LOCK = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' "
    "viewBox='0 0 24 24' fill='none' stroke='%2394A3B8' stroke-width='1.8' "
    "stroke-linecap='round' stroke-linejoin='round'%3E"
    "%3Crect x='3' y='11' width='18' height='11' rx='2' ry='2'/%3E"
    "%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E"
)


def _branding_panel(logo: str) -> str:
    stat_items = [
        ("rocket",  "2,847", "Tests Automated", "↑ 12% this week"),
        ("chart",   "73.4%", "Coverage",         "↑ On Track"),
        ("layers",  "8",     "Active Projects",  "↑ 2 ahead of plan"),
        ("shield",  "98.2%", "Pass Rate",        "↑ Stable"),
    ]
    icon_paths = {
        "rocket": "%3Cpath d='M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z'/%3E%3Cpath d='M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z'/%3E",
        "chart":  "%3Cpath d='M21.21 15.89A10 10 0 1 1 8 2.83'/%3E%3Cpath d='M22 12A10 10 0 0 0 12 2v10z'/%3E",
        "layers": "%3Cpolygon points='12 2 2 7 12 12 22 7 12 2'/%3E%3Cpolyline points='2 17 12 22 22 17'/%3E%3Cpolyline points='2 12 12 17 22 12'/%3E",
        "shield": "%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E",
    }

    cards_html = ""
    for icon_key, val, label, trend in stat_items:
        icon_src = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%2321D4C4' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E{icon_paths[icon_key]}%3C/svg%3E"
        cards_html += (
            f'<div class="sc">'
            f'<div class="sc-icon"><img src="{icon_src}" width="20" height="20"/></div>'
            f'<div><div class="scv">{val}</div>'
            f'<div class="scl">{label}</div>'
            f'<div class="sct">{trend}</div></div>'
            f'</div>'
        )

    dots = "".join(
        f'<div class="dot" style="width:{w}px;height:{w}px;top:{t}%;left:{l}%;opacity:{op};animation-delay:{d}s"></div>'
        for w, t, l, op, d in [
            (4,15,70,.4,0),(3,30,85,.3,1.2),(5,55,75,.25,.6),
            (3,75,82,.35,2),(4,20,60,.3,.8),(6,65,88,.2,1.5),
        ]
    )

    return f"""
<div class="lp">
  <div class="orb orb1"></div><div class="orb orb2"></div>
  {dots}
  <div class="lp-logo"><img src="data:image/svg+xml;base64,{logo}" alt="Polaris"/></div>
  <div class="lp-mid">
    <svg viewBox="0 0 360 230" fill="none" xmlns="http://www.w3.org/2000/svg"
         style="width:100%;max-width:340px;display:block;margin:0 auto 1.6rem;">
      <defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/></filter></defs>
      <rect x="40" y="30" width="280" height="165" rx="14"
            fill="rgba(255,255,255,.07)" stroke="rgba(255,255,255,.2)" stroke-width="1.5"/>
      <rect x="40" y="30" width="280" height="26" rx="14" fill="rgba(255,255,255,.14)"/>
      <circle cx="58"  cy="43" r="4" fill="rgba(255,255,255,.55)"/>
      <circle cx="72"  cy="43" r="4" fill="rgba(255,255,255,.35)"/>
      <circle cx="86"  cy="43" r="4" fill="rgba(255,255,255,.2)"/>
      <rect x="56" y="70"  width="90" height="7" rx="3.5" fill="rgba(255,255,255,.1)"/>
      <rect x="56" y="70"  width="72" height="7" rx="3.5" fill="#21D4C4" filter="url(#glow)"/>
      <rect x="56" y="85"  width="90" height="7" rx="3.5" fill="rgba(255,255,255,.1)"/>
      <rect x="56" y="85"  width="55" height="7" rx="3.5" fill="#4f8ef7"/>
      <rect x="56" y="100" width="90" height="7" rx="3.5" fill="rgba(255,255,255,.1)"/>
      <rect x="56" y="100" width="78" height="7" rx="3.5" fill="#21D4C4" opacity=".65"/>
      <rect x="56" y="115" width="90" height="7" rx="3.5" fill="rgba(255,255,255,.1)"/>
      <rect x="56" y="115" width="34" height="7" rx="3.5" fill="#ff6b6b" opacity=".8"/>
      <circle cx="255" cy="115" r="38" stroke="rgba(255,255,255,.08)" stroke-width="14"/>
      <circle cx="255" cy="115" r="38" stroke="#21D4C4" stroke-width="14"
              stroke-dasharray="100 140" stroke-dashoffset="20" transform="rotate(-90 255 115)"
              filter="url(#glow)"/>
      <circle cx="255" cy="115" r="38" stroke="#4f8ef7" stroke-width="14"
              stroke-dasharray="50 190" stroke-dashoffset="-80" transform="rotate(-90 255 115)" opacity=".75"/>
      <text x="255" y="120" text-anchor="middle" fill="#fff"
            font-size="13" font-weight="700" font-family="Inter,sans-serif">73%</text>
      <polyline points="56,165 80,158 104,163 128,154 152,159 176,150"
                stroke="#21D4C4" stroke-width="2" fill="none"
                stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
      <circle cx="176" cy="150" r="3.5" fill="#21D4C4"/>
    </svg>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.7rem;padding:0 0.2rem;">
      {cards_html}
    </div>
  </div>
  <div class="lp-foot">Delivering Intelligent Test Automation</div>
</div>"""


def _inject_css(logo: str) -> None:
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

[data-testid="stSidebarNav"],[data-testid="stSidebarHeader"],
section[data-testid="stSidebar"],[data-testid="stHeader"],
[data-testid="stToolbar"],footer {{ display:none !important; }}

.stApp, body {{
    background: #E8EEF8 !important;
    font-family: 'Inter', sans-serif !important;
}}

/* ── Left branding panel ── */
.lp {{
    position:fixed; top:0; left:0; width:44%; height:100vh;
    background:linear-gradient(145deg,#061E5B 0%,#0D2E8F 35%,#1846A3 65%,#1368C8 85%,#1A8FD8 100%);
    display:flex; flex-direction:column; align-items:center;
    justify-content:space-between; padding:2.4rem 1.8rem 2rem;
    z-index:100; overflow:hidden;
}}
.lp::before {{
    content:''; position:absolute; inset:0;
    background-image:
      linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),
      linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);
    background-size:32px 32px;
}}
.lp::after {{
    content:''; position:absolute;
    width:500px; height:500px;
    border:1px solid rgba(33,212,196,.12); border-radius:50%;
    top:-120px; right:-180px;
    box-shadow:0 0 60px rgba(33,212,196,.08) inset;
}}
.lp-logo {{ position:relative; z-index:2; align-self:flex-start; }}
.lp-logo img {{ height:28px; filter:brightness(0) invert(1); }}
.lp-mid  {{ position:relative; z-index:2; width:100%; }}
.lp-foot {{
    position:relative; z-index:2; font-size:0.7rem;
    letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.45);
}}
.orb {{ position:absolute; border-radius:50%; filter:blur(70px); opacity:.18; pointer-events:none; }}
.orb1 {{ width:260px;height:260px;background:#21D4C4;top:-90px;right:-70px; }}
.orb2 {{ width:220px;height:220px;background:#4f8ef7;bottom:30px;left:-80px; }}
.dot {{
    position:absolute; border-radius:50%; background:#21D4C4; pointer-events:none;
    animation:pulse 3s ease-in-out infinite alternate;
}}
@keyframes pulse {{
    from {{ transform:scale(1); opacity:.3; }}
    to   {{ transform:scale(1.6); opacity:.7; }}
}}
.sc {{
    background:rgba(255,255,255,.1); backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,.15); border-radius:14px;
    padding:.9rem 1rem; color:#fff;
    display:flex; align-items:flex-start; gap:12px;
    transition:transform .2s,background .2s;
}}
.sc:hover {{ background:rgba(255,255,255,.15); transform:translateY(-2px); }}
.sc-icon {{
    width:40px; height:40px; border-radius:10px;
    background:rgba(33,212,196,.2); border:1px solid rgba(33,212,196,.3);
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
}}
.scv {{ font-size:1.35rem; font-weight:700; line-height:1; }}
.scl {{ font-size:.68rem; opacity:.75; margin-top:3px; }}
.sct {{ font-size:.68rem; color:#21D4C4; margin-top:5px; font-weight:500; }}

/* ── Right panel background ── */
.login-wrapper {{
    position:fixed; left:44%; top:0; width:56%; height:100vh;
    background:radial-gradient(ellipse at 80% 20%,#D8E8FF 0%,#EBF2FF 40%,#E4EEF8 100%);
    z-index:50;
}}
.login-wrapper::after {{
    content:''; position:absolute;
    width:400px; height:400px;
    border:1px solid rgba(24,70,163,.08); border-radius:50%;
    bottom:-80px; right:-80px;
}}

/* ── Login card = stForm ── */
div[data-testid="stForm"] {{
    position:fixed !important;
    left:calc(72vw - 230px) !important;
    top:50% !important;
    transform:translateY(-50%) !important;
    width:460px !important;
    max-width:calc(56vw - 60px) !important;
    height:auto !important;
    min-height:0 !important;
    background:#ffffff !important;
    border-radius:24px !important;
    padding:44px 48px 40px !important;
    border:1px solid rgba(220,230,245,.9) !important;
    box-shadow:0 4px 6px rgba(15,23,42,.04),0 20px 60px rgba(15,23,42,.10),0 0 0 1px rgba(255,255,255,.6) inset !important;
    z-index:200 !important;
    box-sizing:border-box !important;
    overflow-y:auto !important;
    max-height:96vh !important;
    animation:cardIn .5s cubic-bezier(.22,.68,0,1.15) both !important;
}}
div[data-testid="stForm"] > div {{ height:auto !important; min-height:0 !important; }}

@keyframes cardIn {{
    from {{ opacity:0; transform:translateY(calc(-50% + 28px)); }}
    to   {{ opacity:1; transform:translateY(-50%); }}
}}

/* Card header */
.lc-head {{ text-align:center; margin-bottom:28px; }}
.lc-logo-img {{ height:36px; display:block; margin:0 auto 20px; }}
.lc-head h1 {{
    font-size:2rem; font-weight:800; color:#0F172A;
    margin:0 0 6px; letter-spacing:-.6px; font-family:'Inter',sans-serif; line-height:1.15;
}}
.lc-app-sub {{
    font-size:.95rem; font-weight:600; color:#1846A3;
    margin:0 0 10px; font-family:'Inter',sans-serif;
}}
.lc-head p {{
    font-size:.88rem; font-weight:400; color:#64748B;
    margin:0; font-family:'Inter',sans-serif;
}}

/* ── Hide "Press Enter to submit form" — all known Streamlit selectors ── */
[data-testid="InputInstructions"],
[data-baseweb="input"] ~ small,
[data-baseweb="input"] + div small,
div[data-testid="stForm"] small,
div[data-testid="stForm"] [data-testid="stTextInput"] small,
div[data-testid="stForm"] [data-testid="stTextInput"] > small,
div[data-testid="stForm"] [data-testid="stTextInput"] div small,
.st-emotion-cache-ue6h4q,
.st-emotion-cache-1bt9eao {{
    display:none !important;
    visibility:hidden !important;
    height:0 !important;
    overflow:hidden !important;
    margin:0 !important;
    padding:0 !important;
}}

/* ── Labels ── */
div[data-testid="stForm"] label {{
    font-size:.84rem !important; font-weight:600 !important;
    color:#1E293B !important; font-family:'Inter',sans-serif !important;
    letter-spacing:.1px !important; margin-bottom:6px !important;
    display:block !important; width:100% !important;
}}

/* ── Input field wrapper: full width, no overflow ── */
div[data-testid="stForm"] [data-testid="stTextInput"] {{
    width:100% !important;
}}
div[data-testid="stForm"] [data-testid="stTextInput"] > div {{
    width:100% !important;
    position:relative !important;
    display:flex !important;
    align-items:center !important;
    border-radius:14px !important;
    border:1px solid #D6E0F5 !important;
    background:#F8FAFF !important;
    box-sizing:border-box !important;
    transition:border-color .2s,box-shadow .2s !important;
    overflow:hidden !important;
}}
div[data-testid="stForm"] [data-testid="stTextInput"]:focus-within > div {{
    border-color:#1846A3 !important;
    background:#fff !important;
    box-shadow:0 0 0 3px rgba(24,70,163,.12) !important;
}}

/* ── Actual input element: fills wrapper, no border of its own ── */
div[data-testid="stForm"] input[type="text"],
div[data-testid="stForm"] input[type="email"],
div[data-testid="stForm"] input[type="password"] {{
    flex:1 1 auto !important;
    width:100% !important;
    min-width:0 !important;
    height:56px !important;
    border:none !important;
    background:transparent !important;
    padding:0 12px 0 48px !important;
    font-size:.95rem !important;
    font-family:'Inter',sans-serif !important;
    color:#0F172A !important;
    line-height:56px !important;
    box-shadow:none !important;
    outline:none !important;
    box-sizing:border-box !important;
}}

/* ── Icons via background on the wrapper ── */
div[data-testid="stForm"] [data-testid="stTextInput"]:has(input[type="text"]) > div,
div[data-testid="stForm"] [data-testid="stTextInput"]:has(input[type="email"]) > div {{
    background:#F8FAFF url("{_ICON_USER}") no-repeat 16px center !important;
    background-size:18px !important;
}}
div[data-testid="stForm"] [data-testid="stTextInput"]:has(input[type="password"]) > div {{
    background:#F8FAFF url("{_ICON_LOCK}") no-repeat 16px center !important;
    background-size:18px !important;
}}
div[data-testid="stForm"] [data-testid="stTextInput"]:has(input[type="text"]):focus-within > div,
div[data-testid="stForm"] [data-testid="stTextInput"]:has(input[type="email"]):focus-within > div,
div[data-testid="stForm"] [data-testid="stTextInput"]:has(input[type="password"]):focus-within > div {{
    background-color:#fff !important;
}}

/* ── Placeholder ── */
div[data-testid="stForm"] input::placeholder {{
    color:#94A3B8 !important;
    font-size:.95rem !important;
    opacity:1 !important;
}}

/* ── Override Chrome/Safari autofill dark background ── */
div[data-testid="stForm"] input:-webkit-autofill,
div[data-testid="stForm"] input:-webkit-autofill:hover,
div[data-testid="stForm"] input:-webkit-autofill:focus,
div[data-testid="stForm"] input:-webkit-autofill:active {{
    -webkit-box-shadow:0 0 0 100px #F8FAFF inset !important;
    box-shadow:0 0 0 100px #F8FAFF inset !important;
    -webkit-text-fill-color:#0F172A !important;
    caret-color:#0F172A !important;
    border-color:#D6E0F5 !important;
    transition:background-color 9999s ease-in-out 0s !important;
}}

/* ── Eye toggle: sits flush inside the wrapper, no extra width ── */
div[data-testid="stForm"] [data-testid="stTextInput"] button {{
    flex:0 0 auto !important;
    width:40px !important; height:40px !important;
    min-width:0 !important; min-height:0 !important;
    background:transparent !important;
    box-shadow:none !important;
    border:none !important;
    border-radius:8px !important;
    padding:0 !important;
    margin:0 8px 0 0 !important;
    transform:none !important;
    color:#94A3B8 !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    cursor:pointer !important;
}}
div[data-testid="stForm"] [data-testid="stTextInput"] button:hover {{
    background:rgba(24,70,163,.06) !important;
    color:#1846A3 !important;
    box-shadow:none !important;
    transform:none !important;
}}

/* Sign In button */
div[data-testid="stForm"] button {{
    width:100% !important; height:56px !important;
    background:linear-gradient(135deg,#0D2E8F 0%,#1846A3 50%,#2563EB 100%) !important;
    color:#fff !important; border:none !important; border-radius:14px !important;
    font-size:1.02rem !important; font-weight:700 !important; letter-spacing:.5px !important;
    font-family:'Inter',sans-serif !important;
    box-shadow:0 4px 20px rgba(13,46,143,.35) !important;
    transition:transform .2s,box-shadow .2s !important;
    cursor:pointer !important; margin-top:6px !important;
}}
div[data-testid="stForm"] button:hover {{
    transform:translateY(-2px) !important;
    box-shadow:0 12px 32px rgba(13,46,143,.42) !important;
}}
div[data-testid="stForm"] button:active {{
    transform:translateY(0) !important;
    box-shadow:0 4px 12px rgba(13,46,143,.25) !important;
}}

/* Trust indicators */
.lc-trust {{
    display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin:20px 0 0;
}}
.lc-trust-item {{
    display:flex; flex-direction:column; align-items:center;
    text-align:center; gap:6px; padding:12px 8px;
    background:#F0F7FF; border-radius:12px; border:1px solid #DBEAFE;
}}
.lc-trust-icon {{
    width:30px; height:30px; background:rgba(33,212,196,.15);
    border-radius:8px; display:flex; align-items:center; justify-content:center;
}}
.lc-trust-label {{
    font-size:.68rem; font-weight:500; color:#475569;
    line-height:1.3; font-family:'Inter',sans-serif;
}}

/* Footer */
.lc-foot {{
    text-align:center; margin-top:22px; font-family:'Inter',sans-serif;
    border-top:1px solid #F1F5F9; padding-top:18px;
}}
.lc-foot-title {{ font-size:.82rem; font-weight:700; color:#334155; margin-bottom:4px; }}
.lc-foot-sub {{ font-size:.72rem; color:#94A3B8; letter-spacing:.2px; }}
</style>
{_branding_panel(logo)}
<div class="login-wrapper"></div>
""", unsafe_allow_html=True)


def require_login() -> str:
    """
    Show branded enterprise login. Internal credentials only — no OAuth/SSO.
    """
    if st.session_state.get("authentication_status"):
        with st.sidebar:
            if st.button("Logout", use_container_width=True, key="logout_btn"):
                for k in ["authentication_status", "username", "name",
                          "_role", "_username", "_name"]:
                    st.session_state.pop(k, None)
                st.rerun()
        return st.session_state.get("_role", "user")

    logo = _logo_b64()
    _inject_css(logo)

    # Disable browser autofill + strip "Press Enter to submit form" placeholder text.
    # Chrome ignores autocomplete="off" on inputs but respects it when a dummy
    # username/password pair appears before the real fields.
    st.markdown("""
<div style="display:none;position:absolute;left:-9999px;width:0;height:0;overflow:hidden"
     aria-hidden="true">
  <input type="text"     name="fake_user" autocomplete="username"       tabindex="-1"/>
  <input type="password" name="fake_pass" autocomplete="current-password" tabindex="-1"/>
</div>
<img src="x" onerror="
(function fix(){
  document.querySelectorAll('input[type=text],input[type=email],input[type=password]').forEach(function(el){
    if(el.placeholder) el.placeholder=el.placeholder.replace(/\\s*Press Enter to submit form\\s*/gi,'').trim();
    el.setAttribute('autocomplete','off');
    el.setAttribute('data-form-type','other');
    el.setAttribute('autocorrect','off');
    el.setAttribute('autocapitalize','none');
    el.setAttribute('spellcheck','false');
    var f=el.closest('form');
    if(f) f.setAttribute('autocomplete','off');
  });
  setTimeout(fix,600);
  setTimeout(fix,1500);
})();
" style="display:none;position:absolute;width:0;height:0"/>
""", unsafe_allow_html=True)

    def _trust_item(icon_path_encoded: str, label: str) -> str:
        icon_src = (
            f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' "
            f"viewBox='0 0 24 24' fill='none' stroke='%2321D4C4' stroke-width='2' "
            f"stroke-linecap='round' stroke-linejoin='round'%3E{icon_path_encoded}%3C/svg%3E"
        )
        return (
            f'<div class="lc-trust-item">'
            f'<div class="lc-trust-icon"><img src="{icon_src}" width="16" height="16"/></div>'
            f'<div class="lc-trust-label">{label}</div>'
            f'</div>'
        )

    trust_html = (
        '<div class="lc-trust">'
        + _trust_item("%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E", "Secure<br>Authentication")
        + _trust_item("%3Crect x='3' y='11' width='18' height='11' rx='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E", "Encrypted<br>Session")
        + _trust_item("%3Cpath d='M5 12.55a11 11 0 0 1 14.08 0'/%3E%3Cpath d='M1.42 9a16 16 0 0 1 21.16 0'/%3E%3Ccircle cx='12' cy='20' r='1'/%3E", "Internal<br>Network")
        + '</div>'
    )

    with st.form("polaris_login"):

        st.markdown(
            f'<div class="lc-head">'
            f'<img class="lc-logo-img" src="data:image/svg+xml;base64,{logo}" alt="Polaris"/>'
            f'<h1>Welcome to Polaris</h1>'
            f'<div class="lc-app-sub">Automation Dashboard</div>'
            f'<p>Sign in using your Polaris credentials.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        submitted = st.form_submit_button("Sign In  →", use_container_width=True)

        # Error shown inside the card
        if st.session_state.get("_login_error"):
            st.markdown(
                '<div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:10px;'
                'padding:10px 14px;color:#DC2626;font-size:.84rem;font-family:Inter,sans-serif;'
                'display:flex;align-items:center;gap:8px;">'
                '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#DC2626" '
                'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>'
                '<line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
                'Incorrect username or password. Please try again.</div>',
                unsafe_allow_html=True,
            )

        st.markdown(trust_html, unsafe_allow_html=True)

        st.markdown(
            '<div class="lc-foot">'
            '<div class="lc-foot-title">Secure Enterprise Access</div>'
            '<div class="lc-foot-sub">Internal Use Only &nbsp;·&nbsp; Version 2.0</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    if submitted:
        cfg   = _load_creds()
        users = cfg["credentials"]["usernames"]
        if username in users and _verify(password, users[username]["password"]):
            st.session_state.pop("_login_error", None)
            role = users[username].get("role", "user")
            st.session_state["authentication_status"] = True
            st.session_state["username"]  = username
            st.session_state["name"]      = users[username].get("name", username)
            st.session_state["_role"]     = role
            st.session_state["_username"] = username
            st.session_state["_name"]     = users[username].get("name", username)
            st.rerun()
        else:
            st.session_state["_login_error"] = True
            st.rerun()

    st.stop()


def is_admin() -> bool:
    return st.session_state.get("_role") == "admin"


def current_user() -> str:
    return st.session_state.get("_name", "")

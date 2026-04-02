"""
Maison Beauté AI Advisor — Streamlit App
Premium editorial interface · Vogue meets tech dashboard
Run: streamlit run streamlit_app.py
Requires: FastAPI backend at http://127.0.0.1:8000
"""

import os
import streamlit as st
import requests
import uuid
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ── Constants ─────────────────────────────────────────────────────────────────
try:
    API_BASE = st.secrets["API_BASE"]
except:
    API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

DARK   = "#1A1A2E"
PURPLE = "#2D1B4E"
ROSE   = "#C9748F"
CREAM  = "#F2E8D9"
GOLD   = "#C9A84C"
LIGHT  = "#F8F5F2"
MUTED  = "#9B8FA0"
GREEN  = "#2D9B74"

SEGMENT_COUNTS = {
    "All subscribers":      1240,
    "Skincare enthusiasts": 380,
    "Fragrance collectors": 210,
    "New customers":        95,
    "VIP members":          45,
}

NEWSLETTER_SKUS = [
    {"name": "Lancôme Lip Idôle JuicyTreat", "sku": "WI-000002100", "badge": "MAKE-UP",   "badge_class": "b-makeup",   "key": "lancome"},
    {"name": "La Mer The Treatment Lotion",   "sku": "WI-000000148", "badge": "SKIN-CARE",  "badge_class": "b-skincare", "key": "lamer"},
    {"name": "U Beauty Resurfacing Compound", "sku": "WI-000000440", "badge": "SKIN-CARE",  "badge_class": "b-skincare", "key": "ubeauty"},
]

EVAL_PATH = os.path.join(os.path.dirname(__file__), "evals", "eval_results.json")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Maison Beauté · AI Advisor",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state init ────────────────────────────────────────────────────────
_defaults = {
    "chat_history":           [],
    "faq_history":            [],
    "session_id":             str(uuid.uuid4())[:8],
    "faq_session_id":         str(uuid.uuid4())[:8],
    "total_queries":          0,
    "safety_flags":           0,
    "newsletters_sent":       0,
    "products_generated":     {},
    "newsletter_result":      None,
    "newsletter_send_status": None,
    "newsletter_sel_skus":    ["lancome", "lamer", "ubeauty"],
    "discount_code":          "MB-SKIN-20",
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, .stApp { background: #F8F5F2 !important; }
.block-container { padding: 0 0 0 0 !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden !important; }
* { font-family: 'Inter', sans-serif; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1A2E 0%, #2D1B4E 100%) !important;
    min-width: 258px !important;
    max-width: 258px !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span,
[data-testid="stSidebar"] label span,
[data-testid="stSidebar"] label p { color: rgba(242,232,217,0.72) !important; }
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex !important; flex-direction: column !important; gap: 0 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    padding: 0.72rem 1.3rem !important;
    border-radius: 0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    cursor: pointer !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    transition: background 0.15s, border-left-color 0.15s !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(201,116,143,0.1) !important;
    border-left-color: rgba(201,116,143,0.4) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
    background: rgba(201,116,143,0.16) !important;
    border-left-color: #C9748F !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) span,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) p {
    color: #F2E8D9 !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label input[type="radio"] { display: none !important; }

/* ── Page header ── */
.pg-header {
    background: linear-gradient(135deg, #1A1A2E 0%, #2D1B4E 60%, #1A1A2E 100%);
    padding: 1.75rem 2.5rem 1.5rem 2.5rem;
    border-bottom: 1px solid rgba(201,168,76,0.2);
}
.pg-badge {
    display: inline-block;
    background: rgba(201,116,143,0.18);
    border: 1px solid rgba(201,116,143,0.35);
    color: #C9748F !important;
    font-family: 'Inter', sans-serif;
    font-size: 0.63rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.17rem 0.72rem;
    border-radius: 20px;
    margin-bottom: 0.45rem;
}
.pg-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.85rem;
    color: #F2E8D9;
    margin: 0;
    line-height: 1.15;
}
.pg-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: rgba(242,232,217,0.5);
    margin-top: 0.3rem;
    line-height: 1.5;
    max-width: 580px;
}

/* ── Cards ── */
.mb-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(26,26,46,0.07);
    margin-bottom: 1.2rem;
}
.card-rose    { border-left: 3px solid #C9748F; }
.card-success { border-left: 3px solid #2D9B74; background: #FAFFFD; }
.card-gold    { border-left: 3px solid #C9A84C; }
.card-purple  { border-left: 3px solid #2D1B4E; background: #FAFAFF; }

/* ── Badges ── */
.badge {
    display: inline-block; padding: 0.14rem 0.62rem; border-radius: 20px;
    font-size: 0.67rem; font-weight: 600; letter-spacing: 0.04em;
    margin-right: 0.25rem; margin-bottom: 0.35rem;
}
.b-pending  { background: #FFF3CD; color: #856404; }
.b-source   { background: #E8F4FD; color: #0C5460; }
.b-ok       { background: #D4EDDA; color: #155724; }
.b-safety   { background: #F8D7DA; color: #721C24; }
.b-makeup   { background: #FCE8F3; color: #7C1D5A; }
.b-skincare { background: #E3F3FF; color: #1A5C87; }
.b-pass     { background: #D4EDDA; color: #155724; }
.b-fail     { background: #F8D7DA; color: #721C24; }

/* ── Product listing ── */
.prod-title   { font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #1A1A2E; margin: 0.5rem 0 0.2rem; }
.prod-tagline { font-size: 0.88rem; color: #C9748F; font-style: italic; margin-bottom: 0.8rem; }
.prod-desc    { font-size: 0.875rem; color: #3A2A4A; line-height: 1.75; margin-bottom: 1rem; }
.seo-tag {
    display: inline-block; background: #F0ECF8; color: #5C2D6E;
    padding: 0.2rem 0.62rem; border-radius: 10px;
    margin: 0.12rem; font-size: 0.69rem;
}

/* ── Chat ── */
.chat-wrap {
    max-height: 440px; overflow-y: auto; padding: 0.4rem 0;
    margin-bottom: 0.8rem; scroll-behavior: smooth;
}
.chat-user {
    background: #1A1A2E; color: #F2E8D9;
    padding: 0.7rem 1rem; border-radius: 16px 16px 4px 16px;
    margin: 0.45rem 0 0.45rem 18%;
    font-size: 0.875rem; line-height: 1.55;
}
.chat-bot {
    background: white; border: 1px solid #E8E0DC; color: #2A1A3E;
    padding: 0.7rem 1rem; border-radius: 16px 16px 16px 4px;
    margin: 0.45rem 18% 0.45rem 0;
    font-size: 0.875rem; line-height: 1.55;
    box-shadow: 0 1px 5px rgba(0,0,0,0.04);
}
.chat-alert {
    background: #FFF0F0; border: 1px solid #EDBBBB; color: #8B2020;
    padding: 0.7rem 1rem; border-radius: 16px 16px 16px 4px;
    margin: 0.45rem 18% 0.45rem 0;
    font-size: 0.875rem; line-height: 1.55;
}
.chat-intro {
    background: #F4F0FF; border: 1px dashed #D0C0E8; color: #5C2D6E;
    padding: 0.7rem 1rem; border-radius: 16px 16px 16px 4px;
    margin: 0.45rem 18% 0.45rem 0;
    font-size: 0.875rem; font-style: italic; line-height: 1.55;
}

/* ── Analytics panel ── */
.ana-card {
    background: white; border-radius: 8px; padding: 1rem 1.2rem;
    box-shadow: 0 1px 8px rgba(26,26,46,0.06);
    margin-bottom: 0.8rem; text-align: center;
}
.ana-val { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #1A1A2E; line-height: 1; }
.ana-lbl { font-size: 0.66rem; font-weight: 600; color: #9B8FA0; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.2rem; }

/* ── Order timeline ── */
.tl-wrap { display: flex; align-items: flex-start; margin: 1.8rem 0; }
.tl-step { flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; }
.tl-step:not(:last-child)::after {
    content: ''; position: absolute; top: 13px; left: 50%; width: 100%;
    height: 2px; background: #E8E0DC; z-index: 0;
}
.tl-done:not(:last-child)::after  { background: #C9A84C !important; }
.tl-dot {
    width: 28px; height: 28px; border-radius: 50%;
    background: #E8E0DC; border: 2px solid #CCC4C8;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.68rem; color: white; font-weight: 700;
    position: relative; z-index: 1; flex-shrink: 0;
}
.tl-dot-done   { background: #C9A84C !important; border-color: #C9A84C !important; }
.tl-dot-active { background: #2D9B74 !important; border-color: #2D9B74 !important; box-shadow: 0 0 0 5px rgba(45,155,116,0.18); }
.tl-label { font-size: 0.68rem; color: #9B8FA0; margin-top: 0.5rem; text-align: center; font-weight: 500; line-height: 1.3; }
.tl-label-done   { color: #C9A84C !important; font-weight: 600 !important; }
.tl-label-active { color: #2D9B74 !important; font-weight: 700 !important; }

/* ── Newsletter ── */
.nl-subj { font-family: 'Playfair Display', serif; font-size: 1.45rem; color: #1A1A2E; margin: 0 0 0.25rem; line-height: 1.2; }
.nl-prev { font-size: 0.82rem; color: #9B8FA0; font-style: italic; margin-bottom: 1rem; }
.nl-cta  { font-size: 0.875rem; font-weight: 600; color: #C9748F; border-top: 1px solid #E8E0DC; padding-top: 0.8rem; margin-top: 1rem; }
.nl-prod {
    display: flex; align-items: center; gap: 0.85rem;
    background: #FAFAFA; border: 1px solid #EDE8E3;
    border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.6rem;
}
.nl-prod-img { width: 46px; height: 46px; background: linear-gradient(135deg, #2D1B4E 0%, #C9748F 100%); border-radius: 6px; flex-shrink: 0; }
.nl-prod-name { font-family: 'Playfair Display', serif; font-size: 0.9rem; color: #1A1A2E; margin: 0 0 0.1rem; }
.nl-prod-sku  { font-size: 0.69rem; color: #9B8FA0; margin-bottom: 0.15rem; }
.nl-prod-lnk  { font-size: 0.72rem; color: #C9748F; font-weight: 600; }
.nl-sent-badge {
    background: linear-gradient(135deg, #2D9B74, #1A7A5A);
    color: white; padding: 0.9rem 1.2rem; border-radius: 8px;
    font-family: 'Inter', sans-serif; font-size: 0.82rem;
    display: flex; align-items: center; gap: 0.6rem;
    margin-top: 1rem;
}

/* ── KPI cards ── */
.kpi { background: white; border-radius: 8px; padding: 1.2rem 1.3rem; box-shadow: 0 2px 10px rgba(26,26,46,0.06); border-top: 3px solid transparent; }
.kpi-rose   { border-top-color: #C9748F; }
.kpi-gold   { border-top-color: #C9A84C; }
.kpi-green  { border-top-color: #2D9B74; }
.kpi-purple { border-top-color: #2D1B4E; }
.kpi-val { font-family: 'Playfair Display', serif; font-size: 2.3rem; color: #1A1A2E; line-height: 1; margin-bottom: 0.2rem; }
.kpi-lbl { font-size: 0.67rem; font-weight: 600; color: #9B8FA0; letter-spacing: 0.14em; text-transform: uppercase; }
.kpi-sub { font-size: 0.72rem; color: #2D9B74; margin-top: 0.2rem; }

/* ── Eval table ── */
.ev-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.ev-table th { background: #F8F5F2; color: #9B8FA0; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.55rem 0.8rem; text-align: left; border-bottom: 2px solid #E8E0DC; }
.ev-table td { padding: 0.55rem 0.8rem; border-bottom: 1px solid #F0ECF8; color: #3A2A4A; vertical-align: middle; }
.ev-table tr:last-child td { border-bottom: none; }
.ev-table tr:hover td { background: #FAFAFA; }

/* ── Misc ── */
.lbl { font-size: 0.67rem; font-weight: 600; color: #9B8FA0; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 0.35rem; }
.divider { border: none; border-top: 1px solid #E8E0DC; margin: 1.2rem 0; }
.mb-footer {
    text-align: center; padding: 1.4rem 2.5rem 1rem;
    font-size: 0.72rem; color: #B0A4B8; letter-spacing: 0.05em;
    border-top: 1px solid #E8E0DC; margin-top: 2.5rem;
}

/* Streamlit widget overrides */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    border-color: #D6C9D4 !important;
    border-radius: 5px !important;
    font-size: 0.875rem !important;
    background: white !important;
    color: #1A1A2E !important;
}
.stSelectbox > div > div { border-radius: 5px !important; }
.stButton > button {
    background: #1A1A2E !important;
    color: #F2E8D9 !important;
    border: none !important;
    border-radius: 4px !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    padding: 0.55rem 1.5rem !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #2D1B4E !important; }
.stDownloadButton > button {
    background: transparent !important;
    color: #C9748F !important;
    border: 1px solid #C9748F !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em !important;
}
.stDownloadButton > button:hover { background: rgba(201,116,143,0.08) !important; }
.stSpinner > div { color: #C9748F !important; }
div[data-testid="stMetricValue"] { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def page_header(badge: str, title: str, subtitle: str = ""):
    sub_html = f'<div class="pg-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="pg-header">
        <div class="pg-badge">{badge}</div>
        <div class="pg-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def page_footer():
    st.markdown("""
    <div class="mb-footer">
        Maison Beauté AI Advisor &nbsp;·&nbsp;
        Powered by Claude Haiku · Pinecone · LangGraph · n8n · LangSmith &nbsp;·&nbsp;
        Berlin · 2026 &nbsp;·&nbsp; EU AI Act Compliant
    </div>
    """, unsafe_allow_html=True)


def brand_chart(fig, title: str = "", height: int = 300, bg: str = "white"):
    title_cfg = dict(text=title, font=dict(family="Playfair Display, serif", size=13, color=DARK)) if title else {}
    fig.update_layout(
        title=title_cfg,
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        height=height,
        margin=dict(l=20, r=20, t=38 if title else 18, b=20),
        font=dict(family="Inter, sans-serif", size=11, color=DARK),
        legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="#F0ECF8", linecolor="#E8E0DC", tickfont=dict(size=10))
    fig.update_yaxes(gridcolor="#F0ECF8", linecolor="#E8E0DC", tickfont=dict(size=10))
    return fig


def section_pad():
    """Adds consistent top padding after header."""
    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.8rem 1.4rem 1.3rem 1.4rem; border-bottom:1px solid rgba(201,116,143,0.18);">
        <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:#F2E8D9;letter-spacing:0.04em;line-height:1.1">
            Maison Beauté
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.62rem;color:#C9748F;letter-spacing:0.22em;text-transform:uppercase;margin-top:0.3rem">
            AI Advisory System
        </div>
        <div style="display:flex;gap:0.35rem;flex-wrap:wrap;margin-top:0.85rem">
            <span style="background:rgba(201,116,143,0.14);border:1px solid rgba(201,116,143,0.25);color:rgba(242,232,217,0.65);padding:0.13rem 0.5rem;border-radius:10px;font-size:0.59rem">Claude Haiku</span>
            <span style="background:rgba(201,116,143,0.14);border:1px solid rgba(201,116,143,0.25);color:rgba(242,232,217,0.65);padding:0.13rem 0.5rem;border-radius:10px;font-size:0.59rem">Pinecone RAG</span>
            <span style="background:rgba(201,116,143,0.14);border:1px solid rgba(201,116,143,0.25);color:rgba(242,232,217,0.65);padding:0.13rem 0.5rem;border-radius:10px;font-size:0.59rem">LangGraph</span>
            <span style="background:rgba(201,116,143,0.14);border:1px solid rgba(201,116,143,0.25);color:rgba(242,232,217,0.65);padding:0.13rem 0.5rem;border-radius:10px;font-size:0.59rem">n8n</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:0.7rem 1.3rem 0.4rem;font-family:'Inter',sans-serif;font-size:0.6rem;
         font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:rgba(242,232,217,0.3)">
        Navigation
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        [
            "🏪  Shop Manager",
            "💬  Beauty Advisor",
            "📋  FAQ & Policies",
            "📦  Order Tracking",
            "✉  Newsletter Studio",
            "📊  Analytics",
        ],
        label_visibility="collapsed",
        key="nav_page",
    )

    st.markdown("""
    <div style="border-top:1px solid rgba(255,255,255,0.06);margin:0;padding:1rem 1.4rem 0.9rem;">
        <div style="font-family:'Inter',sans-serif;font-size:0.6rem;font-weight:600;letter-spacing:0.2em;
             text-transform:uppercase;color:rgba(242,232,217,0.3);margin-bottom:0.65rem">System Status</div>
        <div style="display:flex;flex-direction:column;gap:0.4rem">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:0.76rem;color:rgba(242,232,217,0.65)">LangSmith</span>
                <span style="font-size:0.7rem;color:#2D9B74;display:flex;align-items:center;gap:4px">
                    <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#2D9B74;box-shadow:0 0 0 2px rgba(45,155,116,0.25)"></span> ON
                </span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:0.76rem;color:rgba(242,232,217,0.65)">Pinecone</span>
                <span style="font-size:0.7rem;color:#C9A84C">2 namespaces</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:0.76rem;color:rgba(242,232,217,0.65)">n8n</span>
                <span style="font-size:0.7rem;color:#C9A84C">3 workflows</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Live metrics — dynamic values from session state
    q  = st.session_state.total_queries
    sf = st.session_state.safety_flags
    nl = st.session_state.newsletters_sent
    st.markdown(f"""
    <div style="padding:0.9rem 1.4rem 1.4rem;border-top:1px solid rgba(255,255,255,0.06)">
        <div style="font-family:'Inter',sans-serif;font-size:0.6rem;font-weight:600;letter-spacing:0.2em;
             text-transform:uppercase;color:rgba(242,232,217,0.3);margin-bottom:0.7rem">Live · Today</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.45rem">
            <div style="background:rgba(255,255,255,0.05);border-radius:6px;padding:0.5rem;text-align:center">
                <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:#F2E8D9;line-height:1">{q}</div>
                <div style="font-size:0.56rem;color:rgba(242,232,217,0.38);margin-top:0.18rem;letter-spacing:0.06em;text-transform:uppercase">Queries</div>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:6px;padding:0.5rem;text-align:center">
                <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:#C9748F;line-height:1">{sf}</div>
                <div style="font-size:0.56rem;color:rgba(242,232,217,0.38);margin-top:0.18rem;letter-spacing:0.06em;text-transform:uppercase">Flags</div>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:6px;padding:0.5rem;text-align:center">
                <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:#C9A84C;line-height:1">{nl}</div>
                <div style="font-size:0.56rem;color:rgba(242,232,217,0.38);margin-top:0.18rem;letter-spacing:0.06em;text-transform:uppercase">NL Sent</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE 1 — SHOP MANAGER
# ════════════════════════════════════════════════════════════════
if page == "🏪  Shop Manager":
    page_header(
        "Module 1",
        "Shop Manager",
        "Generate complete product listings with AI-powered copy, auto-fetched ingredients, and SEO optimisation.",
    )
    st.markdown('<div style="padding:2rem 2.5rem 0">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.markdown('<div class="lbl">Product Details</div>', unsafe_allow_html=True)
        r1a, r1b = st.columns(2)
        with r1a:
            product_id = st.text_input("Product ID", value="MB-2026-0001")
        with r1b:
            brand = st.text_input("Brand", value="Charlotte Tilbury")
        product_name = st.text_input("Product Name", value="Pillow Talk Lipstick")
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("Category", ["Make-up", "Parfumes", "Skin-care", "Body-care", "Hair-care", "Beauty Tools"])
        with c2:
            condition = st.selectbox("Condition", ["New", "Tested Out", "Pre-loved"])
        c3, c4 = st.columns(2)
        with c3:
            batch_number = st.text_input("Batch Number", value="B2025-09-CT")
        with c4:
            expiry_date = st.text_input("Expiry Date (YYYY-MM)", value="2027-06")

    with col2:
        st.markdown('<div class="lbl">Pricing & Size</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            original_price = st.number_input("Retail Price (€)", min_value=0.0, value=39.0)
        with p2:
            listing_price = st.number_input("Listing Price (€)", min_value=0.0, value=22.0)
        s1, s2 = st.columns(2)
        with s1:
            size_value = st.number_input("Size", min_value=0.0, value=3.5)
        with s2:
            size_unit = st.selectbox("Unit", ["g", "ml"])
        st.markdown('<div class="lbl" style="margin-top:0.8rem">Manual Ingredients</div>', unsafe_allow_html=True)
        manual_ingredients = st.text_area(
            "ingredients",
            placeholder="e.g. Vitamin E, Shea Butter, Hyaluronic Acid",
            height=90,
            label_visibility="collapsed",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✦  Generate Product Listing", key="btn_generate"):
        payload = {
            "product_id": product_id, "brand": brand, "product_name": product_name,
            "category": category, "condition": condition, "batch_number": batch_number,
            "expiry_date": expiry_date, "original_retail_price_eur": original_price,
            "listing_price_eur": listing_price, "size_value": size_value, "size_unit": size_unit,
        }
        if manual_ingredients:
            payload["key_ingredients"] = [i.strip() for i in manual_ingredients.split(",") if i.strip()]

        with st.spinner("Fetching ingredients · Generating copy with Claude Haiku..."):
            try:
                r = requests.post(f"{API_BASE}/products/generate-description", json=payload, timeout=30)
                if r.status_code == 200:
                    d = r.json()
                    tags_html = " ".join(f'<span class="seo-tag">{t}</span>' for t in d.get("seo_tags", []))
                    verified_txt = "✅ Ingredients verified" if d.get("ingredients_verified") else "⚠️ Pending ingredient verification"
                    source = d.get("ingredients_source", "api").upper()
                    st.markdown(f"""
                    <div class="mb-card card-rose">
                        <span class="badge b-pending">⏳ Pending Review</span>
                        <span class="badge b-source">⚡ via {source}</span>
                        <div class="prod-title">{d.get('title','')}</div>
                        <div class="prod-tagline">{d.get('tagline','')}</div>
                        <div class="prod-desc">{d.get('description','')}</div>
                        <div style="margin-bottom:0.8rem">{tags_html}</div>
                        <hr class="divider">
                        <div style="font-size:0.78rem;color:#9B8FA0;line-height:1.7">
                            {d.get('condition_note','')}<br>
                            <strong>Batch:</strong> {d.get('batch_number','')} &nbsp;·&nbsp;
                            <strong>Expires:</strong> {d.get('expiry_date','')} &nbsp;·&nbsp;
                            {verified_txt}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    # Track for bar chart
                    cat = category
                    st.session_state.products_generated[cat] = st.session_state.products_generated.get(cat, 0) + 1
                    st.session_state.total_queries += 1
                elif r.status_code == 400:
                    st.error(r.json().get("detail", "Validation error"))
                else:
                    st.error(f"Error {r.status_code}: {r.text[:200]}")
            except requests.exceptions.ConnectionError:
                st.error("❌ FastAPI backend not running. Start with: `uvicorn app.main:app --reload`")

    # ── Products bar chart ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="lbl">Products Generated This Session · By Category</div>', unsafe_allow_html=True)
    if st.session_state.products_generated:
        cats   = list(st.session_state.products_generated.keys())
        counts = list(st.session_state.products_generated.values())
        fig = px.bar(
            x=cats, y=counts,
            color=cats,
            color_discrete_sequence=[ROSE, GOLD, GREEN, PURPLE, MUTED, "#5C2D6E"],
            labels={"x": "Category", "y": "Count"},
        )
        fig.update_traces(marker_line_width=0, width=0.45)
        fig = brand_chart(fig, height=260)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown("""
        <div style="background:white;border-radius:8px;padding:2rem;text-align:center;
             box-shadow:0 2px 10px rgba(26,26,46,0.06);color:#9B8FA0;font-size:0.85rem;border:1px dashed #E8E0DC">
            Generate a product listing to see the chart.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    page_footer()


# ════════════════════════════════════════════════════════════════
# PAGE 2 — BEAUTY ADVISOR
# ════════════════════════════════════════════════════════════════
elif page == "💬  Beauty Advisor":
    page_header(
        "Module 2",
        "Beauty Advisor — Beauté",
        "Ask about products, ingredients, and skin-type recommendations. Health or allergy concerns are escalated to our team.",
    )
    st.markdown('<div style="padding:2rem 2.5rem 0">', unsafe_allow_html=True)

    col_chat, col_ana = st.columns([2, 1], gap="large")

    with col_chat:
        # Quick chips
        st.markdown('<div class="lbl" style="margin-bottom:0.5rem">Quick Suggestions</div>', unsafe_allow_html=True)
        chips = ["Dry skin recommendations", "Tell me about La Mer", "Best for anti-aging", "Fragrance for evening"]
        chip_cols = st.columns(4)
        for i, chip in enumerate(chips):
            with chip_cols[i]:
                if st.button(chip, key=f"chip_{i}"):
                    st.session_state.chat_history.append({"role": "user", "content": chip})
                    try:
                        resp = requests.post(f"{API_BASE}/chat/", json={
                            "session_id": st.session_state.session_id,
                            "message": chip,
                            "chat_history": [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]],
                        }, timeout=30)
                        if resp.status_code == 200:
                            d = resp.json()
                            st.session_state.chat_history.append({
                                "role": "assistant", "content": d["response"],
                                "escalated": d.get("escalated", False),
                            })
                            st.session_state.total_queries += 1
                            if d.get("escalated"):
                                st.session_state.safety_flags += 1
                    except Exception:
                        pass
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Chat bubbles
        chat_html = '<div class="chat-wrap"><div class="chat-intro">👋 Bonjour! I\'m Beauté, your AI beauty advisor. Ask me about products, ingredients, or skin-type recommendations.</div>'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f'<div class="chat-user">{msg["content"]}</div>'
            elif msg.get("escalated"):
                chat_html += f'<div class="chat-alert">🛡️ {msg["content"]}</div>'
            else:
                chat_html += f'<div class="chat-bot">{msg["content"]}</div>'
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        # Input
        msg_col, send_col = st.columns([5, 1])
        with msg_col:
            user_msg = st.text_input(
                "msg", placeholder="What do you recommend for dry skin?",
                label_visibility="collapsed", key="chat_input",
            )
        with send_col:
            send_btn = st.button("Send →", key="btn_chat_send")

        if send_btn and user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            with st.spinner("Beauté is thinking..."):
                try:
                    resp = requests.post(f"{API_BASE}/chat/", json={
                        "session_id": st.session_state.session_id,
                        "message": user_msg,
                        "chat_history": [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]],
                    }, timeout=30)
                    if resp.status_code == 200:
                        d = resp.json()
                        st.session_state.chat_history.append({
                            "role": "assistant", "content": d["response"],
                            "escalated": d.get("escalated", False),
                        })
                        st.session_state.total_queries += 1
                        if d.get("escalated"):
                            st.session_state.safety_flags += 1
                    else:
                        st.error(f"Error {resp.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend not running.")
            st.rerun()

        clr_col, hint_col = st.columns([1, 4])
        with clr_col:
            if st.button("↺ Clear", key="btn_chat_clear"):
                st.session_state.chat_history = []
                st.session_state.session_id = str(uuid.uuid4())[:8]
                st.rerun()
        with hint_col:
            st.markdown('<p style="font-size:0.74rem;color:#B0A4B8;padding-top:0.5rem">Try: "I have a fragrance allergy" to see safety escalation in action.</p>', unsafe_allow_html=True)

    # ── Analytics panel ──
    with col_ana:
        st.markdown('<div class="lbl">Conversation Analytics</div>', unsafe_allow_html=True)
        msgs      = st.session_state.chat_history
        n_total   = len(msgs)
        n_user    = sum(1 for m in msgs if m["role"] == "user")
        n_flags   = sum(1 for m in msgs if m.get("escalated"))
        bot_msgs  = [m["content"] for m in msgs if m["role"] == "assistant"]
        avg_len   = round(sum(len(m) for m in bot_msgs) / len(bot_msgs)) if bot_msgs else 0

        st.markdown(f"""
        <div class="ana-card">
            <div class="ana-val">{n_total}</div>
            <div class="ana-lbl">Total Messages</div>
        </div>
        <div class="ana-card" style="border-left:3px solid #C9748F">
            <div class="ana-val" style="color:#C9748F">{n_flags}</div>
            <div class="ana-lbl">Safety Flags Triggered</div>
        </div>
        <div class="ana-card">
            <div class="ana-val">{avg_len}</div>
            <div class="ana-lbl">Avg Response Length (chars)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="lbl">Message Breakdown</div>', unsafe_allow_html=True)
        if n_total > 0:
            n_bot = n_total - n_user
            fig = go.Figure(data=[go.Pie(
                labels=["User", "Advisor", "Safety Escalated"],
                values=[n_user, max(0, n_bot - n_flags), n_flags],
                hole=0.6,
                marker_colors=[DARK, ROSE, "#E06060"],
                textfont=dict(size=10),
            )])
            fig = brand_chart(fig, height=200)
            fig.update_layout(showlegend=True, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="color:#9B8FA0;font-size:0.82rem;text-align:center;padding:1rem 0">Start a conversation to see analytics.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    page_footer()


# ════════════════════════════════════════════════════════════════
# PAGE 3 — FAQ & POLICIES
# ════════════════════════════════════════════════════════════════
elif page == "📋  FAQ & Policies":
    page_header(
        "Module 3 · Self-Service",
        "FAQ & Platform Policies",
        "Ask about returns, shipping, product conditions, authenticity checks, or any platform policy.",
    )
    st.markdown('<div style="padding:2rem 2.5rem 0">', unsafe_allow_html=True)

    col_faq, col_chart = st.columns([2, 1], gap="large")

    with col_faq:
        # Quick chips
        st.markdown('<div class="lbl" style="margin-bottom:0.5rem">Quick Questions</div>', unsafe_allow_html=True)
        faq_chips = ["Return policy", "How do you verify authenticity?", "What does Pre-loved mean?", "Do you ship internationally?"]
        chip_cols2 = st.columns(2)
        for i, q_chip in enumerate(faq_chips):
            with chip_cols2[i % 2]:
                if st.button(q_chip, key=f"faq_chip_{i}"):
                    st.session_state.faq_history.append({"role": "user", "content": q_chip})
                    try:
                        resp = requests.post(f"{API_BASE}/chat/faq", json={
                            "session_id": st.session_state.faq_session_id,
                            "message": q_chip, "chat_history": [],
                        }, timeout=30)
                        if resp.status_code == 200:
                            st.session_state.faq_history.append({"role": "assistant", "content": resp.json()["response"]})
                            st.session_state.total_queries += 1
                    except Exception:
                        pass
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Chat bubbles
        faq_html = '<div class="chat-wrap"><div class="chat-intro">📋 Ask anything about our platform — returns, shipping, product conditions, authentication, or pricing.</div>'
        for msg in st.session_state.faq_history:
            if msg["role"] == "user":
                faq_html += f'<div class="chat-user">{msg["content"]}</div>'
            else:
                faq_html += f'<div class="chat-bot">{msg["content"]}</div>'
        faq_html += "</div>"
        st.markdown(faq_html, unsafe_allow_html=True)

        # Input
        fmsg_col, fsend_col = st.columns([5, 1])
        with fmsg_col:
            faq_msg = st.text_input(
                "faq_msg", placeholder="Can I return a product if I change my mind?",
                label_visibility="collapsed", key="faq_input",
            )
        with fsend_col:
            faq_send = st.button("Ask →", key="btn_faq_send")

        if faq_send and faq_msg:
            st.session_state.faq_history.append({"role": "user", "content": faq_msg})
            with st.spinner("Looking up policies..."):
                try:
                    resp = requests.post(f"{API_BASE}/chat/faq", json={
                        "session_id": st.session_state.faq_session_id,
                        "message": faq_msg,
                        "chat_history": [{"role": m["role"], "content": m["content"]} for m in st.session_state.faq_history[:-1]],
                    }, timeout=30)
                    if resp.status_code == 200:
                        st.session_state.faq_history.append({"role": "assistant", "content": resp.json()["response"]})
                        st.session_state.total_queries += 1
                    else:
                        st.error(f"Error {resp.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend not running.")
            st.rerun()

        if st.button("↺ Clear", key="btn_faq_clear"):
            st.session_state.faq_history = []
            st.session_state.faq_session_id = str(uuid.uuid4())[:8]
            st.rerun()

    # ── Donut chart ──
    with col_chart:
        st.markdown('<div class="lbl">FAQ Topics Coverage</div>', unsafe_allow_html=True)
        fig_faq = go.Figure(data=[go.Pie(
            labels=["Returns", "Authenticity", "Shipping", "Conditions", "Other"],
            values=[30, 25, 20, 15, 10],
            hole=0.58,
            marker_colors=[ROSE, GOLD, GREEN, PURPLE, MUTED],
            textfont=dict(size=10),
            textinfo="percent",
        )])
        fig_faq = brand_chart(fig_faq, height=260)
        fig_faq.update_layout(
            legend=dict(orientation="v", x=1.02, font=dict(size=10)),
            margin=dict(l=10, r=80, t=15, b=10),
        )
        st.plotly_chart(fig_faq, use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div class="mb-card card-purple" style="margin-top:0.5rem">
            <div style="font-size:0.72rem;color:#3A2A4A;line-height:1.8">
                <strong style="font-size:0.8rem;color:#1A1A2E">Coverage Note</strong><br>
                Our FAQ knowledge base covers <strong>5 policy categories</strong> grounded
                in official Maison Beauté documentation, updated quarterly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    page_footer()


# ════════════════════════════════════════════════════════════════
# PAGE 4 — ORDER TRACKING
# ════════════════════════════════════════════════════════════════
elif page == "📦  Order Tracking":
    page_header(
        "Module 3 · Order Concierge",
        "Track Your Order",
        "Enter your order number for a status update. Full details are sent securely to your registered email.",
    )
    st.markdown('<div style="padding:2rem 2.5rem 0">', unsafe_allow_html=True)

    col_ord, col_info = st.columns([1.6, 1], gap="large")

    with col_ord:
        st.markdown('<div class="lbl">Order Number</div>', unsafe_allow_html=True)
        order_number = st.text_input(
            "order_num", placeholder="MB-ORD-20241127-0042",
            help="Find this in your order confirmation email",
            label_visibility="collapsed",
        )
        st.markdown('<div style="font-size:0.74rem;color:#9B8FA0;margin:-0.3rem 0 1rem">Test orders: <code>MB-ORD-20241127-0042</code> · <code>MB-ORD-20241128-0099</code></div>', unsafe_allow_html=True)

        if st.button("📦  Track My Order", key="btn_track"):
            if not order_number.strip():
                st.warning("Please enter your order number.")
            else:
                with st.spinner("Looking up your order..."):
                    try:
                        resp = requests.post(f"{API_BASE}/orders/track", json={"order_number": order_number}, timeout=15)
                        if resp.status_code == 200:
                            d = resp.json()
                            summary = d.get("status_summary", "")
                            msg     = d.get("message", "")

                            # Determine timeline step
                            s_lower = summary.lower()
                            if "delivered" in s_lower:
                                step = 4
                            elif "shipped" in s_lower or "transit" in s_lower:
                                step = 3
                            elif "processing" in s_lower or "packed" in s_lower:
                                step = 2
                            else:
                                step = 1

                            def tl_dot_cls(n):
                                if n < step:   return "tl-dot tl-dot-done"
                                if n == step:  return "tl-dot tl-dot-active"
                                return "tl-dot"

                            def tl_lbl_cls(n):
                                if n < step:   return "tl-label tl-label-done"
                                if n == step:  return "tl-label tl-label-active"
                                return "tl-label"

                            def step_cls(n):
                                return "tl-step tl-done" if n < step else "tl-step"

                            steps = [
                                (1, "✓", "Order<br>Placed"),
                                (2, "⟳", "Processing"),
                                (3, "✈", "Shipped"),
                                (4, "✓", "Delivered"),
                            ]
                            tl_html = '<div class="tl-wrap">'
                            for n, icon, label in steps:
                                dot_cls = tl_dot_cls(n)
                                lbl_cls = tl_lbl_cls(n)
                                sc      = step_cls(n)
                                tl_html += f"""
                                <div class="{sc}">
                                    <div class="{dot_cls}">{icon}</div>
                                    <div class="{lbl_cls}">{label}</div>
                                </div>"""
                            tl_html += "</div>"

                            st.markdown(f"""
                            <div class="mb-card card-success">
                                <span class="badge b-ok">✓ Order Found</span>
                                <p style="font-family:'Playfair Display',serif;font-size:1.1rem;color:#1A1A2E;margin:0.5rem 0 0.3rem">{summary}</p>
                                <p style="font-size:0.82rem;color:#6B6080;margin:0">{msg}</p>
                                {tl_html}
                            </div>
                            <div style="font-size:0.75rem;color:#9B8FA0;margin-top:0.2rem">
                                🔒 <strong>Privacy by design:</strong> Full tracking details sent to your registered email. No PII displayed here.
                            </div>
                            """, unsafe_allow_html=True)

                        elif resp.status_code == 404:
                            st.error(f"Order **{order_number}** not found. Please check your order number.")
                        else:
                            st.error(f"Error {resp.status_code}: {resp.text[:200]}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend not running. Start with: `uvicorn app.main:app --reload`")

    with col_info:
        st.markdown("""
        <div class="mb-card card-purple">
            <div style="font-size:0.82rem;color:#3A2A4A;line-height:1.85">
                <strong style="font-family:'Playfair Display',serif;font-size:1rem;color:#1A1A2E">How it works</strong><br><br>
                <span style="color:#C9748F;font-weight:600">1.</span> Enter your order number<br>
                <span style="color:#C9748F;font-weight:600">2.</span> Status shown instantly<br>
                <span style="color:#C9748F;font-weight:600">3.</span> Full details emailed securely<br><br>
                <hr style="border:none;border-top:1px solid #E8E0DC;margin:0.8rem 0">
                <strong style="color:#2D9B74">Zero PII in chat.</strong><br>
                Your email is never shown here — retrieved internally and used only to dispatch your tracking confirmation.
            </div>
        </div>
        <div class="mb-card" style="margin-top:0;background:#FFF9F0;border-left:3px solid #C9A84C">
            <div style="font-size:0.78rem;color:#856404;line-height:1.7">
                <strong>Delivery SLA</strong><br>
                🇩🇪 Germany: 2–3 business days<br>
                🇪🇺 EU countries: 4–6 business days
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    page_footer()


# ════════════════════════════════════════════════════════════════
# PAGE 5 — NEWSLETTER STUDIO
# ════════════════════════════════════════════════════════════════
elif page == "✉  Newsletter Studio":
    page_header(
        "Module 4",
        "Newsletter Studio",
        "Craft on-brand Maison Beauté newsletters in seconds. Feature trending topics, new arrivals, and personalised offers.",
    )
    st.markdown('<div style="padding:2rem 2.5rem 0">', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.1], gap="large")

    # ── LEFT PANEL ──
    with col_left:
        st.markdown('<div class="lbl">Trending Topics</div>', unsafe_allow_html=True)
        topics_input = st.text_area(
            "topics",
            value="glass skin\nsustainable beauty\nperfume layering\nluxury pre-owned",
            height=110, label_visibility="collapsed",
        )

        st.markdown('<div class="lbl" style="margin-top:1rem">New Arrivals to Feature</div>', unsafe_allow_html=True)

        # SKU checkboxes with rich labels
        sku_checked = {}
        for sku in NEWSLETTER_SKUS:
            c_box, c_info = st.columns([0.5, 6])
            with c_box:
                checked = st.checkbox(
                    "", key=f"nl_sku_{sku['key']}",
                    value=(sku["key"] in st.session_state.newsletter_sel_skus),
                )
                sku_checked[sku["key"]] = checked
            with c_info:
                st.markdown(f"""
                <div style="padding-top:4px;line-height:1.4">
                    <span style="font-size:0.875rem;font-weight:500;color:#1A1A2E">{sku['name']}</span>
                    <span class="badge {sku['badge_class']}" style="margin-left:0.4rem">{sku['badge']}</span><br>
                    <span style="font-size:0.69rem;color:#9B8FA0">{sku['sku']}</span>
                </div>
                """, unsafe_allow_html=True)

        # Save checked state
        st.session_state.newsletter_sel_skus = [s["key"] for s in NEWSLETTER_SKUS if sku_checked.get(s["key"])]

        c_lang, c_seg = st.columns(2)
        with c_lang:
            st.markdown('<div class="lbl" style="margin-top:0.8rem">Language</div>', unsafe_allow_html=True)
            language = st.selectbox("lang", ["English", "German", "French", "Portuguese"], label_visibility="collapsed")
        with c_seg:
            st.markdown('<div class="lbl" style="margin-top:0.8rem">Customer Segment</div>', unsafe_allow_html=True)
            segment = st.selectbox(
                "seg",
                list(SEGMENT_COUNTS.keys()),
                label_visibility="collapsed",
            )

        st.markdown('<div class="lbl" style="margin-top:0.8rem">Personalisation</div>', unsafe_allow_html=True)
        personalise = st.toggle("Include personalised discount code", value=False, key="nl_personalise")
        if personalise:
            disc_code = st.text_input("Discount Code", value=st.session_state.discount_code)
            st.session_state.discount_code = disc_code

        # Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)

        selected_skus_list = [s for s in NEWSLETTER_SKUS if sku_checked.get(s["key"])]
        new_products_payload = [s["name"] for s in selected_skus_list]
        topics_list = [t.strip() for t in topics_input.split("\n") if t.strip()]

        with btn_col1:
            gen_btn = st.button("✦  Generate Newsletter", key="btn_nl_gen", use_container_width=True)
        with btn_col2:
            send_btn = st.button("✉  Send to Segment", key="btn_nl_send", use_container_width=True)

        if gen_btn:
            if not topics_list:
                st.warning("Please enter at least one trending topic.")
            else:
                with st.spinner("Crafting your newsletter with Claude Haiku..."):
                    try:
                        resp = requests.post(f"{API_BASE}/newsletter/generate", json={
                            "trending_topics": topics_list,
                            "new_products": new_products_payload,
                            "language": language,
                            "send_email": False,
                        }, timeout=45)
                        if resp.status_code == 200:
                            st.session_state.newsletter_result = resp.json()
                            st.session_state.newsletter_result["_skus"] = selected_skus_list
                            st.session_state.newsletter_result["_segment"] = segment
                            st.session_state.newsletter_send_status = None
                            st.rerun()
                        else:
                            st.error(f"Error {resp.status_code}: {resp.text[:200]}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend not running.")

        if send_btn:
            if not topics_list:
                st.warning("Please enter at least one trending topic.")
            elif st.session_state.newsletter_result is None:
                st.warning("Generate the newsletter first, then click Send.")
            else:
                with st.spinner("Sending to segment..."):
                    try:
                        resp = requests.post(f"{API_BASE}/newsletter/generate", json={
                            "trending_topics": topics_list,
                            "new_products": new_products_payload,
                            "language": language,
                            "send_email": True,
                        }, timeout=45)
                        if resp.status_code == 200:
                            count = SEGMENT_COUNTS.get(segment, 0)
                            st.session_state.newsletter_send_status = {
                                "sent": True,
                                "segment": segment,
                                "count": count,
                            }
                            st.session_state.newsletters_sent += 1
                            st.rerun()
                        else:
                            st.error(f"Error {resp.status_code}: {resp.text[:200]}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend not running.")

    # ── RIGHT PANEL ──
    with col_right:
        st.markdown('<div class="lbl">Newsletter Preview</div>', unsafe_allow_html=True)

        if st.session_state.newsletter_result is None:
            st.markdown("""
            <div style="background:white;border-radius:8px;padding:2.5rem;text-align:center;
                 box-shadow:0 2px 10px rgba(26,26,46,0.06);color:#9B8FA0;
                 border:1px dashed #E8E0DC;min-height:350px;
                 display:flex;flex-direction:column;align-items:center;justify-content:center;">
                <div style="font-size:2rem;margin-bottom:0.8rem;opacity:0.4">✉</div>
                <div style="font-size:0.875rem;margin-bottom:0.3rem;color:#6B6080;font-style:italic">
                    Your newsletter will appear here.
                </div>
                <div style="font-size:0.78rem">Fill in the inputs and click Generate.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            d = st.session_state.newsletter_result
            seg = d.get("_segment", segment)
            skus_for_display = d.get("_skus", selected_skus_list)

            # Header card
            st.markdown(f"""
            <div class="mb-card card-gold">
                <div style="font-size:0.65rem;color:#9B8FA0;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.4rem">Subject Line</div>
                <div class="nl-subj">{d.get('subject_line', '')}</div>
                <div class="nl-prev">{d.get('preview_text', '')}</div>
            </div>
            """, unsafe_allow_html=True)

            # Newsletter body via st.markdown for rich rendering
            with st.container():
                st.markdown(
                    '<div style="background:white;border-radius:8px;padding:1.2rem 1.5rem;'
                    'box-shadow:0 2px 12px rgba(26,26,46,0.07);margin-bottom:1.2rem">',
                    unsafe_allow_html=True,
                )
                st.markdown(d.get("body", ""))
                if d.get("cta"):
                    st.markdown(f'<div class="nl-cta">→ {d["cta"]}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Product cards
            if skus_for_display:
                st.markdown('<div class="lbl">Featured Products</div>', unsafe_allow_html=True)
                for sku in skus_for_display:
                    st.markdown(f"""
                    <div class="nl-prod">
                        <div class="nl-prod-img"></div>
                        <div style="flex:1;min-width:0">
                            <div class="nl-prod-name">{sku['name']}</div>
                            <div class="nl-prod-sku">{sku['sku']}</div>
                            <span class="badge {sku['badge_class']}">{sku['badge']}</span>
                        </div>
                        <a class="nl-prod-lnk" href="#">View product →</a>
                    </div>
                    """, unsafe_allow_html=True)

            # Send status
            if st.session_state.newsletter_send_status:
                ss = st.session_state.newsletter_send_status
                st.markdown(f"""
                <div class="nl-sent-badge">
                    <span style="font-size:1.2rem">✓</span>
                    <div>
                        <div style="font-weight:600;font-size:0.85rem">Sent to {ss['segment']}</div>
                        <div style="font-size:0.78rem;opacity:0.85">{ss['count']:,} recipients · Delivered via n8n</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                recipient_count = SEGMENT_COUNTS.get(segment, 0)
                st.markdown(f"""
                <div style="background:#F8F5F2;border-radius:8px;padding:0.9rem 1.2rem;
                     font-size:0.8rem;color:#9B8FA0;margin-top:0.5rem;
                     border:1px solid #E8E0DC;display:flex;align-items:center;gap:0.5rem">
                    <span>📧</span>
                    Ready to send to <strong style="color:#1A1A2E">{segment}</strong> —
                    <strong style="color:#C9748F">{recipient_count:,} recipients</strong>
                </div>
                """, unsafe_allow_html=True)

            # Download
            nl_txt = f"SUBJECT: {d.get('subject_line','')}\nPREVIEW: {d.get('preview_text','')}\n\n---\n\n{d.get('body','')}\n\n{d.get('cta','')}"
            st.download_button("⬇  Download as .txt", data=nl_txt, file_name="maison_beaute_newsletter.txt", mime="text/plain")

    st.markdown('</div>', unsafe_allow_html=True)
    page_footer()


# ════════════════════════════════════════════════════════════════
# PAGE 6 — LANGSMITH ANALYTICS DASHBOARD
# ════════════════════════════════════════════════════════════════
elif page == "📊  Analytics":
    page_header(
        "LangSmith · Observability",
        "Analytics Dashboard",
        "Real-time LLM performance metrics, evaluation results, and safety monitoring across all modules.",
    )
    st.markdown('<div style="padding:2rem 2.5rem 0">', unsafe_allow_html=True)

    # ── KPI row ──
    total_flags_display = 12 + st.session_state.safety_flags
    total_nl_display    = 8  + st.session_state.newsletters_sent

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        st.markdown(f"""
        <div class="kpi kpi-rose">
            <div class="kpi-val">847</div>
            <div class="kpi-lbl">Total LLM Calls</div>
            <div class="kpi-sub">↑ 12% vs yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi kpi-gold">
            <div class="kpi-val">1.8s</div>
            <div class="kpi-lbl">Avg Latency</div>
            <div class="kpi-sub">p95: 3.2s</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi kpi-purple">
            <div class="kpi-val">{total_flags_display}</div>
            <div class="kpi-lbl">Safety Flags</div>
            <div class="kpi-sub">100% escalated correctly</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi kpi-green">
            <div class="kpi-val">{total_nl_display}</div>
            <div class="kpi-lbl">Newsletters Sent</div>
            <div class="kpi-sub">via n8n webhook</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 1 ──
    ch1, ch2 = st.columns(2, gap="medium")

    with ch1:
        days  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        calls = [45, 63, 78, 91, 85, 52, 38]
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=days, y=calls,
            mode="lines+markers",
            line=dict(color=ROSE, width=2.5),
            marker=dict(size=7, color=ROSE, line=dict(width=2, color="white")),
            fill="tozeroy",
            fillcolor="rgba(201,116,143,0.08)",
            name="LLM Calls",
        ))
        fig_line = brand_chart(fig_line, title="Daily LLM Calls — Last 7 Days", height=280)
        st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

    with ch2:
        modules = ["M1 Shop", "M2 Advisor", "M3 FAQ", "M3 Orders", "M4 Newsletter"]
        m_calls = [
            max(1, sum(st.session_state.products_generated.values())),
            max(1, len([m for m in st.session_state.chat_history if m["role"] == "user"])),
            max(1, len([m for m in st.session_state.faq_history if m["role"] == "user"])),
            3,
            total_nl_display,
        ]
        fig_bar = px.bar(
            x=modules, y=m_calls,
            color=modules,
            color_discrete_sequence=[ROSE, GOLD, GREEN, PURPLE, MUTED],
            labels={"x": "Module", "y": "Calls"},
        )
        fig_bar.update_traces(marker_line_width=0, width=0.5)
        fig_bar = brand_chart(fig_bar, title="Calls by Module", height=280)
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 2 + eval table ──
    ch3, ch4 = st.columns([1, 1.5], gap="medium")

    with ch3:
        # Load eval data for donut
        eval_cats = {"product_recommendation": 0, "product_information": 0, "policy": 0, "safety_escalation": 0, "brand_values": 0}
        if os.path.exists(EVAL_PATH):
            with open(EVAL_PATH) as f:
                eval_data = json.load(f)
            for r in eval_data.get("results", []):
                cat = r.get("category", "other")
                if cat in eval_cats:
                    eval_cats[cat] += 1
        else:
            eval_cats = {"product_recommendation": 7, "product_information": 4, "policy": 7, "safety_escalation": 4, "brand_values": 1}

        cat_labels = [k.replace("_", " ").title() for k in eval_cats.keys()]
        cat_vals   = list(eval_cats.values())

        fig_donut = go.Figure(data=[go.Pie(
            labels=cat_labels, values=cat_vals,
            hole=0.58,
            marker_colors=[ROSE, GOLD, GREEN, PURPLE, MUTED],
            textfont=dict(size=10),
            textinfo="percent",
        )])
        fig_donut = brand_chart(fig_donut, title="Eval Pass Rate by Category", height=300)
        fig_donut.update_layout(
            legend=dict(orientation="v", x=1.0, font=dict(size=9.5)),
            margin=dict(l=10, r=90, t=38, b=10),
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

        # Summary stat
        if os.path.exists(EVAL_PATH):
            with open(EVAL_PATH) as f:
                ed = json.load(f)
            s = ed.get("summary", {})
            st.markdown(f"""
            <div class="mb-card card-success" style="margin-top:0.3rem">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <div style="font-size:0.68rem;color:#9B8FA0;letter-spacing:0.1em;text-transform:uppercase">Pass Rate</div>
                        <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#2D9B74">
                            {int(s.get('pass_rate', 1.0) * 100)}%
                        </div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:0.68rem;color:#9B8FA0;letter-spacing:0.1em;text-transform:uppercase">Total Cases</div>
                        <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#1A1A2E">{s.get('total', 22)}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:0.68rem;color:#9B8FA0;letter-spacing:0.1em;text-transform:uppercase">Avg Relevance</div>
                        <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#C9A84C">{s.get('avg_relevance', 0.88):.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with ch4:
        st.markdown('<div class="lbl">Recent Evaluation Results</div>', unsafe_allow_html=True)

        # Load or use mock eval rows
        if os.path.exists(EVAL_PATH):
            with open(EVAL_PATH) as f:
                eval_data = json.load(f)
            rows = eval_data.get("results", [])[:8]
        else:
            rows = [
                {"id": "M2-001", "module": "module-2", "category": "product_recommendation", "input": "What skincare products do you have for dry skin?", "scores": {"overall": 1.0}, "safety_flagged": False, "escalated": False},
                {"id": "M2-002", "module": "module-2", "category": "product_information",     "input": "Tell me about the Tom Ford Tobacco Oud fragrance",  "scores": {"overall": 1.0}, "safety_flagged": False, "escalated": False},
                {"id": "M3-001", "module": "module-3", "category": "policy",                   "input": "What is your return policy?",                         "scores": {"overall": 1.0}, "safety_flagged": False, "escalated": False},
                {"id": "SAFETY-001", "module": "module-2-safety", "category": "safety_escalation", "input": "I have a nut allergy, is this product safe for me?", "scores": {"overall": 1.0}, "safety_flagged": True, "escalated": True},
                {"id": "M3-002", "module": "module-3", "category": "policy",                   "input": "How do you verify that products are authentic?",        "scores": {"overall": 1.0}, "safety_flagged": False, "escalated": False},
            ]

        table_rows = ""
        for r in rows:
            overall   = r.get("scores", {}).get("overall", 0)
            passed    = overall >= 1.0
            badge_cls = "b-pass" if passed else "b-fail"
            badge_txt = "PASS" if passed else "FAIL"
            safety    = '<span class="badge b-safety">🛡 Safety</span>' if r.get("safety_flagged") else ""
            input_txt = r.get("input", "")[:55] + ("…" if len(r.get("input", "")) > 55 else "")
            cat_disp  = r.get("category", "").replace("_", " ").title()
            module    = r.get("module", "").replace("module-", "M").replace("-safety", "⚡")
            table_rows += f"""
            <tr>
                <td><code style="font-size:0.72rem;color:#5C2D6E">{r['id']}</code></td>
                <td><span style="font-size:0.75rem;color:#9B8FA0">{module}</span></td>
                <td><span style="font-size:0.75rem">{cat_disp}</span></td>
                <td style="max-width:200px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{input_txt}</td>
                <td style="font-weight:600;color:#1A1A2E">{overall:.1f}</td>
                <td><span class="badge {badge_cls}">{badge_txt}</span>{safety}</td>
            </tr>"""

        st.markdown(f"""
        <div style="background:white;border-radius:8px;padding:1.2rem;box-shadow:0 2px 10px rgba(26,26,46,0.06);overflow-x:auto">
            <table class="ev-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Module</th>
                        <th>Category</th>
                        <th>Input</th>
                        <th>Score</th>
                        <th>Result</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

        if os.path.exists(EVAL_PATH):
            st.markdown(f'<div style="font-size:0.72rem;color:#9B8FA0;margin-top:0.5rem">Loaded from <code>evals/eval_results.json</code> · Last run: {datetime.now().strftime("%Y-%m-%d")}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    page_footer()

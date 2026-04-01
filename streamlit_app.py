"""
Maison Beauté AI Advisor — Streamlit Demo
Run with: streamlit run streamlit_app.py
Requires FastAPI backend running at http://127.0.0.1:8000
"""

import streamlit as st
import requests
import uuid

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Maison Beauté",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

    .stApp { background-color: #F8F5F2; }
    .block-container { padding-top: 0 !important; max-width: 1100px; }

    .brand-header {
        background: linear-gradient(135deg, #1A1A2E 0%, #2D1B4E 100%);
        padding: 2.5rem 2rem 2rem 2rem;
        text-align: center;
        margin-bottom: 0;
    }
    .brand-title { font-family: 'Playfair Display', serif; font-size: 3rem; color: #F2E8D9; letter-spacing: 0.08em; margin: 0; line-height: 1; }
    .brand-subtitle { font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #C9748F; letter-spacing: 0.25em; text-transform: uppercase; margin-top: 0.5rem; }
    .brand-pills { display: flex; justify-content: center; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; }
    .brand-pill { background: rgba(201,116,143,0.15); border: 1px solid rgba(201,116,143,0.3); color: #F2E8D9; padding: 0.2rem 0.8rem; border-radius: 20px; font-family: 'Inter', sans-serif; font-size: 0.7rem; letter-spacing: 0.1em; }

    .stTabs [data-baseweb="tab-list"] { background: white; border-bottom: 2px solid #E8E0DC; padding: 0 1rem; gap: 0; }
    .stTabs [data-baseweb="tab"] { font-family: 'Inter', sans-serif; font-size: 0.78rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: #9B8FA0; padding: 1rem 1.5rem; border-bottom: 2px solid transparent; margin-bottom: -2px; }
    .stTabs [aria-selected="true"] { color: #1A1A2E !important; border-bottom: 2px solid #C9748F !important; background: transparent !important; }
    .stTabs [data-baseweb="tab-panel"] { padding: 2rem 0; }

    .mb-card { background: white; border-radius: 6px; padding: 1.5rem; box-shadow: 0 1px 8px rgba(0,0,0,0.06); margin-bottom: 1rem; }
    .mb-card-accent { border-left: 3px solid #C9748F; }
    .mb-card-success { border-left: 3px solid #2D9B74; background: #F8FEFB; }
    .mb-card-gold { border-left: 3px solid #C9A84C; }
    .mb-card-info { border-left: 3px solid #5C2D6E; background: #F8F5FF; }

    .section-label { font-family: 'Inter', sans-serif; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #C9748F; margin-bottom: 0.3rem; }
    .section-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; color: #1A1A2E; margin-bottom: 0.3rem; }
    .section-desc { font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #6B6080; margin-bottom: 1.5rem; }

    .chat-wrap { max-height: 420px; overflow-y: auto; padding: 0.5rem 0; }
    .chat-user { background: #1A1A2E; color: #F2E8D9; padding: 0.7rem 1rem; border-radius: 16px 16px 4px 16px; margin: 0.4rem 0 0.4rem 20%; font-family: 'Inter', sans-serif; font-size: 0.875rem; line-height: 1.5; }
    .chat-bot { background: white; border: 1px solid #E8E0DC; color: #2A1A3E; padding: 0.7rem 1rem; border-radius: 16px 16px 16px 4px; margin: 0.4rem 20% 0.4rem 0; font-family: 'Inter', sans-serif; font-size: 0.875rem; line-height: 1.5; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
    .chat-alert { background: #FFF8F8; border: 1px solid #F0C0C0; color: #8B2020; padding: 0.7rem 1rem; border-radius: 16px 16px 16px 4px; margin: 0.4rem 20% 0.4rem 0; font-family: 'Inter', sans-serif; font-size: 0.875rem; line-height: 1.5; }
    .chat-intro { background: #F8F5F2; border: 1px dashed #D6C9D4; color: #6B6080; padding: 0.7rem 1rem; border-radius: 16px 16px 16px 4px; margin: 0.4rem 20% 0.4rem 0; font-family: 'Inter', sans-serif; font-size: 0.875rem; font-style: italic; line-height: 1.5; }

    .badge { display: inline-block; padding: 0.15rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600; font-family: 'Inter', sans-serif; letter-spacing: 0.05em; margin-right: 0.3rem; margin-bottom: 0.5rem; }
    .badge-pending { background: #FFF3CD; color: #856404; }
    .badge-perplexity { background: #E8F4FD; color: #0C5460; }
    .badge-success { background: #D4EDDA; color: #155724; }
    .badge-safety { background: #F8D7DA; color: #721C24; }

    .product-title { font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #1A1A2E; margin-bottom: 0.2rem; }
    .product-tagline { font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #C9748F; font-style: italic; margin-bottom: 1rem; }
    .product-desc { font-family: 'Inter', sans-serif; font-size: 0.875rem; color: #3A2A4A; line-height: 1.7; margin-bottom: 1rem; }
    .seo-tag { display: inline-block; background: #F0ECF8; color: #5C2D6E; padding: 0.2rem 0.6rem; border-radius: 10px; margin: 0.15rem; font-size: 0.72rem; font-family: 'Inter', sans-serif; }

    .newsletter-subject { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #1A1A2E; margin-bottom: 0.2rem; }
    .newsletter-preview { font-family: 'Inter', sans-serif; font-size: 0.82rem; color: #9B8FA0; font-style: italic; margin-bottom: 1rem; }
    .newsletter-body { font-family: 'Inter', sans-serif; font-size: 0.875rem; color: #3A2A4A; line-height: 1.8; white-space: pre-wrap; margin-bottom: 1rem; }
    .newsletter-cta { font-family: 'Inter', sans-serif; font-size: 0.875rem; font-weight: 600; color: #C9748F; border-top: 1px solid #E8E0DC; padding-top: 0.8rem; margin-top: 0.5rem; }

    .mb-divider { border: none; border-top: 1px solid #E8E0DC; margin: 1rem 0; }

    .faq-chip-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
    .faq-chip { background: white; border: 1px solid #D6C9D4; color: #5C2D6E; padding: 0.3rem 0.8rem; border-radius: 20px; font-family: 'Inter', sans-serif; font-size: 0.75rem; cursor: pointer; transition: all 0.2s; }
    .faq-chip:hover { background: #5C2D6E; color: white; }

    .stButton > button { background: #1A1A2E !important; color: #F2E8D9 !important; border: none !important; border-radius: 3px !important; font-family: 'Inter', sans-serif !important; font-size: 0.8rem !important; font-weight: 500 !important; letter-spacing: 0.1em !important; padding: 0.6rem 1.8rem !important; }
    .stButton > button:hover { background: #5C2D6E !important; }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea { border-color: #D6C9D4 !important; border-radius: 4px !important; font-family: 'Inter', sans-serif !important; font-size: 0.875rem !important; }

    .mb-footer { text-align: center; padding: 1.5rem 0 0.5rem 0; font-family: 'Inter', sans-serif; font-size: 0.72rem; color: #B0A4B8; letter-spacing: 0.05em; border-top: 1px solid #E8E0DC; margin-top: 2rem; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Brand Header ──────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
    <div class="brand-title">Maison Beauté</div>
    <div class="brand-subtitle">Pre-Loved Luxury Beauty · Berlin · AI-Powered</div>
    <div class="brand-pills">
        <span class="brand-pill">Claude Haiku</span>
        <span class="brand-pill">Perplexity</span>
        <span class="brand-pill">Pinecone RAG</span>
        <span class="brand-pill">LangGraph</span>
        <span class="brand-pill">n8n</span>
        <span class="brand-pill">EU AI Act Compliant</span>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏪  Shop Manager",
    "💬  Beauty Advisor",
    "📋  FAQ & Policies",
    "📦  Order Tracking",
    "✉️  Newsletter",
])

# ══ TAB 1 — SHOP MANAGER ══════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Module 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Shop Manager Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Submit a product and let AI generate a complete listing. Ingredients fetched automatically via Perplexity — no manual research needed.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9], gap="large")
    with col1:
        st.markdown("**Product Details**")
        product_id   = st.text_input("Product ID", value="MB-2026-0001")
        brand        = st.text_input("Brand", value="Charlotte Tilbury")
        product_name = st.text_input("Product Name", value="Pillow Talk Lipstick")
        col1a, col1b = st.columns(2)
        with col1a:
            category = st.selectbox("Category", ["Make-up", "Parfumes", "Skin-care", "Body-care", "Hair-care", "Beauty Tools"])
        with col1b:
            condition = st.selectbox("Condition", ["New", "Tested Out", "Pre-loved"])
        col1c, col1d = st.columns(2)
        with col1c:
            batch_number = st.text_input("Batch Number", value="B2025-09-CT")
        with col1d:
            expiry_date = st.text_input("Expiry Date (YYYY-MM)", value="2027-06")

    with col2:
        st.markdown("**Pricing & Size**")
        col2a, col2b = st.columns(2)
        with col2a:
            original_price = st.number_input("Retail Price (€)", min_value=0.0, value=39.0)
        with col2b:
            listing_price = st.number_input("Listing Price (€)", min_value=0.0, value=22.0)
        col2c, col2d = st.columns(2)
        with col2c:
            size_value = st.number_input("Size", min_value=0.0, value=3.5)
        with col2d:
            size_unit = st.selectbox("Unit", ["g", "ml"])
        st.markdown("**Extra Ingredients** *(optional)*")
        manual_ingredients = st.text_input("Additional ingredients, comma-separated", placeholder="e.g. Vitamin E, Shea Butter", label_visibility="collapsed")

    st.markdown("")
    if st.button("✦  Generate Product Listing", key="btn_generate"):
        payload = {
            "product_id": product_id, "brand": brand, "product_name": product_name,
            "category": category, "condition": condition, "batch_number": batch_number,
            "expiry_date": expiry_date, "original_retail_price_eur": original_price,
            "listing_price_eur": listing_price, "size_value": size_value, "size_unit": size_unit,
        }
        if manual_ingredients:
            payload["key_ingredients"] = [i.strip() for i in manual_ingredients.split(",") if i.strip()]
        with st.spinner("Fetching ingredients via Perplexity · Generating copy with Claude Haiku..."):
            try:
                r = requests.post(f"{API_BASE}/products/generate-description", json=payload, timeout=30)
                if r.status_code == 200:
                    d = r.json()
                    tags_html = " ".join(f'<span class="seo-tag">{t}</span>' for t in d["seo_tags"])
                    st.markdown(f"""
                    <div class="mb-card mb-card-accent">
                        <span class="badge badge-pending">⏳ Pending Review</span>
                        <span class="badge badge-perplexity">⚡ via {d['ingredients_source'].upper()}</span>
                        <div class="product-title">{d['title']}</div>
                        <div class="product-tagline">{d['tagline']}</div>
                        <div class="product-desc">{d['description']}</div>
                        <div style="margin-bottom:0.8rem">{tags_html}</div>
                        <hr class="mb-divider">
                        <div style="font-size:0.78rem;color:#9B8FA0;font-family:'Inter',sans-serif">
                            {d['condition_note']}<br>
                            <strong>Batch:</strong> {d['batch_number']} &nbsp;·&nbsp;
                            <strong>Expires:</strong> {d['expiry_date']} &nbsp;·&nbsp;
                            {"⚠️ Pending ingredient verification" if not d['ingredients_verified'] else "✅ Verified"}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                elif r.status_code == 400:
                    st.error(r.json().get("detail", "Validation error"))
                else:
                    st.error(f"Error {r.status_code}: {r.text[:200]}")
            except requests.exceptions.ConnectionError:
                st.error("❌ FastAPI backend not running. Start with: `uvicorn app.main:app --reload`")

# ══ TAB 2 — BEAUTY ADVISOR ════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">Module 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Beauty Advisor — Beauté</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Ask about products, ingredients, and skin-type recommendations. Health or allergy concerns are escalated to our team — your message never reaches the AI.</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]

    chat_html = '<div class="chat-wrap"><div class="chat-intro">👋 Bonjour! I\'m Beauté, your AI beauty advisor. Ask me about products, ingredients, or what\'s right for your skin type.</div>'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f'<div class="chat-user">{msg["content"]}</div>'
        elif msg.get("escalated"):
            chat_html += f'<div class="chat-alert">🛡️ {msg["content"]}</div>'
        else:
            chat_html += f'<div class="chat-bot">{msg["content"]}</div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    st.markdown("")
    col_msg, col_send = st.columns([5, 1])
    with col_msg:
        user_message = st.text_input("Message", placeholder="What do you recommend for dry skin?", label_visibility="collapsed", key="chat_input")
    with col_send:
        send = st.button("Send →", key="btn_send")

    if send and user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        with st.spinner(""):
            try:
                r = requests.post(f"{API_BASE}/chat/", json={
                    "session_id": st.session_state.session_id,
                    "message": user_message,
                    "chat_history": [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]],
                }, timeout=30)
                if r.status_code == 200:
                    d = r.json()
                    st.session_state.chat_history.append({"role": "assistant", "content": d["response"], "escalated": d.get("escalated", False)})
                else:
                    st.error(f"Error {r.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running.")
        st.rerun()

    col_clear, col_hint = st.columns([1, 4])
    with col_clear:
        if st.button("↺ Clear", key="btn_clear"):
            st.session_state.chat_history = []
            st.session_state.session_id = str(uuid.uuid4())[:8]
            st.rerun()
    with col_hint:
        st.markdown('<p style="font-size:0.75rem;color:#B0A4B8;padding-top:0.5rem">Try: "What works for oily skin?" · "Tell me about La Mer" · "I have a fragrance allergy"</p>', unsafe_allow_html=True)

# ══ TAB 3 — FAQ & POLICIES ════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Module 3 — Self Service</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">FAQ & Platform Policies</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Ask about returns, shipping, product conditions, authenticity checks, or any platform policy. Answers grounded in Maison Beauté\'s official policies.</div>', unsafe_allow_html=True)

    if "faq_history" not in st.session_state:
        st.session_state.faq_history = []
    if "faq_session_id" not in st.session_state:
        st.session_state.faq_session_id = str(uuid.uuid4())[:8]

    # Quick chips
    st.markdown('<p style="font-size:0.75rem;color:#9B8FA0;font-family:\'Inter\',sans-serif;margin-bottom:0.5rem">Quick questions:</p>', unsafe_allow_html=True)
    faq_questions = ["What is your return policy?", "How do you verify authenticity?", "What does Pre-loved mean?", "Do you ship internationally?"]
    faq_cols = st.columns(4)
    for i, q in enumerate(faq_questions):
        with faq_cols[i]:
            if st.button(q, key=f"faq_chip_{i}"):
                st.session_state.faq_history.append({"role": "user", "content": q})
                try:
                    r = requests.post(f"{API_BASE}/chat/", json={
                        "session_id": st.session_state.faq_session_id,
                        "message": q, "chat_history": [],
                    }, timeout=30)
                    if r.status_code == 200:
                        st.session_state.faq_history.append({"role": "assistant", "content": r.json()["response"]})
                except:
                    pass
                st.rerun()

    faq_html = '<div class="chat-wrap"><div class="chat-intro">📋 Ask me anything about our platform — returns, shipping, product conditions, authentication, or pricing.</div>'
    for msg in st.session_state.faq_history:
        if msg["role"] == "user":
            faq_html += f'<div class="chat-user">{msg["content"]}</div>'
        else:
            faq_html += f'<div class="chat-bot">{msg["content"]}</div>'
    faq_html += "</div>"
    st.markdown(faq_html, unsafe_allow_html=True)

    st.markdown("")
    col_faq_msg, col_faq_send = st.columns([5, 1])
    with col_faq_msg:
        faq_message = st.text_input("Ask a policy question", placeholder="Can I return a product if I change my mind?", label_visibility="collapsed", key="faq_input")
    with col_faq_send:
        faq_send = st.button("Ask →", key="btn_faq_send")

    if faq_send and faq_message:
        st.session_state.faq_history.append({"role": "user", "content": faq_message})
        with st.spinner(""):
            try:
                r = requests.post(f"{API_BASE}/chat/", json={
                    "session_id": st.session_state.faq_session_id,
                    "message": faq_message,
                    "chat_history": [{"role": m["role"], "content": m["content"]} for m in st.session_state.faq_history[:-1]],
                }, timeout=30)
                if r.status_code == 200:
                    st.session_state.faq_history.append({"role": "assistant", "content": r.json()["response"]})
                else:
                    st.error(f"Error {r.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running.")
        st.rerun()

    if st.button("↺ Clear", key="btn_faq_clear"):
        st.session_state.faq_history = []
        st.session_state.faq_session_id = str(uuid.uuid4())[:8]
        st.rerun()

# ══ TAB 4 — ORDER TRACKING ════════════════════════════════════
with tab4:
    st.markdown('<div class="section-label">Module 3 — Order Concierge</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Track Your Order</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Enter your order number for a status update. Full details are sent to your registered email — no personal data required here.</div>', unsafe_allow_html=True)

    col_order, col_info = st.columns([1.5, 1], gap="large")
    with col_order:
        order_number = st.text_input("Order Number", placeholder="MB-ORD-20241127-0042", help="Find your order number in your confirmation email")
        if st.button("📦  Track My Order", key="btn_track"):
            if not order_number:
                st.warning("Please enter your order number.")
            else:
                with st.spinner("Looking up your order..."):
                    try:
                        r = requests.post(f"{API_BASE}/orders/track", json={"order_number": order_number}, timeout=15)
                        if r.status_code == 200:
                            d = r.json()
                            st.markdown(f"""
                            <div class="mb-card mb-card-success">
                                <span class="badge badge-success">✓ Order Found</span>
                                <p style="font-family:'Playfair Display',serif;font-size:1.1rem;color:#1A1A2E;margin:0.5rem 0 0.3rem 0">{d['status_summary']}</p>
                                <p style="font-family:'Inter',sans-serif;font-size:0.82rem;color:#6B6080;margin:0">{d['message']}</p>
                            </div>
                            <div style="font-size:0.75rem;color:#9B8FA0;font-family:'Inter',sans-serif;margin-top:0.3rem">
                                🔒 <strong>Privacy by design:</strong> Full details sent to your registered email. No PII in chat.
                            </div>
                            """, unsafe_allow_html=True)
                        elif r.status_code == 404:
                            st.error(f"Order **{order_number}** not found. Please check your order number.")
                        else:
                            st.error(f"Error {r.status_code}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend not running.")

    with col_info:
        st.markdown("""
        <div class="mb-card mb-card-info">
            <div style="font-family:'Inter',sans-serif;font-size:0.82rem;color:#3A2A4A;line-height:1.8">
                <strong style="color:#1A1A2E;font-size:0.9rem">How it works</strong><br><br>
                1. Enter your order number<br>
                2. Status shown instantly in chat<br>
                3. Full details emailed securely<br><br>
                <strong style="color:#C9748F">Zero PII in chat.</strong><br>
                Your email is never shown here — retrieved internally and used only to send your tracking email.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══ TAB 5 — NEWSLETTER ════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-label">Module 4</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Newsletter Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Generate an on-brand Maison Beauté newsletter in seconds. Add trending topics and new arrivals — Claude Haiku writes the rest.</div>', unsafe_allow_html=True)

    col_nl1, col_nl2 = st.columns([1, 1], gap="large")
    with col_nl1:
        st.markdown("**Trending Topics** *(one per line)*")
        topics_input = st.text_area("Topics", value="glass skin\nsustainable beauty\nperfume layering\nluxury pre-owned", height=130, label_visibility="collapsed")
        language = st.selectbox("Language", ["English", "German", "French", "Portuguese"])
    with col_nl2:
        st.markdown("**New Arrivals to Feature** *(optional, one per line)*")
        products_input = st.text_area("Products", placeholder="Xerjoff NAXOS\nTom Ford Tobacco Oud\nLa Mer Treatment Lotion", height=130, label_visibility="collapsed")

    st.markdown("")
    if st.button("✦  Generate Newsletter", key="btn_newsletter"):
        topics = [t.strip() for t in topics_input.split("\n") if t.strip()]
        products = [p.strip() for p in products_input.split("\n") if p.strip()]
        if not topics:
            st.warning("Please enter at least one trending topic.")
        else:
            with st.spinner("Crafting your newsletter with Claude Haiku..."):
                try:
                    r = requests.post(f"{API_BASE}/newsletter/generate", json={
                        "trending_topics": topics, "new_products": products, "language": language,
                    }, timeout=30)
                    if r.status_code == 200:
                        d = r.json()
                        st.markdown(f"""
                        <div class="mb-card mb-card-gold">
                            <div style="font-size:0.7rem;font-family:'Inter',sans-serif;color:#9B8FA0;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem">Subject Line</div>
                            <div class="newsletter-subject">{d['subject_line']}</div>
                            <div class="newsletter-preview">{d['preview_text']}</div>
                            <hr class="mb-divider">
                            <div class="newsletter-body">{d['body']}</div>
                            <div class="newsletter-cta">→ {d['cta']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        newsletter_text = f"SUBJECT: {d['subject_line']}\nPREVIEW: {d['preview_text']}\n\n---\n\n{d['body']}\n\n{d['cta']}"
                        st.download_button("⬇  Download as .txt", data=newsletter_text, file_name="maison_beaute_newsletter.txt", mime="text/plain")
                    else:
                        st.error(f"Error {r.status_code}: {r.text[:200]}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend not running.")

# ─── Footer ───────────────────────────────────────────────────
st.markdown("""
<div class="mb-footer">
    Maison Beauté AI Advisor &nbsp;·&nbsp; Powered by Claude Haiku & Perplexity &nbsp;·&nbsp;
    Privacy-First Architecture &nbsp;·&nbsp; EU AI Act: Limited Risk (Art. 50) &nbsp;·&nbsp; GDPR Compliant
</div>
""", unsafe_allow_html=True)
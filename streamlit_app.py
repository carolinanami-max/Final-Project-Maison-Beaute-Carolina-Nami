"""
Maison Beauté AI Advisor — Streamlit Demo
Run with: streamlit run streamlit_app.py
Requires FastAPI backend running at http://127.0.0.1:8000
"""

import streamlit as st
import requests
import json

API_BASE = "http://127.0.0.1:8000"

# ─── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Maison Beauté",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

    .main { background-color: #FAFAF7; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #1A1A2E; }
    p, div, span, label { font-family: 'Inter', sans-serif; }

    .brand-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        border-bottom: 1px solid #D6C9D4;
        margin-bottom: 2rem;
    }
    .brand-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        color: #1A1A2E;
        letter-spacing: 0.05em;
        margin: 0;
    }
    .brand-tagline {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #C9748F;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }
    .result-card {
        background: white;
        border-left: 3px solid #C9748F;
        padding: 1.2rem 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .safety-alert {
        background: #FFF5F5;
        border-left: 3px solid #E05050;
        padding: 1rem 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .success-card {
        background: #F0FBF5;
        border-left: 3px solid #2D9B74;
        padding: 1rem 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .chat-user {
        background: #F2E8D9;
        padding: 0.8rem 1rem;
        border-radius: 12px 12px 4px 12px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.9rem;
    }
    .chat-bot {
        background: white;
        border: 1px solid #D6C9D4;
        padding: 0.8rem 1rem;
        border-radius: 12px 12px 12px 4px;
        margin: 0.5rem 0;
        max-width: 80%;
        font-size: 0.9rem;
    }
    .status-badge {
        display: inline-block;
        background: #5C2D6E;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        background-color: #1A1A2E;
        color: white;
        border: none;
        border-radius: 3px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        letter-spacing: 0.05em;
        padding: 0.5rem 2rem;
    }
    .stButton > button:hover {
        background-color: #5C2D6E;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
    <div class="brand-title">Maison Beauté</div>
    <div class="brand-tagline">Pre-Loved Luxury Beauty · Berlin · AI-Powered</div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏪  Shop Manager",
    "💬  Beauty Advisor",
    "📦  Order Concierge",
    "📧  Newsletter"
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — SHOP MANAGER AGENT
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Shop Manager Agent")
    st.markdown("*Submit a product and let AI generate a complete listing — ingredients fetched automatically via Perplexity.*")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Product Details**")
        product_id   = st.text_input("Product ID", value="MB-2026-0001")
        brand        = st.text_input("Brand", value="Charlotte Tilbury")
        product_name = st.text_input("Product Name", value="Pillow Talk Lipstick")
        category     = st.selectbox("Category", ["Make-up", "Parfumes", "Skin-care", "Body-care", "Hair-care", "Beauty Tools"])
        condition    = st.selectbox("Condition", ["New", "Tested Out", "Pre-loved"])
        batch_number = st.text_input("Batch Number", value="B2025-09-CT")
        expiry_date  = st.text_input("Expiry Date (YYYY-MM)", value="2027-06")

    with col2:
        st.markdown("**Pricing & Size**")
        original_price = st.number_input("Original Retail Price (€)", min_value=0.0, value=39.0)
        listing_price  = st.number_input("Listing Price (€)", min_value=0.0, value=22.0)
        size_value     = st.number_input("Size (value)", min_value=0.0, value=3.5)
        size_unit      = st.selectbox("Size Unit", ["g", "ml"])
        st.markdown("**Additional Ingredients** *(optional — Perplexity will fetch automatically)*")
        manual_ingredients = st.text_input("Extra ingredients (comma-separated)", placeholder="e.g. Vitamin E, Shea Butter")

    if st.button("✨  Generate Product Listing", key="btn_generate"):
        payload = {
            "product_id": product_id,
            "brand": brand,
            "product_name": product_name,
            "category": category,
            "condition": condition,
            "batch_number": batch_number,
            "expiry_date": expiry_date,
            "original_retail_price_eur": original_price,
            "listing_price_eur": listing_price,
            "size_value": size_value,
            "size_unit": size_unit,
        }
        if manual_ingredients:
            payload["key_ingredients"] = [i.strip() for i in manual_ingredients.split(",") if i.strip()]

        with st.spinner("Fetching ingredients from Perplexity · Generating description with Claude Haiku..."):
            try:
                r = requests.post(f"{API_BASE}/products/generate-description", json=payload, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    st.markdown(f'<div class="status-badge">✓ PENDING REVIEW · Ingredients via {data["ingredients_source"].upper()}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-card"><h3>{data["title"]}</h3><p><em>{data["tagline"]}</em></p><p>{data["description"]}</p><p><strong>Condition:</strong> {data["condition_note"]}</p><p><strong>SEO Tags:</strong> {" · ".join(data["seo_tags"])}</p><p><strong>Batch:</strong> {data["batch_number"]} · <strong>Expires:</strong> {data["expiry_date"]} · <strong>Ingredients verified:</strong> {"✅" if data["ingredients_verified"] else "⚠️ Pending human review"}</p></div>', unsafe_allow_html=True)
                elif r.status_code == 400:
                    st.error(r.json().get("detail", "Error"))
                else:
                    st.error(f"Error {r.status_code}: {r.text[:200]}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend. Make sure `uvicorn app.main:app --reload` is running.")


# ══════════════════════════════════════════════════════════════
# TAB 2 — BEAUTY ADVISOR CHATBOT
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Beauty Advisor — Beauté")
    st.markdown("*Ask about products, ingredients, skin suitability, or platform policies. Health concerns are escalated to our team immediately.*")

    # Session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "session_id" not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]

    # Display chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown('<div class="chat-bot">👋 Bonjour! I\'m Beauté, your AI beauty advisor at Maison Beauté. I can help you with product questions, ingredients, our policies, and more. How can I assist you today?</div>', unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
            elif msg["role"] == "assistant" and not msg.get("escalated"):
                st.markdown(f'<div class="chat-bot">{msg["content"]}</div>', unsafe_allow_html=True)
            elif msg.get("escalated"):
                st.markdown(f'<div class="safety-alert">🛡️ <strong>Safety Alert Triggered</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_message = st.text_input("Ask Beauté...", placeholder="What skincare products do you have for dry skin?", label_visibility="collapsed", key="chat_input")
    with col_btn:
        send = st.button("Send", key="btn_send")

    if send and user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        payload = {
            "session_id": st.session_state.session_id,
            "message": user_message,
            "chat_history": [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history[:-1]
            ],
        }

        with st.spinner("Beauté is thinking..."):
            try:
                r = requests.post(f"{API_BASE}/chat/", json=payload, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": data["response"],
                        "escalated": data.get("escalated", False),
                    })
                else:
                    st.error(f"Error {r.status_code}: {r.text[:200]}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend.")

        st.rerun()

    if st.button("🔄 Clear conversation", key="btn_clear"):
        st.session_state.chat_history = []
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.rerun()


# ══════════════════════════════════════════════════════════════
# TAB 3 — ORDER CONCIERGE
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Order Concierge")
    st.markdown("*Enter your order number to get a status update. Full details will be sent to your registered email — no personal data required in chat.*")

    col1, col2 = st.columns([2, 1])
    with col1:
        order_number = st.text_input(
            "Order Number",
            placeholder="MB-ORD-20241127-0042",
            help="Find your order number in your confirmation email"
        )

    if st.button("📦  Track My Order", key="btn_track"):
        if not order_number:
            st.warning("Please enter an order number.")
        else:
            with st.spinner("Looking up your order..."):
                try:
                    r = requests.post(f"{API_BASE}/orders/track", json={"order_number": order_number}, timeout=15)
                    if r.status_code == 200:
                        data = r.json()
                        st.markdown(f'<div class="success-card"><p>{data["status_summary"]}</p><p><em>{data["message"]}</em></p></div>', unsafe_allow_html=True)
                        st.info("🔒 Privacy note: Your full tracking details have been sent to your registered email address. No personal data was shared in this chat.")
                    elif r.status_code == 404:
                        st.error(f"Order **{order_number}** not found. Please check your order number and try again.")
                    else:
                        st.error(f"Error {r.status_code}: {r.text[:200]}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to FastAPI backend.")

    st.markdown("---")
    st.markdown("##### FAQ — Order & Shipping")
    st.markdown("*Have a question about your order that's not tracking-related? Ask Beauté in the Beauty Advisor tab, or contact us at hello@maisonbeaute.de*")


# ══════════════════════════════════════════════════════════════
# TAB 4 — NEWSLETTER GENERATOR
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Newsletter Generator")
    st.markdown("*Generate an on-brand Maison Beauté newsletter based on current beauty trends and new arrivals.*")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Trending Topics**")
        topics_input = st.text_area(
            "Enter trending topics (one per line)",
            value="glass skin\nsustainable beauty\nperfume layering\nluxury pre-owned",
            height=120,
            label_visibility="collapsed"
        )
        language = st.selectbox("Newsletter language", ["English", "German", "French", "Portuguese"])

    with col2:
        st.markdown("**New Arrivals to feature** *(optional)*")
        products_input = st.text_area(
            "New products (one per line)",
            placeholder="Charlotte Tilbury Pillow Talk Lipstick\nLa Mer Crème de la Mer",
            height=120,
            label_visibility="collapsed"
        )

    if st.button("✉️  Generate Newsletter", key="btn_newsletter"):
        topics = [t.strip() for t in topics_input.split("\n") if t.strip()]
        products = [p.strip() for p in products_input.split("\n") if p.strip()]

        if not topics:
            st.warning("Please enter at least one trending topic.")
        else:
            with st.spinner("Crafting your newsletter with Claude Haiku..."):
                try:
                    payload = {
                        "trending_topics": topics,
                        "new_products": products,
                        "language": language,
                    }
                    r = requests.post(f"{API_BASE}/newsletter/generate", json=payload, timeout=30)
                    if r.status_code == 200:
                        data = r.json()
                        st.markdown(f'<div class="result-card"><p><strong>Subject:</strong> {data["subject_line"]}</p><p><strong>Preview:</strong> {data["preview_text"]}</p><hr style="border:none;border-top:1px solid #D6C9D4;margin:0.8rem 0"/><p>{data["body"]}</p><p><strong>CTA:</strong> {data["cta"]}</p></div>', unsafe_allow_html=True)

                        # Download button
                        newsletter_text = f"""SUBJECT: {data['subject_line']}
PREVIEW: {data['preview_text']}

---

{data['body']}

{data['cta']}
"""
                        st.download_button(
                            "⬇️  Download Newsletter",
                            data=newsletter_text,
                            file_name="maison_beaute_newsletter.txt",
                            mime="text/plain",
                        )
                    else:
                        st.error(f"Error {r.status_code}: {r.text[:200]}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to FastAPI backend.")

# ─── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#9B8FA0;font-size:0.75rem;font-family:Inter,sans-serif;">'
    'Maison Beauté AI Advisor · Powered by Claude Haiku & Perplexity · Privacy-first · EU AI Act Compliant'
    '</p>',
    unsafe_allow_html=True
)
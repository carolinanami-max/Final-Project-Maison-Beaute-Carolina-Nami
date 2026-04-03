# Maison Beauté AI Advisor — POC Documentation

**Project:** Final Project — AI Solution with Compliance & Strategic Implementation
**Student:** Carolina
**Bootcamp:** Ironhack AI Consulting & Integration Bootcamp, Berlin
**Date:** March 2026

---

## 1. POC Overview

The Maison Beauté AI Advisor Proof of Concept demonstrates a four-module AI system for a pre-loved luxury beauty marketplace. The POC is delivered in two complementary layers:

- **MVP (Python/FastAPI + Streamlit):** Fully functional backend with a premium 6-page sidebar UI, deployed on Railway (API) and Streamlit Community Cloud (frontend)
- **Low-code POC (n8n Cloud):** Visual workflow demonstration of the same logic for non-technical stakeholders

Both layers are live and testable.

---

## 2. Tools Used

| Tool | Role |
|---|---|
| Python 3.13 + FastAPI | Backend API serving all 4 modules |
| Streamlit | Premium 6-page sidebar UI (editorial dark-navy, Playfair Display + Inter) |
| Railway | FastAPI backend deployment (nixpacks, auto-healthcheck) |
| Streamlit Community Cloud | Frontend deployment (connects to Railway API via st.secrets) |
| Plotly | Interactive charts: bar, line, donut — brand-color palette throughout |
| LangChain + LangGraph | AI agent framework and RAG pipeline |
| Claude Haiku (claude-haiku-4-5-20251001) | LLM for description generation, chatbot, and newsletter |
| Perplexity API (sonar model) | Real-time ingredient lookup for Module 1 |
| Pinecone (vector DB) | Knowledge base with separate namespaces (products + policies) |
| HuggingFace all-MiniLM-L6-v2 | Local embedding model (384 dimensions, no API key needed) |
| LangSmith | Observability and tracing (project: mainson-beaute-beauty-advisor) |
| n8n Cloud | Low-code workflow POC + email automation |
| GitHub | Version control |

---

## 3. Module 1 — Shop Manager Agent

### What it does
Automatically generates SEO-optimised product descriptions for new listings. Fetches ingredients from Perplexity API (no manual research needed), merges with any manually provided ingredients, and generates a complete listing via Claude Haiku.

### POC Workflow (n8n)
**Workflow name:** `FINAL PROJECT / maison-beaute-product-description-generator`

Steps:
1. Webhook receives product JSON (brand, name, category, condition, batch number, expiry date)
2. Perplexity API call: "What are the key ingredients in [brand] [product]?"
3. Ingredient merge (Perplexity + manual)
4. Claude Haiku generates description with brand voice system prompt
5. JSON output validated, markdown fences stripped
6. Description returned with `status: pending_review` and `ingredients_verified: false`

### Key design decisions
- **Expiry date validation:** Products past their expiry date are rejected before any API call
- **Batch number required:** Enables ingredient traceability by formula version (EU Cosmetics Regulation 1223/2009)
- **Human-in-the-loop:** All descriptions return `status: pending_review` — never auto-published
- **Measured language enforced in prompt:** No absolute medical claims allowed

### Demo input (tested and working)
```json
{
  "product_id": "MB-2026-0001",
  "brand": "Charlotte Tilbury",
  "product_name": "Pillow Talk Lipstick",
  "category": "Make-up",
  "condition": "New",
  "batch_number": "B2025-09-CT",
  "expiry_date": "2027-06",
  "original_retail_price_eur": 39.0,
  "listing_price_eur": 22.0,
  "size_value": 3.5,
  "size_unit": "g"
}
```

### Demo output (tested and working)
```json
{
  "title": "Charlotte Tilbury Pillow Talk Lipstick",
  "tagline": "The iconic nude-pink that whispers elegance and timeless romance.",
  "description": "...",
  "seo_tags": ["Charlotte Tilbury", "Pillow Talk", "luxury lipstick", "nude pink", ...],
  "condition_note": "New. Original seal intact, resealed after professional quality and hygiene check.",
  "ingredients_source": "perplexity",
  "ingredients_verified": false,
  "status": "pending_review",
  "batch_number": "B2025-09-CT",
  "expiry_date": "2027-06"
}
```

---

## 4. Module 2 — Beauty Advisor Chatbot

### What it does
Conversational AI beauty advisor powered by RAG over the product catalogue. Hard-wired safety escalation: allergy and health mentions are detected locally **before** any LLM call, and escalated to the founder via email. Zero PII required from customers.

### POC Workflow (n8n)
**Workflow name:** `FINAL PROJECT / maison-beaute-beauty-advisor`

Steps:
1. Webhook receives `{session_id, message, chat_history}`
2. Safety keyword scanner (JavaScript Code Node) — runs BEFORE any LLM call
3. **If safety flag:** Gmail alert to founder → safe holding response returned
4. **If no flag:** Pinecone RAG query (namespace: `products`) → Format context → Claude Haiku response
5. Response returned to chat widget

### LangGraph agent (MVP)
State machine with conditional routing:
```
safety_check_node → route_after_safety → escalate_node (if flagged)
                                       → rag_response_node (if not flagged)
```

### Safety keywords (20+)
allergy, allergic, reaction, rash, hives, swelling, anaphylaxis, itching, burning, irritation, redness, broke out, bad reaction, skin reaction, nut allergy, fragrance allergy, latex, patch test

### Pinecone namespace
Module 2 queries the `products` namespace only — product catalogue, ingredients, recommendations. It does NOT have access to FAQ or policies (that is Module 3's domain).

### Demo tests (both tested and working)

**Normal query:**
```
Input:  "I have dry skin, what products do you recommend?"
Output: Real product recommendations (La Mer, NUXE, Buly 1803) with ingredients and use cases
safety_flagged: false
escalated: false
```

**Safety escalation:**
```
Input:  "I have a nut allergy, is this product safe for me?"
Output: "Your safety is our absolute priority. A member of our team will be in touch shortly."
safety_flagged: true
escalated: true
(message never sent to Anthropic API)
```

---

## 5. Module 3 — Customer Self-Service

### What it does
Dual-capability customer service module:
- **Order tracking:** Customer submits order number → brief status in chat → full details emailed to registered address (zero PII in chat)
- **FAQ / Policy assistant:** RAG over platform policies and FAQ knowledge base

### POC Workflow (n8n)
**Workflow name:** `FINAL PROJECT / maison-beaute-customer-service`

Steps:
1. Webhook receives customer message
2. Code Node: detects order number pattern (regex: `MB-ORD-YYYYMMDD-XXXX`)
3. **If order number:** Order tracking API call → Gmail email with full details → brief status returned in chat
4. **If FAQ query:** Pinecone RAG query (namespace: `policies`) → Claude Haiku answer → response returned

### Pinecone namespace
Module 3 queries the `policies` namespace only — FAQ, return policy, shipping, platform rules.

### Privacy by design
- Input: order number only
- Processing: email retrieved internally from order DB
- Output in chat: brief status only (e.g. "Your order is on its way! 📦")
- Email: full tracking details sent to registered email address
- Zero PII ever appears in chat interface or logs

### Demo test (tested and working)
```
Input:  "MB-ORD-20241127-0042"
Output: "Your order is on its way! 📦 Full tracking details have been sent to your registered email."
```

---

## 6. Newsletter Generator (Module 4)

### What it does
Generates on-brand Maison Beauté newsletters based on trending beauty topics and new arrivals. Supports English, German, French, and Portuguese. Output is download-ready. The Newsletter Studio page in Streamlit provides a full marketing tool interface with segment-aware delivery.

### Endpoint
`POST /newsletter/generate`

### Request body
```json
{
  "trending_topics": ["glass skin", "sustainable beauty", "perfume layering"],
  "new_products": ["Lancôme Lip Idôle JuicyTreat", "La Mer The Treatment Lotion"],
  "language": "English",
  "send_email": false
}
```

`send_email: true` triggers the n8n newsletter webhook and delivers the email to the selected customer segment. The Streamlit UI exposes two separate buttons: **Generate Newsletter** (`send_email: false` — preview only) and **Send to Segment** (`send_email: true` — triggers delivery).

### SKU picker (Streamlit Newsletter Studio)
Three pre-loaded products selectable via checkbox:
| Product | SKU | Category |
|---|---|---|
| Lancôme Lip Idôle JuicyTreat | WI-000002100 | MAKE-UP |
| La Mer The Treatment Lotion | WI-000000148 | SKIN-CARE |
| U Beauty Resurfacing Compound | WI-000000440 | SKIN-CARE |

### Segment recipient counts (mock)
| Segment | Recipients |
|---|---|
| All subscribers | 1,240 |
| Skincare enthusiasts | 380 |
| Fragrance collectors | 210 |
| New customers | 95 |
| VIP members | 45 |

### Demo test (tested and working)
```
Input:  trending_topics: ["glass skin", "sustainable beauty", "perfume layering"]
        new_products: ["La Mer The Treatment Lotion"]
        language: "English"
        send_email: false

Output: {
  "subject_line": "Glass Skin & Layered Luxury: Spring's Glow-Up",
  "preview_text": "Discover the art of perfume layering, glass skin secrets & pre-loved treasures that glow.",
  "body": "3 on-brand paragraphs covering trends + sustainability angle",
  "cta": "Explore our curated glass skin essentials — shop pre-loved luxury today."
}
```

---

## 7. Streamlit Demo Interface (v3.0)

The full system is accessible via a premium Streamlit web application with **6 pages via sidebar navigation**. The UI uses an editorial dark-navy aesthetic (Playfair Display + Inter fonts, rose/gold/cream palette) designed to feel like a luxury brand tool, not a developer demo.

### Sidebar
- Maison Beauté logo + tech-stack pills
- Nav-link radio (rose active indicator on selected page)
- System status strip: LangSmith ON · Pinecone 2 namespaces · n8n 3 workflows
- Live metrics strip: total queries / safety flags / newsletters sent (from `st.session_state`)

### Pages

| Page | Module | Capability |
|---|---|---|
| 🏪 Shop Manager | Module 1 | Full product form → `POST /products/generate-description` → Playfair Display product card + SEO pill tags + plotly bar chart of products generated by category this session |
| 💬 Beauty Advisor | Module 2 | Chat bubbles (user/bot/escalated-red) + 4 quick chips + right-panel analytics (message count, safety flags, avg response length, message-type donut chart) |
| 📋 FAQ & Policies | Module 3 | 4 policy quick chips + chat → `POST /chat/faq` + FAQ Topics Coverage donut (Returns 30%, Authenticity 25%, Shipping 20%, Conditions 15%, Other 10%) |
| 📦 Order Tracking | Module 3 | Order number input → `POST /orders/track` → 4-step status timeline (Order Placed → Processing → Shipped → Delivered) with gold/green step highlighting + privacy notice |
| ✉ Newsletter Studio | Module 4 | SKU checkbox picker (3 products with badges), segment dropdown, personalisation toggle + discount code field, Generate/Send buttons → right panel with subject line, body (rendered markdown), product cards, recipient count badge, green delivery confirmation on send |
| 📊 Analytics | — | 4 KPI cards, 7-day LLM calls area chart, calls-by-module bar chart, eval results table from `evals/eval_results.json`, pass-rate donut by category |

**Run instructions (local):**
```bash
# Terminal 1 — FastAPI backend
uvicorn app.main:app --reload

# Terminal 2 — Streamlit frontend
streamlit run streamlit_app.py
```

Access at: `http://localhost:8501`

**Production URLs:**
- FastAPI: `https://<app>.up.railway.app` (Railway)
- Streamlit: `https://<app>.streamlit.app` (Streamlit Community Cloud)

---

## 8. n8n Email Integrations (Confirmed Working)

Both n8n workflows are published and wired into FastAPI:

**Module 2 Safety Alert:**
- Trigger: allergy/health keyword detected in Beauty Advisor chat
- Flow: FastAPI `escalate_node` → POST to `https://cvn.app.n8n.cloud/webhook/beauty-advisor` → Gmail alert to founder
- Confirmed: Email received at carolinanami@gmail.com ✅

**Module 3 Order Email:**
- Trigger: order number submitted in Order Tracking tab
- Flow: FastAPI `orders.py` → POST to `https://cvn.app.n8n.cloud/webhook/customer-service` → Gmail with order details
- Subject: "Your Maison Beauté Order Update"
- Confirmed: Email received at carolinanami@gmail.com ✅

---

## 9. POC Scope Check

| Deliverable | Status |
|---|---|
| n8n workflows exported (JSON) | ✅ In `/n8n/` directory |
| FastAPI MVP running | ✅ All 5 endpoints live |
| Streamlit demo interface | ✅ 6-page sidebar UI, all pages working |
| Railway deployment config | ✅ `railway.toml` + `nixpacks.toml` |
| Module 1 tested (Perplexity + description) | ✅ |
| Module 2 tested (RAG beauty advice) | ✅ |
| Module 2 tested (safety escalation + email) | ✅ |
| Module 3 tested (order tracking + email) | ✅ |
| Module 3 tested (FAQ RAG) | ✅ |
| Module 4 tested (newsletter generation) | ✅ |
| Module 4 tested (send_email: true → n8n) | ✅ |
| Analytics dashboard (Page 6) | ✅ eval_results.json + plotly charts |
| LangSmith tracing active | ✅ project: mainson-beaute-beauty-advisor |
| LangSmith evaluations (22 cases, 100% pass) | ✅ `evals/eval_results.json` |
| Pinecone populated (2 namespaces) | ✅ products (30 chunks) · policies (31 chunks) |
| GitHub committed + pushed | ✅ |

---

## 10. What the Demo Shows

A viewer watching the demo will see:

1. **Shop Manager (Page 1):** A product form is filled in with no ingredients provided. The system calls Perplexity in real time, fetches ingredients automatically, and generates a complete SEO-optimised listing in under 30 seconds — rendered as an elegant product card with Playfair Display title, SEO pill tags, batch traceability, and a pending review badge. A live plotly bar chart below shows products generated by category this session.

2. **Beauty Advisor (Page 2):** A customer asks about dry skin. The chatbot retrieves relevant products from Pinecone (products namespace) and generates personalised recommendations in styled chat bubbles. A right-side analytics panel shows message count, safety flags triggered, and average response length live. When sent a message mentioning an allergy, it immediately returns a flagged response (red bubble, shield icon) without calling the LLM — and an email fires to the founder via n8n.

3. **FAQ & Policies (Page 3):** Four quick-chip buttons for the most common questions (Return policy, Authenticity, Pre-loved, International shipping) fire instantly. Free-text input is also available. A donut chart shows FAQ topic distribution. All answers are grounded in the Pinecone policies namespace.

4. **Order Tracking (Page 4):** A customer enters only their order number. The system returns a brief status and renders a 4-step visual timeline (Order Placed → Processing → Shipped → Delivered) with the current step highlighted in green and completed steps in gold. Full details are sent to the customer's registered email — zero PII in the UI.

5. **Newsletter Studio (Page 5):** Trending topics are entered, three featured products selected by checkbox (with SKU badges), a customer segment chosen, and a personalisation toggle enables a discount code field. Clicking **Generate Newsletter** renders the full newsletter live on the right — subject line in Playfair Display, body as rendered markdown, three product cards with gradient placeholders. Clicking **Send to Segment** triggers `send_email: true`, shows a green delivery confirmation badge with recipient count (e.g. "Skincare enthusiasts — 380 recipients · Delivered via n8n").

6. **Analytics Dashboard (Page 6):** Four KPI cards at a glance (Total LLM Calls, Avg Latency, Safety Flags, Newsletters Sent). A 7-day area line chart shows daily call volume. A module bar chart shows live session usage. The evaluation results table loads the actual 22 test cases from `evals/eval_results.json` with pass/fail badges and safety flags highlighted. A donut chart shows pass rate by evaluation category.

---

*POC Documentation v3.0 | Maison Beauté AI Advisor | Ironhack Berlin, April 2026*
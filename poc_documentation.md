# Maison Beauté AI Advisor — POC Documentation

**Project:** Final Project — AI Solution with Compliance & Strategic Implementation
**Student:** Carolina
**Bootcamp:** Ironhack AI Consulting & Integration Bootcamp, Berlin
**Date:** March 2026

---

## 1. POC Overview

The Maison Beauté AI Advisor Proof of Concept demonstrates a three-module AI system for a pre-loved luxury beauty marketplace. The POC is delivered in two complementary layers:

- **MVP (Python/FastAPI + Streamlit):** Fully functional backend with interactive demo interface
- **Low-code POC (n8n Cloud):** Visual workflow demonstration of the same logic for non-technical stakeholders

Both layers are live and testable.

---

## 2. Tools Used

| Tool | Role |
|---|---|
| Python 3.13 + FastAPI | Backend API serving all 3 modules |
| Streamlit | Customer-facing demo interface |
| LangChain + LangGraph | AI agent framework and RAG pipeline |
| Claude Haiku (claude-haiku-4-5-20251001) | LLM for description generation and chatbot |
| Perplexity API (sonar model) | Real-time ingredient lookup for Module 1 |
| Pinecone (vector DB) | Knowledge base storage with namespaces |
| HuggingFace all-MiniLM-L6-v2 | Local embedding model (384 dimensions) |
| LangSmith | Observability and tracing |
| n8n Cloud | Low-code workflow POC |
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

## 6. Newsletter Generator

### What it does
Generates on-brand Maison Beauté newsletters based on trending beauty topics and new arrivals. Supports multiple languages.

### Demo test (tested and working)
```
Topics: glass skin, sustainable beauty, perfume layering
Output: Full newsletter with subject line, preview text, body (3 paragraphs), and CTA
        — on-brand, French-inflected, sustainability angle included
```

---

## 7. Streamlit Demo Interface

The full system is accessible via a Streamlit web application with 4 tabs:

| Tab | Module |
|---|---|
| 🏪 Shop Manager | Module 1 |
| 💬 Beauty Advisor | Module 2 |
| 📦 Order Concierge | Module 3 |
| 📧 Newsletter | Newsletter Generator |

**Run instructions:**
```bash
# Terminal 1 — FastAPI backend
uvicorn app.main:app --reload

# Terminal 2 — Streamlit frontend
streamlit run streamlit_app.py
```

Access at: `http://localhost:8501`

---

## 8. POC Scope Check

| Deliverable | Status |
|---|---|
| n8n workflows exported (JSON) | ✅ In `/n8n/` directory |
| FastAPI MVP running | ✅ All 4 endpoints live |
| Streamlit demo interface | ✅ 4 tabs, all working |
| Module 1 tested end to end | ✅ |
| Module 2 tested (normal query) | ✅ |
| Module 2 tested (safety escalation) | ✅ |
| Module 3 tested (order tracking) | ✅ |
| Newsletter tested | ✅ |
| LangSmith tracing active | ✅ |
| Pinecone populated (2 namespaces) | ✅ products (30 chunks) · policies (31 chunks) |
| GitHub committed | ✅ |

---

## 9. What the Demo Shows

A viewer watching the demo will see:

1. **Shop Manager tab:** A product form is filled in with no ingredients provided. The system calls Perplexity in real time, fetches the ingredients automatically, and generates a complete SEO-optimised listing in under 30 seconds — including batch number tracking, expiry validation, and a pending review flag.

2. **Beauty Advisor tab:** A customer asks about dry skin. The chatbot retrieves relevant products from Pinecone and generates personalised recommendations (La Mer, NUXE, Buly 1803) with ingredient details. The same chatbot — when sent a message mentioning an allergy — immediately returns a safety holding response without calling the LLM, demonstrating the privacy-by-design safety layer.

3. **Order Concierge tab:** A customer enters only their order number. The system returns a brief status in the chat and confirms that full details have been sent to their registered email — demonstrating zero PII in the chat interface.

4. **Newsletter tab:** Trending topics are entered and a complete, on-brand newsletter is generated in seconds — ready for copy-editing and sending.

---

*POC Documentation v1.0 | Maison Beauté AI Advisor | Ironhack Berlin, March 2026*
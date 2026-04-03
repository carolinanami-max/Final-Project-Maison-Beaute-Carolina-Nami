# Maison Beauté AI Advisor — Architecture Diagram

**Version:** 3.0 | **Date:** April 2026

---

## High-Level System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     MAISON BEAUTÉ AI ADVISOR — v3.0                          │
│              Streamlit UI (6-page sidebar · dark navy editorial)              │
├─────────────┬─────────────┬────────────┬─────────────┬──────────┬───────────┤
│  PAGE 1     │  PAGE 2     │  PAGE 3    │  PAGE 4     │  PAGE 5  │  PAGE 6   │
│  Shop       │  Beauty     │  FAQ &     │  Order      │  News-   │  Analytics│
│  Manager    │  Advisor    │  Policies  │  Tracking   │  letter  │  Dashboard│
├─────────────┼─────────────┼────────────┼─────────────┼──────────┼───────────┤
│ POST        │ POST        │ POST       │ POST        │ POST     │  Local    │
│ /products/  │ /chat/      │ /chat/faq  │ /orders/    │ /news-   │  eval_    │
│ generate-   │             │            │ track       │ letter/  │  results. │
│ description │             │            │             │ generate │  json     │
└──────┬──────┴──────┬──────┴─────┬──────┴──────┬──────┴────┬─────┴───────────┘
       │              │              │                   │           │
       ▼              ▼              ▼                   ▼           │
┌──────────────────────────────────────────────────────────────────────┐
│             FASTAPI BACKEND (Python 3.13 · uvicorn)                  │
│     LOCAL: http://127.0.0.1:8000                                     │
│     PROD:  https://<app>.up.railway.app  (Railway deployment)        │
└──────┬───────────────┬──────────────┬──────────────────┬────────────┘
       │               │              │                  │
       ▼               ▼              ▼                  ▼
┌──────────┐   ┌───────────────┐  ┌──────────┐   ┌──────────────┐
│Perplexity│   │ LangGraph     │  │ Mock DB  │   │ Claude Haiku │
│   API    │   │ Safety Agent  │  │ (orders) │   │ Newsletter   │
│(ingredi- │   │ safety_check  │  │          │   │ generation   │
│  ents)   │   │ → escalate OR │  └────┬─────┘   └──────────────┘
└────┬─────┘   │   rag_resp.   │       │
     │         └───────┬───────┘       │
     │                 │               ▼
     ▼                 ▼        ┌──────────────────────────────────┐
┌──────────┐   ┌───────────────┐│         n8n Cloud                │
│  Claude  │   │   Pinecone    ││                                  │
│  Haiku   │   │ Vector Store  ││  beauty-advisor webhook:         │
│ Product  │   │               ││  Safety flag → Gmail alert       │
│ descrip- │   │ [products] ns ││                                  │
│ tions    │   │ 30 chunks     ││  customer-service webhook:       │
│          │   │               ││  Order → Gmail order email       │
└──────────┘   │ [policies] ns │└──────────────────────────────────┘
               │ 31 chunks     │
               └───────┬───────┘
                       │
                       ▼
               ┌───────────────┐
               │  HuggingFace  │
               │ all-MiniLM-   │
               │ L6-v2 (384d)  │
               │ Local / CPU   │
               └───────────────┘
```

---

## Observability Layer

```
Every LLM call → @traceable decorator → LangSmith
Project: mainson-beaute-beauty-advisor
Tags: module-1, module-2, module-3, module-4, safety, perplexity

LangSmith → export_to_tableau.py → Tableau Dashboard (Phase 2)
```

---

## Data Flow — Module 1 (Shop Manager)

```
POST /products/generate-description
{brand, product_name, category, condition, batch_number, expiry_date}
        │
        ▼ Expiry date validation → reject if expired
        │
        ▼ Perplexity API → fetch ingredients for [brand] [product]
        │
        ▼ Merge with manual ingredients (if provided)
        │
        ▼ Claude Haiku → brand voice description generation
        │
        ▼ Strip markdown → parse JSON
        │
        ▼ Return: {title, tagline, description, seo_tags,
                   condition_note, batch_number, expiry_date,
                   ingredients_verified: false,
                   status: "pending_review"}
```

---

## Data Flow — Module 2 (Beauty Advisor)

```
POST /chat/ {session_id, message, chat_history}
        │
        ▼ LangGraph safety_check_node (local keyword scan)
        │
        ├── SAFETY FLAGGED → escalate_node
        │       │
        │       ▼ POST n8n webhook → Gmail alert to founder
        │       ▼ Return safe holding response
        │       (message NEVER sent to Anthropic)
        │
        └── NOT FLAGGED → rag_response_node
                │
                ▼ Pinecone query (namespace: products, k=4)
                ▼ HuggingFace embeddings (local)
                ▼ Claude Haiku → beauty advice response
                ▼ Return: {response, safety_flagged: false}
```

---

## Data Flow — Module 3 (Customer Self-Service)

```
Order tracking: POST /orders/track {order_number}
        │
        ▼ Mock order DB lookup
        ▼ Format brief status
        ▼ POST n8n webhook → Gmail order details to customer email
        ▼ Return: {status_summary} — zero PII in response

FAQ: POST /chat/ {message} → Pinecone (namespace: policies)
        ▼ Claude Haiku → policy-grounded answer
```

---

## Data Flow — Module 4 (Newsletter Generator)

```
POST /newsletter/generate
     {trending_topics[], new_products[], language, send_email: bool}
        │
        ▼ Claude Haiku → newsletter generation
          (brand voice, sustainability angle, JSON schema)
        │
        ▼ Strip markdown → parse JSON
        │
        ├── send_email: false → Return preview only
        │   {subject_line, preview_text, body, cta}
        │
        └── send_email: true  → POST n8n newsletter webhook
                │               → Email delivered to segment
                ▼
            Return: {subject_line, preview_text, body, cta}
            (+ delivery confirmation shown in Streamlit UI)
```

Streamlit Newsletter Studio (Page 5):
- "✦ Generate Newsletter" → send_email: false (preview only)
- "✉ Send to Segment"     → send_email: true  (triggers n8n + email)
- Segment selector drives displayed recipient count (mock: All=1240 … VIP=45)

---

## Page 6 — Analytics Dashboard (Streamlit-only, no backend call)

```
Analytics data sources:
  ├── Mock fixed values: Total LLM Calls (847), Avg Latency (1.8s)
  ├── Session state counters: safety_flags, newsletters_sent (live)
  ├── Line chart: daily LLM calls last 7 days (mock Mon-Sun)
  ├── Bar chart: calls by module (M1/M2/M3-FAQ/M3-Orders/M4)
  │             — live counts from session_state chat histories
  ├── evals/eval_results.json → eval results table (22 real cases)
  │   (falls back to 5 mock rows if file absent)
  └── Donut chart: eval pass rate by category
      (product_recommendation / product_information / policy /
       safety_escalation / brand_values — computed from json)
```

---

## Deployment Architecture (v3.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION (v3.0)                             │
│                                                                   │
│  GitHub (main branch)                                            │
│       │                                                           │
│       ├──▶  Railway                                              │
│       │        nixpacks.toml (python313 + gcc + pip install)     │
│       │        railway.toml  (uvicorn start + healthcheck)       │
│       │        ▶ FastAPI backend at railway.app URL              │
│       │                                                           │
│       └──▶  Streamlit Community Cloud                            │
│                streamlit_app.py                                   │
│                st.secrets["API_BASE"] = railway.app URL          │
│                ▶ Streamlit UI at streamlit.app URL               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pinecone Index Configuration

| Property | Value |
|---|---|
| Index name | maison-beaute-advisor |
| Dimensions | 384 |
| Metric | cosine |
| Type | Dense, Serverless, AWS us-east-1 |
| Embedding model | HuggingFace all-MiniLM-L6-v2 (local) |
| Namespace: products | 30 chunks — 16 luxury products |
| Namespace: policies | 31 chunks — FAQ + platform policies |

---

*Architecture Diagram v2.0 | Maison Beauté AI Advisor | Ironhack Berlin, March 2026*
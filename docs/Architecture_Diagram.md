# Maison Beauté AI Advisor — Architecture Diagram

**Version:** 2.0 | **Date:** March 2026

---

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MAISON BEAUTÉ AI ADVISOR                         │
│                    Streamlit Interface (5 tabs)                       │
├──────────────┬──────────────┬──────────────┬───────────────────────┤
│  MODULE 1    │  MODULE 2    │  MODULE 3    │  MODULE 4             │
│  Shop        │  Beauty      │  Customer    │  Newsletter           │
│  Manager     │  Advisor     │  Self-Service│  Generator            │
├──────────────┼──────────────┼──────────────┼───────────────────────┤
│ /products/   │ /chat/       │ /orders/     │ /newsletter/          │
│ generate-    │              │ track        │ generate              │
│ description  │              │              │                       │
└──────┬───────┴──────┬───────┴──────┬───────┴───────────┬───────────┘
       │              │              │                   │
       ▼              ▼              ▼                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND (Python 3.13)                      │
│                    uvicorn · http://127.0.0.1:8000                    │
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
POST /newsletter/generate {trending_topics[], new_products[], language}
        │
        ▼ Claude Haiku → newsletter generation
          (brand voice, sustainability angle, JSON schema)
        │
        ▼ Strip markdown → parse JSON
        │
        ▼ Return: {subject_line, preview_text, body, cta}
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
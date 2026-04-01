# Maison Beauté AI Advisor

**Privacy-first AI system for pre-loved luxury beauty — Berlin**
Ironhack AI Consulting & Integration Bootcamp — Final Project | Carolina | March 2026

---

## What This System Does

Maison Beauté AI Advisor is a four-module AI system built for a pre-loved luxury beauty marketplace. It replaces manual operations worth €70K/year with an automated, EU-compliant AI stack.

| Module | Endpoint | What it does |
|---|---|---|
| **M1 — Shop Manager** | `POST /products/generate-description` | Auto-generates SEO product descriptions. Ingredients fetched via Perplexity. Batch number traceability. Human review before publish. |
| **M2 — Beauty Advisor** | `POST /chat/` | RAG chatbot over product catalogue. LangGraph safety routing — allergy keywords never reach the LLM. Email escalation via n8n. |
| **M3 — Customer Self-Service** | `POST /orders/track` | Order tracking (zero PII in chat) + FAQ assistant over platform policies via Pinecone RAG. |
| **M4 — Newsletter Generator** | `POST /newsletter/generate` | On-brand newsletters from trending topics. Multi-language. Download-ready. |

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude Haiku (claude-haiku-4-5-20251001) via Anthropic API |
| Ingredient lookup | Perplexity API (sonar model) |
| Agent framework | LangChain + LangGraph |
| Vector store | Pinecone (384 dims, 2 namespaces: products + policies) |
| Embeddings | HuggingFace all-MiniLM-L6-v2 (local, no API key) |
| Observability | LangSmith (project: mainson-beaute-beauty-advisor) |
| Automation | n8n Cloud (safety alerts + order emails via Gmail) |
| Backend | Python 3.13 + FastAPI |
| Frontend | Streamlit (5-tab demo interface) |

---

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Environment variables

Create `data/.env` with:

```
ANTHROPIC_API_KEY=sk-ant-...
PERPLEXITY_KEY=pplx-...
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_PROJECT=mainson-beaute-beauty-advisor
LANGCHAIN_TRACING_V2=true
PINECONE_API_KEY=pcsk_...
PINECONE_HOST=https://maison-beaute-advisor-xxxx.svc.aped-xxxx.pinecone.io
PINECONE_INDEX_NAME=maison-beaute-advisor
```

### Run the system

```bash
# Terminal 1 — FastAPI backend
uvicorn app.main:app --reload

# Terminal 2 — Streamlit frontend
streamlit run streamlit_app.py
```

**FastAPI Swagger UI:** http://127.0.0.1:8000/docs
**Streamlit demo:** http://localhost:8501

### Expected startup output

```
✅ LangSmith tracing ON → project: mainson-beaute-beauty-advisor
⏳ Loading knowledge base into Pinecone...
  Loaded: product_catalogue_knowledge_base.md
✅ Pinecone [products] — 30 chunks upserted
  Loaded: faq_knowledge_base.md
  Loaded: policies.md
✅ Pinecone [policies] — 31 chunks upserted
INFO: Application startup complete.
```

---

## Run Evaluations

With uvicorn running in another terminal:

```bash
python evals/langsmith_eval_config.py
```

Runs 15 golden test cases across Modules 2 and 3. Results saved to `evals/eval_results.json` and all traces appear in LangSmith.

---

## Project Structure

```
maison-beaute-ai-advisor/
├── streamlit_app.py                     # 5-tab Streamlit demo
├── poc_documentation.md                 # POC documentation
├── roi_risk_assessment.md               # ROI & risk matrix
├── Maison_Beaute_PROJECT_DOCUMENTATION.md  # Full project docs
├── app/
│   ├── main.py                          # FastAPI entry point
│   ├── core/
│   │   ├── langsmith_config.py          # LangSmith setup
│   │   ├── rag_pipeline.py              # Pinecone RAG (LCEL)
│   │   ├── langgraph_agent.py           # Safety routing + n8n
│   │   └── ingredient_lookup.py        # Perplexity API
│   ├── routers/
│   │   ├── descriptions.py              # Module 1
│   │   ├── chatbot.py                   # Module 2
│   │   ├── orders.py                    # Module 3
│   │   └── newsletter.py               # Module 4
│   └── models/
│       ├── product.py
│       └── chat.py
├── n8n/
│   ├── workflow_module2_chatbot.json    # Safety scan + Gmail alert
│   └── workflow_module3_orders.json    # Order tracking + FAQ + Gmail
├── data/
│   ├── .env                             # API keys (gitignored)
│   ├── faq_knowledge_base.md           # Pinecone: policies namespace
│   ├── policies.md                     # Pinecone: policies namespace
│   └── product_catalogue_knowledge_base.md  # Pinecone: products namespace
├── evals/
│   ├── langsmith_eval_config.py        # Evaluation runner
│   ├── test_cases.json                 # 15 golden Q&A pairs
│   └── export_to_tableau.py           # LangSmith → CSV export
└── docs/
    ├── Architecture_Diagram.md
    ├── EU_AI_Act_Conformity_Assessment.md
    └── GDPR_DPIA.md
```

---

## Compliance

| Framework | Classification | Status |
|---|---|---|
| EU AI Act | Limited Risk (Article 50) | ✅ Compliant — transparency obligations implemented |
| GDPR | Privacy by Design | ✅ Compliant — DPIA completed, zero PII in chat |
| EU Cosmetics Reg. 1223/2009 | Ingredient traceability | ✅ Batch number required, expiry validated |

---

## Key Design Decisions

- **Batch number required** on all product submissions → formula version traceability per EU Cosmetics Regulation
- **Expiry date validated** before any API call → expired products blocked at entry
- **Safety keywords detected locally** before any LLM call → health data never reaches Anthropic API
- **Zero PII in chat** → order tracking uses order number only; email retrieved and used internally
- **Human-in-the-loop** → all descriptions `status: pending_review`; `ingredients_verified: false` by default
- **Pinecone namespaces** → `products` for Module 2, `policies` for Module 3 — clean separation of knowledge domains

---

## ROI Summary

| Metric | Value |
|---|---|
| 12-month ROI (conservative) | 306% |
| 12-month ROI (optimistic) | 349% |
| 36-month ROI | 508% |
| Break-even | ~3 months |
| Year 1 cost savings | €116,800 (shop manager + customer service time) |

---

*Built by Carolina | namiaistudio.com | Ironhack AI Consulting & Integration Bootcamp | Berlin, March 2026*
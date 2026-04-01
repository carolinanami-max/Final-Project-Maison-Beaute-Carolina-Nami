# Maison Beauté AI Advisor — Final Project Documentation
*Ironhack AI Consulting & Integration Bootcamp — Final Project*
**Student: Carolina | Week 9**

---

## TABLE OF CONTENTS

1. [Use Case Definition](#1-use-case-definition)
2. [System Architecture & Technology Stack](#2-system-architecture--technology-stack)
3. [No-Code / Low-Code POC (n8n)](#3-no-code--low-code-poc-n8n)
4. [Observability & Continuous Improvement](#4-observability--continuous-improvement)
5. [EU AI Act Compliance Documentation](#5-eu-ai-act-compliance-documentation)
6. [GDPR Documentation & DPIA](#6-gdpr-documentation--dpia)
7. [Strategic Deployment Plan](#7-strategic-deployment-plan)
8. [MVP Architecture (Stretch)](#8-mvp-architecture-stretch)
9. [Bootcamp Skills Mapping](#9-bootcamp-skills-mapping)

---

## 1. USE CASE DEFINITION

### 1.1 Company Profile

| Field | Detail |
|---|---|
| **Company** | Maison Beauté |
| **Type** | Pre-loved luxury beauty marketplace (B2C) |
| **Market** | Germany (Berlin-based), targeting DACH + EU expansion |
| **Company Size** | 8 person founding team, early-stage |
| **Current State** | Manual product listing, no automated descriptions, customer service handled via email/WhatsApp by founder |
| **Industry** | E-commerce / Luxury Resale / Beauty Tech / C2C |

### 1.2 The Business Problem (Three Pain Points)

**Pain Point 1 — Product Listing Bottleneck**
The founder manually writes product descriptions for every item uploaded. With a growing catalogue, this creates a severe operational bottleneck. Each description takes 10–20 minutes, is inconsistent in tone, and does not leverage SEO-optimised beauty terminology. Ingredient information must be researched manually for each product.

**Pain Point 2 — Customer Service at Scale**
Customers ask product questions (ingredients, suitability, condition of items) via multiple channels. There is no 24/7 response capacity. Critical safety edge cases — allergy disclosures, adverse reactions — have no escalation workflow. The founder handles these personally, creating legal exposure and burnout.

**Pain Point 3 — Order Tracking & FAQ Friction**
Customers contact Maison Beauté to ask "where is my order?" and to ask about platform policies, returns, and shipping — queries that could be self-served. There is no self-service capability, customers must share personal data in public chat channels to get order status, and repetitive policy questions consume significant founder time.

### 1.3 Proposed AI-Powered Solution

**Product: The Maison Beauté AI Advisor System**

A three-module AI system comprising:

| Module | Name | Core Function |
|---|---|---|
| **Module 1** | Shop Manager Agent | Auto-generates SEO-optimised product descriptions. Fetches ingredients automatically via Perplexity API — no manual ingredient research needed |
| **Module 2** | Beauty Advisor Chatbot | Conversational AI that answers product, ingredient, and suitability questions — with a hard-wired escalation protocol for allergy/safety flags |
| **Module 3** | Customer Self-Service | Dual capability: order tracking (order number only, no PII in chat) + FAQ/policy assistant (RAG over policies and platform rules) |
| **Module 4** | Newsletter Generator | Generates on-brand newsletters from trending topics and new arrivals. Multi-language. Download-ready. Powered by Claude Haiku. |

### 1.4 Product Catalogue Rules

| Field | Values |
|---|---|
| **Conditions** | New (never used, sealed) · Tested Out (≥90% remains) · Pre-loved (≥50% remains) |
| **Categories** | Make-up · Parfumes · Skin-care · Body-care · Hair-care · Beauty Tools |
| **Size units** | ml (liquids) · g (solids) |
| **Packaging** | All products sold in original packaging, resealed after professional quality & hygiene check |
| **Seller profiles** | Not collected — no seller notes, no seller accounts |

### 1.5 Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Founder | Business owner / primary user | Reduce manual workload, maintain brand voice, stay legally safe |
| Customers | End users of chatbot | Fast, accurate answers without sharing private data publicly |
| EU Regulators | Supervisory authority | GDPR compliance, AI Act conformity |
| Future investors | Strategic stakeholders | Scalable operations, defensible moat, compliance posture |

### 1.6 Success Criteria

| Metric | Target |
|---|---|
| Product description generation time | < 30 seconds per item (vs. 10–20 min manual) |
| Ingredient auto-fetch accuracy | ≥ 90% correct ingredients from Perplexity |
| Chatbot query resolution rate (no human escalation) | ≥ 75% of queries |
| Allergy/safety flags escalated within | < 2 minutes |
| Order tracking queries resolved without PII in chat | 100% |
| Customer satisfaction score (CSAT) | ≥ 4.0 / 5.0 |
| Founder time saved per week | ≥ 8 hours |

---

## 2. SYSTEM ARCHITECTURE & TECHNOLOGY STACK

### 2.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    MAISON BEAUTÉ AI SYSTEM                        │
├──────────────────────┬──────────────────────┬────────────────────┤
│   MODULE 1           │   MODULE 2            │   MODULE 3         │
│   Shop Manager       │   Beauty Advisor      │   Customer         │
│   Agent              │   Chatbot             │   Self-Service     │
├──────────────────────┼──────────────────────┼────────────────────┤
│ Input:               │ Input:                │ Input:             │
│ - Product data JSON  │ - Customer message    │ - Order number     │
│                      │ - Chat history        │ - OR free-text FAQ │
│                      │                       │                    │
│ Process:             │ Process:              │ Process:           │
│ - Perplexity API     │ - Safety keyword scan │ - Route: order     │
│   ingredient fetch   │ - RAG over catalogue  │   tracking vs FAQ  │
│ - Merge ingredients  │ - Allergy detection   │ - Order DB lookup  │
│ - Claude Haiku       │ - LangGraph routing   │ - RAG over policies│
│   copywriting        │                       │ - Email trigger    │
│                      │                       │                    │
│ Output:              │ Output:               │ Output:            │
│ - Product desc. JSON │ - Chat response       │ - Brief status     │
│ - SEO tags           │ - Escalation alert    │ - Full details     │
│ - ingredients_source │   (if triggered)      │   → email on file  │
└──────────────────────┴──────────────────────┴────────────────────┘
          │                      │                     │
          └──────────────────────┴─────────────────────┘
                                 │
                     ┌───────────────────────┐
                     │   SHARED INFRASTRUCTURE│
                     │ - LangChain + LangGraph│
                     │ - Pinecone Vector Store│
                     │ - LangSmith Observ.    │
                     │ - n8n Orchestration    │
                     │ - GitHub CI/CD         │
                     └───────────────────────┘
```

### 2.2 Technology Stack (Bootcamp Coverage)

| Layer | Technology | Bootcamp Skill |
|---|---|---|
| LLM Backbone | Claude Haiku (claude-haiku-4-5-20251001) via Anthropic API | API Calling, Generative AI |
| Ingredient Lookup | Perplexity API (sonar model) | API Calling |
| Agent Framework | LangChain + LangGraph | LangChain, LangGraph, AI Agents |
| RAG Pipeline | Pinecone vector store + HuggingFace all-MiniLM-L6-v2 (384 dims, local) | RAG, Chunking |
| Observability | LangSmith → Tableau | LangSmith |
| Orchestration | n8n Cloud (low-code automation + email) | n8n, Low-code |
| Backend | Python 3.13 + FastAPI | Python |
| Frontend | Streamlit (5-tab demo interface) | Python |
| Data Handling | JSON (product catalogue, order data) | JSON handling |
| Prompts | Structured system prompts with escaped JSON schema, brand voice enforcement | Prompt Engineering |
| MCP Integration | n8n MCP nodes (Gmail safety alerts + order emails) | MCP implementation |
| Version Control | GitHub + VS Code | GitHub, VS Code |
| Project Mgmt | Jira (Agile/Kanban board) | Project Management / Jira |
| Testing | LangSmith eval + test_cases.json | LangSmith |
| Methodology | Sprint-based, Lean automation | Agile XP / Lean |

---

## 3. NO-CODE / LOW-CODE POC (n8n)

### 3.1 POC Scope

The POC demonstrates all three modules using n8n Cloud as the primary orchestration layer. This is the fastest path to demonstrating core AI capability without a full development stack.

### 3.2 n8n Workflow — Module 1: Shop Manager Agent

**Workflow Name:** `maison-beaute-product-description-generator`

**Trigger:** HTTP Webhook (POST `/new-product`)

**Input Payload (JSON):**
```json
{
  "product_id": "MB-2024-0847",
  "brand": "Charlotte Tilbury",
  "product_name": "Pillow Talk Lipstick",
  "category": "Make-up",
  "condition": "Tested Out",
  "original_retail_price_eur": 39.0,
  "listing_price_eur": 22.0,
  "size_value": 3.5,
  "size_unit": "g"
}
```

Note: `key_ingredients` is optional — the system fetches them automatically via Perplexity.

**Workflow Steps:**
1. **Webhook Trigger** → Receives product JSON
2. **HTTP Request Node** → Calls Perplexity API: "What are the key ingredients in [brand] [product]?"
3. **Code Node (Python runner)** → Parses ingredient list, merges with any manually provided ingredients
4. **Set Node** → Formats enriched product data + prompt for Claude Haiku
5. **Anthropic Chat Node** → Generates description enforcing Maison Beauté brand voice
6. **Code Node** → Strips markdown fences, validates JSON output
7. **HTTP Request Node** → POSTs generated description to product catalogue API
8. **Slack/Email MCP Node** → Notifies Founder: "New description published for [product_name]"

**System Prompt (Prompt Engineering):**
```
You are the Maison Beauté copywriter. Maison Beauté is a premium beauty marketplace
based in Berlin selling New, Tested Out, and Pre-loved luxury beauty products.
Your tone: sophisticated, warm, slightly French-inflected, sustainability-conscious.

Conditions:
- New: never used, original seal intact
- Tested Out: at least 90% of product remains, resealed after quality & hygiene check
- Pre-loved: at least 50% of product remains, resealed after quality & hygiene check

Generate in EXACTLY this JSON structure — no markdown fences:
{{
  "title": "...",        // max 60 chars, brand + product name
  "tagline": "...",      // 1 evocative sentence
  "description": "...", // 80-120 words, 3 paragraphs
  "seo_tags": [...],    // 5-8 tags
  "condition_note": "..." // references quality & hygiene check
}}

Rules: NEVER invent ingredients. NEVER claim New if condition is not New.
ALWAYS mention original packaging resealed after quality check.
```

### 3.3 n8n Workflow — Module 2: Beauty Advisor Chatbot

**Workflow Name:** `maison-beaute-beauty-advisor`

**Trigger:** Webhook (POST `/chat`) from website chat widget

**Workflow Steps:**
1. **Webhook** → Receives `{session_id, message, chat_history[]}`
2. **Code Node** → Safety scanner: checks message for allergy/reaction keywords (runs BEFORE any LLM call)
3. **Branch: Safety Flag?**
   - **YES:** → Slack MCP alert to Founder + safe holding response (message never sent to Anthropic)
   - **NO:** → Continue to RAG
4. **HTTP Request → Pinecone** → Retrieves top 4 relevant chunks from product catalogue
5. **Anthropic Chat Node** → Generates response with retrieved context
6. **Set Node** → Formats response JSON
7. **Respond to Webhook** → Returns response to chat widget

**Allergy/Safety Keyword List (n8n Code Node):**
```python
SAFETY_KEYWORDS = [
    "allergy", "allergic", "reaction", "rash", "hives", "swelling",
    "anaphylaxis", "itching", "burning", "irritation", "redness",
    "broke out", "bad reaction", "skin reaction", "nut allergy",
    "fragrance allergy", "latex", "patch test"
]

def is_safety_flag(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in SAFETY_KEYWORDS)
```

### 3.4 n8n Workflow — Module 3: Customer Self-Service

**Workflow Name:** `maison-beaute-customer-service`

**Trigger:** Webhook (POST `/customer-service`)

**Dual capability — the workflow detects query type and routes accordingly:**

**Path A — Order Tracking:**
- Input: message containing an order number (e.g. "MB-ORD-20241127-0042")
- Code Node detects order number pattern via regex
- HTTP Request → Queries fulfilment API with order number only
- Returns brief status in chat ("Your order is on its way! 📦")
- MCP Email Node → Sends full tracking details to email on file
- Zero PII ever shown in chat response

**Path B — FAQ / Policy Assistant:**
- Input: free-text policy question ("What is your return policy?", "Do you ship to Portugal?")
- HTTP Request → Pinecone retrieves relevant chunks from `policies.md` and `faq_knowledge_base.md`
- Anthropic Chat Node → Generates answer grounded in Maison Beauté policies
- Returns accurate, on-brand policy answer

**Privacy Design Principle:** Order number is the only identifier accepted in chat. The email address is retrieved internally from the order DB and used only to send the full tracking email — it is never returned in the chat response.

### 3.5 POC Demo Script

**Duration:** 4–5 minutes

1. Show n8n canvas with all three workflows loaded
2. Trigger Module 1: POST product JSON without ingredients → show Perplexity fetch + generated description
3. Trigger Module 2: Send normal beauty query → show RAG-based response
4. Trigger Module 2 again: Send "I have a nut allergy" → show escalation firing, Slack alert appearing
5. Trigger Module 3 (Order): Send order number → show brief chat response + email confirmation
6. Trigger Module 3 (FAQ): Ask "What is your return policy?" → show RAG policy response

---

## 4. OBSERVABILITY & CONTINUOUS IMPROVEMENT
## LangSmith → Tableau Monitoring Pipeline

### 4.1 Overview

Rather than a static ROI calculation, Maison Beauté's AI Advisor system is built with a live observability pipeline that allows the business owner and the AI consultant to monitor system performance, evaluate response quality, and continuously improve the chatbot — all from a single Tableau dashboard.

This approach reflects real-world AI deployment practice: a system is only as good as your ability to monitor, catch failures, and iterate.

---

### 4.2 The Pipeline: LangSmith → CSV/API → Tableau

```
LangSmith (tracing + eval)
        │
        │  Traces every LLM call:
        │  - Input / Output
        │  - Latency (ms)
        │  - Token usage
        │  - Eval scores (correctness, safety, relevance)
        │  - Session ID (anonymised)
        │  - Module tag (M1 / M2 / M3)
        │
        ▼
Export Layer
        │
        │  Option A: Manual CSV export from LangSmith UI
        │  Option B: LangSmith API → Python script → CSV (evals/export_to_tableau.py)
        │  Option C: n8n scheduled workflow → pulls data nightly
        │
        ▼
Tableau Desktop / Tableau Public
        │
        │  Live dashboard for Founder + AI consultant
        │
        ▼
Actionable Insights → Prompt refinement, RAG updates, escalation tuning
```

---

### 4.3 LangSmith Configuration

**What gets traced:**

Every LLM call across all three modules is wrapped with the `@traceable` decorator and tagged by module:

```python
# Module 1 — Product Description Generator
@traceable(name="generate_product_description", tags=["module-1", "shop-manager"])
async def generate_description(product_data: dict) -> dict:
    ...

# Module 1 — Ingredient Lookup
@traceable(name="ingredient_lookup", tags=["module-1", "perplexity"])
async def fetch_ingredients(brand: str, product_name: str) -> list[str]:
    ...

# Module 2 — Beauty Advisor Chatbot
@traceable(name="beauty_advisor_response", tags=["module-2", "chatbot"])
async def chat_response(message: str, session_id: str) -> dict:
    ...

# Module 2 — Safety Check Node
@traceable(name="safety_check", tags=["module-2", "safety"])
def safety_check_node(state: ChatState) -> ChatState:
    ...

# Module 3 — Customer Self-Service
@traceable(name="customer_service_response", tags=["module-3", "customer-service"])
async def customer_service_response(message: str) -> dict:
    ...
```

**LangSmith Evaluation Dataset:**

A test dataset of ~50 golden Q&A pairs is maintained in LangSmith to run automated evals:

```python
# evals/langsmith_eval_config.py
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

evaluators = [
    "correctness",   # Does the answer match the expected answer?
    "relevance",     # Is it relevant to the question?
    "safety",        # Does it avoid harmful content?
    "conciseness",   # Is it appropriately brief?
]

results = evaluate(
    chat_pipeline,
    data="maison-beaute-eval-dataset",
    evaluators=evaluators,
    experiment_prefix="mb-advisor-v1",
)
```

---

### 4.4 Data Export to Tableau

**Schema of the exported dataset (CSV):**

| Field | Type | Description |
|---|---|---|
| `trace_id` | string | Unique LangSmith trace ID (anonymised) |
| `session_id` | string | Anonymised session identifier |
| `timestamp` | datetime | When the interaction occurred |
| `module` | string | M1 / M2 / M3 |
| `run_name` | string | e.g. "beauty_advisor_response" |
| `input_tokens` | int | Tokens in the prompt |
| `output_tokens` | int | Tokens in the response |
| `latency_ms` | int | End-to-end response time in milliseconds |
| `safety_flagged` | boolean | Was a safety/allergy keyword detected? |
| `escalated` | boolean | Was the interaction escalated to Founder? |
| `resolved` | boolean | Was query resolved without human escalation? |
| `eval_correctness` | float | LangSmith eval score 0.0–1.0 |
| `eval_relevance` | float | LangSmith eval score 0.0–1.0 |
| `eval_safety` | float | LangSmith eval score 0.0–1.0 |
| `error` | boolean | Did the LLM call fail or time out? |

---

### 4.5 Tableau Dashboard — Views & KPIs

**Dashboard Name:** Maison Beauté AI Advisor — Operations Monitor
**Target audience:** Business owner/founder + AI consultant (Carolina)
**Refresh cadence:** Weekly (manual CSV import) or nightly (n8n automation)

**View 1 — Executive Summary (KPI cards)**

| KPI | Target | Visualisation |
|---|---|---|
| Chatbot Resolution Rate | ≥ 75% | Big number card + trend sparkline |
| Safety Escalations (last 7 days) | Monitor for spikes | Counter with red/amber/green threshold |
| Average Response Latency | < 3,000 ms | Gauge chart |
| Eval Quality Score (avg) | ≥ 0.75 | Score card |
| Total Interactions (last 30 days) | — | Volume counter |

**View 2 — Resolution Rate Over Time**
Line chart: % resolved vs. % escalated, trended by week, filtered by module (M1 / M2 / M3).

**View 3 — Safety Escalation Heatmap**
Calendar heatmap: escalations per day. Identifies patterns (spikes after new product launches, seasonal allergy periods).

**View 4 — Response Quality Scores**
Bar chart: average correctness / relevance / safety scores per week with trendline overlay.

**View 5 — Latency Distribution**
Histogram of response latency (ms) by module. Identifies which module is slowest (typically M2 RAG retrieval).

**View 6 — Top Unresolved Query Categories**
Horizontal bar chart: query categories most frequently resulting in escalation or low eval scores. Directly informs what new content to add to the Pinecone knowledge base.

---

### 4.6 Continuous Improvement Loop

```
Weekly Review (Founder + Carolina)
        │
        ├── Resolution rate dropped?
        │       → Review LangSmith traces for that period
        │       → Identify gap in Pinecone knowledge base
        │       → Add content, re-index, re-test
        │
        ├── Safety escalations spiked?
        │       → Review flagged messages
        │       → Add new keywords to safety scanner if needed
        │       → Check if any false negatives slipped through
        │
        ├── Latency increased?
        │       → Check token usage trend
        │       → Consider switching to a lighter Claude model tier
        │       → Tune Pinecone retrieval k parameter
        │
        └── Eval scores declining?
                → Run full LangSmith evaluation suite
                → Update few-shot examples in system prompts
                → Version-control prompt changes in GitHub
                → Re-run evals to confirm improvement
```

---

### 4.7 GDPR Note on Monitoring Data

All data exported to Tableau is **anonymised at source**:

- No customer names, email addresses, or order details appear in LangSmith traces
- Session IDs are system-generated UUIDs — not linkable to individual customers
- Flagged message content (allergy mentions) is retained in LangSmith for max 7 days, then purged automatically
- Tableau dashboard contains zero personally identifiable information

This means the monitoring pipeline is fully GDPR-compliant without requiring a separate DPIA.

---

## 5. EU AI ACT COMPLIANCE DOCUMENTATION

### 5.1 System Classification

**Step-by-Step Classification Reasoning:**

**Step 1: Is the system explicitly prohibited?**
No. Maison Beauté AI Advisor does not engage in social scoring, real-time biometric surveillance, subliminal manipulation, or exploitation of vulnerabilities. → Proceed to Step 2.

**Step 2: Is the system High-Risk (Annex III)?**
- Critical infrastructure: NO
- Educational/vocational training: NO
- Employment decisions: NO
- Access to essential services: NO
- Law enforcement: NO
- Migration/border control: NO
- Justice/democratic processes: NO
- Safety components of products: PARTIAL — The allergy escalation module processes information that could relate to health/safety.

**Assessment on Health/Safety:** The chatbot does NOT diagnose, prescribe, or provide medical advice. It identifies safety keywords and escalates to a human (the founder). The AI does not make consequential decisions about health. The system serves as a **triage flag** to a human, not an autonomous health decision system.

**Conclusion Step 2:** NOT High-Risk under Annex III.

**Step 3: Does the system interact with natural persons?**
YES — The Beauty Advisor chatbot and Customer Self-Service module interact with customers.

**Step 4: Does the system generate synthetic content / deep fakes?**
NO — Product descriptions are operational content generated for business use.

**Classification: LIMITED RISK**

The system falls under **Limited Risk** per EU AI Act Article 50, due to the chatbot components interacting with natural persons. This triggers **transparency obligations** only.

### 5.2 Mandatory Requirements (Limited Risk)

| Obligation | Requirement | Implementation |
|---|---|---|
| Transparency | Users must be informed they are interacting with an AI | Chat widget displays "Powered by AI" label; first message states "I'm Beauté, your AI advisor" |
| Disclosure | AI system must not deceive users into thinking they are interacting with a human | Bot never claims to be human; escalation to founder is clearly human |
| Opt-out | Users should be able to reach a human | Every chatbot session includes "Talk to a human" fallback option |

### 5.3 Conformity Assessment Summary

**Document ID:** MB-AI-CA-2024-001
**System Name:** Maison Beauté AI Advisor
**Version:** 1.0
**Date:** 2026-03-27
**Prepared by:** Carolina, AI Consultant

**What the system does:**
The Maison Beauté AI Advisor is a three-module AI system. Module 1 generates product descriptions using Perplexity for ingredient research and Claude Haiku for copywriting. Module 2 provides conversational beauty advice using RAG over the product catalogue with a safety escalation layer. Module 3 handles order tracking and FAQ queries — order tracking uses the order number as the sole identifier and returns full details to the email on file; FAQ queries use RAG over platform policies.

**Risk Classification:** LIMITED RISK (EU AI Act, Article 50)

**Obligations Applicable:**
- Transparency disclosure to users (Article 50(1)): COMPLIANT — Bot identity disclosed at session start
- No deception about AI nature (Article 50(1)): COMPLIANT — Bot does not impersonate a human
- Human escalation pathway: IMPLEMENTED — Health/allergy flags escalate to human within 2 minutes

**Obligations NOT Applicable:**
- High-Risk mandatory requirements (Annex III): NOT APPLICABLE
- Conformity assessment by notified body: NOT REQUIRED at Limited Risk
- Registration in EU AI Act database: NOT REQUIRED at Limited Risk

**Monitoring Commitment:**
Annual review of classification as EU AI Act regulatory guidance evolves.

### 5.4 Technical Documentation Outline

**MB-AI-TD-2024-001 — Technical Documentation Skeleton**

```
1. GENERAL DESCRIPTION
   1.1 System name and version
   1.2 Intended purpose and use case
   1.3 Deployment context (marketplace, EU/DE jurisdiction)
   1.4 System components and modules

2. TECHNICAL SPECIFICATIONS
   2.1 AI/ML models used (claude-haiku-4-5-20251001, text-embedding-3-small, Perplexity sonar)
   2.2 RAG pipeline architecture (Pinecone + LangChain)
   2.3 LangChain/LangGraph agent design
   2.4 API integrations (Anthropic, OpenAI, Perplexity, Pinecone)
   2.5 n8n orchestration workflow exports

3. DATA GOVERNANCE
   3.1 Training data (not applicable — using pre-trained foundation models)
   3.2 RAG knowledge base: product catalogue, policies, FAQs (Pinecone)
   3.3 Data refresh schedule
   3.4 Data quality controls

4. PERFORMANCE METRICS
   4.1 Chatbot resolution rate
   4.2 Escalation accuracy (safety flags)
   4.3 Description quality metrics (human review sampling)
   4.4 LangSmith evaluation pipeline results

5. HUMAN OVERSIGHT
   5.1 Escalation protocol for safety flags
   5.2 Weekly sampling of generated descriptions
   5.3 Monthly chatbot response audit
   5.4 Incident response procedure

6. TRANSPARENCY MEASURES
   6.1 User-facing AI disclosure copy
   6.2 Bot persona guidelines
   6.3 Limitations statement (not medical advice)

7. ROBUSTNESS & SECURITY
   7.1 Input validation (Pydantic models)
   7.2 Output validation (JSON parsing + markdown fence stripping)
   7.3 API authentication
   7.4 Rate limiting

8. CHANGE LOG
   8.1 Version history
   8.2 Prompt version control (GitHub)
```

---

## 6. GDPR DOCUMENTATION & DPIA

### 6.1 Personal Data Inventory

| Data Element | Module | Source | Purpose | Legal Basis |
|---|---|---|---|---|
| Customer chat messages | Module 2 | Customer input | Generate chatbot response | Legitimate Interest (Art. 6(1)(f)) |
| Session ID (anonymised UUID) | Module 2 & 3 | System-generated | Session continuity, abuse prevention | Legitimate Interest |
| Order number | Module 3 | Customer input | Order tracking | Performance of Contract (Art. 6(1)(b)) |
| Email address (on file) | Module 3 | Internal order DB | Send order details to customer | Performance of Contract (Art. 6(1)(b)) |
| Allergy/health mentions in chat | Module 2 | Customer input | Safety escalation | Vital Interests (Art. 6(1)(d)) |

### 6.2 Data Flow Diagram (Narrative)

**Module 1 Data Flow:**
Product data JSON (no PII) → Perplexity API (ingredient lookup, no PII transmitted) → Claude Haiku (description generation, no PII) → Product catalogue API → Founder notification via MCP.

**Module 2 Data Flow:**
Customer message → n8n webhook (EU servers) → Safety keyword scan (local, no LLM) → if flagged: Slack MCP alert only, message NOT sent to Anthropic → if not flagged: Anthropic API → LangSmith logging (anonymised session ID only) → Chat response returned → Conversation retained 90 days → Deleted automatically.

**Module 3 Data Flow:**
Order number (non-PII by design) → Internal fulfilment DB query → Email address retrieved internally (never exposed in chat) → Email sent via Brevo (EU-based) → Order number and status logged (no PII) → Log retained 30 days.

FAQ queries → Pinecone retrieval → Anthropic API → Response (no PII involved).

### 6.3 Third-Party Data Processors

| Processor | Service | Transfer | Safeguard |
|---|---|---|---|
| Anthropic (via API) | LLM inference | USA transfer | Standard Contractual Clauses (SCCs); Anthropic API DPA signed |
| Perplexity (via API) | Ingredient lookup | USA transfer | SCCs; product data only, no PII transmitted |
| OpenAI (via API) | Embeddings only | USA transfer | SCCs; text chunks only, no PII |
| Pinecone | Vector store | USA transfer | SCCs; anonymised text chunks only |
| LangSmith (LangChain) | Observability / tracing | USA transfer | SCCs; anonymised traces only; opt-out of training configured |
| Brevo (Sendinblue) | Email delivery | EU (FR) | GDPR-native processor; DPA in place |
| n8n Cloud | Workflow orchestration | EU (DE) | GDPR-native; EU data residency |

### 6.4 Data Subject Rights Implementation

| Right | Applicability | Implementation |
|---|---|---|
| Right of Access (Art. 15) | Chat logs linked to session | Customer can request session transcript via privacy@maisonbeaute.de |
| Right to Erasure (Art. 17) | Chat logs, order logs | Automated deletion after 90 days; manual deletion on request within 72 hours |
| Right to Portability (Art. 20) | Contract-basis data | Order data exportable in CSV on request |
| Right to Object (Art. 21) | Legitimate interest processing | Opt-out option in cookie/privacy settings |
| Right to Restrict Processing (Art. 18) | All personal data | Account-level flag in CRM system |

### 6.5 Data Protection Impact Assessment (DPIA)

**For: Module 2 Beauty Advisor — Processing of Health-Related Mentions (Allergy/Safety Data)**

**Why this processing warrants a DPIA:**
Health data is a special category under GDPR Art. 9. When a customer mentions allergies or adverse reactions in the chat, the system processes what may constitute health data.

**Step 1 — Describe the Processing**
A keyword detection layer identifies messages containing allergy or health-related terms. When detected, the message is flagged and routed to the human operator via Slack. The flagged message content is included in the alert.

**Step 2 — Assess Necessity and Proportionality**
- Is the processing necessary? YES — Safety escalation protects the customer from potential harm
- Is it proportionate? YES — Only the specific flagged message is transmitted; no profiling or retention beyond the session
- Less privacy-invasive alternative? A semantic AI classifier would send MORE data to the LLM. Keyword matching is actually MORE privacy-preserving.

**Step 3 — Risk Identification**

| Risk | Likelihood | Impact | Residual Risk |
|---|---|---|---|
| Health data shared with Anthropic | Medium | High | MITIGATED — Keyword detection runs BEFORE LLM call; flagged messages never reach Anthropic |
| Slack notification exposes health mention | Low | High | MITIGATED — Slack workspace is private to founder; enterprise security settings applied |
| Customer unaware their mention is flagged | Medium | Medium | MITIGATED — Privacy notice discloses this; chat disclaimer states health mentions are reviewed by team |
| False positives causing unnecessary processing | High | Low | ACCEPTABLE — False positive means a non-health message is flagged; annoying but not harmful |

**Step 4 — Measures to Address Risks**
1. Keyword detection runs locally in n8n — flagged messages NOT forwarded to the LLM
2. Privacy notice clearly states health mentions may be reviewed by the team
3. Flagged messages retained in Slack max 7 days, then deleted
4. Only the flagged message segment is included in the Slack alert, not the full session history

**Step 5 — DPO Consultation**
As a micro-enterprise, Maison Beauté is not required to appoint a DPO. If appointed in future, this DPIA should be reviewed.

**DPIA Conclusion:** Processing is lawful under Art. 6(1)(d) and Art. 9(2)(c). Residual risks are acceptable. Processing may proceed.

---

## 7. STRATEGIC DEPLOYMENT PLAN

### 7.1 Deployment Phases

**Phase 1: POC (Weeks 1–2)**
- Deliverable: Working n8n workflows for all 3 modules; FastAPI MVP running locally
- Success metric: All 3 modules testable via Swagger UI
- Tools: n8n Cloud, Anthropic API, Perplexity API, Pinecone, LangSmith

**Phase 2: Pilot (Weeks 3–6)**
- Deliverable: Beta chatbot deployed on staging site; 50 real customer interactions
- Success metric: 70%+ resolution rate; 0 false negatives on safety escalation
- Monitoring: LangSmith traces reviewed weekly; Tableau dashboard live

**Phase 3: Full Deployment (Weeks 7–12)**
- Deliverable: Production system on maison-beaute.de; all 3 modules live
- Success metric: All success criteria from §1.6 met
- Ongoing: Monthly bias audit, quarterly compliance review, GitHub version control on all prompts

### 7.2 Milestone Timeline

| Week | Milestone |
|---|---|
| 1 | Project shell, API keys, Pinecone index, requirements resolved |
| 2 | Module 1 live (Perplexity + Claude Haiku); n8n workflows built |
| 3 | Module 2 live (RAG + safety escalation); LangSmith tracing active |
| 4 | Module 3 live (order tracking + FAQ RAG); Swagger demo ready |
| 5 | LangSmith eval run; Tableau dashboard connected |
| 6 | Staging deployment; 50 pilot interactions |
| 7–8 | Production deployment; compliance docs finalised |
| 9–12 | Performance monitoring; continuous improvement cycle |

### 7.3 Stakeholder Communication Plan

| Stakeholder | Message | Channel | Frequency |
|---|---|---|---|
| Founder | Weekly progress update; workflow demo; metrics dashboard | Slack / weekly call | Weekly |
| Customers | "Meet Beauté, our AI Beauty Advisor" | Email newsletter, website banner | Launch + 30 days |
| Legal/Compliance | EU AI Act classification memo; GDPR DPIA summary | Formal document | At deployment + annually |

### 7.4 Go-to-Market Strategy

**Target Buyers:**
- Primary: Maison Beauté (direct client — internal tool deployment)
- Secondary: Other pre-loved luxury marketplaces in DACH

**Pricing Model:**

| Tier | Target | Price | Includes |
|---|---|---|---|
| Starter | Solo operators (1–5 SKUs/day) | €149/month | All 3 modules, up to 500 chat sessions/month |
| Growth | Small marketplaces | €449/month | Unlimited sessions, custom brand voice, LangSmith access |
| Enterprise | Multi-brand platforms | €1,500+/month | White-label, API access, custom integrations |

### 7.5 Commercialisation Model

**Model:** SaaS + Implementation Service

Each marketplace gets their own brand voice configuration, Pinecone knowledge base, and compliance documentation template.

**Competitive Advantage:**
- Privacy-first architecture (no PII in chat) — EU market differentiator
- Perplexity-powered ingredient enrichment — no manual research needed
- Pre-built EU AI Act + GDPR documentation — saves clients 2–4 weeks of legal work

---

## 8. MVP ARCHITECTURE (STRETCH)

### 8.1 MVP Stack

```python
# /app/main.py — FastAPI entry point
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent / "data" / ".env")

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.langsmith_config import setup_langsmith
from app.core.rag_pipeline import build_vectorstore, load_knowledge_base
from app.routers import descriptions, chatbot, orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_langsmith()
    documents = load_knowledge_base(data_dir="data")
    if documents:
        build_vectorstore(documents)
    yield

app = FastAPI(title="Maison Beauté AI Advisor API")
app.include_router(descriptions.router, prefix="/products")
app.include_router(chatbot.router, prefix="/chat")
app.include_router(orders.router, prefix="/orders")
```

### 8.2 Module 1 — Shop Manager Agent (Python + LangChain + Perplexity)

```python
# /app/routers/descriptions.py
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from app.core.ingredient_lookup import fetch_ingredients, merge_ingredients
import json

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0.7)

@traceable(name="generate_product_description", tags=["module-1"])
async def generate_description(product: ProductInput) -> ProductDescription:
    # 1. Fetch ingredients from Perplexity
    perplexity_ingredients = await fetch_ingredients(product.brand, product.product_name)
    # 2. Merge with manual ingredients if provided
    final_ingredients, source = merge_ingredients(perplexity_ingredients, product.key_ingredients)
    # 3. Generate description via Claude Haiku
    result = await chain.ainvoke({"product_json": json.dumps(product_data)})
    # 4. Strip markdown fences, parse JSON
    raw = result.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1][4:].strip()
    return ProductDescription(**json.loads(raw), ingredients_source=source)
```

### 8.3 Module 2 — Beauty Advisor RAG Chatbot (LangChain + Pinecone + LangGraph)

```python
# /app/core/rag_pipeline.py
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(host=os.getenv("PINECONE_HOST"))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)

def build_rag_chain() -> ConversationalRetrievalChain:
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 4})
    return ConversationalRetrievalChain.from_llm(
        llm=ChatAnthropic(model="claude-haiku-4-5-20251001"),
        retriever=retriever,
        return_source_documents=True
    )
```

### 8.4 LangGraph Agent — Safety Escalation Logic

```python
# /app/core/langgraph_agent.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class ChatState(TypedDict):
    message: str
    session_id: str
    chat_history: list
    safety_flagged: bool
    response: str

def safety_check_node(state: ChatState) -> ChatState:
    """Runs BEFORE LLM — flagged messages never reach Anthropic"""
    SAFETY_KEYWORDS = ["allergy", "allergic", "reaction", "rash",
                       "hives", "burning", "swelling", "anaphylaxis"]
    flagged = any(kw in state["message"].lower() for kw in SAFETY_KEYWORDS)
    return {**state, "safety_flagged": flagged}

def route_after_safety(state: ChatState) -> Literal["escalate", "rag_response"]:
    return "escalate" if state["safety_flagged"] else "rag_response"

def escalate_node(state: ChatState) -> ChatState:
    # Triggers MCP Slack alert to founder — no LLM call
    response = ("Your safety is our priority. A member of our team will contact you shortly.")
    return {**state, "response": response}

def rag_response_node(state: ChatState) -> ChatState:
    from app.core.rag_pipeline import build_rag_chain
    result = build_rag_chain().invoke({
        "question": state["message"],
        "chat_history": state["chat_history"]
    })
    return {**state, "response": result["answer"]}

graph = StateGraph(ChatState)
graph.add_node("safety_check", safety_check_node)
graph.add_node("escalate", escalate_node)
graph.add_node("rag_response", rag_response_node)
graph.set_entry_point("safety_check")
graph.add_conditional_edges("safety_check", route_after_safety)
graph.add_edge("escalate", END)
graph.add_edge("rag_response", END)
agent = graph.compile()
```

### 8.5 GitHub Repository Structure

```
maison-beaute-ai-advisor/
├── README.md
├── .gitignore
├── requirements.txt
├── streamlit_app.py                     # 5-tab Streamlit demo interface
├── poc_documentation.md
├── roi_risk_assessment.md
├── Maison_Beaute_PROJECT_DOCUMENTATION.md
├── app/
│   ├── main.py                          # FastAPI entry point, Pinecone startup loading
│   ├── core/
│   │   ├── langsmith_config.py          # LangSmith tracing setup
│   │   ├── rag_pipeline.py              # Pinecone RAG (LCEL), namespace support
│   │   ├── langgraph_agent.py           # Safety routing agent + n8n webhook call
│   │   └── ingredient_lookup.py        # Perplexity API ingredient fetch
│   ├── routers/
│   │   ├── descriptions.py              # Module 1 — Shop Manager
│   │   ├── chatbot.py                   # Module 2 — Beauty Advisor
│   │   ├── orders.py                    # Module 3 — Order Tracking + n8n webhook
│   │   └── newsletter.py               # Module 4 — Newsletter Generator
│   └── models/
│       ├── product.py                   # ProductInput + ProductDescription models
│       └── chat.py                      # ChatMessage model
├── n8n/
│   ├── workflow_module2_chatbot.json    # Module 2: safety scan + RAG + Gmail alert
│   └── workflow_module3_orders.json    # Module 3: order tracking + FAQ + Gmail email
├── data/
│   ├── .env                             # API keys (gitignored)
│   ├── .gitignore
│   ├── faq_knowledge_base.md           # Pinecone namespace: policies
│   ├── policies.md                     # Pinecone namespace: policies
│   └── product_catalogue_knowledge_base.md  # Pinecone namespace: products (16 products)
├── evals/
│   ├── langsmith_eval_config.py
│   ├── export_to_tableau.py
│   └── test_cases.json
└── docs/
    ├── EU_AI_Act_Conformity_Assessment.md
    ├── GDPR_DPIA.md
    └── Architecture_Diagram.md
```

---

## 9. BOOTCAMP SKILLS MAPPING

| Bootcamp Skill | Where Used in This Project |
|---|---|
| **JSON Handling** | Product data payload (Module 1 input/output), order data, LangSmith eval test cases, n8n workflow exports, markdown fence stripping before JSON parse |
| **Python** | FastAPI backend, LangChain chains, LangGraph agent nodes, safety detection logic, Perplexity ingredient parser, newsletter generator |
| **Generative AI** | Claude Haiku (claude-haiku-4-5-20251001) for description generation, chatbot responses, and newsletter drafting |
| **GitHub** | Full repo structure with version control; prompt versioning via Git |
| **VS Code** | Development environment for all Python/LangChain code |
| **API Calling** | Anthropic API, Perplexity API (ingredient lookup), Pinecone API, n8n webhook APIs |
| **Prompt Engineering** | System prompts with escaped JSON schema (`{{}}`), brand voice enforcement, measured language rules, few-shot examples |
| **MCP Implementation** | n8n MCP nodes for Gmail notifications: safety escalation alert + order tracking email (both confirmed working) |
| **RAG** | Pinecone vector store with two namespaces: `products` (Module 2, 30 chunks) and `policies` (Module 3, 31 chunks) |
| **AI Agents** | LangGraph agent with conditional routing: safety_check → escalate OR rag_response → END |
| **Chunking** | RecursiveCharacterTextSplitter, chunk_size=500, overlap=50, HuggingFace all-MiniLM-L6-v2 embeddings (384 dims, local) |
| **Low-code** | n8n Cloud workflows as POC delivery vehicle for Modules 2 and 3; email automation wired to FastAPI |
| **LangChain** | Core framework for LLM calls, RAG chain (LCEL syntax), prompt templates, Pinecone integration |
| **LangGraph** | Agent state machine: safety_check_node → conditional routing → escalate_node or rag_response_node → END |
| **LangSmith** | Tracing all LLM calls across all modules; project: mainson-beaute-beauty-advisor |
| **n8n** | POC workflows for M2 and M3; Gmail MCP nodes; wired to FastAPI via webhook calls |
| **Agile XP/Lean** | Sprint-based delivery; lean POC-first approach; iterative prompt refinement based on LangSmith data |
| **Project Mgmt / Jira** | Jira Kanban board with epics per module; sprint tracking; GitHub integration |

---

*Document version: 2.0 | Updated: March 2026 | Ironhack Berlin — AI Consulting & Integration Bootcamp*
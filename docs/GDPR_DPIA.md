# GDPR Documentation & Data Protection Impact Assessment (DPIA)

**System:** Maison Beauté AI Advisor
**Version:** 2.0
**Date:** March 2026
**Prepared by:** Carolina, AI Consultant (namiaistudio.com)
**Ironhack AI Consulting & Integration Bootcamp — Final Project**

---

## 1. PERSONAL DATA INVENTORY

| Data Element | Module | Source | Purpose | Legal Basis | Retention |
|---|---|---|---|---|---|
| Customer chat messages | Module 2 | Customer input | Generate chatbot response | Legitimate Interest (Art. 6(1)(f)) | 90 days, then auto-deleted |
| Session ID (anonymised UUID) | Modules 2 & 3 | System-generated | Session continuity, abuse prevention | Legitimate Interest | 90 days |
| Order number | Module 3 | Customer input | Order tracking | Performance of Contract (Art. 6(1)(b)) | 30 days |
| Email address (on file) | Module 3 | Internal order DB | Send order details to customer | Performance of Contract (Art. 6(1)(b)) | Per order retention policy |
| Allergy/health mentions in chat | Module 2 | Customer input | Safety escalation | Vital Interests (Art. 6(1)(d)) + Art. 9(2)(c) | 7 days maximum, then purged |
| LangSmith trace data | All modules | System-generated | Quality monitoring, observability | Legitimate Interest | 14 days (LangSmith retention setting) |

**Note:** Module 1 (Shop Manager) and Module 4 (Newsletter Generator) process no personal data — all inputs are product information and marketing topics respectively.

---

## 2. DATA FLOW NARRATIVE

### Module 2 — Beauty Advisor Chatbot
```
Customer message entered in Streamlit
        ↓
FastAPI receives message
        ↓
LangGraph safety keyword scan (LOCAL — no external API call)
        ↓
IF safety flagged:
  → Flagged message content sent to n8n via webhook
  → n8n sends Gmail alert to founder (carolinanami@gmail.com for demo)
  → Message is NOT forwarded to Anthropic API
  → Retained in Gmail max 7 days
        ↓
IF not flagged:
  → Message sent to Anthropic API (Claude Haiku)
  → Only session UUID in LangSmith traces (no customer name/email)
  → Response returned to customer
  → Session log retained 90 days then auto-deleted
```

### Module 3 — Customer Self-Service (Order Tracking)
```
Customer enters order number only (non-PII by design)
        ↓
Internal DB lookup retrieves order status + email address
        ↓
Email address used INTERNALLY only — never returned in chat response
        ↓
n8n sends full order details to email on file
        ↓
Chat response: brief status only (e.g. "Your order is on its way! 📦")
        ↓
Order number + status logged (no PII) — retained 30 days
```

### Module 3 — FAQ Assistant
```
Customer enters free-text policy question
        ↓
Message sent to Anthropic API (Claude Haiku)
        ↓
Pinecone retrieves policy chunks (no PII involved)
        ↓
Response grounded in platform policies
        ↓
No personal data stored beyond session UUID
```

---

## 3. THIRD-PARTY DATA PROCESSORS

| Processor | Service | Data Transferred | Transfer Location | Safeguard |
|---|---|---|---|---|
| Anthropic (via API) | LLM inference (Modules 1, 2, 3, 4) | Chat messages (non-flagged), product data, newsletter topics | USA | Standard Contractual Clauses (SCCs); Anthropic API DPA; health-flagged messages explicitly excluded |
| Perplexity (via API) | Ingredient lookup (Module 1) | Brand name + product name only — no PII | USA | SCCs; product data only |
| Pinecone | Vector store | Text chunks from knowledge base — no PII | USA | SCCs; anonymised text chunks only |
| LangSmith (LangChain) | Observability / tracing | Anonymised session UUIDs, token counts, latency | USA | SCCs; opt-out of model training configured; 14-day retention |
| n8n Cloud | Workflow orchestration + email | Safety-flagged message content; order status data | EU (DE) | GDPR-native processor; EU data residency |
| Brevo (Sendinblue) | Email delivery | Customer email address (order tracking) | EU (FR) | GDPR-native processor; DPA in place |
| HuggingFace (embeddings) | Text embedding model | Text chunks only — no PII | LOCAL (on-device) | No data transfer — model runs locally on CPU |

---

## 4. DATA SUBJECT RIGHTS

| Right | Article | Applicability | Implementation |
|---|---|---|---|
| Right of Access | Art. 15 | Chat logs linked to session | Customer requests via privacy@maisonbeaute.de; session transcript provided within 30 days |
| Right to Erasure | Art. 17 | All personal data | Auto-deleted after retention period; manual deletion within 72 hours on request |
| Right to Portability | Art. 20 | Contract-basis data (orders) | Order data exportable as CSV on request |
| Right to Object | Art. 21 | Legitimate interest processing | Opt-out option in cookie/privacy settings; chat analytics can be disabled |
| Right to Restrict Processing | Art. 18 | All personal data | Account-level flag in CRM system |
| Right not to be subject to automated decisions | Art. 22 | N/A | No fully automated decisions made — all outputs require human review or are informational only |

---

## 5. DATA PROTECTION IMPACT ASSESSMENT (DPIA)

### 5.1 Scope

**Processing activity under assessment:** Processing of health-related mentions (allergy/adverse reaction data) in Module 2 Beauty Advisor chatbot.

**Why this requires a DPIA:** Health data is a special category under GDPR Article 9. When customers mention allergies or adverse reactions in chat, the system processes what may constitute health data about a natural person. The potential impact on data subjects warrants a focused assessment.

### 5.2 Description of Processing

When a customer message contains one or more of 20+ safety keywords (allergy, allergic, reaction, rash, hives, swelling, anaphylaxis, itching, burning, irritation, redness, broke out, bad reaction, skin reaction, nut allergy, fragrance allergy, latex, patch test, etc.), the LangGraph agent routes to the escalation pathway. The message content is transmitted to the founder via n8n/Gmail for human review.

### 5.3 Necessity and Proportionality

| Question | Assessment |
|---|---|
| Is the processing necessary? | YES — Safety escalation protects customers from potential harm from allergic reactions to cosmetics |
| Is it proportionate to the risk? | YES — Only the specific flagged message is processed; no profiling or retention beyond 7 days |
| Is there a less privacy-invasive alternative? | A semantic AI classifier would send MORE data to the LLM. Keyword matching is more privacy-preserving — it processes the minimum data necessary |
| Could the purpose be achieved without processing health data? | NO — The safety function requires identifying health-relevant content |

### 5.4 Risk Identification and Mitigation

| Risk ID | Risk Description | Likelihood (1-5) | Impact (1-5) | Score | Mitigation | Residual Risk |
|---|---|---|---|---|---|---|
| GDPR-R1 | Health data (allergy mention) inadvertently forwarded to Anthropic's API | 2 | 5 | 10 | Keyword detection runs BEFORE any LLM call — flagged messages explicitly excluded from Anthropic API calls | LOW |
| GDPR-R2 | Gmail notification exposes health data to unauthorised parties | 1 | 4 | 4 | Gmail workspace private to founder; enterprise security settings applied | LOW |
| GDPR-R3 | Customer unaware that health mention is flagged and reviewed | 3 | 3 | 9 | Privacy notice discloses this practice; chat interface includes disclaimer; GDPR Art. 13/14 information provided | LOW-MEDIUM |
| GDPR-R4 | Excessive retention of flagged health data | 2 | 4 | 8 | 7-day maximum retention in Gmail; auto-purge configured; no archiving of health data | LOW |
| GDPR-R5 | False positive — non-health message flagged and reviewed | 4 | 1 | 4 | Low impact — slightly annoying for founder but no harm to customer | ACCEPTABLE |
| GDPR-R6 | LangSmith traces contain identifiable health information | 1 | 4 | 4 | Flagged messages excluded from LangSmith traces; only safe responses are logged; session UUIDs only | LOW |

### 5.5 Measures Implemented

1. **Pre-LLM filtering:** Safety keyword scanner runs entirely locally in LangGraph — flagged messages never reach Anthropic
2. **Minimal transmission:** Only the flagged message segment (not full chat history) is included in the n8n/Gmail alert
3. **Strict retention:** 7-day maximum retention; no archiving
4. **Privacy notice:** Platform privacy policy discloses health data handling to users
5. **Data minimisation:** No name, email, or other identifiers linked to the flagged message in the alert

### 5.6 Legal Basis for Health Data Processing

**Primary basis:** Article 6(1)(d) — Vital Interests: Processing is necessary to protect the vital interests of the data subject (preventing potential allergic reaction harm).

**Special category basis:** Article 9(2)(c) — Vital Interests: Processing of special category data (health) necessary to protect vital interests where the data subject may be unable to give consent (e.g. if already experiencing a reaction).

### 5.7 DPO Consultation

As a micro-enterprise (under 250 employees), Maison Beauté is not required to appoint a Data Protection Officer under GDPR Article 37. If a DPO is appointed in future, this DPIA should be reviewed by them.

### 5.8 DPIA Conclusion

**Decision:** Processing may proceed.

**Rationale:** The processing is lawful under Art. 6(1)(d) and Art. 9(2)(c). The primary risk (health data reaching Anthropic's API) is fully mitigated by architectural design — the keyword scanner runs before any external API call. Residual risks are low and proportionate to the safety benefit delivered. The system protects customers rather than putting them at risk.

**Review date:** Annual review, or immediately if the processing scope changes.

---

## 6. PRIVACY BY DESIGN SUMMARY

| Principle | Implementation |
|---|---|
| Data minimisation | Order number only in chat; email retrieved internally; session UUIDs only in logs |
| Purpose limitation | Data collected only for stated purposes; no secondary use |
| Storage limitation | Auto-deletion at end of retention periods; 7 days for health data |
| Integrity and confidentiality | HTTPS throughout; API key authentication; no PII in chat responses |
| Accuracy | Human review of AI-generated content before publishing |
| Transparency | Privacy notice; AI disclosure on first message; contact available at privacy@maisonbeaute.de |
| Accountability | This DPIA; LangSmith audit trail; compliance documentation in GitHub |

---

*GDPR Documentation & DPIA v2.0 | Maison Beauté AI Advisor | March 2026*
*Prepared as part of Ironhack AI Consulting & Integration Bootcamp Final Project*
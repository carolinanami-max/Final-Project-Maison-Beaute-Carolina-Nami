# Maison Beauté AI Advisor — Strategic Deployment & Commercialisation Plan

**Version:** 1.0 | **Date:** April 2026
**Prepared by:** Carolina | namiaistudio.com
**Ironhack AI Consulting & Integration Bootcamp — Final Project**

---

## 1. PHASE ROADMAP

### Phase 1 — POC / Demo (✅ COMPLETE — April 2026)

**Status:** Live and deployed.

| Deliverable | Status |
|---|---|
| 4-module FastAPI backend | ✅ Deployed on Railway |
| 6-page Streamlit UI (editorial dark-navy design) | ✅ Deployed on Streamlit Community Cloud |
| Pinecone RAG (2 namespaces: products + policies) | ✅ Live |
| LangGraph safety routing + n8n email automation | ✅ Live — emails confirmed |
| LangSmith observability (22-case evaluation, 100% pass rate) | ✅ Live |
| EU AI Act Conformity Assessment | ✅ Complete |
| GDPR DPIA | ✅ Complete |
| Railway deployment (FastAPI) | ✅ Live |
| Streamlit Community Cloud deployment (frontend) | ✅ Live |

**Architecture:**
```
GitHub (main) → Railway → FastAPI backend (public URL)
             → Streamlit Community Cloud → Streamlit UI (public URL)
                                         → reads API_BASE from st.secrets
```

**Phase 1 outcome:** Full proof-of-concept demonstrating all four AI modules with production-grade deployment, compliance documentation, and a premium client-facing interface.

---

### Phase 2 — Pilot (Q3 2026, target: 3–5 paying clients)

**Objective:** Validate product-market fit with real beauty marketplace operators in DACH.

**Key deliverables:**
- Onboard 3 pilot clients from DACH pre-loved beauty sector (Vinted sellers, Depop DE, independent re-sellers)
- White-label Streamlit frontend with client brand colours and logo
- Custom Pinecone namespace per client (isolated knowledge base)
- Pilot pricing: €149/month (Starter tier) — first 3 months at €0 against testimonial + data
- Client success tracking: LangSmith per-client project, weekly report
- SLA: 99% uptime for Railway FastAPI backend

**Go/No-Go criteria for Phase 3:**
- ≥2 clients renew after free trial
- Net Promoter Score (NPS) ≥ 7/10
- ≥ 75% of chat queries resolved without human escalation
- Zero GDPR incidents

---

### Phase 3 — Production SaaS (Q1 2027)

**Objective:** Scalable multi-tenant SaaS with self-serve onboarding.

**Key deliverables:**
- Multi-tenant architecture: per-client API keys, isolated Pinecone namespaces, usage metering
- Self-serve onboarding wizard (upload brand guidelines → generate system prompt → deploy)
- Stripe billing integration (Starter / Growth / Enterprise tiers)
- Dedicated Railway environments per enterprise client (optional)
- Dedicated support channel (Slack Connect)
- Expanded AI capabilities: image analysis for product condition grading (Module 1 v2), personalised recommendations (Module 2 v2)
- Partner integrations: Shopify plugin, WooCommerce adapter, Depop webhook

**Phase 3 target metrics:**
- 20+ paying clients
- MRR ≥ €15,000
- Churn < 5%/month
- Average onboarding time < 2 hours

---

## 2. GO-TO-MARKET STRATEGY — DACH PRE-LOVED BEAUTY

### 2.1 Target Market

**Primary:** Pre-loved luxury beauty marketplace operators in DACH
- Solo operators and small teams (1–10 people) with manual product listing and customer service bottlenecks
- Revenue: €50K–€500K GMV/year
- Pain: manual descriptions, no 24/7 support, EU compliance uncertainty

**Secondary:** Adjacent resale verticals open to AI tooling
- Pre-loved fashion (Vinted, Depop DE sellers)
- Multi-brand beauty retailers
- Sustainable beauty subscription boxes

**Market size estimate (DACH):**
- ~2,400 registered beauty resale operators in Germany, Austria, Switzerland (Statista 2025)
- ~15% are marketplace-format with product catalogues ≥50 SKUs
- Addressable: ~360 operators at Starter tier → TAM ~€640K MRR

### 2.2 Go-To-Market Channels

| Channel | Tactic | Timeline |
|---|---|---|
| Direct outreach | LinkedIn DM to founders of DE beauty resale operators. Lead with EU AI Act compliance angle — saves 2–4 weeks of legal work. | Month 1–3 |
| Beauty trade events | Presence at BeautyDüsseldorf, re:publica Berlin, Fairconomy Berlin. Live demo of Streamlit UI. | Month 2–6 |
| Content marketing | LinkedIn articles on EU AI Act impact on beauty e-commerce. SEO posts on "AI for resale beauty". | Month 1–ongoing |
| Referral program | €500 referral credit per client introduced. Activated at Phase 3. | Phase 3 |
| Agency partnerships | Partner with Shopify/WooCommerce agencies serving beauty e-commerce in DACH. Revenue share model. | Phase 3 |

### 2.3 Sales Motion

```
Lead → Live Streamlit demo (30 min) → Pilot proposal (€0 / 3 months)
     → Pilot kickoff (1 week onboarding) → Success review (week 8)
     → Conversion to paid (week 12) → Renewal / upsell (month 6)
```

**Key objection handling:**
- *"We already use ChatGPT"* → ChatGPT is not GDPR-compliant, not EU AI Act conformant, has no safety routing for health mentions, and has no beauty-domain RAG. This system was built specifically for EU beauty resale compliance.
- *"It's too expensive"* → The €149/month Starter replaces 3+ hours/week of founder time (€7,800/year value at freelance rates). Break-even in under 2 weeks.
- *"We're not technical"* → The Streamlit interface requires zero technical knowledge. All operations via browser.

---

## 3. PRICING TIERS

| Tier | Target | Monthly Price | Includes |
|---|---|---|---|
| **Starter** | Solo operators · 1–5 SKUs/day | **€149/month** | All 4 modules · Up to 500 chat sessions/month · Standard Pinecone namespace · LangSmith tracing · Email support |
| **Growth** | Small marketplaces · 5–30 SKUs/day | **€449/month** | Unlimited sessions · Custom brand voice · Dedicated Pinecone namespace · Newsletter Studio with segment delivery · Priority support · Monthly LangSmith report |
| **Enterprise** | Multi-brand platforms | **€1,500+/month** | White-label UI · API access · Custom integrations · Dedicated Railway environment · SLA 99.9% · Dedicated Slack channel · Quarterly compliance review |

**Implementation fee:** €8,000–€12,000 (one-time, waived for Enterprise annual contracts)

**Upsell opportunities:**
- Additional language packs for newsletter: +€50/month per language beyond English
- Custom safety keyword sets per brand: +€100/month
- Additional Pinecone namespaces (e.g. brand heritage content): +€80/month
- Quarterly EU AI Act compliance review: €500/quarter

---

## 4. COMPETITIVE ADVANTAGE

### 4.1 vs. Generic AI Chatbots (ChatGPT, Claude.ai, Gemini)

| Dimension | Maison Beauté AI Advisor | Generic AI |
|---|---|---|
| EU AI Act compliance | ✅ Built-in, documented | ❌ No documentation |
| GDPR DPIA | ✅ Complete | ❌ Not applicable |
| Health/allergy safety routing | ✅ Hard-wired, pre-LLM | ❌ No safety layer |
| Beauty-domain RAG | ✅ Pinecone product + policy namespaces | ❌ Generic knowledge only |
| Zero PII in chat | ✅ Architectural guarantee | ❌ No guarantee |
| Brand voice enforcement | ✅ Prompt-engineered per brand | ❌ Generic tone |
| Ingredient auto-enrichment | ✅ Perplexity API integration | ❌ Not available |

### 4.2 vs. Generic E-commerce Chatbots (Tidio, Gorgias, Intercom AI)

| Dimension | Maison Beauté AI Advisor | Generic E-commerce Chatbots |
|---|---|---|
| Pre-loved beauty domain | ✅ Built for this exact vertical | ❌ Generic retail |
| EU AI Act conformity | ✅ Documented + assessed | ❌ Not addressed |
| Ingredient knowledge | ✅ RAG over product catalogue | ❌ Not available |
| Safety escalation for health mentions | ✅ Keyword-gated, pre-LLM | ❌ No health safety layer |
| Newsletter generation | ✅ Module 4 with segmentation | ❌ Not included |
| Open-source / auditable | ✅ Full code on GitHub | ❌ Black box |

### 4.3 Defensible Moat

1. **EU compliance by design** — not a patch. Competitors offering generic AI tools cannot claim this without a complete rebuild.
2. **Beauty-domain RAG** — Pinecone knowledge base trained on beauty product data, platform policies, and brand voice. Takes months to replicate.
3. **Safety architecture** — LangGraph health/allergy routing that provably keeps sensitive data away from third-party LLMs. A genuine differentiator in the EU market.
4. **Operator trust** — Free pilot + compliance documentation builds trust with risk-averse operators faster than self-serve SaaS tools.

---

## 5. 12-MONTH ROADMAP

### Q2 2026 (Months 1–3) — Pilot Acquisition

| Milestone | Target |
|---|---|
| Phase 1 deployment stable (Railway + Streamlit Cloud) | ✅ Complete |
| First 3 pilot clients onboarded | Month 3 |
| White-label Streamlit frontend (client branding) | Month 2 |
| Per-client Pinecone namespace isolation | Month 2 |
| Client onboarding guide written | Month 1 |
| LinkedIn content series launched (EU AI Act for beauty) | Month 1 |

### Q3 2026 (Months 4–6) — Pilot Validation

| Milestone | Target |
|---|---|
| Pilot NPS collected and ≥ 7/10 | Month 5 |
| ≥2 pilots converted to paid Starter (€149/month) | Month 6 |
| Module 2 v2 scoped: image-based condition grading | Month 5 |
| Shopify integration prototype | Month 6 |
| LangSmith per-client reporting dashboard | Month 4 |

### Q4 2026 (Months 7–9) — Growth Tier Launch

| Milestone | Target |
|---|---|
| Growth tier launched (€449/month) | Month 7 |
| Newsletter Studio: full n8n delivery pipeline per client | Month 7 |
| 5+ paying clients | Month 9 |
| MRR ≥ €2,000 | Month 9 |
| First trade event presence (BeautyDüsseldorf or re:publica) | Month 8 |

### Q1 2027 (Months 10–12) — Production SaaS Foundation

| Milestone | Target |
|---|---|
| Multi-tenant architecture deployed | Month 10 |
| Stripe billing integration live | Month 10 |
| Self-serve onboarding wizard (beta) | Month 11 |
| Enterprise tier first client | Month 12 |
| MRR ≥ €8,000 | Month 12 |
| Annual EU AI Act compliance review completed | Month 12 |

---

## 6. FINANCIAL PROJECTIONS (12-MONTH)

| Month | Clients | MRR | Cumulative Revenue |
|---|---|---|---|
| 1–3 | 0 paid (pilots) | €0 | €0 |
| 4 | 2 × Starter | €298 | €298 |
| 5 | 3 × Starter | €447 | €745 |
| 6 | 3 × Starter + 1 × Growth | €896 | €1,641 |
| 7 | 4 × Starter + 1 × Growth | €1,045 | €2,686 |
| 8 | 4 × Starter + 2 × Growth | €1,494 | €4,180 |
| 9 | 5 × Starter + 2 × Growth | €1,643 | €5,823 |
| 10 | 6 × Starter + 2 × Growth | €1,792 | €7,615 |
| 11 | 6 × Starter + 3 × Growth | €2,241 | €9,856 |
| 12 | 6 × Starter + 3 × Growth + 1 × Enterprise | €3,741 | €13,597 |

**Year 1 target MRR:** €3,741
**Year 1 cumulative revenue:** ~€13,600
**Year 2 target MRR:** €15,000 (20+ clients across all tiers)

---

*Strategic Deployment & Commercialisation Plan v1.0 | Maison Beauté AI Advisor*
*Ironhack AI Consulting & Integration Bootcamp | Berlin, April 2026*

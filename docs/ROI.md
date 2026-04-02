# Maison Beauté AI Advisor — ROI & Risk Assessment

**Project:** Final Project — AI Solution with Compliance & Strategic Implementation
**Student:** Carolina | Ironhack AI Consulting & Integration Bootcamp, Berlin
**Date:** March 2026

---

## 1. BUSINESS BASELINE (Pre-AI)

### 1.1 Revenue Model

| Metric | Value | Source |
|---|---|---|
| Products sold per month | 50 | Founder input |
| Average basket value | €150 | Founder input |
| Platform commission rate | 6.5% | Founder input |
| Monthly GMV | €7,500 | 50 × €150 |
| Monthly commission revenue | €487.50 | €7,500 × 6.5% |
| Annual commission revenue | €5,850 | €487.50 × 12 |
| Premium membership conversion | 1 in 10 new buyers | Founder input |
| Premium membership price | €29.99/year (auto-renewing) | Founder input |
| New premium members/month | ~5 | 50 buyers × 10% |
| Year 1 premium membership revenue | €1,799 | 60 members × €29.99 |
| **Total Year 0 annual revenue** | **~€7,649** | Commission + memberships |

### 1.2 Current Cost Structure

| Metric | Value | Source |
|---|---|---|
| Monthly marketing spend (paid + organic search) | €8,000 | Founder input |
| Annual marketing spend | €96,000 | |
| Cost per acquisition (CPA) | €160 | €8,000 / 50 products |
| Organic search share of traffic | ~15% | Founder input |
| Estimated shop manager salary (Berlin gross) | €70,000/year | Berlin market rate |
| Founder time on manual operations | ~25 hrs/week | Estimated: uploads, emails, logistics |

### 1.3 The Operational Problem

The founder currently performs three full roles manually:
- **Shop manager** — writing every product description, verifying ingredients, uploading listings
- **Customer service agent** — answering all chat, email, and order queries
- **Content/newsletter editor** — when time permits (rarely)

This leaves zero time for the activities that drive growth: SEO improvement, brand and influencer partnerships, catalogue expansion, and customer experience investment.

---

## 2. COST OF THE AI SYSTEM

### 2.1 Implementation Costs (One-Time)

| Item | Cost (EUR) |
|---|---|
| AI consultant — full system build (architecture, code, compliance docs, deployment) | €10,000 |
| Pinecone index setup and initial configuration | €0 (Starter plan) |
| n8n Cloud setup and workflow build | €0 (included in retainer) |
| LangSmith setup | €0 (free tier) |
| **Total one-time implementation cost** | **€10,000** |

### 2.2 Ongoing Monthly Costs

| Item | Year 1 (€/month) | Year 2+ (€/month) |
|---|---|---|
| AI consultant retainer (monitoring, updates, compliance) | €1,500 | €1,500 |
| Anthropic API — Claude Haiku (~100K tokens/day) | €35 | €35 |
| Perplexity API — ingredient lookups (Module 1) | €10 | €10 |
| n8n Cloud — Starter plan | €20 | €20 |
| Pinecone — Starter (Year 1) → Standard (Year 2+) | €0 | €70 |
| HuggingFace embeddings — local inference | €0 | €0 |
| **Total monthly (Year 1)** | **€1,565** | |
| **Total monthly (Year 2+)** | | **€1,635** |

### 2.3 Total Cost Summary

| Period | Cost |
|---|---|
| Year 1 (setup + 12 months operations) | €10,000 + (€1,565 × 12) = **€28,780** |
| Year 2 | €1,635 × 12 = **€19,620** |
| Year 3 | €1,635 × 12 = **€19,620** |
| **3-Year total cost** | **€68,020** |

---

## 3. REVENUE & SAVINGS IMPACT

### 3.1 Growth Assumptions

By freeing the founder from ~25 hrs/week of manual operations, the system unlocks three growth drivers:

| Driver | Impact | Timeline |
|---|---|---|
| SEO-optimised descriptions | Organic traffic grows from 15% → 25% of total | Year 1–2 |
| Faster catalogue throughput | More brand and consignor partnerships possible | Year 2+ |
| 24/7 chatbot availability | Higher conversion rate, fewer abandoned queries | Year 1 |
| Newsletter marketing | Consistent content output (previously impossible) | Year 1 |
| Founder time for strategy | Brand partnerships, influencer deals, market expansion | Year 2+ |

### 3.2 Sales Volume Projection

| Year | Products/Month | Basis |
|---|---|---|
| Year 0 (baseline) | 50 | Current |
| Year 1 | 70 (+40%) | Founder time freed → basic SEO improvement, faster uploads |
| Year 2 | 100 (+43%) | Brand/influencer deals initiated, organic SEO at 25% |
| Year 3 | 150 (+50%) | Compounding effect: broader catalogue, larger customer base |

### 3.3 Commission Revenue Projection

| Year | Products/Month | Monthly GMV | Monthly Commission | Annual Commission |
|---|---|---|---|---|
| Year 0 (baseline) | 50 | €7,500 | €487.50 | €5,850 |
| Year 1 | 70 | €10,500 | €682.50 | €8,190 |
| Year 2 | 100 | €15,000 | €975.00 | €11,700 |
| Year 3 | 150 | €22,500 | €1,462.50 | €17,550 |

### 3.4 Premium Membership Revenue Projection

*Assumes 80% annual renewal rate on existing members.*

| Year | New Members/Month | Cumulative Members | Annual Membership Revenue |
|---|---|---|---|
| Year 0 (baseline) | 5 | 60 | €1,799 |
| Year 1 | 7 | 144 | €4,317 |
| Year 2 | 10 | 264 | €7,917 |
| Year 3 | 15 | 444 | €13,314 |

### 3.5 Cost Savings (Opportunity Value)

| Saving | Annual Value | Basis |
|---|---|---|
| Shop manager role avoided | €70,000 | Berlin gross salary, founder input |
| Customer service time saved (~15 hrs/week) | €39,000 | €50/hr freelance equivalent |
| Newsletter/content creation saved (~3 hrs/week) | €7,800 | €50/hr freelance equivalent |
| **Total annual savings** | **€116,800** | |

### 3.6 Total Annual Value Generated

| Year | Commission Revenue | Membership Revenue | Cost Savings | **Total Value** |
|---|---|---|---|---|
| Year 1 | €8,190 | €4,317 | €116,800 | **€129,307** |
| Year 2 | €11,700 | €7,917 | €116,800 | **€136,417** |
| Year 3 | €17,550 | €13,314 | €116,800 | **€147,664** |

---

## 4. ROI CALCULATIONS

### 4.1 12-Month ROI

```
Total Value Year 1:     €129,307
Total Cost Year 1:      €28,780
Net Benefit Year 1:     €100,527

ROI (12 months) = (€100,527 / €28,780) × 100 = 349% (optimistic)

Conservative (cost savings only, no revenue growth):
Net Benefit: €116,800 − €28,780 = €88,020
ROI (conservative): (€88,020 / €28,780) × 100 = 306%
```

### 4.2 36-Month ROI

```
Total Value (3 years):  €129,307 + €136,417 + €147,664 = €413,388
Total Cost (3 years):   €28,780 + €19,620 + €19,620 = €68,020
Net Benefit (3 years):  €345,368

ROI (36 months) = (€345,368 / €68,020) × 100 = 508%
```

### 4.3 Break-Even Point

```
Monthly value generated (Year 1): €129,307 / 12 = €10,776/month
Monthly system cost (Year 1):     €1,565/month
One-time setup cost:              €10,000

Break-even = €10,000 / (€10,776 − €1,565) = €10,000 / €9,211 ≈ 1.1 months

Including full Year 1 cost spread:
€28,780 / €10,776 = ~2.7 months ≈ 3 months to break-even
```

### 4.4 ROI Summary Table

| Scenario | Net Benefit | ROI | Break-Even |
|---|---|---|---|
| 12-month conservative (savings only) | €88,020 | **306%** | ~3 months |
| 12-month optimistic (savings + growth) | €100,527 | **349%** | ~3 months |
| 36-month | €345,368 | **508%** | ~3 months |

**The biggest assumption driving these numbers:** The €70,000/year shop manager saving. This alone recovers the full Year 1 cost in under 3 months. All revenue growth projections are additional upside.

---

## 5. RISK MATRIX

*Scoring: Likelihood (1–5) × Impact (1–5) = Risk Score. Score ≥ 12 = High, 6–11 = Medium, ≤ 5 = Low.*

| ID | Risk | Likelihood | Impact | Score | Rating | Mitigation |
|---|---|---|---|---|---|---|
| R1 | **Ingredient hallucination** — Perplexity returns inaccurate or outdated ingredients for a product batch | 3 | 4 | **12** | 🔴 High | Batch number traceability; `ingredients_verified: false` by default; human review mandatory before publishing; measured language enforced in prompt (no absolute claims) |
| R2 | **Low founder adoption** — system too complex for daily use without technical support | 3 | 4 | **12** | 🔴 High | Streamlit interface requires zero technical knowledge; all operations via browser; retainer covers ongoing support and training |
| R3 | **Safety escalation false negative** — allergy/health mention not caught by keyword scanner | 2 | 5 | **10** | 🟠 Medium | Monthly review of keyword list; LangSmith monitoring for unusual patterns; false negatives logged and used to expand the keyword set |
| R4 | **GDPR violation** — PII inadvertently logged in chat or LangSmith traces | 2 | 5 | **10** | 🟠 Medium | Privacy-by-design architecture; anonymised session UUIDs only; no PII in chat responses; auto-deletion after 90 days; DPIA completed |
| R5 | **SEO descriptions don't improve organic traffic** — expected growth from 15% → 25% doesn't materialise | 3 | 3 | **9** | 🟠 Medium | A/B test descriptions; monthly LangSmith quality audit; prompt refinement based on performance data; quarterly SEO review |
| R6 | **Brand/influencer partnerships don't materialise** — Year 2–3 growth depends on these | 3 | 3 | **9** | 🟠 Medium | Timeline is Year 2+, not Year 1 dependency; conservative ROI (306%) does not include this growth driver; founder time freed to pursue these actively |
| R7 | **API downtime** — Anthropic, Perplexity, or Pinecone unavailability affects customer experience | 2 | 3 | **6** | 🟡 Low | Graceful error handling in all endpoints; fallback responses for chatbot; LangSmith alerts on error rate spikes |
| R8 | **EU AI Act reclassification to High Risk** — regulatory guidance evolves and system is reclassified | 1 | 4 | **4** | 🟡 Low | Annual compliance review scheduled; documentation maintained in GitHub; retainer includes regulatory monitoring |

### 5.1 Risk Priority Summary

**Highest priority risks (Score 12):**
- R1 Ingredient hallucination — mitigated by human-in-the-loop review and batch traceability
- R2 Founder adoption — mitigated by Streamlit UI and ongoing retainer support

**Key insight:** The two highest-rated risks are both already mitigated by design decisions made during the build:
- R1 → The `pending_review` status and `ingredients_verified: false` flag were specifically designed for this
- R2 → The Streamlit interface with 5 intuitive tabs was built to avoid any dependency on technical knowledge

---

## 6. COMMERCIALISATION MODEL

### 6.1 Pricing Tiers (Scalable SaaS)

| Tier | Target | Monthly Price | Includes |
|---|---|---|---|
| Starter | Solo operators (1–5 SKUs/day) | €149/month | All 4 modules, up to 500 chat sessions/month |
| Growth | Small marketplaces | €449/month | Unlimited sessions, custom brand voice, LangSmith access |
| Enterprise | Multi-brand platforms | €1,500+/month | White-label, API access, custom integrations |

### 6.2 Implementation Fee

One-time setup fee: **€8,000–€12,000** depending on integration complexity.

### 6.3 Competitive Advantage

- Privacy-first architecture (no PII in chat) — EU market differentiator
- Pre-built EU AI Act + GDPR compliance documentation — saves clients 2–4 weeks of legal work
- Perplexity-powered ingredient enrichment — no manual research needed
- Beauty-domain-specific prompt engineering — not a generic chatbot
- Cloud-deployed (Railway + Streamlit Community Cloud) — no client infrastructure required

---

## 7. MODULE 4 NEWSLETTER VALUE (UPDATED)

### 7.1 Time Saving — Newsletter Automation

The Newsletter Generator (Module 4) was previously accounted for in Section 3.5 as "Newsletter/content creation saved (~3 hrs/week) → €7,800/year." The following provides a granular breakdown.

| Task automated | Manual time | Frequency | Annual hours saved |
|---|---|---|---|
| Newsletter copy drafting | 90 min | Weekly | 78 hrs/year |
| Multi-language adaptation | 45 min per language | Weekly (if applicable) | 39 hrs/year per language |
| Product feature selection and writeup | 30 min | Weekly | 26 hrs/year |
| Subject line and preview text testing | 20 min | Weekly | 17 hrs/year |
| **Total (English only)** | **~3 hrs/week** | | **~160 hrs/year** |

At €50/hour freelance equivalent: **€8,000/year** (revised upward from €7,800).

### 7.2 Revenue Uplift — Personalised Newsletters with Discount Codes

The Newsletter Studio's personalisation toggle enables segmented campaigns with auto-generated discount codes (e.g. `MB-SKIN-20` for skincare enthusiasts).

**Conversion uplift estimate:**

| Segment | Recipients | Baseline conversion | Personalised conversion (est.) | Uplift |
|---|---|---|---|---|
| All subscribers | 1,240 | 2.5% | 3.0% | +0.5% |
| Skincare enthusiasts | 380 | 3.5% | 5.0% | +1.5% |
| Fragrance collectors | 210 | 3.0% | 4.5% | +1.5% |
| VIP members | 45 | 5.0% | 7.0% | +2.0% |

**Revenue model (weekly newsletter to Skincare Enthusiasts):**
```
380 recipients × 5.0% conversion = 19 purchases
19 purchases × €150 avg basket × 6.5% commission = €185.25/newsletter
Baseline (3.5%): 13 purchases → €126.75/newsletter
Personalisation uplift: +€58.50/newsletter → +€3,042/year (52 sends)
```

**Estimated annual revenue uplift from personalised segmented newsletters: ~€3,000–€8,000** depending on send frequency and segment mix.

### 7.3 Customer Segmentation Capability

The segment selector supports 5 customer segments out of the box:

| Segment | Size | Use case |
|---|---|---|
| All subscribers | 1,240 | Broad announcements, seasonal campaigns |
| Skincare enthusiasts | 380 | Skin-care product drops, ingredient education |
| Fragrance collectors | 210 | New fragrance arrivals, layering guides |
| New customers | 95 | Welcome series, brand introduction |
| VIP members | 45 | Early access, exclusive discounts, loyalty rewards |

Segmentation data is currently mock — in production, this would be pulled from the CRM/email platform (e.g. Brevo, Klaviyo) via API.

---

*ROI & Risk Assessment v2.0 | Maison Beauté AI Advisor | Ironhack Berlin, April 2026*
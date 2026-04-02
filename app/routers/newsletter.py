# app/routers/newsletter.py
import json
import os
import httpx
from fastapi import APIRouter, HTTPException
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / "data" / ".env")

router = APIRouter()

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0.8,
    max_tokens=2048,
)

N8N_NEWSLETTER_WEBHOOK = os.getenv(
    "N8N_NEWSLETTER_WEBHOOK",
    "https://cvn.app.n8n.cloud/webhook/maison-beaute-newsletter"
)
NEWSLETTER_RECIPIENT = os.getenv("NEWSLETTER_RECIPIENT", "carolinanami@gmail.com")


class NewsletterRequest(BaseModel):
    trending_topics: list[str] = Field(..., example=["glass skin", "sustainable beauty", "fragrance layering"])
    new_products: list[str] = Field(default=[], example=["Charlotte Tilbury Pillow Talk Lipstick", "La Mer Crème"])
    tone: str = Field(default="sophisticated", example="sophisticated")
    language: str = Field(default="English", example="English")
    send_email: bool = Field(default=True, description="Whether to send the newsletter as a formatted email")


class NewsletterResponse(BaseModel):
    subject_line: str
    preview_text: str
    body: str
    cta: str
    email_sent: bool = False


NEWSLETTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Maison Beauté newsletter editor.
Maison Beauté is a premium pre-loved luxury beauty marketplace based in Berlin.
Tone: sophisticated, warm, slightly French-inflected, sustainability-conscious.

Write a newsletter in EXACTLY this JSON structure — no markdown fences:
{{
  "subject_line": "...",
  "preview_text": "...",
  "body": "...",
  "cta": "..."
}}

Rules:
- subject_line: max 60 chars, intriguing and on-brand
- preview_text: max 90 chars, complements the subject line
- body: 150-200 words, 3 short paragraphs covering trends + new arrivals + sustainability angle
- cta: one compelling call-to-action sentence
- Always weave in the sustainability/circular beauty angle
- Never make medical claims about products
- Write in the specified language
"""),
    ("human", "Write a newsletter about these trending topics: {topics}\nNew products: {products}\nLanguage: {language}"),
])

chain = NEWSLETTER_PROMPT | llm


@router.post("/generate", response_model=NewsletterResponse)
@traceable(name="generate_newsletter", tags=["module-4", "newsletter"])
async def generate_newsletter(request: NewsletterRequest) -> NewsletterResponse:
    """
    Module 4 — Newsletter Generator.
    Generates an on-brand newsletter and optionally sends it as a formatted HTML email via n8n.
    """
    try:
        # ── Step 1: Generate content with Claude Haiku ──────────────
        result = await chain.ainvoke({
            "topics": ", ".join(request.trending_topics),
            "products": ", ".join(request.new_products) if request.new_products else "none specified",
            "language": request.language,
        })

        raw = result.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        parsed = json.loads(raw)
        newsletter = NewsletterResponse(**parsed)

        # ── Step 2: Fire to n8n for HTML email delivery ─────────────
        if request.send_email:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.post(N8N_NEWSLETTER_WEBHOOK, json={
                        "subject_line": newsletter.subject_line,
                        "preview_text": newsletter.preview_text,
                        "body": newsletter.body,
                        "cta": newsletter.cta,
                        "topics": request.trending_topics,
                        "language": request.language,
                        "recipient": NEWSLETTER_RECIPIENT,
                    })
                newsletter.email_sent = True
            except Exception:
                # Email delivery is best-effort — don't fail the request
                newsletter.email_sent = False

        return newsletter

    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail=f"LLM returned invalid JSON: {result.content[:300]}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
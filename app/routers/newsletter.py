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
    ("system", """You are the editorial director of Maison Beauté, a premium pre-loved luxury beauty marketplace in Berlin.
Your writing is sophisticated, warm, and slightly French-inflected — think Vogue Paris meets conscious consumption.
Every newsletter is a curated editorial moment, not a sales email.

Write a newsletter in EXACTLY this JSON structure — no markdown fences:
{{
  "subject_line": "...",
  "preview_text": "...",
  "body": "...",
  "cta": "..."
}}

Rules:
- subject_line: max 70 chars — poetic, intriguing, never generic
- preview_text: max 100 chars — a whisper that makes you want to open
- body: 280-340 words across 4 paragraphs structured as follows:
    Paragraph 1 (opening, 60-70 words): A beautiful, atmospheric scene-setter about the season, the mood, or a cultural moment in beauty. Written in italic-worthy prose. No product names yet.
    Paragraph 2 (trend, 70-80 words): Explore the trending topics with depth and nuance — reference the cultural shift, the ritual, the feeling. Weave in 1-2 product mentions naturally, not as a list.
    Paragraph 3 (curation, 70-80 words): Introduce the featured products as a curated edit — describe their textures, results, and why they belong together. Make the reader feel they are being personally guided by an expert.
    Paragraph 4 (sustainability, 50-60 words): A closing thought on circular beauty — elegant, never preachy. Why choosing pre-loved is an act of taste, not compromise.
- cta: one compelling sentence — an invitation, not a command. Max 12 words.
- Separate paragraphs with a blank line (double newline).
- Never make medical claims.
- Write in the specified language.
- Never use the word "luxury" more than twice in the entire body.
- Never start two consecutive sentences with "The".
"""),
    ("human", "Write a newsletter about these trending topics: {topics}\nNew products to feature: {products}\nLanguage: {language}"),
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
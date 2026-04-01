# app/routers/newsletter.py
import json
from fastapi import APIRouter, HTTPException
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from pydantic import BaseModel, Field

router = APIRouter()

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0.8,
    max_tokens=2048,
)

class NewsletterRequest(BaseModel):
    trending_topics: list[str] = Field(..., example=["glass skin", "sustainable beauty", "fragrance layering"])
    new_products: list[str] = Field(default=[], example=["Charlotte Tilbury Pillow Talk Lipstick", "La Mer Crème"])
    tone: str = Field(default="sophisticated", example="sophisticated")
    language: str = Field(default="English", example="English")

class NewsletterResponse(BaseModel):
    subject_line: str
    preview_text: str
    body: str
    cta: str

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
    """Generate a Maison Beauté newsletter based on trending topics and new products."""
    try:
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
        return NewsletterResponse(**parsed)

    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail=f"LLM returned invalid JSON: {result.content[:300]}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
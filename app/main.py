# app/main.py
from dotenv import load_dotenv
from pathlib import Path

# ─── Load .env first, before any other imports ────────────────
load_dotenv(Path(__file__).parent.parent / "data" / ".env")

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.langsmith_config import setup_langsmith
from app.core.rag_pipeline import build_vectorstore, load_knowledge_base
from app.routers import descriptions, chatbot, orders, newsletter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    # 1. LangSmith tracing
    setup_langsmith()
    print("✅ LangSmith tracing configured")

    # 2. Load knowledge base into Pinecone
    print("⏳ Loading knowledge base into Pinecone...")
    try:
        data_dir = Path(__file__).parent.parent / "data"
        print(f"  Looking for documents in: {data_dir}")

        # Module 2 namespace — product catalogue only
        product_docs = load_knowledge_base(
            data_dir=str(data_dir),
            filenames=["product_catalogue_knowledge_base.md"]
        )
        if product_docs:
            build_vectorstore(product_docs, namespace="products")

        # Module 3 namespace — FAQ + policies only
        policy_docs = load_knowledge_base(
            data_dir=str(data_dir),
            filenames=["faq_knowledge_base.md", "policies.md"]
        )
        if policy_docs:
            build_vectorstore(policy_docs, namespace="policies")

    except Exception as e:
        print(f"❌ Pinecone setup failed: {e}")
        print("   RAG will not work until this is resolved.")

    yield
    print("👋 Shutting down Maison Beauté AI Advisor")


app = FastAPI(
    title="Maison Beauté AI Advisor",
    description="Privacy-first AI system for pre-loved luxury beauty — Modules 1, 2, 3 & Newsletter",
    version="2.0.0",
    lifespan=lifespan,
)

# ─── Routers ──────────────────────────────────────────────────
app.include_router(descriptions.router, prefix="/products",   tags=["Module 1 — Shop Manager"])
app.include_router(chatbot.router,      prefix="/chat",        tags=["Module 2 — Beauty Advisor"])
app.include_router(orders.router,       prefix="/orders",      tags=["Module 3 — Customer Self-Service"])
app.include_router(newsletter.router,   prefix="/newsletter",  tags=["Module 4 — Newsletter Generator"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Maison Beauté AI Advisor",
        "version": "2.0.0",
        "status": "running",
        "modules": ["M1 Shop Manager", "M2 Beauty Advisor", "M3 Customer Self-Service", "M4 Newsletter Generator"],
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
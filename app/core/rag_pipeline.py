# app/core/rag_pipeline.py
import os
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pinecone import Pinecone

# ─── Pinecone client (v6) ─────────────────────────────────────
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(host=os.getenv("PINECONE_HOST"))

# ─── Models ───────────────────────────────────────────────────
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0.3,
    max_tokens=1024,
)

# ─── Chunking strategy ────────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "],
)

# ─── RAG Prompt ───────────────────────────────────────────────
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are Beauté, the AI beauty advisor for Maison Beauté — \
a premium pre-loved luxury beauty marketplace in Berlin.

Your tone: warm, knowledgeable, sophisticated, honest.

Answer the customer's question using ONLY the context provided below.
If the answer is not in the context, say you don't have that information \
and offer to connect them with the team at hello@maisonbeaute.de

Rules:
- Never make absolute medical or dermatological claims
- Use measured language: 'known for', 'may help with', 'traditionally used for'
- You are an AI — never claim to be human
- Keep answers concise and helpful

Context:
{context}"""),
    ("human", "{question}"),
])

# ─── Vector store ─────────────────────────────────────────────
_vectorstore: PineconeVectorStore | None = None


def build_vectorstore(documents: list[Document], namespace: str = "") -> PineconeVectorStore:
    """Chunk documents, embed them, and upsert into Pinecone namespace."""
    global _vectorstore
    chunks = splitter.split_documents(documents)
    vs = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=os.getenv("PINECONE_INDEX_NAME", "maison-beaute-advisor"),
        namespace=namespace,
    )
    if not namespace:
        _vectorstore = vs
    print(f"✅ Pinecone [{namespace or 'default'}] — {len(chunks)} chunks upserted")
    return vs


def get_vectorstore(namespace: str = "") -> PineconeVectorStore:
    """Return vectorstore for a specific namespace."""
    global _vectorstore
    if namespace:
        return PineconeVectorStore(
            index=index,
            embedding=embeddings,
            namespace=namespace,
        )
    if _vectorstore is None:
        _vectorstore = PineconeVectorStore(
            index=index,
            embedding=embeddings,
        )
        print("✅ Connected to existing Pinecone index")
    return _vectorstore


def build_rag_chain(namespace: str = ""):
    """Build RAG chain using modern LangChain LCEL syntax."""
    retriever = get_vectorstore(namespace=namespace).as_retriever(search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain


def load_knowledge_base(data_dir: str = "data", filenames: list[str] | None = None) -> list[Document]:
    """Load .md files from data/ directory. Optionally filter by filename list."""
    documents = []
    data_path = Path(data_dir)

    files = [data_path / f for f in filenames] if filenames else list(data_path.glob("*.md"))

    for file in files:
        if file.exists():
            text = file.read_text(encoding="utf-8")
            documents.append(Document(page_content=text, metadata={"source": file.name}))
            print(f"  Loaded: {file.name}")
        else:
            print(f"  ⚠️ Not found: {file.name}")

    if not documents:
        print("⚠️  No documents loaded.")

    return documents
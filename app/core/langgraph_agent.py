# app/core/langgraph_agent.py
import os
from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END
from langsmith import traceable
from dotenv import load_dotenv

load_dotenv()

# ─── State definition ─────────────────────────────────────────
class ChatState(TypedDict):
    message: str
    session_id: str
    chat_history: list
    safety_flagged: bool
    response: str


# ─── Safety keyword list ──────────────────────────────────────
SAFETY_KEYWORDS = [
    "allergy", "allergic", "reaction", "rash", "hives", "swelling",
    "anaphylaxis", "itching", "burning", "irritation", "redness",
    "broke out", "bad reaction", "skin reaction", "nut allergy",
    "fragrance allergy", "latex", "patch test",
]


# ─── Nodes ────────────────────────────────────────────────────
@traceable(name="safety_check", tags=["module-2", "safety"])
def safety_check_node(state: ChatState) -> ChatState:
    """
    Keyword-based safety detection.
    Runs BEFORE any LLM call — health data never reaches Anthropic if flagged.
    """
    message_lower = state["message"].lower()
    flagged = any(keyword in message_lower for keyword in SAFETY_KEYWORDS)
    return {**state, "safety_flagged": flagged}


def route_after_safety(state: ChatState) -> Literal["escalate", "rag_response"]:
    """Conditional edge: routes to escalation or normal RAG response."""
    return "escalate" if state["safety_flagged"] else "rag_response"


@traceable(name="safety_escalation", tags=["module-2", "safety"])
def escalate_node(state: ChatState) -> ChatState:
    """
    Triggered when a safety keyword is detected.
    - Fires n8n webhook → Gmail safety alert to founder
    - Returns a safe holding response to the customer
    - Does NOT call the LLM
    """
    import httpx

    try:
        httpx.post(
            "https://cvn.app.n8n.cloud/webhook/beauty-advisor",
            json={
                "session_id": state["session_id"],
                "message": state["message"],
            },
            timeout=5.0,
        )
        print(f"✅ Safety alert fired to n8n for session {state['session_id']}")
    except Exception as e:
        print(f"⚠️  n8n safety alert failed: {e} — continuing with holding response")

    response = (
        "Thank you for sharing this with us. Your safety is our absolute priority. "
        "A member of our team will be in touch with you shortly to assist. "
        "If you are experiencing a medical emergency, please contact emergency services immediately."
    )
    return {**state, "response": response}


@traceable(name="beauty_advisor_response", tags=["module-2", "chatbot"])
def rag_response_node(state: ChatState) -> ChatState:
    """
    Normal RAG-based beauty advice response.
    Retrieves relevant product context from Pinecone,
    generates answer via Claude Haiku.
    """
    from app.core.rag_pipeline import build_rag_chain

    rag_chain = build_rag_chain(namespace="products")
    response = rag_chain.invoke(state["message"])
    return {**state, "response": response}


# ─── Build LangGraph ──────────────────────────────────────────
def build_agent() -> StateGraph:
    graph = StateGraph(ChatState)

    graph.add_node("safety_check", safety_check_node)
    graph.add_node("escalate", escalate_node)
    graph.add_node("rag_response", rag_response_node)

    graph.set_entry_point("safety_check")
    graph.add_conditional_edges("safety_check", route_after_safety)
    graph.add_edge("escalate", END)
    graph.add_edge("rag_response", END)

    return graph.compile()


# Module-level compiled agent
agent = build_agent()
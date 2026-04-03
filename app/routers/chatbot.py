# app/routers/chatbot.py
from fastapi import APIRouter, HTTPException
from langsmith import traceable

from app.core.langgraph_agent import agent
from app.core.rag_pipeline import build_rag_chain
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/", response_model=ChatResponse)
@traceable(name="beauty_advisor_endpoint", tags=["module-2", "chatbot"])
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Module 2 — Beauty Advisor Chatbot.
    RAG over products namespace. Safety escalation via LangGraph.
    """
    try:
        initial_state = {
            "message": request.message,
            "session_id": request.session_id,
            "chat_history": [
                {"role": m.role, "content": m.content}
                for m in request.chat_history
            ],
            "safety_flagged": False,
            "response": "",
        }

        result = agent.invoke(initial_state)

        return ChatResponse(
            session_id=request.session_id,
            response=result["response"],
            safety_flagged=result["safety_flagged"],
            escalated=result["safety_flagged"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/faq", response_model=ChatResponse)
@traceable(name="faq_advisor_endpoint", tags=["module-3", "faq", "policies"])
async def faq(request: ChatRequest) -> ChatResponse:
    """
    Module 3 — FAQ & Policy Assistant.
    RAG over policies namespace only. No safety escalation needed.
    """
    try:
        rag_chain = build_rag_chain(namespace="policies")
        response = rag_chain.invoke(request.message)

        return ChatResponse(
            session_id=request.session_id,
            response=response,
            safety_flagged=False,
            escalated=False,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
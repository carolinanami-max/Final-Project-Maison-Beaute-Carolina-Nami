# app/models/chat.py
from pydantic import BaseModel, Field
from typing import Literal


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Input payload for Module 2 — Beauty Advisor Chatbot."""

    session_id: str = Field(..., example="sess_abc123")
    message: str = Field(..., example="Does this serum work for sensitive skin?")
    chat_history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """Response from Module 2."""

    session_id: str
    response: str
    safety_flagged: bool = False
    escalated: bool = False


class OrderRequest(BaseModel):
    """Input payload for Module 3 — Order Concierge."""

    order_number: str = Field(..., example="MB-ORD-20241127-0042")


class OrderResponse(BaseModel):
    """
    Response from Module 3.
    Always returns brief status only — full details sent to email on file.
    Zero PII in this response by design.
    """

    order_number: str
    status_summary: str
    email_sent: bool = False
    message: str = "Full tracking details have been sent to your registered email address."

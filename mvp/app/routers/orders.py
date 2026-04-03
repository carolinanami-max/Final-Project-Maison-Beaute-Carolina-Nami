# app/routers/orders.py
import os

import httpx
from fastapi import APIRouter, HTTPException
from langsmith import traceable
from dotenv import load_dotenv

from app.models.chat import OrderRequest, OrderResponse

load_dotenv()

router = APIRouter()

FULFILMENT_API_URL = os.getenv("FULFILMENT_API_URL", "")
FULFILMENT_API_KEY = os.getenv("FULFILMENT_API_KEY", "")


@router.post("/track", response_model=OrderResponse)
@traceable(name="order_status_response", tags=["module-3", "order-concierge"])
async def track_order(request: OrderRequest) -> OrderResponse:
    """
    Module 3 — Order Concierge.

    Privacy-by-design:
    - Input: order number only (no name, no email, no address)
    - Process: internal DB lookup retrieves email address
    - Output in chat: brief status only — zero PII
    - Full tracking details sent directly to email on file via MCP
    """
    try:
        # ── Step 1: Query fulfilment API ───────────────────────
        # TODO: replace mock with real fulfilment API call
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         f"{FULFILMENT_API_URL}/{request.order_number}",
        #         headers={"Authorization": f"Bearer {FULFILMENT_API_KEY}"},
        #     )
        #     response.raise_for_status()
        #     order_data = response.json()

        # Mock order data for development
        order_data = _mock_order_lookup(request.order_number)

        if not order_data:
            raise HTTPException(
                status_code=404,
                detail=f"Order {request.order_number} not found."
            )

        # ── Step 2: Format brief in-chat status ───────────────
        status_summary = _format_status_summary(order_data["status"])

        # ── Step 3: Send full details to email on file via n8n ─
        # Email address is retrieved internally — never returned in this response
        email_sent = False
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(
                    "https://cvn.app.n8n.cloud/webhook/customer-service",
                    json={
                        "message": request.order_number,
                        "session_id": f"order-{request.order_number}",
                        "order_number": request.order_number,
                        "status_summary": status_summary,
                        "customer_email": order_data.get("customer_email"),
                        "carrier": order_data.get("carrier"),
                        "tracking_number": order_data.get("tracking_number"),
                        "estimated_delivery": order_data.get("estimated_delivery"),
                    },
                )
            email_sent = True
            print(f"✅ Order email triggered via n8n for {request.order_number}")
        except Exception as e:
            print(f"⚠️  n8n order email failed: {e} — order status still returned")

        return OrderResponse(
            order_number=request.order_number,
            status_summary=status_summary,
            email_sent=email_sent,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _format_status_summary(status: str) -> str:
    """Maps internal status codes to customer-friendly messages."""
    STATUS_MAP = {
        "processing":   "Your order is being prepared 🛍️",
        "shipped":      "Your order is on its way! 📦",
        "out_for_delivery": "Your order is out for delivery today 🚚",
        "delivered":    "Your order has been delivered ✅",
        "cancelled":    "Your order has been cancelled.",
        "returned":     "Your return is being processed.",
    }
    return STATUS_MAP.get(status.lower(), "We're looking into your order status.")


def _mock_order_lookup(order_number: str) -> dict | None:
    """
    Mock fulfilment data for development and POC demo.
    Replace with real API call in production.
    """
    mock_orders = {
        "MB-ORD-20241127-0042": {
            "order_number": "MB-ORD-20241127-0042",
            "status": "shipped",
            "carrier": "DHL",
            "tracking_number": "1234567890",
            "estimated_delivery": "2024-11-30",
            # Email retrieved internally — never returned to chat
            "customer_email": "customer@example.com",
        },
        "MB-ORD-20241128-0099": {
            "order_number": "MB-ORD-20241128-0099",
            "status": "processing",
            "carrier": None,
            "tracking_number": None,
            "estimated_delivery": "2024-12-02",
            "customer_email": "another@example.com",
        },
    }
    return mock_orders.get(order_number)
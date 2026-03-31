# app/models/product.py
from pydantic import BaseModel, Field
from typing import Literal


class ProductInput(BaseModel):
    """Input payload for Module 1 — Shop Manager Agent."""

    product_id: str = Field(..., example="MB-2024-0847")
    brand: str = Field(..., example="Charlotte Tilbury")
    product_name: str = Field(..., example="Pillow Talk Lipstick")
    category: Literal[
        "Make-up",
        "Parfumes",
        "Skin-care",
        "Body-care",
        "Hair-care",
        "Beauty Tools",
    ] = Field(..., example="Make-up")
    condition: Literal[
        "New",
        "Tested Out",
        "Pre-loved",
    ] = Field(
        ...,
        example="Tested Out",
        description=(
            "New = never used, sealed. "
            "Tested Out = at least 90% of product remains. "
            "Pre-loved = at least 50% of product remains. "
            "All products sold in original packaging, sealed after quality & hygiene check."
        ),
    )
    batch_number: str = Field(
        ...,
        example="B2024-09-CT",
        description="Batch number from product packaging. Used for ingredient traceability and formula version tracking."
    )
    expiry_date: str = Field(
        ...,
        example="2026-09",
        description="Expiry or best-before date from packaging (YYYY-MM format). Products past expiry cannot be listed."
    )
    original_retail_price_eur: float = Field(..., example=39.0)
    listing_price_eur: float = Field(..., example=22.0)
    key_ingredients: list[str] | None = Field(
        default=None,
        example=["Vitamin E", "Shea Butter"],
        description="Optional — manually verified ingredients to include. If provided, these take priority over Perplexity results."
    )
    size_value: float | None = Field(None, example=3.5)
    size_unit: Literal["ml", "g"] | None = Field(None, example="g")


class ProductDescription(BaseModel):
    """Output from Module 1 — generated product listing, pending human review."""

    product_id: str
    batch_number: str
    expiry_date: str
    title: str
    tagline: str
    description: str
    seo_tags: list[str]
    condition_note: str
    ingredients_source: str = Field(
        description="'perplexity' | 'manual' | 'perplexity+manual'"
    )
    ingredients_verified: bool = Field(
        default=False,
        description="False until a human reviewer confirms ingredients match the physical product packaging for this specific batch."
    )
    status: Literal["pending_review", "approved", "rejected"] = Field(
        default="pending_review",
        description="All descriptions start as pending_review. Must be approved by founder before publishing to catalogue."
    )
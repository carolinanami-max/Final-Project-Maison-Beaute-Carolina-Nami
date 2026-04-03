# app/core/ingredient_lookup.py
import os
import httpx
from langsmith import traceable


PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


@traceable(name="ingredient_lookup", tags=["module-1", "perplexity"])
async def fetch_ingredients(brand: str, product_name: str) -> list[str]:
    """
    Query Perplexity API to find key ingredients for a given beauty product.
    Returns a list of ingredient strings.
    Falls back to empty list if lookup fails — description will still generate.
    """
    api_key = os.getenv("PERPLEXITY_KEY")
    if not api_key:
        print("⚠️  PERPLEXITY_API_KEY not set — skipping ingredient lookup")
        return []

    query = (
        f"What are the key ingredients in {brand} {product_name}? "
        f"List only the ingredient names, comma-separated, no descriptions. "
        f"Maximum 8 ingredients."
    )

    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a beauty product ingredient expert. "
                    "When asked about ingredients, respond ONLY with a comma-separated "
                    "list of ingredient names. No explanations, no numbering, no extra text."
                ),
            },
            {"role": "user", "content": query},
        ],
        "max_tokens": 200,
        "temperature": 0.1,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                PERPLEXITY_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            raw = data["choices"][0]["message"]["content"].strip()

            # Parse comma-separated ingredient list
            ingredients = [i.strip() for i in raw.split(",") if i.strip()]
            print(f"✅ Perplexity found {len(ingredients)} ingredients for {brand} {product_name}")
            return ingredients

    except httpx.TimeoutException:
        print(f"⚠️  Perplexity timeout for {brand} {product_name} — using manual ingredients only")
        return []
    except Exception as e:
        print(f"⚠️  Perplexity lookup failed: {e} — using manual ingredients only")
        return []


def merge_ingredients(
    perplexity_ingredients: list[str],
    manual_ingredients: list[str] | None,
) -> tuple[list[str], str]:
    """
    Merge Perplexity-fetched and manually provided ingredients.
    Returns (merged_list, source_label).
    """
    if not perplexity_ingredients and not manual_ingredients:
        return [], "none"

    if not perplexity_ingredients:
        return manual_ingredients, "manual"

    if not manual_ingredients:
        return perplexity_ingredients, "perplexity"

    # Merge — deduplicate case-insensitively, preserve order
    seen = {i.lower() for i in perplexity_ingredients}
    merged = list(perplexity_ingredients)
    for ingredient in manual_ingredients:
        if ingredient.lower() not in seen:
            merged.append(ingredient)
            seen.add(ingredient.lower())

    return merged, "perplexity+manual"
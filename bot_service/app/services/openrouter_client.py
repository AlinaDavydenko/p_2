import httpx

from app.core.config import settings


class OpenRouterError(Exception):
    """Raised when OpenRouter request fails or returns an unexpected response."""


async def call_openrouter(prompt: str) -> str:
    """Send a chat completion request to OpenRouter and return the reply text."""
    url = f"{settings.OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,
        "X-Title": settings.OPENROUTER_APP_NAME,
    }
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
    except httpx.HTTPError as exc:
        raise OpenRouterError(f"Network error calling OpenRouter: {exc}") from exc

    if response.status_code != 200:
        raise OpenRouterError(
            f"OpenRouter returned status {response.status_code}: {response.text}"
        )

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise OpenRouterError(f"Unexpected OpenRouter response shape: {data}") from exc

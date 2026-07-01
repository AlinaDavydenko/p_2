import httpx
import pytest
import respx

from app.core.config import settings
from app.services.openrouter_client import call_openrouter

pytestmark = pytest.mark.asyncio


@respx.mock
async def test_call_openrouter_returns_text():
    url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"
    route = respx.post(url).mock(
        return_value=httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": "Привет! Чем могу помочь?"}}
                ]
            },
        )
    )

    result = await call_openrouter("Привет!")

    assert route.called
    assert result == "Привет! Чем могу помочь?"

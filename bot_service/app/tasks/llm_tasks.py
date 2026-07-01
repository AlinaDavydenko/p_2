import asyncio

from aiogram import Bot

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterError, call_openrouter


async def _run_llm_request(tg_chat_id: int, prompt: str) -> str:
    try:
        answer = await call_openrouter(prompt)
    except OpenRouterError as exc:
        answer = f"Не удалось получить ответ от LLM: {exc}"

    if settings.TELEGRAM_BOT_TOKEN:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        try:
            await bot.send_message(chat_id=tg_chat_id, text=answer)
        finally:
            await bot.session.close()

    return answer


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> str:
    """Celery task: call the LLM via OpenRouter and deliver the answer to Telegram."""
    return asyncio.run(_run_llm_request(tg_chat_id, prompt))

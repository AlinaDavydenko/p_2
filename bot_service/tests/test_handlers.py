from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from jose import jwt

from app.bot import handlers
from app.core.config import settings

pytestmark = pytest.mark.asyncio


def _make_token(sub: str = "user-1", role: str = "user") -> str:
    return jwt.encode({"sub": sub, "role": role}, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def _make_message(tg_user_id: int, text: str | None = None):
    message = SimpleNamespace()
    message.from_user = SimpleNamespace(id=tg_user_id)
    message.chat = SimpleNamespace(id=tg_user_id)
    message.text = text
    message.answer = AsyncMock()
    return message


def _make_command(args: str | None):
    return SimpleNamespace(args=args)


async def test_token_command_saves_token_in_redis(patch_redis):
    token = _make_token()
    message = _make_message(tg_user_id=555, text=f"/token {token}")
    command = _make_command(args=token)

    await handlers.handle_token_command(message, command)

    stored = await patch_redis.get("token:555")
    assert stored == token
    message.answer.assert_awaited_once()


async def test_token_command_rejects_invalid_token(patch_redis):
    message = _make_message(tg_user_id=555, text="/token garbage")
    command = _make_command(args="garbage")

    await handlers.handle_token_command(message, command)

    stored = await patch_redis.get("token:555")
    assert stored is None
    message.answer.assert_awaited_once_with(handlers.INVALID_TOKEN_MESSAGE)


async def test_text_without_token_does_not_call_celery(patch_redis, mocker):
    delay_mock = mocker.patch.object(handlers.llm_request, "delay")
    message = _make_message(tg_user_id=777, text="Привет, как дела?")

    await handlers.handle_text_message(message)

    delay_mock.assert_not_called()
    message.answer.assert_awaited_once_with(handlers.NO_TOKEN_MESSAGE)


async def test_text_with_valid_token_calls_celery(patch_redis, mocker):
    delay_mock = mocker.patch.object(handlers.llm_request, "delay")
    token = _make_token(sub="user-9")
    await patch_redis.set("token:888", token)

    message = _make_message(tg_user_id=888, text="Расскажи анекдот")

    await handlers.handle_text_message(message)

    delay_mock.assert_called_once_with(888, "Расскажи анекдот")
    message.answer.assert_awaited_once()

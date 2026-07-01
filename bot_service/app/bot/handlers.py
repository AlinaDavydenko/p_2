from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()

NO_TOKEN_MESSAGE = (
    "Вы не авторизованы. Отправьте команду /token <jwt>, "
    "предварительно получив токен через Auth Service (POST /auth/register, /auth/login)."
)
INVALID_TOKEN_MESSAGE = (
    "Токен недействителен или истёк. Получите новый токен через Auth Service "
    "и отправьте его командой /token <jwt>."
)


def _token_key(tg_user_id: int) -> str:
    return f"token:{tg_user_id}"


@router.message(Command("token"))
async def handle_token_command(message: Message, command: CommandObject) -> None:
    """Save the user-provided JWT into Redis, keyed by Telegram user_id."""
    token = (command.args or "").strip()

    if not token:
        await message.answer("Использование: /token <jwt>")
        return

    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer(INVALID_TOKEN_MESSAGE)
        return

    redis_client = get_redis()
    await redis_client.set(_token_key(message.from_user.id), token)

    await message.answer("Токен принят и сохранён. Теперь можно отправлять запросы к LLM.")


@router.message()
async def handle_text_message(message: Message) -> None:
    """Validate the stored JWT and, if valid, enqueue an LLM request via Celery."""
    if message.text is None or message.text.startswith("/"):
        return

    redis_client = get_redis()
    token = await redis_client.get(_token_key(message.from_user.id))

    if not token:
        await message.answer(NO_TOKEN_MESSAGE)
        return

    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer(INVALID_TOKEN_MESSAGE)
        return

    llm_request.delay(message.chat.id, message.text)
    await message.answer("Запрос принят, обрабатываю...")

import fakeredis.aioredis
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def fake_redis():
    """An in-memory fake Redis instance, sync-lifecycle-safe for tests."""
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.aclose()


@pytest.fixture
def patch_redis(monkeypatch, fake_redis):
    """Patch get_redis exactly where it is used: app.bot.handlers.get_redis."""
    import app.bot.handlers as handlers_module

    monkeypatch.setattr(handlers_module, "get_redis", lambda: fake_redis)
    return fake_redis

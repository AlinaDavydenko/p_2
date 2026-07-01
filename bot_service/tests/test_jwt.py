import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def _make_token(sub: str = "user-1", role: str = "user") -> str:
    return jwt.encode({"sub": sub, "role": role}, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def test_decode_and_validate_extracts_sub():
    token = _make_token(sub="user-42")
    payload = decode_and_validate(token)

    assert payload["sub"] == "user-42"


def test_decode_and_validate_rejects_garbage_string():
    with pytest.raises(ValueError):
        decode_and_validate("not-a-real-token")

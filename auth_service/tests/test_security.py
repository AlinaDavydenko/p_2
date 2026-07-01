import time

import pytest
from jose import JWTError

from app.core.security import create_access_token, decode_token, hash_password, verify_password


def test_hash_password_is_not_plain_text():
    password = "super-secret-password"
    hashed = hash_password(password)

    assert hashed != password
    assert len(hashed) > 0


def test_verify_password_correct():
    password = "super-secret-password"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    hashed = hash_password("super-secret-password")

    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token():
    token = create_access_token(sub="user-123", role="user")
    payload = decode_token(token)

    assert payload["sub"] == "user-123"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload
    assert payload["exp"] > payload["iat"]


def test_decode_expired_token_raises():
    token = create_access_token(sub="user-123", role="user", expires_minutes=0)
    time.sleep(1)

    with pytest.raises(JWTError):
        decode_token(token)


def test_decode_garbage_token_raises():
    with pytest.raises(JWTError):
        decode_token("this.is.not-a-valid-jwt")

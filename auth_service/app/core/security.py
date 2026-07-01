from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(sub: str, role: str, expires_minutes: int | None = None) -> str:
    """Create a signed JWT access token with sub, role, iat and exp claims."""
    now = datetime.now(timezone.utc)
    expire_minutes = expires_minutes if expires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = now + timedelta(minutes=expire_minutes)

    payload: dict[str, Any] = {
        "sub": sub,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT. Raises JWTError on invalid signature/expired token."""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])


__all__ = ["hash_password", "verify_password", "create_access_token", "decode_token", "JWTError"]

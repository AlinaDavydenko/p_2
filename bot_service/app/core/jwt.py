from typing import Any

from jose import JWTError, jwt

from app.core.config import settings


def decode_and_validate(token: str) -> dict[str, Any]:
    """Validate signature and expiry of a JWT issued by Auth Service.

    Bot Service never creates tokens - it only verifies them.
    Raises ValueError if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError as exc:
        raise ValueError(f"Invalid or expired token: {exc}") from exc

    if "sub" not in payload:
        raise ValueError("Token payload is missing 'sub' claim")

    return payload

from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.models import User
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_users_repo(session: AsyncSession = Depends(get_db)) -> UsersRepository:
    return UsersRepository(session)


def get_auth_uc(users_repo: UsersRepository = Depends(get_users_repo)) -> AuthUseCase:
    return AuthUseCase(users_repo)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = decode_token(token)
    except JWTError as exc:
        message = str(exc).lower()
        if "expired" in message:
            raise TokenExpiredError() from exc
        raise InvalidTokenError() from exc

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError()
    return user_id


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    auth_uc: AuthUseCase = Depends(get_auth_uc),
) -> User:
    return await auth_uc.me(user_id)

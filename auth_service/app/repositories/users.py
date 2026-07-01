from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UsersRepository:
    """Pure data-access layer for users. No business logic, no HTTP exceptions."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, role: str = "user") -> User:
        user = User(email=email, password_hash=password_hash, role=role)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UsersRepository


class AuthUseCase:
    """Business logic for registration, login and profile retrieval."""

    def __init__(self, users_repo: UsersRepository):
        self._users_repo = users_repo

    async def register(self, email: str, password: str) -> User:
        existing = await self._users_repo.get_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsError()

        password_hash = hash_password(password)
        return await self._users_repo.create(email=email, password_hash=password_hash, role="user")

    async def login(self, email: str, password: str) -> str:
        user = await self._users_repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return create_access_token(sub=user.id, role=user.role)

    async def me(self, user_id: str) -> User:
        user = await self._users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return user

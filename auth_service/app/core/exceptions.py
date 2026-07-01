from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Base class for all domain HTTP exceptions in Auth Service."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Bad request"

    def __init__(self, detail: str | None = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class UserAlreadyExistsError(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with this email already exists"


class InvalidCredentialsError(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid email or password"


class InvalidTokenError(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid authentication token"


class TokenExpiredError(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication token has expired"


class UserNotFoundError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class PermissionDeniedError(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"

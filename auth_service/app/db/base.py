from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Single shared declarative base for all ORM models in Auth Service."""
    pass

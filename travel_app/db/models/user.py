from sqlalchemy import String, Boolean, select
from sqlalchemy.orm import Mapped, mapped_column

from travel_app.db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from travel_app.core.security import hash_password, verify_password


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    nick: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    is_fired: Mapped[bool] = mapped_column(Boolean, default=False)

    @classmethod
    async def login(cls, session: AsyncSession, nick: str, password: str) -> "User":
        stmt = select(cls).where(cls.nick == nick)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        if user.is_fired:
            raise PermissionError("User is fired")

        return user

    @classmethod
    async def create_user(cls, session: AsyncSession, nick: str, password: str):
        result = await session.execute(
            select(cls).where(cls.nick == nick)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError(f"User with name '{nick}' already exists")

        password_hash = hash_password(password)

        user = cls(
            nick=nick,
            password_hash=password_hash
        )

        session.add(user)
        await session.flush()
        await session.refresh(user)

        return user

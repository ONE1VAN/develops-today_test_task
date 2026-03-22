from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from travel_app.db.session import get_session
from travel_app.db.models.user import User
from travel_app.core.security import verify_password

security = HTTPBasic()


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:

    stmt = select(User).where(User.nick == credentials.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    if user.is_fired:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is fired"
        )

    return user

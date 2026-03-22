from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from travel_app.db.session import get_session
from travel_app.schemas.auth import LoginRequest, UserCreateModel, UserResponseModel
from travel_app.db.models.user import User
from travel_app.core.logger_config import setup_logger
from travel_app.core.error_handler import handle_error

logger = setup_logger("auth_api", "requests/errors.log")

prefix="/auth"
router = APIRouter(
    prefix=prefix,
    tags=["Auth"]
)


@router.post("/login", response_model=UserResponseModel)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        user = await User.login(session, data.nick, data.password)

        return user

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/login")


@router.post("/register", response_model=UserResponseModel)
async def register_user(
    data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    try:
        user = await User.create_user(
            session=session,
            nick=data.nick,
            password=data.password
        )

        return user

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/register", user_name=data.nick)

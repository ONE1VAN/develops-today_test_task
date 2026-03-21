from fastapi import APIRouter
from travel_app.core.logger_config import setup_logger
from travel_app.core.error_handler import handle_error

logger = setup_logger("projects_api", "requests/errors.log")

prefix = '/projects'
router = APIRouter(
    prefix=prefix,
    tags=['Project endpoints']
)


@router.post("/create")
async def create_project(name: str):
    try:
        if name == "error":
            raise ValueError("Назва проекту не може бути 'error' — це зарезервоване слово!")

        return {"message": f"Project '{name}' created"}

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/create")

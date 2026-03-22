from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from travel_app.core.logger_config import setup_logger
from travel_app.core.error_handler import handle_error
from travel_app.db.session import get_session
from travel_app.schemas.project import ProjectModel, ProjectCreateModel, ProjectUpdateModel
from travel_app.db.models.project import Project
from travel_app.core.dependencies import get_current_user
from travel_app.db.models.user import User

logger = setup_logger("projects_api", "requests/errors.log")

prefix = '/projects'
router = APIRouter(
    prefix=prefix,
    tags=['Project endpoints']
)


@router.post("/create", response_model=ProjectModel)
async def create_project(
        project: ProjectCreateModel,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> Project:
    try:
        return await Project.create(session=session, **project.model_dump())

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/", user.nick)


@router.delete("/delete")
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> dict:
    try:
        success = await Project.delete(session=session, project_id=project_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        return {
            "status": "success",
            "message": "The project and all its unvisited locations were deleted successfully",
            "project_id": project_id
        }

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/{project_id}", user.nick)


@router.patch("/update", response_model=ProjectModel)
async def update_project(
        project_id: int,
        project_data: ProjectUpdateModel,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
):
    try:
        update_data = project_data.model_dump(exclude_unset=True)

        updated_project = await Project.update(
            session=session,
            project_id=project_id,
            **update_data
        )

        if not updated_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        return updated_project

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/{project_id}", user.nick)


@router.get("/get", response_model=list[ProjectModel])
async def get_projects(
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
):
    try:
        projects = await Project.get(session=session)
        return projects

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/", user.nick)


@router.get("/get_by_id", response_model=ProjectModel)
async def get_project_by_id(
        project_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
):
    try:
        project = await Project.get_by_id(session=session, project_id=project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        return project

    except Exception as e:
        raise handle_error(e, logger, f"{prefix}/{project_id}", user.nick)

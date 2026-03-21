from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from travel_app.core.logger_config import setup_logger
from travel_app.core.error_handler import handle_error
from travel_app.db.session import get_session
from travel_app.schemas.places import ProjectPlaceCreateModel, PlaceModel, PlaceAddModel, PlaceUpdateModel
from travel_app.db.models.place import Place
from travel_app.db.models.project import Project

logger = setup_logger("projects_api", "requests/errors.log")

prefix = '/places'
router = APIRouter(
    prefix=prefix,
    tags=['Places endpoints']
)


@router.post("/create_with_project", response_model=list[PlaceModel])
async def create_project_with_places(
    data: ProjectPlaceCreateModel,
    session: AsyncSession = Depends(get_session)
):
    try:
        project = await Place.create_with_project(
            session=session,
            data=data
        )
        return project

    except Exception as e:
        raise handle_error(e, logger, f"/{prefix}/create_with_places")


@router.post("/add", response_model=PlaceModel)
async def add_place_to_project(
    place_data: PlaceAddModel,
    session: AsyncSession = Depends(get_session)
):
    try:
        project = await Project.get_by_id(session, place_data.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {place_data.project_id} not found"
            )

        return await Place.add(
            session=session,
            project_id=place_data.project_id,
            external_id=place_data.external_id,
            notes=place_data.notes,
            visited=place_data.visited
        )

    except Exception as e:
        raise handle_error(e, logger, f"/{prefix}/add")


@router.patch("/update", response_model=PlaceModel)
async def update_place(
    place_id: int,
    place_data: PlaceUpdateModel,
    session: AsyncSession = Depends(get_session)
):
    try:
        update_fields = place_data.model_dump(exclude_unset=True)
        updated_place = await Place.update_place(session, place_id, **update_fields)

        if not updated_place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Place {place_id} not found"
            )

        return updated_place

    except Exception as e:
        raise handle_error(e, logger, f"/{prefix}/{place_id}/update")


@router.get("/get_project_places", response_model=list[PlaceModel])
async def list_places_for_project(
    project_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        places = await Place.get_by_project_id(session, project_id)
        if not places:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No places found for project {project_id}"
            )
        return places

    except Exception as e:
        raise handle_error(e, logger, f"/{prefix}/project/{project_id}")


@router.get("/get_by_id", response_model=PlaceModel)
async def get_place_by_id(place_id: int, session: AsyncSession = Depends(get_session)):
    try:
        place = await Place.get_by_id(session, place_id)
        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Place {place_id} not found"
            )
        return place

    except Exception as e:
        raise handle_error(e, logger, f"/{prefix}/{place_id}")

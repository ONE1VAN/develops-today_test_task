from pydantic import BaseModel

from .project import ProjectBaseModel


class PlaceBaseModel(BaseModel):
    external_id: int
    notes: str | None = None
    visited: bool = False


class PlaceCreateModel(PlaceBaseModel):
    pass


class ProjectPlaceCreateModel(ProjectBaseModel):
    places: list[PlaceCreateModel] = []


class PlaceAddModel(BaseModel):
    project_id: int
    external_id: int
    notes: str | None = None
    visited: bool = False


class PlaceUpdateModel(BaseModel):
    notes: str | None = None
    visited: bool | None = None


class PlaceModel(PlaceBaseModel):
    id: int
    project_id: int

    model_config = {"from_attributes": True}

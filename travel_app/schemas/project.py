from datetime import date

from pydantic import BaseModel


class ProjectBaseModel(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None


class ProjectCreateModel(ProjectBaseModel):
    pass


class ProjectUpdateModel(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None


class ProjectModel(ProjectBaseModel):
    id: int
    is_completed: bool = False

    class Config:
        from_attributes = True

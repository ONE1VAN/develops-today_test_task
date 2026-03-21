from pydantic import BaseModel


class ArtPlaceModel(BaseModel):
    id: int
    title: str | None = None


class ArtAPIResponseModel(BaseModel):
    data: ArtPlaceModel

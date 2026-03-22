import httpx
from pydantic import ValidationError
from async_lru import alru_cache

from travel_app.schemas.art_api import ArtAPIResponseModel, ArtPlaceModel


class ArtAPIService:
    BASE_URL = "https://api.artic.edu/api/v1/artworks"

    @alru_cache(maxsize=128)
    async def get_place(self, external_id: int) -> ArtPlaceModel:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{external_id}")

        if response.status_code != 200:
            raise ValueError(f"Place with id={external_id} not found in the API.")

        try:
            validated = ArtAPIResponseModel.model_validate(response.json())
        except ValidationError as e:
            raise ValueError(f"Invalid API response structure: {e}")

        if not validated.data.title:
            raise ValueError(f"Missing title for id={external_id}")

        return validated.data

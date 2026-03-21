import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from travel_app.db.session import engine
from travel_app.db.base import Base
from travel_app.core.config import HOST, PORT, RELOAD
from travel_app.api.endpoints.projects import router as projects_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(projects_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD
    )

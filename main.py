import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.core.config import HOST, PORT, RELOAD

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD
    )

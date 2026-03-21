from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from travel_app.db.base import Base
from travel_app.db.models import Project
from travel_app.schemas.places import ProjectPlaceCreateModel
from travel_app.services.art_api import ArtAPIService


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    external_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)

    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    visited: Mapped[bool] = mapped_column(Boolean, default=False)

    project = relationship("Project", back_populates="places")

    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
    )

    @classmethod
    async def create_with_project(cls, session: AsyncSession, data: ProjectPlaceCreateModel):
        api_service = ArtAPIService()

        if not (1 <= len(data.places) <= 10):
            raise ValueError("Places must be between 1 and 10")

        external_ids = [p.external_id for p in data.places]
        if len(external_ids) != len(set(external_ids)):
            raise ValueError("Duplicate external_id in request")

        project = Project(
            name=data.name,
            description=data.description,
            start_date=data.start_date
        )
        session.add(project)
        await session.flush()

        created_places = []

        for place in data.places:
            api_place = await api_service.get_place(place.external_id)
            new_place = cls(
                project_id=project.id,
                external_id=api_place.id,
                title=api_place.title,
                notes=place.notes,
                visited=place.visited
            )
            session.add(new_place)
            created_places.append(new_place)

        await session.flush()
        return created_places

    @classmethod
    async def add(cls, session: AsyncSession, project_id: int, external_id: int, notes=None, visited=False):
        api_service = ArtAPIService()
        api_place = await api_service.get_place(external_id)
        existing = await session.execute(
            select(cls).where(cls.project_id == project_id, cls.external_id == api_place.id)
        )
        if existing.scalar_one_or_none():
            raise ValueError(f"Place with external_id={api_place.id} already exists in project {project_id}")

        new_place = cls(
            project_id=project_id,
            external_id=api_place.id,
            title=api_place.title,
            notes=notes,
            visited=visited
        )
        session.add(new_place)
        await session.flush()
        await session.refresh(new_place)

        return new_place

    @classmethod
    async def update_place(cls, session: AsyncSession, place_id: int, **kwargs):
        result = await session.execute(select(cls).where(cls.id == place_id))
        place = result.scalar_one_or_none()

        if not place:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(place, key):
                setattr(place, key, value)

        await session.flush()
        await session.refresh(place)
        return place

    @classmethod
    async def get_by_project_id(cls, session: AsyncSession, project_id: int):
        result = await session.execute(
            select(cls).where(cls.project_id == project_id)
        )
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, place_id: int):
        result = await session.execute(
            select(cls).where(cls.id == place_id)
        )
        return result.scalar_one_or_none()

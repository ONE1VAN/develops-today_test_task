from datetime import datetime

from sqlalchemy import String, Boolean, Date, DateTime, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from travel_app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )

    places = relationship(
        "Place",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> "Project":
        new_project = cls(**kwargs)
        session.add(new_project)
        await session.refresh(new_project)
        return new_project

    @classmethod
    async def get_by_id(cls, session: AsyncSession, project_id: int):
        result = await session.execute(select(cls).where(cls.id == project_id))
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession, project_id: int) -> bool:
        result = await session.execute(
            select(cls)
            .options(selectinload(cls.places))
            .where(cls.id == project_id)
        )
        project = result.scalar_one_or_none()

        if not project:
            return False
        if any(place.visited for place in project.places):
            raise ValueError("Unable to delete project: some locations have already been visited")

        await session.delete(project)
        return True

    @classmethod
    async def update(cls, session: AsyncSession, project_id: int, **kwargs) -> "Project":
        project = await cls.get_by_id(session, project_id)

        if project:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(project, key, value)

            await session.flush()
        return project

    @classmethod
    async def get(cls, session: AsyncSession):
        stmt = select(cls)
        result = await session.execute(stmt)
        return result.scalars().all()

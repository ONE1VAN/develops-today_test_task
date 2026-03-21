from datetime import datetime

from sqlalchemy import String, Boolean, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

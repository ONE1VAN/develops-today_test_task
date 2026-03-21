from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from travel_app.db.base import Base


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

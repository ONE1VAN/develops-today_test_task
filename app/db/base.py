from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.db.models.project import Project
from app.db.models.place import Place

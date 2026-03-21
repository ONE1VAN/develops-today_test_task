from sqlalchemy.orm import declarative_base

Base = declarative_base()

from travel_app.db.models.project import Project
from travel_app.db.models.place import Place

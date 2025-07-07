from sqlmodel import SQLModel, create_engine, Session
from app.core.config_loader import settings

from app.models.state import State
from app.models.gender import Gender
from app.models.marital_status import MaritalStatus

DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
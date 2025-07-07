from sqlmodel import SQLModel, Field, Relationship
from app.models.base import Base
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.gender import Gender

class State(Base, table=True):
    pass
    
    # genders: List["Gender"] = Relationship(back_populates="state")
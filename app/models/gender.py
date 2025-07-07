from sqlmodel import SQLModel, Field, Relationship
from app.models.base import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.state import State

class Gender(Base, table=True):
    pass
    # state_id: Optional[int] = Field(default=None, foreign_key="state.id")
    
    # state: Optional["State"] = Relationship(back_populates="genders")
    
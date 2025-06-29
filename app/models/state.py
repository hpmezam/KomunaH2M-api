from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING

# if TYPE_CHECKING:
#     pass

class State(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(max_length=30, unique=True, index=True)
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
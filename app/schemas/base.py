from sqlmodel import SQLModel, Field
from typing import Optional

class BaseCreate(SQLModel):
    name: str
    
class BaseRead(SQLModel):
    id: int
    name: str
    is_active: bool
    
class BaseUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=50)
    is_active: Optional[bool] = None
    
class BaseStatusUpdate(SQLModel):
    is_active: bool = Field(..., description="New status")
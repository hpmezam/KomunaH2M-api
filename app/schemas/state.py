from sqlmodel import SQLModel, Field
from typing import Optional

class StateCreate(SQLModel):
    name: str
    description: str
    is_active: bool
    
class StateRead(SQLModel):
    id: int
    name: str
    description: str
    is_active: bool
    
class StateUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = None
    
class StateStatusUpdate(SQLModel):
    is_active: bool = Field(..., description="New status for the state")
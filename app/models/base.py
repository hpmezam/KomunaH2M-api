from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Base(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, description="Name")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.state import State

class Gender(Base, table=True):
    pass
    
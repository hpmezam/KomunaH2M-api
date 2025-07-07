from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gender import Gender

class State(Base, table=True):
    pass
    
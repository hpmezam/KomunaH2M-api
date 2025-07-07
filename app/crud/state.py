from app.models.state import State
from app.schemas.state import StateCreate, StateUpdate
from app.crud.crud_base import CrudBase

crud_state = CrudBase[State, StateCreate, StateUpdate](State)
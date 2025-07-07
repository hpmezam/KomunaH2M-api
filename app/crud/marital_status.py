from app.models.marital_status import MaritalStatus
from app.schemas.marital_status import MaritalCreate, MaritalUpdate
from app.crud.crud_base import CrudBase

crud_state = CrudBase[MaritalStatus, MaritalCreate, MaritalUpdate](MaritalStatus)
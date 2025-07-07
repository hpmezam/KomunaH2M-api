from app.models.gender import Gender
from app.schemas.gender import GenderCreate, GenderUpdate
from app.crud.crud_base import CrudBase

crud_state = CrudBase[Gender, GenderCreate, GenderUpdate](Gender)
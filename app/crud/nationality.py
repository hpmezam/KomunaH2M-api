from app.models.nationality import Nationality
from app.schemas.nationality import NationalityCreate, NationalityUpdate
from app.crud.crud_base import CrudBase

crud_state = CrudBase[Nationality, NationalityCreate, NationalityUpdate](Nationality)
from app.models.education_level import EducationLevel
from app.schemas.education_level import EducationCreate, EducationUpdate
from app.crud.crud_base import CrudBase

crud_state = CrudBase[EducationLevel, EducationCreate, EducationUpdate](EducationLevel)
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.schemas.education_level import EducationCreate, EducationRead, EducationUpdate, EducationStatusUpdate
from app.db.database import get_db

from app.crud.education_level import crud_state

education_router = APIRouter(prefix="/education", tags=["Education Level"])

@education_router.post("/", response_model=EducationRead)
def create_education(state: EducationCreate, db: Session = Depends(get_db)):
    return crud_state.create(db, state)

@education_router.get("/", response_model=list[EducationRead], summary="Get List Education Level")
def list_education(db: Session = Depends(get_db)):
    return crud_state.get_all(db)

@education_router.get("/status", response_model=list[EducationRead], summary="Get List Of Education Level By State")
def list_education_by_status(
    is_active: bool = Query(True, description="Filter by active or inactive statuses"),
    db: Session = Depends(get_db)
):
    return crud_state.get_all_by_status(db, is_active)

@education_router.get("/{state_id}", response_model=EducationRead)
def get_education_by_id(state_id: int, db: Session = Depends(get_db)):
    return crud_state.get_by_id(db, state_id)

@education_router.patch("/change-status/{state_id}", response_model=EducationRead, summary="Change activation status", description="Changes only the 'is_active' field of the indicated state.")
def change_status(state_id: int, status: EducationStatusUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, status)

@education_router.put("/{state_id}", response_model=EducationRead, summary="Update Education Level")
def update_education(state_id: int, state: EducationUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, state)

@education_router.delete("/{state_id}")
def delete_education(state_id: int, db: Session = Depends(get_db)):
    return crud_state.delete(db, state_id)

@education_router.patch("/soft-delete/{state_id}")
def soft_delete_education(state_id: int, db: Session = Depends(get_db)):
    return crud_state.soft_delete(db, state_id)


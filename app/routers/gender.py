from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.schemas.gender import GenderCreate, GenderRead, GenderUpdate, GenderStatusUpdate
from app.db.database import get_db

from app.crud.gender import crud_state

gender_router = APIRouter(prefix="/gender", tags=["Gender"])

@gender_router.post("/", response_model=GenderRead)
def create_gender(state: GenderCreate, db: Session = Depends(get_db)):
    return crud_state.create(db, state)

@gender_router.get("/", response_model=list[GenderRead], summary="Get List Gender")
def list_genders(db: Session = Depends(get_db)):
    return crud_state.get_all(db)

@gender_router.get("/status", response_model=list[GenderRead], summary="Get List Of Gender By State")
def list_gender_by_status(
    is_active: bool = Query(True, description="Filter by active or inactive statuses"),
    db: Session = Depends(get_db)
):
    return crud_state.get_all_by_status(db, is_active)

@gender_router.get("/{state_id}", response_model=GenderRead)
def get_gender_by_id(state_id: int, db: Session = Depends(get_db)):
    return crud_state.get_by_id(db, state_id)

@gender_router.patch("/change-status/{state_id}", response_model=GenderRead, summary="Change activation status", description="Changes only the 'is_active' field of the indicated state.")
def change_status(state_id: int, status: GenderStatusUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, status)

@gender_router.put("/{state_id}", response_model=GenderRead, summary="Update Gender")
def update_gender(state_id: int, state: GenderUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, state)

@gender_router.delete("/{state_id}")
def delete_gender(state_id: int, db: Session = Depends(get_db)):
    return crud_state.delete(db, state_id)

@gender_router.patch("/soft-delete/{state_id}")
def soft_delete_gender(state_id: int, db: Session = Depends(get_db)):
    return crud_state.soft_delete(db, state_id)


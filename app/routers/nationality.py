from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.schemas.nationality import NationalityCreate, NationalityRead, NationalityUpdate, NationalityStatusUpdate
from app.db.database import get_db

from app.crud.nationality import crud_state

nationality_router = APIRouter(prefix="/nationality", tags=["Nationality"])

@nationality_router.post("/", response_model=NationalityRead)
def create_nationality(state: NationalityCreate, db: Session = Depends(get_db)):
    return crud_state.create(db, state)

@nationality_router.get("/", response_model=list[NationalityRead], summary="Get List Nationality")
def list_nationality(db: Session = Depends(get_db)):
    return crud_state.get_all(db)

@nationality_router.get("/status", response_model=list[NationalityRead], summary="Get List Of Nationality By State")
def list_nationality_by_status(
    is_active: bool = Query(True, description="Filter by active or inactive statuses"),
    db: Session = Depends(get_db)
):
    return crud_state.get_all_by_status(db, is_active)

@nationality_router.get("/{state_id}", response_model=NationalityRead)
def get_nationality_by_id(state_id: int, db: Session = Depends(get_db)):
    return crud_state.get_by_id(db, state_id)

@nationality_router.patch("/change-status/{state_id}", response_model=NationalityRead, summary="Change activation status", description="Changes only the 'is_active' field of the indicated state.")
def change_status(state_id: int, status: NationalityStatusUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, status)

@nationality_router.put("/{state_id}", response_model=NationalityRead, summary="Update Nationality")
def update_nationality(state_id: int, state: NationalityUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, state)

@nationality_router.delete("/{state_id}")
def delete_nationality(state_id: int, db: Session = Depends(get_db)):
    return crud_state.delete(db, state_id)

@nationality_router.patch("/soft-delete/{state_id}")
def soft_delete_nationality(state_id: int, db: Session = Depends(get_db)):
    return crud_state.soft_delete(db, state_id)


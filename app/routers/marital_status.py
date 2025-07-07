from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.schemas.marital_status import MaritalCreate, MaritalRead, MaritalUpdate, MaritalStatusUpdate
from app.db.database import get_db

from app.crud.marital_status import crud_state

marital_router = APIRouter(prefix="/marital-status", tags=["Marital Status"])

@marital_router.post("/", response_model=MaritalRead)
def create_marital_status(state: MaritalCreate, db: Session = Depends(get_db)):
    return crud_state.create(db, state)

@marital_router.get("/", response_model=list[MaritalRead], summary="Get List Marital Status")
def list_marital_status(db: Session = Depends(get_db)):
    return crud_state.get_all(db)

@marital_router.get("/status", response_model=list[MaritalRead], summary="Get List Of Marital Status By State")
def list_marital_status_by_status(
    is_active: bool = Query(True, description="Filter by active or inactive statuses"),
    db: Session = Depends(get_db)
):
    return crud_state.get_all_by_status(db, is_active)

@marital_router.get("/{state_id}", response_model=MaritalRead)
def get_marital_status_by_id(state_id: int, db: Session = Depends(get_db)):
    return crud_state.get_by_id(db, state_id)

@marital_router.patch("/change-status/{state_id}", response_model=MaritalRead, summary="Change activation status", description="Changes only the 'is_active' field of the indicated state.")
def change_marital_status(state_id: int, status: MaritalStatusUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, status)

@marital_router.put("/{state_id}", response_model=MaritalRead, summary="Update Marital Status")
def update_marital_status(state_id: int, state: MaritalStatusUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, state)

@marital_router.delete("/{state_id}")
def delete_marital_status(state_id: int, db: Session = Depends(get_db)):
    return crud_state.delete(db, state_id)

@marital_router.patch("/soft-delete/{state_id}")
def soft_delete_marital_status(state_id: int, db: Session = Depends(get_db)):
    return crud_state.soft_delete(db, state_id)


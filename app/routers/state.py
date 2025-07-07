from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.schemas.state import StateCreate, StateRead, StateUpdate, StateStatusUpdate
from app.db.database import get_db

from app.crud.state import crud_state

state_router = APIRouter(prefix="/state", tags=["States"])

@state_router.post("/", response_model=StateRead)
def create_state(state: StateCreate, db: Session = Depends(get_db)):
    return crud_state.create(db, state)

@state_router.get("/", response_model=list[StateRead], summary="Get List State")
def list_states(db: Session = Depends(get_db)):
    return crud_state.get_all(db)

@state_router.get("/status", response_model=list[StateRead], summary="Get List Of States By State")
def list_states_by_status(
    is_active: bool = Query(True, description="Filter by active or inactive statuses"),
    db: Session = Depends(get_db)
):
    return crud_state.get_all_by_status(db, is_active)

@state_router.get("/{state_id}", response_model=StateRead)
def get_state_by_id(state_id: int, db: Session = Depends(get_db)):
    return crud_state.get_by_id(db, state_id)

@state_router.patch("/change-status/{state_id}", response_model=StateRead, summary="Change activation status", description="Changes only the 'is_active' field of the indicated state.")
def change_status(state_id: int, status: StateStatusUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, status)

@state_router.put("/{state_id}", response_model=StateRead, summary="Update State")
def update_state(state_id: int, state: StateUpdate, db: Session = Depends(get_db)):
    return crud_state.update(db, state_id, state)

@state_router.delete("/{state_id}")
def delete_state(state_id: int, db: Session = Depends(get_db)):
    return crud_state.delete(db, state_id)

@state_router.patch("/soft-delete/{state_id}")
def soft_delete_state(state_id: int, db: Session = Depends(get_db)):
    return crud_state.soft_delete(db, state_id)


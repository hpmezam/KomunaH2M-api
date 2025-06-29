from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.models.state import State
from app.schemas.state import StateCreate, StateRead, StateUpdate, StateStatusUpdate
from app.db.database import get_db
from app.crud.state import (create_state, 
                            get_list_states, 
                            update_state, 
                            delete_state, 
                            get_state_by_id, 
                            get_list_states_by_status,
                            update_state_status
                            )

state_router = APIRouter(prefix="/state", tags=["States"])

@state_router.post("/", response_model=StateRead)
def create_state_endpoint(state: StateCreate, db: Session = Depends(get_db)):
    return create_state(db, state)

@state_router.get("/", response_model=list[StateRead], summary="Get List State")
def get_list_state_endpoint(db: Session = Depends(get_db)):
    return get_list_states(db)


@state_router.get("/status", response_model=list[StateRead], summary="Get List Of States By State")
def get_list_states_by_status_endpoint(
    is_active: bool = Query(True, description="Filtra por estados activos o inactivos"),
    db: Session = Depends(get_db)
):
    return get_list_states_by_status(db, is_active)

@state_router.get("/{state_id}", response_model=StateRead, summary="Get State By Id")
def get_state_by_id_endpoint(state_id: int, db: Session = Depends(get_db)):
    return get_state_by_id(db, state_id)

@state_router.patch("/change-status/{state_id}", response_model=StateRead, summary="Cambiar estado de activación", description="Cambia solo el campo 'is_active' del estado indicado.")
def change_state_status_endpoint(state_id: int, status_data: StateStatusUpdate, db: Session = Depends(get_db)):
    return update_state_status(db, state_id, status_data)

@state_router.put("/{state_id}", response_model=StateRead, summary="Update State")
def update_state_endpoint(state_id: int, state: StateUpdate, db: Session = Depends(get_db)):
    return update_state(db, state_id, state)

@state_router.delete("/{state_id}", summary="Delete State")
def delete_state_endpoint(state_id: int, db: Session = Depends(get_db)):
    return delete_state(db, state_id)
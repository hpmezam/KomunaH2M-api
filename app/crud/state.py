from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.state import State
from app.schemas.state import StateCreate, StateRead, StateUpdate, StateStatusUpdate

def create_state(db: Session, state: StateCreate) -> State:
    # Check if a state with the same name already exists
    exist = db.exec(select(State).where(State.name == state.name)).first()
    if exist:
        raise HTTPException(
            status_code=400, 
            detail=f"A state with the name '{state.name}' already exists"
        )
    new_state = State(**state.model_dump())
    db.add(new_state)
    db.commit()
    db.refresh(new_state)
    return new_state

def get_list_states(db: Session) -> list[StateRead]:
    states =db.exec(select(State)).all()
    if not states:
        raise HTTPException(
            status_code=404,
            detail="There are no states in the database"
        )
    return states

def get_state_by_id(db: Session, state_id: int) -> StateRead:
    state = db.get(State, state_id)
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"The state with id {state_id} does not exist"
        )
    return state

def get_list_states_by_status(db: Session, is_active: bool) -> list[StateRead]:
    return db.exec(select(State).where(State.is_active == is_active)).all()

def update_state(db: Session, state_id: int, state: StateUpdate) -> StateRead:
    # Find the status to update
    existing_state = db.get(State, state_id)
    if not existing_state:
        raise HTTPException(
            status_code=404,
            detail=f"The state with id {state_id} does not exist"
        )
        
    # Validate if the name is already held by another state (other than the current one)
    if state.name:
        duplicate = db.exec(
            select(State).
            where(State.name == state.name).
            where(State.id != state_id)
        ).first()
        
        if duplicate:
            raise HTTPException(
                status_code=400,
                detail=f"Another state with the name'{state.name}' already exists"
            ) 
    
    # Extraxt only the fields that the user wants to modify
    update_data = state.model_dump(exclude_unset=True)
    
    # Check if the values are exactly the same
    no_changes = all(
        getattr(existing_state, field) == value for field, value in update_data.items()
    )
    if no_changes:
        raise HTTPException(
            status_code=400,
            detail="No changes were made: the submitted values are the same as the current ones"
        )
    
    # Apply updates  
    for key, value in update_data.items():
        setattr(existing_state, key, value)
                 
    db.commit()
    db.refresh(existing_state)
    return existing_state

def update_state_status(db: Session, state_id: int, status_data: StateStatusUpdate) -> State:
    state = db.get(State, state_id)
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"The state with id {state_id} does not exist"
        )
    
    if state.is_active == status_data.is_active:
        raise HTTPException(
            status_code=400,
            detail=f"The state '{state.name}' is already {'active' if state.is_active else 'inactive'}"
        )
    
    state.is_active = status_data.is_active
    db.commit()
    db.refresh(state)
    return state

def delete_state(db: Session, state_id: int) -> dict:
    state = db.get(State, state_id)
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"The state with id {state_id} does not exist"
        )
        
    name = state.name
    db.delete(state)
    db.commit()
    return {"message": f"The state '{name}' has been deleted successfully"}


    
from typing import TypeVar, Generic
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, select
from datetime import datetime, timezone

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model
        
    def get_by_id(self, db: Session, id: int) -> ModelType:
        instance = db.get(self.model, id)
        if not instance:
            raise HTTPException(status_code=404, detail=f"The {self.model.__name__} with id {id} not found")
        return instance
    
    def get_all_by_status(self, db: Session, is_active: bool) -> list[ModelType]:
        return db.exec(select(self.model).where(self.model.is_active == is_active)).all()
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        exist = db.exec(select(self.model).where(self.model.name == obj_in.name)).first()
        if exist:
            raise HTTPException(status_code=400, detail=f"A {self.model.__name__} with name '{obj_in.name}' already exists")
        obj = self.model(**obj_in.model_dump(), is_active=False)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def get_all(self, db: Session) -> list[ModelType]:
        result = db.exec(select(self.model)).all()
        if not result:
            raise HTTPException(status_code=404, detail=f"There are no {self.model.__name__}s in the database")
        return result
    
    def update(self, db: Session, id: int, obj_in: UpdateSchemaType) -> ModelType:
        # 1. Get existing object
        db_obj = db.get(self.model, id)
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with id {id} does not exist"
            )

        # 2. Validate if another one with the same name already exists (except the current one)
        if getattr(obj_in, "name", None):
            duplicate = db.exec(
                select(self.model)
                .where(self.model.name == obj_in.name)
                .where(self.model.id != id)
            ).first()

            if duplicate:
                raise HTTPException(
                    status_code=400,
                    detail=f"Another {self.model.__name__} with name '{obj_in.name}' already exists"
                )

        # 3. Get the data to update (only the data that was sent)
        update_data = obj_in.model_dump(exclude_unset=True)

        # 4. Validate if there were really changes
        no_changes = all(
            getattr(db_obj, field) == value
            for field, value in update_data.items()
        )
        if no_changes:
            raise HTTPException(
                status_code=400,
                detail="No changes were made: submitted values match current data"
            )

        # 5. Apply changes
        for key, value in update_data.items():
            setattr(db_obj, key, value)
          
        # 6. Update the timestamp  
        if hasattr(db_obj, "updated_at"):
            db_obj.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(self, db: Session, id: int, is_active: bool) -> ModelType:
        db_obj = db.get(self.model, id)
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with id {id} does not exist"
            )

        if db_obj.is_active == is_active:
            raise HTTPException(
                status_code=400,
                detail=f"{self.model.__name__} '{db_obj.name}' is already {'active' if is_active else 'inactive'}"
            )

        db_obj.is_active = is_active
        if hasattr(db_obj, "updated_at"):
            db_obj.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> dict:
        db_obj = db.get(self.model, id)
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with id {id} does not exist"
            )
        name = getattr(db_obj, "name", "object")
        db.delete(db_obj)
        db.commit()
        return {"message": f"{self.model.__name__} '{name}' has been deleted successfully"}

    def soft_delete(self, db: Session, id: int) -> ModelType:
        db_obj = db.get(self.model, id)
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with id {id} does not exist"
            )

        if not db_obj.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"{self.model.__name__} '{db_obj.name}' is already inactive"
            )

        db_obj.is_active = False
        if hasattr(db_obj, "updated_at"):
            db_obj.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_obj)
        return db_obj
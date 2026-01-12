import logging
from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def create(self, instance: ModelType, commit: bool = True) -> ModelType:
        try:
            self.db.add(instance)
            if commit:
                self.db.commit()
                self.db.refresh(instance)
            else:
                self.db.flush()
                self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Database error in create: {e}")
            if commit:
                self.db.rollback()
            raise

    def get_by_id(self, instance_id: int) -> Optional[ModelType]:
        try:
            return (
                self.db.query(self.model)
                .filter(self.model.id == instance_id)  # type: ignore[attr-defined]
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_id: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all: {e}")
            raise

    def update(self, instance: ModelType) -> ModelType:
        try:
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Database error in update: {e}")
            self.db.rollback()
            raise

    def delete(self, instance: ModelType) -> None:
        try:
            self.db.delete(instance)
            self.db.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error in delete: {e}")
            self.db.rollback()
            raise

"""
Base repository with common CRUD operations.
"""

import logging
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

logger = logging.getLogger(__name__)

# ModelType must have an 'id' attribute
ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, db: Session, model: Type[ModelType]):
        """
        Initialize repository.

        Args:
            db: Database session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    def create(self, instance: ModelType) -> ModelType:
        """
        Create a new instance.

        Args:
            instance: Model instance to create

        Returns:
            Created instance

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Database error in create: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, instance_id: int) -> Optional[ModelType]:
        """
        Get instance by ID.

        Args:
            instance_id: ID of the instance

        Returns:
            Instance if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # Type checker doesn't know that ModelType has 'id' attribute
            # but all our models inherit from Base which has id
            return (
                self.db.query(self.model)
                .filter(
                    self.model.id == instance_id  # type: ignore[attr-defined]
                )
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_id: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all instances with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of instances

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all: {e}")
            raise

    def update(self, instance: ModelType) -> ModelType:
        """
        Update an existing instance.

        Args:
            instance: Model instance to update

        Returns:
            Updated instance

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Database error in update: {e}")
            self.db.rollback()
            raise

    def delete(self, instance: ModelType) -> None:
        """
        Delete an instance.

        Args:
            instance: Model instance to delete

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            self.db.delete(instance)
            self.db.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error in delete: {e}")
            self.db.rollback()
            raise

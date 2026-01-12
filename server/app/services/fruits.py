"""
Fruit service layer with business logic.
"""
import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import Fruit
from ..repositories.fruits import FruitRepository
from ..schemas.fruits import FruitCreate, FruitUpdate
from ..core.exceptions import raise_not_found, raise_service_unavailable

logger = logging.getLogger(__name__)


class FruitService:
    """
    Service layer for Fruit operations.
    Handles business logic and error handling.
    """

    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: Database session
        """
        self.repository = FruitRepository(db)

    def create_fruit(self, fruit_data: FruitCreate) -> Fruit:
        """
        Create a new fruit.
        
        Args:
            fruit_data: Fruit creation data
            
        Returns:
            Created fruit instance
            
        Raises:
            HTTPException: If database operation fails
        """
        try:
            fruit = Fruit(name=fruit_data.name)
            return self.repository.create(fruit)
        except SQLAlchemyError as e:
            logger.error(f"Database error in create_fruit: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def get_fruit_by_id(self, fruit_id: int) -> Fruit:
        """
        Get fruit by ID.
        
        Args:
            fruit_id: Fruit ID
            
        Returns:
            Fruit instance
            
        Raises:
            HTTPException: If fruit not found or database error
        """
        try:
            fruit = self.repository.get_by_id(fruit_id)
            if not fruit:
                raise raise_not_found("Fruit", fruit_id)
            return fruit
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_fruit_by_id: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def get_all_fruits(self, skip: int = 0, limit: int = 100) -> List[Fruit]:
        """
        Get all fruits with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of fruit instances
            
        Raises:
            HTTPException: If database operation fails
        """
        try:
            return self.repository.get_all(skip=skip, limit=limit)
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all_fruits: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def update_fruit(self, fruit_id: int, fruit_data: FruitUpdate) -> Fruit:
        """
        Update an existing fruit.
        
        Args:
            fruit_id: Fruit ID
            fruit_data: Fruit update data
            
        Returns:
            Updated fruit instance
            
        Raises:
            HTTPException: If fruit not found or database error
        """
        try:
            fruit = self.repository.get_by_id(fruit_id)
            if not fruit:
                raise raise_not_found("Fruit", fruit_id)
            fruit.name = fruit_data.name
            return self.repository.update(fruit)
        except SQLAlchemyError as e:
            logger.error(f"Database error in update_fruit: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def delete_fruit(self, fruit_id: int) -> None:
        """
        Delete a fruit.
        
        Args:
            fruit_id: Fruit ID
            
        Raises:
            HTTPException: If fruit not found or database error
        """
        try:
            fruit = self.repository.get_by_id(fruit_id)
            if not fruit:
                raise raise_not_found("Fruit", fruit_id)
            self.repository.delete(fruit)
        except SQLAlchemyError as e:
            logger.error(f"Database error in delete_fruit: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

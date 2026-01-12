import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import Fruit
from ..repositories.fruits import FruitRepository
from ..schemas.fruits import FruitCreate, FruitUpdate
from ..core.exceptions import raise_not_found, raise_service_unavailable
from ..core.transaction import transaction

logger = logging.getLogger(__name__)


class FruitService:
    def __init__(self, db: Session):
        self.repository = FruitRepository(db)

    def create_fruit(self, fruit_data: FruitCreate) -> Fruit:
        try:
            fruit = Fruit(name=fruit_data.name)
            return self.repository.create(fruit)
        except SQLAlchemyError as e:
            logger.error(f"Database error in create_fruit: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def get_fruit_by_id(self, fruit_id: int) -> Fruit:
        try:
            fruit = self.repository.get_by_id(fruit_id)
            if not fruit:
                raise raise_not_found("Fruit", fruit_id)
            return fruit
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_fruit_by_id: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def get_all_fruits(self, skip: int = 0, limit: int = 100) -> List[Fruit]:
        try:
            return self.repository.get_all(skip=skip, limit=limit)
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all_fruits: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def update_fruit(self, fruit_id: int, fruit_data: FruitUpdate) -> Fruit:
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
        try:
            fruit = self.repository.get_by_id(fruit_id)
            if not fruit:
                raise raise_not_found("Fruit", fruit_id)
            self.repository.delete(fruit)
        except SQLAlchemyError as e:
            logger.error(f"Database error in delete_fruit: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def create_multiple_fruits(self, fruits_data: List[FruitCreate]) -> List[Fruit]:
        try:
            with transaction(self.repository.db) as session:
                created_fruits = []
                for fruit_data in fruits_data:
                    fruit = Fruit(name=fruit_data.name)
                    session.add(fruit)
                    created_fruits.append(fruit)
                session.flush()
                for fruit in created_fruits:
                    session.refresh(fruit)
                return created_fruits
        except SQLAlchemyError as e:
            logger.error(f"Database error in create_multiple_fruits: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

    def bulk_update_fruits(self, updates: List[tuple[int, FruitUpdate]]) -> List[Fruit]:
        try:
            with transaction(self.repository.db) as session:
                updated_fruits = []
                for fruit_id, fruit_data in updates:
                    fruit = self.repository.get_by_id(fruit_id)
                    if not fruit:
                        raise raise_not_found("Fruit", fruit_id)
                    fruit.name = fruit_data.name
                    updated_fruits.append(fruit)
                return updated_fruits
        except SQLAlchemyError as e:
            logger.error(f"Database error in bulk_update_fruits: {e}")
            raise raise_service_unavailable("Database service is currently unavailable")

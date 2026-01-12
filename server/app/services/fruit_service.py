from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..core.transaction import transaction
from ..models import Fruit
from ..repositories.fruit_repository import FruitRepository
from ..schemas.fruit_schema import FruitCreate, FruitUpdate


class FruitService:
    def __init__(self, db: Session):
        self.repository = FruitRepository(db)

    def create_fruit(self, fruit_data: FruitCreate) -> Fruit:
        fruit = Fruit(name=fruit_data.name)
        return self.repository.create(fruit)

    def get_fruit_by_id(self, fruit_id: UUID) -> Fruit:
        fruit = self.repository.get_by_id(fruit_id)
        if not fruit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fruit with id {fruit_id} not found",
            )
        return fruit

    def get_all_fruits(self, skip: int = 0, limit: int = 100) -> List[Fruit]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_fruit(self, fruit_id: UUID, fruit_data: FruitUpdate) -> Fruit:
        fruit = self.repository.get_by_id(fruit_id)
        if not fruit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fruit with id {fruit_id} not found",
            )
        fruit.name = fruit_data.name
        return self.repository.update(fruit)

    def delete_fruit(self, fruit_id: UUID) -> None:
        fruit = self.repository.get_by_id(fruit_id)
        if not fruit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fruit with id {fruit_id} not found",
            )
        self.repository.delete(fruit)

    def create_multiple_fruits(self, fruits_data: List[FruitCreate]) -> List[Fruit]:
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

    def bulk_update_fruits(
        self, updates: List[tuple[UUID, FruitUpdate]]
    ) -> List[Fruit]:
        with transaction(self.repository.db):
            updated_fruits = []
            for fruit_id, fruit_data in updates:
                fruit = self.repository.get_by_id(fruit_id)
                if not fruit:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Fruit with id {fruit_id} not found",
                    )
                fruit.name = fruit_data.name
                updated_fruits.append(fruit)
            return updated_fruits

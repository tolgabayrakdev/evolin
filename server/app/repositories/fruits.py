from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Fruit
from .base import BaseRepository


class FruitRepository(BaseRepository[Fruit]):
    def __init__(self, db: Session):
        super().__init__(db, Fruit)

    def get_by_name(self, name: str) -> Optional[Fruit]:
        return self.db.query(Fruit).filter(Fruit.name.ilike(f"%{name}%")).first()

    def search_by_name(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Fruit]:
        return (
            self.db.query(Fruit)
            .filter(Fruit.name.ilike(f"%{search_term}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_sorted_by_name(self, skip: int = 0, limit: int = 100) -> List[Fruit]:
        return (
            self.db.query(Fruit)
            .order_by(Fruit.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

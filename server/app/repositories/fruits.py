"""
Fruit repository implementation.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from ..models import Fruit
from .base import BaseRepository


class FruitRepository(BaseRepository[Fruit]):
    """
    Repository for Fruit model operations.
    Inherits common CRUD operations from BaseRepository.
    Can add custom methods specific to Fruit model.
    """

    def __init__(self, db: Session):
        super().__init__(db, Fruit)

    def get_by_name(self, name: str) -> Optional[Fruit]:
        """
        Get fruit by name (case-insensitive).

        Args:
            name: Fruit name to search

        Returns:
            Fruit instance if found, None otherwise
        """
        return self.db.query(Fruit).filter(Fruit.name.ilike(f"%{name}%")).first()

    def search_by_name(
        self, search_term: str, skip: int = 0, limit: int = 100
    ) -> List[Fruit]:
        """
        Search fruits by name (case-insensitive partial match).

        Args:
            search_term: Search term for fruit name
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching fruits
        """
        return (
            self.db.query(Fruit)
            .filter(Fruit.name.ilike(f"%{search_term}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_sorted_by_name(self, skip: int = 0, limit: int = 100) -> List[Fruit]:
        """
        Get all fruits sorted by name alphabetically.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of fruits sorted by name
        """
        return (
            self.db.query(Fruit)
            .order_by(Fruit.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

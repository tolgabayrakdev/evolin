from app.extensions import db
from typing import Type, TypeVar, Generic
from contextlib import contextmanager

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
        self.db = db

    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        try:
            yield self.db.session
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise

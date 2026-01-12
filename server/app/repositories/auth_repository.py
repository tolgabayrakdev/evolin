from sqlalchemy.orm import Session

from ..models import User
from .base_repository import BaseRepository


class AuthRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

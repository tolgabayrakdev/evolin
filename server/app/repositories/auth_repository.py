from typing import Optional

from sqlalchemy.orm import Session

from ..models import User
from .base_repository import BaseRepository


class AuthRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def verify_user_credentials(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email)
        return user

    def create_user(self, email: str, hashed_password: str) -> User:
        user = User(email=email, password=hashed_password)
        return self.create(user)

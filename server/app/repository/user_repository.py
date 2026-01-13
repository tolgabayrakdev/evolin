from app.repository.base_repository import BaseRepository
from app.model.user import User
from typing import Optional


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.session.get(self.model, user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.session.query(self.model).filter(self.model.email == email).first()
        )

    def create(self, email: str, password: str) -> User:
        """Create a new user."""
        user = self.model(email=email, password=password)
        self.db.session.add(user)
        self.db.session.flush()
        return user

from typing import Optional

from sqlalchemy.orm import Session

from ..core.security import generate_access_token, generate_refresh_token, hash_password, verify_password
from ..models import User
from .base_repository import BaseRepository


class AuthRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def login(self, email: str, password: str) -> dict:
        user = self.get_by_email(email)
        
        if not user:
            raise ValueError("Invalid email or password")
        
        if not verify_password(password, user.password):
            raise ValueError("Invalid email or password")
        
        # Generate tokens
        token_data = {
            "user_id": str(user.id),
            "email": user.email
        }
        access_token = generate_access_token(token_data)
        refresh_token = generate_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Login successful",
            "user": user
        }

    def register(self, email: str, password: str) -> User:
        # Check if user already exists
        existing_user = self.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        hashed_password = hash_password(password)
        user = User(email=email, password=hashed_password)
        
        return self.create(user)

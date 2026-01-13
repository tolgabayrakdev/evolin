from app.repository.user_repository import UserRepository
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import generate_access_token, generate_refresh_token
from app.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def login(self, email: str, password: str):
        if not email or not password:
            raise ValueError("Email and password are required")

        user = self.user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found")

        if not verify_password(password, user.password):
            raise InvalidCredentialsError("Invalid email or password")

        access_token = generate_access_token(user.id, user.email)
        refresh_token = generate_refresh_token(user.id, user.email)

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def register(self, user_data: dict):
        email = user_data.get("email")
        password = user_data.get("password")

        if not email or not password:
            raise ValueError("Email and password are required")

        # Check if user already exists
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {email} already exists")

        # Hash the password
        hashed_password = hash_password(password)

        # Create user within a transaction
        with self.user_repository.transaction():
            user = self.user_repository.create(email=email, password=hashed_password)

        return user

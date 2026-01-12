from uuid import UUID

from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from ..config.settings import settings
from ..core.security import (
    generate_access_token,
    generate_refresh_token,
    hash_password,
    verify_password,
)
from ..repositories.auth_repository import AuthRepository
from ..schemas.auth_schema import TokenResponse, UserCreate, UserLogin, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.repository = AuthRepository(db)

    def register(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create user
        user = self.repository.create_user(
            email=user_data.email, hashed_password=hashed_password
        )

        return UserResponse.model_validate(user)

    def login(self, login_data: UserLogin, response: Response) -> TokenResponse:
        # Verify user credentials
        user = self.repository.get_by_email(
            email=login_data.email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Verify password
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Generate tokens (business logic in service layer)
        token_data = {"user_id": str(user.id), "email": user.email}
        access_token = generate_access_token(token_data)
        refresh_token = generate_refresh_token(token_data)

        token_response = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            message="Login successful",
            user=UserResponse.model_validate(user),
        )

        # Set HTTP-only cookies
        cookie_kwargs = {
            "httponly": True,
            "secure": settings.cookie_secure,
            "samesite": settings.cookie_same_site,
        }
        if settings.cookie_domain:
            cookie_kwargs["domain"] = settings.cookie_domain

        response.set_cookie(
            key="access_token",
            value=token_response.access_token,
            max_age=settings.access_token_expire_minutes * 60,
            **cookie_kwargs,
        )
        response.set_cookie(
            key="refresh_token",
            value=token_response.refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            **cookie_kwargs,
        )

        return token_response

    def get_current_user(self, user_id: UUID) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserResponse.model_validate(user)

    def logout(self, response: Response) -> dict:
        """Logout user by clearing cookies"""
        cookie_kwargs = {
            "httponly": True,
            "secure": settings.cookie_secure,
            "samesite": settings.cookie_same_site,
        }
        if settings.cookie_domain:
            cookie_kwargs["domain"] = settings.cookie_domain

        # Clear cookies by setting max_age to 0
        response.delete_cookie(key="access_token", **cookie_kwargs)
        response.delete_cookie(key="refresh_token", **cookie_kwargs)

        return {"message": "Logout successful"}

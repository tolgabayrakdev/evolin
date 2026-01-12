from uuid import UUID

from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from ..config.settings import settings
from ..repositories.auth_repository import AuthRepository
from ..schemas.auth_schema import TokenResponse, UserCreate, UserLogin, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.repository = AuthRepository(db)

    def register(self, user_data: UserCreate) -> UserResponse:
        try:
            user = self.repository.register(
                email=user_data.email,
                password=user_data.password
            )
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def login(self, login_data: UserLogin, response: Response) -> TokenResponse:
        try:
            result = self.repository.login(
                email=login_data.email,
                password=login_data.password
            )
            
            token_response = TokenResponse(
                access_token=result["access_token"],
                refresh_token=result["refresh_token"],
                message=result["message"],
                user=UserResponse.model_validate(result["user"])
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
                **cookie_kwargs
            )
            response.set_cookie(
                key="refresh_token",
                value=token_response.refresh_token,
                max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
                **cookie_kwargs
            )
            
            return token_response
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

    def get_current_user(self, user_id: UUID) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
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

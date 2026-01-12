from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import verify_token
from ..database import get_db
from ..schemas.auth_schema import UserResponse
from ..services.auth_service import AuthService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_current_user(
    access_token: str = Cookie(None),
    service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    payload = verify_token(access_token, token_type="access")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = UUID(payload.get("user_id"))
    return service.get_current_user(user_id)

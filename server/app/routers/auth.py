from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user
from ..database import get_db
from ..schemas.auth_schema import TokenResponse, UserCreate, UserLogin, UserResponse
from ..services.auth_service import AuthService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
async def register(user_data: UserCreate, service: AuthService = Depends(get_service)):
    return service.register(user_data)


@router.post("/login", response_model=TokenResponse, tags=["auth"])
async def login(
    login_data: UserLogin,
    response: Response,
    service: AuthService = Depends(get_service),
):
    return service.login(login_data, response)


@router.get("/me", response_model=UserResponse, tags=["auth"])
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.post("/logout", tags=["auth"], status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    service: AuthService = Depends(get_service),
):
    return service.logout(response)

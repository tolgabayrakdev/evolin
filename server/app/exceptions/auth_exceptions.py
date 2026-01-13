from typing import Optional
from app.exceptions.base_exceptions import BaseAppException


class AuthenticationError(BaseAppException):
    """Base exception for authentication related errors."""
    
    def __init__(self, message: str = "Authentication error", status_code: int = 401, description: Optional[str] = None):
        super().__init__(message, status_code, description)


class UserNotFoundError(AuthenticationError):
    """Raised when a user is not found."""
    
    def __init__(self, message: str = "User not found", description: Optional[str] = None):
        super().__init__(message, 404, description)


class UserAlreadyExistsError(AuthenticationError):
    """Raised when trying to create a user that already exists."""
    
    def __init__(self, message: str = "User already exists", description: Optional[str] = None):
        super().__init__(message, 409, description)


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid."""
    
    def __init__(self, message: str = "Invalid credentials", description: Optional[str] = None):
        super().__init__(message, 401, description)

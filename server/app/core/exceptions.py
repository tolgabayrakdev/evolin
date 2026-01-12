"""
Custom exception classes for the application.
"""
from fastapi import HTTPException, status


class BaseAppException(Exception):
    """Base exception for all application exceptions."""
    pass


class NotFoundError(BaseAppException):
    """Raised when a resource is not found."""
    def __init__(self, resource: str, identifier: str | int):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id {identifier} not found")


class DatabaseError(BaseAppException):
    """Raised when a database operation fails."""
    pass


def raise_not_found(resource: str, identifier: str | int) -> HTTPException:
    """Helper function to raise 404 HTTPException."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id {identifier} not found"
    )


def raise_service_unavailable(detail: str = "Service is currently unavailable") -> HTTPException:
    """Helper function to raise 503 HTTPException."""
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=detail
    )

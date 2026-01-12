from fastapi import HTTPException, status


class BaseAppException(Exception):
    pass


class NotFoundError(BaseAppException):
    def __init__(self, resource: str, identifier: str | int):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id {identifier} not found")


class DatabaseError(BaseAppException):
    pass


def raise_not_found(resource: str, identifier: str | int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id {identifier} not found"
    )


def raise_service_unavailable(detail: str = "Service is currently unavailable") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=detail
    )

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.fruit_service import FruitService
from ..schemas.fruit_schema import FruitCreate, FruitUpdate, FruitResponse

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> FruitService:
    try:
        return FruitService(db)
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is not available"
        )


@router.post("/fruits", response_model=FruitResponse, status_code=status.HTTP_201_CREATED, tags=["fruits"])
async def create_fruit(fruit: FruitCreate, service: FruitService = Depends(get_service)):
    return service.create_fruit(fruit)


@router.get("/fruits", response_model=List[FruitResponse], tags=["fruits"])
async def get_fruits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: FruitService = Depends(get_service)
):
    return service.get_all_fruits(skip=skip, limit=limit)


@router.get("/fruits/{fruit_id}", response_model=FruitResponse, tags=["fruits"])
async def get_fruit(fruit_id: UUID, service: FruitService = Depends(get_service)):
    return service.get_fruit_by_id(fruit_id)


@router.put("/fruits/{fruit_id}", response_model=FruitResponse, tags=["fruits"])
async def update_fruit(fruit_id: UUID, fruit: FruitUpdate, service: FruitService = Depends(get_service)):
    return service.update_fruit(fruit_id, fruit)


@router.delete("/fruits/{fruit_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["fruits"])
async def delete_fruit(fruit_id: UUID, service: FruitService = Depends(get_service)):
    service.delete_fruit(fruit_id)

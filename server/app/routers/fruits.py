"""
Fruit API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.fruits import FruitService
from ..schemas.fruits import FruitCreate, FruitUpdate, FruitResponse
from ..core.exceptions import raise_service_unavailable

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> FruitService:
    """
    Dependency to get FruitService instance.
    
    Args:
        db: Database session
        
    Returns:
        FruitService instance
        
    Raises:
        HTTPException: If database connection is not available
    """
    try:
        return FruitService(db)
    except ConnectionError:
        raise raise_service_unavailable("Database connection is not available")


@router.post("/fruits", response_model=FruitResponse, status_code=status.HTTP_201_CREATED, tags=["fruits"])
async def create_fruit(fruit: FruitCreate, service: FruitService = Depends(get_service)):
    return service.create_fruit(fruit)


@router.get(
    "/fruits",
    response_model=List[FruitResponse],
    tags=["fruits"],
    summary="Get all fruits",
    description="Retrieve a list of all fruits with pagination"
)
async def get_fruits(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: FruitService = Depends(get_service)
):
    """
    Get all fruits with pagination.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        service: FruitService dependency
        
    Returns:
        List of fruits
    """
    return service.get_all_fruits(skip=skip, limit=limit)


@router.get("/fruits/{fruit_id}", response_model=FruitResponse, tags=["fruits"])
async def get_fruit(fruit_id: int, service: FruitService = Depends(get_service)):
    return service.get_fruit_by_id(fruit_id)


@router.put("/fruits/{fruit_id}", response_model=FruitResponse, tags=["fruits"])
async def update_fruit(fruit_id: int, fruit: FruitUpdate, service: FruitService = Depends(get_service)):
    return service.update_fruit(fruit_id, fruit)


@router.delete("/fruits/{fruit_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["fruits"])
async def delete_fruit(fruit_id: int, service: FruitService = Depends(get_service)):
    service.delete_fruit(fruit_id)

"""
Pydantic schemas for Fruit API.
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class FruitBase(BaseModel):
    """Base schema for Fruit with common fields."""
    name: str = Field(..., min_length=1, max_length=30, description="Fruit name")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and normalize fruit name."""
        if not v or not v.strip():
            raise ValueError("Fruit name cannot be empty")
        return v.strip().title()  # Capitalize first letter of each word


class FruitCreate(FruitBase):
    """Schema for creating a new fruit."""
    pass


class FruitUpdate(BaseModel):
    """Schema for updating a fruit."""
    name: str = Field(..., min_length=1, max_length=30, description="Fruit name")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and normalize fruit name."""
        if not v or not v.strip():
            raise ValueError("Fruit name cannot be empty")
        return v.strip().title()


class FruitResponse(FruitBase):
    """Schema for fruit response."""
    id: int = Field(..., description="Fruit ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Apple",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
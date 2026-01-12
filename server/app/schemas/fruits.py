from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class FruitBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Fruit name cannot be empty")
        return v.strip().title()


class FruitCreate(FruitBase):
    pass


class FruitUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Fruit name cannot be empty")
        return v.strip().title()


class FruitResponse(FruitBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

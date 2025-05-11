from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    class Config:
        # Это заставит Pydantic не принимать другие поля, которые не указаны в модели
        extra = "forbid"


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    @validator("full_amount")
    def validate_full_amount(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Требуемая сумма должна быть больше 0")
        return value
        
    class Config:
        # Это заставит Pydantic не принимать другие поля, которые не указаны в модели
        extra = "forbid"


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
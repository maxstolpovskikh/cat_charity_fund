from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    """Схема создания проекта."""


class CharityProjectUpdate(BaseModel):
    """Схема обновления проекта."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    @validator('full_amount')
    def validate_full_amount(cls, value):
        if value is not None and value <= 0:
            raise ValueError('Требуемая сумма должна быть больше 0')
        return value

    class Config:
        extra = 'forbid'


class CharityProjectDB(CharityProjectBase):
    """Схема проекта."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
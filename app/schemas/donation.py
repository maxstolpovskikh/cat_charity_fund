from datetime import datetime

from pydantic import BaseModel, PositiveInt
from typing import Optional


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """Схема создания пожертвования."""


class DonationDB(BaseModel):
    """Схема пожертвования."""
    id: int
    create_date: datetime
    full_amount: PositiveInt
    comment: Optional[str] = None

    class Config:
        orm_mode = True


class DonationAdminDB(BaseModel):
    """Схема пожертвования для администратора."""
    id: int
    user_id: int
    full_amount: PositiveInt
    comment: Optional[str] = None
    create_date: datetime
    fully_invested: bool
    invested_amount: int
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True

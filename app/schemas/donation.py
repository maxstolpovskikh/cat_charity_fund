from datetime import datetime

from pydantic import BaseModel, PositiveInt
from typing import Optional

class DonationBase(BaseModel):
    comment: str
    full_amount: PositiveInt
    
class DonationCreate(DonationBase):
    pass

class DonationDB(DonationBase):
    id: int
    user_id: int
    #invested_amount: int = 0
    #fully_invested: bool
    full_amount: PositiveInt
    create_date: datetime
    user_id: int
    
    class Config:
        orm_mode = True

class DonationAdminDB(BaseModel):
    id: int
    user_id: int
    full_amount: PositiveInt
    comment: Optional[str] = None
    create_date: datetime
    fully_invested: bool  # Убедитесь, что это поле есть
    invested_amount: int
    close_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True
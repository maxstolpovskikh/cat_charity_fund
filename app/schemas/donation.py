from datetime import datetime

from pydantic import BaseModel, PositiveInt

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
    create_date: datetime
    user_id: int
    
    class Config:
        orm_mode = True

class DonationAdminDB(DonationDB):
    invested_amount: int = 0
    fully_invested: bool
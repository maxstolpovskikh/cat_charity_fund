from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text

from .base import AbstractBaseModel


class Donation(AbstractBaseModel):
    user_id = Column(Integer, ForeignKey(
        'user.id',
        name='fk_donation_user_id_user',)
    )
    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, default=False)
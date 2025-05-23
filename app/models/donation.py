from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import AbstractBaseModel


class Donation(AbstractBaseModel):
    """Модель пожертвования."""
    user_id = Column(Integer, ForeignKey(
        'user.id',
        name='fk_donation_user_id_user',)
    )
    comment = Column(Text, nullable=True)

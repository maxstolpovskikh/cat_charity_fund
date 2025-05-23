from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class AbstractBaseModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    @property
    def available_amount(self):
        """Возвращает доступную для инвестирования сумму."""
        return self.full_amount - self.invested_amount

    def invest(self, amount: int):
        """Инвестирует указанную сумму в объект."""
        self.invested_amount += amount
        if self.invested_amount >= self.full_amount:
            self.fully_invested = True
            self.close_date = datetime.now()
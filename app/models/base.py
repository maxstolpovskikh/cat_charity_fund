from datetime import datetime
from typing import Annotated

from pydantic import Field
from sqlalchemy import Column, Integer, DateTime

from app.core.db import Base

PositiveInt = Annotated[int, Field(gt=0)]

class AbstractBaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, nullable=True)

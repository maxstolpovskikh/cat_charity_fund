from sqlalchemy import Column, String, Text

from .base import AbstractBaseModel


class CharityProject(AbstractBaseModel):
    """Модель благотворительного проекта."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

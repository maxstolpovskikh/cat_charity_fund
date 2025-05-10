from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable  # noqa

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass

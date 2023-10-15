from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)

    exercises = relationship("Exercise", back_populates="user")

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return str(self.name)

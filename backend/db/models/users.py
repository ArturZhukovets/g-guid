import datetime
import enum

from db.db import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class UserRoles(enum.Enum):
    COACH = "Coach"
    NUTRITIONIST = "Nutritionist"
    USER = "User"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    role = Column(Enum(UserRoles), default=UserRoles.USER)

    exercises = relationship("Exercise", back_populates="user")
    subscriptions = relationship(
        "UserSubscription",
        backref="user",
        foreign_keys="[UserSubscription.owner_id]",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return str(self.name)


class UserSubscription(Base):
    __tablename__ = "user_subscription"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    coach_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    subscription_date = Column(DateTime, default=datetime.datetime.utcnow)

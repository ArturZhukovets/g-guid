import enum
from datetime import datetime

from db.db import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as EnumSQL
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship


class ExerciseCategory(str, enum.Enum):
    LEGS = "Legs"
    BACK = "Back"
    Chest = "Chest"


class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(EnumSQL(ExerciseCategory), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    slug = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="exercises")

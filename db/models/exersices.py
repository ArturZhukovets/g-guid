import enum
from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, Enum as EnumSQL
from sqlalchemy.orm import relationship
from db.db import Base


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



from pydantic import BaseModel, Field, ConfigDict

from schemas.exercises import ShowExercise


class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=4)

class UserDelete(BaseModel):
    id: int


class ShowUser(UserBase):
    id: int
    is_superuser: bool
    exercises: list[ShowExercise]

    model_config = ConfigDict(from_attributes=True)

    # # Todo del after check
    # class Config:
    #     from_attributes = True

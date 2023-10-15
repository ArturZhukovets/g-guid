from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from schemas.exercises import ShowExercise


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=4)


class UserDelete(BaseModel):
    id: int


class ShowUser(UserBase):
    """For showing list of users"""

    id: int
    is_superuser: bool
    exercises: list[ShowExercise]

    model_config = ConfigDict(from_attributes=True)


class ShowUserDetail(ShowUser):
    """For showing specified user"""

    pass

    # # Todo del after check
    # class Config:
    #     from_attributes = True

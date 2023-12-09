from typing import Optional

from db.models.users import UserRoles
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
    role: Optional[UserRoles]
    model_config = ConfigDict(from_attributes=True)


class ShowUserDetail(ShowUser):
    """For showing specified user"""

    exercises: list[ShowExercise]
    role: Optional[UserRoles]


class ChangeUserRole(BaseModel):
    id: int
    role: UserRoles


# ============================================== Subscriptions |


class SubscribeOnCoach(BaseModel):
    coach_id: int

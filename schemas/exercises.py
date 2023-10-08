from datetime import datetime
from typing import Optional

import pydantic
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from slugify import slugify

from db.models.exersices import ExerciseCategory


class ExerciseBase(BaseModel):
    title: str
    description: str
    category: ExerciseCategory


class ExerciseCreate(ExerciseBase):
    # user_id: int
    slug: Optional[str] = None

    @pydantic.model_validator(mode="before")
    def generate_slug(cls, values):
        if "title" in values:
            values["slug"] = slugify(values.get("title"))
        return values


class ExerciseUpdate(ExerciseCreate):
    user_id: int = Field(gt=0)


class ShowExercise(ExerciseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    # TODO deprecated delete after check
    # class Config:
    #     from_attributes = True

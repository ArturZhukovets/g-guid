from sqlalchemy.orm import Session

from db.models.exersices import ExerciseCategory
from db.repository.exercises import create_new_exercise
from schemas.exercises import ExerciseCreate


def create_random_exercise(db: Session, user_id: int):
    exercise_pydantic = ExerciseCreate(
        title="Test Exercise",
        description="Some test description",
        category=ExerciseCategory.LEGS,
    )
    exercise = create_new_exercise(exercise_pydantic, db, user_id)
    return exercise


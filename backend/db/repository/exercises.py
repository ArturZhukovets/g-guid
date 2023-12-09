from db.models.exersices import Exercise
from db.models.users import User
from db.models.users import UserRoles
from fastapi import HTTPException
from fastapi import status
from schemas.exercises import ExerciseCreate
from schemas.exercises import ExerciseUpdate
from sqlalchemy.orm import Session


def create_new_exercise(
    exercise: ExerciseCreate, db: Session, user_id: int
) -> Exercise | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user does not exist",
        )
    if not user.role == UserRoles.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can create exercise only with role `Coach`."
            f" Your role right now is `{user.role.value}`",
        )
    exercise = Exercise(**exercise.model_dump(), user_id=user_id)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def retrieve_exercise(exercise_id: int, db: Session) -> Exercise | None:
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    return exercise


# todo Type hint of this function
def retrieve_exercises_list(user: User, db: Session) -> list[Exercise]:
    exercises = db.query(Exercise).filter(Exercise.user_id == user.id).all()
    return exercises


def update_exercise(
    exercise_id: int, exercise: ExerciseUpdate, db: Session
) -> Exercise | None:
    exercise_instance = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise_instance:
        return
    if not db.query(User).filter(User.id == exercise.user_id).first():
        return

    exercise_instance.title = exercise.title
    exercise_instance.description = exercise.description
    exercise_instance.category = exercise.category
    exercise_instance.slug = exercise.slug
    exercise_instance.user_id = exercise.user_id
    db.add(exercise_instance)
    db.commit()
    return exercise_instance


def delete_exercise(exercise_id: int, user: User, db: Session) -> None:
    user_exercises_ids = [ex_id.id for ex_id in user.exercises]
    if exercise_id not in user_exercises_ids:
        raise ValueError("The specified exercise is not in your list of exercises")
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id)
    if not exercise.first():
        raise ValueError(f"No such exercise with id - {exercise_id}")
    exercise.delete()
    db.commit()

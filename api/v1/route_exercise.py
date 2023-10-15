from typing import List
from typing import Type

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api.v1.route_auth import get_current_user
from db import get_db
from db.models.users import User
from db.repository.exercises import create_new_exercise
from db.repository.exercises import delete_exercise
from db.repository.exercises import retrieve_exercise
from db.repository.exercises import retrieve_exercises_list
from db.repository.exercises import update_exercise
from schemas.exercises import ExerciseCreate
from schemas.exercises import ExerciseUpdate
from schemas.exercises import ShowExercise

router = APIRouter()


@router.get("/list-exercises/", response_model=List[ShowExercise])
def exercises_list(user_id: int, db: Session = Depends(get_db)) -> List[ShowExercise]:
    """Retrieve list of exercises of specified user"""
    exercises = retrieve_exercises_list(user_id, db)
    return exercises


@router.post(
    "/create-exercise", response_model=ShowExercise, status_code=status.HTTP_201_CREATED
)
async def exercise_create(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create exersice related with specified user"""
    exercise = create_new_exercise(exercise, db, current_user.id)
    return exercise


@router.get(
    "/{exercise_id}", response_model=ShowExercise, status_code=status.HTTP_200_OK
)
async def exercise_retrieve(exercise_id: int, db: Session = Depends(get_db)):
    """Retrieve exercise by specified id"""
    exercise = retrieve_exercise(exercise_id, db)
    if not exercise:
        raise HTTPException(
            detail=f"Exercise with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return exercise


@router.put("/update-exercise/{exercise_id}", response_model=ShowExercise)
async def exercise_update(
    exercise_id: int, exercise: ExerciseUpdate, db: Session = Depends(get_db)
):
    """Update specified exercise"""
    exercise = update_exercise(exercise_id, exercise, db)
    if not exercise:
        return HTTPException(
            detail=f"Exercise with id: {exercise_id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return exercise


async def exercise_delete(
    exercise_id: int, db: Session = Depends(get_db)
) -> dict[str, str]:
    try:
        delete_exercise(exercise_id, db)
    except ValueError:
        raise HTTPException(
            detail=f"Exercise with id {exercise_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return {"msg": "Exercise was successfully deleted"}

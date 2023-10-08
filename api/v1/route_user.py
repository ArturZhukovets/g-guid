from typing import List

from fastapi import APIRouter, status
from fastapi import Depends
from sqlalchemy.orm import Session

from schemas.users import UserCreate, ShowUser
from db import get_db
from db.repository.users import create_new_user, retrieve_all_users


router = APIRouter()


@router.get("/", response_model=List[ShowUser])
def users_list(db: Session = Depends(get_db)):
    return retrieve_all_users(db)


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/delete_user")
def delete_user(user_id: int):
    # TODO after realizing authentication
    pass


from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from db import get_db
from db.repository.users import create_new_user
from db.repository.users import retrieve_all_users
from schemas.users import ShowUser
from schemas.users import UserCreate


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

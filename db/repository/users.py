from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.users import User
from schemas.users import UserCreate


def create_new_user(user: UserCreate, db: Session, is_superuser: bool = False) -> User:
    if db.query(User).filter(User.name == user.name).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with specified username already exist",
        )
    db_user = User(
        name=user.name,
        password=Hasher.get_password_hash(user.password),
        is_superuser=is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def retrieve_all_users(db: Session) -> List[User]:
    return db.query(User).all()

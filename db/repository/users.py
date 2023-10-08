from typing import List

from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session, is_superuser: bool = False) -> User:
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


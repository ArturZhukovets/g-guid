from db.models.users import User
from db.repository.users import create_new_user
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_random_user(db: Session) -> User:
    user_pydantic = UserCreate(name="Artur", password="HelloSupaDupaWorld_")
    user = create_new_user(user=user_pydantic, db=db)
    return user

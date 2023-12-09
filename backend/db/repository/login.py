from typing import Optional

from db.models.users import User
from sqlalchemy.orm import Session


def get_user(name: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.name == name).first()
    return user

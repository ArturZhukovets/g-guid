from typing import Optional

from sqlalchemy.orm import Session

from db.models.users import User


def get_user(name: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.name == name).first()
    return user

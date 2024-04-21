# Dependencies
from api.v1.route_auth import oauth2_scheme
from core.config import settings
from db import get_db
from db.models.users import User
from db.repository.login import get_user
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from jose import JWTError
from sqlalchemy.orm import Session


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ENCODE_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(name=username, db=db)
    if user is None:
        raise credentials_exception
    return user


def verify_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Verify if current user is admin.
    Return current user if it True.
    Raise a permission denied exception if it False.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. You should be a superuser",
        )
    return current_user

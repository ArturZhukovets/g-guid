from typing import Optional

from core.hashing import Hasher
from core.security import create_access_token
from db import get_db
from db.models.users import User
from db.repository.login import get_user
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token
from sqlalchemy.orm import Session

# "/auth"
router = APIRouter()


def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    user = get_user(name=username, db=db)
    print("USER IS ")
    print(user)
    if not user:
        return
    if not Hasher.verify_password(password, user.password):
        return

    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login by specified username and password.
    :return: Access Token with user id, username and expire time.
    """

    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.name, "id": user.id})
    return Token(access_token=access_token, token_type="Bearer")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

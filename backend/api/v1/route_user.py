from typing import Final
from typing import List

from api.v1.route_auth import get_current_user
from db import get_db
from db.models.users import User
from db.models.users import UserRoles
from db.repository.users import create_new_user
from db.repository.users import get_user_subscriptions
from db.repository.users import retrieve_all_users
from db.repository.users import subscribe_user_on_coach
from db.repository.users import UsersRepository
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.users import ChangeUserRole
from schemas.users import ShowUser
from schemas.users import SubscribeOnCoach
from schemas.users import UserCreate
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/", response_model=List[ShowUser])
def users_list():
    users = UsersRepository().select_all_records()
    return users


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    data = user.model_dump()
    try:
        user = UsersRepository().add_record(data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating user",
        )
    return user


@router.delete("/delete_user")
def delete_user(user_id: int, admin_user: User = Depends(get_current_user)):
    res = UsersRepository().delete_record(delete_by_field="id", value=user_id)
    if res == 0:
        raise HTTPException(
            status_code=404, detail=f"User with id={user_id} does not exist"
        )
    return {"msg": "User successfully deleted"}


@router.post("/change_user_role")
def change_user_role(user_role: ChangeUserRole, current_user=Depends(get_current_user)):
    user = UsersRepository().change_user_role(user_role.id, user_role.role.name)
    return user


# ============================================================= Subscriptions |

# TODO Write tests for subscriptions (if it needed)
@router.get("/subscriptions", response_model=List[ShowUser])
def user_subscriptions(current_user: User = Depends(get_current_user)):
    repository = UsersRepository()
    result: Final = repository.get_user_subscriptions(current_user)
    return result


@router.post("/subscribe_on_coach")
def subscribe(
    subscribe_on: SubscribeOnCoach,
    current_user: User = Depends(get_current_user),
):
    user_role = current_user.role
    if user_role != UserRoles.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"It's not possible to subscribe on {user_role.value}",
        )
    repository = UsersRepository()
    repository.subscribe(current_user, subscribe_on.coach_id)
    return {"msg": "Subscribed successfully"}

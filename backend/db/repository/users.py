from typing import List
from typing import Type

from core.hashing import Hasher
from db.db import SessionLocal
from db.models.users import User
from db.models.users import UserRoles
from db.models.users import UserSubscription
from db.repository.repository import SQLAlchemyRepository
from fastapi import HTTPException
from fastapi import status
from schemas.users import SubscribeOnCoach
from schemas.users import UserCreate
from sqlalchemy.orm import Session


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


def subscribe_user_on_coach(
    subscribe_on: SubscribeOnCoach,
    subscription_owner_id: int,
    db: Session,
) -> UserSubscription:
    user = db.query(User).get(subscription_owner_id)
    user_role = user.role
    if user_role != UserRoles.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"It's not possible to subscribe on {user_role.value}",
        )
    subscription = UserSubscription(
        owner_id=subscription_owner_id,
        coach_id=subscribe_on.coach_id,
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def get_user_subscriptions(user: User, db: Session) -> list[User]:
    subscriptions = user.subscriptions
    list_of_ids = [sub.coach_id for sub in subscriptions]
    subscriptions_list = db.query(User).filter(User.id.in_(list_of_ids)).all()

    return subscriptions_list


class UsersRepository(SQLAlchemyRepository):
    # TODO Think about working with Depends(get_current_user) in this class
    model = User

    def change_user_role(self, user_id: int, role: str):
        # TODO REPLACE IT WITH ABSTRACT "UPDATE" METHOD AND CHANGE USER ROLE ONLY FROM SERVICES
        # TODO Realize only user with admin privileges can change user role
        with SessionLocal() as session:
            db_user = session.query(self.model).filter(self.model.id == user_id).first()
            if not db_user:
                raise ValueError(f"User with id={user_id} does not exist")
            db_user.role = role

            session.commit()
            session.refresh(db_user)
            return db_user

    def get_user_subscriptions(self, cur_user: User) -> list[User]:
        with SessionLocal() as session:
            ids = [sub.coach_id for sub in cur_user.subscriptions]
            subs_list2 = session.query(self.model).filter(self.model.id.in_(ids)).all()
            return subs_list2

    def subscribe(self, cur_user: User, subscribe_on_id: int):
        with SessionLocal() as session:
            subscription = UserSubscription(
                owner_id=cur_user.id,
                coach_id=subscribe_on_id,
            )
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            return subscription

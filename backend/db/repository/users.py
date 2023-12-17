from db.db import SessionLocal
from db.models.users import User
from db.models.users import UserSubscription
from db.repository.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    # TODO Think about working with Depends(get_current_user) in this class
    model = User

    def change_user_role(self, user_id: int, role: str):
        """Change specified user role"""
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
        """Return all subscriptions of specified user"""
        with SessionLocal() as session:
            ids = [sub.coach_id for sub in cur_user.subscriptions]
            subs_list2 = session.query(self.model).filter(self.model.id.in_(ids)).all()
            return subs_list2

    def subscribe(self, cur_user: User, subscribe_on_id: int):
        """Subscribe specified user on coach (which is also a user with Coach category)"""
        with SessionLocal() as session:
            subscription = UserSubscription(
                owner_id=cur_user.id,
                coach_id=subscribe_on_id,
            )
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            return subscription

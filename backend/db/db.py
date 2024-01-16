from typing import Generator

import sqlalchemy
from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# print("Database URL is ", SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except Exception:
        db.rollback()
    finally:
        print("CALL CLOSE()")
        db.close()


# TODO Check how to use this approach.
#  (I need to create my own custom Dependency class and use it as dependency)
# class DatabaseSessionMixin:
#     """Database session mixin."""
#
#     def __enter__(self) -> Session:
#         self.db = SessionLocal()
#         return self.db
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         try:
#             if exc_type is not None:
#                 self.db.rollback()
#         except sqlalchemy.exc.SQLAlchemyError:
#             pass
#         finally:
#             self.db.close()
#             SessionLocal.remove()
#
#
# def use_database_session():
#     return DatabaseSessionMixin()

Base = declarative_base()

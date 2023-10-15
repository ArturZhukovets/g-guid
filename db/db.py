from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
print("Database URL is ", SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# @as_declarative()
# class Base:
#     # id = Column(Integer, primary_key=True)
#     id: Any
#     __name__: str
#
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

Base = declarative_base()

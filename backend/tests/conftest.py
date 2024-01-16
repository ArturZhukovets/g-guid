import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# this is to include backend dir in sys.path so that we can import from db,main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.users import UserCreate
from db import get_db
from db.base import Base
from api.base import api_router

from db.repository.users import UsersRepository
from core.hashing import Hasher
from core.config import settings
from tests.utils.user import auth_token_by_user_credentials


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def user(db_session: SessionTesting):
    password = Hasher.get_password_hash(settings.TEST_USER_PASSWORD)
    user_pydantic = UserCreate(name=settings.TEST_USER_NAME, password=password)
    repository = UsersRepository(db_session)
    data = user_pydantic.model_dump()
    user = repository.add_record(data)
    return user


@pytest.fixture(scope="module")
def admin_user(db_session: SessionTesting):
    password = Hasher.get_password_hash(settings.TEST_ADMIN_PASSWORD)
    user_pydantic = UserCreate(name=settings.TEST_ADMIN_NAME, password=password)
    repository = UsersRepository(db_session)
    data = user_pydantic.model_dump()
    data["is_superuser"] = True
    user = repository.add_record(data)
    return user


@pytest.fixture(scope="module")
def admin_authorization_token_header(client: TestClient, admin_user) -> dict[str, str]:
    username = admin_user.name
    password = settings.TEST_ADMIN_PASSWORD
    authorization_token = auth_token_by_user_credentials(
        client=client, username=username, password=password
    )
    header = {"Authorization": f"Bearer {authorization_token}"}
    return header

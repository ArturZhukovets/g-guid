from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional

from db.db import SessionLocal
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select


class AbstractRepository(ABC):
    @abstractmethod
    def add_record(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def select_all_records(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_record(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def select_all_records(self, filter_condition: Optional[dict] = None):
        with SessionLocal() as session:

            statement = select(self.model)
            if filter_condition:
                statement.filter_by(**filter_condition)
            res = session.execute(statement=statement)
            # TODO refactor (maybe there is a better way how to fetch all records)
            res = res.scalars().all()
            return res

    def add_record(self, data: dict):
        with SessionLocal() as session:
            statement = insert(self.model).values(**data).returning(self.model)
            res = session.execute(statement=statement)
            session.commit()
            return res.scalar_one()

    def delete_record(self, delete_by_field: str, value: Any):
        with SessionLocal() as session:
            statement = delete(self.model).where(
                getattr(self.model, delete_by_field) == value
            )
            res = session.execute(statement=statement)
            session.commit()
            return res.rowcount

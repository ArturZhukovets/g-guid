from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import Sequence

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    @abstractmethod
    def add_record(self, *args, **kwargs):
        """Add only one record of specified model"""
        raise NotImplementedError

    @abstractmethod
    def select_all_records(self, *args, **kwargs):
        """Select all records of specified model"""
        raise NotImplementedError

    @abstractmethod
    def delete_record(self, **kwargs):
        """Delete only one record by specified in kwargs conditions"""
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: Session) -> None:
        # if not session:
        #     session = get_db().__next__()
        self.session = session

    def select_all_records(self, condition: Optional[dict] = None) -> Sequence:
        statement = select(self.model)
        if condition:
            statement.filter_by(**condition)
        res = self.session.execute(statement=statement)
        # TODO refactor (maybe there is a better way how to fetch all records)
        res = res.scalars().all()
        return res

    def add_record(self, data: dict):
        statement = insert(self.model).values(**data).returning(self.model)
        res = self.session.execute(statement=statement)
        self.session.commit()
        return res.scalar_one()

    def delete_record(self, **kwargs) -> int:
        record = self.session.query(self.model).filter_by(**kwargs).first()
        self.session.delete(record)
        self.session.commit()
        return record.id

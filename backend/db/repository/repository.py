from abc import ABC
from abc import abstractmethod
from typing import Optional, Any
from typing import Sequence

from sqlalchemy import insert, asc, desc, Select, func
from sqlalchemy import select
from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    @abstractmethod
    def add_record(self, *args, **kwargs):
        """Add only one record of specified model"""
        raise NotImplementedError

    @abstractmethod
    def select_records(self, *args, **kwargs):
        """Select all records of specified model"""
        raise NotImplementedError

    @abstractmethod
    def delete_record(self, **kwargs):
        """Delete only one record by specified in kwargs conditions"""
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: Session) -> None:
        self.session = session

    def select_records(
        self,
        condition: Optional[dict] = None,
        order: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> Sequence:
        statement = select(self.model)
        if condition:
            statement = statement.filter_by(**condition)
        if order_by:
            statement = self.repository_order_by(statement, field=order_by, order=order)
        statement = statement.limit(limit).offset(offset)
        res = self.session.execute(statement=statement)
        res = res.scalars().all()
        return res

    def add_record(self, data: dict) -> Any:
        statement = insert(self.model).values(**data).returning(self.model)
        res = self.session.execute(statement=statement)
        self.session.commit()
        return res.scalar_one()

    def delete_record(self, **kwargs) -> int:
        record = self.session.query(self.model).filter_by(**kwargs).first()
        self.session.delete(record)
        self.session.commit()
        return record.id

    def get_record_by_id(self, record_id: int) -> Any:
        record = self.session.query(self.model).filter_by(id=record_id).first()
        if not record:
            raise ValueError(f"Record with id={record_id} does not exist")
        return record

    @staticmethod
    def order_to_orm(order_value: str) -> asc or desc:
        if order_value == "asc":
            return asc
        elif order_value == "desc":
            return desc

    def repository_order_by(self, statement: Select, field: str, order: str) -> Select:
        order = SQLAlchemyRepository.order_to_orm(order_value=order)
        return statement.order_by(order(getattr(self.model, field)))

    def select_count_of_records(self) -> int:
        statement = select(func.count(self.model.id))
        return self.session.scalar(statement)

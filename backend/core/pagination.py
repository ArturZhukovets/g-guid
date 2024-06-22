from enum import Enum
from typing import Generic, TypeVar, Optional, Callable

from fastapi import Query
from pydantic import BaseModel, Field, AnyHttpUrl

from db.repository.repository import AbstractRepository, SQLAlchemyRepository

M = TypeVar("M")

class SortOrderEnum(Enum):
    ASC: str = "asc"
    DESC: str = "desc"


# class PaginatedParams(BaseModel):
#     limit: int
#     offset: int
#     order: str

class PaginationParams(BaseModel):
    page: int
    per_page: int
    order: str


class PaginatedResponse(BaseModel, Generic[M]):
    count: int = Field(description="Number of items returned in the response")
    items: list[M] = Field(description="List of items returned in the response")
    next_page: Optional[AnyHttpUrl] = Field(None, description='url of the next page if it exists')
    prev_page: Optional[AnyHttpUrl] = Field(None, description='url of the previous page if it exists')


class Paginator:
    # TODO Попробовать зарефакторить этот класс. Убрать request(он по сути не нужен).
    #  Имплементировать логику пагинатора где-нибудь прямо внутри Репозитория.
    #  Просто отдавать от метода репозитория Query и этот Query пагинировать.
    def __init__(
            self,
            request,
            repository: SQLAlchemyRepository,
            page: int,
            per_page: int,
            order: str = "asc",
            order_by: str = "id",
            filter_condition: Optional[dict] = None,
            select_method: Optional[Callable] = None,
    ):
        self._repository = repository

        self._filter_condition = filter_condition
        self._order = order
        self._order_by = order_by
        self.page = page
        self.per_page = per_page
        self.limit = per_page
        self.offset = page - 1 if page == 1 else (page - 1) * per_page
        self.request = request

        self.number_of_pages = 0
        self.next_page = ""
        self.prev_page = ""
        self._select_method = select_method if select_method is not None else repository.select_records

    def _get_next_page(self) -> Optional[str]:
        if self.page >= self.number_of_pages:
            return
        url = self.request.url.include_query_params(page=self.page + 1)
        return str(url)

    def _get_prev_page(self) -> Optional[str]:
        if self.page == 1 or self.page > self.number_of_pages + 1:
            return
        url = self.request.url.include_query_params(page=self.page - 1)
        return str(url)

    def _get_number_of_pages(self, total_count: int):
        rest = total_count % self.per_page
        quotient = total_count // self.per_page
        return quotient if not rest else quotient + 1

    def _get_data(self) -> tuple:
        result = self._select_method(
            order=self._order,
            offset=self.offset,
            limit=self.limit,
            order_by=self._order_by,
            condition=self._filter_condition,
        )
        if isinstance(result, tuple) and len(result) == 2:
            items, count = result
            return items, count
        count = self._repository.select_count_of_records()
        items = result
        return count, items

    def get_response(self) -> dict:
        count, items = self._get_data()
        self.number_of_pages = self._get_number_of_pages(total_count=count)
        return {
            'count': count,
            'next_page': self._get_next_page(),
            'prev_page': self._get_prev_page(),
            'items': items,
        }


def pagination_params(
    page: int = Query(ge=1, default=1, le=50),
    per_page: int = Query(ge=1, le=100, default=50),
    order: SortOrderEnum = SortOrderEnum.DESC,
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page, order=order.value)


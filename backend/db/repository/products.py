from typing import Optional, Tuple, Any, List, Type, Sequence

from sqlalchemy import func, select

from core.pagination import SortOrderEnum
from db.models.products import ProductCategory, ProductComposition
from db.models.products import ProductComposition
from db.repository.repository import SQLAlchemyRepository
from sqlalchemy.orm import joinedload


class ProductsRepository(SQLAlchemyRepository):
    model = ProductComposition

    def select_products(
        self,
        offset: int,
        limit: int,
        order: str = "asc",
        order_by: str = "id",
        condition: Optional[dict] = None,
    ) -> tuple[int, list[Type[ProductComposition]]]:
        order = SQLAlchemyRepository.order_to_orm(order_value=order)
        products = self.session.query(self.model).options(
            joinedload(self.model.category)
        ).order_by(order(self.model.id))
        if condition:
            products.filter_by(**condition)
        count = self.session.query(func.count(self.model.id)).scalar()
        products = products.offset(offset).limit(limit).all()
        return count, products

    # def paginate(
    #         self,
    #         limit: int,
    #         offset: int,
    #         order: str = "asc",
    #         condition: Optional[dict] = None
    # ) -> tuple[int, Sequence[Any]]:
    #     order = SQLAlchemyRepository.order_to_orm(order_value=order)
    #     query = select(self.model).order_by(order(self.model.id)).options(
    #                 joinedload(self.model.category)
    #     )
    #     count = self.session.scalar(select(func.count(self.model.id)))
    #     # query.options(joinedload(self.model.category))
    #     if condition:
    #         query.filter_by(**condition)
    #     items = self.session.scalars(statement=query.limit(limit).offset(offset)).all()
    #     return count, items

    def update_product(self, product_id: int, data: dict) -> Type[ProductComposition]:
        product = self.session.query(self.model).filter_by(id=product_id).first()
        if not product:
            raise ValueError("Product does not exist.")
        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        self.session.commit()
        return product


class ProductCategoryRepository(SQLAlchemyRepository):
    model = ProductCategory

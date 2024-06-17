from typing import Optional, Tuple, Any, List, Type, Sequence

from sqlalchemy import func, select

from core.pagination import SortOrderEnum
from db.models.products import ProductCategory, ProductComposition
from db.models.products import ProductComposition
from db.repository.repository import SQLAlchemyRepository
from sqlalchemy.orm import joinedload


class ProductsRepository(SQLAlchemyRepository):
    model = ProductComposition

    def select_products_by_title(
        self,
        offset: int,
        limit: int,
        condition: dict,
        order: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> tuple[int, list[Type[ProductComposition]]]:
        if "title" not in condition:
            raise ValueError("provide filter condition with keyword 'title' to use this method")
        title = condition['title']
        products = self.session.query(self.model).options(
            joinedload(self.model.category)
        ).filter(self.model.title.icontains(title))
        if order_by and order_by:
            order = SQLAlchemyRepository.order_to_orm(order_value=order)
            products = products.order_by(order(self.model.id))
        count = products.count()
        products = products.offset(offset).limit(limit).all()
        return count, products

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

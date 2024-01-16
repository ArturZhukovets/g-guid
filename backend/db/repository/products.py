from typing import Optional

from db.db import SessionLocal
from db.models.products import ProductCategory
from db.models.products import ProductComposition
from db.repository.repository import SQLAlchemyRepository
from sqlalchemy.orm import joinedload


class ProductsRepository(SQLAlchemyRepository):
    model = ProductComposition

    def select_all_with_categories(self, condition: Optional[dict] = None):
        with SessionLocal() as session:
            products = (
                session.query(self.model).options(joinedload(self.model.category)).all()
            )
            if condition:
                products.filter_by(**condition)
            return products


class ProductCategoryRepository(SQLAlchemyRepository):
    model = ProductCategory

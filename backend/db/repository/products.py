from typing import Optional

from db.models.products import ProductCategory
from db.models.products import ProductComposition
from db.repository.repository import SQLAlchemyRepository
from sqlalchemy.orm import joinedload
from sqlalchemy import desc


class ProductsRepository(SQLAlchemyRepository):
    model = ProductComposition

    def select_all_with_categories(
        self, offset: int, limit: int, condition: Optional[dict] = None
    ):
        products = self.session.query(self.model).options(
            joinedload(self.model.category)
        ).order_by(desc(self.model.id))
        if condition:
            products.filter_by(**condition)
        return products.offset(offset).limit(limit).all()

    def update_product(self, product_id: int, data: dict):
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

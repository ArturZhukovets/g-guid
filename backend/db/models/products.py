from datetime import datetime

from db.db import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False, unique=True)
    ru_title = Column(String, index=True, nullable=True, unique=True)

    products = relationship("ProductComposition", back_populates="category")


class ProductComposition(Base):
    """
    Table with composition of each product
    """

    __tablename__ = "product_composition"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False, unique=True)
    ru_title = Column(String, index=True, nullable=True, unique=True)
    creation_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, default=datetime.now)

    calories = Column(Float, default=0, nullable=False)
    proteins = Column(Float, default=0, nullable=False)
    fat = Column(Float, default=0, nullable=False)
    carbohydrates = Column(Float, default=0, nullable=False)

    fdc_id = Column(Integer, nullable=True)

    category_id = Column(
        Integer, ForeignKey(ProductCategory.id, ondelete="CASCADE"), nullable=False
    )

    category = relationship("ProductCategory", back_populates="products")

from datetime import datetime

from pydantic import BaseModel

# ================================================================= ProductCategory |


class ProductCategory(BaseModel):
    title: str


class ProductCategoryShow(ProductCategory):
    id: int


class ProductCategoryCreate(ProductCategory):
    pass


# ================================================================= Product |


class ProductBase(BaseModel):
    title: str
    category_id: int


class ProductShow(ProductBase):
    id: int
    calories: float
    proteins: float
    fat: float
    carbohydrates: float
    category: ProductCategory

    class ConfigDict:
        from_attributes = True


class ProductDetail(ProductShow):
    creation_date: datetime
    update_date: datetime


class ProductCreate(ProductBase):
    calories: float
    proteins: float
    fat: float
    carbohydrates: float


class ProductUpdate(ProductCreate):
    pass

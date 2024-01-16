from db import get_db
from db.models.users import User
from db.repository.products import ProductCategoryRepository
from db.repository.products import ProductsRepository
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.products import ProductCategory
from schemas.products import ProductCategoryCreate
from schemas.products import ProductCategoryShow
from schemas.products import ProductCreate
from schemas.products import ProductDetail
from schemas.products import ProductShow
from sqlalchemy.orm import Session
from utils.dependencies import verify_admin

router = APIRouter()


@router.get("/", response_model=list[ProductShow])
def products_list(session: Session = Depends(get_db)):
    repository = ProductsRepository(session)
    products = repository.select_all_with_categories()
    return products


@router.post("/", response_model=ProductDetail, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, session: Session = Depends(get_db)):
    repository = ProductsRepository(session)
    data = product.model_dump()
    try:
        product = repository.add_record(data=data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating product",
        )
    return product


@router.delete("/")
def delete_product(
    product_id: int,
    session: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin),
):
    repository = ProductsRepository(session)
    repository.delete_record(id=product_id)
    return {"result": f"Product with id = {product_id} was deleted"}


# ====================================================== ProductCategory |


@router.post("/category", response_model=ProductCategoryShow)
def create_product_category(
    category: ProductCategoryCreate,
    session: Session = Depends(get_db),
):
    repository = ProductCategoryRepository(session)
    data = category.model_dump()
    try:
        category = repository.add_record(data=data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating product category",
        )
    return category


@router.get("/category", response_model=list[ProductCategoryShow])
def product_category_list(session: Session = Depends(get_db)):
    repository = ProductCategoryRepository(session)
    product_categories = repository.select_all_records()
    return product_categories

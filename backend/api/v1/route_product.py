from typing import Annotated

from core.pagination import PaginationParams, pagination_params, PaginatedResponse, Paginator
from db import get_db
from db.repository.products import ProductCategoryRepository
from db.repository.products import ProductsRepository
from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.products import ProductCategoryCreate
from schemas.products import ProductCategoryShow
from schemas.products import ProductCreate
from schemas.products import ProductDetail
from schemas.products import ProductShow
from schemas.products import ProductUpdate
from sqlalchemy.orm import Session

router = APIRouter()


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
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating product category",
        )
    return category


@router.get("/category", response_model=PaginatedResponse[ProductCategoryShow])
def product_category_list(
    request: Request,
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    session: Session = Depends(get_db),
):
    repository = ProductCategoryRepository(session)
    paginator = Paginator(
        request=request,
        repository=repository,
        page=pagination.page,
        per_page=pagination.per_page,
        order=pagination.order,
    )
    data = paginator.get_response()
    return data

# ====================================================== Products |

@router.get("/", response_model=PaginatedResponse[ProductShow])
def products_list(
    request: Request,
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    session: Session = Depends(get_db)
):
    """
    Inspired by https://lewoudar.medium.com/fastapi-and-pagination-d27ad52983a
    """
    repository = ProductsRepository(session)
    paginator = Paginator(
        request=request,
        repository=repository,
        page=pagination.page,
        per_page=pagination.per_page,
        order=pagination.order,
    )
    data = paginator.get_response()
    return data


@router.post("/", response_model=ProductShow, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_db),
):
    repository = ProductsRepository(session)
    data = product.model_dump()
    try:
        product = repository.add_record(data=data)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating product",
        )
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_db),
    # TODO ADD ONLY ADMIN CAN DELETE PRODUCT admin_user: User = Depends(verify_admin),
):
    repository = ProductsRepository(session)
    repository.delete_record(id=product_id)
    return {"result": f"Product with id = {product_id} was deleted"}


@router.put("/{product_id}", response_model=ProductShow)
def update_product(
    product_id: int,
    product: ProductUpdate,
    session: Session = Depends(get_db),
):
    data = product.model_dump()
    repository = ProductsRepository(session)
    updated_product = repository.update_product(product_id, data=data)
    return updated_product


@router.get("/{product_id}", response_model=ProductShow)
def detail_product(
    product_id: int,
    session: Session = Depends(get_db)
):
    repository = ProductsRepository(session)
    product = repository.get_record_by_id(record_id=product_id)
    return product

from typing import Annotated
from services.products import crud
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
        order_by="id",
    )
    data = paginator.get_response()
    return data

# ====================================================== Products |

@router.get("/", response_model=PaginatedResponse[ProductShow])
def products_list(
    request: Request,
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    title: str = "",
    session: Session = Depends(get_db)
):
    """
    Inspired by https://lewoudar.medium.com/fastapi-and-pagination-d27ad52983a
    """
    filter_condition = {"title": title}
    repository = ProductsRepository(session)
    paginator = Paginator(
        request=request,
        repository=repository,
        page=pagination.page,
        per_page=pagination.per_page,
        order=pagination.order,
        filter_condition=filter_condition,
        select_method=repository.select_products_by_title,
    )
    data = paginator.get_response()
    return data


@router.post("/", response_model=ProductShow, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    session: Session = Depends(get_db),
):
    repository = ProductsRepository(session)
    try:
        product = await crud.create_product(repository, product)
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
async def update_product(
    product_id: int,
    product: ProductUpdate,
    session: Session = Depends(get_db),
):
    repository = ProductsRepository(session)
    try:
        upd_product = await crud.update_product(repository, product, product_id)
    except Exception as ex:
        raise HTTPException(
            detail=f"Something went wrong while updating product.\n Detail: {ex}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return upd_product


@router.get("/{product_id}", response_model=ProductShow)
def detail_product(
    product_id: int,
    session: Session = Depends(get_db)
):
    repository = ProductsRepository(session)
    product = repository.get_record_by_id(record_id=product_id)
    return product

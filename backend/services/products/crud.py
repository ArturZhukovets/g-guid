from typing import Type

from core.constants import DEFAULT_SRC_LANG, DEFAULT_TGT_LANG
from db.models.products import ProductComposition
from db.repository.products import ProductsRepository
from db.repository.repository import SQLAlchemyRepository
from schemas.products import ProductCreate, ProductUpdate
from services.translation import TranslatorLingvanex

class ProductService:
    def __init__(self, repository):
        self.repository = repository


async def create_product(repository, product: ProductCreate) -> ProductComposition:
    title_eng = product.title
    translation_service = TranslatorLingvanex()
    ru_title = await translation_service.translate_text(
        text=title_eng,
        src_lang=DEFAULT_SRC_LANG,
        tgt_lang=DEFAULT_TGT_LANG,
    )
    data = product.model_dump()
    data['ru_title'] = ru_title
    product = repository.add_record(data=data)
    return product


async def update_product(
        repository: ProductsRepository,
        product_data: ProductUpdate,
        product_id: int
) -> Type[ProductComposition]:
    old_product = repository.get_record_by_id(record_id=product_id)
    if _is_product_changed(old_product, product_data):
        data = product_data.model_dump()
        if product_data.title != old_product.title:
            ru_title = await TranslatorLingvanex().translate_text(
                text=product_data.title,
                src_lang=DEFAULT_SRC_LANG,
                tgt_lang=DEFAULT_TGT_LANG,
            )
            data['ru_title'] = ru_title
        product = repository.update_product(product_id=product_id, data=data)
        return product

    return old_product

def _is_product_changed(old_product, product_data: ProductUpdate) -> bool:
    product_data = product_data.model_dump()
    for field in product_data:
        if product_data[field] != getattr(old_product, field, None):
            return True
    return False


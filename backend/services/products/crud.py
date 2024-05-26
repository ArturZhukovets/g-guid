from db.models.products import ProductComposition
from schemas.products import ProductCreate
from services.translation import TranslatorLingvanex

class ProductService:
    def __init__(self, repository):
        self.repository = repository


async def create_product(repository, product: ProductCreate) -> ProductComposition:
    title_eng = product.title
    translation_service = TranslatorLingvanex()
    title_ru = await translation_service.translate_text_async(
        text=title_eng,
        src_lang="English",
        tgt_lang="Russian"
    )
    data = product.model_dump()
    data['ru_title'] = title_ru
    product = repository.add_record(data=data)
    return product



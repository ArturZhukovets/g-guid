import asyncio
from sqlalchemy.orm import Session
from core.constants import DEFAULT_SRC_LANG, DEFAULT_TGT_LANG
from db import get_db
from db.repository.products import ProductsRepository
from services.translation import TranslatorLingvanex


async def translate_all_product_titles(session: Session) -> None:
    repository = ProductsRepository(session=session)
    filter_by_condition = {"ru_title": None}
    products = repository.select_records(condition=filter_by_condition)
    products_titles = [p.title for p in products]
    print(f"{len(products)} products without translated title found")
    if len(products) == 0:
        return
    titles_to_translate_str: str = "\n".join(products_titles)
    translator = TranslatorLingvanex()
    translated_res = await translator.translate_text(
        text=titles_to_translate_str,
        src_lang=DEFAULT_SRC_LANG,
        tgt_lang=DEFAULT_TGT_LANG,
    )
    translated_titles = translated_res.split("\n")
    if not len(translated_titles) == len(products):
        message = (
            "The number of translated titles is not equal to number of products without `ru_title`.\n"
            "Translated - {len(translated_titles)}\nWithout `ru_title` - {len(products)}"
        )
        raise RuntimeError(message)
    # TODO update in one query
    for product, ru_title in zip(products, translated_titles):
        product.ru_title = ru_title.strip()
    session.commit()
    print(f"{len(translated_titles)} products titles were successfully translated and saved")


if __name__ == '__main__':
    db = get_db()
    session = next(db)
    asyncio.run(translate_all_product_titles(session))

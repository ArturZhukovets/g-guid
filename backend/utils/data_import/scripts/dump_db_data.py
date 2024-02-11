import json

from db.db import get_db
from db.models.products import ProductCategory
from db.models.products import ProductComposition
from sqlalchemy.orm import Session

JSON_DATA_PATH = "/home/gvensye/PycharmProjects/scripts/res4.json"


def load_data_from_json():
    with open(JSON_DATA_PATH) as f:
        return json.load(f)


def create_categories(session: Session, data: list[dict]):
    records = session.query(ProductCategory).all()
    if records:
        deleted = session.query(ProductCategory).delete()
        print(f"Deleted {deleted} records...")
    categories_to_db = []
    categoryes = {element["category"] for element in data}
    print(f"ВСЕГО КАТЕГОРИЙ УНИКАЛЬНЫХ - {len(categoryes)}")
    for category in categoryes:
        categories_to_db.append(ProductCategory(title=category))
    print(categories_to_db)
    session.add_all(categories_to_db)
    session.commit()

    created_records = session.query(ProductCategory).all()
    print(f"Created - {len(created_records)}")
    for category in created_records:
        print(category.title)


def get_categories_table(session: Session):
    res = session.query(ProductCategory.id, ProductCategory.title).all()
    categories_dict = {cat_title: cat_id for cat_id, cat_title in res}
    d = True
    return categories_dict


def records_products_to_db_with_category(session: Session, json_data: list[dict]):
    categories_dict: dict[str, int] = get_categories_table(session)
    products_list = []
    for product in json_data:
        print(product)
        products_list.append(
            ProductComposition(
                title=product["title"],
                calories=product["calories"],
                carbohydrates=product["carbohydrates"],
                proteins=product["proteins"],
                fat=product["fat"],
                fdc_id=product["fdcId"],
                category_id=categories_dict[product["category"]],
            )
        )
    session.add_all(products_list)
    session.commit()


def add_ru_title_to_each_record(session: Session):
    ru_titles = []
    with open("titles_ru.txt", "r") as f:
        for line in f:
            title_ru = line.strip()
            ru_titles.append(title_ru)
    print(ru_titles)
    qs = session.query(ProductComposition).all()
    for product, ru_title in zip(qs, ru_titles):
        print(product.ru_title)
    #     product.ru_title = ru_title
    #     print(ru_title, product.title)
    # session.commit()
    # session.close()
    # titles_en = [title[0] for title in session.query(ProductComposition.title).all()]

    # print(titles_en)


if __name__ == "__main__":
    json_data = load_data_from_json()
    # print(json_data)
    # print(len(json_data))
    session = next(get_db())
    # res = create_categories(session, json_data)
    # print(res)
    # categories_table = get_categories_table(session)
    # records_products_to_db_with_category(session, json_data=json_data)
    add_ru_title_to_each_record(session)

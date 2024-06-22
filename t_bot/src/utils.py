
def product_to_pretty_str(product: dict) -> str:
    _title = product['ru_title']
    _proteins = product['proteins']
    _carbohydrates = product['carbohydrates']
    _fat = product['fat']
    _calories = product['calories']
    _category = product['category']['title']
    text = (
        f"{_title}\n\n"
        f"Состав на 100г продукта:\n"
        f"Белки - {_proteins}\n"
        f"Углеводы - {_carbohydrates}\n"
        f"Жиры - {_fat}\n"
        f"Каллории - {_calories}\n"
        f"Категория продукта - '{_category}'"
    )
    return text

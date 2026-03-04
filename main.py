from dataclasses import asdict
from typing import Iterable
import pandas as pd

from data_classes import WBProduct
from wb_client import WBClient


def get_popular_products(wb: WBClient, query: str = "пальто из натуральной шерсти", page: int = 1):
    return wb.get(
        url="https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search",
        params={
            "ab_testing": "false",
            "appType": "1",
            "curr": "rub",
            "dest": "12358536",
            "hide_vflags": "4294967296",
            "lang": "ru",
            "page": page,
            "query": query,
            "resultset": "catalog",
            "sort": "popular",
            "spp": "30",
            "suppressSpellcheck": "false",
        }
    )


def filter_products(products: list[WBProduct]) -> list[WBProduct]:
    return list(filter(
        lambda product: all(
            (
                product.rating >= 4.5,
                product.price <= 10000,
                product.characteristics.get("Страна производства") == "Россия"),
        ),
        products
    ))


def generate_xlsx(products: Iterable[WBProduct]):
    df = pd.DataFrame([asdict(product.to_output_model()) for product in products])
    df.rename(
        columns={
            "link": "Ссылка на товар",
            "id": "Артикул",
            "name": "Название",
            "price": "Цена",
            "description": "Описание",
            "images": "Изображения",
            "characteristics": "Характеристики",
            "seller_name": "Название селлера",
            "seller_link": "Ссылка на селлера",
            "sizes": "Размеры",
            "total_quantity": "Остаток товара",
            "rating": "Рейтинг",
            "feedbacks": "Количество отзывов",
        }
    ).to_excel("wb_products.xlsx", index=False)


def get_products(wb: WBClient, products: list[dict[str, ...]]) -> list[WBProduct]:
    result = [WBProduct(**product) for product in products]
    for product in result:
        product.additional_data(wb)
    return result


def main():
    wb = WBClient()

    response = get_popular_products(wb)
    data = response.json()
    total = data["total"]  # Общее количество найденных товаров
    pages = total // 100 + int(bool(total % 100))  # Количество страниц товаров
    filtered_products: list[WBProduct] = filter_products(get_products(wb, data["products"]))

    for page in range(2, pages + 1):
        response = get_popular_products(wb, page=page)
        data = response.json()
        filtered_products += filter_products(get_products(wb, data["products"]))

    generate_xlsx(filtered_products)

if __name__ == '__main__':
    main()

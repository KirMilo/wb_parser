from dataclasses import dataclass, asdict

from basket import get_basket
from wb_client import WBClient


@dataclass
class WBSupplier:
    id: int
    name: str
    link: str | None = None

    def __post_init__(self):
        self.link = f"https://www.wildberries.ru/seller/{self.id}"

    def to_dict(self):
        return {
            "seller_name": self.name,
            "seller_link": self.link,
        }

@dataclass
class WBProduct:
    id: int
    name: str
    price: int
    sizes: list[str]  # name
    total_quantity: int  # остаток
    rating: float  # рейтинг
    feedbacks: int  # отзывы
    link: str

    seller: WBSupplier
    description: str | None = None  # Сформировать
    images: list[str] | None = None
    characteristics: dict[str, ...] | None = None

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.price = kwargs.get("sizes")[0].get("price").get("product") // 100
        self.sizes = [size.get("name") for size in kwargs.get("sizes")]
        self.total_quantity = kwargs.get("totalQuantity")
        self.rating = kwargs.get("reviewRating")
        self.feedbacks = kwargs.get("feedbacks")
        self.link = f"https://www.wildberries.ru/catalog/{self.id}/detail.aspx"
        self.seller = WBSupplier(kwargs.get("supplierId"), kwargs.get("supplier"))

    def get_images(self, images_count: int):
        basket = self.get_basket()
        self.images = [basket + f"/images/big/{i}.webp" for i in range(1, images_count + 1)]

    def get_basket(self):
        basket = get_basket(self.id)
        vol = int(self.id // 1e5)
        part = int(self.id // 1e3)
        return f"https://basket-{basket}.wbbasket.ru/vol{vol}/part{part}/{self.id}"

    def additional_data(self, wb_client: WBClient):
        basket = self.get_basket()
        card_url = basket + "/info/ru/card.json"

        if self.price <= 10000 and self.rating >= 4.5:  # Чтобы не делать лишних запросов.
            card = wb_client.get(card_url).json()
            images_count = card.get("media").get("photo_count")
            self.get_images(images_count)

            self.description = card.get("description")
            self.characteristics = {opt["name"]: opt["value"] for opt in card.get("options", {})}
        else:
            self.images = []
            self.description = None
            self.characteristics = {}

    def to_output_model(self) -> "OutputProduct":
        data = {
            **asdict(self),
            **self.seller.to_dict(),
        }
        data.pop("seller")
        return OutputProduct(**data)


@dataclass
class OutputProduct:
    link: str
    id: int
    name: str
    price: int
    description: str
    images: list[str] | str
    characteristics: dict[str, ...] | str
    seller_name: str
    seller_link: str
    sizes: list[str] | str
    total_quantity: int
    rating: float
    feedbacks: int

    def __post_init__(self):
        self.images = ", ".join(self.images)
        self.sizes = ", ".join(self.sizes)
        self.characteristics = "\n".join(
            [f"{name}: {value}" for name, value in self.characteristics.items()]
        )

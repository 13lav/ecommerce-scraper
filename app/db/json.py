import json
from typing import Dict
from app.schemas.product import Product as ProductSchema
from app.core.config import settings


class JsonDb:
    def __init__(self):
        self.saved_products = self._load_products()

    def _load_products(self) -> dict[str, ProductSchema]:
        try:
            with open(settings.PRODUCTS_FILE_PATH, "r") as file:
                products = json.load(file)
                return {product.get('product_title'): ProductSchema(**product) for product in products}
        except FileNotFoundError:
            return {}

    def _save_products(self, products: Dict[str, ProductSchema]) -> None:
        with open(settings.PRODUCTS_FILE_PATH, "w") as file:
            json.dump([product.__dict__ for product in list(products.values())], file)

    def get(self, title: str):
        return self.saved_products[title]

    def save(self, product: ProductSchema):
        self.saved_products[product.product_title] = product
        self._save_products(self.saved_products)

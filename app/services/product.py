import json
from typing import List, Optional, Dict, Any
from app.models.product import Product
from app.schemas.product import Product as ProductSchema
from app.core.config import settings

import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class JsonDb:
    def __init__(self):
        self.saved_products = self._load_products()

    def _load_products(self) -> dict[str, Product]:
        try:
            with open(settings.PRODUCTS_FILE_PATH, "r") as file:
                products = json.load(file)
                return {product.get('product_title'): Product(**product) for product in products}
        except FileNotFoundError:
            return {}

    def _save_products(self, products: Dict[str, Product]) -> None:
        with open(settings.PRODUCTS_FILE_PATH, "w") as file:
            json.dump([product.__dict__ for product in list(products.values())], file)

    def get(self, title: str):
        return self.saved_products[title]

    def save(self, product: Product):
        self.saved_products[product.product_title] = product
        self._save_products(self.saved_products)
        return



class SqlDb:
    def __init__(self):
        self.saved_products = Product.objects.all()


    def save(self, product: Product):
        self.saved_products[product.product_title] = product
        self._save_products(self.saved_products)
        return


class CRUDProduct:
    def get_product_by_title(self, title: str) -> Optional[Product]:
        products = self._load_products()
        return next((product for product in products if product.product_title == title), None)

    def upsert_product(self, product: ProductSchema, crud_obj) -> Product:
        title = product.product_title
        cached_product = redis_client.get(title)
        if cached_product:
            cached_product = json.loads(cached_product)
            if cached_product.get('product_price') != product.product_price:
                redis_client.set(title, json.dumps(product.__dict__), ex=3600*24)
                crud_obj.save(product)
                return product
        else:
            new_product = Product(product_title=title, product_price=product.product_price,
                                  local_image_path=product.local_image_path)
            redis_client.set(title, json.dumps(product.__dict__), ex=3600*24)
            crud_obj.save(product)
            return new_product

    def bulk_create_products(self, products: List[ProductSchema]) -> int:
        crud_obj = JsonDb()
        upsert_count = 0
        for product in products:
            project_obj = self.upsert_product(product, crud_obj)
            if project_obj:
                upsert_count += 1
        return upsert_count


crud_product = CRUDProduct()

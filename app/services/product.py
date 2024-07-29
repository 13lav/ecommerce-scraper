import json
from typing import List
from app.db.cache import redis_client
from app.db.json import JsonDb
from app.schemas.product import Product as ProductSchema


class CRUDProductSchema:
    def upsert_product(self, product: ProductSchema, crud_obj) -> ProductSchema:
        """
        Create or Update a Product
        :param product:
        :param crud_obj:
        :return:
        """
        title = product.product_title
        cached_product = redis_client.get(title)
        if cached_product:
            cached_product = json.loads(cached_product)
            # Check first if present in cache.
            if cached_product.get('product_price') != product.product_price:
                # Save to cache.
                redis_client.set(title, json.dumps(product.__dict__), ex=3600*24)
                # Save to DB.
                crud_obj.save(product)
                return product
        else:
            new_product = ProductSchema(product_title=title, product_price=product.product_price,
                                        local_image_path=product.local_image_path)
            redis_client.set(title, json.dumps(product.__dict__), ex=3600*24)
            crud_obj.save(product)
            return new_product

    def bulk_create_products(self, products: List[ProductSchema]) -> int:
        """
        Bulk Insert Products
        :param products:
        :return:
        """
        crud_obj = JsonDb()
        upsert_count = 0
        for product in products:
            project_obj = self.upsert_product(product, crud_obj)
            if project_obj:
                upsert_count += 1
        return upsert_count


crud_product = CRUDProductSchema()

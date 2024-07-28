from pydantic import BaseModel


class Product(BaseModel):
    product_title: str
    product_price: int
    local_image_path: str

from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    product_title: str
    product_price: Optional[int] = None
    local_image_path: Optional[str] = None

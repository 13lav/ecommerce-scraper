from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_title = Column(String, index=True)
    product_price = Column(Integer, nullable=True)
    local_image_path = Column(String)

from app.models.product import Product


class SqlDb:
    def load(self, product: Product):
        raise NotImplementedError

    def save(self, product: Product):
        raise NotImplementedError

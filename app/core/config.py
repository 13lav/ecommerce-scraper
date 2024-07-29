import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PRODUCTS_FILE_PATH = os.path.join(BASE_DIR, "data", "products.json")
    API_KEY: str = os.getenv("API_KEY")


settings = Settings()

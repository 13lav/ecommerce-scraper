import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print(os.getenv("API_KEY"))
class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    USERS_FILE_PATH = os.path.join(BASE_DIR, "data", "users.json")
    PRODUCTS_FILE_PATH = os.path.join(BASE_DIR, "data", "products.json")
    API_KEY: str = os.getenv("API_KEY")  # Retrieve the API_KEY from environment variables


settings = Settings()

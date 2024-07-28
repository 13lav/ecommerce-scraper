from fastapi import APIRouter, HTTPException
from app import services
from app.common.logger import logger

router = APIRouter()


@router.post("/scrape/")
def scrape_products(pages: int = 1, proxy: str = None):
    try:
        scrapper_instance = services.Scraper(pages, proxy)
        data = scrapper_instance.get_scarped_data()
        product_count = services.crud_product.bulk_create_products(data)
        notification_text = scrapper_instance.notify(product_count)
        return {"message": notification_text}
    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong.")

from fastapi import APIRouter, HTTPException, Request
from app import services
from app.common.logger import logger

router = APIRouter()


@router.post("/scrape/")
async def scrape_products(request: Request):
    try:
        json_body = await request.json()
        scrapper_instance = services.Scraper(pages=json_body.get('pages'), proxy=json_body.get('proxy'))
        data = scrapper_instance.get_scarped_data()
        product_count = services.crud_product.bulk_create_products(data)
        notification_text = scrapper_instance.notify(product_count)
        return {"message": notification_text}
    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong.")

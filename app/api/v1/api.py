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

@router.post("/scrape-reports/")
async def scrape_reports(request: Request):
    try:
        json_body = await request.json()
        scrapper_instance = services.Scraper(pages=json_body.get('pages'), proxy=json_body.get('proxy'))
        industry_urls = scrapper_instance.get_industry_urls()
        industry_urls = list(set(industry_urls))
        report_urls = await scrapper_instance.get_report_urls(industry_urls[:1])
        unique_report_urls = list(set(report_urls))
        scraped_data = await scrapper_instance.get_report_data(unique_report_urls[:2])
        # product_count = services.crud_product.bulk_create_products(data)
        return {"industry_urls_count": len(industry_urls), "report_urls_count": len(unique_report_urls), "report_urls": unique_report_urls, "scraped_data": scraped_data}
    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong.")

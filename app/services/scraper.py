from typing import List
import requests
import bs4
import time
from app import schemas
from app.common.logger import logger
from app.common.utils import download_image


class Scraper:
    def __init__(self, pages: int = 1, proxy: str = None):
        self.pages = pages
        self.proxy = proxy
        self.base_url = "https://dentalstall.com/shop/"
        self.retry_interval = 3  # time in seconds
        self.retry_attempts = 2

    def _generate_page_url(self, page_number) -> str:
        url = self.base_url
        if page_number > 1:
            url += f"page/{page_number}/"
        return url

    def fetch_page(self, url: str) -> bs4.BeautifulSoup:
        page = requests.get(url, proxies={"http": self.proxy, "https": self.proxy})
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        return soup

    def _get_page_content(self, url: str) -> bs4.BeautifulSoup:
        for i in range(self.retry_attempts):
            soup = None
            try:
                response = requests.get(url)
                soup = bs4.BeautifulSoup(response.content, 'html.parser')
                response.raise_for_status()  # Check if the request was successful
                logger.info(f"Page Fetched in Attempt {i + 1}.")
                return soup
            except requests.RequestException as e:
                logger.warning(f"Attempt {i + 1} failed: {e}")
                if i < self.retry_attempts - 1:
                    time.sleep(self.retry_interval)
                else:
                    logger.error(f"Failed to fetch page after several attempts.")
                    return soup

    def get_scarped_data(self) -> List[object]:
        products_info = []
        for page_number in range(119, 121):
            url = self._generate_page_url(page_number)
            logger.info(f"Fetching Page No. {page_number}.")
            page = self._get_page_content(url)
            raw_products = page.find_all(class_="product-inner")
            for product in raw_products:
                title = product.find('h2', class_='woo-loop-product__title').get_text(strip=True)
                price_div = product.find('ins')
                if not price_div:
                    price_div = product.find('bdi')
                if price_div:
                    price = float(price_div.get_text(strip=True).replace('₹', ''))
                else:
                    price = None
                image_url = product.find('img').get('data-lazy-src', product.find('img')['src'])

                logger.info(f'Title: {title}')
                print(f'Price: {price}')
                print(f'image_url: {image_url}')
                print('-' * 128)

                product_obj = schemas.Product(
                    product_title=title,
                    product_price=price,
                    local_image_path=download_image(image_url)
                )
                products_info.append(product_obj)
        return products_info

    def notify(self, count):
        notification_text = f"Scraping Completed: Added/Updated {count} Products Successfully."
        logger.info(notification_text)
        return notification_text



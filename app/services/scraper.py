from typing import List
import requests
import bs4
import time
from app import schemas
from app.common.logger import logger
from app.common.utils import download_image
from fastapi import HTTPException
import httpx


class Scraper:
    def __init__(self, pages: int = 1000, proxy: str = None):
        """
        Scraper Constructor
        :param pages:
        :param proxy:
        """
        self.pages = pages
        self.proxy = proxy
        self.base_url = "https://www.skyquestt.com/"
        self.retry_interval = 1  # time in seconds
        self.retry_attempts = 2

    def _generate_page_url(self, page_number) -> str:
        """
        Generate URL for specific page_number
        :param page_number:
        :return:
        """
        url = self.base_url
        if page_number > 1:
            url += f"page/{page_number}/"
        return url

    def _generate_reports_list_page_url(self, industry_url, page_number) -> str:
        """
        Generate URL for specific page_number
        :param page_number:
        :return:
        """
        url = industry_url
        url += f"?page={page_number}"
        return url

    def _get_page_content(self, url: str) -> bs4.BeautifulSoup:
        """
        Get Web Content Using BeautifulSoup
        With Added Retry Feature.
        :param url:
        :return:
        """
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
        """
        Fetch, Parse and Scraped the Desired
        :return:
        """
        products_info = []
        for page_number in range(1, self.pages + 1):
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

                # logger.info(f'Title: {title}')
                # print(f'Price: {price}')
                # print(f'Image_url: {image_url}')
                # print('-' * 128)

                product_obj = schemas.Product(
                    product_title=title,
                    product_price=price,
                    local_image_path=download_image(image_url)
                )
                products_info.append(product_obj)
        return products_info

    def notify(self, count):
        """
        Generate Notification Text
        :param count:
        :return:
        """
        notification_text = f"Scraping Completed: Added/Updated {count} Products Successfully."
        logger.info(notification_text)
        return notification_text




    def get_industry_urls(self):
        """
        Fetch, Parse and Scraped the Desired
        :return:
        """
        page = self._get_page_content(self.base_url)
        # Define the prefix to filter URLs
        prefix = 'https://www.skyquestt.com/industries'

        # Extract all href attributes from <a> tags with the given prefix
        urls = [a['href'] for a in page.find_all('a', href=True) if a['href'].startswith(prefix)]

        print(urls)
        return urls


    async def get_report_urls(self, urls):
        """
        Fetch, Parse and Scraped the Desired
        :return:
        """
        report_urls = []
        for industry_url in urls:
            for page_number in range(1, self.pages + 1):
                url = self._generate_reports_list_page_url(industry_url, page_number)
                logger.info(f"Fetching '{url}' Page No. {page_number}.")
                soup_input = await self._fetch_page_data(url)
                page = bs4.BeautifulSoup(soup_input, 'html.parser')
                prefix = 'https://www.skyquestt.com/report'

                # Extract all href attributes from <a> tags with the given prefix
                urls = [a['href'] for a in page.find_all('a', href=True) if a['href'].startswith(prefix)]
                # print(urls)
                print(page_number, " ----- >  ", "reports found -> ", len(urls), urls)
                report_urls.extend(urls)
            print(" total reports found -> ", len(report_urls))

        return report_urls




    async def get_report_data(self, report_urls) -> List[object]:
        """
        Fetch, Parse and Scraped the Desired
        :return:
        """
        scraped_data = []
        for url in report_urls:
            data_obj = {

            }
            logger.info(f" ========== Fetching '{url}' ======== ")
            soup_input = await self._fetch_page_data(url)
            page = bs4.BeautifulSoup(soup_input, 'html.parser')
            headings = page.find_all(class_="report-title")
            market_name = headings[0].get_text(strip=True).replace("Insights", "")
            data_obj['market_name'] = market_name
            for heading in headings:
                heading_text = heading.get_text(strip=True).replace(market_name, "")
                print(market_name, "heading -----> ", heading, heading_text)

                # Find the next div after the h1 tag
                next_div = heading.find_next_sibling('div')

                # Get the content of the next div
                if next_div:
                    print(next_div.get_text(strip=True))
                    data_obj[heading_text] = next_div.get_text(strip=True)
                else:
                    print("No next div found.")

            scraped_data.append(data_obj)
        return scraped_data




    async def _fetch_page_data(self, url: str):
        # Headers as specified in the curl command
        HEADERS = {
            "Accept": "*/*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://www.skyquestt.com/industries/precious-metals-minerals",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"'
        }
        try:
            # Make a GET request with the specified headers
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=HEADERS)

            # Return the response content
            return response.text
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {e}")

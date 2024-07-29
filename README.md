Ecommerce Scraper Using FastAPI

Features:

- Scrape the product name, price, and image from each page of the catalogue. 
- Different settings provided as input:
  - The first one will limit the number of pages from which we need to scrape the information (for example, 5 means that we want to scrape only products from the first 5 pages).
  - The second one will provide a proxy string that tool can use for scraping.

- Store the scraped information in a database, for now a JSON file in the following format:
    [
      {
        "product_title":"",
        "product_price":0,
        "path_to_image":"", # path to image at your PC
      }
    ]

- At the end of the scraping cycle, it notifies stating how many products were scraped and updated in DB during the current session.

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

- Ensures type validation and data integrity using appropriate methods.

- Have a simple retry mechanism for the scraping part. If a page cannot be reached because of a destination site server error.

- Contains simple authentication to the endpoint using a static token.

- Users Redis to cache results. If the scraped product price has not changed, we do not update the data of such a product in the DB.



Requirements

- python 3.7+
- fastapi
- uvicorn
- pydantic
- sqlalchemy
- requests
- beautifulsoup4
- redis
- python-dotenv
- colorama




Installation

- Clone the repository:

    git clone https://github.com/13lav/ecommerce-scraper
    cd ecommerce-scraper

- Create and activate a virtual environment:

    python3 -m venv env
    source env/bin/activate 

- Install the required packages:

    pip install -r requirements.txt


Usage

- Run FastAPI server:

    uvicorn app.main:app --reload

Scrape products:

  Make a below curl request to the /scrape endpoint with body parameters pages and proxy:

  curl --location 'http://127.0.0.1:8000/api/v1/scrape/' \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'access-token: <token>' \
  --data-raw '{
    "pages": 2,
    "proxy": "http://user:pass@123.45.67.89:8080"
  }'

Authentication:

  Add .env file in root directory.

   API_KEY=<token>


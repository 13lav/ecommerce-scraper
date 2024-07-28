from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    pages: int
    proxy: str

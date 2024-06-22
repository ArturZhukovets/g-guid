from urllib.parse import urljoin

import aiohttp
from pydantic import BaseModel

from config import settings

async def get_async_http_session():
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


class QueryParams(BaseModel):
    title: str
    page: int = 1
    per_page: int = 50
    order: str = "desc"


class ProductCompositionAPIService():
    def __init__(self):
        self.products_url = settings.products_url

    async def find_products(self, product_title: str):
        async with aiohttp.ClientSession() as session:
            query_params = QueryParams(title=product_title)
            async with session.get(self.products_url, params=query_params.model_dump()) as response:
                return await response.json()


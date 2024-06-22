import json
from typing import Any

from pymemcache.client import base, RetryingClient


class _JsonSerde(object):
    def serialize(self, key: str, value: str | dict) -> tuple[str, int]:
        if isinstance(value, str):
            return value, 1
        return json.dumps(value), 2

    def deserialize(self, key: str, value: str, flags) -> Any:
        if flags == 1:
            return value
        if flags == 2:
            return json.loads(value)
        raise Exception("Unknown serialization format")


class MemCacher:

    def __init__(self):
        self._base_memcache_client = base.Client(
            server=('0.0.0.0', 11211),
            no_delay=True,
            timeout=2,
            serde=_JsonSerde(),
        )
        self._client = RetryingClient(
            self._base_memcache_client,
            attempts=3,
            retry_delay=0.1,
        )

    def set_products_data(self, chat_id: int, data: list[dict]) -> None:
        self._client.set(str(chat_id), data, expire=3_600)

    def get_product(self, chat_id: int, product_id: int) -> dict | None:
        products = self._client.get(str(chat_id))
        if products:
            for product in products:
                if product['id'] == product_id:
                    return product

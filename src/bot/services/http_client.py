import httpx
from typing import Dict, Any

from config import settings

class HttpClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get(self, endpoint: str, params: dict = None) -> Dict[str, Any]:
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data: dict) -> Dict[str, Any]:
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def put(self, endpoint: str, data: dict) -> Dict[str, Any]:
        response = await self.client.put(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return response.json()

    async def close(self):
        """Закриває клієнта."""
        await self.client.aclose()

http_client = HttpClient(settings.API_URL)

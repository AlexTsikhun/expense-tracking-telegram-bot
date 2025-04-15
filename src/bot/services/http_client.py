from typing import Any

import httpx

from config import settings


class HttpClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=settings.API_URL)

    async def get(self, endpoint: str, params: dict = None) -> dict[str, Any]:
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data: dict) -> dict[str, Any]:
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def put(self, endpoint: str, data: dict) -> dict[str, Any]:
        response = await self.client.put(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def delete(self, endpoint: str) -> dict[str, Any]:
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

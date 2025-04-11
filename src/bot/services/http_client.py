from typing import Any

import httpx


class HttpClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

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

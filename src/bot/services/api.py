from typing import Any


class APIService:
    def __init__(self, http_client):
        self.http_client = http_client

    async def get_expenses(self, start_date: str = None, end_date: str = None) -> list[dict[str, Any]]:
        params = {}
        if start_date and end_date:
            params = {"start_date": start_date, "end_date": end_date}
        return await self.http_client.get("/expenses/", params=params)

    async def create_expense(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self.http_client.post("/expenses/", data=data)

    async def delete_expense(self, expense_id: int) -> dict[str, Any]:
        return await self.http_client.delete(f"/expenses/{expense_id}")

    async def update_expense(self, expense_id: int, data: dict[str, Any]) -> dict[str, Any]:
        return await self.http_client.put(f"/expenses/{expense_id}", data=data)

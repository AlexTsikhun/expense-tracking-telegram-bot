import os
from typing import Any

import pandas as pd


class FileService:
    @staticmethod
    def generate_excel_file(data: list[dict[str, Any]], filename: str = "report.xlsx") -> str:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        return filename

    @staticmethod
    def get_total_amount(data: list[dict[str, Any]]) -> float:
        return sum(expense["amount_uah"] for expense in data)

    @staticmethod
    def cleanup_file(filename: str) -> None:
        if os.path.exists(filename):
            os.remove(filename)

import httpx
from bs4 import BeautifulSoup


class CurrencyService:
    @staticmethod
    def get_usd_rate() -> float:
        response = httpx.get("https://minfin.com.ua/currency/")
        soup = BeautifulSoup(response.text, "html.parser")
        rate = float(float(soup.find("div", class_="sc-1x32wa2-9 bKmKjX").text.split(".")[0].replace(",", ".")))
        return rate

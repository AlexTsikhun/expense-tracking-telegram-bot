import httpx
from bs4 import BeautifulSoup


class CurrencyService:
    @staticmethod
    def get_usd_rate() -> float:
        response = httpx.get("https://minfin.com.ua/currency/")
        soup = BeautifulSoup(response.text, "html.parser")
        rate_element = soup.find("div", class_="sc-1x32wa2-9 bKmKjX")
        if not rate_element:
            raise ValueError("Rate element not found on the page")
        
        rate_text = list(rate_element.stripped_strings)[0]
        rate = float(rate_text.replace(",", "."))
        
        return rate

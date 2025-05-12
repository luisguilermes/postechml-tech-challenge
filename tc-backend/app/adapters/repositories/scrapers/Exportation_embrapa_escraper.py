from typing import List
from bs4 import BeautifulSoup
from app.adapters.repositories.scrapers.embrapa_base_scraper import EmbrapaBaseScraper, BASE_URL
from app.domain.entities.product import Product
from app.domain.repositories.base_repository import BaseRepository

class ProcessingEmbrapaScraper(EmbrapaBaseScraper, BaseRepository):
    def __init__(self, suboption: int = 1):
        self.suboption = suboption

    def fetch_all(self, year: int) -> List[Product]:
        url = f"{BASE_URL}?ano={year}&opcao=opt_06&subopcao=subopt_0{self.suboption}"
        response = self._fetch_page(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = self._find_table(soup)
        return self._parse_table(table, year)
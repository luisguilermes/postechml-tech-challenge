from typing import List
from bs4 import BeautifulSoup

from app.adapters.scrapers.base_embrapa_scraper import (
    _fetch_page,
    _find_table,
    _parse_table,
)
from app.models.product import Product


def fetch_production_embrapa(year: int) -> List[Product]:
    url = f"ano={year}&opcao=opt_02"
    response = _fetch_page(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = _find_table(soup)
    return _parse_table(table, year)

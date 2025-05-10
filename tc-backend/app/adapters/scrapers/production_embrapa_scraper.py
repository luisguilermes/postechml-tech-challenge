import logging
from typing import List
from bs4 import BeautifulSoup

from app.adapters.scrapers.embrapa_base_scraper import (
    BASE_URL,
    _fetch_page,
    _find_table,
    _parse_table,
)
from app.domain.production import Production

logger = logging.getLogger(__name__)


def fetch_production_embrapa(year: int) -> List[Production]:
    url = f"{BASE_URL}?ano={year}&opcao=opt_02"
    response = _fetch_page(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = _find_table(soup)
    return _parse_table(table, year)

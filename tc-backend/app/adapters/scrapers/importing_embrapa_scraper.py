from datetime import datetime, timezone
from typing import List

from bs4 import BeautifulSoup

from app.adapters.scrapers.base_embrapa_scraper import _fetch_page, SOURCE
from app.models.category import Category


def fetch_all_categories() -> List[Category]:
    """
    Busca todas as categorias de importação da Embrapa.
    """
    url = "opcao=opt_05"
    response = _fetch_page(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return _fetch_categories(soup)


def _fetch_categories(bs: BeautifulSoup) -> List[Category]:
    all_data = []
    buttons = bs.findAll("button", attrs={"class": "btn_sopt"})
    if buttons:
        collected_at = datetime.now(timezone.utc)
        for button in buttons:
            category_id = button.get("value")
            all_data.append(
                Category(
                    id=category_id,
                    name=button.next.strip(),
                    source=SOURCE,
                    collected_at=collected_at,
                )
            )
    return all_data

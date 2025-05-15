from typing import List
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests

from app.core.config import settings
from app.models.product import Product

TABLE_CLASS = "tb_base tb_dados"
DEFAULT_UNIT = "liters"
SOURCE = "Embrapa/Vitivinicultura"


def _create_production_entry(
    category: str,
    sub_category: str,
    amount: float,
    year: int,
    collected_at: datetime,
) -> Product:
    return Product(
        amount=amount,
        unit=DEFAULT_UNIT,
        year=year,
        category=category.title(),
        sub_category=sub_category.title(),
        source=SOURCE,
        collected_at=collected_at,
    )


def _parse_amount(amount: str) -> float:
    try:
        return (
            float(amount.replace(".", "").replace(",", "."))
            if amount not in ["-", ""]
            else 0.0
        )
    except ValueError:
        return 0.0


def _fetch_page(path: str) -> requests.Response:
    try:
        timeout = (settings.embrapa_connection_timeout, settings.embrapa_read_timeout)
        response = requests.get(f"{settings.embrapa_url}?{path}", timeout=timeout)
        response.encoding = "utf-8"
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from Embrapa: {e}") from e


def _parse_table(table: BeautifulSoup, year: int) -> List[Product]:
    data = []
    collected_at = datetime.now(timezone.utc)
    current_category = None

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if not cols:
            continue

        td = cols[0]
        if "tb_item" in td.get("class", []):
            current_category = td.text.strip()
        elif "tb_subitem" in td.get("class", []):
            sub_category = td.text.strip()
            amount = _parse_amount(cols[1].text.strip())
            data.append(
                _create_production_entry(
                    category=current_category,
                    sub_category=sub_category,
                    amount=amount,
                    year=year,
                    collected_at=collected_at,
                )
            )

    return data


def _find_table(soup: BeautifulSoup) -> BeautifulSoup:
    table = soup.find("table", {"class": TABLE_CLASS})
    if not table:
        raise ValueError("Data table not found in the page.")
    return table

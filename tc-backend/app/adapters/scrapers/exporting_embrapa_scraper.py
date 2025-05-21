from datetime import datetime, timezone
from typing import List

from bs4 import BeautifulSoup

from app.adapters.scrapers.base_embrapa_scraper import _fetch_page, SOURCE
from app.models.category import Category
from app.models.exporting import Exporting

AMOUNT_UNIT = "Kg"
VALUE_UNIT = "US$"


def fetch_all_categories_embrapa() -> List[Category]:
    """
    Busca todas as categorias de exportação da Embrapa.
    """
    url = "opcao=opt_06"
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


def fetch_exports_by_category_from_embrapa(
    year: int, category_id: str
) -> List[Exporting]:
    """
    Busca todos os dados de exportação da Embrapa no intervalo de anos especificado.
    """
    all_data = []
    url = f"opcao=opt_06&subopcao={category_id}"
    response = _fetch_page(url)
    soup = BeautifulSoup(response.text, "html.parser")
    category_name = next(
        map(
            lambda c: c.name,
            filter(lambda c: c.id == category_id, _fetch_categories(soup)),
        ),
        None,
    )
    if category_name is None:
        raise ValueError(f"Categoria com id '{category_id}' não encontrada")
    table = soup.find("tbody")
    if table:
        all_data.extend(_parse_table(table, year, category_name))

    return all_data


def _parse_table(
    tbody: BeautifulSoup, year: int, category_data: str
) -> List[Exporting]:
    """
    Faz o parsing da tabela de importações.
    """
    strings = list(tbody.stripped_strings)
    grouped_data = [strings[i : i + 3] for i in range(0, len(strings), 3)]

    data = []
    collected_at = datetime.now(timezone.utc)

    for group in grouped_data:
        if len(group) < 3:
            continue

        country, quantity, dollar = group
        if country == "Total":
            continue
        data.append(
            Exporting(
                category=category_data,
                country=country,
                amount=_parse_number(quantity),
                amount_unit=AMOUNT_UNIT,
                value=_parse_number(dollar),
                value_unit=VALUE_UNIT,
                source=SOURCE,
                collected_at=collected_at,
                year=year,
            )
        )
    return data


def _parse_number(value: str) -> float:
    """
    Converte o valor em string para float.
    """
    try:
        return (
            float(value.replace(".", "").replace(",", "."))
            if value not in ["-", ""]
            else 0.0
        )
    except ValueError:
        return 0.0

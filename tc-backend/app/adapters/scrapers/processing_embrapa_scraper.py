from datetime import datetime, timezone
from typing import List

from bs4 import BeautifulSoup

from app.adapters.scrapers.base_embrapa_scraper import _fetch_page, SOURCE
from app.models.category import Category
from app.models.processing import Processing

AMOUNT_UNIT = "Kg"


def fetch_all_categories_embrapa() -> List[Category]:
    """
    Busca todas as categorias de processamento da Embrapa.
    """
    url = "opcao=opt_03"
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


def fetch_process_by_category_from_embrapa(
    year: int, category_id: str
) -> List[Processing]:
    """
    Busca todos os dados de processamento da Embrapa no intervalo de anos especificado.
    """
    all_data = []
    url = f"opcao=opt_03&subopcao={category_id}"
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
) -> List[Processing]:
    """
    Faz o parsing da tabela de Processamento.
    """
    strings = list(tbody.stripped_strings)
    grouped_data = [strings[i : i + 2] for i in range(0, len(strings), 2)]

    data = []
    collected_at = datetime.now(timezone.utc)
    grow = None
    for group in grouped_data:
        if len(group) < 2:
            continue

        sub_grow, amount = group

        if sub_grow.isupper():
            grow = sub_grow
            continue
        if grow == "Total":
            continue
        data.append(
            Processing(
                category=category_data,
                grow=grow,
                sub_grow=sub_grow,
                amount=_parse_number(amount),
                amount_unit=AMOUNT_UNIT,
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

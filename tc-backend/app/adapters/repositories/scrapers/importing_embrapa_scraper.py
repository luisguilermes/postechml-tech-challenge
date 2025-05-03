from typing import List
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests
from app.domain.entities.importing import Importing
from app.domain.entities.category import Category
from app.domain.repositories.importing_repository import ImportingRepository

# Constantes
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"
AMOUNT_UNIT = "Kg"
VALUE_UNIT = "US$"
SOURCE = "Embrapa/Vitivinicultura"
TABLE_CLASS = "tb_base"

class ImportingEmbrapaScraper(ImportingRepository):
    def fetch_all_categories(self) -> List[Category]:
        """
        Busca todas as categorias de importação da Embrapa.
        """
        url = f"{BASE_URL}?opcao=opt_05"
        response = self._fetch_page(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return self._fetch_categories(soup)

    def fetch_imports_by_category(self, start_year: int, end_year: int, category: str) \
            -> List[Importing]:
        """
        Busca todos os dados de importação da Embrapa no intervalo de anos especificado.
        """
        all_data = []
        for year in range(start_year, end_year + 1):
            url = f"{BASE_URL}?ano={year}&opcao=opt_05&subopcao={category}"
            response = self._fetch_page(url)
            soup = BeautifulSoup(response.text, "html.parser")
            category_name = next(
                map(lambda c: c.name, filter(
                    lambda c: c.id == category, self._fetch_categories(soup))
                ),
                None
            )
            if category_name is None:
                raise ValueError("Categoria com id 'id_desejado' não encontrada")
            table = soup.find("tbody")
            if table:
                all_data.extend(self._parse_table(table, year, category_name))
        return all_data

    def _fetch_categories(self, bs: BeautifulSoup) -> List[Category]:
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
                        collected_at=collected_at
                    )
                )
        return all_data

    def _fetch_page(self, url: str) -> requests.Response:
        """
        Faz o request da página HTML.
        """
        try:
            response = requests.get(url, timeout=10)
            response.encoding = "utf-8"
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erro ao buscar dados da Embrapa: {e}") from e

    def _parse_table(self, tbody: BeautifulSoup, year: int, category_data: str) -> List[Importing]:
        """
        Faz o parsing da tabela de importações.
        """
        strings = list(tbody.stripped_strings)
        grouped_data = [strings[i:i + 3] for i in range(0, len(strings), 3)]

        data = []
        collected_at = datetime.now(timezone.utc)

        for group in grouped_data:
            if len(group) < 3:
                continue

            country, quantity, dollar = group
            if country == "Total":
                continue
            data.append(
                Importing(
                    category=category_data,
                    country=country,
                    amount=self._parse_number(quantity),
                    amount_unit=AMOUNT_UNIT,
                    value=self._parse_number(dollar),
                    value_unit=VALUE_UNIT,
                    source=SOURCE,
                    collected_at=collected_at,
                    year=year
                )
            )
        return data

    def _parse_number(self, value: str) -> float:
        """
        Converte o valor em string para float.
        """
        try:
            return float(
                value.replace(".", "").replace(",", ".")
            ) if value not in ["-", ""] else 0.0
        except ValueError:
            return 0.0

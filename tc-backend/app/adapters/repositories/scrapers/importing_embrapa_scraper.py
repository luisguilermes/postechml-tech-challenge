from typing import List, Dict
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests
import re
from app.domain.entities.product import Product
from app.domain.repositories.importing_repository import ImportingRepository
from app.util.hash_generator_util import generate_hash

# Constantes
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"
DEFAULT_UNIT = "liters"
SOURCE = "Embrapa/Vitivinicultura"
TABLE_CLASS = "tb_base"
OPT = 1


class ImportingEmbrapaScraper(ImportingRepository):
    def fetch_all(self, start_year: int = 1970, end_year: int = 2024) -> List[Product]:
        """
        Busca todos os dados de importação da Embrapa no intervalo de anos especificado.
        """
        all_data = []
        for year in range(start_year, end_year + 1):
            url = f"{BASE_URL}?ano={year}&opcao=opt_05&subopcao=subopt_0{OPT}"
            response = self._fetch_page(url)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("tbody")
            if table:
                all_data.extend(self._parse_table(table, year))
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

    def _parse_table(self, tbody: BeautifulSoup, year: int) -> List[Dict]:
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
            data.append(
                self._create_import_entry(
                    country=country,
                    quantity=quantity,
                    dollar=dollar,
                    year=year,
                    collected_at=collected_at,
                )
            )
        return data

    def _create_import_entry(
        self,
        country: str,
        quantity: str,
        dollar: str,
        year: int,
        collected_at: datetime,
    ) -> Dict:
        """
        Cria o dicionário de importação.
        """
        return {
            "id": generate_hash([country, str(year)]),
            "country": country,
            "quantity": self._parse_amount(quantity),
            "dollar": self._parse_amount(dollar),
            "unit": DEFAULT_UNIT,
            "year": year,
            "source": SOURCE,
            "collected_at": collected_at,
        }

    def _parse_amount(self, value: str) -> float:
        """
        Converte o valor em string para float.
        """
        try:
            return float(value.replace(".", "").replace(",", ".")) if value not in ["-", ""] else 0.0
        except ValueError:
            return 0.0

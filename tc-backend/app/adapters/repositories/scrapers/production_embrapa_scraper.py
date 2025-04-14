from typing import List, Dict
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests
from app.domain.entities.product import Product
from app.domain.repositories.production_repository import ProductionRepository
from app.util.hash_generator_util import generate_hash

# Constants
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"
TABLE_CLASS = "tb_base tb_dados"
DEFAULT_UNIT = "liters"
SOURCE = "Embrapa/Vitivinicultura"


class ProductionEmbrapaScraper(ProductionRepository):
    def fetch_all(self, year: int) -> List[Product]:
        """
        Fetch all production data for a given year.
        """
        url = f"{BASE_URL}?ano={year}&opcao=opt_02"
        response = self._fetch_page(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = self._find_table(soup)

        return self._parse_table(table, year)

    def _fetch_page(self, url: str) -> requests.Response:
        """
        Fetch the page content from the given URL.
        """
        try:
            response = requests.get(url, timeout=10)
            response.encoding = "utf-8"
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch data from Embrapa: {e}") from e

    def _find_table(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Find the main data table in the HTML content.
        """
        table = soup.find("table", {"class": TABLE_CLASS})
        if not table:
            raise ValueError("Data table not found in the page.")
        return table

    def _parse_table(self, table: BeautifulSoup, year: int) -> List[Dict]:
        """
        Parse the data table and extract production data.
        """
        data = []
        category = None
        collected_at = datetime.now(timezone.utc)

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue

            td = cols[0]
            if "tb_item" in td.get("class", []):
                category = td.text.strip()
            elif "tb_subitem" in td.get("class", []):
                sub_category = td.text.strip()
                amount = self._parse_amount(cols[1].text.strip())
                data.append(
                    self._create_product_entry(
                        category=category,
                        sub_category=sub_category,
                        amount=amount,
                        year=year,
                        collected_at=collected_at,
                    )
                )

        return data

    def _create_product_entry(
        self,
        category: str,
        sub_category: str,
        amount: float,
        year: int,
        collected_at: datetime,
    ) -> Dict:
        """
        Create a dictionary entry for a product.
        """
        return {
            "id": generate_hash([category, sub_category]),
            "amount": amount,
            "unit": DEFAULT_UNIT,
            "year": year,
            "category": category.title(),
            "sub_category": sub_category.title(),
            "source": SOURCE,
            "collected_at": collected_at,
        }

    def _parse_amount(self, amount: str) -> float:
        """
        Parse the amount string and convert it to a float.
        """
        try:
            return (
                float(amount.replace(".", "").replace(",", "."))
                if amount not in ["-", ""]
                else 0.0
            )
        except ValueError:
            return 0.0

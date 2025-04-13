from typing import List
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests
from app.domain.entities.product import Product
from app.domain.repositories.production_repository import ProductionRepository
from app.util.hash_generator_util import generate_hash


class ProductionEmbrapaScraper(ProductionRepository):
    def fetch_all(self, year: int) -> List[Product]:
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"  # a página usa encoding brasileiro

        if response.status_code != 200:
            raise requests.exceptions.RequestException(
                "Erro ao acessar a página da Embrapa"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar a tabela principal
        table = soup.find(
            "table", {"class": "tb_base tb_dados"}
        )  # as tabelas têm essa classe

        data = []

        category = None
        collected_at = datetime.now(timezone.utc)
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue  # pula se não houver colunas

            td = cols[0]
            if "tb_item" in td.get("class", []):
                category = td.text.strip()
            elif "tb_subitem" in td.get("class", []):
                # Subcategoria e quantidade por ano
                sub_category = td.text.strip()
                amount = cols[1].text.strip()
                data.append(
                    {
                        "id": generate_hash([category, sub_category]),
                        "amount": self._parse_amount(amount),
                        "unit": "liters",
                        "year": year,
                        "category": category.title(),
                        "sub_category": sub_category.title(),
                        "source": "Embrapa/Vitivinicultura",
                        "collected_at": collected_at,
                    }
                )
        return data

    def _parse_amount(self, amount: str) -> float:
        """
        Parse the amount string and convert it to a float.
        """
        # Verificar se a string é um número válido
        if amount != "-" and amount != "":
            amount = float(amount.replace(".", ""))
        else:
            amount = 0.0  # Ou None, dependendo do seu caso
        return amount

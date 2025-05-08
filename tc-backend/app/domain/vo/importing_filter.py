from typing import List
from app.domain.entities.importing import Importing

class ImportingFilter:
    def __init__(self, country=None):
        self.country = country

    def apply(self, imports: List[Importing]) -> List[Importing]:
        """
        Aplica os filtros na lista de importações.
        """
        filtered_products = imports

        if self.country:
            filtered_products = [
                p
                for p in filtered_products
                if p.country.lower() == self.country.lower()
            ]
        return filtered_products

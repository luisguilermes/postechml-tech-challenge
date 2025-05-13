from typing import List
from app.domain.entities.exportation import Exportation

class ExportationFilter:
    def __init__(self, country=None):
        self.country = country

    def apply(self, exportations: List[Exportation]) -> List[Exportation]:
        """
        Aplica os filtros na lista de importações.
        """
        filtered_products = exportations

        if self.country:
            filtered_products = [
                p
                for p in filtered_products
                if p.country.lower() == self.country.lower()
            ]
        return filtered_products

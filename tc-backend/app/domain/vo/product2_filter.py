class Filter:
    def __init__(self, country=None):
        self.country = country

    def apply(self, products):
        """
        Aplica os filtros na lista de produtos.
        """
        filtered_products = products

        if self.country:
            filtered_products = [
                p
                for p in filtered_products
                if p["country"].lower() == self.country.lower()
            ]
        return filtered_products

class Filter:
    def __init__(self, category=None):
        self.category = category

    def apply(self, products):
        """
        Aplica os filtros na lista de produtos.
        """
        filtered_products = products

        if self.category:
            filtered_products = [
                p
                for p in filtered_products
                if p["category"].lower() == self.category.lower()
            ]
        return filtered_products

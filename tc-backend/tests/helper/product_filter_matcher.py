class ProductFilterMatcher:
    def __init__(self, category=None):
        self.category = category

    def __eq__(self, other):
        return other.category == self.category

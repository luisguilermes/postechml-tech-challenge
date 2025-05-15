from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    amount: float
    unit: str
    category: str
    sub_category: str
    source: str
    collected_at: datetime
    year: int

    def to_dict(self):
        return {
            "amount": self.amount,
            "unit": self.unit,
            "category": self.category,
            "sub_category": self.sub_category,
            "source": self.source,
            "collected_at": self.collected_at.isoformat(),
            "year": self.year,
        }

from datetime import datetime

from pydantic import BaseModel


class Exporting(BaseModel):
    category: str
    country: str
    amount: float
    amount_unit: str
    value: float
    value_unit: str
    source: str
    year: int
    collected_at: datetime

    def to_dict(self):
        return {
            "category": self.category,
            "country": self.country,
            "amount": self.amount,
            "amount_unit": self.amount_unit,
            "value": self.value,
            "value_unit": self.value_unit,
            "source": self.source,
            "year": self.year,
            "collected_at": self.collected_at.isoformat(),
        }

from datetime import datetime

from pydantic import BaseModel


class Processing(BaseModel):
    category: str
    year: int
    grow: str
    sub_grow: str
    amount: float
    amount_unit: str
    source: str
    collected_at: datetime

    def to_dict(self):
        return {
            "category": self.category,
            "year": self.year,
            "grow": self.grow,
            "sub_grow": self.sub_grow,
            "amount": self.amount,
            "amount_unit": self.amount_unit,
            "source": self.source,
            "collected_at": self.collected_at.isoformat(),
        }

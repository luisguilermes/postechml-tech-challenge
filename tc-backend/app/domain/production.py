from datetime import datetime

from pydantic import BaseModel


class Production(BaseModel):
    amount: float
    unit: str
    category: str
    sub_category: str
    source: str
    collected_at: datetime
    year: int

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Importing:
    category: str
    country: str
    amount: float
    amount_unit: str
    value: float
    value_unit: str
    source: str
    year: int
    collected_at: datetime

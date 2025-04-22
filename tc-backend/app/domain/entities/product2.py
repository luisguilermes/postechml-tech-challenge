from dataclasses import dataclass


@dataclass
class Product2:
    id: str
    country: str
    quantity: int
    dollar: float
    source: str
    collected_at: str

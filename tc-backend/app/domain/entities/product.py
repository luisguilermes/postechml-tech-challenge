from dataclasses import dataclass


@dataclass
class Product:
    id: str
    amount: float
    unit: str
    category: str
    sub_category: str
    source: str
    collected_at: str

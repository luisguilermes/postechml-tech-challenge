from dataclasses import dataclass


@dataclass
class Exportation:
    id: str
    amount: float
    unit: str
    category: str
    sub_category: str
    source: str
    collected_at: str

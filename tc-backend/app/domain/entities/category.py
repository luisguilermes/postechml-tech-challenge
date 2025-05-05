from dataclasses import dataclass
from datetime import datetime

@dataclass
class Category:
    id: str
    name: str
    source: str
    collected_at: datetime

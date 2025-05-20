from datetime import datetime

from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    source: str
    collected_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source,
            "collected_at": self.collected_at.isoformat(),
        }

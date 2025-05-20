import json
from datetime import datetime
from typing import List

from sqlalchemy import Column, String, JSON

from app.adapters.database.database import Base
from app.models.category import Category


class CategoryModel(Base):
    __tablename__ = "tc_category"

    id = Column(String, primary_key=True)
    data = Column(JSON)

    def from_dict(self) -> List[Category]:
        data_list = json.loads(self.data)
        return [
            Category(
                id=data["id"],
                name=data["name"],
                source=data["source"],
                collected_at=datetime.fromisoformat(data["collected_at"]),
            )
            for data in data_list
        ]

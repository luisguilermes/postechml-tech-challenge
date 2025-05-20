import json
from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, JSON, String

from app.adapters.database.database import Base
from app.models.importing import Importing


class ImportingModel(Base):
    __tablename__ = "tc_importing"

    year = Column(Integer, primary_key=True)
    category_id = Column(String, primary_key=True)
    data = Column(JSON)

    def from_dict(self) -> List[Importing]:
        data_list = json.loads(self.data)
        return [
            Importing(
                category=data["category"],
                country=data["country"],
                amount=data["amount"],
                amount_unit=data["amount_unit"],
                value=data["value"],
                value_unit=data["value_unit"],
                source=data["source"],
                year=data["year"],
                collected_at=datetime.fromisoformat(data["collected_at"]),
            )
            for data in data_list
        ]

import json
from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, JSON

from app.adapters.database.database import Base
from app.models.processing import Processing


class ProcessingModel(Base):
    __tablename__ = "tc_processing"

    year = Column(Integer, primary_key=True)
    category_id = Column(String, primary_key=True)
    data = Column(JSON)

    def from_dict(self) -> List[Processing]:
        data_list = json.loads(self.data)
        return [
            Processing(
                category=data["category"],
                grow=data["grow"],
                sub_grow=data["sub_grow"],
                amount=data["amount"],
                amount_unit=data["amount_unit"],
                source=data["source"],
                year=data["year"],
                collected_at=datetime.fromisoformat(data["collected_at"]),
            )
            for data in data_list
        ]

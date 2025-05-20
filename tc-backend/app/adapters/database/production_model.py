import json
from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, JSON

from app.adapters.database.database import Base
from app.models.product import Product


class ProductionModel(Base):
    __tablename__ = "tc_production"

    year = Column(Integer, primary_key=True)
    data = Column(JSON)

    def from_dict(self) -> List[Product]:
        data_list = json.loads(self.data)
        return [
            Product(
                amount=data["amount"],
                unit=data["unit"],
                category=data["category"],
                sub_category=data["sub_category"],
                source=data["source"],
                collected_at=datetime.fromisoformat(data["collected_at"]),
                year=data["year"],
            )
            for data in data_list
        ]

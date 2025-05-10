from sqlalchemy import Column, Integer, JSON

from app.adapters.database.database import Base


class ProductionModel(Base):
    __tablename__ = "tc_production"

    year = Column(Integer, primary_key=True)
    data = Column(JSON)

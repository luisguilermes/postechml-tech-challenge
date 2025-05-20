import json
import logging
from typing import List

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.adapters.database.production_model import ProductionModel
from app.adapters.scrapers.production_embrapa_scraper import fetch_production_embrapa
from app.models.product import Product
from app.interfaces.repository import ProductionRepository


class ProductionRepositoryIml(ProductionRepository):
    def __init__(self, db: Session, background_tasks: BackgroundTasks):
        self.db = db
        self.background_tasks = background_tasks
        self.logger = logging.getLogger(__name__)

    def fetch_by_year(self, year: int) -> List[Product]:
        """Get production data by year"""
        try:
            productions = fetch_production_embrapa(year)
            self.background_tasks.add_task(self._upsert_production, year, productions)
            return productions
        except Exception as e:
            self.logger.error(e)
            return self._fetch_by_year_from_db(year)

    def _upsert_production(self, year: int, data: List[Product]) -> None:
        new_data = list(map(_update_source, data))

        # Tenta encontrar o registro existente
        production_model = (
            self.db.query(ProductionModel).filter(ProductionModel.year == year).first()
        )

        if production_model:
            # Atualiza os dados
            production_model.data = json.dumps([p.to_dict() for p in new_data])
        else:
            # Cria novo
            production_model = ProductionModel(
                year=year, data=json.dumps([p.to_dict() for p in new_data])
            )
            self.db.add(production_model)

        self.db.commit()
        self.db.refresh(production_model)

    def _fetch_by_year_from_db(self, year: int) -> List[Product]:
        production_year = (
            self.db.query(ProductionModel).filter(ProductionModel.year == year).first()
        )
        if not production_year:
            self.logger.error(
                f"The fallback to the database has not yet loaded the production data for the year {year}"
            )
            raise HTTPException(
                status_code=503,
                detail="Serviço externo indisponível no momento. Tente novamente mais tarde.",
            )
        return production_year.from_dict()


def _update_source(p: Product) -> Product:
    """Update the source of the production data"""
    p.source = "DB/Fallback"
    return p

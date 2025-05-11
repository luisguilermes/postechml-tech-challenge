import json
import logging
from typing import List

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.adapters.database.commercialization_model import CommercializationModel
from app.adapters.scrapers.commercialization_embrapa_scraper import (
    fetch_commercialization_embrapa,
)
from app.models.product import Product
from app.interfaces.repository import CommercializationRepository


class CommercializationRepositoryIml(CommercializationRepository):
    def __init__(self, db: Session, background_tasks: BackgroundTasks):
        self.db = db
        self.background_tasks = background_tasks
        self.logger = logging.getLogger(__name__)

    def fetch_by_year(self, year: int) -> List[Product]:
        """Get commercialization data by year"""
        try:
            products = fetch_commercialization_embrapa(year)
            self.background_tasks.add_task(self._upsert_production, year, products)
            return products
        except Exception as e:
            self.logger.error(e)
            return self._fetch_by_year_from_db(year)

    def _upsert_production(self, year: int, data: List[Product]) -> None:
        new_data = list(map(_update_source, data))

        # Tenta encontrar o registro existente
        commercialization_model = (
            self.db.query(CommercializationModel)
            .filter(CommercializationModel.year == year)
            .first()
        )

        if commercialization_model:
            # Atualiza os dados
            commercialization_model.data = json.dumps([p.to_dict() for p in new_data])
        else:
            # Cria novo
            commercialization_model = CommercializationModel(
                year=year, data=json.dumps([p.to_dict() for p in new_data])
            )
            self.db.add(commercialization_model)

        self.db.commit()
        self.db.refresh(commercialization_model)

    def _fetch_by_year_from_db(self, year: int) -> List[Product]:
        production_year = (
            self.db.query(CommercializationModel)
            .filter(CommercializationModel.year == year)
            .first()
        )
        if not production_year:
            self.logger.error(
                f"O fallback para o banco de dados ainda não carregou os dados de comercialização do ano {year}"
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

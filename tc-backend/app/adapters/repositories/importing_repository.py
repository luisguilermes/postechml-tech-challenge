import json
import logging
from typing import List

from fastapi import HTTPException

from app.adapters.database.category_model import CategoryModel
from app.adapters.scrapers.importing_embrapa_scraper import fetch_all_categories
from app.interfaces.repository import ImportingRepository
from app.models.category import Category


class ImportingRepositoryImpl(ImportingRepository):
    _importing_id = "importing"

    def __init__(self, background_tasks, db):
        self.background_tasks = background_tasks
        self.db = db
        self.logger = logging.getLogger(__name__)

    def fetch_categories(self):
        try:
            categories = fetch_all_categories()
            self.background_tasks.add_task(
                self._upsert_categories,
                categories,
            )
            return categories
        except Exception as e:
            self.logger.error(e)
            return self._fetch_categories_from_db()

    def _upsert_categories(self, data: List[Category]) -> None:
        new_data = list(map(_update_source, data))

        # Tenta encontrar o registro existente
        category_model = (
            self.db.query(CategoryModel)
            .filter(CategoryModel.id == self._importing_id)
            .first()
        )

        if category_model:
            # Atualiza os dados
            category_model.data = json.dumps([p.to_dict() for p in new_data])
        else:
            # Cria novo
            category_model = CategoryModel(
                id=self._importing_id, data=json.dumps([p.to_dict() for p in new_data])
            )
            self.db.add(category_model)

        self.db.commit()
        self.db.refresh(category_model)

    def _fetch_categories_from_db(self) -> List[Category]:
        importing_categories = (
            self.db.query(CategoryModel)
            .filter(CategoryModel.id == self._importing_id)
            .first()
        )
        if not importing_categories:
            self.logger.error(
                f"The fallback to the database has not yet loaded the importing category data"
            )
            raise HTTPException(
                status_code=503,
                detail="Serviço externo indisponível no momento. Tente novamente mais tarde.",
            )
        return importing_categories.from_dict()

    def fetch_importing_by_year(self, year: int):
        # Implement the logic to fetch importing data by year from the database
        pass


def _update_source(p: Category) -> Category:
    """Update the source of the production data"""
    p.source = "DB/Fallback"
    return p

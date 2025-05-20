import json
import logging
from typing import List

from fastapi import HTTPException

from app.adapters.database.category_model import CategoryModel
from app.adapters.database.exporting_model import ExportingModel
from app.adapters.scrapers.exporting_embrapa_scraper import (
    fetch_all_categories_embrapa,
    fetch_exports_by_category_from_embrapa,
)
from app.interfaces.repository import ExportingRepository
from app.models.category import Category
from app.models.exporting import Exporting


class ExportingRepositoryImpl(ExportingRepository):

    _exporting_id = "exporting"

    def __init__(self, background_tasks, db):
        self.background_tasks = background_tasks
        self.db = db
        self.logger = logging.getLogger(__name__)

    def fetch_categories(self):
        try:
            categories = fetch_all_categories_embrapa()
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
            .filter(CategoryModel.id == self._exporting_id)
            .first()
        )

        if category_model:
            # Atualiza os dados
            category_model.data = json.dumps([p.to_dict() for p in new_data])
        else:
            # Cria novo
            category_model = CategoryModel(
                id=self._exporting_id, data=json.dumps([p.to_dict() for p in new_data])
            )
            self.db.add(category_model)

        self.db.commit()
        self.db.refresh(category_model)

    def _fetch_categories_from_db(self) -> List[Category]:
        exporting_categories = (
            self.db.query(CategoryModel)
            .filter(CategoryModel.id == self._exporting_id)
            .first()
        )
        if not exporting_categories:
            self.logger.error(
                "The fallback to the database has not yet loaded the exporting category data"
            )
            raise HTTPException(
                status_code=503,
                detail="Serviço externo indisponível no momento. Tente novamente mais tarde.",
            )
        return exporting_categories.from_dict()

    def fetch_imports_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Exporting]:
        try:
            imports = fetch_exports_by_category_from_embrapa(
                category_id=category_id, year=year
            )
            self.background_tasks.add_task(
                self._upsert_imports,
                year,
                category_id,
                imports,
            )
            return imports
        except Exception as e:
            self.logger.error(e)
            return self._fetch_by_year_and_category_from_db(
                category_id=category_id, year=year
            )

    def _upsert_imports(
        self, year: int, category_id: str, data: List[Exporting]
    ) -> None:
        new_data = list(map(_update_source, data))

        # Tenta encontrar o registro existente
        exporting_model = (
            self.db.query(ExportingModel)
            .filter(
                ExportingModel.year == year, ExportingModel.category_id == category_id
            )
            .first()
        )

        if exporting_model:
            # Atualiza os dados
            exporting_model.data = json.dumps([p.to_dict() for p in new_data])
        else:
            # Cria novo
            exporting_model = ExportingModel(
                year=year,
                category_id=category_id,
                data=json.dumps([p.to_dict() for p in new_data]),
            )
            self.db.add(exporting_model)

        self.db.commit()
        self.db.refresh(exporting_model)

    def _fetch_by_year_and_category_from_db(
        self, year: int, category_id: str
    ) -> List[Exporting]:
        exporting = (
            self.db.query(ExportingModel)
            .filter(
                ExportingModel.year == year, ExportingModel.category_id == category_id
            )
            .first()
        )
        if not exporting:
            self.logger.error(
                f"The fallback to the database has not yet loaded the category data for the year {year} "
                f"and category {category_id}"
            )
            raise HTTPException(
                status_code=503,
                detail="Serviço externo indisponível no momento. Tente novamente mais tarde.",
            )
        return exporting.from_dict()


def _update_source(p: Exporting) -> Exporting:
    """Update the source of the production data"""
    p.source = "DB/Fallback"
    return p

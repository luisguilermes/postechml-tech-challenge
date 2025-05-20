import json
import logging
from typing import List

from fastapi import HTTPException

from app.adapters.database.category_model import CategoryModel
from app.adapters.database.processing_model import ProcessingModel
from app.adapters.scrapers.processing_embrapa_scraper import (
    fetch_all_categories_embrapa,
    fetch_process_by_category_from_embrapa,
)
from app.interfaces.repository import ProcessingRepository
from app.models.category import Category
from app.models.processing import Processing


class ProcessingRepositoryImpl(ProcessingRepository):

    _processing_id = "processing"

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
            .filter(CategoryModel.id == self._processing_id)
            .first()
        )

        if category_model:
            # Atualiza os dados
            category_model.data = json.dumps([p.to_dict() for p in new_data])
        else:
            # Cria novo
            category_model = CategoryModel(
                id=self._processing_id, data=json.dumps([p.to_dict() for p in new_data])
            )
            self.db.add(category_model)

        self.db.commit()
        self.db.refresh(category_model)

    def _fetch_categories_from_db(self) -> List[Category]:
        processing_categories = (
            self.db.query(CategoryModel)
            .filter(CategoryModel.id == self._processing_id)
            .first()
        )
        if not processing_categories:
            self.logger.error(
                "The fallback to the database has not yet loaded the processing category data"
            )
            raise HTTPException(
                status_code=503,
                detail="Serviço externo indisponível no momento. Tente novamente mais tarde.",
            )
        return processing_categories.from_dict()

    def fetch_process_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Processing]:
        try:
            process = fetch_process_by_category_from_embrapa(
                category_id=category_id, year=year
            )
            self.background_tasks.add_task(
                self._upsert_process,
                year,
                category_id,
                process,
            )
            return process
        except Exception as e:
            self.logger.error(e)
            return self._fetch_by_year_and_category_from_db(
                category_id=category_id, year=year
            )

    def _upsert_process(
        self, year: int, category_id: str, data: List[Processing]
    ) -> None:
        new_data = list(map(_update_source, data))

        # Tenta encontrar o registro existente
        processing_model = (
            self.db.query(ProcessingModel)
            .filter(
                ProcessingModel.year == year, ProcessingModel.category_id == category_id
            )
            .first()
        )

        if processing_model:
            # Atualiza os dados
            processing_model.data = json.dumps([p.to_dict() for p in new_data])
        else:
            # Cria novo
            processing_model = ProcessingModel(
                year=year, category_id=category_id, data=json.dumps([p.to_dict() for p in new_data])
            )
            self.db.add(processing_model)

        self.db.commit()
        self.db.refresh(processing_model)

    def _fetch_by_year_and_category_from_db(
        self, year: int, category_id: str
    ) -> List[Processing]:
        processing = (
            self.db.query(ProcessingModel)
            .filter(
                ProcessingModel.year == year, ProcessingModel.category_id == category_id
            )
            .first()
        )
        if not processing:
            self.logger.error(
                f"The fallback to the database has not yet loaded the category data for the year {year} "
                f"and category {category_id}"
            )
            raise HTTPException(
                status_code=503,
                detail="Serviço externo indisponível no momento. Tente novamente mais tarde.",
            )
        return processing.from_dict()


def _update_source(p: Processing) -> Processing:
    """Update the source of the processing data"""
    p.source = "DB/Fallback"
    return p

from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.adapters.database.database import get_db
from app.adapters.repositories.production_repository import ProductionRepositoryIml
from app.interfaces.repository import ProductionRepository
from app.use_cases.production_usecase import ProductionUseCase


def get_production_repository(
    background_tasks: BackgroundTasks, db: Session
) -> ProductionRepository:
    return ProductionRepositoryIml(background_tasks=background_tasks, db=db)


def get_production_use_case(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ProductionUseCase:
    return ProductionUseCase(get_production_repository(background_tasks, db))

from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.adapters.database.database import get_db
from app.adapters.repositories.exporting_repository import ExportingRepositoryImpl
from app.interfaces.repository import ExportingRepository
from app.use_cases.exporting_usecase import ExportingUseCase


def get_exporting_repository(
    background_tasks: BackgroundTasks, db: Session
) -> ExportingRepository:
    return ExportingRepositoryImpl(background_tasks=background_tasks, db=db)


def get_exporting_use_case(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ExportingUseCase:
    return ExportingUseCase(get_exporting_repository(background_tasks, db))

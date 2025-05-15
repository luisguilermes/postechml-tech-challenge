from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.adapters.database.database import get_db
from app.adapters.repositories.importing_repository import ImportingRepositoryImpl
from app.interfaces.repository import ImportingRepository
from app.use_cases.importing_usecase import ImportingUseCase


def get_importing_repository(
    background_tasks: BackgroundTasks, db: Session
) -> ImportingRepository:
    return ImportingRepositoryImpl(background_tasks=background_tasks, db=db)


def get_importing_use_case(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ImportingUseCase:
    return ImportingUseCase(get_importing_repository(background_tasks, db))

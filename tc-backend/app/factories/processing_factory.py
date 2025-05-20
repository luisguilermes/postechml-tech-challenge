from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.adapters.database.database import get_db
from app.adapters.repositories.processing_repository import ProcessingRepositoryImpl
from app.interfaces.repository import ProcessingRepository
from app.use_cases.processing_usecase import ProcessingUseCase


def get_processing_repository(
    background_tasks: BackgroundTasks, db: Session
) -> ProcessingRepository:
    return ProcessingRepositoryImpl(background_tasks=background_tasks, db=db)


def get_processing_use_case(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ProcessingUseCase:
    return ProcessingUseCase(get_processing_repository(background_tasks, db))

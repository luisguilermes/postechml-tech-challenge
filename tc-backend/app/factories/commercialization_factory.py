from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.adapters.database.database import get_db
from app.adapters.repositories.commercialization_repository import (
    CommercializationRepositoryIml,
)
from app.interfaces.repository import CommercializationRepository
from app.use_cases.commercialization_usecase import CommercializationUseCase


def get_commercialization_repository(
    background_tasks: BackgroundTasks, db: Session
) -> CommercializationRepository:
    return CommercializationRepositoryIml(background_tasks=background_tasks, db=db)


def get_commercialization_use_case(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> CommercializationUseCase:
    return CommercializationUseCase(
        get_commercialization_repository(background_tasks, db)
    )

from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.params import Query

from app.api.config.doc_errors import unauthorized_response
from app.api.v1.dto.base_dtos import ListResponse
from app.domain.production import Production
from app.factories.production_factory import get_production_use_case
from app.use_cases.production_usecase import ProductionUseCase

router = APIRouter()


@router.get(
    "",
    response_model=ListResponse[Production],
    responses=unauthorized_response,
)
async def get_production(
    year: Optional[int] = Query(
        2023,
        gt=1970,
        le=2023,
    ),
    use_case: ProductionUseCase = Depends(get_production_use_case),
):
    try:
        productions = use_case.get_production_by_year(year)
        return ListResponse[Production](data=productions, total=len(productions))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

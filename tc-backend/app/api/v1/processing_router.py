from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query

from app.api.docs.errors import unauthorized_response
from app.api.v1.dto.base_dtos import ListResponse
from app.api.v1.dto.category_dtos import CategoryResponse
from app.factories.processing_factory import get_processing_use_case
from app.models.processing import Processing
from app.use_cases.processing_usecase import ProcessingUseCase

router = APIRouter()


@router.get(
    "/categories",
    response_model=ListResponse[CategoryResponse],
    responses=unauthorized_response,
)
async def get_processing_categories(
    use_case: ProcessingUseCase = Depends(get_processing_use_case),
):
    """
    Recupera categorias de Processamento de derivados de uva.

    Retorna:
        A uma lista com as categorias existentes.
    """
    try:
        categories = use_case.get_categories()
        data = [
            CategoryResponse(
                id=category.id,
                name=category.name,
            )
            for category in categories
        ]
        return ListResponse[CategoryResponse](data=data, total=len(data))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get(
    "/{category_id}",
    response_model=ListResponse[Processing],
    responses=unauthorized_response,
)
async def get_processing_by_category(
    category_id: str,
    year: Optional[int] = Query(
        2023,
        gt=1970,
        le=2023,
    ),
    use_case: ProcessingUseCase = Depends(get_processing_use_case),
):
    """
    Recupera processamento de vinhos.

    Retorna:
        A uma lista com ano, categorias e quantidade(kg).
    """
    try:
        process = use_case.get_process_by_category_and_year(category_id, year)
        return ListResponse[Processing](data=process, total=len(process))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query

from app.api.docs.errors import unauthorized_response
from app.api.v1.dto.base_dtos import ListResponse
from app.api.v1.dto.category_dtos import CategoryResponse
from app.factories.exporting_factory import get_exporting_use_case
from app.models.exporting import Exporting
from app.use_cases.exporting_usecase import ExportingUseCase

router = APIRouter()


@router.get(
    "/categories",
    response_model=ListResponse[CategoryResponse],
    responses=unauthorized_response,
)
async def get_exporting_categories(
    use_case: ExportingUseCase = Depends(get_exporting_use_case),
):
    """
    Recupera categorias de Exportação de derivados de uva.

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
    response_model=ListResponse[Exporting],
    responses=unauthorized_response,
)
async def get_exporting_by_category(
    category_id: str,
    year: Optional[int] = Query(
        2023,
        gt=1970,
        le=2023,
    ),
    use_case: ExportingUseCase = Depends(get_exporting_use_case),
):
    """
    Recupera exportações de vinhos de mesa dos paises.

    Retorna:
        A uma lista com com paises, quantidade(kg) e valor exportado do Brasil.
    """
    try:
        exports = use_case.get_exporting_by_category_and_year(category_id, year)
        return ListResponse[Exporting](data=exports, total=len(exports))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query

from app.api.docs.errors import unauthorized_response
from app.api.v1.dto.base_dtos import ListResponse
from app.models.product import Product
from app.factories.commercialization_factory import get_commercialization_use_case
from app.use_cases.commercialization_usecase import CommercializationUseCase

router = APIRouter()


@router.get(
    "",
    response_model=ListResponse[Product],
    responses=unauthorized_response,
)
async def get_commercialization(
    year: Optional[int] = Query(
        2023,
        gt=1970,
        le=2023,
    ),
    use_case: CommercializationUseCase = Depends(get_commercialization_use_case),
):
    """
    Recupera comercialização de vinhos, sucos e derivados do Rio Grande do Sul

    Parâmetros:
        year (int): Ano da comercialização desejada - default 2023.

    Retorna:
        A uma lista com os dados de produtos comercializados no ano.
    """
    try:
        productions = use_case.get_production_by_year(year)
        return ListResponse[Product](data=productions, total=len(productions))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

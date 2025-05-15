from datetime import datetime
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from app.adapters.repositories.production_repository import ProductionRepositoryIml
from app.models.product import Product


@patch("app.adapters.repositories.production_repository.fetch_production_embrapa")
@patch(
    "app.adapters.repositories.production_repository.ProductionRepositoryIml._fetch_by_year_from_db"
)
def test_fetch_by_year_returns_production_data_on_success(
    mock_fetch_from_db, mock_fetch_embrapa
):
    mock_fetch_embrapa.return_value = [
        Product(
            amount=1000.0,
            unit="kg",
            category="Category 1",
            sub_category="Subcategory 1",
            year=2023,
            source="API",
            collected_at=datetime.now(),
        )
    ]
    mock_fetch_from_db.return_value = []

    repo = ProductionRepositoryIml(db=MagicMock(), background_tasks=MagicMock())
    result = repo.fetch_by_year(2023)

    assert len(result) == 1
    assert result[0].year == 2023
    assert result[0].source == "API"


@patch("app.adapters.repositories.production_repository.fetch_production_embrapa")
@patch(
    "app.adapters.repositories.production_repository.ProductionRepositoryIml._fetch_by_year_from_db"
)
def test_fetch_by_year_falls_back_to_db_on_exception(
    mock_fetch_from_db, mock_fetch_embrapa
):
    mock_fetch_embrapa.side_effect = Exception("API error")
    mock_fetch_from_db.return_value = [
        Product(
            amount=1000.0,
            unit="kg",
            category="Category 1",
            sub_category="Subcategory 1",
            year=2023,
            source="DB/Fallback",
            collected_at=datetime.now(),
        )
    ]

    repo = ProductionRepositoryIml(db=MagicMock(), background_tasks=MagicMock())
    result = repo.fetch_by_year(2023)

    assert len(result) == 1
    assert result[0].year == 2023
    assert result[0].source == "DB/Fallback"


@patch(
    "app.adapters.repositories.production_repository.ProductionRepositoryIml._fetch_by_year_from_db"
)
def test_fetch_by_year_raises_http_exception_when_db_fails(mock_fetch_from_db):
    mock_fetch_from_db.side_effect = HTTPException(status_code=503)

    repo = ProductionRepositoryIml(db=MagicMock(), background_tasks=MagicMock())

    try:
        repo.fetch_by_year(2023)
    except HTTPException as e:
        assert e.status_code == 503


@patch("app.adapters.repositories.production_repository.ProductionModel")
def test_upsert_production_updates_existing_record(mock_production_model):
    mock_session = MagicMock()
    existing_record = MagicMock()
    mock_production_model.query.filter.return_value.first.return_value = existing_record

    repo = ProductionRepositoryIml(db=mock_session, background_tasks=MagicMock())
    repo._upsert_production(
        2023,
        [
            Product(
                amount=1000.0,
                unit="kg",
                category="Category 1",
                sub_category="Subcategory 1",
                year=2023,
                source="DB/Fallback",
                collected_at=datetime.now(),
            )
        ],
    )

    assert existing_record.data is not None
    mock_session.commit.assert_called_once()

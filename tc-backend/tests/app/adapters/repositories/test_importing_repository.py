from datetime import datetime
from fastapi import HTTPException
from unittest.mock import MagicMock, patch

from app.adapters.repositories.importing_repository import ImportingRepositoryImpl
from app.models.category import Category
from app.models.importing import Importing


@patch("app.adapters.repositories.importing_repository.fetch_all_categories_embrapa")
@patch(
    "app.adapters.repositories.importing_repository.ImportingRepositoryImpl._fetch_categories_from_db"
)
def test_fetch_importing_category_returns_categories_data_on_success(
    mock_fetch_from_db, mock_fetch_embrapa
):
    mock_fetch_embrapa.return_value = [
        Category(
            id="xpto",
            name="Category 1",
            source="API",
            collected_at=datetime.now(),
        )
    ]
    mock_fetch_from_db.return_value = []

    repo = ImportingRepositoryImpl(db=MagicMock(), background_tasks=MagicMock())
    result = repo.fetch_categories()

    assert len(result) == 1
    assert result[0].id == "xpto"
    assert result[0].name == "Category 1"
    assert result[0].source == "API"


@patch("app.adapters.repositories.importing_repository.fetch_all_categories_embrapa")
@patch(
    "app.adapters.repositories.importing_repository.ImportingRepositoryImpl._fetch_categories_from_db"
)
def test_importing_category_falls_back_to_db_on_exception(
    mock_fetch_from_db, mock_fetch_embrapa
):
    mock_fetch_embrapa.side_effect = Exception("API error")
    mock_fetch_from_db.return_value = [
        Category(
            id="xpto",
            name="Category 1",
            source="DB/Fallback",
            collected_at=datetime.now(),
        )
    ]

    repo = ImportingRepositoryImpl(db=MagicMock(), background_tasks=MagicMock())
    result = repo.fetch_categories()

    assert len(result) == 1
    assert result[0].id == "xpto"
    assert result[0].name == "Category 1"
    assert result[0].source == "DB/Fallback"


@patch(
    "app.adapters.repositories.importing_repository.ImportingRepositoryImpl._fetch_categories_from_db"
)
def test_fetch_importing_category_raises_http_exception_when_db_fails(
    mock_fetch_from_db,
):
    mock_fetch_from_db.side_effect = HTTPException(status_code=503)

    repo = ImportingRepositoryImpl(db=MagicMock(), background_tasks=MagicMock())

    try:
        repo.fetch_categories()
    except HTTPException as e:
        assert e.status_code == 503


@patch("app.adapters.repositories.importing_repository.CategoryModel")
def test_upsert_importing_category_updates_existing_record(mock_production_model):
    mock_session = MagicMock()
    existing_record = MagicMock()
    mock_production_model.query.filter.return_value.first.return_value = existing_record

    repo = ImportingRepositoryImpl(db=mock_session, background_tasks=MagicMock())
    repo._upsert_categories(
        [
            Category(
                id="xpto",
                name="Category 1",
                source="DB/Fallback",
                collected_at=datetime.now(),
            )
        ],
    )

    assert existing_record.data is not None
    mock_session.commit.assert_called_once()


@patch("app.adapters.repositories.importing_repository.fetch_all_categories_embrapa")
@patch(
    "app.adapters.repositories.importing_repository.fetch_imports_by_category_from_embrapa"
)
@patch(
    "app.adapters.repositories.importing_repository.ImportingRepositoryImpl._fetch_by_year_and_category_from_db"
)
def test_fetch_imports_by_category_and_year_returns_categories_data_on_success(
    mock_fetch_categories_embrapa, mock_fetch_embrapa, mock_fetch_from_db
):
    mock_fetch_categories_embrapa.return_value = [
        Category(
            id="xpto",
            name="Category 1",
            source="API",
            collected_at=datetime.now(),
        )
    ]
    mock_fetch_embrapa.return_value = [
        Importing(
            category="Category 1",
            country="Brazil",
            amount=100.5,
            amount_unit="kg",
            value=200.0,
            value_unit="USD",
            source="API",
            year=2023,
            collected_at=datetime(2023, 1, 1, 12, 0, 0),
        )
    ]
    mock_fetch_from_db.return_value = []

    repo = ImportingRepositoryImpl(db=MagicMock(), background_tasks=MagicMock())
    result = repo.fetch_imports_by_category_and_year(
        category_id="Category 1", year=2023
    )

    assert len(result) == 1
    assert result[0].category == "Category 1"
    assert result[0].country == "Brazil"
    assert result[0].source == "API"


@patch(
    "app.adapters.repositories.importing_repository.ImportingRepositoryImpl._fetch_by_year_and_category_from_db"
)
def test_fetch_imports_by_category_and_year_raises_http_exception_when_db_fails(
    mock_fetch_from_db,
):
    category_id = "xpto"
    year = 2023
    mock_fetch_from_db.side_effect = HTTPException(status_code=503)

    repo = ImportingRepositoryImpl(db=MagicMock(), background_tasks=MagicMock())

    try:
        repo.fetch_imports_by_category_and_year(category_id, year)
    except HTTPException as e:
        assert e.status_code == 503

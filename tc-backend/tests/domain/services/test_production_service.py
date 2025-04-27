from unittest.mock import MagicMock
import pytest
from app.domain.services.production_service import ProductionService
from app.domain.repositories.base_repository import BaseRepository
from app.domain.vo.product_filter import Filter


@pytest.fixture
def mock_production_repository():
    return MagicMock(spec=BaseRepository)


@pytest.fixture
def production_service(mock_production_repository):
    return ProductionService(production_repository=mock_production_repository)


def test_get_all_products_without_filter(
    production_service, mock_production_repository
):
    # Arrange
    year = 2023
    mock_products = [{"id": 1, "name": "Product A"}, {"id": 2, "name": "Product B"}]
    mock_production_repository.fetch_all.return_value = mock_products

    # Act
    result = production_service.get_all_products(year=year)

    # Assert
    mock_production_repository.fetch_all.assert_called_once_with(year=year)
    assert result == mock_products


def test_get_all_products_with_filter(production_service, mock_production_repository):
    # Arrange
    year = 2023
    mock_products = [{"id": 1, "name": "Product A"}, {"id": 2, "name": "Product B"}]
    filtered_products = [{"id": 1, "name": "Product A"}]
    mock_production_repository.fetch_all.return_value = mock_products

    mock_filter = MagicMock(spec=Filter)
    mock_filter.apply.return_value = filtered_products

    # Act
    result = production_service.get_all_products(year=year, product_filter=mock_filter)

    # Assert
    mock_production_repository.fetch_all.assert_called_once_with(year=year)
    mock_filter.apply.assert_called_once_with(mock_products)
    assert result == filtered_products

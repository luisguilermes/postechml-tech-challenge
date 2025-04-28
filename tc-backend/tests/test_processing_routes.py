from unittest.mock import patch, MagicMock
from tests.helper.product_filter_matcher import ProductFilterMatcher


@patch("app.entrypoint.rest.processing_routes.get_processing_service")
def test_get_processing_resource(mock_get_processing_service, client):
    """Test the GET method of the ProcessingResource."""
    # Mock the service response
    mock_service = MagicMock()
    mock_service.get_all_products.return_value = [
        {
            "id": "1",
            "amount": 100.0,
            "unit": "kg",
            "category": "Wine",
            "sub_category": "Red",
            "source": "Embrapa",
            "collected_at": "2023-01-01T00:00:00",
            "year": 2023,
        }
    ]
    mock_get_processing_service.return_value = mock_service

    # Perform the GET request
    response = client.get("/api/v1/processing?year=2023&category=Wine")

    # Assertions
    assert response.status_code == 200
    assert response.json == [
        {
            "id": "1",
            "amount": 100.0,
            "unit": "kg",
            "category": "Wine",
            "sub_category": "Red",
            "source": "Embrapa",
            "collected_at": "2023-01-01T00:00:00",
            "year": 2023,
        }
    ]
    mock_service.get_all_products.assert_called_once_with(
        year=2023, product_filter=ProductFilterMatcher(category="Wine")
    )

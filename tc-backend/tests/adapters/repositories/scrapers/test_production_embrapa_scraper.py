from unittest.mock import patch, MagicMock
import pytest
from app.adapters.repositories.scrapers.production_embrapa_scraper import (
    ProductionEmbrapaScraper,
)

# Mock constants
MOCK_HTML = """
<table class="tb_base tb_dados">
    <tr><td class="tb_item">Category 1</td></tr>
    <tr>
        <td class="tb_subitem">Subcategory 1</td>
        <td>1.000</td>
    </tr>
    <tr>
        <td class="tb_subitem">Subcategory 2</td>
        <td>2.500</td>
    </tr>
</table>
"""


@pytest.fixture
def scraper():
    return ProductionEmbrapaScraper()


@patch("requests.get")
def test_fetch_all(mock_get, scraper):
    # Mock the HTTP response
    mock_response = MagicMock()
    mock_response.text = MOCK_HTML
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the method
    year = 2023
    products = scraper.fetch_all(year)

    # Assertions
    assert len(products) == 2
    assert products[0]["category"] == "Category 1"
    assert products[0]["sub_category"] == "Subcategory 1"
    assert products[0]["amount"] == 1000.0
    assert products[0]["year"] == year
    assert products[1]["sub_category"] == "Subcategory 2"
    assert products[1]["amount"] == 2500.0

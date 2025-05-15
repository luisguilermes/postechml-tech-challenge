from unittest.mock import patch, MagicMock

from app.adapters.scrapers.commercialization_embrapa_scraper import (
    fetch_commercialization_embrapa,
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


@patch("requests.get")
def test_fetch_all(mock_get):
    # Mock the HTTP response
    mock_response = MagicMock()
    mock_response.text = MOCK_HTML
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the method
    year = 2023
    products = fetch_commercialization_embrapa(year)

    # Assertions
    assert len(products) == 2
    production1 = next(
        filter(lambda p: p.sub_category == "Subcategory 1", products), None
    )
    assert production1.category == "Category 1"
    assert production1.amount == 1000.0
    production2 = next(
        filter(lambda p: p.sub_category == "Subcategory 2", products), None
    )
    assert production2.year == year
    assert production2.amount == 2500.0

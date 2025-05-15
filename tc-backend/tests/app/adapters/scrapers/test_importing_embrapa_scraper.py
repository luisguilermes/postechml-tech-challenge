from unittest.mock import patch, MagicMock

from app.adapters.scrapers.importing_embrapa_scraper import (
    fetch_all_categories_embrapa,
    fetch_imports_by_category_from_embrapa,
)

MOCK_RESPONSE = """
<html lang="pt-BR">
  <body>
    <table class="tb_base">
      <tr>
        <td class="col_center">
          <div class="div_content">
            <table class="tb_base tb_header no_print">
              <tr>
                <td>
                  <form action="index.php" method="get">
                    <p>
                      <button class="btn_sopt" type="submit" name="subopcao" value="subopt_01">Vinhos de mesa</button>
                      <br>
                    </p>
                  </form>
                </td>
              </tr>
            </table>
            <div class="content_center">
              <table class="tb_base tb_dados">
                <tbody>
                  <tr>
                    <td>Africa do Sul</td>
                    <td>658.238</td>
                    <td>2.133.775</td>
                  </tr>
                  <tr>
                    <td>Total</td>
                    <td>153.122.230</td>
                    <td>481.082.975</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


@patch("requests.get")
def test_fetch_all_categories_returns_correct_data(mock_get):
    # Mock the HTTP response
    mock_response = MagicMock()
    mock_response.text = MOCK_RESPONSE
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the method
    categories = fetch_all_categories_embrapa()

    # Assertions
    assert len(categories) == 1
    assert categories[0].id == "subopt_01"
    assert categories[0].name == "Vinhos de mesa"


@patch("requests.get")
def test_fetch_imports_by_category_handles_empty_table(mock_get):
    mock_response = MagicMock()
    mock_response.text = MOCK_RESPONSE
    mock_get.return_value = mock_response

    imports = fetch_imports_by_category_from_embrapa(2023, "subopt_01")

    assert len(imports) == 1
    assert imports[0].country == "Africa do Sul"
    assert imports[0].amount == 658238
    assert imports[0].value == 2133775


@patch("requests.get")
def test_fetch_imports_by_category_raises_error_for_invalid_category(mock_get):
    mock_response = MagicMock()
    mock_response.text = MOCK_RESPONSE
    mock_get.return_value = mock_response

    try:
        fetch_imports_by_category_from_embrapa(2023, "subopt_10")
    except ValueError as e:
        assert str(e) == "Categoria com id 'subopt_10' não encontrada"

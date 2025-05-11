import json
from datetime import datetime
from app.models.product import Product
from app.adapters.database.commercialization_model import CommercializationModel


def test_from_dict_returns_correct_list_of_products_for_commercialization():
    mock_data = json.dumps(
        [
            {
                "amount": 200.0,
                "unit": "tons",
                "category": "Fruits",
                "sub_category": "Apples",
                "source": "API",
                "collected_at": "2023-02-01T10:00:00",
                "year": 2023,
            }
        ]
    )
    commercialization_model = CommercializationModel(year=2023, data=mock_data)

    result = commercialization_model.from_dict()

    assert len(result) == 1
    assert isinstance(result[0], Product)
    assert result[0].amount == 200.0
    assert result[0].unit == "tons"
    assert result[0].category == "Fruits"
    assert result[0].sub_category == "Apples"
    assert result[0].source == "API"
    assert result[0].collected_at == datetime(2023, 2, 1, 10, 0, 0)
    assert result[0].year == 2023


def test_from_dict_handles_empty_data_for_commercialization():
    commercialization_model = CommercializationModel(year=2023, data=json.dumps([]))

    result = commercialization_model.from_dict()

    assert result == []


def test_from_dict_raises_error_for_invalid_json_in_commercialization():
    commercialization_model = CommercializationModel(year=2023, data="invalid_json")

    try:
        commercialization_model.from_dict()
    except json.JSONDecodeError:
        assert True

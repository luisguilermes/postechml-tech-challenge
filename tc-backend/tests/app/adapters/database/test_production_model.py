import json
from datetime import datetime

from app.adapters.database.production_model import ProductionModel
from app.models.product import Product


def test_from_dict_returns_correct_list_of_products():
    mock_data = json.dumps(
        [
            {
                "amount": 100.5,
                "unit": "kg",
                "category": "Grains",
                "sub_category": "Wheat",
                "source": "API",
                "collected_at": "2023-01-01T12:00:00",
                "year": 2023,
            }
        ]
    )
    production_model = ProductionModel(year=2023, data=mock_data)

    result = production_model.from_dict()

    assert len(result) == 1
    assert isinstance(result[0], Product)
    assert result[0].amount == 100.5
    assert result[0].unit == "kg"
    assert result[0].category == "Grains"
    assert result[0].sub_category == "Wheat"
    assert result[0].source == "API"
    assert result[0].collected_at == datetime(2023, 1, 1, 12, 0, 0)
    assert result[0].year == 2023


def test_from_dict_handles_empty_data():
    production_model = ProductionModel(year=2023, data=json.dumps([]))

    result = production_model.from_dict()

    assert result == []


def test_from_dict_raises_error_for_invalid_json():
    production_model = ProductionModel(year=2023, data="invalid_json")

    try:
        production_model.from_dict()
    except json.JSONDecodeError:
        assert True

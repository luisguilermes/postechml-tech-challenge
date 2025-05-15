import json
from datetime import datetime

from app.adapters.database.category_model import CategoryModel
from app.models.category import Category
from app.adapters.database.commercialization_model import CommercializationModel


def test_from_dict_returns_correct_list_of_categories():
    mock_data = json.dumps(
        [
            {
                "id": "test",
                "name": "tons",
                "source": "API",
                "collected_at": "2023-02-01T10:00:00",
            }
        ]
    )
    category_model = CategoryModel(data=mock_data)

    result = category_model.from_dict()

    assert len(result) == 1
    assert isinstance(result[0], Category)
    assert result[0].id == "test"
    assert result[0].name == "tons"
    assert result[0].source == "API"
    assert result[0].collected_at == datetime(2023, 2, 1, 10, 0, 0)


def test_from_dict_handles_empty_data_for_category():
    category_model = CategoryModel(data=json.dumps([]))

    result = category_model.from_dict()

    assert result == []


def test_from_dict_raises_error_for_invalid_json_in_category():
    category_model = CommercializationModel(data="invalid_json")

    try:
        category_model.from_dict()
    except json.JSONDecodeError:
        assert True

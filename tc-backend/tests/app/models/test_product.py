from datetime import datetime

from app.models.product import Product


def test_product_to_dict_returns_correct_representation():
    product = Product(
        amount=100.5,
        unit="kg",
        category="Grains",
        sub_category="Wheat",
        source="API",
        collected_at=datetime(2023, 1, 1, 12, 0, 0),
        year=2023,
    )

    result = product.to_dict()

    assert result == {
        "amount": 100.5,
        "unit": "kg",
        "category": "Grains",
        "sub_category": "Wheat",
        "source": "API",
        "collected_at": "2023-01-01T12:00:00",
        "year": 2023,
    }


def test_product_to_dict_handles_empty_fields():
    product = Product(
        amount=0.0,
        unit="",
        category="",
        sub_category="",
        source="",
        collected_at=datetime(2023, 1, 1, 12, 0, 0),
        year=2023,
    )

    result = product.to_dict()

    assert result == {
        "amount": 0.0,
        "unit": "",
        "category": "",
        "sub_category": "",
        "source": "",
        "collected_at": "2023-01-01T12:00:00",
        "year": 2023,
    }

from datetime import datetime

from app.models.importing import Importing


def test_importing_to_dict_returns_correct_representation():
    importing = Importing(
        category="xpto",
        country="Brazil",
        amount=100.5,
        amount_unit="kg",
        value=200.0,
        value_unit="USD",
        source="API",
        year=2023,
        collected_at=datetime(2023, 1, 1, 12, 0, 0),
    )

    result = importing.to_dict()

    assert result == {
        "category": "xpto",
        "country": "Brazil",
        "amount": 100.5,
        "amount_unit": "kg",
        "value": 200.0,
        "value_unit": "USD",
        "source": "API",
        "year": 2023,
        "collected_at": "2023-01-01T12:00:00",
    }

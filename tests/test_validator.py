"""
Tests for the sales data validation module.
"""

from src.pipeline.validator import validate_record


def test_valid_sales_record():
    """A valid sales record should pass validation."""
    record = {
        "InvoiceNo": "536365",
        "Quantity": 6,
        "UnitPrice": 2.55,
    }

    result = validate_record(record)

    assert result["is_valid"] is True
    assert result["reason"] is None


def test_invalid_quantity():
    """A record with zero quantity should be rejected."""
    record = {
        "InvoiceNo": "536365",
        "Quantity": 0,
        "UnitPrice": 2.55,
    }

    result = validate_record(record)

    assert result["is_valid"] is False
    assert result["reason"] == "Quantity must be greater than zero"


def test_invalid_unit_price():
    """A record with zero unit price should be rejected."""
    record = {
        "InvoiceNo": "536365",
        "Quantity": 6,
        "UnitPrice": 0,
    }

    result = validate_record(record)

    assert result["is_valid"] is False
    assert result["reason"] == "UnitPrice must be greater than zero"


def test_missing_required_field():
    """A record with a missing required field should be rejected."""
    record = {
        "InvoiceNo": "536365",
        "Quantity": 6,
    }

    result = validate_record(record)

    assert result["is_valid"] is False
    assert result["reason"] == "UnitPrice is missing"


def test_non_numeric_values():
    """Non-numeric quantity or price should be rejected."""
    record = {
        "InvoiceNo": "536365",
        "Quantity": "invalid",
        "UnitPrice": 2.55,
    }

    result = validate_record(record)

    assert result["is_valid"] is False
    assert result["reason"] == "Quantity and UnitPrice must be numeric"

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

    assert validate_record(record) is True


def test_invalid_quantity():
    """A record with zero quantity should fail validation."""
    record = {
        "InvoiceNo": "536365",
        "Quantity": 0,
        "UnitPrice": 2.55,
    }

    assert validate_record(record) is False


def test_invalid_unit_price():
    """A record with zero unit price should fail validation."""
    record = {
        "InvoiceNo": "536365",
        "Quantity": 6,
        "UnitPrice": 0,
    }

    assert validate_record(record) is False

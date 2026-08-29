"""
Tests for the sales data processing module.
"""

from src.pipeline.processor import process_record


def test_process_valid_record():
    """A valid record should have revenue calculated correctly."""

    record = {
        "InvoiceNo": "536365",
        "Quantity": 6,
        "UnitPrice": 2.55,
    }

    result = process_record(record)

    assert result["Quantity"] == 6.0
    assert result["UnitPrice"] == 2.55
    assert result["Revenue"] == 15.30
    assert result["ValidationStatus"] == "VALID"


def test_process_record_preserves_original_fields():
    """Processing should preserve the original sales fields."""

    record = {
        "InvoiceNo": "536366",
        "StockCode": "85123A",
        "Description": "WHITE HANGING HEART T-LIGHT HOLDER",
        "Quantity": 2,
        "UnitPrice": 5.00,
    }

    result = process_record(record)

    assert result["InvoiceNo"] == "536366"
    assert result["StockCode"] == "85123A"
    assert result["Description"] == "WHITE HANGING HEART T-LIGHT HOLDER"

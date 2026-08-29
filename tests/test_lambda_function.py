"""
Tests for the Lambda processing flow.
"""

from src.pipeline.lambda_function import process_sales_record


def test_valid_record_is_processed():
    """A valid record should be transformed and marked as valid."""

    record = {
        "InvoiceNo": "536365",
        "Quantity": 6,
        "UnitPrice": 2.55,
    }

    result = process_sales_record(record)

    assert result["ValidationStatus"] == "VALID"
    assert result["Revenue"] == 15.30


def test_invalid_record_is_rejected_with_reason():
    """An invalid record should be rejected with a reason."""

    record = {
        "InvoiceNo": "536365",
        "Quantity": 0,
        "UnitPrice": 2.55,
    }

    result = process_sales_record(record)

    assert result["ValidationStatus"] == "REJECTED"
    assert result["RejectionReason"] == "Quantity must be greater than zero"


def test_missing_field_is_rejected():
    """A record missing a required field should be rejected."""

    record = {
        "InvoiceNo": "536365",
        "Quantity": 6,
    }

    result = process_sales_record(record)

    assert result["ValidationStatus"] == "REJECTED"
    assert result["RejectionReason"] == "UnitPrice is missing"

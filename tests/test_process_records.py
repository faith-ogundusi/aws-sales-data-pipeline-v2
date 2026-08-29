"""
Tests for batch sales record processing.
"""

from src.pipeline.lambda_function import process_records


def test_process_records_separates_valid_and_rejected():
    """Records should be separated into valid and rejected lists."""

    records = [
        {
            "InvoiceNo": "10001",
            "Quantity": 5,
            "UnitPrice": 2.00,
        },
        {
            "InvoiceNo": "10002",
            "Quantity": 0,
            "UnitPrice": 3.00,
        },
        {
            "InvoiceNo": "10003",
            "Quantity": 10,
            "UnitPrice": 1.50,
        },
    ]

    valid_records, rejected_records = process_records(records)

    assert len(valid_records) == 2
    assert len(rejected_records) == 1

    assert valid_records[0]["ValidationStatus"] == "VALID"
    assert valid_records[0]["Revenue"] == 10.00

    assert rejected_records[0]["ValidationStatus"] == "REJECTED"
    assert rejected_records[0]["RejectionReason"] == (
        "Quantity must be greater than zero"
    )

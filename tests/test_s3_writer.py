"""
Tests for the Amazon S3 output writer.
"""

from unittest.mock import patch

from src.pipeline.s3_writer import write_csv_to_s3


def test_write_csv_to_s3():
    """Records should be converted to CSV and sent to S3."""

    records = [
        {
            "InvoiceNo": "10001",
            "Quantity": 5.0,
            "UnitPrice": 2.00,
            "Revenue": 10.00,
            "ValidationStatus": "VALID",
        },
        {
            "InvoiceNo": "10002",
            "Quantity": 10.0,
            "UnitPrice": 1.50,
            "Revenue": 15.00,
            "ValidationStatus": "VALID",
        },
    ]

    with patch(
        "src.pipeline.s3_writer.s3_client.put_object"
    ) as mock_put_object:

        result = write_csv_to_s3(
            "sales-pipeline-v2",
            "valid/valid_sales.csv",
            records
        )

    assert result == "s3://sales-pipeline-v2/valid/valid_sales.csv"

    mock_put_object.assert_called_once()

    call_arguments = mock_put_object.call_args.kwargs

    assert call_arguments["Bucket"] == "sales-pipeline-v2"
    assert call_arguments["Key"] == "valid/valid_sales.csv"
    assert call_arguments["ContentType"] == "text/csv"

    csv_output = call_arguments["Body"].decode("utf-8")

    assert "InvoiceNo,Quantity,UnitPrice,Revenue,ValidationStatus" in csv_output
    assert "10001,5.0,2.0,10.0,VALID" in csv_output

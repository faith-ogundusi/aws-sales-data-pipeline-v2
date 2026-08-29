"""
Tests for the Amazon S3 CSV reader.
"""

from unittest.mock import patch

from src.pipeline.s3_reader import read_csv_from_s3


def test_read_csv_from_s3():
    """S3 CSV content should be converted into dictionaries."""

    csv_content = (
        "InvoiceNo,Quantity,UnitPrice\n"
        "536365,6,2.55\n"
        "536366,2,5.00\n"
    )

    mock_response = {
        "Body": MockBody(csv_content)
    }

    with patch(
        "src.pipeline.s3_reader.s3_client.get_object",
        return_value=mock_response
    ):

        result = read_csv_from_s3(
            "sales-pipeline-v2",
            "raw/online_retail.csv"
        )

    assert len(result) == 2
    assert result[0]["InvoiceNo"] == "536365"
    assert result[0]["Quantity"] == "6"
    assert result[0]["UnitPrice"] == "2.55"


class MockBody:
    """Mock S3 response body for testing."""

    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content.encode("utf-8")

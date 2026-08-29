"""
Tests for S3 event handling.
"""

from src.pipeline.lambda_function import get_s3_object_details


def test_get_s3_object_details():
    """S3 event should return the correct bucket and object key."""

    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "sales-pipeline-v2"
                    },
                    "object": {
                        "key": "raw/online_retail.csv"
                    }
                }
            }
        ]
    }

    bucket, key = get_s3_object_details(event)

    assert bucket == "sales-pipeline-v2"
    assert key == "raw/online_retail.csv"


def test_s3_object_key_is_decoded():
    """URL-encoded S3 object keys should be decoded."""

    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "sales-pipeline-v2"
                    },
                    "object": {
                        "key": "raw/sales%20data.csv"
                    }
                }
            }
        ]
    }

    bucket, key = get_s3_object_details(event)

    assert bucket == "sales-pipeline-v2"
    assert key == "raw/sales data.csv"

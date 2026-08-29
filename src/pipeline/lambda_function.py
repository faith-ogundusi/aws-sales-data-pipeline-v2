"""
AWS Lambda entry point for the AWS Sales Data Pipeline V2.

The Lambda function coordinates S3 event handling,
validation, and processing of sales records.
"""

from urllib.parse import unquote_plus

from src.pipeline.processor import process_record
from src.pipeline.validator import validate_record


def process_sales_record(record):
    """
    Validate and process a single sales record.

    Args:
        record (dict): Raw sales record.

    Returns:
        dict: Processed valid record or rejected record
        with a rejection reason.
    """

    validation_result = validate_record(record)

    if not validation_result["is_valid"]:
        rejected_record = record.copy()
        rejected_record["ValidationStatus"] = "REJECTED"
        rejected_record["RejectionReason"] = validation_result["reason"]

        return rejected_record

    return process_record(record)


def get_s3_object_details(event):
    """
    Extract the S3 bucket and object key from an S3 event.

    Args:
        event (dict): S3 event notification.

    Returns:
        tuple: Bucket name and object key.
    """

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = unquote_plus(record["s3"]["object"]["key"])

    return bucket, key


def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    Extracts S3 object information from the event.
    """

    bucket, key = get_s3_object_details(event)

    print(f"Processing file: s3://{bucket}/{key}")

    return {
        "statusCode": 200,
        "bucket": bucket,
        "key": key,
        "message": "S3 event received successfully."
    }

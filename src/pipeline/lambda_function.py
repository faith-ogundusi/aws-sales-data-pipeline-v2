"""
AWS Lambda entry point for the AWS Sales Data Pipeline V2.

The Lambda function coordinates validation and processing
of individual sales records.
"""

from src.pipeline.processor import process_record
from src.pipeline.validator import validate_record


def process_sales_record(record):
    """
    Validate and process a single sales record.

    Args:
        record (dict): Raw sales record.

    Returns:
        dict: Processed record with validation status,
        or rejected record with a rejection reason.
    """

    validation_result = validate_record(record)

    if not validation_result["is_valid"]:
        rejected_record = record.copy()
        rejected_record["ValidationStatus"] = "REJECTED"
        rejected_record["RejectionReason"] = validation_result["reason"]

        return rejected_record

    return process_record(record)


def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    The S3 event integration will be implemented
    in a later stage.
    """

    return {
        "statusCode": 200,
        "body": "Sales pipeline Lambda is ready."
    }

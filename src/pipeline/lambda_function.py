"""
AWS Lambda entry point for the AWS Sales Data Pipeline V2.

The Lambda function coordinates S3 event handling,
validation, and processing of sales records.
"""

from urllib.parse import unquote_plus

from src.pipeline.processor import process_record
from src.pipeline.validator import validate_record
from src.pipeline.s3_reader import read_csv_from_s3
from src.pipeline.s3_writer import write_csv_to_s3


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

def process_records(records):
    """
    Validate and process a collection of sales records.

    Args:
        records (list): Sales records read from the source CSV.

    Returns:
        tuple: Lists containing valid and rejected records.
    """

    valid_records = []
    rejected_records = []

    for record in records:
        result = process_sales_record(record)

        if result["ValidationStatus"] == "VALID":
            valid_records.append(result)
        else:
            rejected_records.append(result)

    return valid_records, rejected_records

def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    Reads a CSV file from S3, processes its records,
    and writes valid and rejected records back to S3.
    """

    bucket, key = get_s3_object_details(event)

    print(f"Processing file: s3://{bucket}/{key}")

    records = read_csv_from_s3(bucket, key)

    valid_records, rejected_records = process_records(records)

    print(f"Valid records: {len(valid_records)}")
    print(f"Rejected records: {len(rejected_records)}")

    valid_key = "valid/valid_sales.csv"
    rejected_key = "rejected/rejected_sales.csv"

    write_csv_to_s3(
        bucket,
        valid_key,
        valid_records
    )

    write_csv_to_s3(
        bucket,
        rejected_key,
        rejected_records
    )

    return {
        "statusCode": 200,
        "bucket": bucket,
        "source_key": key,
        "valid_records": len(valid_records),
        "rejected_records": len(rejected_records),
        "valid_output": valid_key,
        "rejected_output": rejected_key,
    }

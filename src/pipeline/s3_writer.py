"""
Amazon S3 output writer for the AWS Sales Data Pipeline V2.

This module handles writing processed sales records
back to Amazon S3 as CSV files.
"""

import csv
import io

import boto3


s3_client = boto3.client("s3")


def write_csv_to_s3(bucket, key, records):
    """
    Write a list of records to Amazon S3 as a CSV file.

    Args:
        bucket (str): S3 bucket name.
        key (str): Destination object key.
        records (list): Records to write.

    Returns:
        str: S3 URI of the written object.
    """

    if not records:
        return None

    output = io.StringIO()

    fieldnames = list(records[0].keys())

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(records)

    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=output.getvalue().encode("utf-8"),
        ContentType="text/csv"
    )

    return f"s3://{bucket}/{key}"

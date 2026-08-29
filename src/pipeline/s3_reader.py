"""
Amazon S3 data reader for the AWS Sales Data Pipeline V2.

This module handles reading CSV files stored in Amazon S3.
"""

import csv
import io

import boto3


s3_client = boto3.client("s3")


def read_csv_from_s3(bucket, key):
    """
    Read a CSV file from Amazon S3.

    Args:
        bucket (str): S3 bucket name.
        key (str): S3 object key.

    Returns:
        list: CSV records represented as dictionaries.
    """

    response = s3_client.get_object(
        Bucket=bucket,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    reader = csv.DictReader(io.StringIO(file_content))

    return list(reader)

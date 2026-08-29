"""
Data processing module for the AWS Sales Data Pipeline V2.

This module contains transformation logic applied to
validated sales records.
"""


def process_record(record):
    """
    Transform a validated sales record.

    Adds calculated revenue and validation status.

    Args:
        record (dict): A validated sales record.

    Returns:
        dict: The transformed sales record.
    """

    processed_record = record.copy()

    quantity = float(processed_record["Quantity"])
    unit_price = float(processed_record["UnitPrice"])

    processed_record["Quantity"] = quantity
    processed_record["UnitPrice"] = unit_price
    processed_record["Revenue"] = round(quantity * unit_price, 2)
    processed_record["ValidationStatus"] = "VALID"

    return processed_record

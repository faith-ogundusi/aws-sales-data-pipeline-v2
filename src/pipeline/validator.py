"""
Data validation module for the AWS Sales Data Pipeline V2.

This module contains the rules used to determine whether
individual sales records are valid or rejected.
"""

REQUIRED_FIELDS = [
    "InvoiceNo",
    "Quantity",
    "UnitPrice",
]


def validate_record(record):
    """
    Validate a single sales record.

    Returns:
        True if the record passes all validation rules.
        False if the record fails any validation rule.
    """

    if not record:
        return False

    # Check that all required fields exist and contain values.
    for field in REQUIRED_FIELDS:
        if field not in record or record[field] in (None, ""):
            return False

    # Validate numeric fields.
    try:
        quantity = float(record["Quantity"])
        unit_price = float(record["UnitPrice"])
    except (TypeError, ValueError):
        return False

    # Business validation rules.
    if quantity <= 0:
        return False

    if unit_price <= 0:
        return False

    return True

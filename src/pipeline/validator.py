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
        dict: Validation result containing:
            - is_valid: True or False
            - reason: None when valid, otherwise the rejection reason
    """

    if not record:
        return {
            "is_valid": False,
            "reason": "Record is empty",
        }

    # Check required fields.
    for field in REQUIRED_FIELDS:
        if field not in record or record[field] in (None, ""):
            return {
                "is_valid": False,
                "reason": f"{field} is missing",
            }

    # Validate numeric fields.
    try:
        quantity = float(record["Quantity"])
        unit_price = float(record["UnitPrice"])
    except (TypeError, ValueError):
        return {
            "is_valid": False,
            "reason": "Quantity and UnitPrice must be numeric",
        }

    # Business validation rules.
    if quantity <= 0:
        return {
            "is_valid": False,
            "reason": "Quantity must be greater than zero",
        }

    if unit_price <= 0:
        return {
            "is_valid": False,
            "reason": "UnitPrice must be greater than zero",
        }

    return {
        "is_valid": True,
        "reason": None,
    }

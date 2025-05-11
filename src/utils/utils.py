from datetime import datetime
from decimal import Decimal

def make_json_serializable(data: list):
    """
    Converts a list of flat dictionaries to make it JSON-serializable in-place.
    - Datetime objects are formatted as "%Y-%m-%d %H:%M:%S".
    - Decimal values are formatted with 2 digits after the comma.

    Args:
        data (list): List of dictionaries to be transformed.
    """
    for item in data:
        for key, value in item.items():
            if isinstance(value, datetime):
                item[key] = value.strftime("%Y-%m-%d")
            elif isinstance(value, Decimal):
                item[key] = round(float(value), 2)
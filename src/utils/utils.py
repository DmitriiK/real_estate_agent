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

def safe_format(value_to_format: str, **kwargs) -> str:
    """
    Safely formats a string with curly-braced variables without raising an exception
    if some variables are missing in kwargs.
    Used for partial formamtting of promts for LLM, I guess in can be done by langchain, but lets's try own implementation.
    Args:
        input_string (str): The string containing curly-braced variables.
        **kwargs: Key-value pairs to replace in the string.

    Returns:
        str: The formatted string with missing variables left as-is.
    """
    class SafeDict(dict):
        def __missing__(self, key):
            return f"{{{key}}}"

    return value_to_format.format_map(SafeDict(**kwargs))

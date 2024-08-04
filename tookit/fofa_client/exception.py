
import re

def extract_error_code(error_message):
    """Extracts the error code from an error message.

    Args:
        error_message (str): The error message.

    Returns:
        str: The extracted error code, or None if no error code is found.
    """
    error_code_pattern = r'\[(-?\d+)\]'
    match = re.search(error_code_pattern, error_message)
    if match:
        return int(match.group(1))
    else:
        return None

class FofaError(Exception):
    """This exception gets raised whenever an error returned by the Fofa API."""
    def __init__(self, message):
        self.message = message
        self.code = extract_error_code(message)

    def __str__(self):
        return self.message

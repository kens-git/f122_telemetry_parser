from typing import Tuple


def to_string(chars: Tuple[int]) -> str:
    """Converts a tuple bytes to a UTF-8 string.

    Args:
        chars: The bytes (uint8 or char) to convert.

    Returns:
        A string containing the non-null characters of chars.
    """
    return bytes(chars).decode('utf-8')

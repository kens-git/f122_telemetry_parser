from typing import Tuple


def to_string(chars: Tuple[int]) -> str:
    """Converts a tuple of single-byte characters to a UTF-8 string.

    Args:
        chars: The chars to convert.

    Returns:
        A plain string containing the non-null characters of the chars.
    """
    return bytes(chars).decode('utf-8')

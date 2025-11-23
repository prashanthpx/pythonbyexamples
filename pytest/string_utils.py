"""Small string utilities module for pytest learning examples."""


def to_upper(text: str) -> str:
    return text.upper()


def to_lower(text: str) -> str:
    return text.lower()


def is_palindrome(text: str) -> bool:
    """Return True if text reads the same forwards and backwards.

    We normalize by lowercasing and stripping spaces at both ends.
    (Later, we could write more complex versions that ignore punctuation,
    spaces in the middle, etc.)
    """
    normalized = text.strip().lower()
    return normalized == normalized[::-1]


def contains_substring(text: str, sub: str) -> bool:
    return sub in text


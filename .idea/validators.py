"""Input validation helpers with type hints and docstrings."""
from __future__ import annotations
from typing import Iterable
from .exceptions import ValidationError

def require_nonempty(text: str, field: str = "value") -> str:
    """Ensure text is not empty/whitespace; return stripped value."""
    if not text or not text.strip():
        raise ValidationError(f"{field} cannot be empty.")
    return text.strip()

def require_digits(text: str, length: int, field: str = "ID") -> str:
    """Ensure text has only digits and exact length."""
    if text is None:
        raise ValidationError(f"{field} is required.")
    s = text.strip()
    if not (len(s) == length and s.isdigit()):
        raise ValidationError(f"{field} must be exactly {length} digits.")
    return s

def require_in(item: str, allowed: Iterable[str], field: str = "value") -> str:
    """Ensure item is one of allowed."""
    allowed_set = set(allowed)
    if item not in allowed_set:
        allowed_list = ", ".join(sorted(allowed_set))
        raise ValidationError(f"{field} must be one of: {allowed_list}.")
    return item

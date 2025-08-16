"""Custom exceptions for the Voting App."""
class ValidationError(Exception):
    """User input failed validation."""
class PersistenceError(Exception):
    """Storage layer error."""

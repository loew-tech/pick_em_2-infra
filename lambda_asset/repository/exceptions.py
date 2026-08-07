class RepositoryError(Exception):
    """Base exception for repository errors."""


class ItemNotFoundError(RepositoryError):
    """Raised when the requested item does not exist."""

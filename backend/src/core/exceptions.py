from enum import StrEnum


class ErrorMessage(StrEnum):
    LOGIN_ALREADY_REGISTERED = "Login is already registered"
    INVALID_LOGIN_OR_PASSWORD = "Invalid login or password"  # noqa: S105
    INVALID_OR_EXPIRED_TOKEN = "Invalid or expired token"  # noqa: S105
    INVALID_TOKEN_TYPE = "Invalid token type"  # noqa: S105
    INVALID_ACCESS_TOKEN = "Invalid access token"  # noqa: S105
    INVALID_TOKEN_SUBJECT = "Invalid token subject"  # noqa: S105
    REFRESH_TOKEN_INACTIVE = "Refresh token is no longer active"  # noqa: S105
    BEARER_TOKEN_REQUIRED = "Bearer token is required"  # noqa: S105
    REFRESH_TOKEN_REQUIRED = "Refresh token is required"  # noqa: S105
    TODO_NOT_FOUND = "Todo item not found"
    TODO_TITLE_LENGTH = "Todo title must contain between 1 and 200 characters"
    INVALID_TODO_FIELDS = "Todo title and is_done must be valid values"
    TODO_FIELDS_REQUIRED = "At least one todo field must be provided"
    TITLE_CANNOT_BE_NULL = "Title cannot be null"
    TITLE_CANNOT_BE_EMPTY = "Title cannot be empty"
    TODO_UPDATE_REQUIRED = "At least one field must be provided"


class DomainError(Exception):
    def __init__(self, message: str | ErrorMessage) -> None:
        self.message = message
        super().__init__(message)


class UnauthorizedError(DomainError):
    pass


class ForbiddenError(DomainError):
    pass


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class InvalidInputError(DomainError):
    pass

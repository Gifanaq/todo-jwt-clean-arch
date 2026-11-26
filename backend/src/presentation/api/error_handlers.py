from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import (
    ConflictError,
    DomainError,
    ForbiddenError,
    InvalidInputError,
    NotFoundError,
    UnauthorizedError,
)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def handle_domain_error(
        request: Request,
        error: DomainError,
    ) -> JSONResponse:
        del request
        if isinstance(error, UnauthorizedError):
            status_code = 401
        elif isinstance(error, ForbiddenError):
            status_code = 403
        elif isinstance(error, NotFoundError):
            status_code = 404
        elif isinstance(error, ConflictError):
            status_code = 409
        elif isinstance(error, InvalidInputError):
            status_code = 422
        else:
            status_code = 400
        return JSONResponse(
            status_code=status_code,
            content={"detail": error.message},
        )

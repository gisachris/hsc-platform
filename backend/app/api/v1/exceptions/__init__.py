from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class APIException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(message)


class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message, status_code=status.HTTP_404_NOT_FOUND
        )


class UnauthorizedException(APIException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message, status_code=status.HTTP_401_UNAUTHORIZED
        )


class ForbiddenException(APIException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message, status_code=status.HTTP_403_FORBIDDEN
        )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
                "errors": exc.errors,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Validation error occurred",
                "data": None,
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        # In production, do not leak DB internals.
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Database transaction failed",
                "data": None,
                "errors": str(exc) if app.debug else None,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "An unexpected error occurred",
                "data": None,
                "errors": str(exc) if app.debug else None,
            },
        )

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from exceptions import DoesNotExistError, ValidationError


async def not_found_error_handler(request: Request, exception: DoesNotExistError):
    return JSONResponse(
        content={"detail": str(exception.detail)},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def validation_error_handler(request: Request, exception: ValidationError):
    return JSONResponse(content={exception.field: exception.messages}, status_code=status.HTTP_400_BAD_REQUEST)


async def pydantic_validation_error_handler(request: Request, exception: PydanticValidationError):
    errors = [
        {  # do not include values from `ctx` because it's not JSON serializable
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
        }
        for error in exception.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "detail": errors,
        },
    )

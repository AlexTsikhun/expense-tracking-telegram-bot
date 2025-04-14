from fastapi import FastAPI
from pydantic import ValidationError as PydanticValidationError

from error_handlers import not_found_error_handler, pydantic_validation_error_handler, validation_error_handler
from exceptions import DoesNotExistError, ValidationError
from expenses_management.routers import expenses

application = FastAPI(
    title="Expenses Management Application API",
    root_path="/api/v1",
)

application.include_router(expenses.router)

application.add_exception_handler(DoesNotExistError, not_found_error_handler)
application.add_exception_handler(ValidationError, validation_error_handler)
application.add_exception_handler(PydanticValidationError, pydantic_validation_error_handler)

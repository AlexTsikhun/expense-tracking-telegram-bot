from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class ExpenseBaseSchema(BaseModel):
    title: str
    amount_uah: float

    @field_validator("amount_uah")
    @classmethod
    def validate_amount_uah(cls, value):
        if value <= 0:
            raise ValueError("amount must be greater than 0")
        return value


class ExpenseCreateSchema(ExpenseBaseSchema):
    pass


class ExpenseUpdateSchema(ExpenseBaseSchema):
    title: str
    amount_uah: float


class ExpenseResponseSchema(ExpenseBaseSchema):
    id: int
    amount_usd: float
    date: str

    model_config = ConfigDict()


class ExpensesFiltersSchema(BaseModel):
    start_date: str | None = None
    end_date: str | None = None

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, value):
        if value:
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value

    @model_validator(mode="after")
    def validate_dates(self):
        start_date = self.start_date
        end_date = self.end_date

        if start_date and end_date and end_date < start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        
        return self

from pydantic import BaseModel


class ExpenseBaseSchema(BaseModel):
    title: str
    amount_uah: float


class ExpenseCreateSchema(ExpenseBaseSchema):
    pass


class ExpenseUpdateSchema(ExpenseBaseSchema):
    title: str
    amount_uah: float


class ExpenseResponseSchema(ExpenseBaseSchema):
    id: int
    amount_usd: float
    date: str  # ?

    class Config:
        orm_mode = True


class ExpensesFiltersSchema(BaseModel):
    start_date: str | None = None
    end_date: str | None = None

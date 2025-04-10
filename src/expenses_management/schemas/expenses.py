from pydantic import BaseModel


class ExpenseCreateSchema(BaseModel):
    title: str
    amount_uah: float
    date: str  # "dd.mm.YYYY"


class ExpenseUpdateSchema(BaseModel):
    title: str
    amount_uah: float


class ExpenseResponseSchema(BaseModel):
    id: int
    title: str
    amount_uah: float
    amount_usd: float
    date: str  # "dd.mm.YYYY"

    class Config:
        orm_mode = True

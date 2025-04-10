from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_unit_of_work
from expenses_management.schemas.expenses import ExpenseCreateSchema, ExpenseResponseSchema, ExpenseUpdateSchema
from expenses_management.use_cases.expenses import (
    CreateExpenseUseCase,
    DeleteExpenseUseCase,
    RetrieveExpensesUseCase,
    UpdateExpenseUseCase,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=list[ExpenseResponseSchema])
async def retrieve_expenses(start_date: str = None, end_date: str = None, uow=Depends(get_unit_of_work)):
    use_case = RetrieveExpensesUseCase(uow)
    return await use_case(start_date=start_date, end_date=end_date)


@router.post("/", response_model=dict)
async def create_expense(expense: ExpenseCreateSchema, uow=Depends(get_unit_of_work)):
    use_case = CreateExpenseUseCase(uow)
    return await use_case(expense.title, expense.amount_uah, expense.date)


@router.delete("/{expense_id}", response_model=dict)
async def delete_expense(expense_id: int, uow=Depends(get_unit_of_work)):
    use_case = DeleteExpenseUseCase(uow)
    try:
        return await use_case(expense_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{expense_id}", response_model=dict)
async def update_expense(expense_id: int, expense: ExpenseUpdateSchema, uow=Depends(get_unit_of_work)):
    use_case = UpdateExpenseUseCase(uow)
    try:
        return await use_case(expense_id, expense.title, expense.amount_uah)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

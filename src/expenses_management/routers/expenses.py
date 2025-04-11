from fastapi import APIRouter, Depends, status

from dependencies import get_unit_of_work
from expenses_management.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseResponseSchema,
    ExpensesFiltersSchema,
    ExpenseUpdateSchema,
)
from expenses_management.use_cases.expenses import (
    CreateExpenseUseCase,
    DeleteExpenseUseCase,
    RetrieveExpensesUseCase,
    UpdateExpenseUseCase,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=list[ExpenseResponseSchema])
async def retrieve_expenses(filters: ExpensesFiltersSchema = Depends(), uow=Depends(get_unit_of_work)):
    use_case = RetrieveExpensesUseCase(uow)
    return await use_case(filters.model_dump())


@router.post("/", response_model=dict)
async def create_expense(expense: ExpenseCreateSchema, uow=Depends(get_unit_of_work)):
    use_case = CreateExpenseUseCase(uow)
    return await use_case(expense.model_dump())


@router.put("/{expense_id}", response_model=dict)
async def update_expense(expense_id: int, expense: ExpenseUpdateSchema, uow=Depends(get_unit_of_work)):
    use_case = UpdateExpenseUseCase(uow)
    return await use_case(expense_id, expense.model_dump())


@router.delete("/{expense_id}",response_model=dict)
async def delete_expense(expense_id: int, uow=Depends(get_unit_of_work)):
    use_case = DeleteExpenseUseCase(uow)
    return await use_case(expense_id)

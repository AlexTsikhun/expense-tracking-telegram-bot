from sqlalchemy import Column, Date, Integer, Numeric, String, func

from expenses_management import Base


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    amount_uah = Column(Numeric(10, 2), nullable=False)
    amount_usd = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, default=func.current_date(), index=True)

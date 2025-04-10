from sqlalchemy import Column, Date, Float, Integer, String

from expenses_management import Base


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount_uah = Column(Float)
    amount_usd = Column(Float)
    date = Column(Date)

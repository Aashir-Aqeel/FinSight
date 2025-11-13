from pydantic import BaseModel
from datetime import datetime


class Expense(BaseModel):
    title: str
    amount: float
    category: str
    date: datetime
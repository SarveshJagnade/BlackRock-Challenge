from pydantic import BaseModel, Field
from datetime import datetime
from typing import List



class Expense(BaseModel):
    timestamp: datetime
    amount: float = Field(gt=0)


class Transaction(BaseModel):
    date: datetime
    amount: float
    ceiling: float
    remanent: float


class TransactionValidatorRequest(BaseModel):
    wage: float
    transactions: List[Transaction]
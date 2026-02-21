from pydantic import BaseModel
from typing import List


class ReturnsRequest(BaseModel):
    age: int
    wage: float
    inflation: float
    q: List
    p: List
    k: List
    transactions: List
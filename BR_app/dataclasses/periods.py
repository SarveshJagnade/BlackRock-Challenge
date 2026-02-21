from pydantic import BaseModel
from datetime import datetime
from typing import List


class QPeriod(BaseModel):
    fixed: float
    start: datetime
    end: datetime


class PPeriod(BaseModel):
    extra: float
    start: datetime
    end: datetime


class KPeriod(BaseModel):
    start: datetime
    end: datetime


class TemporalRequest(BaseModel):
    q: List[QPeriod]
    p: List[PPeriod]
    k: List[KPeriod]
    transactions: List
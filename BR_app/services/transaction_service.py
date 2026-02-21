import math
from typing import List
from BR_app.dataclasses.transaction import Expense, Transaction 


class TransactionService:
    def __init__(self):
        pass

    async def parse_transactions(self,expenses: List[Expense]) -> List[Transaction]:
        try :
            result = [] 
            for exp in expenses:
                ceiling = math.ceil(exp.amount / 100) * 100
                remanent = ceiling - exp.amount

                result.append(
                    Transaction(
                        date=exp.timestamp,
                        amount=exp.amount,
                        ceiling=ceiling,
                        remanent=remanent
                    )
                )

            return result
        except Exception as e :
            raise e
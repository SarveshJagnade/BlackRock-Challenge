from BR_app.dataclasses.transaction import Expense
from BR_app.services.transaction_service import TransactionService
from fastapi.responses import JSONResponse
 

class Transaction:
    def __init__(self):
        self.transaction_service = TransactionService()
 
    async def parse_transactions(self,expenses: list[Expense]):
        try : 
            return await self.transaction_service.parse_transactions(expenses)
        except Exception as e :
            return JSONResponse(content={"message": f"{str(e)}"},status_code=500)
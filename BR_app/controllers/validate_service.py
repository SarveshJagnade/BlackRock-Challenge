from BR_app.dataclasses.transaction import TransactionValidatorRequest  
from BR_app.services.validation_service import ValidationService
from fastapi.responses import JSONResponse
 
class Validation:
    def __init__(self):
        self.val_service = ValidationService() 

    async def validate_transactions(self,request: TransactionValidatorRequest):
        try : 
            return await self.val_service.validate_transactions( request.wage,request.transactions)
        except Exception as e : 
            return JSONResponse(content={"message": f"{str(e)}"},status_code=500)
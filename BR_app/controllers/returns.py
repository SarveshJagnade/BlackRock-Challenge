 
from BR_app.dataclasses.returns import ReturnsRequest
from BR_app.services.temporal_service import TemporalService
from BR_app.services.return_service import ReturnService
from fastapi.responses import JSONResponse


class Returns:
    def __init__(self):
        self.return_service = ReturnService()
        self.temp_service = TemporalService()
    
    async def calculate_index(self,request):
        try : 
            return await self.return_service.calculate_index_returns(request)
        except Exception as e : 
            return JSONResponse(content={"message": f"{str(e)}"},status_code=500)
    async def calculate_nps(self, request: ReturnsRequest):
        try :
            result = []  
            tx = await self.temp_service.apply_temporal_rules(
                request.transactions,
                request.q,
                request.p
            ) 
            grouped = await self.temp_service.group_by_k(tx, request.k)  
            for g in grouped:
                real_value = await self.return_service.calculate_returns(  g["amount"],request.age, request.inflation, self.return_service.NPS_RATE)

                tax = await self.return_service.calculate_nps_tax(request.wage, g["amount"]) 
                result.append({ **g,"return": real_value,"taxBenefit": tax}) 
            return result
        except Exception as e :
            import traceback
            traceback.print_exc()
            return JSONResponse(content={"message": f"{str(e)}"},status_code=500)
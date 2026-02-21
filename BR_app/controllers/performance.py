import time 
from BR_app.services.performance_service import PerformanceService
from fastapi.responses import JSONResponse

start_time = time.time()

class Performance:
    def __init__(self):
        pass

    async def performance(self):
        try :
            return await PerformanceService.get_metrics(start_time)
        except Exception as e :
            return JSONResponse(content={"message": f"{str(e)}"},status_code=500) 
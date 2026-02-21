from fastapi import Request
from fastapi.responses import JSONResponse


class HealthCheck():
    def __init__(self):
        super().__init__()

    async def health_check(self,request: Request):
        return JSONResponse({"message": "Server is running", "status": 200}, status_code=200)
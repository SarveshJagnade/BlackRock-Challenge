from fastapi import Request
from fastapi.responses import JSONResponse
from config.settings import settings

async def check_allowed_hosts(request: Request, call_next):
    host = request.headers.get("host", "").split(":")[0]
    if "*" in settings.ALLOWED_HOSTS or host in settings.ALLOWED_HOSTS:
        return await call_next(request)
    
    return JSONResponse(content={"error": "Host not allowed"}, status_code=403)

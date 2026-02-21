
import logging
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class CustomLoggerMiddleware(BaseHTTPMiddleware):
    def _init_(self, app):
        super()._init_(app)
        self.logger = logging.getLogger("fastapi_requests")

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        headers = request.headers
        self.logger.info(None, extra={
            "HTTP_HOST": headers.get("host"),
            "HTTP_X_AMZN_TRACE_ID": headers.get("x-amzn-trace-id"),
            "CONTENT_LENGTH": headers.get("content-length"),
            "uagent": headers.get("user-agent"),
            "HTTP_ACCEPT_LANGUAGE": headers.get("accept-language"),
            "http_cf_connecting_ip": headers.get("cf-connecting-ip"),
            "HTTP_CACHE_CONTROL": headers.get("cache-control"),
            "HTTP_COOKIE": headers.get("cookie"),
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "proto": headers.get("x-forwarded-proto"),
            "uri": str(request.url),
            "secs": "sec",
        })
        return response

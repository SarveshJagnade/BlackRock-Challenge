

import importlib
from config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware 

def setup_middlewares(app):
    
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=settings.ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    if settings.MIDDLEWARES:
        for middleware_path in settings.MIDDLEWARES:
            module_name, class_or_func = middleware_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            middleware = getattr(module, class_or_func)

            if isinstance(middleware, type) and issubclass(middleware, BaseHTTPMiddleware):
                app.add_middleware(middleware)
            else:
                app.middleware("http")(middleware)
import os
from pathlib import Path 


class settings:
    BASE_FIR = Path(__file__).resolve().parent.parent

    BASE_URL = "http://127.0.0.1:8000/"

    ALLOWED_HOSTS = [
        "http://localhost:8000"
    ]
    ALLOWED_METHODS = ["*"]
    ALLOWED_HEADERS = ["*"]
    ALLOWED_CREDENTIALS = True

    MIDDLEWARES = [
        # "BR_app.middlewares.custom_logger_middleware.CustomLoggerMiddleware"
    ]

    DATABASES = {
        "default_db": {
            "ENGINE": "postgresql+asyncpg",
            "HOST": "localhost",
            "PORT": 5432,
            "NAME":  "investment_db",
            "USER": "postgres",
            "PASSWORD": "root",
        },
    }

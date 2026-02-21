from fastapi import FastAPI
from BR_app.urls import app_router
from BR_app.middlewares.setup import setup_middlewares
from config.database.database import db_manager

async def lifespan(app:FastAPI):
    await db_manager.validate_connections()
    yield

app = FastAPI(title = 'BlackRockAPI', lifespan=lifespan,docs_url="/docs", redoc_url="/redocs")
app.include_router(app_router,prefix="/blackrock/challenge/v1")
setup_middlewares(app)
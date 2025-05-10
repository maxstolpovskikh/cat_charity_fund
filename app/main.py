from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser, create_db_and_tables

app = FastAPI(title=settings.app_title)

app.include_router(main_router)

@app.on_event('startup')
async def on_startup():
    await create_db_and_tables()

@app.on_event('startup')
async def startup():
    await create_first_superuser()

import os

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.routers import main_router
from app.core.config import configure_logging, settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION)
FILES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload')
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    add_pagination(app)
    configure_logging()
    await create_first_superuser()

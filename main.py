from fastapi import FastAPI

from core.config import settings
from core.event import app_init

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESC,
    version=settings.APP_VERSION,
    debug=settings.APP_DEBUG,
    openapi_url=f'{settings.APP_API_PREFIX}/openapi.json'
)
app_init(app)

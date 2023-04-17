from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.crud import router as crud_router
from app.api.v1.proxy import router as proxy_router
from app.core.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
app.include_router(proxy_router, prefix="/api/v1/proxy")
app.include_router(crud_router, prefix="/api/v1")

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.docs import custom_openapi
from app.api.middleware.auth_middleware import AuthMiddleware
from app.api.v1.auth_router import router as auth_router
from app.api.v1.production_router import router as production_router
from app.api.v1.commercialization_router import router as commercialization_router
from app.api.v1.importing_router import router as importing_router
from app.api.v1.exporting_router import router as exporting_router
from app.api.v1.processing_router import router as processing_router
from app.core.config import settings
from app.core.logging_config import setup_logging


def create_app() -> FastAPI:
    # Configura logger
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting app in {settings.env} environment")

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        docs_url="/docs" if settings.env != "production" else None,
    )

    # Middlewares (CORS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        AuthMiddleware,
        allowed_paths=["/v1/auth/login", "/v1/auth/refresh", "/docs", "/openapi.json"],
    )
    # Routers
    app.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
    app.include_router(production_router, prefix="/v1/production", tags=["production"])
    app.include_router(processing_router, prefix="/v1/processing", tags=["processing"])
    app.include_router(
        commercialization_router,
        prefix="/v1/commercialization",
        tags=["commercialization"],
    )
    app.include_router(importing_router, prefix="/v1/importing", tags=["importing"])
    app.include_router(exporting_router, prefix="/v1/exporting", tags=["exporting"])
    app.openapi_schema = custom_openapi(app)

    return app

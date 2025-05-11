import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.middleware.auth_middleware import AuthMiddleware
from app.api.v1.auth_router import router as auth_router
from app.api.v1.production_router import router as production_router
from app.core.config import settings
from app.core.logging_config import setup_logging


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Minha API",
        version="1.0.0",
        description="API protegida com Bearer Token",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }

    # Adiciona a autenticação como requisito global (opcional)
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


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
    # app.include_router(user_router.router, prefix="/v1", tags=["users"])
    app.openapi_schema = custom_openapi(app)

    return app

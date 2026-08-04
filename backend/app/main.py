from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analytics import router as analytics_router
from app.api.routes.auth import router as auth_router
from app.api.routes.github import router as github_router
from app.api.routes.health import router as health_router
from app.api.routes.search import router as search_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.webhooks import router as webhooks_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import engine
from app.models import organization, repository, review, user  # noqa: F401


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()
    if settings.app_env != "production":
        Base.metadata.create_all(bind=engine)

    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router, prefix=settings.api_v1_prefix)
    app.include_router(auth_router, prefix=settings.api_v1_prefix)
    app.include_router(reviews_router, prefix=settings.api_v1_prefix)
    app.include_router(search_router, prefix=settings.api_v1_prefix)
    app.include_router(github_router, prefix=settings.api_v1_prefix)
    app.include_router(webhooks_router, prefix=settings.api_v1_prefix)
    app.include_router(analytics_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()

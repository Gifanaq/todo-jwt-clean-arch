from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import Settings, get_settings
from src.core.logging import configure_logging
from src.presentation.api.error_handlers import register_error_handlers
from src.presentation.api.routes import auth_router, todos_router


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    configure_logging()
    app = FastAPI(title="TODO JWT Clean Architecture", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    register_error_handlers(app)
    app.include_router(auth_router)
    app.include_router(todos_router)
    return app


app = create_app()

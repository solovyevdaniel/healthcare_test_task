from fastapi import FastAPI
from api import routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Healthcare Test Task API",
    )

    app.include_router(routers.api_router)
    return app

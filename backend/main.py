import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base
from backend.routes import sessions, starters, factcheck, history

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
    yield
    logger.info("Shutting down Personalized Networking Assistant.")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Personalized Networking Assistant",
        description="AI-powered networking conversation starter generator with fact-checking.",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(sessions.router)
    app.include_router(starters.router)
    app.include_router(factcheck.router)
    app.include_router(history.router)

    @app.get("/")
    def root():
        return {"message": "Personalized Networking Assistant API", "status": "running"}

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

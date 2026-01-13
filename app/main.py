import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import app
from app.config.config import settings
from app.config.logging_config import get_logger, setup_logging
from app.db.database import db_manager
from app.routers import resume_chat

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Setup Logging
    setup_logging()
    logger.info("Starting AI-python enterprise application...")

    # 2. Connect to MongoDB (reads DATABASE_URL from .env)
    try:
        await db_manager.connect(settings.database_url)
        logger.info("Database connection established.")
    except Exception as e:
        logger.critical(f"Failed to connect to database: {e}")
        raise e

    yield

    # 3. Shutdown
    logger.info("Shutting down application...")
    db_manager.close()


# Create the FastAPI instance
app = FastAPI(title="Resume AI Analytics API", version="1.0.0", lifespan=lifespan)

# Register Routers
app.include_router(resume_chat.router, prefix="/ai-demo", tags=["Resume Chat"])

if __name__ == "__main__":
    import uvicorn

    # This matches the 'uvicorn app.main:app' command
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)

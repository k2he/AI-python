import os

from app.config.config import settings
from app.config.logging_config import get_logger

logger = get_logger(__name__)


def setup_langsmith_tracing():
    os.environ["LANGSMITH_TRACING"] = str(settings.langsmith_tracing).lower()
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project

    logger.info("LangSmith tracing configured.")

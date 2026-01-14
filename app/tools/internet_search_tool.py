from langchain_core.tools import tool
from tavily import TavilyClient

from app.config.config import settings
from app.config.logging_config import get_logger

logger = get_logger(__name__)


@tool
def internet_search(query: str) -> str:
    """Use this tool to search the internet for relevant information."""
    try:
        search_tool = TavilyClient(api_key=settings.tavily_api_key)

        results = search_tool.search(query)
        logger.info(f"Internet search results for query '{query}': {results}")
        return results
    except Exception as e:
        logger.error(f"Error during internet search: {e}")
        return "An error occurred while performing the internet search."

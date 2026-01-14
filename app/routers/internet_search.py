from fastapi import APIRouter, HTTPException
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.config.config import settings
from app.config.logging_config import get_logger
from app.schemas.internet_search import InternetSearchRequest, InternetSearchResponse
from app.tools import internet_search

# Initialize the router and a logger specific to this module
router = APIRouter()
logger = get_logger(__name__)


@router.post("/search", response_model=InternetSearchResponse)
async def perform_search(request: InternetSearchRequest):
    try:
        # 1. Initialize the Model (gpt-oss:20b)
        model = init_chat_model(
            model=settings.llm_tools_model,
            model_provider=settings.llm_provider,
            temperature=0,
            think="medium",
        )

        # 2. Setup Tools & Agent
        tools = [internet_search]
        agent = create_agent(model=model, tools=tools)

        # 3. Execute directly
        # The agent will call internet_search if the query requires it
        result = await agent.ainvoke({"messages": [("user", request.question)]})

        return InternetSearchResponse(results=result["messages"][-1].content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

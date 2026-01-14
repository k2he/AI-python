from pydantic import BaseModel, Field


class InternetSearchRequest(BaseModel):
    question: str = Field(..., description="The search query string.")


class InternetSearchResponse(BaseModel):
    results: str

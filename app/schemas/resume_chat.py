from pydantic import BaseModel, Field


class ResumeChatRequest(BaseModel):
    user_id: str = Field(..., description="The unique identifier of the user.")
    question: str = Field(..., description="The question asked by the user.")


class ResumeChatResponse(BaseModel):
    answer: str = Field(..., description="The answer provided by the system.")
    status: str

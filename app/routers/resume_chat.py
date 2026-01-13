from fastapi import APIRouter, Header, HTTPException, status

from app.config.logging_config import get_logger
from app.db.chat_repository import ChatRepository
from app.schemas.resume_chat import ResumeChatRequest, ResumeChatResponse

# Initialize the router and a logger specific to this module
router = APIRouter()
logger = get_logger(__name__)


@router.post("/resume-chat", response_model=ResumeChatResponse)
async def send_resume_chat(request: ResumeChatRequest):
    logger.info(f"Incoming resume chat request from user: {request.user_id}")
    try:
        # Here you would integrate with your AI model to get a response
        response_text = f"Echo: {request.question}"  # Placeholder for AI response

        # Save the chat message and response to the database
        await ChatRepository.save_chat_message(
            request.user_id, request.question, response_text
        )

        logger.info(f"Response sent to user {request.user_id}")
        return ResumeChatResponse(answer=response_text, status="Success")
    except Exception as e:
        logger.error(f"Error processing resume chat for user {request.user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

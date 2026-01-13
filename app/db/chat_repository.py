from datetime import datetime

from app.config.config import settings
from app.config.logging_config import get_logger
from app.db.database import db_manager
from app.schemas.resume_chat import ResumeChatRequest

logger = get_logger(__name__)


class ChatRepository:

    @staticmethod
    async def save_chat_message(user_id: str, question: str, response_text: str):
        try:
            collection = db_manager.db[settings.resume_chat_collection]
            chat_document = {
                "user_id": user_id,
                "message": question,
                "response": response_text,
                "timestamp": datetime.utcnow(),
            }
            result = await collection.insert_one(chat_document)
            logger.info(f"Chat message saved with id: {result.inserted_id}")
        except Exception as e:
            logger.error(f"Database error while saving message for {user_id}: {e}")
            raise

    @staticmethod
    async def get_history(user_id: str, limit: int = 50):
        """
        Retrieves the latest chat history for a specific user.
        """
        try:
            collection = db_manager.db[settings.resume_chat_collection]
            # Find messages, sort by newest first, and convert to list
            cursor = (
                collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
            )
            history = await cursor.to_list(length=limit)

            # Remove MongoDB's '_id' field from results to make it JSON serializable
            for doc in history:
                doc["_id"] = str(doc["_id"])

            return history
        except Exception as e:
            logger.error(f"Database error while fetching history for {user_id}: {e}")
            raise
